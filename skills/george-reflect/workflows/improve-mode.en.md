# Continuous improvement of a personal mode

Sources include automate-me, reflect and correct. First distinguish "distilling preferences" from "proving a method works". Preferences come from the person's explicit words; agent-written text, duplicated profiles and parent-agent assignments are not independent user evidence.

Building or rebuilding a mode: check the existing mode, and read authorized history sharded by time period/project; default to the current workspace—a one-time authorization to scan everything does not become a future default. A candidate becomes a high-confidence habit only if it appears in at least two independent shards; keep counterexamples, outdated preferences and current corrections alongside. Ask a few questions for missing preferences; do not ask about facts existing evidence can answer.

Post-task review: analyze only the skills and tools actually used in the current session. Complex tasks use three independent perspectives: judgment bias, tools/process, and anomalous alternative explanations. The owner verifies each piece of evidence and outputs Accepted/Rejected/Backlog with reasons.

Land Accepted items only with current authorization to modify skills; do not re-ask for authorization already given. Without authorization, give only reviewable suggestions. Deterministic constraints go preferably into types, metadata, lint or scripts rather than stacking permanent bans. A one-off correction is fixed within scope first; project rules are updated only with appropriate authorization and repeated evidence. Memory and the master theory text have their own modification boundaries.

After updating, run behavior verification and record version and rollback method; compare real feedback with the prior goal, and avoid declaring a rule effective just because you like it.

## Structural repair of recurring errors

When an error repeats at least twice, group by class and look back at real commits, reverts, comments and user corrections. Priority: architecture removes multiple state sources/error entry points → types make bad states unconstructable → lint or CI points to the specific correct entry → behavior tests → doc rules that rely on judgment only.

Every new check must fail on a real historical error and then prove the current fix passes; run the same command locally and in CI. When there are many legacy errors, first limit new ones rather than suddenly blocking all legacy. Record the mapping from rules to actual enforcers; redundant instructions already removed by structure can be deleted. Exceptions state reasons and deadlines; no permanent escape. Handle the most frequent errors within scope; do not refactor without bounds in the name of correction.
