#!/usr/bin/env python3
"""初始化项目知识库：把模板复制到 <项目根目录>/.kb/ 并创建 assets 子目录。

用法: python3 init_kb.py <项目根目录>

已存在的文件不会被覆盖，可安全重复运行。
"""
import shutil
import sys
from pathlib import Path

ASSET_SUBDIRS = ["diagrams", "screenshots", "icons"]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    project_root = Path(sys.argv[1]).expanduser().resolve()
    if not project_root.is_dir():
        print(f"错误：项目目录不存在: {project_root}")
        return 1

    templates_dir = Path(__file__).resolve().parent.parent / "assets" / "templates"
    kb_dir = project_root / ".kb"
    kb_dir.mkdir(exist_ok=True)

    created, skipped = [], []
    for template in sorted(templates_dir.glob("*.md")):
        target = kb_dir / template.name
        if target.exists():
            skipped.append(template.name)
        else:
            shutil.copy2(template, target)
            created.append(template.name)

    for sub in ASSET_SUBDIRS:
        sub_dir = kb_dir / "assets" / sub
        sub_dir.mkdir(parents=True, exist_ok=True)
        gitkeep = sub_dir / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()

    print(f"知识库位置: {kb_dir}")
    print(f"新建文档 ({len(created)}): {', '.join(created) if created else '无'}")
    if skipped:
        print(f"已存在、跳过 ({len(skipped)}): {', '.join(skipped)}")
    print(f"资源目录: assets/{{{', '.join(ASSET_SUBDIRS)}}}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
