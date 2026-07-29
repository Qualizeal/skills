---
name: change-impact-scoring
description: Method for computing blast radius and risk-ranking regression tests from a code diff, including the minimum viable test scope model. Use when scoping regression testing for a PR, branch or release, or answering what needs retesting after a change.
---

# Change impact scoring

## Blast radius tracing

Trace outward from each changed symbol, at least two hops:

- **Hop 0** — the changed symbol itself.
- **Hop 1** — direct callers and direct consumers of its output.
- **Hop 2** — callers of those callers; anything reading state the symbol writes.

Record where tracing fails. Static tracing cannot follow: reflection, dynamic dispatch, dependency injection containers, event buses and message queues, string-keyed routing, feature-flag branches, ORM lifecycle hooks, or anything crossing a network boundary. Each of these is an `OPAQUE EDGE` and must appear in the output. An unreported blind spot is worse than a reported one.

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

## Minimum viable test scope

The smallest set that would catch a regression — not the smallest set that runs fast.

1. Every P0 path gets at least one end-to-end test.
2. Every changed branch gets a unit test at the decision point.
3. Every contract change gets a consumer-side contract test.
4. Every opaque edge gets a manual verification note, since automation cannot reach it.
5. Deduplicate: if an E2E test already traverses a P1 path, do not add a second.

## Output sections

Change summary with the exact ref range, impacted surfaces table, P0/P1/P2 bands with justification, uncovered gaps, opaque edges.
