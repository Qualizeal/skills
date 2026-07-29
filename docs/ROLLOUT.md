# Rollout checklist

## Phase 0 — before anyone else sees it

- [ ] `pip install pyyaml && python scripts/validate.py` → 0 errors
- [ ] `claude plugin validate .` → passes
- [ ] `/plugin marketplace add ./qz-agent-clusters` locally
- [ ] Install one cluster, `/reload-plugins`, confirm `/agents` lists only that cluster's agents
- [ ] Run each agent once against a real artefact from your codebase — a real PR, a real story, a real red pipeline
- [ ] Replace the `owner` block in `marketplace.json`
- [ ] Decide the final plugin `name` slugs. **This is the last cheap moment to change them** — the slug is immutable once published, and renaming breaks every existing install unless you ship a `renames` map

## Phase 1 — calibrate the thresholds

The defaults are reasonable, not yours. Measure first, then set gates at or just above the current baseline. Gates set to aspiration get disabled within a fortnight and then everyone ignores the pipeline.

- [ ] `ci-quality-gates` — changed-line coverage floor, flake ceiling, latency regression budget
- [ ] `quality-metrics-model` — readiness weights and the component floors
- [ ] `knowledge-fabric-curation` — replace the `domain` and `component` vocabularies with your real service names. An unlisted tag makes a document invisible to filtered retrieval
- [ ] `playwright-conventions` — reconcile with your existing `playwright.config` and page-object layout

## Phase 2 — pilot on one team

- [ ] Pick the cluster with the clearest pain. `qa-execution` and `qa-intelligence` usually show value fastest
- [ ] One team, two sprints, one cluster
- [ ] Track the correction rate: how much of each agent's output gets edited before use. Falling means the skills are converging on your conventions; flat means they aren't and the skills need editing, not the prompts
- [ ] Feed every recurring correction back into the **skill**, not the agent prompt

## Phase 3 — organisation rollout

- [ ] Publish to your git host
- [ ] Add `extraKnownMarketplaces` + `enabledPlugins` to the team repositories' `.claude/settings.json` (see `docs/team-settings.json`)
- [ ] Enable the CI validation workflow
- [ ] Name an owner per cluster. Unowned skills go stale, and a stale skill is worse than no skill because it is confidently wrong
- [ ] Set a review cadence — quarterly is usually enough

## Phase 4 — keep it honest

- [ ] Run `@continuous-learning` each retrospective
- [ ] Re-baseline thresholds every quarter as the real numbers improve
- [ ] Delete agents nobody invokes. A cluster of fifteen where four get used is worse than a cluster of four
