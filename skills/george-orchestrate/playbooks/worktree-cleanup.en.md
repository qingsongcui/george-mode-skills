# Workspace and runtime resource cleanup

Run this flow only when the user asks to clean up the corresponding resources; ordinary task wrap-up handles only temporary resources it created itself.

1. Audit candidates using the actual git worktree list, disk usage, branches and dirty state. Check active/pinned tasks, running processes, uncommitted and unpushed content, PR/base and merge evidence; when recent chat is unknown, keep checking the corresponding records.
2. A classification suggestion is not deletion authorization. Keep shared/main worktrees, active tasks, user pins and unarchived changes; untracked files may also have value. Never delete based on name, merge status or a scratch classification alone.
3. Prefer recoverable archive tools provided by the host. If deletion is truly needed, list the exact objects, usage, use and recovery state; outside the authorized scope, prepare reviewable candidates first.
4. Re-read the live state before cleanup to prevent races; never force-remove/reset an unknown state. Simulator/app data/caches have their own objects and usage audits and are not cleaned up along with worktrees.
5. Afterwards, re-check the actual list, disk space and retained recovery evidence, reporting actual space freed rather than estimates.

Source: pstack `skills/poteto-mode/playbooks/worktree-cleanup.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root); adapted per the [George integration contract](../../george-mode/references/integration.md).
