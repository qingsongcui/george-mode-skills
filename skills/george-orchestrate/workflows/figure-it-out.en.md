# Custom flow for complex tasks

For migrations or complex deliveries with no existing playbook and many callers; a single routine task uses a dedicated playbook, and multi-day projects use orchestrate.

1. Define the user-visible completion predicate, scope, authorization, budget, risks and behavior that must not break. Identify the biggest unknown and put cheap, high-information verification first.
2. Understand the system first, then establish a verification baseline on real artifacts. Use prototypes to settle factual disagreements when needed; important trade-offs go to george-decide.
3. Design phases, dependencies, ownership, artifacts, verification and recovery conditions. Each phase is checkable; "improve" or "optimize" is not a completion standard.
4. Run a pilot to validate the tools/process before rolling out. Prefer deterministic scripts over many agents repeating manual operations; verify each unit right after changing it.
5. Keep writing the [decision trail](decision-trail.md); pivot when evidence goes against you, keeping revert records. INCONCLUSIVE is not a pass; when the budget runs out, keep remaining items honestly.
6. Do final real delivery acceptance and independent review, reporting the actual state of the completion predicate.
