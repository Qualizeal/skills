---
name: regulatory-profiles
description: "GDPR, PCI-DSS, HIPAA and data-residency constraints on generated data, plus the conventions that keep synthetic identifiers visibly fake. Use when test data touches personal, payment or health information."
---

# Regulatory profiles

## Regulatory profiles

| Regime | Constraint |
|---|---|
| GDPR | No real personal data. Synthetic records must not resemble identifiable individuals. Data residency applies to test environments too. |
| PCI-DSS | Use documented test card numbers only. Never generate values that could pass as a live PAN. No CVV-like values in logs or fixtures. |
| HIPAA | No real PHI. Synthetic patient records only; avoid real-world rare-condition combinations that could be identifying. |
| Residency | Generated data stays in the jurisdiction the environment is bound to. |

## Visibly synthetic identifiers

Generated identifiers should be recognisable as fake so nobody mistakes a fixture for a real record:

- emails at `@example.com` / `@example.org`
- phone numbers in reserved test ranges
- documented-invalid payment card BINs
- names drawn from synthetic pools, never from public figures or real customers
- addresses that are structurally valid but not real premises
