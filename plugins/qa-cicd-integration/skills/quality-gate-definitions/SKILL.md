---
name: quality-gate-definitions
description: "Merge and release gate thresholds for pass rate, changed-line coverage, flake rate, security findings and open defects, plus the audited override policy. Use when defining or re-baselining release criteria."
---

# Quality gate definitions

## Gate definitions

Every gate needs four things: a threshold, a rationale, a named owner, and an audited override path.

| Gate | Merge | Release |
|---|---|---|
| Unit test pass rate | 100% | 100% |
| Coverage on changed lines | ≥ 80% | ≥ 80% |
| Coverage regression | No drop > 0.5% | No drop |
| `@p0` E2E pass rate | 100% | 100% |
| Flake rate | < 2% | < 1% |
| New critical/high SAST findings | 0 | 0 open |
| New critical dependency CVEs | 0 | 0; highs triaged |
| p95 latency regression | — | < 10% vs baseline |
| Open P0/P1 defects | — | 0 P0; P1 decided |

**Changed-line coverage, not total.** Total coverage percentage is gamed by testing easy code and is insensitive to exactly the lines most likely to break — the ones that just changed.

**Set thresholds at or just above the current baseline.** A gate set to aspiration gets disabled within a fortnight, and then you have neither the gate nor the honesty.

## Override policy

Every gate must be overridable and every override recorded: who, which gate, why, and a linked follow-up. A gate with no override path gets bypassed by disabling the pipeline entirely — which loses the audit trail and the signal at the same time.
