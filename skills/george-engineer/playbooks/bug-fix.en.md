# Bug fix

Entry condition: fixing a reported error. Reproduce the error by running it first; do not guess from source alone.
1. Reproduce through the same kind of entry point where the user hit the problem; record version, input, state, error and minimal trigger. Operate it yourself whenever you can; only when the target surface is genuinely unreachable, explain why and ask the user for evidence.
2. Build candidate mechanisms with [how/why](../../george-design/workflows/how-why.md). Each time, choose the observation that best discriminates between hypotheses and bisect the range; add temporary logs, counters or traces when needed. For errors that appear only after a restart, check persisted state first.
3. Trace to the point where the first wrong state is produced. If a legal state is unhandled, fix it at that boundary; if an illegal state is being produced, fix the producer—never mask it by swallowing errors, clamping or infinite retries. If two consecutive failures share the same premise, test that premise before trying another patch.
4. Once evidence supports the mechanism, design a minimal fix. When it crosses boundaries or has several structural options, go to george-design; separate implementation from review. Mechanical edits can be delegated; the main owner checks the diff against the original reproduction.
5. When a cheap local test path exists, follow [TDD](../workflows/code-quality.md): leave a failing behavior test first, then fix and rerun. Under the same conditions the original surface must go from failing to passing; keep before/after output; a test must not invent its own expectation to prove itself.
6. Search for other instances of the same error pattern and fix affected ones within scope. Remove patches built on invalidated assumptions, temporary debugging and useless defenses. Run relevant regressions and finish via [PR delivery](opening-a-pr.md).
Deliverable: trigger, root cause, change, before/after evidence on the same surface; if it could not be reproduced, call it only a hypothetical fix.

Source: pstack `skills/poteto-mode/playbooks/bug-fix.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
