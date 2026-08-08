# Vacuum & Table Bloat

## Identity
- ID: databases.postgresql.vacuum
- Type: ops-mechanism
- Status: active

## Purpose
Manage PostgreSQL's dead-version cleanup: prevent bloat, keep xid horizons safe, and stop vacuum from ever eating your Friday.

## Core Concept
MVCC leaves dead tuples after UPDATE/DELETE; `VACUUM` reclaims them (and freezes old xids). Autovacuum runs it for you — but needs configuration sanity and your cooperation (no long-running idle transactions).

## Mental Model
A recycling truck that must keep up with the trash rate. If your buildings (long transactions) block the truck’s lane (snapshot horizon), trash piles up (bloat) until performance suffocates.

## Key knobs / thresholds
- `autovacuum` on by default; tune `autovacuum_vacuum_scale_factor` / `threshold` for big tables
- `vacuum_cost_limit` / `cost_delay` throttle (avoid I/O storms)
- `track_counts` must be on (it feeds autovacuum)
- `maintenance_work_mem` for faster vacuum
- **Freeze** limits: `autovacuum_freeze_max_age` (prevent wraparound emergencies!)

## Decision Rules
1. Long transactions = vacuum blocker. Find idle-in-transaction regularly.
2. Huge table + tiny autovacuum scale factor = practically never → set explicit thresholds per big table
3. Bloat measurement: query `pgstattuple`/`pg_stat_user_tables` (n_dead_tup, n_tup_del)
4. When bloat is severe: `VACUUM (FULL)` (locks!) vs `pg_repack` (online) — choose by outage tolerance
5. Index bloat separately: `REINDEX` (PG12+: `REINDEX INDEX CONCURRENTLY`)
6. Autovacuum must run **during** big window loads, not right after

## Signs of trouble
- table size much larger than live data (SELECT pg_total_relation_size vs pg_relation_size)
- `n_dead_tup` not falling between days
- CPU spikes at odd hours where autovacuum catches up

## Code Tiers — coupling-shaped

### ❌ Bad — no monitoring, defaults on a 50GB table
```sql
-- nothing; dead tuples grow; index scans get slow; overnight crash
```

### ✅ Good — watch and act
```sql
SELECT relname, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 100000;
-- takes action: manual VACUUM during window
```

### ⚡ Better — right-sized autovacuum
```sql
ALTER TABLE orders SET (autovacuum_vacuum_scale_factor = 0.02,
                        autovacuum_vacuum_threshold = 10000);
-- per-big-table tuning; also watch idle-in-transaction queries
```

### 🏆 Excellent — lifecycle discipline
```sql
-- 1) wraparound safety: ALTER TABLE ... SET (autovacuum_freeze_max_age = ...) tuned
-- 2) low-churn approach: exponential backoff isn't for VACUUM — it's a steady baseline
-- 3) daily alert when n_dead_tup > x% of live rows; weekly bloat report
-- 4) test pg_repack path before you need it (maintenance window rehearsal)
```

## Security/Perf/Rel notes
- VACUUM FULL takes locks: schedule, never during peak
- Bloat is the silent RDS killer; index-only scans fail if the index is 2× real size
- Replication: vacuum on primary emits WAL (replica has no separate bloat) — keep WAL archive size in mind

## Observability
- pg_stat_user_tables.*, pg_stat_archiver, WAL positioned
- autovacuum queue status (pg_stat_activity for autovacuum worker)

## Evidence
- PostgreSQL docs on VACUUM/autovacuum (VERIFIED for 15-18)