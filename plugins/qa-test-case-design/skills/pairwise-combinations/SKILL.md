---
name: pairwise-combinations
description: "Cover all pairs of parameter values instead of all combinations when configuration dimensions multiply beyond a testable count, and document what was consciously excluded. Use for cross-browser, multi-currency, multi-role or device matrices."
---

# Pairwise combination testing

## 5. Pairwise

When configuration dimensions multiply past a testable count, cover all *pairs* rather than all combinations — most combinatorial defects involve two factors.

Dimensions: code type (2) × account type (2) × payment method (4) × currency (3) × device (3) = 144 combinations. A pairwise set covers every pair in roughly 12-16 cases.

Document which higher-order combinations you consciously excluded. "We did not test staff + expired + Amex + EUR together" is a decision; not mentioning it is an accident.
