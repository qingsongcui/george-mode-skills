# Skill authoring and updating

1. First read the applicable skill-creator; define when it triggers and when it does not, inputs, steps that must not be lost, artifacts and pass conditions. Map source skills capability by capability; a summary is not an equivalent implementation.
2. Put stable rules in the entry, long procedures in on-demand references, and deterministic actions in rerunnable scripts. Keep the original source, version and reason for adaptation; all references point to real files inside the package, not depending on the original skill still being installed.
3. If the user has asked to create or modify, implement directly; other business reviews only propose improvements and never write global memory on their own. New rules state their scope, counterexamples and removal conditions.
4. Verify frontmatter, internal links, scripts, dependencies, non-overwriting installation, and reachability from the main entry to leaves and tools.
5. Verify behavior with [blind testing](eval.md) or independent real tasks; anything touching structural safety includes at least one counterexample that should fail. Record actual reads and artifacts; static checks cannot replace behavior evaluation.
6. After comparing old and new versions, publish to the local skill source, keep a rollback snapshot, and update the matrix and version hashes. Across hosts, record install/discovery/execution evidence layer by layer. Create a PR only if the task needs it.
Deliverable: concrete changes, capability coverage, real acceptance, unverified capabilities.

Source: pstack `skills/poteto-mode/playbooks/authoring-a-skill.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
