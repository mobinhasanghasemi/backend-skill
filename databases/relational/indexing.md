# Indexing (relational)

## Identity
- ID: databases.relational.indexing
- Type: knowledge
- Status: active

## Purpose
Know what an index buys and costs, when each access method fits, and how to prove an index helps.

## Core Concept
Indexes trade write cost + storage for read speed: point lookups, range scans, orderings, covering queries. They help only when the planner uses them (plan type + selectivity).

## Mental Model
The table is a stack of files; an index is a separate sorted dictionary pointing to pages. A selective lookup skips most of the pile.

## Index types (PostgreSQL focus; MySQL similar)
| Type | Best for | Cost |
|---|---|---|
| B-tree | equality, range, ORDER BY, IN | small (default) |
| Hash | simple equality | rare need (B-tree fine) |
| GIN | arrays, JSONB, full-text | write cost |
| GiST | geometry, ranges | special |
| BRIN | huge sorted-append tables (time series) | tiny; needs correlation |
| (PG18) B-tree **skip scan** | queries skipping leading columns | read trade |

Composite indexes: order matters (leftmost prefix rule) — `(user_id, created_at)` serves user's time range but not created_at alone.

## Code Tiers

### ❌ Bad — no index on hot path
```sql
-- 10M orders table, query per second: full scan
SELECT * FROM orders WHERE user_id = 123 ORDER BY created_at DESC LIMIT 10;
-- plan: Seq Scan (cost: 180k) — every request pays it
```

### ✅ Good — single index
```sql
CREATE INDEX idx_orders_user_id ON orders (user_id);
-- plan: Index Scan (cost ~8) — 20k× cheaper
```

### ⚡ Better — composite serving the real query
```sql
CREATE INDEX idx_orders_user_created ON orders (user_id, created_at DESC);
-- exactly the sort+filter in the query: no sort node
```

### 🏆 Excellent — proven, monitored, covering
```sql
-- verify with ANALYZE + actual plan:
EXPLAIN (ANALYZE, BUFFERS)
SELECT user_id, status FROM orders
WHERE user_id = 123 AND created_at > now() - interval '30 days';

CREATE INDEX idx_orders_user_created_cov
  ON orders (user_id, created_at DESC) INCLUDE (status);
-- covering index: status read from index → index-only scan (no heap fetch)
-- + pg_stat_user_indexes: idx_scan counter; drop indexes with ~0 scans
-- + btree skip scan (PG18) can now also serve missing leading columns
```

## Decision Rules
1. Index AFTER measurement (EXPLAIN shows seq scan on hot query)
2. One index serves several queries → composite covers
3. Index the FK side of joins (join perf)
4. Don't index everything (write amplification, storage)
5. **Partial indexes** for hot subsets (PG): `WHERE status='active'` — smaller, faster
6. Never "tune by heart": PG18 stats retained across upgrades (pg_upgrade) — still recheck with ANALYZE

## Anti-patterns
- index on every column "just in case" (writes slow, bloat)
- indexing low-cardinality columns alone (sex/status) — rarely helps
- function calls in WHERE that aren't expression-indexed (`WHERE lower(email)=…` needs `ON lower(email)`)

## Observability
- pg_stat_user_indexes (idx_scan, idx_tup_read)
- EXPLAIN (ANALYZE, BUFFERS) is the single proof tool
- unused-index reports (pg_stat_*)

## Performance
- Measure first: EXPLAIN (ANALYZE, BUFFERS) for query shape; pg_stat_statements for hot queries (S-044/S-047). No index/cache without measurement per PERFORMANCE_ENGINE.
- p95/p99 before/after; one change at a time.

## Reliability
- Timeouts on DB/client, retry with jitter + idempotency, backup/PITR tested monthly (S-046), RPO/RTO defined.
- Failure: pool exhaustion -> shed load, replica lag -> read-your-writes check.

## Evidence
- PostgreSQL index docs (VERIFIED); PG18 skip scan from release notes (VERIFIED)