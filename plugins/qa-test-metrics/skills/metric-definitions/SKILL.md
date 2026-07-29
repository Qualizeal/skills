---
name: metric-definitions
description: "Formulas and time windows for coverage, defect density, escape rate, flake rate, detection stage, ageing and suite runtime, and why changed-line coverage beats total coverage. Use when computing or defining quality metrics."
---

# Metric definitions

## Definitions

Every metric needs a denominator and a time window. A number without them is not a metric.

| Metric | Formula | Window |
|---|---|---|
| Changed-line coverage | covered changed lines / changed lines | per PR |
| Requirements coverage | ACs with ≥1 linked test / total ACs | per release |
| Defect density | defects / KLOC changed, by component | per release |
| Defect escape rate | production defects / (production + pre-production defects) | rolling 90 days |
| Detection stage distribution | defect count by stage found | rolling 90 days |
| Flake rate | tests passing only on retry / total test executions | rolling 14 days |
| Mean time to detect | commit timestamp → failure detected | rolling 30 days |
| Defect ageing | open defects bucketed by age × severity | current |
| Suite runtime | p50 and p95 wall clock per stage | rolling 14 days |
| Fix regression rate | defects classified `regression-from-fix` / total fixes | rolling 90 days |

## Why changed-line coverage, not total coverage

Total coverage percentage is trivially gamed by adding tests to easy code and is insensitive to exactly the code most likely to break — the code that just changed. Changed-line coverage answers the question people actually mean: is the new work tested?
