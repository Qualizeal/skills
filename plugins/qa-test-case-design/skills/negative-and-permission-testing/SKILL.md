---
name: negative-and-permission-testing
description: "The per-input negative checklist and the CRUD-by-role permissions matrix, including the rule that every denial is tested at the API rather than assumed from hidden UI. Use when designing error-path and authorisation cases."
---

# Negative and permission testing

## 6. Negative testing checklist

Per input: empty · null · whitespace only · wrong type · exceeds max length · below min · malformed encoding · unicode and RTL · SQL/script injection payload · path traversal payload · duplicate submission · concurrent modification · expired token · insufficient permission.

Per operation: what happens if it is retried? Interrupted halfway? Called twice concurrently? Called by a user who lost permission between page load and submit?

## 7. CRUD and permissions matrices

For any resource, walk the grid rather than trusting that the implementation is uniform. Authorisation defects hide in the cells nobody thought about.

| Role | Create | Read own | Read others' | Update own | Update others' | Delete |
|---|---|---|---|---|---|---|
| Anonymous | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Customer | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ |
| Staff | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| Admin | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Every ✗ needs a test that it is genuinely denied — and denied at the API, not merely hidden in the UI. A hidden button is not an authorisation control.
