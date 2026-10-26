# Blind testing and capability evaluation

1. First fix what is compared, the task distribution, success behavior and three to six observable scoring criteria. Scoring notes go only to the judge and are saved in advance; negative controls must be distinguishable.
2. Give each subject its own naturally named project directory, with identical inputs, tools, budget and environment, changing only the variable under evaluation. Directories/files/prompts visible to candidates carry no evaluation hints such as eval, judge, score, rubric, candidate or benchmark; normal product test files may exist but must not leak hidden criteria.
3. Use the same natural user request; do not tell a candidate there are others, and do not ask it to self-report which skills, principles or chain of thought it used. Verify skill reads through tool traces and artifacts.
4. Run candidates independently; record failures, timeouts, cost/time and missing outputs—do not cherry-pick successes. Cross-model evaluation uses genuinely different models only when tools allow and user settings support it; the same model in different roles is not cross-model.
5. One blind judge scores anonymous A/B outputs on the same scale without seeing model or version labels. Run objective behavior checks separately; judge opinions cannot override actual errors.
6. The main owner reads every artifact and this task's tool traces, checking which leaves were actually read, code shape and runtime evidence; self-claims do not prove the execution chain. Access only this round's candidate records; do not read unrelated project history along the way.
7. Trace subjective disagreements item by item; small samples only describe performance in that scenario. When generalization is needed, expand real tasks and repeated trials, reporting distribution and limitations. Promote a version only when evidence supports it.
Deliverable: plan, unsealed hidden criteria, anonymous results, real checks, judge and owner verdicts, rerunnable path.

Source: pstack `skills/poteto-mode/playbooks/eval.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
