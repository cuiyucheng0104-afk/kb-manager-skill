# 开发规范

> 最后更新：（待填写）

## 代码规范

- **格式化工具**：（待补充，如 Prettier / Black，配置文件位置）
- **Lint 工具**：（待补充，如 ESLint / Ruff，如何运行）
- **命名约定**：（待补充：文件、变量、组件/类的命名风格）

```bash
# 提交前自查（替换为项目真实命令）
（待补充：lint 命令）
（待补充：format 命令）
```

## Git 工作流

- **分支模型**：（待补充，如 main + feature 分支 / Git Flow）
- **分支命名**：（待补充，如 `feat/xxx`、`fix/xxx`）
- **合并方式**：（待补充，如 squash merge，是否要求 PR + Review）

### Commit 信息规范

（待补充。若使用 Conventional Commits，示例如下：）

```
feat(auth): 支持 JWT 刷新令牌
fix(order): 修复重复扣款
docs(kb): 更新 API 文档
```

> 规范见 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/)：`feat` 表示新增功能（对应 SemVer 的 MINOR），
> `fix` 表示修复 bug（对应 PATCH）；破坏性变更在脚注写 `BREAKING CHANGE:` 或在 `<类型>(范围)` 后加 `!`（对应 MAJOR）。

## Code Review 清单

- [ ] 功能符合需求，边界条件有处理
- [ ] 有对应测试且通过
- [ ] 无明显性能/安全问题
- [ ] 涉及接口/表结构/配置变更时，已同步更新 `.kb/` 对应文档
