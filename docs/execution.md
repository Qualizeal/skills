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

Skills: `playwright-automation` · `failure-analysis-self-healing` · `script-maintenance` · `cicd-integration` · `shift-left-security-testing` · `performance-testing`

Two behaviours are enforced throughout: never make a pipeline green by suppressing a test, and never repair a broken locator by raising a timeout.

## The Playwright skill split

Four skills rather than one, because they are consulted at different moments and by different agents:

| Skill | Answers |
|---|---|
| `playwright-framework` | How is the suite structured? Config, fixtures, page objects, auth, parallelism |
| `playwright-locator-strategy` | How do I address this element, and will it survive a refactor? |
| `playwright-script-generation` | How does a designed test case become code? Templates, data-driven, codegen review |
| `playwright-mcp` | How do I drive a real browser to explore, discover locators or reproduce a defect? |

`playwright-automator` uses the first three when writing. `script-maintainer` and `failure-analyst` reach for `playwright-locator-strategy` and `self-healing-locators` when repairing. `playwright-mcp` covers the exploration loop that happens before any of them.

## Files

- Agents: `agents/execution/`
- Skills: `skills/execution/`
- Install: `/plugin install qa-execution@qz-agent-clusters`
