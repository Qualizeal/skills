---
name: state-transition-testing
description: "Cover valid transitions, invalid transitions and terminal states for any entity with a lifecycle, using 0-switch and 1-switch coverage. Use when testing orders, approvals, subscriptions or anything with a status field."
---

# State transition testing

## 4. State transition

For any entity with a lifecycle, draw the machine and cover valid transitions, invalid transitions and terminal states.

```
DRAFT ──submit──► PENDING ──approve──► ACTIVE ──expire──► EXPIRED
                     │                    │
                     └──reject──► REJECTED└──revoke──► REVOKED
```

Coverage levels:

- **0-switch** — every valid transition once
- **1-switch** — every valid pair of consecutive transitions, where budget allows
- **Invalid transitions** — this is where the defects live. Approve an already-approved code; revoke a draft; submit an expired one. Most systems handle the happy graph correctly and fall over on the edges nobody wired up
- **Terminal states** — verify nothing escapes `EXPIRED` or `REVOKED`
