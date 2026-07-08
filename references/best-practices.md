# 知识库方法论参考

> **何时读这份文件：** 这是 kb-manager 的按需参考资料，汇总各模板背后引用的 8 个方法论的已核实要点与出处。
> 日常初始化、更新知识库时**不必**加载本文件——模板本身已内置这些约定；
> 只在需要向用户解释某条规范的细节、或对模板中某个约定产生疑问时，再查阅对应小节。
> 每节要点均严格取自"来源"链接页面的原文，宁缺毋滥。

## Keep a Changelog（更新日志）

**是什么/为什么。** 更新日志（Change Log）是一个由人工编辑、以时间为倒序的列表，用于记录项目中每个版本的显著变动。它写给人而非机器：直接把 git 日志当更新日志是非常糟糕的方式——git 日志充满合并提交、语焉不详的提交标题、文档更新等无意义信息。

**关键规则。**
- 七条指导原则：日志是写给人而非机器的；每个版本都应该有独立的入口；同类改动应该分组放置；不同版本应分别设置链接；新版本在前，旧版本在后；应包括每个版本的发布日期；注明是否遵守语义化版本规范。
- 六种变动类型（中文页保留英文类型名，只给中文释义）：`Added` 新添加的功能；`Changed` 对现有功能的变更；`Deprecated` 已经不建议使用、即将移除的功能；`Removed` 已经移除的功能；`Fixed` 对 bug 的修复；`Security` 对安全性的改进。
- 在文档最上方提供 `Unreleased` 区块记录即将发布的更新内容。两个好处：大家可以预知未来版本中可能有哪些变更；发布新版本时，直接把 `Unreleased` 区块中的内容移动至新版本的描述区块即可。
- 日期推荐 `2012-06-02` 这种从大到小排列、符合 ISO 标准的格式，不易与其他日期格式混淆。
- 文件通常命名为 `CHANGELOG.md`；也有项目命名为 HISTORY、NEWS 或 RELEASES。

**在本技能中怎么用。** 对应模板 `assets/templates/changelog.md`：`[未发布]` 段就是 Unreleased 区块，工作流二要求每次更新知识库都在其中追加一条；版本条目按上述六种类型分组，日期用 `YYYY-MM-DD`。

**来源**：https://keepachangelog.com/zh-CN/1.1.0/

## Conventional Commits（约定式提交）

**是什么/为什么。** 一套提交信息的书写约定，让提交历史可读、可被工具解析，并与语义化版本（SemVer）直接对应。

**关键规则。**
- 完整结构：`<type>[optional scope]: <description>`，其后可跟可选正文（body）和可选脚注（footer）。
- `fix` 类型表示在代码库中修复了一个 bug，对应 SemVer 的 PATCH；`feat` 类型表示在代码库中新增了一个功能，对应 SemVer 的 MINOR。规范以"必须"级别规定：实现新功能必须用 `feat`，修复 bug 必须用 `fix`。
- 除 `feat`、`fix` 外也可以使用其他类型，例如 @commitlint/config-conventional（基于 Angular 约定）推荐的 `build`、`chore`、`ci`、`docs`、`style`、`refactor`、`perf`、`test`。
- 破坏性变更有两种标记方式，均对应 SemVer 的 MAJOR，且可出现在任意类型的提交中：
  - 脚注方式：必须包含大写的 `BREAKING CHANGE`，后面紧跟冒号、空格和描述；
  - 前缀方式：在 `<类型>(范围)` 后、`:` 之前加 `!`；使用了 `!` 时脚注中可以不写 `BREAKING CHANGE:`，此时提交信息的描述应用于描述破坏性变更。

**在本技能中怎么用。** 对应模板 `assets/templates/dev-standards.md` 的"Commit 信息规范"一节，示例即此格式；扫描项目时如发现提交历史已遵循该约定，应在该节如实记录。

**来源**：https://www.conventionalcommits.org/zh-hans/v1.0.0/

## SemVer（语义化版本 2.0.0）

