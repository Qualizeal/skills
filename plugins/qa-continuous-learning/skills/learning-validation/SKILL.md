---
name: learning-validation
description: "The evidence bar before a learning is written into a shared skill — at least three similar corrections — and the record each change must carry. Use before propagating any change to shared guidance."
---

# Learning validation

## The validation bar

**Never propagate a learning from a single data point.** Require at least three similar corrections before changing a shared skill. Over-fitting the system to one reviewer's preference is a real and common failure mode — it looks like responsiveness and produces a corpus that contradicts itself as reviewers change.

Each proposed change carries:

```
learning:
evidence: <count> instances, <dates>
source: corrections | rejections | outcomes | escapes
validated-by: <human>
destination: skill <name> | knowledge fabric | agent prompt
supersedes: <what this replaces, if anything>
```

Unvalidated learnings corrupt the corpus everything else reads from, and the damage is slow, diffuse and hard to trace back.
