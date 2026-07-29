---
name: artefact-ingestion
description: "Canonical front-matter schema and provenance requirements for admitting a document into the shared QA knowledge store. Use when ingesting a spec, runbook, post-mortem, test plan or decision record into the knowledge base."
---

# Artefact ingestion

## Canonical artefact schema

Every ingested document carries this front matter:

```yaml
id: KF-<domain>-<nnnn>        # stable, never reused
title:
type: spec | runbook | post-mortem | test-plan | api-contract | decision-record
source:                        # path or URL of the original
author:
created:                       # ISO date
valid-until:                   # ISO date; required for anything environment-specific
supersedes:                    # id, optional
superseded-by:                 # id, optional
tags:
  domain:
  component:
  test-level:
  lifecycle-stage:
  sensitivity:
abstract:                      # one paragraph
answers:                       # list of questions this document answers
related:                       # list of ids
```

An artefact without `source` and `created` is rejected. Provenance is not optional.
