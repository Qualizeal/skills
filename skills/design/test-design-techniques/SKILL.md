---
name: test-design-techniques
description: Systematic test design techniques — equivalence partitioning, boundary value analysis, decision tables, state transition, pairwise — plus the traceability matrix format and test level assignment rules. Use when designing test cases, reviewing test coverage, or building a traceability matrix.
---

# Test design techniques

Apply in this order. Each technique reduces the case count the next one has to handle.

## 1. Equivalence partitioning

Divide each input into classes where every member is expected to be handled identically. Test one representative per class, not many.

For every field derive: valid classes, invalid-by-type classes, invalid-by-range classes, invalid-by-format classes, and the absent/null class.

## 2. Boundary value analysis

Defects cluster at boundaries. For every ordered domain with bounds `[min, max]`, test:

`min-1, min, min+1, max-1, max, max+1`

Also treat as boundaries: zero, empty string, empty collection, single-element collection, maximum field length, integer overflow points, date rollovers (month, year, leap day), DST transitions, and timezone-boundary timestamps.

## 3. Decision tables

When behaviour depends on a combination of conditions, tabulate rather than prose. Columns are rules, rows are conditions and actions. Collapse rules where a condition is irrelevant, and mark it `-`.

A decision table forces you to notice the combination nobody specified. Every `-` and every impossible combination should be justified in a note.

## 4. State transition testing

For any entity with a lifecycle, draw the state machine and cover:

- Every valid transition once (0-switch coverage)
- Every pair of consecutive transitions where budget allows (1-switch)
- **Every invalid transition** — attempting to cancel a delivered order, approving an already-approved record. These are where the defects live.
- Terminal states: verify nothing escapes them.

## 5. Pairwise (all-pairs)

When configuration dimensions multiply beyond a testable count, cover all pairs of parameter values rather than all combinations. Most combinatorial defects involve two factors. Document which higher-order combinations you consciously excluded.

## Negative test checklist

Per input: empty, null, whitespace only, wrong type, exceeds max length, below min, malformed encoding, unicode and RTL, SQL/script injection payload, path traversal payload, duplicate submission, concurrent modification, expired token, insufficient permission.

## Test level assignment

Push every case to the cheapest level that can catch the defect.

| Level | Use for | Do not use for |
|---|---|---|
| Unit | Logic, calculation, validation, boundaries | Wiring, configuration |
| Integration | Contracts between components, persistence, serialisation | Business rule permutations |
| Contract | Provider/consumer API compatibility | UI behaviour |
| E2E | Critical user journeys only | Boundary permutations, error message text |
| Performance | Throughput, latency, resource behaviour under load | Functional correctness |

Any case placed at E2E requires a written justification of why a lower level cannot catch the defect.

## Traceability matrix

```
| AC ID | AC summary | TC IDs | Levels | Priority | Status |
```

Verify both directions and report both:
- **Orphan ACs** — acceptance criteria with no test case. This is a coverage gap.
- **Orphan TCs** — test cases mapping to no acceptance criterion. This is either scope creep or an undocumented requirement; decide which and say so.

## Prioritisation

- **P0** — revenue path, data integrity, security boundary, regulatory obligation
- **P1** — core feature behaviour, common error paths
- **P2** — secondary features, uncommon paths
- **P3** — cosmetic, rarely reached
