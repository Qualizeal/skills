---
name: test-type-selection
description: "Choose between load, stress, soak, spike and capacity tests by the question being asked, and establish a baseline before comparing anything. Use when scoping a performance test."
---

# Test type selection

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
