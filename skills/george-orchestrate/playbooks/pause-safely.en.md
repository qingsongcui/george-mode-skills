# Safe pause and checkpoint

Stop the task only on an explicit "pause/stop"; on context compaction, save a checkpoint and continue; a user's "continue" must not be treated as a pause. Never let a pause become completion.

1. Stop new dispatches and new external writes; propagate the pause to all owners and watchers, and check actual end states rather than only sending notifications.
2. If the current atomic step can be completed safely, complete it to a checkpoint; otherwise revert only this round's separable changes; reconcile unknown external operations first. Never reset unknown user work.
3. Save the uncommitted diff, branch/worktree, verified versions, processes, artifacts, pending gates, original goal, all user corrections and the exact next action. Follow project commit constraints; do not mechanically create wip commits or push.
4. Confirm no orphaned background process will keep writing and that evidence still exists after cleanup. Record commands/environment needed for recovery, never secrets.
5. Report the paused state and unfinished items clearly. Resume via session-pickup.

Source: pstack `skills/poteto-mode/playbooks/pause-safely.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root); adapted per the [George integration contract](../../george-mode/references/integration.md).
