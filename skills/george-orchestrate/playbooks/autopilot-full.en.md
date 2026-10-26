# Autopilot for an independent queue

Precondition: the user has authorized implementing this queue; merging happens only if this round's authorization covers it. If only a plan is wanted, output the plan without executing. Interdependent changes use autopilot-stack.

1. Fix the queue boundary and completion predicate; each independent PR has one owner responsible from implementation to authorized delivery; the root coordinator is responsible for independent verification and never treats the owner's self-test as the final verdict.
2. Each owner gets an independent worktree, branch and brief, and understands/designs/implements first. Open PRs early when appropriate so CI runs in parallel; use draft for unfinished work per repo rules; an early PR is never completion.
3. The owner reports the exact code-ready SHA, baseline, commands and evidence, and freezes writes for that round. The root sends a verifier who did not author it to test real behavior per the risk matrix and record a version-bound verdict; the owner of the queue verifies the report.
4. The owner handles conflicts, comments and CI, reporting every subsequent SHA. Major behavior changes rerun the corresponding coverage matrix; small changes also have an independent party check affected behavior. An old head's green does not stand in for a new head; old verdicts are not reused automatically.
5. Before merging, check whether trunk changes affect calls, contracts, runtime, dependencies or integration points. For relevant changes rebase/integrate first, then verify; record the basis for treating drift as unrelated. patch-id can help judge differences but does not alone prove integration safety.
6. Enter Shipping only when new-head CI, independent evidence, forge gates and user authorization are all satisfied; without authorization, deliver merge-ready. Owners must never turn a fail into a pass themselves.
7. When the user explicitly pauses, stop dispatching, tell all owners to stop new external actions, and save the live state. The root finally checks every actual merge state against the user's goal.
Artifacts: per-PR owner, head, verification result, CI/delivery status and reasons for anything unfinished.
Source: pstack `skills/poteto-mode/playbooks/autopilot-full.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root); adapted per the [George integration contract](../../george-mode/references/integration.md).
