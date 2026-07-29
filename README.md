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

## Upgrading from 0.1.0

If your marketplace panel shows four plugins (`qa-intelligence`, `qa-design`, `qa-execution`, `qa-governance`) at version `0.1.0`, each with one skill named after its cluster folder, you are running the first build. Nothing in the client will change until the repository contents are replaced.

**Check what is actually deployed** before changing anything else:

```bash
python3 scripts/check-deployment.py            # run inside the repo you pushed
```

It prints the marketplace version, the entry count, and whether each `skills` path resolves to a real `SKILL.md`. The 0.1.0 layout is called out explicitly.

**Then replace and refresh:**

```bash
# 1. In your marketplace repo, delete the old contents and copy this build in.
#    Keep .git; replace everything else, including .claude-plugin/.
git add -A && git commit -m "Restructure: 15 independently installable capabilities" && git push

# 2. Refresh the client's cached copy — this step is not optional.
/plugin marketplace update qz-agent-clusters
/reload-plugins
```

If the panel still shows the old entries, remove and re-add the marketplace — that forces a clean clone:

```bash
/plugin marketplace remove qz-agent-clusters
/plugin marketplace add your-org/your-repo
```

Removing a marketplace uninstalls plugins installed from it, which is fine here since the old four no longer exist.

**Old plugin names are handled.** The four cluster plugins are gone, so `marketplace.json` carries a `renames` map pointing each to `null`. Existing users get a one-line notice that the plugin was removed, and the stale key is dropped from their settings, instead of a `plugin-not-found` error every session. Automatic migration needs Claude Code v2.1.193 or later.

**Marketplace name.** The install suffix comes from the `name` field in `marketplace.json`, not from the repository path — so it stays `@qz-agent-clusters` even when hosted at `your-org/skills`. Change `name` if you want the suffix to match the repo, but note that each user can register only one marketplace per name.

## Install individual capabilities

Each of the 15 capabilities is its own plugin, so you install exactly what you want:

```bash
/plugin marketplace add ./qz-agent-clusters        # local
/plugin marketplace add your-org/qz-agent-clusters # published

/plugin install qa-knowledge-fabric@qz-agent-clusters      # just this one
/reload-plugins
```

Installing a whole cluster means installing its members:

```bash
/plugin install qa-requirements-refinement@qz-agent-clusters
/plugin install qa-change-impact-analysis@qz-agent-clusters
/plugin install qa-knowledge-fabric@qz-agent-clusters
/plugin install qa-rag-augmented-authoring@qz-agent-clusters
```

Entries carry `category` set to their cluster, so `/plugin > Discover` groups them as Intelligence, Design, Execution and Governance.

### The 15 plugins and their skills

Each plugin bundles one agent with the task-level skills that agent works from. 67 skills in total.

| Plugin | Cluster | Skills | Skill names |
|---|---|---|---|
| `qa-requirements-refinement` | Intelligence | 3 | `invest-scoring`, `ambiguity-detection`, `acceptance-criteria-authoring` |
| `qa-change-impact-analysis` | Intelligence | 3 | `blast-radius-tracing`, `change-risk-scoring`, `minimum-viable-test-scope` |
| `qa-knowledge-fabric` | Intelligence | 5 | `artefact-ingestion`, `tagging-vocabulary`, `retrieval-chunking`, `redaction-policy`, `retrieval-quality-audit` |
| `qa-rag-augmented-authoring` | Intelligence | 3 | `grounding-contract`, `retrieval-quality-bar`, `citation-and-relevance-reporting` |
| `qa-test-case-design` | Design | 7 | `equivalence-and-boundary-analysis`, `decision-tables`, `state-transition-testing`, `pairwise-combinations`, `negative-and-permission-testing`, `test-level-assignment`, `traceability-matrix` |
| `qa-synthetic-test-data` | Design | 5 | `schema-derivation`, `referential-integrity`, `edge-case-distribution`, `regulatory-profiles`, `data-lineage` |
| `qa-playwright-automation` | Execution | 5 | `playwright-operating-rules`, `playwright-framework`, `playwright-locator-strategy`, `playwright-script-generation`, `playwright-mcp` |
| `qa-failure-analysis` | Execution | 4 | `failure-triage`, `flake-classification`, `locator-drift-repair`, `quarantine-policy` |
| `qa-script-maintenance` | Execution | 3 | `suite-health-audit`, `automation-repair-rules`, `test-deletion-criteria` |
| `qa-cicd-integration` | Execution | 7 | `pipeline-stage-design`, `quality-gate-definitions`, `playwright-sharding`, `github-actions-pipeline`, `azure-devops-jenkins-pipeline`, `artefacts-and-secrets`, `pipeline-debugging` |
| `qa-shift-left-security` | Execution | 4 | `stride-threat-modelling`, `security-acceptance-criteria`, `scanner-triage`, `security-testing-boundaries` |
| `qa-performance-testing` | Execution | 5 | `workload-modelling`, `slo-definition`, `test-type-selection`, `bottleneck-analysis`, `performance-reporting` |
| `qa-defect-reporting` | Governance | 4 | `defect-screening`, `defect-report-template`, `severity-and-priority`, `root-cause-categories` |
| `qa-test-metrics` | Governance | 5 | `metric-definitions`, `release-readiness-scoring`, `predictive-defect-scoring`, `metrics-reporting-rules`, `dashboard-specification` |
| `qa-continuous-learning` | Governance | 4 | `signal-capture`, `learning-validation`, `effectiveness-tracking`, `learning-loop-failure-modes` |

Skills register as `<plugin-name>:<skill-name>`, so installing `qa-knowledge-fabric` gives you `qa-knowledge-fabric:artefact-ingestion`, `qa-knowledge-fabric:tagging-vocabulary` and three more. Claude loads whichever is relevant to the task rather than the whole set.

