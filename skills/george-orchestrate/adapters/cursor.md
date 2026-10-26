# Cursor自主调度协议 0.3.2

适用：用户显式启用George后的Cursor任务。主agent负责决策、整合和验收；不要求用户选择人数、角色、模型或推理强度。上级限制、当前授权及本会话实际工具schema优先。不修改Cursor全局规则、pstack模型文件或锁定角色配置来完成单次调度。

本文件是Cursor专属。不得把其中的工具名、模型slug或参数写成三宿主统一规则。Codex基线见同目录 `codex.md`（0.3.1），不得改写。形状参考见同目录 `cursor-capability.schema.json`（技能树内 catalogs 保持空；会话快照写在任务目录）。

## 1. Skip（小任务不派）

交付物小、单写入范围、验收便宜时，主控直接做，一句话说明理由。不探测、不建快照、不为编排而编排。

## 2. Probe（每个需要委派的新任务）

从**当前会话**宿主提示读取子agent类型列表、模型白名单，以及本轮实际派发工具的参数表。写入任务目录 `cursor-capability.json`（字段对齐 `cursor-capability.schema.json`）。忽略上一会话快照。不把 pstack 或其它规则文件当作授权来源。

`absent` 至少列入本会话不可调用的异宿主名（例如 Codex 的 spawn/wait/effort/额度工具名）。把某名写进 `absent` 又当可调用，视为无效快照。

`quota.status` 只能是 `unknown` 或本任务已见限流后的 `rate-limit-seen`。没有用量接口时不要填百分比。

## 3. Choose（只根据快照选型）

1. **写入默认**用通用可写类型（本会话目录中标明可写的通用名；常见为 `generalPurpose`）+ 本轮精确简报。
2. **只读调查**才用只读类型（常见为 `explore`）。只读类型不得接写入单元。
3. **`poteto-agent` 不是 George 默认写入者。** 仅当本轮明确在跑 poteto-mode 剧本且其启动要求先读 poteto-mode 时使用。
4. **用户门控类型**（目录说明须用户点名才可用的审查类）默认不启，除非本条用户消息点名。
5. **模型**：仅当 slug 出现在本会话 `models` 且不是“继承父会话”的占位时才传 `model`；否则省略以继承父会话。推理强度只体现在所选 slug 上，不另传 effort 字段。起点策略（非价格测量）：窄机械活 → 白名单里的经济/fast 档；有界实现 → 白名单里的 high 档；不确定根因/架构/高后果审查 → 白名单里的 xhigh 档。被拒绝则用错误返回的允许列表换一次，不原样重试，不让用户选型。
6. **并发**：互不重叠的写入范围最多 2；范围重叠或本任务已见限流则最多 1。`unknown` 额度不是第二道上限，也不等于耗尽。
7. **隔离**：默认本地共享工作区，靠独占绝对路径。`cloud` 仅用户明确要求时使用。
8. **resume**：只指向已结束的 agent id，用于补输入后继续。禁止 `resume: "self"`。resume 不得夹带新 `model`；要换更强模型就新开 Task，并确认旧写入者已停写。
9. **interrupt**：默认不传。仅当用户明确要求打断时才允许。
10. worker 简报自洽：绝对路径、独占 write_scope、禁改范围、验收标准、并非唯一写入者且不得回滚他人。不传密钥、不传父会话全文、不传预期结论。

## 4. Call → Accept

1. 依赖未完成不得派依赖方。独立写入单元可在同一消息里并行派发并后台运行；主控继续做事，完成后按通知读回，不空转轮询。
2. 工具返回 agent id 后才登记 running；创建失败不登记成功。
3. 回执约定 `PASS` / `ISSUES` / `BLOCKED`、改动、命令/结果、证据路径、剩余项。主控**读回文件并跑必要检查**后才验收；最终一句 PASS 不能盖过失败命令。模型观察标 `accepted-not-observed`，除非宿主给出可核对遥测。
4. 多 agent 时在任务目录写调度记录：`task` / `version` / `reason` / `units` / `depends_on` / `owner` / `write_scope` / `model_requested` / `subagent_type` / `quota_snapshot` / `concurrency` / `retry_limit` / `acceptance` / `actual_execution` / `model_observation`。单 agent 一句话即可。
5. 失败分类：输入 → 补齐后 resume 或重派一次；环境 → 修前提后重派；能力 → 升级一次或主控接管；限流 → 并发降为 1，不并行重试，不买额度、不换未授权账户。最多一次自动重派；验收标准不随降模型放宽。
6. 高后果结果另派无实施历史的验证者；验证者 id 不得等于 owner，简报不含 owner 结论。
7. 目标、额度状态或质量门槛实质变化时才重算调度。

## 5. 持久状态与降级

长任务可用 [state工具](../tools/README.md)。短任务仍要真实读回。技能不会在对话结束后自行后台恢复。

探测失败或派发工具不可用时：主控串行自做，并标明独立审查未满足。禁止打开 `codex.md` 填补 Cursor 缺口。

## 6. 与 Codex 分支隔离

- 不修改 `adapters/codex.md` 及其验收证据。
- 共享入口只保留“Cursor 读本文件 / Codex 读 codex.md”的路径分支。
- OMP 与其它宿主不因本文件宣称已具备同等动态调度。
