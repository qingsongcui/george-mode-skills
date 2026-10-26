# Orchestration and persistent execution

> English translation of [SKILL.md](SKILL.md). Hosts load `SKILL.md`; this file is the full English body.

Each task uses the autonomous-dispatch adapter for its host: Codex reads [codex.md](adapters/codex.md); Cursor reads [cursor.md](adapters/cursor.md); oh-my-pi (`omp`) reads [omp.md](adapters/omp.md); Grok Build / the `grok` CLI reads [grok.md](adapters/grok.md); Google Antigravity (Antigravity 2.0 / IDE / `agy` CLI) reads [antigravity.md](adapters/antigravity.md). The main agent decides whether to delegate and this round's model and reasoning effort; it does not wait for the user to choose.

First read the [integration contract](../george-mode/references/integration.md). The original goal, user corrections, authorization and the real completion predicate run through the whole task. Ordinary tasks that only need to finish this round are not escalated to long-term orchestration.

| Situation | Playbook |
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

For the division-of-labor mechanism see [swarm](workflows/swarm.md); for complex tasks without an existing flow see [figure-it-out](workflows/figure-it-out.md); for key decisions see [decision trail](workflows/decision-trail.md).

[Persistent state, plan and PR-watch tools](tools/README.md) ship with the package. The state tool does not dispatch agents or grant external permissions; execution uses the current host's real tools. Each subtask must have an exclusive write scope, an acceptable artifact and an owner; the main agent reads back evidence and is responsible for integration.

Optional capabilities: [role and budget setup](workflows/setup-roles.md), [webhook button UI](workflows/bot-ui.md). They have explicit task triggers and never automatically change models or open the network.
