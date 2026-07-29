---
name: invest-scoring
description: "Score a user story against Independent, Negotiable, Valuable, Estimable, Small and Testable with a 0-2 rubric and a readiness verdict. Use when assessing whether a story, epic or requirement is ready for development or test design."
---

# INVEST scoring

## Scoring rubric

Score each dimension 0-2. A total below 9, or any single 0, means the story is NOT READY.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Independent | Cannot start without another unfinished story | Soft dependency, sequenceable | No dependency |
| Negotiable | Prescribes implementation | Mixes what and how | States outcome only |
| Valuable | No stated beneficiary | Beneficiary implied | Named actor and benefit |
| Estimable | Unknown unknowns dominate | Bounded uncertainty | Team can size confidently |
| Small | Multi-sprint | Fills a sprint | Days |
| Testable | No observable outcome | Outcome observable but not measurable | Measurable pass/fail |

Testable is the veto dimension. A story scoring 0 on Testable is NOT READY regardless of its total.
