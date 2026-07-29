---
name: schema-derivation
description: "Derive types, constraints, keys and application-level invariants from migrations, DDL or ORM models rather than assuming them — and why masked production data is never an acceptable substitute. Use before generating any test dataset."
---

# Schema derivation

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
