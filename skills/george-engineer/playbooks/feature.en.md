# Feature and interface development

Entry condition: a clear request to add or change behavior. Pure explanation requests go to investigation; continue directly with an already chosen design.
1. Read [structural investigation](../../george-design/workflows/how-why.md) and determine callers, inputs, state, boundaries and existing constraints along the real call path. Write data shapes and invariants first, logic second.
2. When there is a substantive architectural choice, read [design contest](../../george-design/workflows/architect-arena.md). Compare at least structurally different options; ordinary local changes need no contest. Link important product/architecture trade-offs to george-decide's pre-registered rationale.
3. For non-trivial multi-step tasks leave the four throughput checks: blocking prerequisites, independent artifact streams, shared mutable objects, minimal safe split. Explain any item that does not apply. Fix shared types first, parallelize after.
4. Use the [orchestration contract](../../george-orchestrate/SKILL.md) to assign implementation and independent review. Each work unit gets file ownership, a caller example, data shape, no-edit zones and acceptance evidence. Cross-module coupled features are coordinated by one owner; never let several agents write a shared interface at once.
5. First complete one runnable vertical path, then spread out to independent branches. Verify each unit when it finishes; when a shared primitive changes, check every consumer. When counter-evidence appears, remove the invalid changes it supported.
6. Run [project verification](../../george-verify/workflows/project-verification.md), covering the real happy path, key failure paths, and persistence/restart or permission boundaries. Wrong surface, unobservable or inconclusive never count as passing.
7. Contested or high-consequence changes go through [adversarial review](../../george-design/workflows/interrogate.md). Organize delivery in a verifiable order: foundation, feature, integration. When a PR is needed, go to [PR delivery](opening-a-pr.md).
Deliverable: change in user behavior, choice and rationale, verification evidence, what is actually unfinished.

Source: pstack `skills/poteto-mode/playbooks/feature.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
