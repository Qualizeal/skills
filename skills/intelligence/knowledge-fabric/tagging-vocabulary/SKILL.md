---
name: tagging-vocabulary
description: "The controlled tag vocabulary — domain, component, test-level, lifecycle-stage, sensitivity — and the rule against inventing tags. Use when tagging or classifying an artefact, or when filtered retrieval is failing to find documents that exist."
---

# Tagging and controlled vocabulary

## Controlled vocabulary

- **domain** — payments, identity, catalogue, fulfilment, reporting, platform
- **component** — the service or module name as it appears in the repository, exactly
- **test-level** — unit, integration, contract, e2e, performance, security, exploratory
- **lifecycle-stage** — requirements, design, build, execute, release, operate
- **sensitivity** — public, internal, restricted

Never invent a tag. Propose vocabulary additions as an explicit request; an unapproved tag is invisible to every filtered retrieval and the document is effectively lost.
