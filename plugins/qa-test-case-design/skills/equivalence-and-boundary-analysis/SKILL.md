---
name: equivalence-and-boundary-analysis
description: "Divide inputs into equivalence classes and test the boundaries where defects cluster — min-1, min, max, max+1, plus zero, empty, overflow, leap days and DST transitions. Use when designing cases for any field with a range, length or format constraint."
---

# Equivalence partitioning and boundary values

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
