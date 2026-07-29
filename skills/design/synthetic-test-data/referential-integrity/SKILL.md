---
name: referential-integrity
description: "Generate in topological dependency order and verify foreign keys, unique indexes, check constraints and application invariants independently afterwards. Use when producing a multi-table fixture or seeding an environment."
---

# Referential integrity generation

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
