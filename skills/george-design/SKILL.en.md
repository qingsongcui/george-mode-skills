# Investigation, design and review

> English translation of [SKILL.md](SKILL.md). Hosts load `SKILL.md`; this file is the full English body.

First read the [integration contract](../george-mode/references/integration.md), then choose by the actual problem:

| Situation | Workflow |
|---|---|
| How it runs / historical reasons / explaining to a reader | [how and why](workflows/how-why.md) |
| Read-only understanding or advice | [investigation](playbooks/investigation.md) |
| Architecture trade-offs / multiple options / code contest | [architect and arena](workflows/architect-arena.md) |
| Layout or behavior disagreements that can be tested | [prototype](playbooks/prototype.md) |
| Independent review, disputes, security and bot findings | [interrogate](workflows/interrogate.md) |
| External impact of a small change; restating or sharpening a task | [blast-radius](workflows/blast-radius.md) |

Structurally different candidates, the same criteria, independent review and post-synthesis verification together make up the full design capability. Simple changes run only the relevant parts. Major real-world trade-offs go to [george-decide](../george-decide/SKILL.md); once an authorized implementation option is chosen, proceed directly; a request for a plan only ends when the plan is delivered.
