---
name: quality-metrics-model
description: Definitions, formulas and reporting rules for quality metrics including release readiness scoring, coverage, defect density, escape rate and flake rate, plus dashboard design guidance. Use when computing quality metrics, assessing release readiness, or specifying dashboards.
---

# Quality metrics model

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

## Release readiness score

```
readiness = 0.20·requirements_coverage
          + 0.25·P0_pass_rate
          + 0.20·(1 − open_critical_factor)
          + 0.10·(1 − flake_rate_normalised)
          + 0.15·security_gate
          + 0.10·performance_gate
```

Rules:
- Publish the weights and every component value. A composite nobody can decompose gets ignored or gamed.
- Report the trend alongside the value. 82 and rising is a different decision from 82 and falling.
- Any component below its floor blocks release regardless of the composite. A high score cannot buy off an open S1.

Floors: `P0_pass_rate = 1.0`, `open_critical_factor = 0`, `security_gate = pass`.

## Predictive defect scoring

Where sufficient history exists, model defect probability per component from: recent churn, cyclomatic complexity, historical defect density, changed-line coverage, and number of distinct authors.

Report as a probability with a confidence interval and the sample size. Below roughly 50 historical defects, the model is not predictive — report the raw signals instead and say so. A decorated guess is worse than an honest absence.

## Reporting rules

1. Distinguish **measured**, **estimated** and **modelled** in every report. Never blur them.
2. Report percentiles, not averages, wherever the distribution has a tail.
3. Report metrics trending the wrong way even when still inside threshold — the trend precedes the breach.
4. Report bad news as prominently as good. A dashboard that only surfaces green manufactures confidence and destroys its own credibility the first time something ships broken.
5. When data is missing, state that it is missing. Do not interpolate and present the result as measurement.

## Dashboard panel specification

Every panel declares:

```
metric:
source:
window:
refresh:
audience:
threshold:        # what turns it amber and red
decision:         # the decision this panel informs
```

A panel that informs no decision is deleted. Dashboards fail by accumulating panels nobody acts on until the ones that matter are invisible.
