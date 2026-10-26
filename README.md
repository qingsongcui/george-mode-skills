# george-mode

A matrix of 11 agent skills that make a coding/knowledge agent work in a **decide → act → verify → reflect** loop: register goals, assumptions, falsifiers, predictions and stop conditions before high-stakes choices, and verify real behavior before claiming "done". Everything ships in both English and Chinese (中文说明见 [README.zh.md](README.zh.md)).

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

## Theory toolkit

[`theory/`](theory/) holds the full method behind the skills: *Reflexive Practice: Private Canon* (the complete theory text), a loop operating manual, AI collaboration instructions, nine blank project-dossier templates, a field and numbering specification, sources and revision notes, and a blank eight-sheet loop workbook (`.xlsx`, Chinese and English). Start with [theory/00_开始使用.en.md](theory/00_开始使用.en.md). The templates and workbook are blank; no real project data is included.

## Bilingual layout

Every Markdown file has a sibling in the other language:

- Chinese original `name.md` → English `name.en.md` (all skills, playbooks, references, theory).
- English original `name.md` → Chinese `name.zh.md` (the 24 engineering principles, this README, NOTICE).
- Each `SKILL.md` keeps its frontmatter (hosts load it), with a `中文 / English` description and a link to `SKILL.en.md` at the top. Siblings have no frontmatter, so hosts never load them as separate skills.
- Shared terminology: [docs/glossary.md](docs/glossary.md).

The original language is authoritative if a translation differs.

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
cd skills/george-orchestrate/tools/pstack && bun install --frozen-lockfile && bun test
```

## Attribution

Large parts (the 24 engineering principles, engineer/design/evaluate/orchestrate playbooks, and the watch-pr tool) are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (@poteto), MIT License. See [NOTICE.md](NOTICE.md) and [third_party/pstack-LICENSE.txt](third_party/pstack-LICENSE.txt).

## License

MIT. See [LICENSE](LICENSE). Portions adapted from pstack keep their original MIT notice in [NOTICE.md](NOTICE.md).
