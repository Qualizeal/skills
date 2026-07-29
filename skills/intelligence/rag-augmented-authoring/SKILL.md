---
name: rag-augmented-authoring
description: Grounding rules for authoring QA artefacts from retrieved organisational knowledge — the in-network retrieval contract, citation format, gap declaration, conflict handling and the contextual relevance report. Use when writing test plans, test cases, runbooks or QA documentation that must follow this organisation's conventions rather than generic best practice.
---

# RAG-augmented authoring

The point of retrieval-augmented authoring is that the output reflects *this* organisation, not the industry average. An artefact that could have been written without reading anything has failed, however polished it reads.

## The grounding contract

1. **Retrieve before writing.** Search the knowledge fabric, the existing test suite and prior artefacts of the same type. No exceptions, including for topics you know well — what you know is the general case, and the general case is what the reader could have got elsewhere.
2. **In-network only.** Every substantive claim — a naming convention, an SLA figure, an environment name, a business rule, a threshold — traces to a retrieved artefact.
3. **Cite inline** as `[source: <path or KF-id>#<section>]`. A claim without a citation is either generic or invented, and the reader cannot tell which.
4. **Declare gaps.** Where the corpus is silent, mark the passage `[UNGROUNDED — generic guidance]`. Never quietly fill a gap with a plausible default; that is how a convention nobody agreed to becomes the standard.
5. **Surface conflicts.** When two sources disagree, present both and name the conflict. Silently picking one hides a decision that belongs to a human.
6. **Prefer linking over restating.** Duplicated content drifts out of sync. Link to the canonical artefact and summarise in one line.

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

## Contextual relevance report

Every artefact ends with this. It is the reader's basis for trusting the rest.

```
## Retrieval note
Sources consulted: N        Sources used: M
Grounded: <estimate>%       Ungrounded passages: K (marked inline)
Most recent source: <id / date>
Conflicts found: <none | description>
Coverage gaps worth commissioning: <list>
```

Be honest about the grounded percentage. An inflated figure is the single most damaging thing this role can produce, because it converts an unreliable artefact into a trusted one.

## Anti-patterns

| Anti-pattern | Why it damages | Instead |
|---|---|---|
| Writing first, retrieving to confirm | You find sources that agree with you | Retrieve, then write |
| Paraphrasing an identifier | Breaks traceability silently | Reuse verbatim |
| Filling a gap with best practice | Invents a local convention | Mark `[UNGROUNDED]` |
| Picking a side in a source conflict | Hides a human decision | Present both |
| Restating a linked document | Two copies, one goes stale | Link and summarise |
| Reporting 100% grounded | Almost never true; destroys trust when found out | Estimate honestly |
