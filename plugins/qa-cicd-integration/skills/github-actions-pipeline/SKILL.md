---
name: github-actions-pipeline
description: "A working GitHub Actions workflow for unit and sharded E2E stages with artefact upload and report merging, plus the platform specifics that bite — SHA-pinned actions, explicit permissions, pinned container tags. Use when configuring tests on GitHub Actions."
---

# GitHub Actions pipeline

## GitHub Actions

```yaml
name: Tests

on: [pull_request]

jobs:
  unit:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: coverage, path: coverage/ }

  e2e:
    needs: unit
    runs-on: ubuntu-latest
    timeout-minutes: 30
    container:
      image: mcr.microsoft.com/playwright:v1.50.0-noble   # pin: an unpinned browser silently changes results
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npx playwright test --grep @p0 --shard=${{ matrix.shard }}/4
        env:
          BASE_URL: ${{ vars.TEST_BASE_URL }}
          TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: blob-report-${{ matrix.shard }}
          path: blob-report/
          retention-days: 7

  report:
    needs: e2e
    if: ${{ !cancelled() }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with: { path: all-blob-reports, pattern: blob-report-*, merge-multiple: true }
      - run: npx playwright merge-reports --reporter html ./all-blob-reports
      - uses: actions/upload-artifact@v4
        with: { name: html-report, path: playwright-report/, retention-days: 14 }
```

Platform specifics that bite:

- **Pin actions by SHA**, not tag, for anything touching secrets. A tag is mutable.
- **Set `permissions` explicitly** at workflow level; the default token is broader than most jobs need.
- **`if: always()` vs `if: ${{ !cancelled() }}`** — use the latter for artefact upload so a cancelled run does not spend minutes uploading.
- **Pin the Playwright container tag** to match the `@playwright/test` version. A drifting browser version turns into "flaky tests" nobody can reproduce locally.
