---
name: blast-radius-tracing
description: "Trace outward from changed symbols through callers and consumers, and identify the opaque edges where static tracing cannot follow — reflection, DI containers, event buses, feature flags. Use when working out what a code change can affect."
---

# Blast radius tracing

## Blast radius tracing

Trace outward from each changed symbol, at least two hops:

- **Hop 0** — the changed symbol itself.
- **Hop 1** — direct callers and direct consumers of its output.
- **Hop 2** — callers of those callers; anything reading state the symbol writes.

Record where tracing fails. Static tracing cannot follow: reflection, dynamic dispatch, dependency injection containers, event buses and message queues, string-keyed routing, feature-flag branches, ORM lifecycle hooks, or anything crossing a network boundary. Each of these is an `OPAQUE EDGE` and must appear in the output. An unreported blind spot is worse than a reported one.
