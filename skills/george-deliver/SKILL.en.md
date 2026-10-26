# Implementation and delivery

> English translation of [SKILL.md](SKILL.md). Hosts load `SKILL.md`; this file is the full English body.

Code tasks go to the [engineering domain pack](../george-engineer/SKILL.md), which picks a specific playbook per task; this module keeps the general delivery constraints.

First re-check the existing implementation, user changes, dependencies and acceptance target. For fixes, first reproduce or obtain enough failure evidence and locate the first wrong step; for making things, first define the target reader, usage and finished-product standard. Implementation covers only this round's goal. When the user asks to adapt a reference, keep the specified features; redesign only when originality is requested. For visual deliverables, check real assets, layout and interaction; fake icons, placeholder content or script success do not substitute for finished quality.

Split work into independently acceptable units. Build the smallest useful loop first, then widen coverage; never claim a real feature is done with shells, placeholder data or self-test wrappers. For architecture changes, explain how data and state flow; for config changes, keep a restorable backup and modify only the target application.

Investigate observable problems yourself or run a minimal experiment. Autonomous execution does not mean swapping products, raising budgets, publishing or sending messages on your own. Explicit authorization stays valid for this round; if the scope is unchanged, do not ask for it again.

Use multiple agents only when permitted and the task is divisible. Each one gets bounded read/write paths, deliverables and evidence standards; one owner writes the shared ledger. Different reports are never merged without checking. When the host lacks delegation, run sequentially; never fake parallel conclusions.

After each delivery unit, verify with [george-verify](../george-verify/SKILL.md); after fixing newly found issues, re-verify in a targeted way. Deliver after enough relevant checks pass; do not repeat tests just to raise the test count.
