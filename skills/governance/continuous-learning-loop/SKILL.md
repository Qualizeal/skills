---
name: continuous-learning-loop
description: Closing the feedback loop on agent output — capturing correction, rejection, outcome and escape signals, classifying and validating learnings before propagation, and tracking whether quality is actually compounding. Use during retrospectives, after a defect escape, or when reviewing how well the agent ecosystem is performing.
---

# Continuous learning loop

Without this loop, every agent starts each sprint exactly as good as it was last sprint. The loop is what converts corrections into compounding improvement — and it only works if the reporting is honest about whether that is happening.

## Four signal sources

| Source | Signal | Usually captured? |
|---|---|---|
| **Reviewer corrections** | The edit itself: what was wrong, what the correct form was | Sometimes |
| **Outcome signals** | Did the generated test catch a real defect? Did the impact analysis miss an area that later broke? | Rarely |
| **Escaped defects** | Which agent in the chain could have caught it, and what would it have needed to know? | At post-mortem only |
| **Rejected output** | Output discarded entirely | Almost never |

The last row is the most informative and the least recorded, because nobody files a ticket about work they threw away. Ask for it directly in retrospectives; it will not arrive on its own.

## Classification

| Class | Destination | Example |
|---|---|---|
| Missing knowledge | Knowledge fabric, via the curation pipeline | The agent did not know the SLA for this service |
| Wrong convention | The **skill** — conventions never belong in an agent prompt | Test IDs written in camelCase, house style is kebab |
| Prompt gap | The agent's instructions | The agent skipped a required output section |
| Model limitation | Documented; route the task to a human | Judgement calls on visual polish |
| One-off | Recorded, not generalised | A reviewer's personal phrasing preference |

Routing matters. A convention fixed in one agent's prompt improves one agent; the same fix in a skill improves every agent that reads it.

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

## Failure modes to watch for

| Failure mode | Symptom | Fix |
|---|---|---|
| Loop theatre | Signals rise, correction rate flat | Report the flat metric; investigate routing |
| Over-fitting | Skills contradict each other | Raise the evidence bar; review conflicts |
| Prompt sprawl | Agent prompts grow with conventions | Move conventions to skills |
| Silent rejection | Correction rate looks great, adoption is low | Measure rejection separately |
| Stale learnings | Corpus contradicts current practice | Expire on a schedule; date every learning |
