# ADR-001: Cache strategy for catalog

- **Status:** accepted
- **Date:** 2026-08-10
- **Owner:** backend chapter
- **Context:** Catalog reads 1200 req/s, p95 340ms, DB CPU 71%. Writes 4/s. Stale tolerance 60s. Team=3, single PG primary, no replica yet.
- **Alternatives:**
  - A) Direct DB + index only — rejected: still 180ms p95, replica needed at 2k req/s anyway
  - B) Full cache-everything — rejected: invalidation blast, stale money-adjacent data risk
- **Decision:** PG partial index `(category, created_at)` + read replica → then Redis cache-aside `catalog:{id}:v2:{tenant}` TTL 60s, explicit delete on write, jittered TTL, single-flight rebuild, metrics hit-ratio
- **Consequences:** p95 38ms (measured), DB CPU 22%, ops +1 (Redis), invalidation complexity; rollback = flip flag off, no schema change
- **Validation:** k6 2k req/s · EXPLAIN before/after · hit 94% · stale window test · replica lag <50ms
- **Genome:**
  ```yaml
  Before: { Style: monolith, Database: postgresql, Cache: none, Messaging: none }
  After:  { Style: monolith, Database: postgresql+replica, Cache: redis(cache-aside), Messaging: none }
  ```