**是什么/为什么。** 版本号格式与递增规则的规范：版本格式为"主版本号.次版本号.修订号"，让版本号本身传达变更的兼容性含义。

**关键规则。**
- 主版本号（MAJOR）：做了不兼容的 API 修改时递增；每当主版本号递增，次版本号和修订号必须归零。
- 次版本号（MINOR）：有向下兼容的新功能出现时必须递增；任何公共 API 的功能被标记为弃用时也必须递增；每当次版本号递增，修订号必须归零。
- 修订号（PATCH）：必须在只做了向下兼容的修正时才递增——这里的修正指针对不正确结果而进行的内部修改。
- 主版本号为零（0.y.z）表示开发初始阶段，一切都可能随时被改变，公共 API 不应被视为稳定版。
- 与约定式提交的对应（Conventional Commits FAQ）：`fix` 对应 PATCH 版本，`feat` 对应 MINOR 版本，带 `BREAKING CHANGE` 的提交不管类型如何都对应 MAJOR 版本。

**在本技能中怎么用。** 为 `assets/templates/changelog.md` 中的版本号命名提供依据；Keep a Changelog 也要求在日志中注明是否遵守语义化版本规范。

**来源**：https://semver.org/lang/zh-CN/

## ADR（架构决策记录）

**是什么/为什么。** 架构决策（AD）是一个有充分理由的设计选择，针对具有架构显著性的功能性或非功能性需求（即对系统架构与质量有可度量影响的需求）。一条 ADR 记录单个架构决策及其理由，帮助人们理解所选决策的原因及其权衡与后果。项目中创建并维护的全部 ADR 构成该项目的"决策日志"（decision log）。

**关键规则。**
- Nygard 模板由五部分组成：title（标题）、status（状态）、context（上下文）、decision（决策）、consequences（后果）；这一结构出自 Michael Nygard 2011 年的博文《Documenting Architecture Decisions》——正是这篇文章使 ADR 概念普及，五段式模板可在该站的 ADR Templates 子页查到（另有 Markdown 版本可用）。
- ADR 属于架构知识管理（AKM）范畴，用法可以扩展到设计决策及其他类型的决策（"any decision record"）。

**在本技能中怎么用。** 对应模板 `assets/templates/tech-stack.md` 的"技术决策记录"一节：每条按"背景 → 决策 → 后果"记录，即简化版的 context / decision / consequences；按时间倒序累积，就是项目的决策日志。

**来源**：https://adr.github.io/

## Diátaxis（文档四象限）

**是什么/为什么。** Diátaxis 识别出四种不同的用户需求，以及与之对应的四种文档形式——tutorials（教程）、how-to guides（操作指南）、technical reference（技术参考）、explanation（解释），并主张文档本身应围绕这些需求的结构来组织。

**关键规则。**
- Tutorial：一次在导师指导下发生的体验，始终以学习为导向；目的不是帮用户完成某件事，而是帮助用户学会。
- How-to guide：引导读者解决某个问题或达成某个结果的方向指引，以目标为导向。
- Reference：对系统及其操作方式的技术性描述，以信息为导向。
- Explanation：对某一主题的论述性阐述、允许读者反思，以理解为导向。
- 两条划分轴：tutorials 和 how-to guides 关注用户做什么（行动），reference 和 explanation 关注用户知道什么（认知）；tutorials 和 explanation 服务技能的习得（用户的学习），how-to guides 和 reference 服务技能的应用（用户的工作）。

**在本技能中怎么用。** 帮助判断内容该放进哪份文档、避免一份文档混塞不同导向的内容：`project-config.md` 的本地启动步骤、`deployment.md`、`faq.md` 偏操作指南；`api.md`、`database.md` 偏技术参考；`tech-stack.md` 的选型理由、`business-logic.md` 偏解释。

**来源**：https://diataxis.fr/（两条划分轴见其子页 https://diataxis.fr/map/）

## 12-Factor 配置

**是什么/为什么。** 12-Factor 方法论第三条"配置"：要求代码和配置严格分离——配置在各部署（预发布、生产、开发等）间存在大幅差异，代码却完全一致；在代码中用常量保存配置违背这一要求。