## Layout

Files stay grouped by cluster on disk; the manifest decides what installs together.

```
qz-agent-clusters/
├── .claude-plugin/
│   └── marketplace.json               # 15 entries, one per capability
├── skills/
│   └── <cluster>/
│       └── <capability>/              # = one plugin
│           └── <skill-name>/
│               └── SKILL.md
├── agents/
│   └── <cluster>/
│       └── <agent-name>.md            # one per capability
├── docs/
├── scripts/
│   ├── validate.py
│   └── check-deployment.py
└── README.md
```

For example, `qa-knowledge-fabric` is:

```
skills/intelligence/knowledge-fabric/
├── artefact-ingestion/SKILL.md
├── tagging-vocabulary/SKILL.md
├── retrieval-chunking/SKILL.md
├── redaction-policy/SKILL.md
└── retrieval-quality-audit/SKILL.md
agents/intelligence/knowledge-fabric-curator.md
```

Each entry is one capability:

```json
{
  "name": "qa-knowledge-fabric",
  "displayName": "Knowledge Fabric",
  "source": "./",
  "strict": false,
  "skills": ["./skills/intelligence/knowledge-fabric"],
  "agents": ["./agents/intelligence/knowledge-fabric-curator.md"],
  "category": "intelligence"
}
```

Four things are load-bearing:

- **One skill and one agent per entry.** This is what makes capabilities individually installable. Bundling four skills into one entry means users can only take all four. `scripts/validate.py` warns on any entry that is not exactly 1:1.
- **Each `skills` path points at the directory containing `SKILL.md`** — never at a parent folder. `"./skills/intelligence"` registers one skill named `intelligence` with no `SKILL.md` and the cluster appears broken. The validator fails the build on this.
- **`source: "./"`** — every entry points at the marketplace root rather than a separate plugin directory.
- **`strict: false`** — the entry is the entire plugin definition. All 15 share one root, so there is deliberately no `plugin.json` anywhere in this repository; one at the root would conflict with every entry.

Skills register as `<plugin-name>:<skill-name>`, so this one is `qa-knowledge-fabric:knowledge-fabric`.

### Adding a capability

1. `skills/<cluster>/<skill-name>/SKILL.md`
2. `agents/<cluster>/<agent-name>.md`
3. One entry in `marketplace.json` pairing them
4. `python scripts/validate.py`

### Cluster bundles

If you also want one-click cluster installs, add four more entries listing each cluster's skills and agents. Deliberately not shipped: a user who installs both `qa-intelligence` and `qa-knowledge-fabric` registers the same skill twice, and the individual entries are what you asked for. Add them only if the convenience outweighs that.

## Agents vs skills

The split is applied consistently and it is the reason the restructure is cheap:

- **Agents** are *who does the work* — a role with its own context window, tool grants and system prompt. Invoke with `@agent-name`, or let Claude delegate based on the `description` field.
- **Skills** are *how the work is done* — rubrics, taxonomies, thresholds, output formats. Claude loads them when relevant, and several agents share one skill rather than each carrying a duplicate copy of the method.

Put a convention in a skill, not an agent prompt. When the convention changes you edit one file and every agent depending on it improves at once.

## Clusters — 15 agents, 15 skills, paired 1:1

Every box in the diagram is one agent and one skill. Full map in `docs/AGENT-SKILL-MAP.md`.

### Intelligence — Perceive · Retrieve · Understand

| Agent | Skill | Covers |
|---|---|---|
| `requirements-refiner` | `requirements-refinement` | INVEST rubric, ambiguity taxonomy, AC enrichment |
| `change-impact-analyst` | `change-impact-analysis` | Blast radius tracing, risk scoring, minimum viable test scope |
| `knowledge-fabric-curator` | `knowledge-fabric` | Artefact schema, tag vocabulary, chunking, redaction, workflow coverage |
| `rag-authoring-assistant` | `rag-augmented-authoring` | Grounding contract, citation format, gap declaration, relevance report |

### Design — Specify · Scope · Prepare

| Agent | Skill | Covers |
|---|---|---|
| `test-case-designer` | `test-case-design` | Partitioning, boundaries, decision tables, state transition, pairwise, traceability |
| `synthetic-data-architect` | `synthetic-test-data` | Schema derivation, referential integrity, regulatory profiles, lineage |

### Execution — Build · Run · Maintain · Secure

| Agent | Skill | Covers |
|---|---|---|
| `playwright-automator` | `playwright-automation` | Ten rules + references on framework, locators, script generation, MCP |
| `failure-analyst` | `failure-analysis-self-healing` | Triage decision tree, flake taxonomy, locator drift detection, repair |
| `script-maintainer` | `script-maintenance` | Health audit, fragility × churn scoring, quarantine ledger, deletion criteria |
| `cicd-integrator` | `cicd-integration` | Stage ordering, gates, sharding, GHA/ADO/Jenkins configs, debugging table |
| `shift-left-security` | `shift-left-security-testing` | STRIDE at BRD stage, security AC, reachability-based scanner triage |
| `performance-tester` | `performance-testing` | Telemetry-grounded workload models, SLO definition, bottleneck analysis |

### Governance — Validate · Measure · Improve

| Agent | Skill | Covers |
|---|---|---|
| `defect-reporter` | `defect-reporting-enrichment` | Screening, report template, severity vs priority, RCA categories |
| `metrics-analyst` | `test-metrics-dashboards` | Metric definitions, release readiness score, predictive scoring, panel spec |
| `continuous-learning` | `continuous-learning-loop` | Signal capture, validation bar, effectiveness tracking, failure modes |

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
