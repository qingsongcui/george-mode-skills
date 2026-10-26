# Theoretical positioning and scope

george-mode's decision method is written in full in the [decision loop](decision-loop.md), and the execution and acceptance floor in [verify before deliver](verify-before-deliver.md). Both are self-contained and need no external theory files, business ledgers or the author's private materials.

## Mapping method to execution

| Part of the method | Role in the skills |
|---|---|
| World and constraints | Check the current state and changes; refuse to substitute old state for the live situation |
| Actors, values and interaction | Distinguish goals, resources, capabilities, authorization and other parties' reactions |
| Evidence and causality | Trace original sources, deduplicate same-source evidence, keep competing explanations and falsifiers |
| Levers, action and risk | Compare baselines, alternatives, value of information, reversibility and stop conditions |
| Measurement, feedback and evolution | Clear definitions, real read-back, layered attribution and updates |
| Governance and AI | Keep human responsibility, rule boundaries, AI inference and authorization separate |

## File architecture

Keep the logic "analysis → plan and prior predictions → execution and observation → review and update → bounded rules". Concrete file names, numbering and archiving are decided by the current project's own rules; without project rules, no extra ledgers are created.

The method's source, personal experience and the task workspace are three different concepts. Using this method does not mean inheriting any project's goals, budgets, platform rules or thresholds.

The full theory toolkit (in Chinese, with English translations) is shipped in the repository's `theory/` directory as an optional reference; the skills do not require it at runtime.
