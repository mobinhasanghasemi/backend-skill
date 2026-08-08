# Architecture Evolution — From Simple to Scale

## Identity
- ID: architecture.evolution.stages
- Type: process
- Domain: architecture

## The stages in detail

### Stage 0 — Simple (MVP, internal)
- one app server + one DB (auto-managed) + backups
- artifacts: genome visible here

### Stage 1 — Measured optimization
- profile, query optimizes, indexes, cache hot reads
- now: keep complexity LOW; measure everything

### Stage 2 — Scaling reads
- read replicas (DB), edge cache, CDN
- consistency note: read-after-write on replica (routing deterministic)

### Stage 3 — Scaling writes / async
- by queues: background jobs, then messaging/streams when *ordering + replay* needed
- partition writes where justified (partitioning.md)

### Stage 4 — Teams grow
- module boundaries first (modular monolith); extraction to services ONLY on team/scale mismatch
- strangled per capability

### Stage 5 — Extreme
- k8s (at 500-1000 RPS+ self-managed? OR compliance mandates)
- multi-region/cells only with a real reason

## When each stage fires (signal → response table)

| Signal | Response stage |
|---|---|
| DB CPU > 70% at peak (queries fine) | replicas / cache |
| Slow queries in top-10 (pg_stat_statements) | Stage 1 first |
| Writes blocked by reads | replicas + isolation |
| Queue backlog | Stage 4-ish (message system) |
| 2 teams block each other's deploys | Stage 4 module boundaries |
| 1 team, healthy | Stay put |

## The proof rule
Each escalation MUST be paired with measured evidence (metrics, profile data, log data of the trait). No evidence → stay at the current stage.

## Failure modes
- Skipping stages without measurement (a "theoretical" transition that jumps to distributed)
- Treating each reader-driven congestion with caching instead of read replicas
- Never load-testing the transition — simulate the new stage (load test) before committing to it