---
name: automation-repair-rules
description: "How to repair automation properly — fix the locator not the timeout, add a test id to the application rather than reaching for XPath, refactor setup into fixtures, never wrap a flake in a retry. Use when fixing a failing or fragile test."
---

# Automation repair rules

## Repair rules

- **Fix the locator strategy, not the timeout.** Raising a timeout hides a race; it does not remove it, and it lengthens every subsequent run.
- **No stable handle? Change the application.** Add a `data-testid` rather than reaching for XPath. This is a normal code change, not test pollution.
- **Refactor shared setup into fixtures**, never into inter-test dependencies.
- **Delete rather than skip.** A deleted test is honest about coverage; a permanently skipped one is not.
- **Never wrap a flaky test in a retry** to close the ticket. Name the mechanism — see `failure-analysis-self-healing` — and fix it.
