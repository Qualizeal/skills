---
name: security-acceptance-criteria
description: "Write security requirements as Given/When/Then acceptance criteria so they enter the traceability matrix and get tested rather than discussed. Use when turning a threat model into testable requirements."
---

# Security acceptance criteria

## Security acceptance criteria

Write them in the same Given/When/Then form as functional AC so they land in the same traceability matrix and get tested rather than discussed.

```
AC-S1  Given a customer authenticated as user A
       When they request /api/orders/{id} for an order belonging to user B
       Then the response is 404, not 403
       And the attempt is recorded in the audit log

AC-S2  Given an upload endpoint
       When a file exceeding 10MB is submitted
       Then it is rejected before being written to disk
```

404 rather than 403 in AC-S1 is deliberate: 403 confirms the resource exists, which leaks information. Detail at this level is the difference between a security AC and a security aspiration.
