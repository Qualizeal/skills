# QZ Agent Clusters

A Claude Code plugin marketplace containing **15 purpose-built quality engineering agents** and **10 skills**, grouped by cluster at the marketplace root.

```
INTELLIGENCE          DESIGN              EXECUTION              GOVERNANCE
Perceive · Retrieve   Specify · Scope     Build · Run            Validate · Measure
Understand            Prepare             Maintain · Secure      Improve

requirements-refiner  test-case-designer  playwright-automator   defect-reporter
change-impact-analyst synthetic-data-     failure-analyst        metrics-analyst
knowledge-fabric-       architect         script-maintainer      continuous-learning
  curator                                 cicd-integrator
rag-authoring-                            shift-left-security
  assistant                               performance-tester
```

## Layout

There is no `plugins/` directory. All four clusters live side by side under `skills/` and `agents/`, and each marketplace entry claims its own subdirectory:

```
qz-agent-clusters/
├── .claude-plugin/
│   └── marketplace.json          # four entries, all source "./"
├── skills/
│   ├── intelligence/             # invest-requirements-analysis, change-impact-scoring,
│   │   └── <skill>/SKILL.md      #   knowledge-fabric-curation
│   ├── design/                   # test-design-techniques, synthetic-test-data
│   ├── execution/                # playwright-conventions, self-healing-locators,
│   │                             #   ci-quality-gates
│   └── governance/               # defect-enrichment, quality-metrics-model
├── agents/
│   ├── intelligence/  (4 agents)
│   ├── design/        (2 agents)
│   ├── execution/     (6 agents)
│   └── governance/    (3 agents)
├── docs/                         # per-cluster documentation
└── README.md
```

Each entry in `marketplace.json` looks like this:

```json
{
  "name": "qa-execution",
  "source": "./",
  "strict": false,
  "skills": ["./skills/execution"],
  "agents": ["./agents/execution"]
}
```

Three things make this work, and all three are load-bearing:

- **`source: "./"`** — every entry points at the marketplace root rather than a separate plugin directory.
- **`skills` / `agents` paths** — with a marketplace-root source, the listed paths are the *complete* set for that entry. Installing `qa-design` loads only `skills/design` and `agents/design`; the other three clusters stay dormant. Drop the `skills` field and the entry would scan the whole shared folder and pull in all ten skills.
- **`strict: false`** — the marketplace entry is the entire plugin definition. Since all four entries share one root, there can be no per-plugin `plugin.json`; a root `plugin.json` declaring components would conflict with all four and every entry would fail to load. There is deliberately no `plugin.json` anywhere in this repository.

## Install

```bash
/plugin marketplace add ./qz-agent-clusters      # local
/plugin marketplace add your-org/qz-agent-clusters   # published

/plugin install qa-intelligence@qz-agent-clusters
/plugin install qa-design@qz-agent-clusters
/plugin install qa-execution@qz-agent-clusters
/plugin install qa-governance@qz-agent-clusters

/reload-plugins
```

Validate before publishing:

```bash
claude plugin validate .
```

## Agents vs skills

The split is applied consistently and it is the reason the restructure is cheap:

- **Agents** are *who does the work* — a role with its own context window, tool grants and system prompt. Invoke with `@agent-name`, or let Claude delegate based on the `description` field.
- **Skills** are *how the work is done* — rubrics, taxonomies, thresholds, output formats. Claude loads them when relevant, and several agents share one skill rather than each carrying a duplicate copy of the method.

Put a convention in a skill, not an agent prompt. When the convention changes you edit one file and every agent depending on it improves at once.

## Clusters

### Intelligence — Perceive · Retrieve · Understand

| Agent | Model | Does |
|---|---|---|
| `requirements-refiner` | sonnet | INVEST scoring, ambiguity detection, acceptance criteria enrichment |
| `change-impact-analyst` | opus | Diff → blast radius → risk-ranked minimum viable test scope |
| `knowledge-fabric-curator` | sonnet | Ingest, structure, chunk, tag and enrich the RAG knowledge store |
| `rag-authoring-assistant` | sonnet | Authors artefacts grounded in retrieved organisational knowledge only |

Skills: `invest-requirements-analysis` · `change-impact-scoring` · `knowledge-fabric-curation`

### Design — Specify · Scope · Prepare

