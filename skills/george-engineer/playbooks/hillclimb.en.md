# Controlled iterative optimization

1. Define the realistic workload, a single primary metric, direction, regression floor, budget and checkable stop condition. If a minimum number of attempts is used, set it in advance by research need; do not mechanically fix it at ten. If the complaint cannot be reproduced, fix the measurement task first.
2. Build a rerunnable measurement tool; prove its sensitivity with easy and hard workloads, then freeze the tool, data, metric and baseline. Output errors and work done; sample repeatedly and judge noise by median/distribution. Read [measurement audit](../../george-evaluate/workflows/benchmark.md).
3. Create decision.tsv; for each attempt record id, mechanism hypothesis, benchmark, change, before/after values, distribution, regression, keep/revert and reason. Read earlier rows each time to avoid repeating failures.
4. Change only one explainable mechanism per round; competing hypotheses use independent worktrees with the same measurement conditions. Implementation may be delegated; the metric and verdict stay with the owner. Never stack unmeasured changes.
5. Keep a change only if the gain exceeds noise and regressions pass; otherwise revert this round's own change. Each accepted change forms an independently verifiable unit. A simplification that does not hurt the metric may be kept but is labeled a simplification, not a performance gain.
6. On a plateau, switch hypothesis category, re-examine the mechanism, check the measurement tool; do not retry blindly. End by the pre-set rule when the target is met, the budget is used up, or remaining gains fall below cost; keep the not-achieved status rather than relaxing the target to fake success.
7. Run full relevant regressions at the end and summarize attempts and reasons for discarding. For unattended runs, borrow only the wake-up mechanism of [continuous run](../../george-orchestrate/playbooks/autonomous-run.md).
Deliverable: frozen baseline and target, final value, keep/revert counts, decision log, untried hypotheses and stop reason.

Source: pstack `skills/poteto-mode/playbooks/hillclimb.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
