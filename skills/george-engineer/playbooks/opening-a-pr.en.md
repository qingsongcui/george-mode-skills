# Engineering output and PR delivery

1. Read the current workspace and the user's changes; check the final diff, behavior, dependencies and necessary docs. Never overwrite others' work with reset --hard or indiscriminate git add. Use a new worktree when isolation is needed; prefer reusing a suitable existing one.
2. Clean up per [code quality](../workflows/code-quality.md) and [technical writing](../workflows/writing.md). Complex/high-consequence changes get independent review; real checks finish first; unverified items keep their label.
3. When the task needs Git delivery, organize changes into replayable, verifiable units. Do not casually rewrite existing user history; stage only paths owned by this round; a related failing test can be shown on its own before the fix.
4. Choose the currently available forge/native PR tool; write title and description per the repo template, explaining the user problem, change, evidence, risk and scope. Draft/ready follows actual completeness and the user's request; not every PR must be marked ready.
5. Dependent PRs chain by base branch with one topology writer; only independent changes branch from trunk. After creating a PR, read back its real link and status; attach associations when the host requires them.
6. Creating a PR does not automatically start babysitting or merging. When the user asks for follow-through, route to [PR follow-through](../../george-orchestrate/playbooks/babysit.md); when merging is authorized, go to [Shipping](../../george-orchestrate/playbooks/shipping.md).
7. Local deliverables or read-only tasks need no PR; deliver the actual artifact and verification directly.

Source: the opening-a-pr playbook of pstack `poteto-mode` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root); removed premises unsuited to George such as resetting unknown work, forcing non-draft, and always opening a PR.
