---
name: release-readiness-scoring
description: "Composite readiness score with published weights, per-component floors that block release regardless of the total, and trend reporting. Use for a go/no-go release review."
---

# Release readiness scoring

## Release readiness score

```
readiness = 0.20·requirements_coverage
          + 0.25·P0_pass_rate
          + 0.20·(1 − open_critical_factor)
          + 0.10·(1 − flake_rate_normalised)
          + 0.15·security_gate
          + 0.10·performance_gate
```

Rules:
- Publish the weights and every component value. A composite nobody can decompose gets ignored or gamed.
- Report the trend alongside the value. 82 and rising is a different decision from 82 and falling.
- Any component below its floor blocks release regardless of the composite. A high score cannot buy off an open S1.

Floors: `P0_pass_rate = 1.0`, `open_critical_factor = 0`, `security_gate = pass`.
