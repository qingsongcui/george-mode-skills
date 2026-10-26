# Live runtime forensics

This task delivers a diagnosis; do not modify production code unless a fix was requested.
1. Capture a CPU profile, heap snapshot, network or render trace matching the live situation; record process, version, sampling window and trigger.
2. Reduce large data with tools or read-only agents, keeping the hot call tree, retention chains from leaked objects to GC roots, and loops/counts that run with no input.
3. When a probe is needed, first confirm whether it is read-only or changes runtime state. In an isolated environment, add temporary instrumentation or a reversible hot patch to test the mechanism, and record its effect on the system. A read-only production task does not treat "forensics" as authorization to inject changes.
4. Map signals to files, symbols and code locations, keeping observation distinct from inference. What could not be verified by intervention is written as the best-supported hypothesis.
5. Deliver evidence references and diagnosis; continue into the bug/perf playbook only if the original task includes a fix. The throughput check may be recorded as not applicable to read-only forensics.

Source: pstack `skills/poteto-mode/playbooks/runtime-forensics.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
