---
name: severity-and-priority
description: "Separate technical severity from business priority using two independent rubrics, and why conflating them corrupts defect density metrics. Use when classifying a defect or triaging a queue."
---

# Severity and priority

## Severity rubric (technical impact)

| Level | Definition |
|---|---|
| S1 | Data loss or corruption, security breach, complete outage, regulatory violation |
| S2 | Core function unusable, no workaround |
| S3 | Function degraded, workaround exists |
| S4 | Cosmetic, minor inconvenience, no functional impact |

## Priority rubric (business urgency)

| Level | Definition |
|---|---|
| P0 | Fix now, block the release |
| P1 | Fix this sprint |
| P2 | Fix when convenient |
| P3 | Backlog, may never be fixed |

Keep the axes separate. A cosmetic defect on a launch-week landing page is legitimately S4/P0. Inflating severity to obtain priority corrupts the defect density metrics that everything downstream is measured on.
