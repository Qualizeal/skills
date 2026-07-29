---
name: pipeline-debugging
description: "Symptom-to-cause table for pipelines that are slow, intermittently red, green while the product is broken, or routinely bypassed. Use when a pipeline has stopped producing a signal people trust."
---

# Pipeline debugging

## Debugging a bad pipeline

| Symptom | Usual cause | Fix |
|---|---|---|
| Intermittent reds nobody trusts | Flake rate above ~2% | Freeze features, fix flakes first; nothing else works until this is done |
| One shard far slower | File-count sharding | Shard by historical duration |
| Local pass, CI fail | Browser version drift, timing, missing env | Pin the container tag; check waits |
| Slow feedback | Full E2E gating merges | Move to `@p0` smoke on merge |
| Green pipeline, broken product | Tests assert too little, or gates too loose | Audit assertions; check escape rate |
| Everyone bypassing a gate | Threshold set above baseline | Re-baseline honestly |
