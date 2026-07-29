---
name: decision-tables
description: "Tabulate combinations of conditions into rules so the combination nobody specified becomes impossible to miss. Use when behaviour depends on several conditions interacting, such as eligibility, pricing or permission rules."
---

# Decision tables

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
