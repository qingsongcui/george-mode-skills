# One-off performance issue

1. Capture a baseline trace at the correct entry point with a realistic workload. Record data volume, history, state, concurrency, cache, work completed, error count, clock and environment. Read [measurement audit](../../george-evaluate/workflows/benchmark.md) first.
2. Locate the limiting factor from hotspots and system counters, and explain why it is not twice as fast; do not imagine a performance ceiling from source. Investigate the mechanism with how, and try in cost order: skip useless work → don't repeat → reduce frequency → defer → move off the critical interaction → parallelize → make each pass cheaper.
3. Change one mechanism at a time. Compare architectures when needed; keep implementation and review separate. Keep the measurement tool fixed, capture a post-change trace, and compare on the same basis as the baseline.
4. Parse large traces into queryable tables; compare hotspots, end-to-end latency, work counts, errors and resource cost. Rule out cache hits, skipped work, client bottlenecks, one-sided untuned parameters and noise.
5. Stop when the target is met; revert on errors or regressions. Long-running iteration moves to [hillclimb](hillclimb.md). Keep measurement commands and evidence per [PR delivery](opening-a-pr.md).
Deliverable: baseline → result, units, sample count/dispersion, mechanism and end-to-end impact; small samples do not claim general improvement.

Source: pstack `skills/poteto-mode/playbooks/perf-issue.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
