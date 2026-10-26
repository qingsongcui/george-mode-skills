<!-- English translation of george-mode.md for reference only. The installer links only george-mode.md as the OMP command. -->

First prefer using `read` to read `skill://george-mode` (if the host environment does not support resolving skill URIs, fall back per install semantics to reading `~/.agents/skills/george-mode/SKILL.md` or the package source path `skills/george-mode/SKILL.md`).

Then use `read` to read `skill://george-orchestrate/adapters/omp.md`. Only after both entries have actually been read, start handling the user task below. The OMP adapter is the dispatch contract for subsequent new tasks in this session; you cannot claim autonomous dispatch has started after reading only the main entry or role files. Self-contained small tasks are still finished directly by the controller; this step does not require scanning other projects or starting workers.

Note: this command is the OMP native command entry (it works by guiding the reading of skills and routing; it does not claim to inject skills directly at a lower level).

Following `george-mode`'s weight-based routing rules and constraints throughout, complete the following user input within the current session's authorization boundaries:

$ARGUMENTS

Execution red lines:
1. Expanding this command and the initial phase run no bash commands and do not automatically modify host configuration, models, credentials or environment variables.
2. Read the corresponding module files only on demand when routing names them; no unrelated scanning.
3. Strictly inherit the current session's explicit authorization boundaries; if no arguments are provided, expand by the default entry and confirm the current task goal.
