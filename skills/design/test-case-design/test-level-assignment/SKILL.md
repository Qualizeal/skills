---
name: test-level-assignment
description: "Push every case to the cheapest level that can catch the defect — unit, integration, contract, E2E or performance — and justify anything placed at E2E. Use when deciding where a test belongs or reviewing an E2E-heavy suite."
---

# Test level assignment

## Test level assignment

Push every case to the cheapest level that can catch the defect.

| Level | Use for | Do not use for |
|---|---|---|
| Unit | Logic, calculation, validation, boundaries | Wiring, configuration |
| Integration | Contracts between components, persistence, serialisation | Business rule permutations |
| Contract | Provider/consumer API compatibility | UI behaviour |
| E2E | Critical user journeys only | Boundary permutations, error copy |
| Performance | Throughput, latency, resource behaviour | Functional correctness |

Applied to the example: the 1-50% boundary set belongs at unit level (six cheap cases). One E2E case covers "customer applies a valid code and sees the discounted total". Putting all six boundaries through the browser costs roughly forty times as much and catches nothing extra.

Any case placed at E2E needs a written justification of why a lower level cannot catch the defect.

## Prioritisation

- **P0** — revenue path, data integrity, security boundary, regulatory obligation
- **P1** — core feature behaviour, common error paths
- **P2** — secondary features, uncommon paths
- **P3** — cosmetic, rarely reached
