---
name: defect-enrichment
description: Defect report template, severity and priority rubrics, duplicate and false-positive screening method, and root cause categorisation. Use when writing, triaging, deduplicating or improving defect reports.
---

# Defect reporting and enrichment

## Screening (do this first)

Around a third of raised defects are duplicates, environment problems or misread requirements. Screen before filing.

1. **Duplicate** — search by error signature, component and symptom, not by title wording. Titles vary; stack traces do not.
2. **Requirement check** — identify the acceptance criterion or spec clause violated. No violated requirement means this is a question or an enhancement request.
3. **Environment check** — reproduce on a clean environment before attributing to the product.
4. **Reproducibility** — always / intermittent (state the rate as n of m attempts) / once-observed. Never label an intermittent defect as reproducible to make it seem more urgent.

## Report template

```
Title: <component> — <observable symptom> when <condition>

Environment
  Build/commit:
  Environment:
  Client (browser/OS/device):
  Data set / feature flags:

Classification
  Severity: S1-S4    Rationale:
  Priority: P0-P3    Rationale:
  Reproducibility:   always | intermittent (n/m) | once
  Requirement violated: <AC or spec reference>

Steps to reproduce
  1. <from an explicitly stated starting state>

Expected:  <quoted from the requirement>
Actual:    <exact observed behaviour and verbatim error text>

Evidence:  trace / screenshot / video / log excerpt with timestamps / request-response pair
Root cause hypothesis: <labelled as hypothesis>
Blast radius:
Workaround:
```

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

## Root cause categories

Use a fixed set so RCA data is aggregable:

`requirements-gap` · `design-flaw` · `coding-error` · `integration-mismatch` · `configuration` · `data` · `infrastructure` · `third-party` · `regression-from-fix` · `test-defect`

`regression-from-fix` deserves particular attention — a rising count means the fix process itself needs review.

## Enrichment rules

- Quote errors verbatim. Paraphrase makes them unsearchable and breaks deduplication.
- One defect per report.
- Attach the failing test's trace where one exists; it removes an entire round trip.
- Never include real customer data, credentials or tokens. Redact and state that you redacted.
- Label hypotheses as hypotheses. A confident wrong root cause costs more than no root cause.
