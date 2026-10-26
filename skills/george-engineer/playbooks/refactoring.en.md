# Refactoring and migration

Entry condition: structure changes, behavior is preserved. New features or existing defects found along the way are listed separately, never silently mixed into the equivalence goal.
1. Pin the behavior contract before moving structure. Record old behavior with real inputs/outputs, characterization tests, snapshots, replays or equivalence tools; lint/typecheck cannot replace a behavior baseline.
2. Map existing callers and the target data structure; explain which branches, illegal states, tracing layers or hidden state the new structure removes. Without such a gain, keep the plain code.
3. Read [design contest](../../george-design/workflows/architect-arena.md) to compare necessary structural options. For large migrations use [custom run](../../george-orchestrate/workflows/figure-it-out.md): remove dead code first, then build the necessary foundation.
4. Migrate in small steps, keeping the behavior baseline at each step. Enumerate code, strings, config, docs, serialization and dynamic callers; read back renames one by one. When internal consumers can migrate together, migrate them all and delete the old API; do not accumulate dual paths.
5. When external consumers or live data truly need compatibility, write a phased migration, observation, rollback and the conditions for deleting the old API. An isolated branch may be temporarily unbuildable, but that state is never a releasable unit; state the boundary where full verification is restored.
6. Compare old and new output on the real artifact, measure necessary performance, check dependency direction and persistence compatibility. Claim unchanged behavior only after equivalence is proven. Revert abstractions that do not lower reading burden.
7. The delivery order reflects the evidence: behavior baseline → subtraction → structural migration → cleanup; handle needed version delivery via [PR delivery](opening-a-pr.md).
Deliverable: preserved behavior, structural gain, equivalence evidence, migration and rollback status.

Source: pstack `skills/poteto-mode/playbooks/refactoring.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
