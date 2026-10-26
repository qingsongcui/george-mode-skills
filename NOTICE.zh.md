# 声明 / 第三方署名

本包含有改编自 Lauren Tan（@poteto）所著 **pstack** 的内容。

- 上游：https://github.com/cursor/plugins/tree/main/pstack（独立镜像：https://github.com/backnotprop/pstack）
- 许可：MIT 许可证，Copyright (c) 2026 Lauren Tan —— 全文见 [third_party/pstack-LICENSE.txt](third_party/pstack-LICENSE.txt)

改编（经修改）的文件：

| 本包内路径 | 上游来源 |
|---|---|
| `skills/george-mode/principles/principle-*.md`（24 个文件）及 `principles/INDEX.md` | pstack `skills/principle-*/SKILL.md` |
| `skills/george-engineer/playbooks/*.md` | pstack `skills/poteto-mode/playbooks/*.md` |
| `skills/george-design/playbooks/*.md`、`skills/george-design/workflows/*.md` | pstack `poteto-mode` 剧本及 `how`/`why`/`architect`/`arena`/`interrogate` 技能 |
| `skills/george-evaluate/playbooks/*.md`、`skills/george-evaluate/workflows/*.md` | pstack `poteto-mode` 剧本（eval、authoring-a-skill）及 `benchmark-checklist` |
| `skills/george-orchestrate/playbooks/*.md`、`workflows/*.md` | pstack `poteto-mode` 剧本（orchestrate、autopilot、babysit、shipping 等） |
| `skills/george-orchestrate/tools/pstack/**`（watch-pr 的 TypeScript 源码与测试、package.json、bootstrap.ts、bun.lock） | pstack `poteto-mode` 工具 / watch-pr |
| `skills/george-verify/**`（验证工作流部分） | pstack `create-verification-skill` / `maintain-verification-skill` |

修改内容：在标注处翻译或用中文改写；重新组织进 george-* 模块结构；调整触发强度与授权假设；移除 watch-pr 的自动安装并增加进程组硬时限。

上述 MIT 许可声明必须保留在这些文件的所有副本或实质部分中。

除此之外不捆绑其他第三方源代码或文本。适配器中提到的宿主名称（Codex、Cursor、oh-my-pi/OMP、Grok CLI、Google Antigravity）仅为互操作而引用。

各 Markdown 文件均提供中英双语版本；译文是原文的翻译，署名与许可同样适用。
