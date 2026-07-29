# QZ Agent Clusters

A Claude Code plugin marketplace: **15 independently installable QA capabilities** across four clusters. Each plugin bundles one agent with its task-level skills — **67 skills** in total.

## Layout

Every plugin is a self-contained directory. Skills and agents are **auto-discovered** from the conventional folders, so there are no paths in `marketplace.json` that can drift out of sync with the files.

```
qz-agent-clusters/
├── .claude-plugin/
│   └── marketplace.json                  # 15 entries: name + source only
└── plugins/
    └── qa-knowledge-fabric/
        ├── .claude-plugin/plugin.json
        ├── agents/
        │   └── knowledge-fabric-curator.md
        ├── skills/
        │   ├── artefact-ingestion/SKILL.md
        │   ├── tagging-vocabulary/SKILL.md
        │   ├── retrieval-chunking/SKILL.md
        │   ├── redaction-policy/SKILL.md
        │   └── retrieval-quality-audit/SKILL.md
        └── README.md
```

Each plugin's `plugin.json` also declares its skills and agents explicitly:

```json
{
  "name": "qa-knowledge-fabric",
  "version": "3.1.0",
  "skills": [
    "./skills/artefact-ingestion",
    "./skills/redaction-policy",
    "./skills/retrieval-chunking",
    "./skills/retrieval-quality-audit",
    "./skills/tagging-vocabulary"
  ],
  "agents": ["./agents/knowledge-fabric-curator.md"]
}
```

Both mechanisms are in place deliberately. Claude Code discovers skills by walking `skills/`; other tooling — including the VS Code marketplace panel — reads the arrays in `plugin.json` and shows only what is listed there. `scripts/validate.py` fails the build if the arrays and the folders ever disagree, in either direction.

And the marketplace entry repeats them, because some viewers read only the catalog and never open the plugin directory:

```json
{
  "name": "qa-knowledge-fabric",
  "displayName": "Knowledge Fabric",
  "version": "3.2.0",
  "source": "./plugins/qa-knowledge-fabric",
  "skills": [
    "./skills/artefact-ingestion",
    "./skills/redaction-policy",
    "./skills/retrieval-chunking",
    "./skills/retrieval-quality-audit",
    "./skills/tagging-vocabulary"
  ],
  "agents": ["./agents/knowledge-fabric-curator.md"]
}
```

Three levels declare the same thing on purpose:

| Level | Read by |
|---|---|
| `skills/<name>/SKILL.md` folders | Claude Code, by walking the directory |
| `plugin.json` `skills` array | tools that open the plugin manifest |
| marketplace entry `skills` array | viewers that read only the catalog |

A viewer with none of these to go on falls back to a default version and a placeholder count of one skill — which looks exactly like a broken build. `scripts/validate.py` fails if any level is missing or disagrees with the files.

Previously the entry was just:

```json
{
  "name": "qa-knowledge-fabric",
  "displayName": "Knowledge Fabric",
  "source": "./plugins/qa-knowledge-fabric",
  "category": "intelligence"
}
```

Everything else comes from the plugin's own `plugin.json`, and the components come from the folder structure. Adding a skill is one step: drop `skills/<name>/SKILL.md` into the plugin directory. No manifest edit, nothing to forget.

## Install

```bash
/plugin marketplace add Qualizeal/skills
/plugin install qa-knowledge-fabric@qz-agent-clusters
/reload-plugins
```

Each capability installs on its own. Skills register as `<plugin>:<skill>`, so that one gives you `qa-knowledge-fabric:artefact-ingestion` and four others.

## The 15 plugins

