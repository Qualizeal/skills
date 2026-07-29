---
name: locator-drift-repair
description: "Detect broken and ambiguous locators proactively, score them for fragility, and repair by fixing the locator strategy rather than raising a timeout. Use after a UI change or when selectors start failing."
---

# Locator drift detection and repair

## Locator drift detection

Run proactively, before failures accumulate:

1. Extract every locator used in the suite.
2. For each, resolve against the current application: does it match exactly one element?
   - 0 matches → **broken**
   - 2+ matches → **ambiguous**, will break as soon as ordering changes
   - 1 match → healthy
3. Score each healthy locator for fragility (see below) and rank the backlog by `fragility × churn` of the underlying UI area.

## Fragility scoring

| Strategy | Score |
|---|---|
| `getByRole` with name | 0 |
| `getByLabel` / `getByText` | 1 |
| `data-testid` | 2 |
| Stable CSS (id, semantic class) | 3 |
| Generated class or structural CSS | 5 |
| XPath | 8 |

Add 3 for any hard wait in the same test, and 4 for order dependency.

## Repair method

When a locator breaks, repair in this order:

1. Find the element's current accessible role and name → rewrite as `getByRole`.
2. If the element has no accessible name, **that is an accessibility defect**. Raise it, and fix it in the application rather than routing around it in the test.
3. If no semantic handle exists, add a `data-testid` to the application.
4. Only if the application cannot be changed, use stable CSS with a justification comment and a follow-up ticket.

Never repair by raising a timeout, adding a sleep, or wrapping in a retry. Those hide the mechanism and the test will fail again less predictably.
