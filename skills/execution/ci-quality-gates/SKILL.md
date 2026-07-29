---
name: ci-quality-gates
description: Pipeline design and release quality gates for test execution — stage ordering, gate thresholds and overrides, Playwright sharding and report merging, working GitHub Actions, Azure DevOps and Jenkins configurations, artefact and secret handling. Use when configuring CI for tests, defining merge or release criteria, or debugging a slow or noisy pipeline.
---

# CI pipelines and quality gates

A pipeline has one job: produce a signal people believe. A pipeline that is red half the time for reasons unrelated to the change trains everyone to ignore it, and then it protects nothing.

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

## Gate definitions

Every gate needs four things: a threshold, a rationale, a named owner, and an audited override path.

| Gate | Merge | Release |
|---|---|---|
| Unit test pass rate | 100% | 100% |
| Coverage on changed lines | ≥ 80% | ≥ 80% |
| Coverage regression | No drop > 0.5% | No drop |
| `@p0` E2E pass rate | 100% | 100% |
| Flake rate | < 2% | < 1% |
| New critical/high SAST findings | 0 | 0 open |
| New critical dependency CVEs | 0 | 0; highs triaged |
| p95 latency regression | — | < 10% vs baseline |
| Open P0/P1 defects | — | 0 P0; P1 decided |

**Changed-line coverage, not total.** Total coverage percentage is gamed by testing easy code and is insensitive to exactly the lines most likely to break — the ones that just changed.

**Set thresholds at or just above the current baseline.** A gate set to aspiration gets disabled within a fortnight, and then you have neither the gate nor the honesty.

## Override policy

Every gate must be overridable and every override recorded: who, which gate, why, and a linked follow-up. A gate with no override path gets bypassed by disabling the pipeline entirely — which loses the audit trail and the signal at the same time.

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

## Azure DevOps

```yaml
trigger: [main]

pool:
  vmImage: ubuntu-latest

jobs:
  - job: e2e
    timeoutInMinutes: 30
    strategy:
      parallel: 4
    steps:
      - task: NodeTool@0
        inputs: { versionSpec: '20.x' }
      - script: npm ci && npx playwright install --with-deps
      - script: npx playwright test --shard=$(System.JobPositionInPhase)/$(System.TotalJobsInPhase)
        env:
          TEST_USER_PASSWORD: $(TEST_USER_PASSWORD)
      - task: PublishTestResults@2
        condition: succeededOrFailed()
        inputs:
          testResultsFormat: JUnit
          testResultsFiles: 'results/junit.xml'
          mergeTestResults: true
```

Use templates for shared stages, and set `timeoutInMinutes` on every job.

## Jenkins

```groovy
pipeline {
  agent { docker { image 'mcr.microsoft.com/playwright:v1.50.0-noble' } }
  options { timeout(time: 30, unit: 'MINUTES'); disableConcurrentBuilds() }
  stages {
    stage('E2E') {
      steps {
        sh 'npm ci'
        withCredentials([string(credentialsId: 'test-user-password', variable: 'TEST_USER_PASSWORD')]) {
          sh 'npx playwright test --grep @p0'
        }
      }
    }
  }
  post {
    always {
      junit 'results/junit.xml'
      archiveArtifacts artifacts: 'playwright-report/**', allowEmptyArchive: true
    }
  }
}
```

Declarative pipelines with a shared library; avoid inline scripts that cannot be reviewed as code.

## Retry policy

- At most one retry, CI only.
- A test that passes on retry is reported as **flaky**, not as passed, and enters the flake ledger.
- Never retry the whole job to clear a failure. Job-level retries hide environment problems that will recur at a worse moment.

## Artefacts

Publish on failure, always: Playwright trace, screenshot, video, JUnit XML, blob report, and application logs covering the run window. Retain 30 days for main-branch runs, 7 for PR runs. Traces are the difference between a five-minute diagnosis and a two-hour reproduction attempt.

## Secrets

Platform secret store only. Never in workflow files, never echoed, masked in logs. If a scan finds a secret committed anywhere in history, treat it as compromised and rotate it — removing the commit does not un-publish it.

## Debugging a bad pipeline

| Symptom | Usual cause | Fix |
|---|---|---|
| Intermittent reds nobody trusts | Flake rate above ~2% | Freeze features, fix flakes first; nothing else works until this is done |
| One shard far slower | File-count sharding | Shard by historical duration |
| Local pass, CI fail | Browser version drift, timing, missing env | Pin the container tag; check waits |
| Slow feedback | Full E2E gating merges | Move to `@p0` smoke on merge |
| Green pipeline, broken product | Tests assert too little, or gates too loose | Audit assertions; check escape rate |
| Everyone bypassing a gate | Threshold set above baseline | Re-baseline honestly |
