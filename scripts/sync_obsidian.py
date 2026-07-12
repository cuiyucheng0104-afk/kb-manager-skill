#!/usr/bin/env python3
"""把项目知识库（.kb/）同步到 Obsidian 仓库。

用法:
    python3 sync_obsidian.py <项目根目录或.kb目录> <Obsidian仓库路径> [--name 项目名] [--dest 目标文件夹]

行为:
    在 <仓库>/<目标文件夹>/<项目名>/ 下生成:
      - <项目名>.md          索引笔记（由 .kb/README.md 转换而来，含 frontmatter 与 wikilink 导航）
      - 其余全部知识库文档    （标准情况下为 10 份主题文档；加 frontmatter，内部链接转为 wikilink；
                              已自带 frontmatter 的文档保持原样，不重复注入）
      - assets/              资源目录原样复制（跳过 .gitkeep）

    转换细节: 代码块内的示例链接不转换；表格内 wikilink 的 | 自动转义为 \\|；
    "> ⏳ 待补充：" 引用块升级为 Obsidian 的 [!todo] callout。

    同步是"只增改不删"的镜像: 每次覆盖上述同步产物（包括你手工改过的同名笔记——
    请把自己的笔记起不同的名字），但不会删除目标文件夹里的其他文件；改过 --name/--dest
    后旧文件夹会残留，需手动清理。同步成功后在 .kb/.obsidian-sync.json 记录目标位置，
    供下次直接复用。可安全重复运行。

    --dest 默认为 "项目知识库"；--name 默认为项目根目录名。
"""
import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote

# 指向本地 .md 文件的相对链接（排除 http(s)、锚点开头、含目录的路径；(?<!!) 排除 ![嵌入] 语法）
MD_LINK = re.compile(r"(?<!!)\[([^\]\[]+)\]\((?!https?://|#)([^)/\s]+\.md)(#[^)]*)?\)")
FENCE = re.compile(r"(```.*?```|~~~.*?~~~)", re.S)
INLINE_CODE = re.compile(r"(`[^`\n]*`)")
PENDING = "> ⏳ 待补充："


def to_wikilink(match: re.Match, prefix: str, in_table: bool) -> str:
    label, target, anchor = match.group(1), unquote(match.group(2)), match.group(3) or ""
    stem = target[:-3]
    head = f"#{anchor.lstrip('#')}" if anchor else ""
    sep = "\\|" if in_table else "|"  # 表格内的 | 必须转义，否则 Obsidian 会拆碎表格列
    # 全路径 wikilink：不同项目共用同名文档（tech-stack.md 等），全路径可避免跨项目歧义
    return f"[[{prefix}/{stem}{head}{sep}{label}]]"


def convert_body(text: str, prefix: str) -> str:
    """转换正文：跳过代码块与行内代码，处理 wikilink 与待补充 callout。"""
    parts = FENCE.split(text)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # 代码围栏原样保留
            out.append(part)
            continue
        lines = []
        for line in part.split("\n"):
            stripped = line.lstrip()
            if stripped.startswith(PENDING):
                content = stripped[len(PENDING):].strip()
                lines.append("> [!todo] 待补充")
                lines.append(f"> {content}")
                continue
            in_table = stripped.startswith("|")
            segs = INLINE_CODE.split(line)
            for j, seg in enumerate(segs):
                if j % 2 == 0:
                    segs[j] = MD_LINK.sub(lambda m: to_wikilink(m, prefix, in_table), seg)
            lines.append("".join(segs))
        out.append("\n".join(lines))
    return "".join(out)


def yaml_scalar(v) -> str:
    return json.dumps(str(v), ensure_ascii=False)  # JSON 字符串是合法 YAML 标量，天然处理引号/冒号/井号


def add_frontmatter(text: str, props: dict) -> str:
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        return text  # 已有 frontmatter 就不重复加
    lines = ["---"]
    for k, v in props.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            lines.extend(f"  - {yaml_scalar(item)}" for item in v)
        else:
            lines.append(f"{k}: {yaml_scalar(v)}")
    lines.append("---\n")
    return "\n".join(lines) + "\n" + text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", help="项目根目录或 .kb 目录")
    ap.add_argument("vault", help="Obsidian 仓库路径")
    ap.add_argument("--name", help="项目名（默认取项目根目录名）")
    ap.add_argument("--dest", default="项目知识库", help='仓库内目标文件夹（默认 "项目知识库"）')
    args = ap.parse_args()

    src = Path(args.source).expanduser().resolve()
    kb = src if src.name == ".kb" else src / ".kb"
    root = kb.parent
    if not kb.is_dir():
        print(f"错误：找不到知识库目录 {kb}（先运行 init_kb.py 初始化）")
        return 1

    vault = Path(args.vault).expanduser().resolve()
    if not (vault / ".obsidian").is_dir():
        print(f"错误：{vault} 不是 Obsidian 仓库（缺少 .obsidian 目录）")
        return 1

    name = args.name or root.name
    if any(s in name for s in ("/", "\\", "..")):
        print(f"错误：项目名不能包含路径分隔符或 '..'：{name}")
        return 1

    doc_stems = {d.stem for d in kb.glob("*.md") if d.name != "README.md"}
    if name in doc_stems:
        print(f"错误：项目名 {name!r} 与知识库文档 {name}.md 同名，索引笔记会被覆盖。请用 --name 换一个名字。")
        return 1

    target = (vault / args.dest / name).resolve()
    if not target.is_relative_to(vault):
        print(f"错误：目标路径逃逸出仓库范围：{target}")
        return 1
    target.mkdir(parents=True, exist_ok=True)

    link_prefix = f"{args.dest}/{name}"
    today = date.today().isoformat()

    synced = []
    for doc in sorted(kb.glob("*.md")):
        text = doc.read_text(encoding="utf-8-sig")
        text = convert_body(text, link_prefix)
        if doc.name == "README.md":
            out = target / f"{name}.md"
            text = add_frontmatter(text, {
                "title": name,
                "tags": ["项目知识库", f"项目知识库/{name}"],
                "source": str(root),
                "synced": today,
            })
        else:
            out = target / doc.name
            text = add_frontmatter(text, {
                "tags": [f"项目知识库/{name}"],
                "synced": today,
            })
        out.write_text(text, encoding="utf-8")
        synced.append(out.name)

    assets = kb / "assets"
    n_assets = 0
    if assets.is_dir():
        for f in assets.rglob("*"):
            if f.is_file() and f.name != ".gitkeep":
                rel = f.relative_to(assets)
                dst = target / "assets" / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                n_assets += 1

    record = {"vault": str(vault), "dest": args.dest, "name": name, "synced": today}
    (kb / ".obsidian-sync.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"已同步到: {target}")
    print(f"笔记 ({len(synced)}): {', '.join(synced)}")
    print(f"资源文件: {n_assets} 个")
    print(f"同步记录: {kb / '.obsidian-sync.json'}")
    print(f"在 Obsidian 中打开 [[{link_prefix}/{name}]] 即可进入导航。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
