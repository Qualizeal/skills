---
name: minimum-viable-test-scope
description: "Select the smallest set of tests that would actually catch a regression for a given change, and report it with uncovered gaps and opaque edges. Use when answering what needs retesting before merge or release."
---

# Minimum viable test scope

## Minimum viable test scope

The smallest set that would catch a regression — not the smallest set that runs fast.

1. Every P0 path gets at least one end-to-end test.
2. Every changed branch gets a unit test at the decision point.
3. Every contract change gets a consumer-side contract test.
4. Every opaque edge gets a manual verification note, since automation cannot reach it.
5. Deduplicate: if an E2E test already traverses a P1 path, do not add a second.

## Output sections

Change summary with the exact ref range, impacted surfaces table, P0/P1/P2 bands with justification, uncovered gaps, opaque edges.
