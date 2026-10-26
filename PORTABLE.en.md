# George mode standalone package

This package contains 11 skills, the self-contained decision loop and acceptance references (skills/george-mode/references/decision-loop.md, verify-before-deliver.md), five host adapters and runtime tools. It needs no author workspace, business ledger or conversation history.

Unpack it into a directory you will keep long-term and run from the package root:

```sh
python3 scripts/verify_package.py
python3 scripts/install.py
python3 scripts/install.py --apply
```

Python 3 is required. verify_package checks integrity; install previews without --apply; with --apply it creates skill links for the current user and the OMP default-profile command. Existing content with the same name is refused. To install only for hosts you actually use, you can manually place the whole set of george-* directories in that host's skill directory, keeping the sibling relationship. For separate OMP profiles, install the command alias per the host's instructions. Hosts and model services must be provided by you; the skill package carries no accounts or credentials.

Codex invokes $george-mode; Cursor, the Grok CLI and Antigravity invoke /george-mode; OMP invokes /skill:george-mode or the installed /george-mode. Grok discovers the existing ~/.agents/skills links, and the installer does not write ~/.grok/skills separately; Antigravity links into ~/.gemini/config/skills. Current project rules are read from that project; no other project's rules are inherited automatically.

Installation runs via links: you can unpack anywhere, but do not move the source directory directly after installing; to migrate, first run python3 scripts/install.py --remove --apply from the old location, then install from the new location. Uninstall removes only links pointing to this package.

The GitHub watcher is optional and needs Bun and gh; before use, install dependencies from the lockfile in its pstack directory. Other Python runtime tools use the standard library. Environment dependencies are not dependencies on the author's workspace.

The distribution does not include original sessions, private research, workbooks, account settings or archives of old-version verification. File hashes are in PACKAGE-MANIFEST.json; historical results are not promised to reproduce in a new environment.

The optional theory toolkit lives in `theory/` (Chinese originals with `.en.md` translations, plus blank workbook templates); the skills do not need it at runtime.
