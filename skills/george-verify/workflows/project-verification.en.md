# Creating and maintaining project-specific verification

## Building

1. Inspect project source, run docs, package scripts and the real UI to determine what can be launched, how to drive it, what to observe and what to isolate. List the user's three to five most important features and build a feature map from real actions; do not substitute source file names for user features.
2. Create verify notes and minimal tools in a directory the project allows. Include launch, doctor, drive, evidence, cleanup and needed helpers. Write actual commands, port/process identification, test account/data source, selectors or CLI input and expected visible results; never fill in guessed selectors.
3. doctor checks the target process/version/port/health and isolation state; never treat an old service or cached screenshot as this round's instance. drive verifies the action, the result, and storage or external side effects together. Evidence includes time, version fingerprint, input, result and output path.
4. Actually run launch → doctor → one feature → save evidence → cleanup end to end at least once, then check the evidence still exists. Clean up only processes/isolated data created this round; do not kill every app with the same name. Run recovery and cleanup on failure or timeout too.
5. You may use this package's [verification runner](../scripts/run_verification.py) to execute an explicit step contract; see the [contract template](../templates/verification.json). Commands come from project discovery, not invented from the template. Long-running services are managed by dedicated launch/cleanup pairs.

## Maintenance

First read the feature map and find all affected features from the source diff; when authorized, investigate read-only in parallel with each reporting changes. The owner drives every feature the coverage promises, one by one in the real environment; on failure, doctor/reset first and locate.

Mark results clean/changed/blocked. Maintenance tasks change only the verification skill and scripts; product defects are listed separately—never weaken thresholds, change screenshot baselines or delete steps to make it pass. Record completion only after the evidence opens again after cleanup.

Independent verifiers take a fixed version, the same contract and an isolated environment, and do not modify the implementation or acceptance criteria. CLI success with body failure, broken artifacts, non-success end states or controlling the wrong object all count as failure.
