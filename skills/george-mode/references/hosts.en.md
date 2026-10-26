# Host adaptation

The five hosts share this package's skills/ skill source. Installation location and task workspace are independent of each other; project-local rules and host permissions take precedence. Session-level autonomous dispatch is managed by each host's adapter, without changing persistent configuration or credentials.

## Invocation and discovery

| Host | Install entry | Invocation and commands |
|---|---|---|
| Codex | `~/.codex/skills/george-*`, linked to the same source | `$george-mode` plus the task; or choose from the skill menu |
| Cursor | `~/.cursor/skills/george-*`, linked to the same source | `/george-mode` plus the task; if it doesn't appear, start a new session or refresh skill discovery |
| OMP | `~/.agents/skills/george-*` (the installer also provides an OMP-specific `/george-mode` command alias) | The native command is `/skill:george-mode`; after installing the alias you can also type `/george-mode` |
| Grok CLI | No separate `~/.grok/skills/george-*` install; it scans the installed `~/.agents/skills/george-*` by default | `/george-mode` plus the task; `grok inspect` can check discovery. The installer does not change `~/.grok/config.toml` |
| Antigravity | `~/.gemini/config/skills/george-*`, linked to the same source | `/george-mode` plus the task (supports Antigravity 2.0, IDE and the `agy` CLI); the Language Server's `GetAllSkills` can check discovery |

`disable-model-invocation: true` is an extension field supported by some hosts; you cannot assume all hosts recognize it: in OMP and Antigravity it hides the skill from the model's automatic tool calls, but **hidden does not mean the command disappears**—users can still invoke it natively and explicitly via `/skill:george-mode` (OMP) or `/george-mode` (Antigravity). The Grok CLI recognizes this field; the slash `/george-mode` can still be invoked explicitly. Codex additionally uses `allow_implicit_invocation: false` in `agents/openai.yaml`. **OMP, Grok and Antigravity do not use `agents/openai.yaml`**, set no fixed model, and do not rely on automatic skill triggering. All entries default to explicit on-demand invocation and create no always-on rule.

The OMP installer only places the alias at `~/.omp/agent/commands/george-mode.md` in the default profile and changes no profile configuration. Other profiles should install the same-source command in their own `commands/` directory; you cannot assume the default profile's command is in effect. Native skill discovery from `~/.agents/skills` depends on the host having the agents source enabled; the installer does not flip the source switch on its own.

Do not equate manual reading with native menu discovery, nor native discovery with a passed task. For usage see [usage and acceptance](使用与验收.md).

## Execution differences

- Relative links in skill bodies point only to that skill or sibling `george-*` directories. Cursor Read folds `..` literally and does not follow the `~/.cursor/skills/george-*` install symlink. In-skill help and navigation uniformly use sibling relative paths (e.g. `../../george-investigate/SKILL.md`) (resolved relative to the location of the file actually read), ensuring they open unambiguously on all hosts.
- Invocation mechanisms are isolated: Codex uses `$george-*` and `agents/openai.yaml`; Cursor uses `/george-mode`; OMP uses native `/skill:george-mode` and the installer-provided OMP-only `/george-mode` file command alias; the Grok CLI uses `/george-mode`, discovered from `~/.agents/skills`; Antigravity uses `/george-mode`, discovered from `~/.gemini/config/skills`. OMP, Grok and Antigravity do not depend on `agents/openai.yaml` at all.
- File operations, command line, browser, MCP, sub-agents and question tools all use the interfaces the current host actually provides. When a tool is missing, choose a verifiable alternative or report the gap; do not reuse other hosts' tool names and parameters.
- If delegation is needed, first confirm this round allows it and write task boundaries and path ownership. Without native sub-agents, run sequentially; do not install plugins or start paid models on your own.
- Autonomous dispatch branches by host: Codex reads `george-orchestrate/adapters/codex.md`; Cursor reads `george-orchestrate/adapters/cursor.md`; oh-my-pi (`omp`) reads `george-orchestrate/adapters/omp.md`; the Grok CLI reads `george-orchestrate/adapters/grok.md`; Antigravity reads `george-orchestrate/adapters/antigravity.md`. Dispatch details stay only in the corresponding adapter; one host's parameters, roles and quota semantics are not imposed on others.
- Do not fix model names in skills. OMP's model configuration and provider selection, Codex's role settings, Cursor's selectable models, Grok's parent-session inheritance and Antigravity's `Model` tier enum all differ; the user's existing models, credentials and routing configuration are fully kept.
- When OMP/Cursor/Grok/Antigravity lack Codex app-server tools, do not copy its read-back commands; use their own real load logs or interactive UI instead. Grok uses `grok inspect` to check discovery and `spawn_subagent` to dispatch; Antigravity uses the Language Server's `GetAllSkills` to check discovery and `invoke_subagent` / `send_message` / `manage_subagents` to dispatch and manage.
- Documents/visual works need the generation and rendering tools available on the current host. Skill text does not claim any host automatically has browser, desktop control or model service capabilities. Keep the source shared and each host's permission boundaries.

## Updating and removal

All links follow source file updates. Moving or deleting the install package directory breaks the links; when migrating, reinstall first and then verify. The install script is `scripts/install.py` inside the package; it previews by default and creates links only with `--apply`; it refuses to overwrite existing paths with the same name.

Uninstall removes only links pointing to this source: run `python3 scripts/install.py --remove --apply` in the package root. It does not delete the original skill source, other skills or host configuration.
