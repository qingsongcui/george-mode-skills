# Codex autonomous dispatch protocol 0.3.1

> English translation of [codex.md](codex.md). The Chinese file is authoritative for hosts and tests.

Applies to: Codex tasks after the user explicitly enables George. The main agent is responsible for decisions, integration and acceptance; it does not ask the user to choose headcount, roles, models or effort. Higher-level limits, current authorization and the actual tool schema take precedence. Do not modify global model/role configuration to accomplish a one-off dispatch.

## 1. Deciding whether to delegate

For each new task, check the deliverable, dependencies, write scope, consequences and verifiability. Benefits include: cheaper models handling bounded work, parallel independent branches, isolating large intermediate context, and independent acceptance. Compare against startup, context transfer, merging and expected rework costs; do not expand the team just because something is "complex" or "parallelizable". Strictly serial work may also be delegated to save cost; small tasks are usually done by the main agent directly.

The main agent briefly states the decision and reason without waiting for approval. A single agent needs one sentence; with multiple agents, save a dispatch record in a local task directory the project allows: task/version, reason, units, depends_on, owner, write_scope, model_requested, effort_requested, selection_reason, quota_snapshot or unknown, concurrency, retry_limit, acceptance, actual_execution. Do not copy secrets, accounts or full sessions. Record a summary of the main agent's decision; internal chain of thought is not required.

## 2. Selecting from this round's real capabilities

Read the role, model and effort combinations from the current spawn tool schema; take concurrency limits from the current tool description and agent status rather than hardcoding a permanent catalog. Read role configuration as needed to identify locks. A similar role must have the required write permissions/tools; a read-only explorer cannot replace a worker.

Prefer the general worker/default with this round's precise task brief to form a temporary responsibility; there is no need to create a role file each time. Use fixed specialized roles only when they fit; when temporary responsibilities are not supported, choose the closest existing role; with no qualified role, the main agent takes over. Never pass an unknown role name to the tool.

If the current tool is collaboration.spawn_agent: when specifying model or reasoning_effort you must set fork_turns="none"; a full-history fork cannot override the model. The user's George autonomous-dispatch authorization allows choosing per task. Workers are assigned a write scope and told they do not own the codebase exclusively and must not revert others' changes. Pass only the background, absolute paths, constraints and acceptance criteria the task needs. Do not pass conflicting overrides to locked roles.

Choose the economical combination that meets the quality bar; do not disguise a price or quality ranking based on model names as a measurement. Typically: clear retrieval / local mechanical edits use an available economical model at low/medium; well-bounded implementation medium; uncertain root causes, architecture and high-consequence review a stronger model at high or above. This is a starting point, adjusted by capability, acceptance history and returned results. Do not fix all cheap tasks at max. The main agent's current model may not be hot-swappable; keep the controller session; when stronger judgment is needed, delegate an independent expert and let the controller decide.

## 3. Quota, cost and concurrency

When tool discovery finds the Codex app's get_usage_limits, read it once; without the interface, record unknown—do not invent an API or extract credentials from auth files. Remaining percentage of an account window is not a per-model token budget; shared account/provider quota cannot be double-counted as independent resources. Without price or consumption data, write only cost assumptions; never claim savings.

Start with at most 2 workers by default, adjusting by independent workload and actual slots; reserve capacity and time for quality-critical acceptance. Temporary conservative policy: when any relevant known limit window has <=20% remaining, at most 1 worker; at <=5%, prioritize controller wrap-up and necessary verification and start no optional exploration. These thresholds are a revisable policy, not a host guarantee. Stop dispatching on a constrained resource only when a hard quota limit is known to be hit; a missing interface or quota field is treated as unknown, not exhausted, and a checkpoint is saved; never automatically buy quota, use paid resets or switch to unauthorized accounts.

With unknown quota, trial-run at most 1 worker with an explicit timeout and at most 1 retry of the same kind; prefer already available models. Check quota again when each phase completes, a rate limit is received or expansion is planned—not every round. On a 429, first identify the window/reset time and avoid concurrent retries; move to alternative resources only if they are authorized and available; otherwise save the unfinished state.

## 4. Actual calls from dispatch to wrap-up

1. List existing agents and available slots. Manage only this task's agents; historical finished agents are not considered active. Assign exclusive write scopes to parallel write units; read-only units may share read scopes; do not dispatch a dependent before its dependency completes; shared writes are serialized or use an isolated checkout.
2. Dispatch independent units one by one with native spawn_agent. Register running and the requested parameters after the tool returns an agent id; failed creation is not registered as success. The controller keeps working independently.
3. Use send_message to pass constraint corrections; an idle agent needs followup_task to trigger a new turn. Check status of dispatched tasks with list_agents and wait with bounded wait_agent (this session's working norm requires no more than 60 seconds per call—not a tool schema limit); the final message is a receipt pending verification.
4. Receipts include PASS/ISSUES/BLOCKED, actual changes, executed commands/results, evidence paths and remaining items. The controller reads back files and necessary tests before accepting; when supported, check the actual runtime model/effort; if the tool only accepts parameters without providing runtime metadata, mark accepted-not-observed—never claim to have verified the backend's actual model.
5. On timeout, check progress first: if there is still valid progress, extend once; if stalled or erroring, interrupt_agent, verify the old worker has stopped and inspect partial artifacts before handing over. Cancelling an agent does not mean its background processes are cleaned up; verify this task's processes separately. Never let two owners write the same scope at once.
6. Failure classification: input/environment problems—fix the precondition first; insufficient capability—escalate once or the controller takes over; insufficient quota—reduce concurrency/choose an available alternative. Keep the same acceptance criteria; never lower correctness requirements along with the model. At most one automatic redispatch; if it still fails, the controller handles it or reports the specific blocker.
7. High-consequence/complex results get a separate verifier with no implementation history, given the original requirement, artifact and acceptance conditions without hinting at the expected conclusion. If verification finds problems, fix and verify the new version; the independent party cannot be the owner.
8. Summarize what was actually done and not done, terminate this task's active workers and save a recovery pointer. When the task changes, broadcast the new constraints first, then stop affected units, read back partial results and reassign; do not redo units already validly accepted.

If the current session exposes a different native agent API, map the lifecycle above onto its schema; when capabilities are missing, automatically shrink to an executable mode and report it—do not copy tools that do not exist.

## 5. Hooking into persistent state

Long tasks use the [state tool](../tools/README.md): after dispatch, unit.put records owner/version/scope; on receiving a receipt, inbox.push first; after the controller reads back the evidence, verdict.record; finally inbox.ack. Failures are recorded as failed/blocked; PASS text cannot override a failed command. Changing owner requires confirming the old owner stopped, then handoff=previous-owner-stopped. On recovery, status/inbox.read first, check the current content version, then continue; verification of old versions is not reused. This tool manages facts; it is not a daemon that executes agents automatically.

Short tasks need no SQLite but must still actually receive, check artifacts and explain failures. After the process terminates or the conversation ends, the skill does not resume dispatch in the background on its own; the next start recovers from the checkpoint.
