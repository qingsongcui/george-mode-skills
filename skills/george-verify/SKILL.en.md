# Acceptance by real results

> English translation of [SKILL.md](SKILL.md). Hosts load `SKILL.md`; this file is the full English body.

First identify which layer of result this round promised, then choose the matching check.

| Result layer | Evidence required |
|---|---|
| Local file or package | Content, dependencies, links, open or unpack result; visual deliverables must be render-checked |
| Code behavior | Actual call path and key failure paths; meaningful tests or a minimal reproduction |
| Model and configuration | A real minimal request on the target host and the exact error; saved settings or a model list are not proof of usability |
| Host adaptation | Verify skill discovery/loading, task execution and host artifacts separately; verify the control entry separately when non-interactive control is needed |
| Platform write | Correct account and object, submission receipt, and actual state read back |
| Usage and business effect | Evidence of real external use, adoption, payment or profit, excluding self-tests and double counting |

Checks not run are written as unverified. Tool exit 0 cannot override body failures, timeouts or error end states. When there is no visible state, restore observability before operating.

Sends, publications, orders or money operations with unknown outcome must not be retried blindly. First reconcile by object identifier, time window and historical state; if undecidable, keep unknown with recovery conditions.

Multi-host reports separate "files installed, loading verified, real task passed"; none substitutes for another. If a required real call exceeds current authorization or would incur unknown cost, keep it unverified and state the specific gap.

Record check method, time, result and limitations. When the project requires EX/OB, workbooks and freeze checksums, complete them together; finished bookkeeping is not business effect.

## Project-level verification tools

When software needs to be driven repeatedly, run [project verification creation and maintenance](workflows/project-verification.md). Record evidence bound to head/content fingerprint; an independent verifier cannot be impersonated by the author. Record persistent results with the [orchestration tools](../george-orchestrate/tools/README.md).
