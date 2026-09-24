# Query Planner & EXPLAIN

## Identity
- ID: databases.postgresql.query-planner
- Type: procedure
- Status: active

## Purpose
Read the planner's mind: why queries are slow, which plan is used, and how to steer it — via statistics, indexes, and rewritten queries. **EXPLAIN is evidence; tuning without it is guesswork.**

## Core Concept
The planner picks a plan by **cost estimation** using table statistics (row counts, histograms, correlation) sampled by ANALYZE. Wrong stats → wrong plans. You influence: stats freshness, indexes, work_mem (sort/hash), planner configuration, and query shape.

## Mental Model
A navigation app choosing routes by live traffic data (stats). If the map (statistics) is stale, it sends you through blocked streets (seq scans on hot queries).

## The EXPLAIN vocabulary
- **Seq Scan** — reads whole table; fine for small, deadly for big
- **Index Scan / Index Only Scan** — uses index (covering = no heap)
- **Bitmap Heap Scan** — many matches: index → page bitmap → fetch
- **Nested Loop / Hash Join / Merge Join** — join strategies
- Costs: startup vs total, rows estimate; `actual` after ANALYZE
- **Buffers** — memory/disk touches (the real I/O story)

## Code Tiers — the diagnostic ladder

### ❌ Bad — "add index" without evidence
```sql
-- Query slow in prod:
SELECT * FROM orders WHERE user_id = 123 AND created_at > now() - '30 days'::interval;
-- indexes were added "because people say so": two single-column indexes,
-- no stats re-analysis after bulk load → planner still guesses wrong
```

### ✅ Good — look at the plan first
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE user_id = 123 AND created_at > now() - '30 days'::interval;
-- notice: Seq Scan, 12M rows read, filter keeps 3 rows
```

### ⚡ Better — stats + targeted index, plan rechecked
```sql
ANALYZE orders;                                    -- fresh statistics
CREATE INDEX idx_orders_user_created ON orders (user_id, created_at DESC);
EXPLAIN (ANALYZE, BUFFERS) SELECT ... ;            -- now Index Scan; cost -90%
```

### 🏆 Excellent — systematic
```sql
-- 1) confirm plan before/after with identical params (pgbench or application queries)
-- 2) pg_stat_statements shows the top offender list
-- 3) if plan flips with data skew → consider:
--    * expression/partial indexes (WHERE status='active')
--    * correlation checks (BRIN for append-ordered)
--    * planner config (only when measured: enable_seqscan etc. — LAST resort)
-- 4) PG18: planner statistics survive pg_upgrade — but still re-ANALYZE after big loads
```

## Decision Rules
1. EXPLAIN first. Always. (VERIFIED methodology)
2. Fresh stats before conclusions (autovacuum/ANALYZE defaults are good; after bulk loads: ANALYZE)
3. Costs are estimates — `actual` vs `estimated` mismatch = stale stats
4. Index for the slowest top-5 via pg_stat_statements
5. Huge work_mem doesn't cure bad plans — index/pick better query shape
6. When joining with heavy sort → work_mem/hash settings, only after measured

## Failure modes
- params plans cached vs generic (join collapse), PG12+ custom plans still possible
- nerd issues: wrong stats (vacuumless), correlation decay
- hint-plague: forcing seqscan off permanently

## Observability
- pg_stat_statements (calls, mean/max time, rows)
- auto_explain (log slow plans with params) — golden tool in prod
- EXPLAIN ANALYZE BUFFERS on the app's actual query strings

## Performance
- Measure first: EXPLAIN (ANALYZE, BUFFERS) for query shape; pg_stat_statements for hot queries (S-044/S-047). No index/cache without measurement per PERFORMANCE_ENGINE.
- p95/p99 before/after; one change at a time.

## Reliability
- Timeouts on DB/client, retry with jitter + idempotency, backup/PITR tested monthly (S-046), RPO/RTO defined.
- Failure: pool exhaustion -> shed load, replica lag -> read-your-writes check.

## Evidence
- PostgreSQL docs: planner, EXPLAIN (VERIFIED); PG18 stats-preserving upgrade (VERIFIED)