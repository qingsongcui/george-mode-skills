# George mode 0.3.0 usage and acceptance

Invoked on demand, layered by task weight. Theory, personal evidence principles, full engineering flows and runnable tools are in the same package; using George does not require installing pstack separately.

## Host invocation and discovery

All hosts share the same skill source directory and default to explicit on-demand invocation:

- **Codex**: type `$george-mode` plus the task, or choose from the skill menu;
- **Cursor**: type `/george-mode` or choose from the skill menu;
- **OMP**: the native command is `/skill:george-mode`, or choose from the skill list; the install script also provides an OMP-specific `/george-mode` file command alias.
- **Grok CLI**: type `/george-mode`; it discovers the installed `~/.agents/skills/george-*`, which can be checked with `grok inspect`.
- **Antigravity**: type `/george-mode` (supports Antigravity 2.0, IDE and the `agy` CLI); it discovers the installed `~/.gemini/config/skills/george-*`, which can be checked with the Language Server's `GetAllSkills`.
- If the menu does not show it, you can tell the agent to read the skill entry `SKILL.md`; manual reading is not the same as native discovery. For detailed execution differences and configuration see [host adaptation](hosts.md).

Example: `Use George mode to fix this problem and verify through the real entry point.` A settled plan is carried out directly; if only an explanation/plan is wanted, deliver that artifact. Complex tasks automatically bring in design contests, independent review, evaluation and orchestration according to actual risk; simple tasks keep relevant acceptance without requiring the full theory or multiple people.

When OMP 0.3.3 is enabled, first actually read [OMP autonomous dispatch](../../george-orchestrate/adapters/omp.md). When Grok 0.3.4 is enabled, first actually read [Grok autonomous dispatch](../../george-orchestrate/adapters/grok.md). When Antigravity 0.3.5 is enabled, first actually read [Antigravity autonomous dispatch](../../george-orchestrate/adapters/antigravity.md). For every subsequent task in the current George session, the controller automatically decides whether to delegate and the responsibilities, models, effort, concurrency, budget and recovery, without asking the user to choose technical parameters; small tasks are still finished directly. This contract does not become a global standing rule, nor does it expand external operation permissions.

OMP role request values are not actual runtime values and must be checked per worker; hard cancellation, reviving parked workers and reclaiming descendant processes follow what the current host actually measures.

## The 11 module entries

In-skill navigation uniformly uses relative paths, resolving without escaping the skill root on the Codex, Cursor, OMP and Grok hosts:

| Entry | Purpose |
|---|---|
| [george-mode](../SKILL.md) | Main routing, weight tiers, authorization and evidence boundaries |
| [george-investigate](../../george-investigate/SKILL.md) | Original evidence, project and history investigation |
| [george-decide](../../george-decide/SKILL.md) | Theory loop and pre-commitment for important trade-offs |
| [george-design](../../george-design/SKILL.md) | how/why, architect/arena, prototype, interrogate |
| [george-engineer](../../george-engineer/SKILL.md) | Features, bugs, refactors, performance, forensics, visual parity, delivery |
| [george-deliver](../../george-deliver/SKILL.md) | General making, configuration and deliverables |
| [george-verify](../../george-verify/SKILL.md) | Real-surface verification, project verification tools, platform read-back |
| [george-evaluate](../../george-evaluate/SKILL.md) | Blind tests, measured numbers, skill behavior verification |
| [george-orchestrate](../../george-orchestrate/SKILL.md) | Multi-phase, queues, PR follow-through, pause and resume |
| [george-reflect](../../george-reflect/SKILL.md) | Theory/prediction feedback, personal mode and structured correction |
| [george-resume](../../george-resume/SKILL.md) | Original goal, authorization scope and live resumption |

## Core specifications and references

- [Host adaptation](hosts.md): Codex, Cursor, OMP, Grok invocation syntax, permission boundaries and execution differences
- [Integration contract](integration.md): standard for absorbing pstack playbooks and principles
- [Decision loop](decision-loop.md): goals, assumptions, falsifiers, predictions and stop conditions
- [Verify before deliver](verify-before-deliver.md): execution and acceptance floor
- [Theory mapping](theory.md): mapping method to execution
- [Sources of experience and boundaries](evidence.md): experiential principles, reflexivity and evidence boundaries

## Delivery package

The methods, host adapters and tools needed to run are all in this package, with no dependence on the author's private materials. Historical host verification cannot prove the current install environment works; after installing, re-verify against this machine's capabilities.

## Acceptance status

- The 11 local modules share the same source; install links existing, host loading and real task success are accepted separately. One host's success cannot be generalized to others passing.
- Regression tests for state, plan, verification runner and the GitHub watcher are in `tests/` and `tools/pstack/watch-pr/*.test.ts`.
- Help navigation uses host-safe relative links, eliminating cross-host broken links and skipped-check gaps caused by old symlinks.
- Codex keeps `$george-*` and `agents/openai.yaml`; Cursor keeps `/george-mode`; OMP keeps `/skill:george-mode` and its dedicated command alias; Grok keeps `/george-mode` and `adapters/grok.md`, without a separate `~/.grok/skills/george-*` install; Antigravity keeps `/george-mode`, `~/.gemini/config/skills/george-*` and `adapters/antigravity.md`. Each host's existing model and credential configuration stays unchanged.

## Installation, maintenance and rollback

Install operations run from the unpacked package root, not from the current business project or this file's directory. Read PORTABLE.md in the package root first. Run `python3 scripts/install.py` to preview, `--apply` to install; existing paths with the same name are refused. To uninstall, `--remove --apply` removes only links pointing to this package.

For the standalone package, run `python3 scripts/verify_package.py` to check file integrity and required resources; it does not prove host model services work. `python3 -m unittest discover -s tests` runs the package's regression tests.
