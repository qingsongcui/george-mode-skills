# Cursor autonomous dispatch protocol 0.3.2

> English translation of [cursor.md](cursor.md). The Chinese file is authoritative for hosts and tests.

Applies to: Cursor tasks after the user explicitly enables George. The main agent is responsible for decisions, integration and acceptance; it does not ask the user to choose headcount, roles, models or reasoning effort. Higher-level limits, current authorization and this session's actual tool schema take precedence. Do not modify Cursor global rules, pstack model files or locked role configuration to accomplish a one-off dispatch.

This file is Cursor-specific. Its tool names, model slugs or parameters must not be written up as a unified rule for the three hosts. The Codex baseline is `codex.md` in the same directory (0.3.1) and must not be rewritten. For the shape reference see `cursor-capability.schema.json` in the same directory (catalogs in the skill tree stay empty; session snapshots are written to the task directory).

## 1. Skip (don't dispatch small tasks)

When the deliverable is small, has a single write scope and acceptance is cheap, the controller does it directly, with a one-sentence reason. No probing, no snapshots, no orchestration for its own sake.

## 2. Probe (every new task that needs delegation)

Read from the **current session's** host prompt the sub-agent type list, the model allowlist, and the parameter table of the dispatch tool actually available this round. Write `cursor-capability.json` to the task directory (fields aligned with `cursor-capability.schema.json`). Ignore previous sessions' snapshots. Do not treat pstack or other rule files as a source of authorization.

`absent` lists at least the other hosts' names not callable in this session (for example Codex's spawn/wait/effort/quota tool names). Writing a name into `absent` and also treating it as callable makes the snapshot invalid.

`quota.status` may only be `unknown` or `rate-limit-seen` after rate limiting has been seen in this task. Without a usage interface, do not fill in a percentage.

## 3. Choose (select only from the snapshot)

1. **Default for writes**: the general writable type (the general name marked writable in this session's catalog; commonly `generalPurpose`) + this round's precise brief.
2. **Read-only investigation** only uses a read-only type (commonly `explore`). Read-only types must not take write units.
3. **`poteto-agent` is not George's default writer.** Use it only when this round is explicitly running a poteto-mode playbook whose startup requires reading poteto-mode first.
4. **User-gated types** (review types the catalog says require the user to name them) are off by default unless named in this user message.
5. **Model**: pass `model` only when the slug appears in this session's `models` and is not an "inherit parent session" placeholder; otherwise omit it to inherit the parent session. Reasoning effort is expressed only through the chosen slug; do not pass a separate effort field. Starting policy (not a price measurement): narrow mechanical work → an economical/fast tier from the allowlist; bounded implementation → a high tier from the allowlist; uncertain root causes/architecture/high-consequence review → an xhigh tier from the allowlist. If rejected, switch once using the allowed list returned in the error; do not retry unchanged, and do not make the user choose.
6. **Concurrency**: at most 2 for non-overlapping write scopes; at most 1 if scopes overlap or rate limiting has been seen in this task. `unknown` quota is not a second cap, nor does it mean exhausted.
7. **Isolation**: default to the local shared workspace, isolated by exclusive absolute paths. Use `cloud` only when the user explicitly asks.
8. **resume**: only points to a finished agent id, used to continue after supplying input. `resume: "self"` is forbidden. resume must not carry a new `model`; to switch to a stronger model, open a new Task and confirm the old writer has stopped writing.
9. **interrupt**: not passed by default. Allowed only when the user explicitly asks to interrupt.
10. Worker briefs are self-contained: absolute paths, exclusive write_scope, no-edit scope, acceptance criteria, a note that it is not the only writer and must not revert others. Do not pass secrets, the full parent session, or expected conclusions.

## 4. Call → Accept

1. Do not dispatch a dependent before its dependency completes. Independent write units may be dispatched in parallel in the same message and run in the background; the controller keeps working and reads back on notification after completion, without idle polling.
2. Register running only after the tool returns an agent id; failed creation is not registered as success.
3. Receipts follow `PASS` / `ISSUES` / `BLOCKED`, changes, commands/results, evidence paths and remaining items. The controller **reads back files and runs necessary checks** before accepting; a final PASS sentence cannot override a failed command. Mark model observation as `accepted-not-observed` unless the host provides verifiable telemetry.
4. With multiple agents, write a dispatch record in the task directory: `task` / `version` / `reason` / `units` / `depends_on` / `owner` / `write_scope` / `model_requested` / `subagent_type` / `quota_snapshot` / `concurrency` / `retry_limit` / `acceptance` / `actual_execution` / `model_observation`. A single agent needs just one sentence.
5. Failure classification: input → supply it, then resume or redispatch once; environment → fix the precondition and redispatch; capability → escalate once or the controller takes over; rate limit → reduce concurrency to 1, no parallel retries, no buying quota, no switching to unauthorized accounts. At most one automatic redispatch; acceptance criteria do not loosen with a weaker model.
6. High-consequence results get a separate verifier with no implementation history; the verifier id must not equal the owner, and the brief excludes the owner's conclusions.
7. Recompute dispatch only when the goal, quota state or quality bar changes substantively.

## 5. Persistent state and degradation

Long tasks may use the [state tool](../tools/README.md). Short tasks still need real read-back. The skill does not resume in the background on its own after the conversation ends.

When probing fails or the dispatch tool is unavailable: the controller does the work serially and marks independent review as unmet. Never open `codex.md` to fill Cursor gaps.

## 6. Isolation from the Codex branch

- Do not modify `adapters/codex.md` or its acceptance evidence.
- The shared entry keeps only the path branch "Cursor reads this file / Codex reads codex.md".
- OMP and other hosts do not claim equivalent dynamic dispatch because of this file.
