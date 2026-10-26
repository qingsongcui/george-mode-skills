# Continuous single-task execution

1. Write done as a real, checkable predicate, and set the budget, stop/revert rules, authorization and evidence that must be saved. "How long it has worked" cannot be the only end condition.
2. When there are events, wait on host events; without events, back off checks according to how fast results change; the current session may keep running. Create host-native automation only when the user explicitly asks for later/continuous monitoring; never substitute a hidden shell for scheduling.
3. Each round: smallest evidenced change → real check → keep effective changes or revert failed attempts → append to decisions. Independent artifacts may be delegated; the owner verifies.
4. Resolve in-scope obstacles yourself; record unrelated improvements without expanding the task; keep necessary independent fixes reviewable. On failure, trace the root cause first; for unknown platform results, reconcile first.
5. Report the actual state when a phase completes, the goal is met, a budget/stop condition triggers, or it truly cannot continue. On a plateau, change approach—never lower the predicate to pass; no unbounded consumption.
6. Final real acceptance, state check and a clean checkpoint; clean up this task's monitors.

Source: pstack `skills/poteto-mode/playbooks/autonomous-run.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root); adapted per the [George integration contract](../../george-mode/references/integration.md).