| Agent | Model | Does |
|---|---|---|
| `test-case-designer` | sonnet | Functional, boundary, negative and edge cases + traceability matrix |
| `synthetic-data-architect` | sonnet | Schema-aware synthetic data with lineage and zero production PII |

Skills: `test-design-techniques` · `synthetic-test-data`

### Execution — Build · Run · Maintain · Secure

| Agent | Model | Does |
|---|---|---|
| `playwright-automator` | sonnet | Web UI and REST/GraphQL automation to house conventions |
| `failure-analyst` | opus | Triage into product defect / test defect / environment / flake, with RCA |
| `script-maintainer` | sonnet | Locator drift, fragility backlog, dead tests, runtime hotspots |
| `cicd-integrator` | sonnet | GitHub Actions, Azure DevOps, Jenkins pipelines and release gates |
| `shift-left-security` | opus | BRD-stage threat modelling, SAST/DAST triage by exploitability |
| `performance-tester` | sonnet | Telemetry-grounded workload models and SLA validation |

Skills: `playwright-conventions` · `self-healing-locators` · `ci-quality-gates`

### Governance — Validate · Measure · Improve

| Agent | Model | Does |
|---|---|---|
| `defect-reporter` | sonnet | Enriched reports with RCA, duplicate and false-positive screening |
| `metrics-analyst` | sonnet | Release readiness, coverage, defect density, predictive scoring |
| `continuous-learning` | sonnet | Captures correction signals, validates and feeds them back |

Skills: `defect-enrichment` · `quality-metrics-model`

## How the clusters chain

```
requirements-refiner ──► test-case-designer ──► playwright-automator ──► cicd-integrator
        │                        │                       │
        │                synthetic-data-architect   failure-analyst ──► defect-reporter
        │                                                │                     │
change-impact-analyst ──────────────────────────► script-maintainer      metrics-analyst
        ▲                                                                      │
        └──────────── knowledge-fabric-curator ◄──── continuous-learning ◄─────┘
```

Example: `@change-impact-analyst` scopes a PR → `@test-case-designer` fills the coverage gaps it found → `@playwright-automator` automates the P0 cases → `@failure-analyst` triages what goes red → `@continuous-learning` feeds the correction back into the knowledge fabric.

## Adding to a cluster

Drop the file in the right subdirectory. No manifest edit is needed, because each entry claims a directory rather than a file list:

- New skill → `skills/<cluster>/<skill-name>/SKILL.md`
- New agent → `agents/<cluster>/<agent-name>.md`
- New cluster → create both directories, then add one entry to `marketplace.json`

## Customising before you publish

1. **`owner`** in `marketplace.json`.
2. **Thresholds** in `ci-quality-gates` and `quality-metrics-model` — coverage floors, flake ceilings and readiness weights should reflect your current baseline, not aspiration. Gates set above where a team actually sits get disabled within a fortnight.
3. **Controlled vocabulary** in `knowledge-fabric-curation` — the `domain` and `component` lists must match your real service names, or filtered retrieval will not find the documents.
4. **Model assignments** in agent frontmatter — `opus` on the three reasoning-heavy agents, `sonnet` elsewhere. Use `inherit` to follow the session model instead.
5. **Tool grants** — agents get the minimum they need. Widen deliberately.

## Validation

```bash
pip install pyyaml && python scripts/validate.py   # structural, auth-free, runs in CI
claude plugin validate .                            # official schema check
```

`scripts/validate.py` catches the failure modes specific to this shared-root layout: a stray `plugin.json`, an entry missing its `skills`/`agents` paths (which would silently load all four clusters), two entries claiming the same directory, a skill directory without a `SKILL.md`, and frontmatter names that drift from their filenames. `.github/workflows/validate-marketplace.yml` runs both on every PR.

## Publishing

1. Push to a git host with `.claude-plugin/marketplace.json` at the repository root.
2. Share `/plugin marketplace add your-org/qz-agent-clusters`.
3. For automatic team rollout, add the marketplace to `extraKnownMarketplaces` in the project's `.claude/settings.json`.
4. Bump `version` on each entry every release — with a pinned version, users receive nothing until that string changes.

One constraint this layout inherits: `source: "./"` is a relative path, so it resolves only for git-based or local marketplaces. If you ever distribute a bare `marketplace.json` over a URL, only that file is downloaded and the relative sources will not resolve — switch to `github` or `git-subdir` sources at that point.

Reference: https://code.claude.com/docs/en/plugin-marketplaces
