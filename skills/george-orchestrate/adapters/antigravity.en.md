# Antigravity autonomous dispatch protocol 0.3.5

> English translation of [antigravity.md](antigravity.md). The Chinese file is authoritative for hosts and tests.

Applies to: tasks after the user explicitly enables George in Google Antigravity (Antigravity 2.0, Antigravity IDE, `agy` CLI). The main agent is responsible for decisions, integration and acceptance; it does not ask the user to choose headcount, roles, model tiers or workspace isolation mode. Higher-level limits, current authorization and this session's actual tool schema take precedence. Do not modify `~/.gemini/config/config.json`, `settings.json`, default models, credentials, global plugins or standing rules to accomplish a one-off dispatch.

This file is Antigravity-specific. Its tool names, parameters or quota semantics must not be written up as a unified rule for all five hosts. The Codex baseline is `codex.md` in the same directory (0.3.1), Cursor is `cursor.md` (0.3.2), OMP is `omp.md` (0.3.3), Grok is `grok.md` (0.3.4); none may be rewritten. For the shape reference see `antigravity-capability.schema.json` in the same directory (catalogs in the skill tree stay empty; session snapshots are written to the task directory).

Recognition: read this file only when the current session can call `invoke_subagent`, `manage_subagents`, `send_message` (or the environment contains `ANTIGRAVITY_AGENT=1`), and has no Codex `collaboration.spawn_agent`, Cursor `Task`, OMP `task` or Grok `spawn_subagent`. Without actually reading this file, you cannot claim Antigravity dispatch has started.

## 1. Skip (don't dispatch small tasks)

When the deliverable is small, has a single write scope and acceptance is cheap, the controller does it directly, with a one-sentence reason. No probing, no snapshots, no orchestration for its own sake.

## 2. Probe (every new task that needs delegation)

Read from the **current session's** host tool definitions the `invoke_subagent` parameter table, built-in sub-agent types (`self`, `research`, `image-generator`), optional `define_subagent` capability, the model tier enum (`inherit`, `flash_lite`, `flash`, `pro`) and `Workspace` isolation modes (`inherit`, `branch`, `share`). Write `antigravity-capability.json` to the task directory (fields aligned with `antigravity-capability.schema.json`). Ignore previous sessions' snapshots. Do not treat `~/.gemini/config/config.json` or `settings.json` as a source of authorization.

`absent` lists at least the other hosts' names not callable in this session (Codex's `spawn_agent` / `wait_agent` / `get_usage_limits`, Cursor's `Task`, OMP's `task` / `omp_roles.py`, Grok's `spawn_subagent` / `resume_from`). Writing a name into `absent` and also treating it as callable makes the snapshot invalid.

`quota.status` may only be `unknown` or `rate-limit-seen` after rate limiting has been seen in this task. When the current session exposes no account-remaining-quota percentage interface, do not fill in a percentage.

## 3. Choose (select only from the snapshot)

