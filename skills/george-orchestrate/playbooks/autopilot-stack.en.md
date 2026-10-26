# Dependent change stack

For queues with prerequisite dependencies, where the user wants to review first or retains merge rights. Reuse autopilot-full's implementation and independent verification, replacing the topology and merge rules.

1. Order by DAG; dependents are created from the exact tip of the parent branch, not as unrelated parallel branches from trunk. Each owner maintains only their own slice and reports the tip and parent branch.
2. The root coordinator alone rebases/retargets the chain; owners must not reorder, merge, close PRs or enable auto-merge. After each root update, owners first check the new base and their write lease. Conflicts are resolved by the relevant slice owner, then integrated centrally.
3. The root PR targets trunk, children target their parent branch; check trunk drift and patch changes link by link, and update head evidence on any change. Do not depend on Graphite or platform-specific plugins.
4. Deliver a linear chain with a verdict per item, giving root/tip links and each layer's purpose. After the user authorizes landing, enter Shipping and stop other writers; problems during landing stop first and are re-coordinated—never rewrite the chain while merging.
Artifacts: current dependency graph, the single topology writer, per-layer version/evidence, a reviewable stack.
Source: pstack `skills/poteto-mode/playbooks/autopilot-stack.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root); adapted per the [George integration contract](../../george-mode/references/integration.md).
