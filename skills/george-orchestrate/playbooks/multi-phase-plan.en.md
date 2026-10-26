# Multi-phase plan delivery

When the user only wants a plan, the plan is the artifact; do not implement, create execution queues or publish. When the user has explicitly asked to plan and do at the same time, do not ask for a go again.

1. Read the goal and current state and confirm a plan is needed. Obvious one- or two-file changes do not require a big table. When key facts are unknown, do read-only verification or an isolated prototype first, keeping prototype evidence.
2. Each unit states: id, dependencies, ownership, file scope, actual deliverable, user-visible behavior, execution playbook, behavior check, real-surface verification, performance applicability, review gate, rollback/stop and delivery method.
3. Every checkbox has an evidence path and pass predicate. Write unit/live/perf applicability separately; non-applicability needs a reason, and important real behavior cannot be replaced by "unit tests only". Verification lanes cover by risk; a fixed ten lanes is no longer required.
4. Check the DAG is acyclic, file ownership does not conflict, prerequisites are verified first, and each unit is verifiable at its end. Separate facts in the plan from items pending decision.
5. Validate the [structure template](../templates/plan.json) with the [plan checker](../tools/check_plan.py). The checker reviews only structure/dependencies/evidence definitions; it cannot prove actual behavior or plan quality.
6. Deliver the plan, key choices, prototype evidence, check results and execution boundary. A plan-only request ends here.

Source: pstack `skills/poteto-mode/playbooks/multi-phase-plan.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root); adapted per the [George integration contract](../../george-mode/references/integration.md).
