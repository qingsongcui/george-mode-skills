# Prototype to decide

1. Write down the specific question the prototype must settle: layout, density, interaction, behavior, timing or feasibility. If there is no choice to settle, go back to feature development. Settle factual disagreements that can be measured by observation first; product preferences remain the user's call.
2. When the direction is open, collect citable references and propose two or three substantively different directions; do not reopen a direction the user has already chosen. Build with the lightest stack in a separate scratch directory; never modify the production baseline.
3. Put visual options side by side in one switcher; run behavioral options on the same input and metrics. Prototypes may be rough and unabstracted, but must not pollute business data or leak credentials.
4. Actually operate, render, screenshot or measure on a matching surface. Prove the prototype really triggers the behavior being compared: a nice picture does not prove interactivity, and a timing simulation does not prove production performance.
5. Give evidence, trade-offs and a recommendation, and keep the prototype openable. After a choice is made, implement it properly via the [feature playbook](../../george-engineer/playbooks/feature.md); do not call experimental code a production deliverable.
Deliverable: the open question, each option, observations, recommendation and prototype path.

Source: pstack `skills/poteto-mode/playbooks/prototype.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
