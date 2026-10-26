# 宿主适配

五个宿主共享本包的 skills/ 技能源。安装位置与任务工作区相互独立；项目本地规则和宿主权限优先。会话级自主调度由各宿主适配器管理，不擅改持久配置或凭据。

## 调用和发现

| 宿主 | 安装入口 | 调用与命令 |
|---|---|---|
| Codex | `~/.codex/skills/george-*`，链接到同一源 | `$george-mode` 加任务；也可从技能菜单选择 |
| Cursor | `~/.cursor/skills/george-*`，链接到同一源 | `/george-mode` 加任务；未出现时新建会话或刷新技能发现 |
| OMP | `~/.agents/skills/george-*`（安装器亦提供 OMP 专属 `/george-mode` 命令别名） | 原生命令为 `/skill:george-mode`；安装别名后亦可输入 `/george-mode` |
| Grok CLI | 不另装 `~/.grok/skills/george-*`；默认扫描已安装的 `~/.agents/skills/george-*` | `/george-mode` 加任务；`grok inspect` 可核发现。安装器不改 `~/.grok/config.toml` |
| Antigravity | `~/.gemini/config/skills/george-*`，链接到同一源 | `/george-mode` 加任务（支持 Antigravity 2.0、IDE 与 `agy` CLI）；Language Server `GetAllSkills` 可核发现 |

`disable-model-invocation: true` 是部分宿主支持的扩展字段，不能假定所有宿主都识别：在 OMP 与 Antigravity 中，它会向模型的自动工具调用隐藏该技能，但**隐藏不等于命令消失**，用户仍可明确通过 `/skill:george-mode`（OMP）或 `/george-mode`（Antigravity）原生调用。Grok CLI 识别该字段，斜杠 `/george-mode` 仍可显式调用。Codex 另用 `agents/openai.yaml` 中的 `allow_implicit_invocation: false`。**OMP、Grok 与 Antigravity 不使用 `agents/openai.yaml`**，不设固定模型，不依赖自动技能触发。所有入口默认按需显式调用，不创建 always-on rule。

OMP 安装器只在默认 profile 的 `~/.omp/agent/commands/george-mode.md` 放置别名，不改任何 profile 配置。其他 profile 应在其自己的 `commands/` 目录安装同源命令，不能假定默认 profile 的命令已生效。`~/.agents/skills` 的原生技能发现依赖该宿主启用 agents 来源；安装器不擅自打开来源开关。

不要把手动读取等同原生菜单发现，不把原生发现等同任务效果通过。使用方式见 [使用与验收](使用与验收.md)。

## 执行差异

- 技能正文里的相对链接只指向该技能或兄弟 `george-*` 目录。Cursor Read 按字面收折 `..`，不跟随 `~/.cursor/skills/george-*` 这条安装符号链接。技能内部帮助与导航统一使用兄弟相对路径（如 `../../george-investigate/SKILL.md`）（基于实际读取文件的位置解析），确保在所有宿主中均可无歧义打开。
- 调用机制隔离：Codex 使用 `$george-*` 与 `agents/openai.yaml`；Cursor 使用 `/george-mode`；OMP 使用原生 `/skill:george-mode` 及安装器提供的 OMP-only `/george-mode` 文件命令别名；Grok CLI 使用 `/george-mode`，发现来自 `~/.agents/skills`；Antigravity 使用 `/george-mode`，发现来自 `~/.gemini/config/skills`。OMP、Grok 与 Antigravity 完全不依赖 `agents/openai.yaml`。
- 文件操作、命令行、浏览器、MCP、子 Agent 和提问工具都使用当前宿主实际提供的接口。工具缺失时选可验证替代或报告缺口，不复用其他宿主的工具名和参数。
- 若需要委派，先确认本轮允许，写出任务边界与路径所有权。未提供原生子 Agent 时顺序执行，不自行安装插件或启动付费模型。
- 自主调度按宿主分支：Codex 读 `george-orchestrate/adapters/codex.md`；Cursor 读 `george-orchestrate/adapters/cursor.md`；oh-my-pi（`omp`）读 `george-orchestrate/adapters/omp.md`；Grok CLI 读 `george-orchestrate/adapters/grok.md`；Antigravity 读 `george-orchestrate/adapters/antigravity.md`。调度细则只留在对应适配器内，不把某一宿主的参数、角色与额度语义强加给其他宿主。
- 不在技能中固定模型名称。OMP 的模型配置与提供商选择、Codex 的角色设置、Cursor 的可选模型、Grok 的父会话继承和 Antigravity 的 `Model` 档位枚举各不相同，完全保留用户现有的模型、凭据与路由配置。
- OMP/Cursor/Grok/Antigravity 不拥有 Codex app-server 工具时，不能照抄其回读命令；改用各自真实加载日志或交互界面。Grok 用 `grok inspect` 核发现，用 `spawn_subagent` 派工；Antigravity 用 Language Server `GetAllSkills` 核发现，用 `invoke_subagent` / `send_message` / `manage_subagents` 派工与管理。
- 文档/视觉作品需调用当前宿主可用的生成和渲染工具。技能文本不声称任何宿主自动具有浏览器、桌面控制或模型服务能力。保持源共享和各端权限边界。

## 更新与移除

所有链接跟随源文件更新。移动或删除安装包目录会让链接失效，迁移时先重新安装再验证。安装脚本位于安装包内 `scripts/install.py`，默认只预览，`--apply` 才创建链接；遇同名已有路径拒绝覆盖。

撤销只删除指向本源的链接：在安装包根目录运行 `python3 scripts/install.py --remove --apply`。不会删除原技能源、其他技能或宿主配置。
