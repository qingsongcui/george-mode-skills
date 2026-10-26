# Blast radius and task clarification

A small diff can still change many consumers. Enumerate exports, callers, config, persisted fields, cache keys, protocols, toolchains and docs; find "the one fact that must be true for this change to be safe" and prove it with search or a run. Output the affected parties, the evidenced safety condition and uncovered edges.

When the user asks to restate the requirement, restate the outcome, scope, acceptance conditions and ambiguities in your own words; do not quietly write assumptions awaiting confirmation into the goal. When the user asks to improve task quality, first identify the real consumer and outcome, remove over-specified implementation details, keep constraints and metrics, and give a clearer task statement; do not inflate a small request into a big project on your own.

When sharpen is used on a task that has already been asked to start, fold the original sources, methods and independent checks an expert would use into the actual execution, then complete the work; deliver only a rewritten prompt when the user explicitly asks for a prompt. Keep the user's necessary constraints; never drop them on the user's behalf.
