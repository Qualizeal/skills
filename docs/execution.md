# Execution Cluster

Build · Run · Maintain · Secure — the largest cluster, covering everything from writing a test to gating a release.

| Agent | Model | Invoke for |
|---|---|---|
| `playwright-automator` | sonnet | Web UI and REST/GraphQL automation |
| `failure-analyst` | opus | Triaging red pipelines into defect / test defect / environment / flake |
| `script-maintainer` | sonnet | Suite health, locator drift, fragility backlog |
| `cicd-integrator` | sonnet | Pipeline wiring and release quality gates |
| `shift-left-security` | opus | BRD-stage threat modelling and scanner triage |
| `performance-tester` | sonnet | Telemetry-grounded load, stress, soak and spike testing |

Skills: `playwright-conventions` · `self-healing-locators` · `ci-quality-gates`

Two behaviours are enforced throughout: never make a pipeline green by suppressing a test, and never repair a broken locator by raising a timeout.

## Files

- Agents: `agents/execution/`
- Skills: `skills/execution/`
- Install: `/plugin install qa-execution@qz-agent-clusters`
