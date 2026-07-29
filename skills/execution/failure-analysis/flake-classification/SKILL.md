---
name: flake-classification
description: "Name the mechanism behind a flaky test — timing race, shared state, order dependency, unseeded randomness, network, animation, clock or resource contention — and the fix for each. Use when a test passes on retry."
---

# Flake classification

## Flake sub-classification

Name the mechanism. "Flaky" without a mechanism is not a diagnosis.

| Mechanism | Signature | Fix |
|---|---|---|
| Timing race | Fails under parallelism or on slow runners | Wait for state, not time |
| Shared state | Fails when run after a specific other test | Isolate fixture data |
| Order dependency | Passes alone, fails in suite | Make the test self-sufficient |
| Unseeded randomness | Fails intermittently with different data | Seed the generator |
| Network non-determinism | Fails on external calls | Stub or contract-test |
| Animation/transition | Fails on element interception | Wait for a stable state |
| Clock/timezone | Fails at particular times of day or near midnight | Freeze the clock, pin the timezone |
| Resource contention | Fails only at high shard counts | Bound parallelism or pool resources |
