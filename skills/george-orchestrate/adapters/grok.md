# Grok CLI 自主调度协议 0.3.4

适用：用户在 Grok Build / `grok` CLI 显式启用 George 后的任务。主 agent 负责决策、整合和验收；不要求用户选择人数、角色、模型或推理强度。上级限制、当前授权及本会话实际工具 schema 优先。不修改 `~/.grok/config.toml`、默认模型、凭据、锁定角色或全局 subagent 配置来完成单次调度。

本文件是 Grok 专属。不得把其中的工具名、参数或额度语义写成四宿主统一规则。Codex 基线见同目录 `codex.md`（0.3.1），Cursor 见 `cursor.md`（0.3.2），OMP 见 `omp.md`（0.3.3），均不得改写。形状参考见同目录 `grok-capability.schema.json`（技能树内 catalogs 保持空；会话快照写在任务目录）。

识别：当前会话可调用 `spawn_subagent`，且没有 Codex `collaboration.spawn_agent`、Cursor `Task`、OMP `task` 时，才读本文件。没有实际读到本文件不能称已启动 Grok 调度。

## 1. Skip（小任务不派）

交付物小、单写入范围、验收便宜时，主控直接做，一句话说明理由。不探测、不建快照、不为编排而编排。

## 2. Probe（每个需要委派的新任务）

从**当前会话**宿主提示读取 `spawn_subagent` 参数表、内置 `subagent_type`、隔离选项、深度限制。写入任务目录 `grok-capability.json`（字段对齐 `grok-capability.schema.json`）。忽略上一会话快照。不把 `~/.grok/config.toml`、`[subagents.models]` 或其它规则文件当作授权来源。

`absent` 至少列入本会话不可调用的异宿主名（Codex 的 `spawn_agent` / `wait_agent` / `get_usage_limits`，Cursor 的 `Task`，OMP 的 `task` / `omp_roles.py` 派发语义）。把某名写进 `absent` 又当可调用，视为无效快照。

`quota.status` 只能是 `unknown` 或本任务已见限流后的 `rate-limit-seen`。`grok usage` 需要 session id，给出的是该会话 token/cost，不是账户窗口百分比；没有账户额度接口时不要填百分比。

## 3. Choose（只根据快照选型）

1. **写入默认**用通用可写类型（本会话常见为 `general-purpose`）+ 本轮精确简报。
2. **只读调查**才用 `explore`。只读类型不得接写入单元。
3. **仅计划/方案**可用 `plan`。`plan` 不得写文件。
4. **不要**把 Claude/Cursor 兼容目录里的红队或门禁类型当 George 默认写入者；仅当本条用户消息点名才用。
5. **模型**：默认省略 `model`，继承父会话。本轮工具说明若要求「用户未点名模型则不得传 `model`」，遵守该限制，不把自主调度理解成擅自换模型。用户本轮明确指定 slug 且该 slug 出现在当前允许列表时才传 `model`。`resume_from` 不得夹带新 `model`。
6. **并发**：互不重叠的写入范围最多 2；范围重叠或本任务已见限流则最多 1。`unknown` 额度不是第二道上限，也不等于耗尽。
7. **隔离**：默认 `isolation: none`（共享工作区，靠独占绝对路径）。`worktree` 仅在独立产物确需隔离且用户未禁止时使用；合并前主控读回 worktree 路径并验收，不把创建 worktree 当成完成。
8. **resume_from**：只指向已结束、属于本会话、且类型相同的 agent id，用于补输入后继续。禁止指向仍在运行的 id。要换更强判断就新开 spawn，并确认旧写入者已停写。
9. **纠偏**：根会话可用 `send_subagent_message`；空闲则排队一轮，运行中则在安全点注入。不要假设子 agent 能再 spawn。
10. **停止**：`kill_command_or_subagent`。取消 agent 不等于其后台进程已清理，另核对本任务进程。
11. **深度**：只有顶层会话能 spawn。子 agent 再调用 `spawn_subagent` 会因深度限制失败。swarm / arena / 分区验证必须由主控平铺成兄弟单元，不能让 worker 再开子队。
12. worker 简报自洽：绝对路径、独占 write_scope、禁改范围、验收标准、并非唯一写入者且不得回滚他人。不传密钥、不传父会话全文、不传预期结论。

不要为选模型改用户配置、创建 always-on 角色，或把 `workflow`（Rhai）当成本协议的派发器。Rhai workflow 是另一套编排，本协议不使用。

## 4. Call → Accept

1. 依赖未完成不得派依赖方。独立写入单元可在同一消息里并行 `background: true` 派发；主控继续做事，完成后按通知或 `get_command_or_subagent_output` 读回，不空转轮询。
2. 工具返回 subagent id 后才登记 running；创建失败不登记成功。
3. 回执约定 `PASS` / `ISSUES` / `BLOCKED`、改动、命令/结果、证据路径、剩余项。主控**读回文件并跑必要检查**后才验收；最终一句 PASS 不能盖过失败命令。模型观察标 `accepted-not-observed`，除非宿主给出可核对遥测。
4. 多 agent 时在任务目录写调度记录：`task` / `version` / `reason` / `units` / `depends_on` / `owner` / `write_scope` / `subagent_type` / `model_requested` / `isolation` / `quota_snapshot` / `concurrency` / `retry_limit` / `acceptance` / `actual_execution` / `model_observation`。单 agent 一句话即可。
5. 失败分类：输入 → 补齐后 `resume_from` 或重派一次；环境 → 修前提后重派；能力 → 主控接管（默认不能靠擅自换 spawn model 升级）；限流 → 并发降为 1，不并行重试，不买额度、不换未授权账户。最多一次自动重派；验收标准不随降模型放宽。
6. 高后果结果另派无实施历史的验证者；验证者 id 不得等于 owner，简报不含 owner 结论，禁止 `resume_from` owner。
7. 目标、额度状态或质量门槛实质变化时才重算调度。

## 5. 持久状态与降级

长任务可用 [state工具](../tools/README.md)。短任务仍要真实读回。技能不会在对话结束后自行后台恢复。

探测失败、`--no-subagents` 或派发工具不可用时：主控串行自做，并标明独立审查未满足。禁止打开 `codex.md` / `cursor.md` / `omp.md` 填补 Grok 缺口。

## 6. 与已有分支隔离

- 不修改 `adapters/codex.md`、`cursor.md`、`omp.md` 及其验收证据。
- 共享入口只保留「Grok 读本文件 / 其它宿主读各自适配器」的路径分支。
- 安装器继续把技能链到 `~/.agents/skills`；Grok 默认扫描该目录。不要为去重再链一套 `~/.grok/skills/george-*`，除非另有经 inspect 证实的独立安装路径。
- 不把 Grok 的 spawn 参数、worktree 或深度限制强加给 Codex、Cursor 或 OMP。
