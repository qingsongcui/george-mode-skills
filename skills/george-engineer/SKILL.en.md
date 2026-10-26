# Engineering domain pack

> English translation of [SKILL.md](SKILL.md). Hosts load `SKILL.md`; this file is the full English body.

Inherit George's goals, theory, evidence and authorization boundaries; first read the [integration contract](../george-mode/references/integration.md). Check project rules, current changes, and real run/test entry points. When only an explanation or plan is requested, do not implement automatically.

| Task | Playbook |
|---|---|
| Feature / interface | [feature](playbooks/feature.md) |
| Bug fix | [bug-fix](playbooks/bug-fix.md) |
| Behavior-preserving refactor | [refactoring](playbooks/refactoring.md) |
| One-off performance issue | [perf-issue](playbooks/perf-issue.md) |
| Iterative metric optimization | [hillclimb](playbooks/hillclimb.md) |
| Live runtime forensics | [runtime-forensics](playbooks/runtime-forensics.md) |
| Existing trace analysis | [trace-forensics](playbooks/trace-forensics.md) |
| Visual-parity migration | [visual-parity](playbooks/visual-parity.md) |
| Engineering / PR delivery | [opening-a-pr](playbooks/opening-a-pr.md) |

[Design contest and independent review](../george-design/SKILL.md), [multi-phase orchestration](../george-orchestrate/SKILL.md) and [blind behavior testing](../george-evaluate/SKILL.md) are full companions, brought in by risk and task type.

Common execution: data shape before logic; for non-trivial work write the four items—blockers / independent artifacts / shared state / minimal split; separate write areas, one owner; separate implementation from high-risk review; verify at the end of each unit; evidence on the real surface decides completion.

Code rules are in [behavior tests and types](workflows/code-quality.md); docs/PRs in [technical writing](workflows/writing.md). Read the full leaf principles from the [index](../george-mode/principles/INDEX.md) rather than restating slogans. A project without Git can still be completed as a local deliverable; a PR is not mandatory.
