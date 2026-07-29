---
name: script-maintenance
description: Proactive automation suite health — the audit checklist, fragility and churn scoring, dead and duplicate test detection, runtime hotspots, quarantine ledger policy, and repair rules. Use for suite health reviews, after a UI refactor, when the suite gets slow or noisy, or when deciding whether to fix or delete a test.
---

# Script maintenance

An automation suite is an asset that depreciates. This work is preventive: find the tests that are *about to* break, before a release finds them for you.

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

## Repair rules

- **Fix the locator strategy, not the timeout.** Raising a timeout hides a race; it does not remove it, and it lengthens every subsequent run.
- **No stable handle? Change the application.** Add a `data-testid` rather than reaching for XPath. This is a normal code change, not test pollution.
- **Refactor shared setup into fixtures**, never into inter-test dependencies.
- **Delete rather than skip.** A deleted test is honest about coverage; a permanently skipped one is not.
- **Never wrap a flaky test in a retry** to close the ticket. Name the mechanism — see `failure-analysis-self-healing` — and fix it.

## Deletion criteria

Delete a test when any of these hold, and say plainly that you are deleting it:

- It asserts nothing meaningful
- It duplicates coverage that exists at a cheaper level
- It has been quarantined more than 30 days with no owner acting
- Its fragility cost exceeds its value: repeatedly repaired, never caught a real defect
- It tests a feature that no longer exists

Track "tests deleted" as a positive maintenance metric. A suite that only ever grows is a suite nobody is maintaining.

## Output

```
## Health scorecard (with trend if history exists)
## Fragility backlog — ranked, with effort estimates
## Dead and duplicate tests — recommended for deletion, with reasons
## Runtime hotspots — with recoverable time
## Quarantine ledger — with ages and overdue items flagged
## Repairs applied this pass
```
