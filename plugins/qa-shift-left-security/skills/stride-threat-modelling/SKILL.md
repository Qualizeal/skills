---
name: stride-threat-modelling
description: "Work STRIDE against each data flow at requirements time — spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege. Use during design or BRD review, before any code exists."
---

# STRIDE threat modelling

## Threat modelling at BRD stage

Walk STRIDE against each data flow in the feature. One row per entry point, answered concretely.

| Category | The question to answer |
|---|---|
| **S**poofing | How is the actor authenticated at each entry point? |
| **T**ampering | What protects integrity in transit and at rest? |
| **R**epudiation | What is logged, and can the actor alter or delete it? |
| **I**nformation disclosure | What is the most sensitive field here, and who can read it? |
| **D**enial of service | What is unbounded — input size, retries, fan-out, query cost, file upload? |
| **E**levation of privilege | Where is authorisation checked, and is it checked on *every* path including the API? |

The highest-yield question in practice is the last one. Hidden UI is not an access control, and features routinely ship with the button removed and the endpoint open.
