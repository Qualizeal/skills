---
name: predictive-defect-scoring
description: "Model defect-prone components from churn, complexity, history and coverage, with the sample-size threshold below which the model is a decorated guess. Use when targeting testing effort at likely hotspots."
---

# Predictive defect scoring

## Predictive defect scoring

Where sufficient history exists, model defect probability per component from: recent churn, cyclomatic complexity, historical defect density, changed-line coverage, and number of distinct authors.

Report as a probability with a confidence interval and the sample size. Below roughly 50 historical defects, the model is not predictive — report the raw signals instead and say so. A decorated guess is worse than an honest absence.
