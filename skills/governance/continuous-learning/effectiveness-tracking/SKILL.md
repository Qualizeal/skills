---
name: effectiveness-tracking
description: "Track correction rate, rejection rate, outcome accuracy and attributable escapes per agent, and report honestly when the correction rate is flat. Use when reviewing whether the agent ecosystem is actually improving."
---

# Effectiveness tracking

## Effectiveness tracking

Per agent, per period:

| Metric | Definition | Healthy direction |
|---|---|---|
| Correction rate | Edits per output | Falling |
| Rejection rate | Outputs discarded entirely | Falling |
| Outcome accuracy | e.g. proportion of generated tests that ever caught a real defect | Rising |
| Attributable escapes | Production defects an agent should have caught | Falling |
| Time-to-usable | Human minutes from output to accepted artefact | Falling |

**The correction rate is the honest measure.** If it is flat, the loop is not closing — and the report must say that plainly rather than substituting activity metrics like "signals captured" or "learnings recorded". Reporting throughput instead of effect is how a feedback loop becomes theatre while everyone believes it is working.

## Retrospective output

```
## Signals captured — by source, with counts
## Validated learnings — evidence count and destination each
## Rejected candidates — and why they did not meet the bar
## Effectiveness trend — per agent, with direction and honest verdict
## Recommendations — ranked, with expected effect
```
