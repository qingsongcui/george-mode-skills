# Runnable tools

All paths are relative to this skill directory. Tools never automatically dispatch agents, change models, publish or merge. Python tools depend only on the standard library; the GitHub watcher additionally needs Bun and gh.

## Persistent orchestration

`python3 tools/state.py --store /absolute/path/task.sqlite init` creates a task workbench. Other operations take JSON via `--input /absolute/path/request.json`, never inserting user content into the shell.

| Operation | Input |
|---|---|
| unit.put | id, owner, version (head or content hash), scope, state (pending/running/code-ready/blocked); changing owner additionally requires handoff=previous-owner-stopped |
| verdict.record | unit, version, verifier, level, evidence (real absolute file), observed_at |
| verdict.check | unit, optional required_level; exits 1 when evidence of the required level for the current version with intact file hashes is missing |
| inbox.push | unique id, unit, sender, report; retries with the same id are idempotent, conflicting content is rejected |
| inbox.read | none; reads only un-acked messages, rereadable after a crash |
| inbox.ack | id, evidence (post-handling receipt); archiving keeps the original message, no deletion |
| gate.put | id, question, optional suggested_default; a default cannot close a gate |
| gate.resolve | id, answer, source (where the actual user decision is) |
| frontier.set | items each with id, parent (null for root), version, source, observed_at; parents before children, no duplicates |
| standing.add | id, instruction, source |
| status | none; full facts and content hash—category counts do not stand in for content changes |

level is static, unit, real-surface, independent-real-surface, blocked or failed. Each unit+version+scope keeps its current verdict, with historical changes appended to the event table; a later failure overrides an earlier success. The independent verifier cannot be the owner; evidence must exist and its hash is stored; the tool cannot authenticate real identity or evidence semantics, so the owner still has to check content.

SQLite transactions prevent concurrent overwrites. frontier increments generation only on topology or version change, not on updated observation time; remote head must come from a forge read-back, never an old local ref passed off as current. The tool never infers safety or authorization automatically.

## Plan checking

`python3 tools/check_plan.py templates/plan.json` checks the DAG, ownership conflicts, per-unit acceptance and unit/live/perf applicability. project_root must be an absolute path; files resolve against this root with normalized paths/symlinks; use explicit paths—glob expansion is not supported; the tool does not run tasks or judge whether reasons are correct.

## GitHub status watching

`tools/pstack/watch-pr/` keeps Poteto's reads, state machine and tests. It was adapted to not auto-install, with a hard process-group time limit around it. For the first dependency install, explicitly run `bun install --frozen-lockfile` in `tools/pstack/`.

One-off status: `python3 tools/watch_pr.py --deadline 55 --pr 123 --status-only`.

Fixed queue: `python3 tools/watch_pr.py --deadline 55 --queued-stack --stack-prs 123,124 --interval 10 --timeout 45`. Verify the PR base chain independently first; the script does not prove the list order is correct. Long-term monitoring uses approved host automation.

Read kind, terminal, observedAt, head and blocker from the JSON/NDJSON. STATUS/exit 0 is not a pass; READY is not independent acceptance or the forge's final permission to merge; WAITING merge-queue is not merged; COMPLETE means the PRs in scope were actually merged. On wrapper timeout it exits 5 and kills the process group, keeping the state unknown.

The watcher only reads GitHub; it does not support Origin/other forges, and does not create/reply to/merge PRs. Other forges use their actual native tools with the same semantics, without claiming this script has been adapted.

## Source and adaptation

state.py redoes the original orch persistence mechanism, adding recoverable messages, full-content change detection, stable generation and evidence hashes. The original source snapshot is in the research directory and is not an active execution entry. The fixed ten-lane plan check became a risk-trimmable structural contract; worktree cleanup uses recoverable archiving and live audit rather than auto-deleting by the old tool's safe classification.

Tool source: [state workbench](state.py), [plan check](check_plan.py), [bounded watch entry](watch_pr.py), [watcher implementation](pstack/watch-pr/cli.ts).

Read-only queries use SQLite read-only transactions without taking the write lock; both scope changes and version changes invalidate old verdicts.

[Watcher state machine](pstack/watch-pr/policy.ts).

## OMP per-round roles

Only oh-my-pi (`omp`) uses `omp_roles.py`; Codex/Cursor do not read these roles.

```text
python3 tools/omp_roles.py prepare --project /current/project --input /this-round/roles.json --receipt /this-round/roles-receipt.json
python3 tools/omp_roles.py cleanup --receipt /this-round/roles-receipt.json
```

The input shape is `run_id` and `roles[]`; each item contains `name, description, model, thinking, tools, brief`. Names must start with `george-omp-` and be unique within the round. Models and thinking are first verified against the host's current catalog; this tool does not fix brands or price lists. A creation conflict rejects the whole batch; cleanup only touches this round's files for that project's roles whose content hash is unchanged.

The tool only prepares project `.omp/agents` files; it does not start inference or change global models or other hosts' roles. The requested field in the receipt is not evidence of actual execution; after the controller passes the role name via native `task.tasks[].agent`, it checks the actual model, thinking, status and usage from the child session. The native tool allowlist goes in the role frontmatter; the eval-only `tasks[].tools` is not the same field.

Protocol and boundaries are in the [OMP adapter](../adapters/omp.md). The package-root `scripts/probe_omp_autonomy.py` provides bounded native trial runs, recovery from stopped checkpoints, takeover on independent quality failure and evidence replay; failures are kept, and a directory existing or a worker's self-report is never acceptance.
