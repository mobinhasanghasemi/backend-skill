# Partitioning (PostgreSQL)

## Identity
- ID: databases.postgresql.partitioning
- Type: mechanism
- Status: active — use for size/time-driven tables, not landmine

## Purpose
Divide one large table into smaller physical tables (partitions) sharing one logical schema — for session-level maintenance, performance on time/data pruned queries, and bulk deletion.

## Core Concept
Parent table with `PARTITION BY RANGE|LIST|HASH`. Queries hitting partition keys prune to the relevant partition(s). Partitioned tables are child tables; indexes per partition. PG11+: full partition-write-path (insert routing, FKs, unique+global?). PG18: better partition pruning & joins; virtual gen cols on partitions.

## When to partition (triggers)
- table > tens of GB (or **> disk of maintenance ops**)
- time-bounded data (logs, events, orders by date) with retention
- queries always filter by the partition key
- vacuum/target maintenance per partition

## When NOT to
- small tables (partition overhead)
- no partition-key filter in queries (prune doesn't matter)
- over-partitioning (hundreds of partitions = planning cost)

## Mental Model
A filing cabinet with drawers per month. Reading only asks for the right drawer (pruning). Cleaning = throw away an old drawer (drop partition) — instead of vacuuming the whole archive.

## Code Tiers

### ❌ Bad — late or naive
```sql
-- single table grows to 500GB; deleting old rows = slow bulk DELETEs, indexes bloated
```

### ✅ Good — range partitioned by time
```sql
CREATE TABLE events (
  id bigint GENERATED ALWAYS AS IDENTITY,
  occurred_at timestamptz NOT NULL,
  ...
) PARTITION BY RANGE (occurred_at);

CREATE TABLE events_2026_08 PARTITION OF events
  FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
-- queries with occurred_at in range prune easily
```

### ⚡ Better — operations-shaped
```sql
-- retention = DETACH + DROP (instant-ish, no giant DELETE):
ALTER TABLE events DETACH PARTITION events_2026_06;
DROP TABLE events_2026_06;

-- autovacuum per partition; partition-level analyze; indexes per partition
CREATE INDEX ON events (user_id, occurred_at DESC) LOCAL;
```

### 🏆 Excellent — full production
```sql
-- pre-created partitions via cron for next 2 months (no write to missing partition)
-- default partition for out-of-range (with alert on usage!)
-- partition pruning verified per query: EXPLAIN shows "Append" only on needed parts
-- composite unique constraint: partition key MUST appear in unique/PRIMARY KEY
-- retention SLO, and per-partition autovacuum thresholds tuned
```

## Decisions
- Partition AND index per partition (indexes don't cross partitions)
- unique/primary key **must include the partition key**
- FK from non-partitioned table → avoid (post-update FKs to partitions = complexity)
- declarative partitioning; avoid manual inheritance

## Failure Modes
- queries without partition key → seq-scan all partitions (pruning miss)
- default partition swallowing junk → check constraint drift
- huge partitions (year) reduces benefit — keep ≤30-90d per partition
- adding partitions at the wrong frequency (monthly vast)

## Observability
- per-partition size, scan counts, last vacuum; EXPLAIN prune check "Partitions scanned: 1/31"

## Evidence
- PostgreSQL partitioning docs (VERIFIED, 15-18)