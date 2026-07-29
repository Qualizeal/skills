---
name: slo-definition
description: "State a performance objective precisely: percentile, threshold, measurement point, window, load level and the error rate that must hold simultaneously. Use when agreeing performance targets or interpreting a vague one."
---

# SLO definition

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
