---
name: security-testing-boundaries
description: "What security testing must never produce — exploit code, discovered secrets in reports, tests against production or third-party systems — and the required output structure. Use before writing or publishing any security finding."
---

# Security testing boundaries

## Hard boundaries

- **Analyse and report; do not write exploits.** No proof-of-concept attack code, no payloads designed to run against a live system.
- **Never put discovered secrets in output.** Report the existence and location; the value goes to the rotation process, not into a report, a ticket or a chat transcript. A secret pasted into a defect report has been published.
- **Test payloads for input-validation testing stay inert** and are documented as test fixtures.
- **Never test against production**, and never against a third party's system without written authorisation.

## Output

```
## Threat model — STRIDE table per data flow
## Security acceptance criteria — Given/When/Then, with IDs
## Ranked findings — with reachability evidence per finding
## False positives — each with the reasoning that establishes it
## Accepted risks — with named owner and review date
```
