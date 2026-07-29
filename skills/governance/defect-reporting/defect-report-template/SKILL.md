---
name: defect-report-template
description: "The full report structure — environment, classification, steps, expected versus actual with verbatim error text, evidence, root cause hypothesis, blast radius — plus the enrichment rules. Use when writing or improving a defect report."
---

# Defect report template

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

## Enrichment rules

- Quote errors verbatim. Paraphrase makes them unsearchable and breaks deduplication.
- One defect per report.
- Attach the failing test's trace where one exists; it removes an entire round trip.
- Never include real customer data, credentials or tokens. Redact and state that you redacted.
- Label hypotheses as hypotheses. A confident wrong root cause costs more than no root cause.
