# Resumption and handoff

> English translation of [SKILL.md](SKILL.md). Hosts load `SKILL.md`; this file is the full English body.

When the user specifies a subdirectory, that subdirectory is this round's task root; do not expand to parent/sibling directories because source is missing or there are other projects alongside. Reading an explicitly given skill source does not change the task root. Resumption notes keep the authorized paths verbatim.

First find the original request, later corrections, the current authoritative files and the last verified checkpoint. The newest message usually adjusts the current task, unless the user explicitly cancels or replaces the goal. When an old summary conflicts with the live state, check the original evidence.

Save a minimal checkpoint: goal, scope and authorization, done items and evidence, unfinished items, modified files, running jobs, external operations with unknown outcome, next executable action and stop condition. For credentials, record only how to obtain them; never copy secrets.

On resumption, first check whether the live state changed, especially branches, user edits, platform objects and running processes. Do not redo verified actions from scratch, and do not mark unfinished tasks as done. Do not grab back a UI the user has taken over.

Parallel tasks provide explicit file ownership, source paths, acceptance criteria and report format. The main agent verifies results and writes shared state alone; conclusions from two sub-agents with the same evidence source are not two independent pieces of evidence. Models follow the settings the current host allows; do not copy historical model names or change configuration for the user.

## Specific resumption methods

Read [context reconstruction](workflows/context.md) to distinguish resuming a specific task, reviewing a topic and explaining current progress; persistent queues, pausing and resuming are handled by [george-orchestrate](../george-orchestrate/SKILL.md).
