---
name: synthetic-test-data
description: Rules for generating schema-aware synthetic test data with referential integrity, regulatory constraints, edge-case distribution and lineage documentation. Use when creating test fixtures, seeding an environment, or when asked about test data, anonymisation or masking.
---

# Synthetic test data

## The prime constraint

Production personal data never enters a test environment. Masking is not a substitute: masked data retains distributional and relational structure that can re-identify individuals, and masking pipelines fail silently. Generate synthetic data instead, always.

If someone asks for a masked production extract, offer a synthetic dataset matched to the production schema and distribution instead, and explain why.

## Schema derivation

Derive, never assume, from migrations, DDL or ORM models:

- column types, precision, nullability
- primary and unique keys
- foreign keys and cascade behaviour
- check constraints and enums
- **application-level invariants** — cross-field rules enforced in code rather than the database. These are the ones that get missed, because the database will happily accept violating rows that the application then chokes on.

## Generation order

Topologically sort tables by foreign key dependency; generate parents first. After generation, verify independently:

```
- every FK resolves to an existing parent row
- every unique index holds
- every check constraint holds
- every enum value is in range
- application invariants hold (assert these explicitly; the DB will not)
```

Report the verification result. A generator that claims success without verification is a generator that ships broken fixtures.

## Distribution coverage

A dataset of uniformly valid rows finds no defects. Every dataset should deliberately include:

| Category | Examples |
|---|---|
| Boundaries | min, max, zero, negative, overflow-adjacent |
| Strings | empty, single char, maximum length, leading/trailing whitespace |
| Unicode | multi-byte, emoji, RTL scripts, combining characters, zero-width |
| Temporal | leap day, DST transition, year boundary, far-future, epoch |
| Collections | empty, single element, maximum cardinality |
| Nullability | null in every nullable column, at least once |
| Referential | orphan-adjacent cases where cascade behaviour matters |

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
