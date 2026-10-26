# OMP autonomous dispatch protocol 0.3.3

> English translation of [omp.md](omp.md). The Chinese file is authoritative for hosts and tests.

The applicable host is oh-my-pi's `omp` command, not OpenCode or oh-my-opencode. After the user explicitly enables George in OMP, for every new task in this session the main agent decides whether to delegate and chooses responsibilities, models, reasoning effort, concurrency, budget and recovery; these technical choices are not handed back to the user. Recompute when goals, authorization, quality or resources change substantively. The main agent is responsible for integration and final acceptance. This protocol does not expand platform operations, spending, publishing or credential permissions.

## 1. Judge the benefit first; no dispatch for its own sake

Compare the benefits delegation can bring—a competent economical model, independent artifact streams, context isolation, independent acceptance—with startup, brief transfer, merging and expected rework costs. Small well-bounded tasks are done directly by the controller with a one-sentence explanation, without enumerating the whole repo or starting workers. When isolated context or independent acceptance is needed, even strictly serial work may be delegated. Do not expand the team just because things "can be parallel", and do not claim savings have been measured just because a model was chosen by name.

When delegating, leave four brief checks: blocking prerequisites, independent artifacts, shared mutable objects, minimal safe split. Dependencies finish first and are accepted by the controller before dispatching downstream; overlapping write areas use independent checkouts or run serially—renaming an agent is not isolation.

## 2. Bounded by this round's real capabilities

First look at the current `task` schema. As needed, check with read-only `omp --version`, `omp config get <key>`, `omp models --json`, `omp usage --json`, without dumping whole configs or quotas containing account information. RPC `get_state.dumpTools` can prove the actual tool parameters; check agent sources and role definitions against this machine's release `omp://task-agent-discovery.md`; never fabricate parameters from Codex/Cursor.

- With batch enabled, the call is `task({context, tasks:[{name?, agent?, task, solutionSpace, ...actually available fields}]})`. `context` is the shared brief; each unit gives absolute paths, responsibility, write area, no-edit zones, deliverable and acceptance; sub-agents do not inherit the full parent session. `solutionSpace` describes how open the problem is, not workload or peer coordination.
- `task` has no general `model`, `subagent_type` or `run_in_background` field. Default general tasks omit `agent`; investigation, mechanical processing and review choose a competent type from the current catalog; never send a read-only type to write files.
- If the current session has `task.enableEffort=false` or the schema has no `effort`, never pass per-task `effort`. `solutionSpace` only takes part in classification when the chosen agent is configured as `auto`; it is not an effort switch.
- Only when the schema really has `effort` may OMP's `lo/med/hi` be used. These are relative tiers mapped and capped by the chosen model's capability and `task.maxEffort`, not absolute low/high/max.
- Model catalog, role config, parameters accepted, host runtime metadata, actual backend service and actual charges are different evidence layers. Being in the catalog does not prove a call works; switching the parent session's model does not prove a sub-agent switched models.
- `tasks[].tools` binds tool names already registered in the parent eval kernel; it is not a native `read/write/bash` tool allowlist; omit it when shared eval tools are not needed. Native tool permissions are written in the project role frontmatter's `tools`; you cannot isolate by guessing this parameter.

Write the model, role and parameter snapshot to this task's directory; do not write fixed model brands/prices into the skill body. Save only the version, tool fields, allowed roles, selectors, supported thinking levels, current limits, redacted quota and discovery source. Fields that cannot be observed stay `unknown`; never backfill actual values from requested ones.

## 3. Task-specific responsibilities, models and reasoning

First set this round's responsibilities and acceptance, then choose a competent economical combination. Clear mechanical tasks prefer cheaper configurations already verified as competent; bounded implementation uses an adequate mid-tier configuration; uncertain root causes, complex design and high-consequence acceptance prefer stronger judgment. When prices are unknown, call it only a conservative choice; never claim it is the cheapest or has saved money.

OMP can discover new roles from the project's `.omp/agents/*.md` at execution time. Prefer the [per-round role tool](../tools/omp_roles.py) to create unique `george-omp-` names for the current task, writing the actually discovered selector and supported thinking into frontmatter, then call it via native `task`'s `agent`. Role briefs and tool permissions follow this round's needs; do not create general standing super-roles. Preparation example:

```text
python3 <George source>/skills/george-orchestrate/tools/omp_roles.py prepare --project <current project> --input <this round roles.json> --receipt <this round roles-receipt.json>
```

