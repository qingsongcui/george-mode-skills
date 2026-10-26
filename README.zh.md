# george-mode

由 11 个技能组成的 Agent 技能矩阵，让编码/知识型 Agent 按“**决策 → 执行 → 验证 → 复盘**”闭环工作：高后果选择前登记目标、假设、反证、预测和停止条件；声称完成前先验证真实行为。

适用于任何能加载 `SKILL.md` 技能目录的宿主：Claude Code、OpenAI Codex、Cursor、oh-my-pi（OMP）、Grok CLI、Google Antigravity。

## 技能列表

| 技能 | 用途 |
|---|---|
| `george-mode` | 总入口，按任务轻重路由；授权与证据规则。需显式调用（`/george-mode`、`$george-mode`）。 |
| `george-investigate` | 只读调查：项目摸底、原始证据核查 |
| `george-decide` | 重要/不可逆选择的决策闭环 |
| `george-design` | 结构调查、设计竞争、对抗审查 |
| `george-engineer` | 功能、故障、重构、性能、取证、视觉等价、PR |
| `george-evaluate` | 盲测、性能数字审计、技能行为验证 |
| `george-orchestrate` | 多阶段计划、PR 推进与落地、暂停与续接；各宿主子代理适配 |
| `george-deliver` | 已定目标的制作与配置，做到完成 |
| `george-verify` | 真实表面验收、宿主适配、平台回读 |
| `george-reflect` | 对照预测与结果，提炼有边界的经验 |
| `george-resume` | 长任务续接与交接 |

自包含方法参考：[决策闭环](skills/george-mode/references/decision-loop.md)、[先验证、后交付](skills/george-mode/references/verify-before-deliver.md)。

## 安装

需要 Python 3（仅标准库），在包根目录运行：

```sh
python3 scripts/verify_package.py
python3 scripts/install.py            # 预览
python3 scripts/install.py --apply    # 建立软链
python3 scripts/install.py --remove --apply   # 卸载
```

安装器把 `skills/george-*` 软链到 `~/.agents/skills`、`~/.codex/skills`、`~/.cursor/skills`、`~/.gemini/config/skills`，并为 OMP 添加命令别名；已有同名路径拒绝覆盖。

**Claude Code** 手动安装：把全部 `skills/george-*` 目录一起复制或软链到 `~/.claude/skills/`（或项目 `.claude/skills/`），保持兄弟目录关系。

可选：`skills/george-orchestrate/tools/pstack/` 的 PR 监视器需要 Bun 与 `gh`，先在该目录运行 `bun install --frozen-lockfile`。

## 测试

```sh
python3 -m unittest discover -s tests
```

## 署名

工程原则、engineer/design/evaluate/orchestrate 剧本及 watch-pr 工具大量改编自 Lauren Tan（@poteto）的 [pstack](https://github.com/cursor/plugins/tree/main/pstack)，MIT 许可。见 [NOTICE.md](NOTICE.md) 与 [third_party/pstack-LICENSE.txt](third_party/pstack-LICENSE.txt)。

## 许可证

MIT，见 [LICENSE](LICENSE)。改编自 pstack 的部分保留其原 MIT 声明，见 [NOTICE.md](NOTICE.md)。
