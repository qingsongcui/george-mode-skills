# Partitioned parallelism, contests and verification matrix

1. First write a decidable completion predicate, and choose partitioned coverage, same-task contest or cross-checking. Partitions use mutually exclusive inputs/files; design contests go to george-design's arena.
2. List a coverage matrix by risk with fields feature/boundary/data state/platform/expected/evidence/owner. Headcount is set by independent artifacts, budget and host slots—not mechanically ten people or fixed models.
3. Each worker receives the same fixed contract, actual head/input hash, owned paths, no-edit zones, run commands, time limit and report path; it is told it is not the only writer and must not revert others' work. Write operations are isolated in a worktree or directory.
4. Report PASS/ISSUES/BLOCKED, executed commands, actual artifacts and version. The main agent personally checks outputs; a coverage gap is not a PASS. At most one redispatch without a root cause; if it fails again, check the shared premise first.
5. For contests, set selection criteria, termination conditions and the disposition of remaining workers in advance. As the budget nears its limit, stop new dispatches first, merge and verify existing artifacts, and leave no orphaned processes.
6. The coordinator maintains the coverage table and handles shared state and integration; report uncovered items and stragglers. Different agents reading the same material are not independent sources.
