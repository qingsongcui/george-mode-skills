# Antigravity 自主调度协议 0.3.5

适用：用户在 Google Antigravity（Antigravity 2.0、Antigravity IDE、`agy` CLI）显式启用 George 后的任务。主 agent 负责决策、整合和验收；不要求用户选择人数、角色、模型档位或工作区隔离模式。上级限制、当前授权及本会话实际工具 schema 优先。不修改 `~/.gemini/config/config.json`、`settings.json`、默认模型、凭据、全局插件或常驻规则来完成单次调度。

本文件是 Antigravity 专属。不得把其中的工具名、参数或额度语义写成五宿主统一规则。Codex 基线见同目录 `codex.md`（0.3.1），Cursor 见 `cursor.md`（0.3.2），OMP 见 `omp.md`（0.3.3），Grok 见 `grok.md`（0.3.4），均不得改写。形状参考见同目录 `antigravity-capability.schema.json`（技能树内 catalogs 保持空；会话快照写在任务目录）。

识别：当前会话可调用 `invoke_subagent`、`manage_subagents`、`send_message`（或环境含 `ANTIGRAVITY_AGENT=1`），且没有 Codex `collaboration.spawn_agent`、Cursor `Task`、OMP `task`、Grok `spawn_subagent` 时，才读本文件。没有实际读到本文件不能称已启动 Antigravity 调度。

## 1. Skip（小任务不派）

交付物小、单写入范围、验收便宜时，主控直接做，一句话说明理由。不探测、不建快照、不为编排而编排。

## 2. Probe（每个需要委派的新任务）

从**当前会话**宿主工具定义读取 `invoke_subagent` 参数表、内置子代理类型（`self`、`research`、`image-generator`）、可选 `define_subagent` 能力、模型档位枚举（`inherit`、`flash_lite`、`flash`、`pro`）与 `Workspace` 隔离模式（`inherit`、`branch`、`share`）。写入任务目录 `antigravity-capability.json`（字段对齐 `antigravity-capability.schema.json`）。忽略上一会话快照。不把 `~/.gemini/config/config.json` 或 `settings.json` 当作授权来源。

`absent` 至少列入本会话不可调用的异宿主名（Codex 的 `spawn_agent` / `wait_agent` / `get_usage_limits`，Cursor 的 `Task`，OMP 的 `task` / `omp_roles.py`，Grok 的 `spawn_subagent` / `resume_from`）。把某名写进 `absent` 又当可调用，视为无效快照。

`quota.status` 只能是 `unknown` 或本任务已见限流后的 `rate-limit-seen`。当前会话不暴露账户剩余额度百分比接口时不要填百分比。

## 3. Choose（只根据快照选型）

1. **写入默认**用通用可写类型 `TypeName: "self"` + 本轮精确简报（Role 写 2–5 词职责名）。
2. **只读调查**用内置只读类型 `TypeName: "research"`，或用 `define_subagent` 定义 `EnableWriteTools: false, EnableSubagentTools: false` 的只读角色。只读类型不得接写入单元。
3. **图像/媒体生成**仅在任务确需生图时才用 `image-generator`。
4. **独立验证者 / 对抗审查**：优先用 `define_subagent` 定义本会话只读验证角色（`EnableWriteTools: false, EnableSubagentTools: false`），或新开无实施历史的 `self` 子代理（`conversationId` 严禁等于 `owner`）。
5. **模型档位（`Model`）**：默认省略或传 `'inherit'`（继承父会话模型）。需要按任务复杂度选型时，只允许使用 schema 枚举值 `'inherit' | 'flash_lite' | 'flash' | 'pro'`（窄检索/局部机械处理可用 `'flash_lite'` 或 `'flash'`；有界实现用 `'inherit'` 或 `'flash'`；不确定根因、复杂架构与高后果审查用 `'pro'` 或 `'inherit'`）。`invoke_subagent` 不接受单次 `effort` 参数，禁止伪造 `effort` 字段。没有实收账单遥测时不声称节省费用。
6. **并发**：互不重叠的写入范围最多 2；范围重叠或本任务已见限流则最多 1。`unknown` 额度不是第二道上限，也不等于耗尽。
7. **隔离（`Workspace`）**：默认 `Workspace: "inherit"`（共享当前工作区，靠独占绝对路径隔离）。仅在并行写入确实需要独立仓库副本且用户未禁止时才用 `"share"` 或 `"branch"`；使用隔离工作区时，主控必须读回并核验合并结果，不把子工作区改动直接当成主工作区已完成。
8. **续接与纠偏（`send_message`）**：每个子代理实例由 `invoke_subagent` 返回的唯一 `conversationId` 标识并保留上下文。补齐缺失输入后继续、或向子代理传达约束修正时，调用 `send_message(Recipient=conversationId, Message=...)`。禁止用 `send_message` 向用户发消息，禁止向非本任务子代理发消息。要换更强模型档位或不同角色类型时，必须确认旧写入者已停写后再新开 `invoke_subagent`。
9. **停止与管理（`manage_subagents`）**：用 `manage_subagents(Action="list" | "kill" | "kill_all", ConversationIds=[...])` 查看状态或终止失控/停滞子代理。杀死子代理会连带终止其后代并清理分支工作区，但主控仍须核实本任务进程与部分产物后再重派。
10. **深度**：默认子代理不再向下派发（深度 1）；通过 `define_subagent` 创建自定义角色时默认设 `EnableSubagentTools: false`。swarm / arena / 分区验证由主控平铺成兄弟单元，不让 worker 递归扩队。
11. **代码编排（`run_workflow`）**：仅当本轮暴露 `run_workflow` 工具且任务适合批量同构 fan-out 时才可选用；常规 1–2 路委派直接用 `invoke_subagent`。
12. worker 简报自洽：绝对路径、独占 `write_scope`、禁改范围、验收标准、并非唯一写入者且不得回滚他人。不传密钥、不传父会话全文、不传预期结论。

