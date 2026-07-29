# Agent ↔ skill map

Every box in the cluster diagram is one **plugin**, containing one agent and one skill. Fifteen of each, paired 1:1, each installable on its own.

| # | Cluster | Diagram item | Agent | Skill |
|---|---|---|---|---|
| 1 | Intelligence | Requirements Refinement | `requirements-refiner` | `requirements-refinement` |
| 2 | Intelligence | Change Impact Analysis | `change-impact-analyst` | `change-impact-analysis` |
| 3 | Intelligence | Knowledge Fabric Agent | `knowledge-fabric-curator` | `knowledge-fabric` |
| 4 | Intelligence | RAG-Augmented Authoring | `rag-authoring-assistant` | `rag-augmented-authoring` |
| 5 | Design | Test Case Design | `test-case-designer` | `test-case-design` |
| 6 | Design | Synthetic Test Data | `synthetic-data-architect` | `synthetic-test-data` |
| 7 | Execution | Playwright Automation | `playwright-automator` | `playwright-automation` |
| 8 | Execution | Failure Analysis & Self-Healing | `failure-analyst` | `failure-analysis-self-healing` |
| 9 | Execution | Script Maintenance | `script-maintainer` | `script-maintenance` |
| 10 | Execution | CI/CD Integration | `cicd-integrator` | `cicd-integration` |
| 11 | Execution | Shift-Left Security | `shift-left-security` | `shift-left-security-testing` |
| 12 | Execution | Performance Testing (RIC) | `performance-tester` | `performance-testing` |
| 13 | Governance | Defect Reporting & Enrichment | `defect-reporter` | `defect-reporting-enrichment` |
| 14 | Governance | Test Metrics & Dashboards | `metrics-analyst` | `test-metrics-dashboards` |
| 15 | Governance | Continuous Learning | `continuous-learning` | `continuous-learning-loop` |

## Why 1:1

The pairing keeps ownership unambiguous: each capability has exactly one place its behaviour is defined (the agent) and one place its method is defined (the skill). Adding a capability means adding both; retiring one means deleting both.

The split within each pair stays the same as before:

- The **agent** is the role — its workflow, its tool grants, its output contract, its judgement calls.
- The **skill** is the method — rubrics, thresholds, taxonomies, formats, worked examples. Skills load on relevance, so a human or another agent can read the method without invoking the role.

## Where depth lives

Only one skill needs more than a single file. `playwright-automation` carries ten operating rules in its `SKILL.md` and four references beside it:

```
skills/execution/playwright-automation/
├── SKILL.md                          # the rules, plus routing
└── references/
    ├── framework.md                  # config, fixtures, page objects, auth
    ├── locator-strategy.md           # the priority ladder, strictness, test-ids
    ├── script-generation.md          # test case → code, codegen review
    └── playwright-mcp.md             # live browser exploration, MCP vs CLI
```

This is progressive disclosure: the agent reads `SKILL.md` every time and pulls a reference only when the task calls for it. Splitting these into four sibling skills instead would have broken the 1:1 mapping and put four Playwright entries against one diagram box.

Any other skill can grow the same way — add a `references/` directory beside its `SKILL.md` when one file stops being enough.
