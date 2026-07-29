---
name: performance-testing
description: Designing telemetry-grounded load, stress, soak, spike and capacity tests — SLO definition, workload modelling from APM data, baselines, bottleneck analysis and honest reporting of percentiles. Use when performance testing, capacity planning, or investigating a latency or throughput regression.
---

# Performance testing

A load test built on guessed traffic measures something, but not your system under its actual load. Everything here starts from telemetry.

## Ingest telemetry first

Pull from APM before designing anything:

- request mix by endpoint, as a proportion of total
- arrival distribution over the day and week — real traffic is bursty, not uniform
- payload size distribution, including the tail
- cache hit rates
- concurrency and session length
- current p50/p95/p99 latency and error rate as the baseline

If telemetry is unavailable, say so explicitly and label every derived figure as an assumption. Presenting a modelled number as a measured one is the fastest way to lose a performance practice's credibility.

## Define the SLO precisely

"The API should be fast" is not an SLO. An SLO states:

```
p95 latency of POST /orders < 400ms
  measured at the load balancer
  over a 5-minute window
  at 500 requests/second
  with error rate < 0.1%
```

Percentile, threshold, measurement point, window, load level, and the error rate that must hold simultaneously. Without the measurement point, two teams will measure different things and both will be right.

## Model the workload

- Match the production request mix, not an even spread across endpoints. An even spread over-tests cheap endpoints and under-tests the expensive one that actually falls over.
- Model think time. Closed-loop generators with zero think time produce a queue shape no real user population creates, and the results mislead in both directions.
- Model the arrival process, not just the average rate. Bursts are where systems fail.
- Include the cold-start case: empty caches, fresh connection pools.

## Test types

| Type | Shape | Answers |
|---|---|---|
| **Load** | Expected peak, sustained | Does it meet the SLO under normal conditions? |
| **Stress** | Ramp beyond peak until degradation | Where does it break, and *how* does it break? |
| **Soak** | Moderate load, extended duration | Leaks, pool exhaustion, log growth, unbounded caches |
| **Spike** | Sudden step change | Does autoscaling and queueing hold? |
| **Capacity** | Stepped ramp | Throughput per unit of resource, for planning |

The failure *mode* from a stress test is often more valuable than the breaking point. Graceful degradation and shedding is a different operational situation from cascading timeout collapse, and only a stress test distinguishes them.

## Baselines

Establish one before comparing anything. A number without a baseline is not a result. Re-baseline after any environment change, and record the environment's relationship to production: CPU, memory, data volume, topology, and whether downstream dependencies are real or stubbed.

Extrapolating from a quarter-size environment without stating you did so is misleading, even when the ratio is reasonable.

## Analysis

Read four signals together — any one alone lies:

1. **Latency percentiles** — p50, p95, p99. Never averages.
2. **Error rate** — latency that looks fine while errors climb means requests are being shed, not served. Fast failures are not fast successes.
3. **Throughput** — did the system actually accept the offered load, or did the generator become the bottleneck?
4. **Resource saturation** — CPU, memory, IO, network, connection pool, lock contention, downstream dependency.

Name the bottleneck resource explicitly. "Performance degrades under load" is an observation; "the connection pool saturates at 220 concurrent requests and requests queue upstream" is a finding someone can act on.

## Regression vs noise

Run enough iterations to establish variance before declaring a regression. Report the confidence and the number of runs. A single slow run is not a regression, and a practice that cries regression on noise gets ignored when a real one arrives.

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
