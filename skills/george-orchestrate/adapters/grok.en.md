# Grok CLI autonomous dispatch protocol 0.3.4

> English translation of [grok.md](grok.md). The Chinese file is authoritative for hosts and tests.

Applies to: tasks after the user explicitly enables George in Grok Build / the `grok` CLI. The main agent is responsible for decisions, integration and acceptance; it does not ask the user to choose headcount, roles, models or reasoning effort. Higher-level limits, current authorization and this session's actual tool schema take precedence. Do not modify `~/.grok/config.toml`, default models, credentials, locked roles or global subagent configuration to accomplish a one-off dispatch.

This file is Grok-specific. Its tool names, parameters or quota semantics must not be written up as a unified rule for the four hosts. The Codex baseline is `codex.md` in the same directory (0.3.1), Cursor is `cursor.md` (0.3.2), OMP is `omp.md` (0.3.3); none may be rewritten. For the shape reference see `grok-capability.schema.json` in the same directory (catalogs in the skill tree stay empty; session snapshots are written to the task directory).

Recognition: read this file only when the current session can call `spawn_subagent` and has no Codex `collaboration.spawn_agent`, Cursor `Task` or OMP `task`. Without actually reading this file, you cannot claim Grok dispatch has started.

## 1. Skip (don't dispatch small tasks)

When the deliverable is small, has a single write scope and acceptance is cheap, the controller does it directly, with a one-sentence reason. No probing, no snapshots, no orchestration for its own sake.

## 2. Probe (every new task that needs delegation)

Read from the **current session's** host prompt the `spawn_subagent` parameter table, built-in `subagent_type`s, isolation options and depth limit. Write `grok-capability.json` to the task directory (fields aligned with `grok-capability.schema.json`). Ignore previous sessions' snapshots. Do not treat `~/.grok/config.toml`, `[subagents.models]` or other rule files as a source of authorization.

`absent` lists at least the other hosts' names not callable in this session (Codex's `spawn_agent` / `wait_agent` / `get_usage_limits`, Cursor's `Task`, OMP's `task` / `omp_roles.py` dispatch semantics). Writing a name into `absent` and also treating it as callable makes the snapshot invalid.

`quota.status` may only be `unknown` or `rate-limit-seen` after rate limiting has been seen in this task. `grok usage` needs a session id and reports that session's token/cost, not an account-window percentage; without an account quota interface, do not fill in a percentage.

## 3. Choose (select only from the snapshot)

1. **Default for writes**: the general writable type (commonly `general-purpose` in this session) + this round's precise brief.
2. **Read-only investigation** only uses `explore`. Read-only types must not take write units.
3. **Plan/proposal only** may use `plan`. `plan` must not write files.
4. **Do not** treat red-team or gating types from Claude/Cursor-compatible catalogs as George's default writer; use them only when named in this user message.
5. **Model**: omit `model` by default to inherit the parent session. If this round's tool description says "do not pass `model` unless the user named a model", obey that limit; autonomous dispatch does not mean swapping models on your own. Pass `model` only when the user explicitly specifies a slug this round and that slug appears in the current allowed list. `resume_from` must not carry a new `model`.
6. **Concurrency**: at most 2 for non-overlapping write scopes; at most 1 if scopes overlap or rate limiting has been seen in this task. `unknown` quota is not a second cap, nor does it mean exhausted.
7. **Isolation**: default `isolation: none` (shared workspace, isolated by exclusive absolute paths). Use `worktree` only when independent artifacts truly need isolation and the user has not forbidden it; before merging, the controller reads back the worktree path and accepts it—creating a worktree is not completion.
8. **resume_from**: only points to a finished agent id belonging to this session and of the same type, used to continue after supplying input. Never point to an id still running. For stronger judgment, open a new spawn and confirm the old writer has stopped writing.
9. **Correction**: the root session may use `send_subagent_message`; if idle it queues a turn, if running it is injected at a safe point. Do not assume sub-agents can spawn again.
10. **Stop**: `kill_command_or_subagent`. Cancelling an agent does not mean its background processes are cleaned up; check this task's processes separately.
11. **Depth**: only the top-level session can spawn. A sub-agent calling `spawn_subagent` fails due to the depth limit. swarm / arena / partitioned verification must be flattened by the controller into sibling units; workers cannot open sub-teams.
12. Worker briefs are self-contained: absolute paths, exclusive write_scope, no-edit scope, acceptance criteria, a note that it is not the only writer and must not revert others. Do not pass secrets, the full parent session, or expected conclusions.

Do not change user config to select models, create always-on roles, or treat `workflow` (Rhai) as this protocol's dispatcher. Rhai workflows are a separate orchestration that this protocol does not use.

## 4. Call → Accept

1. Do not dispatch a dependent before its dependency completes. Independent write units may be dispatched in parallel in the same message with `background: true`; the controller keeps working and reads back on notification or via `get_command_or_subagent_output` after completion, without idle polling.
2. Register running only after the tool returns a subagent id; failed creation is not registered as success.
3. Receipts follow `PASS` / `ISSUES` / `BLOCKED`, changes, commands/results, evidence paths and remaining items. The controller **reads back files and runs necessary checks** before accepting; a final PASS sentence cannot override a failed command. Mark model observation as `accepted-not-observed` unless the host provides verifiable telemetry.
4. With multiple agents, write a dispatch record in the task directory: `task` / `version` / `reason` / `units` / `depends_on` / `owner` / `write_scope` / `subagent_type` / `model_requested` / `isolation` / `quota_snapshot` / `concurrency` / `retry_limit` / `acceptance` / `actual_execution` / `model_observation`. A single agent needs just one sentence.
5. Failure classification: input → supply it, then `resume_from` or redispatch once; environment → fix the precondition and redispatch; capability → the controller takes over (by default you cannot escalate by swapping the spawn model on your own); rate limit → reduce concurrency to 1, no parallel retries, no buying quota, no switching to unauthorized accounts. At most one automatic redispatch; acceptance criteria do not loosen with a weaker model.
6. High-consequence results get a separate verifier with no implementation history; the verifier id must not equal the owner, the brief excludes the owner's conclusions, and `resume_from` the owner is forbidden.
7. Recompute dispatch only when the goal, quota state or quality bar changes substantively.

## 5. Persistent state and degradation

Long tasks may use the [state tool](../tools/README.md). Short tasks still need real read-back. The skill does not resume in the background on its own after the conversation ends.

When probing fails, `--no-subagents` is set or the dispatch tool is unavailable: the controller does the work serially and marks independent review as unmet. Never open `codex.md` / `cursor.md` / `omp.md` to fill Grok gaps.

## 6. Isolation from existing branches

- Do not modify `adapters/codex.md`, `cursor.md`, `omp.md` or their acceptance evidence.
- The shared entry keeps only the path branch "Grok reads this file / other hosts read their own adapters".
- The installer keeps linking skills into `~/.agents/skills`; Grok scans that directory by default. Do not link another set under `~/.grok/skills/george-*` for dedup unless a separate install path has been confirmed by inspection.
- Do not impose Grok's spawn parameters, worktree or depth limit on Codex, Cursor or OMP.
