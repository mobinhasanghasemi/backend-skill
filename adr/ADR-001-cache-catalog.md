# ADR-001: Cache strategy for catalog accepted

- **Status:** accepted
- **Date:** 2026-08-10
- **Owner:** backend chapter
- **Related neurons:** databases/postgresql/ROOT.md, caching/ROOT.md, caching/strategies.md, caching/redis-ops.md, performance/ROOT.md, reliability/backup-drill.md

## Context
Catalog reads 1200 req/s peak, p95 340ms (SeqScan on 8M rows), DB CPU 71%. Writes 4/s. Stale tolerance 60s. Team=3, single PG primary. Requirement: stay on monolith + single DB if possible (SIMPLICITY_GOVERNOR).

## Alternatives
- A) Index only (partial index on category+created_at) — rejected: p95 180ms, still single-node read pressure at 2k req/s
- B) Cache-everything — rejected: invalidation fan-out, stale risk on adjacent domains, ops cost unearned

## Decision
Partial index `orders(category, created_at)` + read replica → then Redis 8 cache-aside `catalog:{id}:v2:{tenant}` TTL 60s±jitter, explicit delete on write, single-flight rebuild, hit-ratio metrics, per-tenant keys (ARCH025).

## Consequences
+ p95 38ms (measured k6 2k req/s), DB CPU 22%, hit 94%
- +1 component (Redis), invalidation complexity, replica lag <50ms must be monitored
- Regression signal: `cache.hit_ratio <0.85` or `p95 >100ms` → alert and re-ADR

## Validation loop
- Criteria: EXPLAIN shows Index Scan, hit >0.9, stale window test passes, replica lag <50ms
- Result: 2026-08-11 — all green; drill restore of replica OK
