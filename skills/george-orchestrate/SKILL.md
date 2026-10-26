---
name: george-orchestrate
description: "George 的多阶段编排、PR推进、持续执行、暂停和恢复。按任务寿命和规模启用。 / George's multi-phase orchestration, PR progression, continuous execution, pausing and resuming. Enabled according to task lifetime and scale."
disable-model-invocation: true
---

> English: [SKILL.en.md](SKILL.en.md) · 中文正文见下方。

# 编排与持久执行

每个任务按宿主使用自主调度适配器：Codex 读 [codex.md](adapters/codex.md)；Cursor 读 [cursor.md](adapters/cursor.md)；oh-my-pi（`omp`）读 [omp.md](adapters/omp.md)；Grok Build / `grok` CLI 读 [grok.md](adapters/grok.md)；Google Antigravity（Antigravity 2.0 / IDE / `agy` CLI）读 [antigravity.md](adapters/antigravity.md)。由主agent决定是否委派及本轮模型与推理强度，不等待用户选型。

先读 [接入合同](../george-mode/references/integration.md)。原目标、用户修正、授权和真实完成谓词贯穿任务。只需本轮完成的普通任务不升级长期编排。

| 场景 | 剧本 |
|---|---|
| orchestrate | [orchestrate](playbooks/orchestrate.md) |
| autopilot-full | [autopilot-full](playbooks/autopilot-full.md) |
| autopilot-stack | [autopilot-stack](playbooks/autopilot-stack.md) |
| babysit | [babysit](playbooks/babysit.md) |
| shipping | [shipping](playbooks/shipping.md) |
| multi-phase-plan | [multi-phase-plan](playbooks/multi-phase-plan.md) |
| pause-safely | [pause-safely](playbooks/pause-safely.md) |
| session-pickup | [session-pickup](playbooks/session-pickup.md) |
| worktree-cleanup | [worktree-cleanup](playbooks/worktree-cleanup.md) |
| autonomous-run | [autonomous-run](playbooks/autonomous-run.md) |

分工机制见 [swarm](workflows/swarm.md)，没有现成流程的复杂任务见 [figure-it-out](workflows/figure-it-out.md)，关键决定见 [决策轨迹](workflows/decision-trail.md)。

[持久状态、计划与PR监视工具](tools/README.md) 已随包提供。状态工具不派发Agent、不授予外部权限；执行使用当前宿主真实工具。每个子任务必须有独占写入范围、可验收产物和负责人，主代理读回证据负责整合。

可选能力：[角色与预算设置](workflows/setup-roles.md)、[Webhook按钮界面](workflows/bot-ui.md)。它们有明确任务触发，不自动修改模型或开放网络。
