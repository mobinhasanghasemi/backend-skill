# Database Performance Tuning (engine)

## Identity
- Type: procedure
- Importance: medium
- ID: databases.optimization.performance-tuning
- Status: active

## Purpose
Right-sized server settings and operational budgets for a database — AFTER query shape is handled. Tuning without a baseline is guesswork.

## The honest rule
- Workloads discriminate. Tuning = changing variables under reproducible load tests
- Defaults (PostgreSQL autovacuum, MySQL auto-sizing pools) are current-friendly for OLAP/OLTP — don't covet "best config" guides blindly
- Every change: before/after measurement

## Settings commonly adjusted (verify current advice per version!)
**PostgreSQL**
- `shared_buffers` (≈25% if dedicated RAM), `effective_cache_size`, `work_mem` (≈small; for big sorts raise per-session!), `maintenance_work_mem`, `max_connections` ↔ pooling, `checkpoint_*` (chunks/stall), `wal_*`, `synchronous_commit`, `autovacuum_*` per-table

**MySQL**
- `innodb_buffer_pool_size` (70-80% for dedicated), `innodb_flush_log_at_trx_commit` (1 = safest), `innodb_log_file_size`, `max_connections`, `key_buffer_size` (MyISAM— legacy), `sql_mode` sanity

## Only-if evidence (each knob needs data)
- pool size → cache hit %, RAM budget
- work_mem → sort/hash spill counters
- connections → pool queue depth observed
- fsync → WAL commit ms latency/D value

## Tier ladder (apply in this order!)
1. Confirm OS/database **I/O stack** (storage class, iops/latency profile) — this is where "tuning" starts
2. Buffer sizes per measurement
3. settings per behavior AFTER (2)
   work_mem up only for specific sessions
4. Advanced: autovacuum calibrations, bloat cleanup

Never: changing settings "because a guide says so"; never: `max_connections=1` bandage that halves the exact bottleneck symptom.

## Capstones
- Benchmark protocol: same dataset+load, before/after table
- Record each change in an ADR-like note: WHY (which measured signal), effect, rollback state
- Re-validate after upgrades: many upgrades change defaults or check hints — recheck conflicting performance knobs on every major version

## Evidence: official docs VERIFIED; "measure, then change" as method (STRONGLY SUPPORTED by perf practice)