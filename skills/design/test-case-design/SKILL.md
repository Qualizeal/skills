---
name: test-case-design
description: Systematic test case design with worked examples — equivalence partitioning, boundary value analysis, decision tables, state transition, pairwise, and the CRUD/permissions checklists — plus test level assignment, prioritisation and the traceability matrix. Use when designing test cases, reviewing coverage, or building a traceability matrix.
---

# Test design techniques

Apply in order. Each technique reduces what the next has to handle. The goal is defect-finding power per case, not case count — a hundred redundant cases is a worse outcome than twenty well-chosen ones.

## Worked example used throughout

> **Promo code redemption.** A customer applies a promo code at checkout. Codes are 6-12 alphanumeric characters. A code may be percentage-based (1-50%) or fixed-amount (£1-£100). Fixed-amount codes require a minimum spend of £20. Codes have a start and expiry date. Each code has a usage limit; a customer may use a given code once. Staff accounts may apply expired codes.

## 1. Equivalence partitioning

Divide each input into classes handled identically; test one representative per class.

**Input: promo code string**

| Class | Representative | Valid |
|---|---|---|
| Valid length, valid code | `SAVE10` | ✓ |
| Valid length, unknown code | `NOPE99` | ✗ |
| Too short (< 6) | `SAVE` | ✗ |
| Too long (> 12) | `SAVE10SAVE10X` | ✗ |
| Non-alphanumeric | `SAVE-10` | ✗ |
| Empty | `` | ✗ |
| Whitespace only | `   ` | ✗ |
| Case variant | `save10` | ? — **undefined in the spec, raise it** |

That last row is the real output of this technique. Partitioning surfaces the classes nobody specified, and a question at design time costs minutes where the same question after release costs a defect.

## 2. Boundary value analysis

Defects cluster at boundaries. For every ordered domain `[min, max]`, test `min-1, min, min+1, max-1, max, max+1`.

**Percentage discount (1-50%)**

| Value | Expect |
|---|---|
| 0 | rejected |
| 1 | accepted |
| 2 | accepted |
| 49 | accepted |
| 50 | accepted |
| 51 | rejected |

**Minimum spend (£20 threshold)** — the boundary is on the *cart total*, not the discount:

| Cart total | Expect |
|---|---|
| £19.99 | code rejected, minimum-spend message |
| £20.00 | code applied |
| £20.01 | code applied |

Also treat as boundaries: zero, empty string, empty collection, single-element collection, max field length, integer overflow, month and year rollovers, leap day, DST transitions, and timestamps either side of a timezone boundary. The expiry date rule above needs a case at 23:59:59 and 00:00:00 in the *customer's* timezone, and it is worth asking which timezone the rule is evaluated in — that question alone finds defects regularly.

## 3. Decision tables

When behaviour depends on a combination of conditions, tabulate. Prose hides the combination nobody specified.

| Condition | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| Code exists | Y | Y | Y | Y | N |
| Within validity dates | Y | N | Y | Y | – |
| Staff account | – | Y | – | – | – |
| Cart ≥ minimum spend | Y | – | N | Y | – |
| Usage limit remaining | Y | – | – | N | – |
| **Discount applied** | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Message** | success | staff override | min spend | limit reached | unknown code |

Every `–` needs a justification. R2 encodes the staff-override rule; note that the spec never says whether staff override also bypasses minimum spend or usage limits — a gap the table makes impossible to miss, and one that prose would have hidden.

Collapse rules where a condition is genuinely irrelevant; do not collapse to make the table smaller.

## 4. State transition

For any entity with a lifecycle, draw the machine and cover valid transitions, invalid transitions and terminal states.

```
DRAFT ──submit──► PENDING ──approve──► ACTIVE ──expire──► EXPIRED
                     │                    │
                     └──reject──► REJECTED└──revoke──► REVOKED
```

Coverage levels:

- **0-switch** — every valid transition once
- **1-switch** — every valid pair of consecutive transitions, where budget allows
- **Invalid transitions** — this is where the defects live. Approve an already-approved code; revoke a draft; submit an expired one. Most systems handle the happy graph correctly and fall over on the edges nobody wired up
- **Terminal states** — verify nothing escapes `EXPIRED` or `REVOKED`

## 5. Pairwise

When configuration dimensions multiply past a testable count, cover all *pairs* rather than all combinations — most combinatorial defects involve two factors.

Dimensions: code type (2) × account type (2) × payment method (4) × currency (3) × device (3) = 144 combinations. A pairwise set covers every pair in roughly 12-16 cases.

Document which higher-order combinations you consciously excluded. "We did not test staff + expired + Amex + EUR together" is a decision; not mentioning it is an accident.

## 6. Negative testing checklist

Per input: empty · null · whitespace only · wrong type · exceeds max length · below min · malformed encoding · unicode and RTL · SQL/script injection payload · path traversal payload · duplicate submission · concurrent modification · expired token · insufficient permission.

Per operation: what happens if it is retried? Interrupted halfway? Called twice concurrently? Called by a user who lost permission between page load and submit?

## 7. CRUD and permissions matrices

For any resource, walk the grid rather than trusting that the implementation is uniform. Authorisation defects hide in the cells nobody thought about.

| Role | Create | Read own | Read others' | Update own | Update others' | Delete |
|---|---|---|---|---|---|---|
| Anonymous | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Customer | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ |
| Staff | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| Admin | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Every ✗ needs a test that it is genuinely denied — and denied at the API, not merely hidden in the UI. A hidden button is not an authorisation control.

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

## Prioritisation

- **P0** — revenue path, data integrity, security boundary, regulatory obligation
- **P1** — core feature behaviour, common error paths
- **P2** — secondary features, uncommon paths
- **P3** — cosmetic, rarely reached

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
