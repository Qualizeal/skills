---
name: acceptance-criteria-authoring
description: "House format and rules for writing Given/When/Then acceptance criteria, plus the coverage checklist every story must satisfy before it is declared ready. Use when writing or rewriting acceptance criteria, or checking a story covers its negative paths and boundaries."
---

# Acceptance criteria authoring

## Acceptance criteria format

```
AC-<n>  Given <precondition in a known state>
        When <single action by a named actor>
        Then <observable, measurable outcome>
        And <side effect, if any: audit entry, notification, state change>
```

Rules:
- One action per AC. If the When clause contains "and", split it.
- The Then clause must be checkable by someone who cannot see the code.
- Numeric and temporal fields need boundary ACs at min, min-1, max, max+1.
- Every AC needs a stable ID; downstream traceability matrices key on it.

## Coverage checklist

Before declaring READY, confirm the story has:
- [ ] Happy path
- [ ] At least one negative/error path
- [ ] Boundaries on every numeric, temporal or length-constrained field
- [ ] Permission/role behaviour if the feature is role-sensitive
- [ ] Empty, single and maximal state for any list or collection
- [ ] Idempotency or concurrency behaviour if the action can be repeated or raced
- [ ] Explicitly stated non-goals

## Output

Scorecard table, numbered ambiguity list with rewrites, refined AC set, open questions marked `NEEDS DECISION`, and a one-line verdict.
