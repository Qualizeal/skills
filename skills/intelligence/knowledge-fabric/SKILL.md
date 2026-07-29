---
name: knowledge-fabric
description: Canonical document schema, controlled tag vocabulary, chunking rules and redaction policy for the shared QA knowledge store. Use when ingesting documents into the knowledge base, tagging artefacts, or diagnosing poor retrieval quality.
---

# Knowledge fabric curation

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

## Controlled vocabulary

- **domain** — payments, identity, catalogue, fulfilment, reporting, platform
- **component** — the service or module name as it appears in the repository, exactly
- **test-level** — unit, integration, contract, e2e, performance, security, exploratory
- **lifecycle-stage** — requirements, design, build, execute, release, operate
- **sensitivity** — public, internal, restricted

Never invent a tag. Propose vocabulary additions as an explicit request; an unapproved tag is invisible to every filtered retrieval and the document is effectively lost.

## Chunking rules

- Split on semantic boundaries — section headings, procedure steps, table rows that stand alone.
- Target 200-500 tokens. Never split mid-procedure or mid-table.
- Prefix every chunk with its heading breadcrumb (`Document title > Section > Subsection`) so a retrieved fragment carries its own context.
- Keep code blocks and their explanatory sentence in the same chunk.
- Overlap by one sentence at chunk boundaries where prose runs continuously.

## Redaction policy

Scan before writing. Stop and report — do not silently redact — if you find:

- credentials, tokens, private keys, connection strings
- production personal data of any kind
- named customers or contract terms
- internal-only hostnames or URLs in a document tagged `public`

## Retrieval quality diagnosis

When retrieval degrades, sample ten recent queries and attribute each failure to one cause:

| Symptom | Likely cause | Fix |
|---|---|---|
| Right doc, wrong fragment | Chunking | Re-chunk on semantic boundaries |
| Doc exists, never retrieved | Tagging or missing abstract | Re-tag, add `answers` list |
| Nothing relevant exists | Coverage gap | Commission the artefact |
| Relevant doc ranked low | Ranking or duplication | Deduplicate, merge near-identical docs |
| Retrieved content is wrong | Stale artefact | Expire or mark superseded |

Report the distribution across these five causes, not just an aggregate quality figure.

## Workflows the fabric serves

The fabric exists to answer real workflow queries. Curate against these, and treat a workflow that cannot be answered from the corpus as a coverage gap to commission rather than a retrieval failure.

| Workflow | Needs from the fabric | Typical tags |
|---|---|---|
| `refine-jira-story` | Story templates, AC conventions, domain glossary, prior refinements of similar stories | `lifecycle-stage: requirements` |
| `refine-ado-story` | The same, plus the ADO field mapping and work-item type rules | `lifecycle-stage: requirements` |
| `audit-story-age` | Ageing thresholds, definition-of-ready, past decisions on stale stories | `lifecycle-stage: requirements` |
| `author-tests` | House test-case format, level assignment rules, prior cases for the component | `test-level: *` |
| `plan-test-automation` | Automation standards, suite structure, what is already covered | `lifecycle-stage: build` |
| `analyze-failures` | Failure taxonomy, known flakes, prior RCAs for the component | `lifecycle-stage: execute` |
| `create-defect` | Defect template, severity/priority rubrics, duplicate history | `lifecycle-stage: execute` |
| `orchestrate-quality-workflow` | The chain definitions themselves: which agent hands to which, and the entry criteria for each | `lifecycle-stage: *` |

Two consequences for curation:

- **Tool-specific variants are separate artefacts, not one merged document.** Jira and ADO refinement differ in field semantics, work-item hierarchy and transition rules. Merging them produces a document that is subtly wrong for both, and retrieval cannot tell which half applies.
- **The orchestration definitions belong in the fabric too.** If the handoff rules live only in agent prompts, no agent can answer "what happens after this step", and nobody can audit the chain.

## Coverage review

Quarterly, walk the workflow table and ask of each row: could an agent answer this from the corpus alone today? Record the answer. A row that has been "no" for two consecutive reviews is either a commissioning failure or a workflow nobody actually runs — decide which and act, rather than carrying it indefinitely.
