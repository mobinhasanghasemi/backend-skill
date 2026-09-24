# Partitioning vs Sharding — PostgreSQL Scale Path

## Identity
- ID: databases.postgresql.partitioning-vs-sharding
- Domain: databases
- Type: procedure
- Status: active
- Importance: high
- Last Verified: 2026-08

## Purpose
Pick the correct write-scale step for PG: partitioning (single node) vs sharding (multi-node) — with numeric thresholds, not lore.

## Core Concept
Partitioning splits a table into children on one node (pruning, retention, index size). Sharding splits across nodes (routing, 2PC, rebalancing). Partition first, replicate, then shard — per databases/ROOT.

## Activation Conditions
- Table >10M rows, hot writes, or retention deletes are heavy; S-045 relevant

## Decision Rules
- **Partition** when: single-node write headroom exists, need pruning (`WHERE created_at BETWEEN`), or TTL deletes (`DROP PARTITION` vs `DELETE`). Range by `created_at` or hash by `tenant_id`; keep <100 partitions (S-045).
- **Sharding** only when: single-node writes saturated (CPU/IO/wal), or size > node limit, or noisy-neighbor isolation required — after replica + partitioning exhausted. Needs router (Citus/pg_shardman) + cross-shard tx avoidance.
- Thresholds (measure, not guess): partition at 10M rows or 50GB; shard at 100M+ rows or 500GB or p95 write >100ms with partitioning done.

## Security
- Partition pruning must respect RLS (S-048); sharding router must enforce tenant routing (no cross-shard leak).

## Performance
- EXPLAIN shows `Append` + `Partition pruning`; index per partition; autovacuum per partition tuning (S-011).

## Reliability
- Partition: one backup; shard: per-shard PITR + rebalancing plan; both need partition/shard-aware monitoring.

## Evidence
- PG partitioning VERIFIED via S-045, replication via S-046, RLS via S-048 (accessed 2026-08).

## Code Tiers
<!-- executable -->
```sql
-- range partition (executable, PG 14+)
CREATE TABLE orders (id uuid PRIMARY KEY, tenant_id uuid, created_at timestamptz NOT NULL) PARTITION BY RANGE (created_at);
CREATE TABLE orders_2026_08 PARTITION OF orders FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
-- pruning verified: EXPLAIN SELECT * FROM orders WHERE created_at BETWEEN '2026-08-10' AND '2026-08-11';
```
