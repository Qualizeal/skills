---
name: defect-screening
description: "Screen for duplicates, requirement violations, environment causes and reproducibility before filing, because roughly a third of raised defects are none of the above. Use before creating any defect."
---

# Defect screening

## Screening (do this first)

Around a third of raised defects are duplicates, environment problems or misread requirements. Screen before filing.

1. **Duplicate** — search by error signature, component and symptom, not by title wording. Titles vary; stack traces do not.
2. **Requirement check** — identify the acceptance criterion or spec clause violated. No violated requirement means this is a question or an enhancement request.
3. **Environment check** — reproduce on a clean environment before attributing to the product.
4. **Reproducibility** — always / intermittent (state the rate as n of m attempts) / once-observed. Never label an intermittent defect as reproducible to make it seem more urgent.
