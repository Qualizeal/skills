---
name: redaction-policy
description: "What must never enter the knowledge store — credentials, production personal data, customer names, internal-only URLs — and the stop-and-report rule when any is found. Use before writing any artefact into the shared corpus."
---

# Redaction policy

## Redaction policy

Scan before writing. Stop and report — do not silently redact — if you find:

- credentials, tokens, private keys, connection strings
- production personal data of any kind
- named customers or contract terms
- internal-only hostnames or URLs in a document tagged `public`
