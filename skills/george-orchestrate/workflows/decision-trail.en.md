# Reviewable decision trail

For long tasks, later review after the user leaves, and evaluations/migrations, create an append-only decisions.tsv with fields: time, unit, version, observation, decision, reason, evidence path, result, next step. Record only decisions/pivots/checkpoints/rollbacks; do not copy chat.

Each round, first read the last checkpoint and identify what others added. Multiple workers each write their own log, merged by reference by the coordinator, never contending for the same file; existing logs are not overwritten. For credentials, record only how to obtain them.

At the end, compare the log with this round's real tool traces and open every key piece of evidence; an independent reviewer checks for false completion, missed pivots, version mismatches and risks, outputting Attention items. Keep unknown where evidence is insufficient. The log may stay local and is committed only if the project requires audit; a log never automatically authorizes long-term polling.
