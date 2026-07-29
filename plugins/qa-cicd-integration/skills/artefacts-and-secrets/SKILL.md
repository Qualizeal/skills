---
name: artefacts-and-secrets
description: "Retry policy that reports flakes instead of hiding them, what to publish on failure and for how long, and secret handling including what to do when one is found in history. Use when configuring CI reporting or reviewing pipeline security."
---

# Retries, artefacts and secrets

## Retry policy

- At most one retry, CI only.
- A test that passes on retry is reported as **flaky**, not as passed, and enters the flake ledger.
- Never retry the whole job to clear a failure. Job-level retries hide environment problems that will recur at a worse moment.

## Artefacts

Publish on failure, always: Playwright trace, screenshot, video, JUnit XML, blob report, and application logs covering the run window. Retain 30 days for main-branch runs, 7 for PR runs. Traces are the difference between a five-minute diagnosis and a two-hour reproduction attempt.

## Secrets

Platform secret store only. Never in workflow files, never echoed, masked in logs. If a scan finds a secret committed anywhere in history, treat it as compromised and rotate it — removing the commit does not un-publish it.
