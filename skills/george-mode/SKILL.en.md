# George mode

> English translation of [SKILL.md](SKILL.md). Hosts load `SKILL.md`; this file is the full English body.

Enabled on demand. The package's [decision loop](references/decision-loop.md) and [verify before deliver](references/verify-before-deliver.md) are the methodological basis, and real user feedback constrains execution. The user's current decision outranks historical preferences; inference is never treated as authorization.

## Getting started

First fix this round's deliverable, the scope of allowed operations and the evidence of completion. For tasks touching a workspace, read the current workspace's AGENTS.md and authoritative entry points, and check existing changes and open items. Self-contained rewrites, translations or single-fact Q&A are handled directly without extra workspace scanning for this mode; mandatory rules already required by higher levels are still followed. When the user says "understand first", read without changing; when they say "fix, continue, execute", carry through to an acceptable result. Look up missing facts yourself first; ask only about things that would change the goal, preferences that cannot be inferred, or missing authorization, and keep doing independent work while waiting.

George is not bound to any business workspace. The scope is the project the current task specifies; entry points, ledgers, numbering and archiving requirements come only from that project's current rules; without project rules, do not create operational ledgers or apply another project's process. The directory holding the skill source files does not represent the task workspace.

## Autonomous dispatch per task

Once the user enables George, the main agent decides on its own whether to delegate this round, and the roles, models, reasoning effort, concurrency and failure takeover; these technical choices are not handed back to the user. Judge once per new task; recompute when the goal, quota or quality changes substantively. Simple tasks get only a short judgment and are executed directly, without extra scanning for dispatch.

Read the adapter for the current host and then execute: Codex uses [Codex autonomous dispatch](../george-orchestrate/adapters/codex.md); Cursor uses [Cursor autonomous dispatch](../george-orchestrate/adapters/cursor.md); oh-my-pi (`omp`) first reads [OMP autonomous dispatch](../george-orchestrate/adapters/omp.md) on this enablement; Grok Build / the `grok` CLI uses [Grok autonomous dispatch](../george-orchestrate/adapters/grok.md); Google Antigravity (Antigravity 2.0 / IDE / `agy` CLI) uses [Antigravity autonomous dispatch](../george-orchestrate/adapters/antigravity.md). For OMP this step reads only one adapter file; it does not require scanning the repo or dispatching for small tasks; without actually reading the adapter you cannot claim that host's dispatch has started. This authorization covers only dispatch within the current task; it does not expand external operation permissions or override the host's higher-level limits. Other hosts without a dedicated adapter keep their original behavior and cannot claim equivalent dynamic dispatch.

## Routing by weight

| Task | Depth and entry |
|---|---|
| Simple Q&A, translation, single reversible edit | Finish directly; check the result; no full dossier |
| Project understanding, evidence investigation, history mining | [george-investigate](../george-investigate/SKILL.md) |
| New business plans, important architecture trade-offs, irreversible or high-consequence decisions | [george-decide](../george-decide/SKILL.md) |
| Code features, bugs, refactors, performance, code review and engineering delivery | [george-engineer](../george-engineer/SKILL.md) |
| Structural investigation, design contest, independent adversarial review | [george-design](../george-design/SKILL.md) |
| Skill/prompt blind tests, measurement audits | [george-evaluate](../george-evaluate/SKILL.md) |
| Multi-phase plans, continuous orchestration, PR follow-through/landing, safe pause | [george-orchestrate](../george-orchestrate/SKILL.md) |
| Making and configuring toward a settled goal | [george-deliver](../george-deliver/SKILL.md) |
| Deliverable acceptance, host adaptation, read-back after platform actions | [george-verify](../george-verify/SKILL.md) |
| Failure review, rule distillation, theory correction | [george-reflect](../george-reflect/SKILL.md) |
| Long-task resumption, handoff, parallel division of labor | [george-resume](../george-resume/SKILL.md) |

Mixed tasks serve the current delivery goal first: read-only investigation does not automatically turn into development; settled plans are implemented directly; new decisions are registered before implementation; every implementation is verified afterwards, and long tasks also save checkpoints.

The routing table and module entries are for navigation only. After choosing, actually open the full text of the corresponding main playbook or workflow before executing; never fill in steps on your own after reading only the index.

Inside the mode, modules are chained by reading the needed module files, not by relying on the host to auto-trigger skills again. `disable-model-invocation` restricts automatic selection; it does not prevent this mode from reading modules by path.

Read only the modules you need. When a specific project requires the full S01–S11, comply; do not bypass it with lightweight routing. Escalate depth when a new problem is high-risk, goals conflict or evidence is insufficient; routine sub-actions under an already frozen strategy get only incremental checks.

## Constraints throughout

- Keep facts, user reports, inferences, predictions and unknowns separate. Multiple restatements of the same source count as one evidence group. Conclusions from past agents are not user preferences or independent evidence.
- Proceed directly with authorized local preparation and fixes. Authorization covers only the specified objects, operations and scope; the skill cannot authorize publishing, spending, customer messages or global configuration changes on the user's behalf.
- Accept by the real delivery form. Report separately: file exists, tests pass, UI saved, real run, platform effect, user adoption, revenue realized.
- On consecutive failures, check the shared premise and the first failing step; do not retry indefinitely under the same conditions. When an external operation's result is unknown, reconcile first; do not resubmit.
- Do only the current task. Keep the user's chosen products, directories, models and workflows; changing them requires a current basis. Do not fix unrelated configuration along the way.
- At wrap-up, state the result first, then the actual evidence and unfinished items. If the user wants Markdown, deliver Markdown; if they want a finished product, check the product itself—never hand over only the build script.

For theoretical positioning see [theory mapping](references/theory.md); for principle evidence see [sources of experience and boundaries](references/evidence.md); for host capabilities and invocation see [host adaptation](references/hosts.md). These are on-demand references; loading all of them every round is not required.

## Full engineering capability

Before engineering and long tasks, read the [integration contract](references/integration.md) as needed. All 23 playbooks adapted from pstack (Poteto) have real entry points inside George's domain modules; the [24 engineering principles](principles/INDEX.md) keep their full mechanisms and scope boundaries. Choosing a lightweight flow does not switch off the deeper capabilities.

When a task needs independent design, adversarial review, evaluation or partitioned verification, read the corresponding workflow; with authorization and host support, run the independent-agent steps; without the capability, honestly label it self-review or unverified. Planning, implementation, acceptance and release each have their own completion criteria; high-consequence real-world decisions go through the theory loop, while engineering implementation still goes through full acceptance.

For usage, help and per-host status see [usage and acceptance](references/使用与验收.md). When asked to introduce the architecture, answer with current real capabilities and evidence without starting the whole flow.
