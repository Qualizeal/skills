---
name: grounding-contract
description: "The rules for writing only from retrieved organisational knowledge — retrieve before writing, cite inline, declare gaps, surface conflicts, link rather than restate — with the anti-pattern table. Use when authoring any artefact that must follow house conventions rather than generic advice."
---

# Grounding contract

## The grounding contract

1. **Retrieve before writing.** Search the knowledge fabric, the existing test suite and prior artefacts of the same type. No exceptions, including for topics you know well — what you know is the general case, and the general case is what the reader could have got elsewhere.
2. **In-network only.** Every substantive claim — a naming convention, an SLA figure, an environment name, a business rule, a threshold — traces to a retrieved artefact.
3. **Cite inline** as `[source: <path or KF-id>#<section>]`. A claim without a citation is either generic or invented, and the reader cannot tell which.
4. **Declare gaps.** Where the corpus is silent, mark the passage `[UNGROUNDED — generic guidance]`. Never quietly fill a gap with a plausible default; that is how a convention nobody agreed to becomes the standard.
5. **Surface conflicts.** When two sources disagree, present both and name the conflict. Silently picking one hides a decision that belongs to a human.
6. **Prefer linking over restating.** Duplicated content drifts out of sync. Link to the canonical artefact and summarise in one line.

## Anti-patterns

| Anti-pattern | Why it damages | Instead |
|---|---|---|
| Writing first, retrieving to confirm | You find sources that agree with you | Retrieve, then write |
| Paraphrasing an identifier | Breaks traceability silently | Reuse verbatim |
| Filling a gap with best practice | Invents a local convention | Mark `[UNGROUNDED]` |
| Picking a side in a source conflict | Hides a human decision | Present both |
| Restating a linked document | Two copies, one goes stale | Link and summarise |
| Reporting 100% grounded | Almost never true; destroys trust when found out | Estimate honestly |
