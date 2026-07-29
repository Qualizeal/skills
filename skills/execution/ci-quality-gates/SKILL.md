---
name: ci-quality-gates
description: Standard release quality gate definitions, pipeline stage ordering, sharding and retry policy, and artefact handling for GitHub Actions, Azure DevOps and Jenkins. Use when configuring CI for tests or defining merge and release criteria.
---

# CI quality gates

## Stage ordering

Cheapest first, fail fast:

| Stage | Typical budget | Blocking |
|---|---|---|
| Lint + type check | < 2 min | Yes |
| Unit tests | < 5 min | Yes |
| Contract tests | < 5 min | Yes |
| Integration tests | < 15 min | Yes |
| Build + deploy to test env | < 10 min | Yes |
| E2E smoke (P0) | < 10 min | Yes |
| Full E2E / security / performance | parallel | Release gate, not merge gate |

## Standard gate set

Each gate needs a threshold, a rationale, an owner and an audited override path.

| Gate | Merge threshold | Release threshold |
|---|---|---|
| Unit test pass rate | 100% | 100% |
| Coverage on changed lines | ≥ 80% | ≥ 80% |
| Coverage regression | No decrease > 0.5% | No decrease |
| P0 E2E pass rate | 100% | 100% |
| Flake rate | < 2% | < 1% |
| Critical/high SAST findings | 0 new | 0 open |
| Dependency vulnerabilities | 0 new critical | 0 critical, high triaged |
| p95 latency regression | — | < 10% vs baseline |
| Open P0/P1 defects | — | 0 P0, P1 triaged with a decision |

Coverage is measured **on changed lines**, not on the whole repository. Total coverage percentage is a metric people game; changed-line coverage is one they cannot.

## Override policy

Every gate must be overridable, and every override must be recorded: who, why, which gate, and a linked follow-up. A gate with no override path gets bypassed by disabling the pipeline entirely, which loses the audit trail and the signal at once.

## Sharding

Split by historical duration, not file count. Report per-shard balance — a suite where one shard takes three times as long as the others has no effective parallelism. Rebalance when the spread exceeds 25%.

## Retry policy

- Maximum one retry, CI only.
- A test that passes on retry is reported as **flaky**, not as passed. It enters the flake ledger.
- Never retry the whole job to clear a failure. Job-level retries hide environment problems that will recur at a worse time.

## Artefacts

Always publish on failure: Playwright trace, screenshot, video, structured results (JUnit XML or equivalent), and the application logs for the window of the run. Retain 30 days for main-branch runs, 7 for PR runs.

## Secrets

From the platform's secret store only. Never in workflow files. Never echoed. Mask in logs. If a scan finds a secret in a workflow file or in history, treat it as compromised and rotate — removing the commit is not sufficient.

## Platform notes

- **GitHub Actions** — pin actions by SHA, not tag. Set `permissions` explicitly at the workflow level; the default is broader than most jobs need.
- **Azure DevOps** — use templates for shared stages; set `timeoutInMinutes` on every job.
- **Jenkins** — declarative pipelines with the shared library; avoid inline scripts that cannot be reviewed as code.

Every job needs a timeout. An unbounded hanging job blocks the queue for everyone.
