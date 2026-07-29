---
name: dashboard-specification
description: "Per-panel specification requiring metric, source, window, audience, threshold and the decision the panel informs — panels informing no decision get deleted. Use when designing or pruning a quality dashboard."
---

# Dashboard specification

## Dashboard panel specification

Every panel declares:

```
metric:
source:
window:
refresh:
audience:
threshold:        # what turns it amber and red
decision:         # the decision this panel informs
```

A panel that informs no decision is deleted. Dashboards fail by accumulating panels nobody acts on until the ones that matter are invisible.
