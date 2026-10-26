# George integration contract 0.3.0

pstack's (Lauren Tan / @poteto, MIT, https://github.com/cursor/plugins/tree/main/pstack) 23 playbooks, 24 principles and accompanying specialized workflows are the functional source; the adapted files in this package are the execution entry points, with attribution in NOTICE.md at the package root. George keeps the full operating mechanisms and changes trigger strength, authorization assumptions and host binding.

## Depth decides how, not whether

- Lightweight: self-contained small tasks, delivered directly with relevant checks.
- Standard engineering: investigate the call chain → necessary design → implementation → real-surface verification → review → delivery. Relevant steps cannot drop evidence requirements for being "lightweight".
- Complex/high-consequence: competing designs, independent review, behavior evaluation, project verification tools, dependency orchestration and recovery records are all available. High-consequence real-world trade-offs go to george-decide, with important predictions pre-registered.
- Long-term projects: reuse the above, plus persistent state, a single writer, dependency graph, version-bound verification, stopping and resumption.

## Delegation and hosts

George workflows require independent sub-agents for complex design contests, independent review, partitioned investigation and blind testing, provided the user has invoked this mode and the host allows delegation and has the tools. Simple tasks do not require multiple agents. Every agent must know it is not the only writer, must not revert others' changes, and receives ownership, evidence, acceptance and no-edit scope.

Without delegation capability, execute serially and clearly label it self-review; the high-consequence release gate requiring independent review remains unmet and cannot pass by renaming. When George is enabled, choose this round's sub-agents by host: Codex per [Codex autonomous dispatch](../../george-orchestrate/adapters/codex.md); Cursor per [Cursor autonomous dispatch](../../george-orchestrate/adapters/cursor.md); Grok Build / `grok` CLI per [Grok autonomous dispatch](../../george-orchestrate/adapters/grok.md); Google Antigravity per [Antigravity autonomous dispatch](../../george-orchestrate/adapters/antigravity.md); other hosts keep their actual model settings. Cross-review with different available models is allowed; changing global configuration or falsely claiming multiple models is forbidden.

Reviewers read facts independently; consensus from same-source evidence or the same model cannot replace a real run.

## Adaptation rules

Reversible, authorized work is completed directly. External messages, publishing, spending and merging/deploying follow this round's explicit authorization; Poteto's broad default for external actions is not used. Do not reset unknown workspaces, delete unarchived work, or automatically change the theory/global memory. The user's specified products and goals are kept.

Complex tasks run in parallel only with independent artifacts; the main agent is responsible for verification and shared state. Project source and persistent default model configuration are kept; Codex, Cursor and Grok per-round dispatch parameters may be chosen per their respective autonomous-dispatch adapters. When a tool is missing, choose a verifiable alternative; if it cannot be verified, write the gap—software being present does not mean the capability is in effect.

Output keeps only facts, rationale, changes, acceptance and unfinished items that affect decisions. Principles need not be named one by one, and English punctuation restrictions are not imposed. PRs follow the repo template and current completeness; unfinished work may use draft; do not force a PR for read-only explanations or local deliverables.
