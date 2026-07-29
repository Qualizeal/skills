---
name: shift-left-security-testing
description: Threat modelling at requirements time using STRIDE, security acceptance criteria, and triage of SAST/DAST/dependency scanner output by reachability and exploitability. Use during design or BRD review, when triaging scanner findings, or when writing security test cases.
---

# Shift-left security testing

Two jobs: model threats at the point where fixing them is cheapest — the requirement — and turn scanner output from volume into decisions.

## Threat modelling at BRD stage

Walk STRIDE against each data flow in the feature. One row per entry point, answered concretely.

| Category | The question to answer |
|---|---|
| **S**poofing | How is the actor authenticated at each entry point? |
| **T**ampering | What protects integrity in transit and at rest? |
| **R**epudiation | What is logged, and can the actor alter or delete it? |
| **I**nformation disclosure | What is the most sensitive field here, and who can read it? |
| **D**enial of service | What is unbounded — input size, retries, fan-out, query cost, file upload? |
| **E**levation of privilege | Where is authorisation checked, and is it checked on *every* path including the API? |

The highest-yield question in practice is the last one. Hidden UI is not an access control, and features routinely ship with the button removed and the endpoint open.

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

## Scanner triage

Scanner output is mostly noise. The value is separating signal, and the separation must be evidenced rather than asserted.

For each finding, establish four things:

1. **Reachability** — is the vulnerable code path reachable from untrusted input? Trace it and record the trace. Unreachable findings are deprioritised *with the evidence attached*, so the next person does not redo the work.
2. **Exploitability** — what does an attacker need? Network position, valid credentials, a specific configuration, a race window? Be concrete; "could be exploited" is not triage.
3. **Impact** — what is compromised, and how far does it reach.
4. **Fix cost** — dependency bump, code change, or architectural change.

Rank into four buckets:

| Bucket | Criteria |
|---|---|
| Fix now | Reachable from untrusted input, high impact |
| Fix this sprint | Reachable, moderate impact, or high impact behind authentication |
| Backlog with a decision | Low exploitability, documented and accepted by a named owner |
| False positive | With the reasoning that establishes it, not just the label |

An unexplained "false positive" label is how a real finding gets buried. Write the reason every time.

## Dependency findings

- A critical CVE in a transitive dependency you never call is still a supply-chain risk, but it is not the same urgency as one in a direct call path. Say which it is.
- Check whether a fixed version exists before filing. A finding with no available fix needs a mitigation, not a ticket that sits open for months.
- Version bumps are behavioural changes: they need the same regression scope as any other change — see `change-impact-analysis`.

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
