---
name: requirements-refinement
description: Scoring rubric and ambiguity taxonomy for evaluating user stories and requirements, plus the house format for acceptance criteria. Use whenever a requirement, user story, epic, PRD or ticket needs to be assessed for testability or rewritten into verifiable acceptance criteria.
---

# INVEST analysis and acceptance criteria enrichment

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

## Ambiguity taxonomy

Flag every occurrence and quote the offending text.

1. **Weasel words** — fast, robust, seamless, intuitive, appropriate, reasonable, as needed, etc.
2. **Unquantified comparatives** — better, faster, more secure. Compared to what, by how much?
3. **Missing actor** — passive voice hiding who performs the action ("the record is archived").
4. **Undefined state** — references a status, mode or flag with no definition or enumeration.
5. **Implicit assumption** — behaviour that only makes sense given an unstated precondition.
6. **Dangling pronoun** — "it", "this", "they" with more than one possible referent.
7. **Compound requirement** — one line specifying two independently testable behaviours; split it.
8. **Unbounded quantity** — any list, upload, retry or timeout with no stated limit.
9. **Missing error path** — a success behaviour with no specified failure behaviour.

## Acceptance criteria format

```
AC-<n>  Given <precondition in a known state>
        When <single action by a named actor>
        Then <observable, measurable outcome>
        And <side effect, if any: audit entry, notification, state change>
```

Rules:
- One action per AC. If the When clause contains "and", split it.
- The Then clause must be checkable by someone who cannot see the code.
- Numeric and temporal fields need boundary ACs at min, min-1, max, max+1.
- Every AC needs a stable ID; downstream traceability matrices key on it.

## Coverage checklist

Before declaring READY, confirm the story has:
- [ ] Happy path
- [ ] At least one negative/error path
- [ ] Boundaries on every numeric, temporal or length-constrained field
- [ ] Permission/role behaviour if the feature is role-sensitive
- [ ] Empty, single and maximal state for any list or collection
- [ ] Idempotency or concurrency behaviour if the action can be repeated or raced
- [ ] Explicitly stated non-goals

## Output

Scorecard table, numbered ambiguity list with rewrites, refined AC set, open questions marked `NEEDS DECISION`, and a one-line verdict.
