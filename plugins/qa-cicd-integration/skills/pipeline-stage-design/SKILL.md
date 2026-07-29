---
name: pipeline-stage-design
description: "Order stages cheapest-first with time budgets, and keep full E2E out of the merge gate. Use when designing or restructuring a test pipeline."
---

# Pipeline stage design

## Stage ordering

Cheapest first, fail fast.

| Stage | Budget | Blocks merge | Blocks release |
|---|---|---|---|
| Lint + type check | < 2 min | Yes | Yes |
| Unit tests | < 5 min | Yes | Yes |
| Contract tests | < 5 min | Yes | Yes |
| Integration tests | < 15 min | Yes | Yes |
| Build + deploy to test env | < 10 min | Yes | Yes |
| E2E smoke (`@p0`) | < 10 min | Yes | Yes |
| Full E2E | parallel | No | Yes |
| Security scan (SAST/deps) | parallel | New criticals only | Yes |
| Performance | nightly | No | Yes |

Full E2E as a merge gate is a common and expensive mistake: it puts a 40-minute suite between a developer and every merge, and the response is invariably to bypass it.
