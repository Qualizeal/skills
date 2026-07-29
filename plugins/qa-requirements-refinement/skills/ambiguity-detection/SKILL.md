---
name: ambiguity-detection
description: "Nine-category taxonomy for finding ambiguity in requirements — weasel words, unquantified comparatives, missing actors, undefined states, implicit assumptions, dangling pronouns, compound requirements, unbounded quantities and missing error paths. Use when reviewing a story, PRD or spec for anything untestable as written."
---

# Ambiguity detection

## Ambiguity taxonomy

Flag every occurrence and quote the offending text.

1. **Weasel words** — fast, robust, seamless, intuitive, appropriate, reasonable, as needed, etc.
2. **Unquantified comparatives** — better, faster, more secure. Compared to what, by how much?
3. **Missing actor** — passive voice hiding who performs the action ("the record is archived").
4. **Undefined state** — references a status, mode or flag with no definition or enumeration.
5. **Implicit assumption** — behaviour that only makes sense given an unstated precondition.
6. **Dangling pronoun** — "it", "this", "they" with more than one possible referent.
7. **Compound requirement** — one line specifying two independently testable behaviours; split it.
8. **Unbounded quantity** — any list, upload, retry or timeout with no stated limit.
9. **Missing error path** — a success behaviour with no specified failure behaviour.
