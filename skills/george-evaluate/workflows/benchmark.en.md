# Explaining a measured number

1. First write the claim to be reported, metric, unit, direction, realistic workload and failure criterion; read the measurement script to confirm timing boundaries and statistics.
2. Baseline and treatment use the same hardware/limits, the same amount of work and result requirements, with reasonable configuration on both sides—never default on one side versus tuned on the other. Confirm the real path ran, results are correct, and count errors/drops/retries.
3. A formal comparison alternates at least five rounds, with fixed warm-up and cold/warm cache policy, recording raw values, sample count, median/range or an appropriate distribution. If the user only needs a rough estimate, a single round is fine but labeled rough, still checking errors and work completed.
4. Capture a profile or system counters to find the real limit: CPU, locks, disk, network, load generator. Explain with evidence "why it can't be twice as fast". A micro-benchmark saving cannot exceed that stage's original time; return to end-to-end impact.
5. Rule out caching, skipped work, error responses, noise, unequal load, sampling bias and extremes unrepresentative of real use. If the measurer cannot distinguish workloads, it cannot be used to optimize.
6. Output faster/slower/no difference/uncertain. When the bottleneck is unclear, either side is unfairly configured, or successful output is unconfirmed, keep it uncertain; never pick only the best round.

Agent evaluations likewise check that every trial actually did the task, whether failures were excluded, whether differences hold across repetitions/models, and whether scenarios represent the user's work.
