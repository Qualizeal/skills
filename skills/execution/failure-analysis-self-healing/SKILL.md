---
name: failure-analysis-self-healing
description: Failure triage taxonomy for CI test failures and the locator drift detection and repair method behind self-healing automation. Use when classifying a test failure, diagnosing flakiness, or repairing broken selectors after a UI change.
---

# Failure triage and locator self-healing

## Triage decision tree

```
Did the test fail on retry of the same commit?
├─ No  → non-deterministic → FLAKE (sub-classify below)
└─ Yes → deterministic
   ├─ Do many unrelated tests fail together?
   │  └─ Yes → ENVIRONMENT (or shared fixture defect)
   ├─ Does the assertion reflect current intended behaviour?
   │  ├─ No  → TEST DEFECT (stale expectation)
   │  └─ Yes → does the failing path touch the change under test?
   │           ├─ Yes → PRODUCT DEFECT (high confidence)
   │           └─ No  → PRODUCT DEFECT (investigate further) or UNDETERMINED
```

`UNDETERMINED` is a valid verdict. Guessing a cause is more expensive than admitting insufficient evidence.

## Flake sub-classification

Name the mechanism. "Flaky" without a mechanism is not a diagnosis.

| Mechanism | Signature | Fix |
|---|---|---|
| Timing race | Fails under parallelism or on slow runners | Wait for state, not time |
| Shared state | Fails when run after a specific other test | Isolate fixture data |
| Order dependency | Passes alone, fails in suite | Make the test self-sufficient |
| Unseeded randomness | Fails intermittently with different data | Seed the generator |
| Network non-determinism | Fails on external calls | Stub or contract-test |
| Animation/transition | Fails on element interception | Wait for a stable state |
| Clock/timezone | Fails at particular times of day or near midnight | Freeze the clock, pin the timezone |
| Resource contention | Fails only at high shard counts | Bound parallelism or pool resources |

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

## Quarantine policy

A quarantined test is a coverage gap that looks like coverage. Every quarantine carries an owner, a reason, a linked defect and a date. At 30 days, it is fixed or deleted — never renewed silently.
