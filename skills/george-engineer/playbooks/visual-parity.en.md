# Visual-parity migration

1. Before changing anything, establish a real screenshot baseline covering component states, viewports, fonts, themes, data and animation moments; when matching two implementations, screenshot under identical conditions. Without a baseline, parity cannot be claimed.
2. Fix the comparator, rendering environment, masks and threshold. When pixel-exact is required, the threshold is zero; unavoidable rendering noise may only get a tolerance set in advance from repeated baselines, with an explanation—never relaxed after a difference appears.
3. Migrate and verify shared primitives first, then isolate ownership per component. Migrate one safe unit at a time, run the image diff and inspect the differing regions; never pass on eyeballing or an aggregate score alone.
4. Do not change the baseline, mask failing regions, or make it pass by rewriting the comparator. If the user really wants a new look, explicitly change the acceptance contract and establish a new approved baseline.
5. Also drive key interactions and accessibility states. Identical images do not prove events, focus, error and loading states are correct.
6. Deliver per-component comparison results, images/diff images, environment and remaining items, then go to PR delivery.

Source: pstack `skills/poteto-mode/playbooks/visual-parity.md` (MIT, © 2026 Lauren Tan; see NOTICE.md at the package root). Adaptation rationale: [integration contract](../../george-mode/references/integration.md).
