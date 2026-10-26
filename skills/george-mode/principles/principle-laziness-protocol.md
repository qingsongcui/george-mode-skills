# Laziness Protocol

- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.

## George scope (George 适用边界)

Apply when the trigger fits; results carry evidence, scope limits and counterexamples. Important real-world decisions go through the theory loop; ordinary engineering does not require full operational record-keeping.
