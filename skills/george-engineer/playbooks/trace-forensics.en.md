# Forensics on existing trace data

1. Identify the format, sampling window and completeness of the given cpuprofile, JSON/gzip, spindump or heap snapshot. Analyze the fixed data; do not re-run on your own and change the conditions.
2. For large data, first convert it with a format-appropriate parser into queryable tables/SQLite, one row per sample/frame/node; keep the original file and conversion commands.
3. Query hotspots, call chains, waiting threads and wait reasons; for memory issues, follow retention chains to the root. Aggregate numbers must state the denominator and the repeated-sampling basis.
4. Map file/symbol/line via the symbols shipped with the data; when symbols are missing, add a mapping or mark it unattributable—do not guess source from function names.
5. With paired captures, compare on the same basis; with only one capture, label conclusions as evidence-supported hypotheses. Give the next observation that would discriminate between alternative explanations.
6. Deliver a traceable diagnosis, queries and evidence; move to bug/perf only if the task already includes a fix.

Source: pstack `skills/poteto-mode/playbooks/trace-forensics.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
