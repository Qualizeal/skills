---
name: edge-case-distribution
description: "Deliberately include boundaries, unicode and RTL, temporal edges, empty and maximal collections and nulls, because a dataset of uniformly valid rows finds no defects. Use when designing the shape of a test dataset."
---

# Edge case distribution

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