**关键规则。**
- 这里的"配置"指在不同部署间差异很大的内容：数据库、Memcached 及其他后端服务的配置；第三方服务的证书（如 Amazon S3、Twitter）；每份部署特有的配置（如域名）。不包括部署间无差异的应用内部配置（如 Rails 的 `config/routes.rb`）。
- 推荐将应用的配置存储于环境变量（env vars, env）中。三个理由：跨部署修改方便且不动一行代码；不小心签入代码库的概率微乎其微；与语言和系统无关。
- 不纳入版本控制的配置文件虽好于代码常量，但仍有缺点：总会不小心签入代码库、分散在不同目录且格式不一、格式通常是语言或框架特定的。
- 试金石：判断配置是否正确排除在代码之外，看基准代码能否立刻开源而不用担心暴露任何敏感信息。

**在本技能中怎么用。** 对应模板 `assets/templates/project-config.md` 的"环境变量"一节：以 `.env.example` 和代码中的实际读取为准逐一记录；模板已要求密钥类变量只写"去哪里申请"，不把真实值写进文档。

**来源**：https://12factor.net/zh_cn/config

## Mermaid ER 图

**是什么/为什么。** Mermaid 的 `erDiagram` 用纯文本描述实体-关系图，可直接内嵌在 Markdown 里渲染，便于随代码一起版本管理。

**关键规则。**
- 每条语句的语法：`<first-entity> [<relationship> <second-entity> : <relationship-label>]`，关系标签从第一个实体的视角描述；实体名支持任意 Unicode 字符，含空格时须用双引号包裹。
- 基数标记由两个字符组成：最外侧字符表示最大值，最内侧字符表示最小值。四种基数：`|o` / `o|` 零或一；`||` / `||` 恰好一个；`}o` / `o{` 零或多（无上限）；`}|` / `|{` 一或多（无上限）。另有文字别名，如 `zero or one`、`one or more`、`1+`、`0+`、`1` 等。
- 属性在实体名后用 `{` `}` 包裹的块定义，块内是多个 "type name"（类型 名称）对，渲染在实体框内。type 须以字母开头，可含数字、连字符、下划线、圆括号和方括号；name 格式类似，还可以星号开头表示主键；没有隐含的合法数据类型集合。
- 属性的键可以是 PK、FK 或 UK（主键、外键、唯一键）；同一属性多个键约束用逗号分隔（如 `PK, FK`）；注释写在属性末尾并用双引号包裹，注释内容本身不能包含双引号字符。

**在本技能中怎么用。** 对应模板 `assets/templates/database.md` 的"ER 图"一节：用真实表名、字段和基数替换示例；导出的图片放 `.kb/assets/diagrams/`。

**来源**：https://mermaid.js.org/syntax/entityRelationshipDiagram.html

## Mermaid 流程图

**是什么/为什么。** Mermaid 的 `flowchart` 用纯文本描述流程图，同样可直接内嵌 Markdown，适合业务流程、部署流程等示意。

**关键规则。**
- 五个方向关键字：`TB`（自上而下）、`TD`（Top-down，等同 TB）、`BT`（自下而上）、`RL`（从右到左）、`LR`（从左到右）。
- 节点形状：默认是矩形，`id1[方框文字]` 为节点设置与 id 不同的显示文字；`id1(文字)` 圆角矩形；`id1{文字}` 菱形（判断/决策）。
- 带箭头且带文字标签的边有两种等价写法：`A-->|text|B` 或 `A-- text -->B`。
- 节点文本包含会破坏语法的特殊字符（如圆括号）时，把文本放在引号内，如 `id1["This is the (text) in the box"]`；Unicode 文本同样用双引号包裹，如 `id["This ❤ Unicode"]`。

**在本技能中怎么用。** 用于 `assets/templates/business-logic.md` 的业务流程图等流程示意；Mermaid 源码直接内嵌 Markdown，导出图片放 `.kb/assets/diagrams/`。

**来源**：https://mermaid.js.org/syntax/flowchart.html
