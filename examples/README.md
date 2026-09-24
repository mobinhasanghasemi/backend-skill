# Examples — 3 traced decisions (before/after genome)

Each example is a complete reasoning trace per `DECISION_ENGINE.md` + ADR + genome diff.

## 1) Cache strategy for catalog (`ADR-001`)
- **Problem:** 1200 req/s catalog reads, p95 340ms (DB SeqScan)
- **Decision:** PG partial index → read replica → Redis cache-aside with `catalog:{id}:v{version}:{tenant}` + TTL 60s + explicit invalidation on write
- **Genome diff:**
  ```
  Old: monolith + single PG + no cache
  New: monolith + PG + replica + redis (cache-aside)
  Why: measured hot reads (95% hit), stale tolerance 60s, SIMPLICITY_GOVERNOR passed
  ```
- **Files:** `examples/adr-001-cache-catalog.md` · `examples/genome-001.yaml`

## 2) Outbox for webhook delivery (`ADR-002`)
- **Problem:** payment webhook lost on crash (at-least-once required)
- **Decision:** transactional outbox + Celery relay + idempotent consumer + DLQ
- **Genome diff:** `+ outbox + queue (celery/redis) + idempotency store`
- **Files:** `examples/adr-002-outbox-webhook.md`

## 3) Row-Level Security vs app-enforced authz (`ADR-003`)
- **Problem:** multi-tenant SaaS, IDOR risk (ARCH014)
- **Decision:** PG RLS for tenant isolation (defense in depth) + app-level check + per-tenant cache keys
- **Files:** `examples/adr-003-rls-vs-app.md`

### How to use
1. Read `BRAIN.md` pipeline
2. Pick one example, follow its trace
3. Adapt constraints → re-run Decision Engine → new ADR
