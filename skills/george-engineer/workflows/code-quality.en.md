# Behavior tests, types and code cleanup

## Tests

When the user explicitly asks for TDD, or a bug has a cheap, clear local reproduction: write a minimal behavior test → confirm it actually fails because the target behavior is wrong → minimal fix → the same test passes → relevant regressions. A red light from a compile failure, missing dependency or wrongly written test does not count as reproducing the original problem. For expensive, complex tests use the nearest real executable check; do not invent a test for a one-line copy change.

Testing a test: deliberately breaking a return value / side effect / dedup should make it fail; refactoring internals with unchanged behavior should let it pass. Do not compute expectations from the code under test, and do not fake coverage with loose truthy assertions. Pair negative cases with positive ones to prove the observer can see the behavior.

## Structure and TypeScript

First eliminate illegal combinations with state machines, discriminated unions, tables/registries and domain models; parse external data at the boundary and use trusted contracts internally. Re-validate when concurrency or persisted state changes the guarantees. In TypeScript prefer deriving from the authoritative schema, exhaustive switches and branded semantic IDs; remove unjustified any/as/non-null assertions. Strengthen types only as far as needed to avoid real partial functions/illegal states; no showing off.

## Pre-review cleanup

Read the final diff; delete unevidenced defenses, valueless single-caller wrappers, duplicated state, empty abstractions, leftover debugging and AI boilerplate. Keep comments that state non-obvious reasons the code cannot express, interface contracts and necessary licenses; do not apply "delete all comments". Complex changes get a second look from someone who did not write them. Run relevant checks after trimming; tidy wording is not functional verification.
