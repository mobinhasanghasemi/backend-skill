# ARCHITECTURE — ROOT NEURON

## Identity
- ID: architecture.root
- Domain: architecture
- Type: root-technique
- Status: active
- Importance: critical
- Last Verified: 2026-08

## Purpose
Router for structural decisions: how to organize systems, when to split, which pattern to apply, how to evolve.

## Activation Conditions
- any system/solution design
- "architecture", "structure", "services", "monolith vs microservices"
- evolutionary questions (tech debt, rewrites)
- review of existing system

## Do Not Activate When
- purely framework-level question (go to django/python instead)
- already-concrete implementation choice (e.g., "how do I write an index")
- a decision fully constrained to one domain

## Routing Rules (child selection)

```text
if structural organization → patterns/
if simplicity check       → SIMPLICITY_GOVERNOR.md
if inter-team stuck       → patterns/microservices.md or modular-monolith.md
if real-time/event-heavy  → patterns/event-driven.md
if reads vs writes...     → cqrs.md (only if justified)
if historic events needed → event-sourcing
if migrate from monolith  → strangler-fig.md + evolution/*
if API-of-frontends      → bff.md
if scale-safety          → cell-based.md
if multi-client API      → patterns/ (api domain embraces)
if "how do systems talk" → api/ + messaging/
```

## Mandatory Questions (before architecture verdict)

1. **Team size & structure** (Conway's Law: service boundaries must trace team boundaries)
2. **Traffic math**: current + projected (per second? per minute?)
3. **Consistency expectations**: hard (payments) or eventual (feeds)?
4. **Ops capability**: who runs it? on-call? k8s experience?
5. **Data model**: normalized? must it stay? (god-database risk)
6. **Evolution horizon**: what changes in 12–18 months?
7. **Compliance** impact (audit, retention)

## Decision Rules

- Default: **modular monolith** for most products. Only decompose when constraints demand.
- Architecture change driven by: team boundaries, measured contention, compliance isolation — established causes.
- Never adopt a distributed pattern for the future; adopt for **measured** reasons.

## Common Failure Modes (architecture domain)

- Over-architecture: multiple services + Kafka before the traffic exists
- God database: every service writes to one shared schema → tight coupling
- Silent distributed choices: K8s guessed, discovered only at day 10
- Boulder monolith (no internal boundaries) — overdue refactoring

## Anti-Patterns (see directory)

- `distributed-monolith`, `god-database`, `database-as-queue`, `sync-change` chains, `caching-everything`, `premature optimization`, `single-point-of-failure`, `unbounded-queue`, `big-bang rewrite`

## Security Checks
- Every service boundary = new attack surface → SECURITY_GUARDIAN for each
- AuthN/AuthZ must be designed, not bolted
- Internal services still require authz (zero-trust is default in production)

## Performance Checks
- No perf claim accepted without measurement at architecture level
- Any new network hop must be justified by ability to measure it

## Reliability Checks
- Each component: failure model card (brain/failure-propagation.md)
- Timeouts on every cross-service call (ARCH001)

## Evidence Requirements
- Claims about scale/“best architecture” → REQUIRE real requirement numbers, not vibes
- Official recommendation where available (e.g., Kubernetes → need justification — this is the Governor)

## Children
architecture.patterns.*, architecture.anti-patterns.*, architecture.evolution.*, architecture.system-design.*

## Parent
security, reliability, performance, observability (cross-cutting)

## Connected Neurons
- databases (data architecture)
- api
- messaging
- distributed-systems.consistency
- deployment

## AI Instructions
- For "should we split?" — run SIMPLICITY_GOVERNOR first; then pattern neurons
- Always apply the Genome — architecture comparison rather than instinct

## Questions To Ask (before recommending runtime topology)
- single team? multi-team? — which split?
- what's the actual traffic number and its shape (bursts)?
- what observability exists?

## Validation Checklist
- [ ] Constraints extracted
- [ ] Simplest pattern that satisfies
- [ ] Failure cards present
- [ ] Pattern neurons referenced where detailed
- [ ] Decision trace recorded (ADR)