## 4. Call → Accept

1. 依赖未完成不得派依赖方。独立写入单元可在同一回合并行调用 `invoke_subagent` 派发；工具返回 `conversationId` 后才登记 `running`，创建失败不登记成功。
2. **响应式唤醒（Reactive Wakeup，禁止轮询）**：Antigravity 在子代理完成或发来消息时会自动唤醒主控。派发后主控继续独立工作或直接结束当前回合等待系统唤醒，**严禁**在循环中调用 `manage_subagents(Action="list")` 轮询或使用 shell `sleep`。
3. 回执约定 `PASS` / `ISSUES` / `BLOCKED`、改动文件、执行命令/结果、证据路径、剩余项。主控**必须自己读回文件并跑必要检查**后才验收；最终一句 `PASS` 不能盖过失败命令。模型观察标 `accepted-not-observed`，除非宿主给出可核对的后端运行遥测。
4. 多 agent 时在任务目录写调度记录 `dispatch.json`：`task` / `version` / `reason` / `units` / `depends_on` / `owner`（`conversationId`） / `write_scope` / `subagent_type` / `model_requested` / `workspace_mode` / `quota_snapshot` / `concurrency` / `retry_limit` / `acceptance` / `actual_execution` / `model_observation`。单 agent 一句话即可。
5. 失败分类：输入缺失 $\to$ 主控补齐真实输入后用 `send_message(Recipient=conversationId, ...)` 在原会话恢复一次（或重派一次），禁止虚构输入；环境问题 $\to$ 修前提后重派；能力不足 $\to$ 主控接管或换 `'pro'` 重派一次；限流 $\to$ 并发降为 1，不并行重试，不买额度、不换未授权账户。最多一次自动恢复/重派；验收标准不随模型档位放宽。
6. 高后果结果另派无实施历史的独立验证者（`conversationId != owner`）；简报不含 owner 结论，禁止复用 owner 的 `conversationId`。
7. 目标、额度状态或质量门槛实质变化时才重算调度。

## 5. 持久状态与降级

长任务可用 [state工具](../tools/README.md)。短任务仍要真实读回。技能不会在对话结束后自行后台常驻恢复。

探测失败或子代理工具不可用时：主控串行自做，并标明独立审查未满足。禁止打开 `codex.md` / `cursor.md` / `omp.md` / `grok.md` 填补 Antigravity 缺口。

## 6. 与已有分支隔离

- 不修改 `adapters/codex.md`、`cursor.md`、`omp.md`、`grok.md` 及其验收证据。
- 共享入口只保留「Antigravity 读本文件 / 其它宿主读各自适配器」的路径分支。
- 安装器通过 `~/.gemini/config/skills/george-*` 建立指向同一技能源的符号链接，与其它跨宿主技能一致。
- 不把 Antigravity 的 `invoke_subagent`、`Model` 四档枚举或 `Workspace` 参数强加给 Codex、Cursor、OMP 或 Grok。