| Plugin | Cluster | Skills |
|---|---|---|
| `qa-requirements-refinement` | Intelligence | 3 — `acceptance-criteria-authoring`, `ambiguity-detection`, `invest-scoring` |
| `qa-change-impact-analysis` | Intelligence | 3 — `blast-radius-tracing`, `change-risk-scoring`, `minimum-viable-test-scope` |
| `qa-knowledge-fabric` | Intelligence | 5 — `artefact-ingestion`, `redaction-policy`, `retrieval-chunking`, `retrieval-quality-audit`, `tagging-vocabulary` |
| `qa-rag-augmented-authoring` | Intelligence | 3 — `citation-and-relevance-reporting`, `grounding-contract`, `retrieval-quality-bar` |
| `qa-test-case-design` | Design | 7 — `decision-tables`, `equivalence-and-boundary-analysis`, `negative-and-permission-testing`, `pairwise-combinations`, `state-transition-testing`, `test-level-assignment`, `traceability-matrix` |
| `qa-synthetic-test-data` | Design | 5 — `data-lineage`, `edge-case-distribution`, `referential-integrity`, `regulatory-profiles`, `schema-derivation` |
| `qa-playwright-automation` | Execution | 5 — `playwright-framework`, `playwright-locator-strategy`, `playwright-mcp`, `playwright-operating-rules`, `playwright-script-generation` |
| `qa-failure-analysis` | Execution | 4 — `failure-triage`, `flake-classification`, `locator-drift-repair`, `quarantine-policy` |
| `qa-script-maintenance` | Execution | 3 — `automation-repair-rules`, `suite-health-audit`, `test-deletion-criteria` |
| `qa-cicd-integration` | Execution | 7 — `artefacts-and-secrets`, `azure-devops-jenkins-pipeline`, `github-actions-pipeline`, `pipeline-debugging`, `pipeline-stage-design`, `playwright-sharding`, `quality-gate-definitions` |
| `qa-shift-left-security` | Execution | 4 — `scanner-triage`, `security-acceptance-criteria`, `security-testing-boundaries`, `stride-threat-modelling` |
| `qa-performance-testing` | Execution | 5 — `bottleneck-analysis`, `performance-reporting`, `slo-definition`, `test-type-selection`, `workload-modelling` |
| `qa-defect-reporting` | Governance | 4 — `defect-report-template`, `defect-screening`, `root-cause-categories`, `severity-and-priority` |
| `qa-test-metrics` | Governance | 5 — `dashboard-specification`, `metric-definitions`, `metrics-reporting-rules`, `predictive-defect-scoring`, `release-readiness-scoring` |
| `qa-continuous-learning` | Governance | 4 — `effectiveness-tracking`, `learning-loop-failure-modes`, `learning-validation`, `signal-capture` |

## Agents vs skills

- **Agents** are *who does the work* — a role with its own context window, tool grants and system prompt. Invoke with `@agent-name`, or let Claude delegate on the `description` field.
- **Skills** are *how the work is done* — rubrics, thresholds, taxonomies, formats, worked examples. Claude loads whichever matches the task rather than the whole plugin, which is the point of splitting them.

Put a convention in a skill, not an agent prompt. Change it once and every agent reading it improves.

## Validate

```bash
pip install pyyaml && python3 scripts/validate.py
claude plugin validate .
```

The validator checks that every plugin directory is listed, every listed source exists and has a `plugin.json`, every skill directory has a `SKILL.md` whose frontmatter name matches its folder, and that no description contains an unquoted `": "` (which breaks YAML silently and stops the skill loading).

Expect: `15 plugins, 67 skills, 15 agents — 0 errors`.

## Deploy

```bash
python3 scripts/check-deployment.py     # what is actually live
```

See `HOW-TO-RUN.md` for Windows specifics, `DEPLOY.md` for the update procedure.

Version history:

| Version | Layout |
|---|---|
| 0.1.0 | 4 cluster plugins, shared root |
| 1.0.0 | 15 plugins, 1 skill each, shared root |
| 2.0.0 | 15 plugins, 67 skills, shared root with explicit skill paths |
| 3.0.0 | 15 self-contained plugin directories, skills auto-discovered |
| 3.1.0 | as 3.0.0, plus explicit `skills`/`agents` arrays in every `plugin.json` |
| **3.2.0** | **plus `version` and `skills`/`agents` arrays in every marketplace entry** |

The shared-root layout (`source: "./"` with `strict: false`) required every skill path to be listed by hand in `marketplace.json`. It worked, but a single wrong path silently loaded one broken skill instead of the cluster, and that is what caused the repeated "only one skill" problem. 3.0.0 removes the failure mode rather than documenting it.
