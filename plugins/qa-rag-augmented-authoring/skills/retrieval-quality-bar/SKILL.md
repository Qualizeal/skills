---
name: retrieval-quality-bar
description: "The checks that decide whether retrieval was good enough to write from, and how to match the structure of existing artefacts. Use before drafting, and when deciding whether to stop and report a coverage gap instead of writing."
---

# Retrieval quality bar

## Retrieval quality bar

Before writing, confirm the retrieval was good enough to write from:

- [ ] At least three distinct sources consulted, or a documented reason there are fewer
- [ ] The most recent relevant artefact is included, not just the highest-ranked
- [ ] Nothing retrieved is past its `valid-until` date
- [ ] Terminology matches the retrieved sources exactly — synonyms break traceability
- [ ] Identifiers (AC IDs, component names, environment names) are reused verbatim, never paraphrased

If retrieval returns nothing usable, say so and stop. An artefact written from an empty corpus, presented as grounded, is worse than no artefact: it will be cited later as though it were authoritative.

## Structure matching

Match the closest existing artefact of the same type rather than imposing a template. If test plans in this organisation open with a risk summary, yours does too. A structurally novel artefact forces every reader to re-orient, and it will not survive review.
