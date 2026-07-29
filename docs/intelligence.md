# Intelligence Cluster

Perceive · Retrieve · Understand — the agents that build shared understanding before any test is written.

| Agent | Model | Invoke for |
|---|---|---|
| `requirements-refiner` | sonnet | INVEST scoring, ambiguity detection, acceptance criteria enrichment |
| `change-impact-analyst` | opus | Blast radius tracing and risk-ranked minimum viable test scope from a diff |
| `knowledge-fabric-curator` | sonnet | Ingesting and tagging artefacts into the RAG knowledge store |
| `rag-authoring-assistant` | sonnet | Authoring artefacts grounded strictly in retrieved organisational knowledge |

Skills: `invest-requirements-analysis` · `change-impact-scoring` · `knowledge-fabric-curation`

Retrieval quality is bounded by curation quality — `knowledge-fabric-curator` is the agent that determines how well every other RAG-dependent agent performs.

## Files

- Agents: `agents/intelligence/`
- Skills: `skills/intelligence/`
- Install: `/plugin install qa-intelligence@qz-agent-clusters`