1. **Default for writes**: the general writable type `TypeName: "self"` + this round's precise brief (Role is a 2–5 word responsibility name).
2. **Read-only investigation** uses the built-in read-only type `TypeName: "research"`, or a read-only role defined with `define_subagent` as `EnableWriteTools: false, EnableSubagentTools: false`. Read-only types must not take write units.
3. **Image/media generation** uses `image-generator` only when the task truly needs images.
4. **Independent verifier / adversarial review**: prefer a session read-only verification role defined with `define_subagent` (`EnableWriteTools: false, EnableSubagentTools: false`), or a new `self` sub-agent with no implementation history (`conversationId` must never equal `owner`).
5. **Model tier (`Model`)**: omit by default or pass `'inherit'` (inherit the parent session's model). When choosing by task complexity, only the schema enum values `'inherit' | 'flash_lite' | 'flash' | 'pro'` are allowed (narrow retrieval / local mechanical work may use `'flash_lite'` or `'flash'`; bounded implementation `'inherit'` or `'flash'`; uncertain root causes, complex architecture and high-consequence review `'pro'` or `'inherit'`). `invoke_subagent` does not accept a per-call `effort` parameter; never fake an `effort` field. Without actual billing telemetry, do not claim cost savings.
6. **Concurrency**: at most 2 for non-overlapping write scopes; at most 1 if scopes overlap or rate limiting has been seen in this task. `unknown` quota is not a second cap, nor does it mean exhausted.
7. **Isolation (`Workspace`)**: default `Workspace: "inherit"` (share the current workspace, isolated by exclusive absolute paths). Use `"share"` or `"branch"` only when parallel writes truly need an independent repo copy and the user has not forbidden it; when using an isolated workspace, the controller must read back and verify the merge result, never treating sub-workspace changes as done in the main workspace.
8. **Resume and correction (`send_message`)**: each sub-agent instance is identified by the unique `conversationId` returned by `invoke_subagent` and keeps its context. To continue after supplying missing input, or to pass a constraint correction to a sub-agent, call `send_message(Recipient=conversationId, Message=...)`. Never use `send_message` to message the user, and never message sub-agents outside this task. To switch to a stronger model tier or a different role type, confirm the old writer has stopped writing before opening a new `invoke_subagent`.
9. **Stop and manage (`manage_subagents`)**: use `manage_subagents(Action="list" | "kill" | "kill_all", ConversationIds=[...])` to view status or terminate runaway/stalled sub-agents. Killing a sub-agent also terminates its descendants and cleans its branch workspace, but the controller must still verify this task's processes and partial artifacts before redispatching.
10. **Depth**: by default sub-agents do not dispatch further (depth 1); custom roles created via `define_subagent` default to `EnableSubagentTools: false`. swarm / arena / partitioned verification are flattened by the controller into sibling units; workers do not recursively grow the team.
11. **Code orchestration (`run_workflow`)**: optional only when this round exposes the `run_workflow` tool and the task suits batch homogeneous fan-out; routine 1–2-way delegation uses `invoke_subagent` directly.
12. Worker briefs are self-contained: absolute paths, exclusive `write_scope`, no-edit scope, acceptance criteria, a note that it is not the only writer and must not revert others. Do not pass secrets, the full parent session, or expected conclusions.

## 4. Call → Accept

1. Do not dispatch a dependent before its dependency completes. Independent write units may be dispatched in parallel via `invoke_subagent` in the same turn; register `running` only after the tool returns a `conversationId`; a failed creation is not registered as success.
2. **Reactive wakeup (no polling)**: Antigravity automatically wakes the controller when a sub-agent finishes or sends a message. After dispatching, the controller keeps doing independent work or ends the current turn to wait for the system wakeup; it **must never** call `manage_subagents(Action="list")` in a loop to poll or use shell `sleep`.
3. Receipts follow `PASS` / `ISSUES` / `BLOCKED`, changed files, executed commands/results, evidence paths and remaining items. The controller **must read back files and run necessary checks itself** before accepting; a final `PASS` sentence cannot override a failed command. Mark model observation as `accepted-not-observed` unless the host provides verifiable backend runtime telemetry.
4. With multiple agents, write a dispatch record `dispatch.json` in the task directory: `task` / `version` / `reason` / `units` / `depends_on` / `owner` (`conversationId`) / `write_scope` / `subagent_type` / `model_requested` / `workspace_mode` / `quota_snapshot` / `concurrency` / `retry_limit` / `acceptance` / `actual_execution` / `model_observation`. A single agent needs just one sentence.
5. Failure classification: missing input → the controller supplies the real input, then resumes once in the original conversation with `send_message(Recipient=conversationId, ...)` (or redispatches once); never invent input; environment problem → fix the precondition and redispatch; insufficient capability → the controller takes over or redispatches once with `'pro'`; rate limit → reduce concurrency to 1, no parallel retries, no buying quota, no switching to unauthorized accounts. At most one automatic recovery/redispatch; acceptance criteria do not loosen with the model tier.
6. High-consequence results get a separate independent verifier with no implementation history (`conversationId != owner`); the brief excludes the owner's conclusions; never reuse the owner's `conversationId`.
7. Recompute dispatch only when the goal, quota state or quality bar changes substantively.

## 5. Persistent state and degradation

Long tasks may use the [state tool](../tools/README.md). Short tasks still need real read-back. The skill does not stay resident in the background to resume after the conversation ends.

When probing fails or sub-agent tools are unavailable: the controller does the work serially and marks independent review as unmet. Never open `codex.md` / `cursor.md` / `omp.md` / `grok.md` to fill Antigravity gaps.

## 6. Isolation from existing branches

- Do not modify `adapters/codex.md`, `cursor.md`, `omp.md`, `grok.md` or their acceptance evidence.
- The shared entry keeps only the path branch "Antigravity reads this file / other hosts read their own adapters".
- The installer creates symlinks via `~/.gemini/config/skills/george-*` pointing to the same skill source, consistent with other cross-host skills.
- Do not impose Antigravity's `invoke_subagent`, the four-tier `Model` enum or the `Workspace` parameter on Codex, Cursor, OMP or Grok.
