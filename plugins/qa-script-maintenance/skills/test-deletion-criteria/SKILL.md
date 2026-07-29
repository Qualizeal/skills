---
name: test-deletion-criteria
description: "When to delete a test rather than repair or skip it, and the reporting format for a maintenance pass. Use when triaging a maintenance backlog or a suite that only ever grows."
---

# Test deletion criteria

## Deletion criteria

Delete a test when any of these hold, and say plainly that you are deleting it:

- It asserts nothing meaningful
- It duplicates coverage that exists at a cheaper level
- It has been quarantined more than 30 days with no owner acting
- Its fragility cost exceeds its value: repeatedly repaired, never caught a real defect
- It tests a feature that no longer exists

Track "tests deleted" as a positive maintenance metric. A suite that only ever grows is a suite nobody is maintaining.

## Output

```
## Health scorecard (with trend if history exists)
## Fragility backlog — ranked, with effort estimates
## Dead and duplicate tests — recommended for deletion, with reasons
## Runtime hotspots — with recoverable time
## Quarantine ledger — with ages and overdue items flagged
## Repairs applied this pass
```
