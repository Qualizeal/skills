---
name: signal-capture
description: "Collect corrections, rejections, outcome signals and escaped defects, and classify each learning to its correct destination — skill, knowledge fabric, agent prompt or human. Use during retrospectives or after a defect escape."
---

# Signal capture

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
