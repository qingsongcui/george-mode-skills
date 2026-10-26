# Authorized delivery and actual landing

Entry condition: the implementation is reviewable and the task requires publishing/merging; finish local preparation and reviewable evidence before dealing with any missing authorization. Do not re-request authorization already given.

1. For each PR, check a non-author independent verdict, exact head, real artifact evidence, current CI, open comments, target base and the forge's mergeable conditions. green/READY/exit 0 never pass on their own.
2. Only a contiguous passing segment starting from the root may be delivered; if a lower layer has not passed, an upper layer cannot be skipped ahead even if green. Record the queue and current authorization.
3. A version change invalidates old verdicts by default. An identical patch-id only supports "the patch content is the same"; base, dependencies, environment and runtime contract still need checking; when unsure, re-verify and record against the new head—never copy an old SHA's record.
4. Land only the lowest item each time. A successful merge command or successful queueing is not completion; re-read MERGED and the target commit. After a parent merges, the single topology owner checks the child's new base/diff, retargets/rebases if needed, and re-verifies.
5. During landing, other owners must not write to the chain. On anomalies, stop that item first, save a recoverable state and check whether an external write already happened; do not retry blindly.
6. After completion, verify the delivered artifact via its real entry point and keep evidence. Stop only watchers belonging to this task; a merge is not business adoption or revenue effect.
Artifacts: actual landing record, per-item evidence, reasons for anything not landed and recovery points.
Source: pstack `skills/poteto-mode/playbooks/shipping.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root); adapted per the [George integration contract](../../george-mode/references/integration.md).
