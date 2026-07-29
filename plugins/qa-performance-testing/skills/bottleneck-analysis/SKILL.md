---
name: bottleneck-analysis
description: "Read latency percentiles, error rate, throughput and resource saturation together, name the bottleneck resource, and separate a real regression from run-to-run noise. Use when interpreting performance results."
---

# Bottleneck analysis

## Analysis

Read four signals together — any one alone lies:

1. **Latency percentiles** — p50, p95, p99. Never averages.
2. **Error rate** — latency that looks fine while errors climb means requests are being shed, not served. Fast failures are not fast successes.
3. **Throughput** — did the system actually accept the offered load, or did the generator become the bottleneck?
4. **Resource saturation** — CPU, memory, IO, network, connection pool, lock contention, downstream dependency.

Name the bottleneck resource explicitly. "Performance degrades under load" is an observation; "the connection pool saturates at 220 concurrent requests and requests queue upstream" is a finding someone can act on.

## Regression vs noise

Run enough iterations to establish variance before declaring a regression. Report the confidence and the number of runs. A single slow run is not a regression, and a practice that cries regression on noise gets ignored when a real one arrives.
