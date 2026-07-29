---
name: performance-reporting
description: "Report percentiles never averages, error rate alongside every latency figure, the environment relationship to production, and an explicit split between measured and modelled values. Use when writing up a performance test."
---

# Performance reporting

## Reporting rules

- Percentiles, never averages — the average hides the tail where users actually suffer
- Error rate alongside every latency figure
- The environment's relationship to production, stated
- Measured, modelled and assumed values labelled distinctly
- The bottleneck named
- SLA verdict per SLO, not one overall pass/fail

## Output

```
## Workload model — with telemetry provenance
## Test configuration — type, duration, load profile, environment
## Results — percentiles, error rate, throughput, saturation
## Bottleneck analysis
## SLA verdict per SLO
## Measured vs modelled — explicit split
```
