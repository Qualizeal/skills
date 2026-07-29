---
name: change-risk-scoring
description: "Classify changes by type and compute a risk score from blast radius, complexity, churn and coverage, banding results into P0, P1 and P2. Use when ranking what to retest for a pull request or release."
---

# Change risk scoring

## Change classification

| Class | Default risk | Notes |
|---|---|---|
| Schema / migration | Critical | Always P0. Irreversible in production. |
| Public API surface | High | Contract change affects unknown consumers. |
| Shared utility / validator | High | Small diff, wide radius. |
| Auth / authz / crypto | Critical | Always P0 plus a security review. |
| Business logic (leaf) | Medium | Scope to the owning feature. |
| Configuration | Medium | Environment-dependent; verify per environment. |
| Dependency bump | Medium-High | Read the changelog; transitive risk. |
| Cosmetic / comments / formatting | Minimal | Verify no behavioural change, then drop. |

## Risk score

```
risk = blast_radius × change_complexity × churn_factor × coverage_penalty
```

- `blast_radius` — 1 (leaf), 2 (module), 3 (cross-module), 5 (cross-service)
- `change_complexity` — 1 (rename/constant), 2 (logic edit), 3 (control flow or state machine), 5 (concurrency, data migration, security)
- `churn_factor` — 1 (stable file), 1.5 (moderate history of fixes), 2 (frequently patched hotspot)
- `coverage_penalty` — 1 (well covered), 2 (partial), 3 (uncovered)

Banding: P0 ≥ 18, P1 6-17, P2 < 6. Schema, migration and auth changes are P0 irrespective of score.
