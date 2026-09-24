# Query Optimization (relational)

## Identity
- Type: procedure
- Importance: medium
- ID: databases.optimization.query-optimization
- Status: active
- Importance: critical

## Purpose
The practical method to make a slow query fast — with evidence at each step, free of guesswork.

## Diagnostic ladder
1. What is slow? (which query; latency from application, not "everything")
2. Reproduce with same data
3. `EXPLAIN (ANALYZE, BUFFERS)` — the current plan
4. Identify the node's cost: SeqScan on bottleneck? Hash join spool? sort spill?
5. Hypothesis: missing index? stale stats? wrong join order? work_mem? ORM missevery
6. Change ONE thing → re-EXPLAIN
7. Benchmark identical input → compare (plan shape + actual time + buffers)
8. Ship if metrics say win; LINT the rest

## The toolbelt
- Indexes (data-modeling/indexing) — the #1
- Composite/partial/covering indexes
- query shape (WHERE on indexed expr, avoid function calls on columns)
- JOIN strategy steering (settings as last resort)
- work_mem for sorts/hash joins (big sorts spill to disk)
- LIMIT + pagination (cursors) shapes
- Denormalization/materialized views for hot aggregates/projections

## Code Tiers (one love-pass)

### ❌ Bad
```sql
SELECT * FROM orders
WHERE status = 'paid' AND created_at > now() - interval '7 days'
ORDER BY created_at DESC;
-- no index: Seq Scan on 20M rows for 40 rows serviced
```

### ✅ Good
```sql
CREATE INDEX idx_orders_status_created ON orders (status, created_at DESC);
-- plan: Index Scan + no Sort node
```

### ⚡ Better — partial index (hot subset)
```sql
CREATE INDEX idx_orders_active_created ON orders (created_at DESC)
WHERE status = 'paid';
-- index only for paid: smaller, everything cached hot
```

### 🏆 Excellent — verified + monitored
```sql
-- measure: EXPLAIN (ANALYZE, BUFFERS) before/after; assert same params
-- pg_stat_statements: this query moves out of top-20
-- covering index if repeated access of same cols (INCLUDE)
-- watch plan regressions over time (auto_explain logs plan changes)
```

## Anti-patterns
- Index first, ask later (write-amplification)
- Changing SQL to "please the planner" without EXPLAIN
- Tuning server settings before query shape
- SELECT * in hot loops

## Rules
- Explain before and after, always. Plan output is evidence
- Selectivity: index helps when row subset is small (selectivity < ~5%)
- Functions in WHERE need expression indexes

## Evidence: PG/MySQL docs EXPLAIN (VERIFIED)