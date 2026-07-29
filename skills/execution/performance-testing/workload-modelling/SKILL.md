---
name: workload-modelling
description: "Build a load profile from real APM telemetry — request mix, arrival distribution, payload sizes, think time — instead of a uniform guess. Use before designing any performance test."
---

# Workload modelling

## Ingest telemetry first

Pull from APM before designing anything:

- request mix by endpoint, as a proportion of total
- arrival distribution over the day and week — real traffic is bursty, not uniform
- payload size distribution, including the tail
- cache hit rates
- concurrency and session length
- current p50/p95/p99 latency and error rate as the baseline

If telemetry is unavailable, say so explicitly and label every derived figure as an assumption. Presenting a modelled number as a measured one is the fastest way to lose a performance practice's credibility.

## Model the workload

- Match the production request mix, not an even spread across endpoints. An even spread over-tests cheap endpoints and under-tests the expensive one that actually falls over.
- Model think time. Closed-loop generators with zero think time produce a queue shape no real user population creates, and the results mislead in both directions.
- Model the arrival process, not just the average rate. Bursts are where systems fail.
- Include the cold-start case: empty caches, fresh connection pools.