Input contains `run_id` and `roles`; each role gives `name, description, model, thinking, tools, brief`. The tool only prepares roles and an ownership receipt; it does not dispatch agents, grant model permissions, or guarantee the requested model actually takes effect. First confirm the project directory matches the current task's cwd; roles in another subdirectory are not considered discovered by this session. Role names must not override the user's existing or fixed roles.

For a dynamic role to really take effect, pass the newly created role name in the `agent` field of a `tasks[]` unit; dispatching the built-in `task` and then having the worker read the role Markdown does not let you claim the model or effort changed. The absence of `task.model/effort` fields does not mean there is no role-level routing. When the current schema's `agent` is a string, the old catalog in the prompt is not an enum allowlist; the project's roles are rediscovered at execution time. Degrade only after an actual unknown/disabled/depth rejection, and keep that failure.

`task.agentModelOverrides[agentName]` takes precedence over agent frontmatter, then falls back to role/parent session. Avoid occupied names; do not change the overrides of the five built-in roles to implement this round's choice. Model aliases expand only per this round's `modelRoles`; `m1/m2` may be used only when the user actually tagged them—never forge composer tags. Choose one explicit expression—frontmatter thinking or a selector suffix—then check the run result.

In development-time native trial runs, a role requested `medium` and the corresponding worker actually recorded `low`, yet the role still started and completed. So you cannot rely on "unsupported thinking will definitely reject dispatch"; check the supported set before choosing and verify with the same worker's run record after dispatch. The specific normalization or default fallback mechanism is unconfirmed; do not infer mapping rules for all models from this one result.

When the host does not allow new roles, a role is disabled or the schema rejects it, choose the closest existing role with adequate permissions; with no qualified one, the controller takes over, and the independent-acceptance gap remains unmet. Never repeatedly hot-switch the parent session or change Codex/Cursor settings to choose models.

Per-round roles are written only to the project OMP directory. Existing same-name paths and roles modified by others must not be overwritten. After workers stop and results are read back, use the same tool's `cleanup --receipt <this round roles-receipt.json>` to clean only your own roles whose hash is unchanged; others' roles and config are kept. Any necessary persistent change must be OMP-specific, backed up first, revertible, and preserve other providers and user settings.

## 4. Budget, quota and concurrency

Read this round's actual `task.maxConcurrency`, `task.maxRecursionDepth`, async and provider limits. The host cap is not the target concurrency; start with at most 2 independent workers by default, reserving controller acceptance resources. Workers do not dispatch further by default unless there is real independent benefit and depth allows.

`omp usage --json` can query quotas for some providers; project only an allowlist of provider, window, shared group, status and remaining amount; do not store emails, account IDs, credentials or raw provider metadata. Percentages are account windows, not this task's token or dollar budget. The same account/shared group cannot be summed twice; another account's balance in a pool is not this worker's bound balance. Without a reliable binding, mark `unknown`.

Unknown quota does not mean exhausted. For unknown resources, do only short, bounded trial runs; start with 1 worker, and expand to 2 if independent artifacts truly benefit and there is already a successful receipt. When a relevant hard limit has been observed, stop new dispatches on the constrained resource; when quota is tight, reduce concurrency and prioritize integration and necessary acceptance. Simulated low quota must be separately labeled `simulated`; it cannot pass for a live 429, and you must never artificially exhaust, buy quota, use reset benefits or switch to unauthorized accounts.

Each dispatch sets an observable deadline, at most 1 retry of the same kind, and bounds on total workers/requests. `task.softRequestBudget` is a soft threshold on request count, not a hard token/money cap; `task.maxRuntimeMs=0` means unlimited, and a timeout sentence in a brief is not a host hard limit. When hard bounds are needed, use a per-round `--config` overlay or project-level config without changing global settings; still never cancel other tasks' workers.

The controller deadline for a dependency chain accumulates along the critical path; do not apply one worker's cap to a whole serial chain. If the artifact is done but the controller has not wrapped up, first distinguish a coordination deadline from a worker timeout; after saving a checkpoint, a bounded continuation may happen once, without redispatching accepted phases or turning failure into success by repeatedly enlarging the budget.

## 5. Dispatch, receipt and real acceptance

