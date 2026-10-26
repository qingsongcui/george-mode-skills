# george-mode

A matrix of 11 agent skills that make a coding/knowledge agent work in a **decide → act → verify → reflect** loop: register goals, assumptions, falsifiers, predictions and stop conditions before high-stakes choices, and verify real behavior before claiming "done". Skill text is in Chinese; this README and [README.zh.md](README.zh.md) explain the package.

Works with any host that loads `SKILL.md` skill folders: Claude Code, OpenAI Codex, Cursor, oh-my-pi (OMP), Grok CLI, Google Antigravity.

## Skills

| Skill | Purpose |
|---|---|
| `george-mode` | Entry point. Routes a task by weight; holds the authorization and evidence rules. Invoke explicitly (`/george-mode`, `$george-mode`). |
| `george-investigate` | Read-only investigation: project survey, raw-evidence checks. |
| `george-decide` | Decision loop for important/irreversible choices (goal, assumptions, falsifiers, predictions, stop conditions). |
| `george-design` | Structural investigation, competing designs, adversarial review. |
| `george-engineer` | Features, bugs, refactors, performance, forensics, visual parity, PRs. |
| `george-evaluate` | Blind tests, perf-number audits, skill behavior checks. |
| `george-orchestrate` | Multi-phase plans, PR babysitting/landing, pausing and resuming; per-host sub-agent adapters. |
| `george-deliver` | Build and configure an already-decided deliverable to completion. |
| `george-verify` | Acceptance on the real surface, host adaptation, platform read-back. |
| `george-reflect` | Compare predictions with outcomes, extract bounded lessons. |
| `george-resume` | Resume long tasks and handoffs without losing goal or scope. |

Self-contained method references: [`decision-loop.md`](skills/george-mode/references/decision-loop.md) and [`verify-before-deliver.md`](skills/george-mode/references/verify-before-deliver.md).

## Install

Requires Python 3 (standard library only). From the package root:

```sh
python3 scripts/verify_package.py        # integrity check against PACKAGE-MANIFEST.json
python3 scripts/install.py               # dry run: shows planned symlinks
python3 scripts/install.py --apply       # create symlinks
python3 scripts/install.py --remove --apply   # uninstall (only links pointing here)
```

The installer symlinks each `skills/george-*` folder into `~/.agents/skills`, `~/.codex/skills`, `~/.cursor/skills`, `~/.gemini/config/skills`, and adds an OMP command alias. It never overwrites an existing path. Use `--home DIR` to target a different home.

Manual install (e.g. **Claude Code**): copy or symlink all `skills/george-*` folders together into `~/.claude/skills/` (or a project's `.claude/skills/`). Keep them as siblings — skills link to each other with relative paths.

Optional: the GitHub PR watcher in `skills/george-orchestrate/tools/pstack/` needs Bun and `gh`; run `bun install --frozen-lockfile` there first.

## Tests

```sh
python3 -m unittest discover -s tests
```

## Attribution

Large parts (the 24 engineering principles, engineer/design/evaluate/orchestrate playbooks, and the watch-pr tool) are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (@poteto), MIT License. See [NOTICE.md](NOTICE.md) and [third_party/pstack-LICENSE.txt](third_party/pstack-LICENSE.txt).

## License

MIT. See [LICENSE](LICENSE). Portions adapted from pstack keep their original MIT notice in [NOTICE.md](NOTICE.md).
