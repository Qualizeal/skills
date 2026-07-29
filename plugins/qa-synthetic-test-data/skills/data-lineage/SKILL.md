---
name: data-lineage
description: "Seed every generator and ship a lineage document recording generator version, seed, schema version, row counts and the regeneration command. Use when producing a dataset that anyone will need to reproduce."
---

# Determinism and lineage

## Determinism

Seed every generator explicitly. Record the seed in the lineage document. A non-reproducible fixture makes a flaky failure impossible to investigate.

## Lineage document

Ships alongside every dataset:

```yaml
dataset: <name>
generated: <ISO timestamp>
generator: <tool and version>
seed: <value>
schema-version: <migration id>
row-counts: { table: n, ... }
regulatory-profile: <GDPR | PCI-DSS | HIPAA | none>
constraint-verification: PASS | FAIL <details>
edge-coverage: <list of categories exercised>
regenerate: <exact command>
```
