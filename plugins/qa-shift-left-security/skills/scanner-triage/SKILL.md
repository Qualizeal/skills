---
name: scanner-triage
description: "Rank SAST, DAST and dependency findings by reachability, exploitability, impact and fix cost, with evidence attached to every deprioritisation and false positive. Use when working through scanner output."
---

# Scanner triage

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
