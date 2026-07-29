---
name: failure-triage
description: "Decision tree for classifying a CI failure as product defect, test defect, environment or flake, with undetermined as a legitimate verdict. Use when a pipeline goes red and you need an accurate classification before anyone starts fixing."
---

# Failure triage

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
