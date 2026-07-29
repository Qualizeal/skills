---
name: traceability-matrix
description: "The house test case format and the requirement-to-test traceability matrix, checked in both directions to surface orphan acceptance criteria and orphan cases. Use when writing cases or reporting coverage against requirements."
---

# Traceability and case format

## Case format

```
TC-<id> | AC-<id> | <level> | <priority>
Title:         <observable behaviour under test>
Preconditions:
Steps:         1. ... 2. ...
Expected:      <single, specific, observable assertion>
Data:          <synthetic data profile reference>
```

- One assertion per case. Cases verifying three things fail ambiguously.
- Expected results must be specific. "An error is shown" is not an expected result; "the message `Minimum spend of £20 required` appears below the promo field, and the order total is unchanged" is.
- If you cannot state the defect a case would catch, delete it.

## Traceability matrix

```
| AC ID | AC summary | TC IDs | Levels | Priority | Automated | Status |
```

Check and report **both** directions:

- **Orphan ACs** — acceptance criteria with no test case. A coverage gap.
- **Orphan TCs** — cases mapping to no acceptance criterion. Either scope creep or an undocumented requirement; decide which and say which. An orphan case is often the trace of a real rule that never made it into the spec.

## Coverage self-check

Before declaring a design complete:

- [ ] Every AC has at least one case
- [ ] Every numeric or temporal field has boundary cases
- [ ] Every enumerated field has an invalid-value case
- [ ] Every role appears in the permissions matrix, with denials tested at the API
- [ ] Every state machine edge, valid and invalid, is covered
- [ ] Empty, single and maximal collection states are covered
- [ ] Concurrency and idempotency are addressed for any repeatable action
- [ ] Every case names the defect it would catch
- [ ] Every undefined behaviour found during design has been raised, not assumed
