# NOTICE / Third-party attribution

This package contains material adapted from **pstack** by Lauren Tan (@poteto).

- Upstream: https://github.com/cursor/plugins/tree/main/pstack (standalone mirror: https://github.com/backnotprop/pstack)
- License: MIT License, Copyright (c) 2026 Lauren Tan — full text in [third_party/pstack-LICENSE.txt](third_party/pstack-LICENSE.txt)

Adapted (modified) files:

| Path in this package | Upstream origin |
|---|---|
| `skills/george-mode/principles/principle-*.md` (24 files) and `principles/INDEX.md` | pstack `skills/principle-*/SKILL.md` |
| `skills/george-engineer/playbooks/*.md` | pstack `skills/poteto-mode/playbooks/*.md` |
| `skills/george-design/playbooks/*.md`, `skills/george-design/workflows/*.md` | pstack `poteto-mode` playbooks and the `how`/`why`/`architect`/`arena`/`interrogate` skills |
| `skills/george-evaluate/playbooks/*.md`, `skills/george-evaluate/workflows/*.md` | pstack `poteto-mode` playbooks (eval, authoring-a-skill) and `benchmark-checklist` |
| `skills/george-orchestrate/playbooks/*.md`, `workflows/*.md` | pstack `poteto-mode` playbooks (orchestrate, autopilot, babysit, shipping, …) |
| `skills/george-orchestrate/tools/pstack/**` (watch-pr TypeScript sources and tests, package.json, bootstrap.ts, bun.lock) | pstack `poteto-mode` tools / watch-pr |
| `skills/george-verify/**` (verification workflow parts) | pstack `create-verification-skill` / `maintain-verification-skill` |

Modifications: translated/re-written in Chinese where noted, re-routed into the george-* module structure, trigger strength and authorization assumptions changed, auto-install removed from watch-pr and a hard process-group timeout added.

The MIT permission notice above must be kept in all copies or substantial portions of these files.

No other third-party source code or text is bundled. Host names mentioned in adapters (Codex, Cursor, oh-my-pi/OMP, Grok CLI, Google Antigravity) are referenced for interoperability only.
