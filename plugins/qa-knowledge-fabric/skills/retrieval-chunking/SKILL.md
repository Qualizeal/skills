---
name: retrieval-chunking
description: "How to split documents on semantic boundaries with heading breadcrumbs preserved, so a retrieved fragment still carries its context. Use when preparing a document for indexing or when retrieval returns the right document but the wrong passage."
---

# Chunking for retrieval

## Chunking rules

- Split on semantic boundaries — section headings, procedure steps, table rows that stand alone.
- Target 200-500 tokens. Never split mid-procedure or mid-table.
- Prefix every chunk with its heading breadcrumb (`Document title > Section > Subsection`) so a retrieved fragment carries its own context.
- Keep code blocks and their explanatory sentence in the same chunk.
- Overlap by one sentence at chunk boundaries where prose runs continuously.
