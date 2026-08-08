# DATABASES — ROOT NEURON

## Identity
- ID: databases.root
- Domain: databases
- Type: root
- Status: active
- Importance: critical
- Last Verified: 2026-08

## Purpose
Router for persistence decisions: choosing engines, schema design, storage, consistency, and performance of the data layer. The brain's most-referred domain.

## Activation Conditions
- persistence, schema, data model, SQL, storage engines
- consistency/durability/inter

## Do Not Activate When
- API-layer questions unrelated to data shape (go api/)
- pure runtime optimization w/o DB

## Routing Rules (child selection)
```text
engine choice         → relational/ROOT + (postgresql | mysql | nosql) by workload
schema/data modeling  → relational/data-modeling
tx / consistency      → relational/transactions (+postgresql/isolation if PG)
query perf            → optimization/query-optimization (+ pg query-planner if PG; + index neurons)
read load             → caching/ROOT (only after replicas thought!)
availability/DR       → reliability/backups-recovery
scale writes          → partitioning → replication → sharding (in order!)
document/vector       → nosql/*
cache-flavor store    → nosql/redis
```

## Mandatory Questions (BEFORE any engine recommendation)
1. What are the **write and read patterns** (rates, size, burst)?
2. Consistency: strong vs eventual for this data?
3. **Data relations** (joins needed? graph? nested?)
4. Volume + growth / retention?
5. Query patterns (exact-key, range, free text, geo?)
6. Durability (financial data vs analytics logs?)
7. Concurrency (writers per sec, hot records)?
8. Ops capability (who runs pg? failover? vacuum?)
9. Security class (PII, crypto; compliance)
10. Cost appetite (managed vs self-hosted)

## Evidence requirements
- Engine claim (postgres/mysql/mongo/redis) must include version + workload context
- perf numbers must say MEASURED vs REPORTED vs ESTIMATED

## Decision Rules (allowed as guidance, not rank)
- Default: single PostgreSQL for relational needs (see its neuron), unless the workload argues otherwise (document/N:1...)
- Do NOT pick a NoSQL engine for "feels modern"; pick for data shape.
- Never recommend a second database until the first is proven to be the bottleneck (except architectural-firewalls: vector store for embeddings, cache for hot value lookups)

## Attention weights
- Transactions/concurrency → IMPORTANT for money-like domains
- Query planning/index → the #1 perf warning
- Replication/DR → only when prod HA/DR requested

## Common Failure Modes
- N+1 (django.orm) or loop-queries going unnoticed
- Connection pool exhaustion (pool size × latency vs concurrency)
- Index-less hot path (seq scans on hot table)
- Entity bloat → dead table indexing/sprawl
- Migration (schema drift, no rollback plan)

## Security checks
- least-privilege DB roles per service (not root on prod)
- encryption at rest & TLS transit (security/data-protection)
- PII handled per compliance; query log hygiene
- SQL injection: parameterized (ORM or psycopg placeholders)

## Reliability
- backups continuously tested (PG: pg_basebackup + WAL PITR)
- RPO/RTO acknowledged per workload

## Validation Checklist
- [ ] constraints recorded (scale data)
- [ ] engine chosen from data, not taste
- [ ] schema design fits load (index plan exists)
- [ ] security role model
- [ ] failure modes enumerated

## Children (all in this directory's subfolders)
databases.relational.* / databases.postgresql.* / databases.mysql / databases.nosql.* / databases.optimization.*