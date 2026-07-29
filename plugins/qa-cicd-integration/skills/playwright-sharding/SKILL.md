---
name: playwright-sharding
description: "Split a suite by historical duration rather than file count and merge blob reports into a single HTML report, with per-shard balance reporting. Use when parallelising a slow test suite."
---

# Sharding and report merging

## Playwright sharding and report merging

Split by historical duration, not file count.

```yaml
strategy:
  fail-fast: false
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}/4
```

Shards produce separate blob reports; merge them into one HTML report afterwards:

```bash
npx playwright merge-reports --reporter html ./all-blob-reports
```

Report per-shard balance. If one shard takes three times another, you have no effective parallelism — rebalance when the spread exceeds 25%.