1. The controller saves this round's dispatch summary: task/version, reason, units, depends_on, owner, write_scope, role, requested_model/thinking, selection_reason, quota/price or unknown, concurrency, deadline, retry_limit, acceptance. Small tasks need no database or full dossier.
2. Independent units start in the same `tasks[]` batch to actually run in parallel; dependent units go in later batches, with the next batch sent only after the controller accepts its prerequisites. Shared write areas run serially or in independent checkouts. Non-Git projects use explicit isolated directories rather than blindly passing `isolated:true`.
3. Record running only when the native tool successfully returns an ID. With `async.enabled=true`, a background job returning does not mean done; the controller keeps working independently, completion notifications arrive automatically, and it `wait`s only when there is nothing else to do—no idle polling.
4. Per the actual host, use `agent://<id>`, `history://<id>`, `proc://<id>` to view receipts/progress, and `write agent://<id>` to pass corrections; never copy Codex's spawn/wait/resume API. The controller must read the artifacts itself, run acceptance and record commands and real results; a worker's PASS is not acceptance evidence.
5. OMP's returned `resolvedModel`, `resolvedThinkingLevel`, `usage/tokens/requests`, lifecycle and sub-session messages can serve as host observations; RPC can supplement with `get_subagents`, `get_subagent_messages` and session stats. The sub-session entries observed so far are `model_change.model` and `thinking_level_change.thinkingLevel`, not guessed Pi fields. If the tool surface cannot provide them for now, write unknown and let the acceptance checker fetch them; do not repeatedly scan, print the full raw session or private thinking to fill one invisible field. Backend service identity and the real bill may still be unobservable; catalog price estimates are not actual payment.
6. High-consequence results get a separate verifier with no implementation history; give only the requirement, artifact and acceptance conditions, not the implementer's conclusions. After the controller integrates a version, re-verify affected parts; approval from several instances of the same model is not an independent fact.

## 6. Failure recovery, stopping and continuation

- Missing input: record the original failure/gap; if the task context can supply it, supply it and redispatch once; never invent input.
- Environment failure: fix the earliest precondition first (directory, dependency, permission, schema); do not attribute environment errors to model capability.
- Insufficient capability or quality: escalate model/reasoning once or the controller takes over; acceptance criteria are not lowered. Classify model plan/401/403/429 separately; switch only to authorized available alternatives, never loop unchanged.
- Timeout: verify whether there is still valid progress. To stop this task's worker, use the actual `write proc://<id>/kill` or an available OMP cancel; confirm writing stopped and check partial artifacts before handing to a new owner. Cancelling an agent does not prove its background processes are cleaned up; check this task's processes separately.
- OMP idle/parked workers are continued via the actual messaging mechanism; recovery counts only with new execution evidence from the same worker. During development the history list showed parked, but the RPC registry was empty and parked→execution was not verified; an empty registry does not mean parked does not exist. After a hard abort/cancel, you cannot pretend to resume the same process: a local trial obtained a receipt where the host explicitly refused to message/revive a hard-aborted worker; use a new worker with a merged task contract instead. Do not wake unrelated historical agents.
- Goal, quota or quality changes mid-run: notify affected workers first, isolate shared write state, then reschedule for the new goal. If it still fails at the retry bound, the controller handles it or saves the exact blocker; do not let the user decide technical roles/models.
- A depth setting existing does not mean the rejection path has been verified. A role lacking task permission, `spawns:none` or a worker refusing to try does not prove the host enforced a recursion-depth rejection; that needs an actual nested call in the same sub-session and a matching host error receipt.

Long tasks reuse the [state tool](../tools/README.md)'s owner/version/scope, inbox, blocked/failed and version-bound acceptance; the state file is not a native dispatcher. On recovery, first check the artifact version and the old owner's state. After the conversation ends, OMP exits or the process is cancelled, the skill does not become a background daemon on its own; it resumes on the next explicit enablement / from a valid checkpoint.

## 7. Integration and rollback boundaries

Only OMP reads this file. Keep Codex's `codex.md`, Cursor's `cursor.md`, their respective configs and historical acceptance. This protocol does not inject task parameters, OMP role aliases, effort or account semantics into other hosts. The automatic scope of one enablement is per-task judgment within the current George session and this task's lifecycle—not global always-on, and no promise to run across processes on its own.

Rollback should remove only the OMP branch of the shared entry and OMP resources added this round; merge later modifications to shared files first, and never blindly overwrite other agents' work from a backup. Clean only this task's unmodified roles per the role list, keeping historical evidence and failure records.
