# ARCHITECTURE EVOLUTION — ROOT NEURON

## Identity
- ID: architecture.evolution
- Type: process-knowledge
- Domain: architecture

## Purpose
Model how architectures change over time — the expected evolution path, when to escalate, and the constraints that force it. **Never jump to complexity without measured evidence** — the whole point is *staged, evidence-driven* change.

## Evolution model

```text
Simple Architecture
    │  (measure; bottlenecks appear)
    ▼
Targeted Optimization      (indexes, cache for hot reads, replicas)
    │  (measure; bottleneck shifts)
    ▼
Scaling                    (scale-up → replicas → partition)
    │  (new constraint: team/consistency/compliance)
    ▼
Architectural Change       (split services, add queue, add region)
    │  (each change justified: measured, mandated, or expense)
    ▼
Next plateau
```

## The staged evolution checks

Move to a stage on the right only when the left one is insufficient, each with a "bottleneck card":

1. **Simple monolith, single DB** — most products end here
2. Read pressure → read replicas + query optimization FIRST (cheap)
3. Write pressure → partition (schema-level) → shard only after
4. Async/hot parts → background jobs (queue) — not Kafka
5. Team pressure (2+ squads, release conflict) → module boundaries → extractitude
6. Scale SLO out of reach (measured) → k8s/cells/regions

## Rules
- STAGE GATE: A step requires *either* a measurement (profile, load test) *or* an explicit requirement from the stakeholder (user's team, compliance).
- GO TOO FAR penalty — the cost
- Do not "future-proof" — design the *thinnest* seam that can evolve
- Each evolution step records an ADR (why, alternatives, costs)

## Failure Modes
- The "architectural flight" pattern: adopting the full ladder (Kubernetes + Kafka + event sourcing + multi-region) for a system with no evidence step
- Extreme-late-stage architecture (cells, multi-region) for a product that would be fine as a modular monolith
- Evolution stops: tech debt accumulates, migrations never happen, the system hardens around no change