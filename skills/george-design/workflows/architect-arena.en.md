# Design contest, selection and synthesis

Triggers: cross-module ownership or data shape changes, an important unsettled structural choice, a novel interaction. Read how; add why when changing the motive behind an existing layering. Do not reopen a design contest for a settled design or a simple local change.

1. First write user behavior, caller usage, data structures, invariants, failure states and constraints. Express the design as types/signatures, module boundaries, data flow and a minimal call example; do not pile up implementation first.
2. Fix three to six judging criteria, e.g. contract correctness, representability of illegal states, consumer burden, migration cost, reader tracing cost, verifiability; state the budget and which criteria cannot be sacrificed.
3. Produce at least two structurally different options. When independent agents are available, give the same brief to different candidates writing into separate directories; cross-model if conditions allow. Without that capability, compare them yourself and label it "single-designer"; do not claim independent exploration.
4. Each candidate provides a caller sketch, core types, module diagram, one-page rationale, risks, the hardest counterexample and a verification path. Check red flags: parameter/boolean-flag explosion, phase modules without domain meaning, leaked storage types, single-caller wrappers, state synchronized in several places, error fallbacks that can never be reached.
5. A reviewer who did not implement any candidate judges all of them by the same criteria and picks one as the base; the owner verifies item by item and grafts only parts of other options with independent value, never splicing conflicting ownership models.
6. After synthesis, re-verify callers and invariants; keep rejected options and the reasons. Output the choice, trade-offs, risks and next step. When the user wants a "design checkpoint / plan only", stop at a reviewable plan; when implementation is authorized, move straight to feature/refactor.
7. If implementation keeps drifting from the sketch, go back and test the design against the data shape instead of patching endlessly.

A code contest uses the same flow: same task and data, isolated outputs, blind-labeled review, pick a base, graft sparingly, verify for real. For changes in evaluation mode use [blind testing](../../george-evaluate/playbooks/eval.md).
