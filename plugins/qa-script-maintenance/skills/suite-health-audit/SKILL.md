---
name: suite-health-audit
description: "The seven-check audit — locator drift, fragility inventory scored by churn, dead tests, duplicate coverage, runtime hotspots, quarantine ledger and flake rate. Use for a periodic suite health review or after a UI refactor."
---

# Suite health audit

## The health audit

Run all seven checks. Report counts and file references for each, not a general impression.

### 1. Locator drift

Extract every locator in the suite and resolve each against the current application:

- **0 matches** → broken; the test is passing only because it is skipped, or failing and being ignored
- **2+ matches** → ambiguous; it will break the moment ordering or content changes
- **1 match** → healthy, but still score it for fragility

### 2. Fragility inventory

```
fragility = selector_risk + wait_risk + coupling_risk
ranked by  fragility × churn_factor
```

| Factor | Values |
|---|---|
| `selector_risk` | 0 role+name · 1 label/text · 2 testid · 3 stable CSS · 5 generated/structural CSS · 8 XPath |
| `wait_risk` | 0 web-first assertions · 3 any `waitForTimeout` |
| `coupling_risk` | 0 self-contained · 2 shared fixture state · 4 order-dependent |
| `churn_factor` | 1 stable UI area · 1.5 moderate churn · 2 frequently changed (from `git log` on the component) |

Ranking by fragility alone produces a backlog of fragile tests over screens nobody touches. Multiplying by churn puts the work where the breakage will actually happen.

### 3. Dead tests

- Always skipped
- Passing trivially (no assertion, or asserting a constant)
- Asserting only that a page loaded

A test with no meaningful assertion is worse than no test: it reports coverage that does not exist.

### 4. Duplicate coverage

Multiple tests exercising the same path. Keep the one at the cheapest level, delete the rest. Duplication at E2E level is the most expensive kind and the most common.

### 5. Runtime hotspots

The slowest 10% of tests and the reason for each. The usual cause is UI-driven setup that should be API-driven. Report the time that would be recovered by fixing each.

### 6. Quarantine ledger

Every skipped or quarantined test with its age, owner, reason and linked defect. **Anything quarantined beyond 30 days is fixed or deleted.** A permanent quarantine is a lie about coverage that compounds: nobody remembers it exists, and the gap it leaves is invisible in every coverage report.

### 7. Flake rate

Per test, from recent CI history. Anything above 2% is a maintenance item, not a retry candidate.
