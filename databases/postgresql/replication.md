# Replication & Failover

## Identity
- ID: databases.postgresql.replication
- Type: ops-mechanism
- Status: active

## Purpose
Understand replication modes (streaming vs logical), how replicas serve reads and failover, lag, and consistency choices — the chief currency of PG availability.

## Core Concept
- **Streaming replication** (WAL-based, physical): a replica replays the primary's WAL; same data files, **can't filter**, used for failover + read scaling
- **Logical replication** (PG16+/18 matured): replication via WAL→logical slots; per-table granularity, cross-version → used for migrations, feature queues, analytics
- **Synchronous vs asynchronous** commitment; sync = durability (zero loss), async = low latency (loss window)
- Failover: Patroni/PG Have-a or managed (RDS/Aurora style), streaming + archive catchup; 18 adds parallel streaming + auto-drop idle slots

## Mental Model
Primary keeps a journalist's notes (WAL); replicas read those notes at their own pace (lag); when the editor dies, a copy takes over (failover). Sync = printer waits for each sheet to confirm receipt.

## Decisions
- RPO: async → minutes of loss; sync → zero loss (at latency + availability price of the standby)
- Replicas for reads: only when reads tolerate lag (ARCH rules in mind) & you route writes to primary
- Failover automation vs manual (Patroni: needed for nines beyond 3 in self-managed)
- Replication slots: monitor (slots falling behind → WAL growth!)

## Code Tiers — failures start in config

### ❌ Bad (config)
```
primary_conninfo = 'host=replica1 port=5432 user=repl password=... sslmode=prefer'
# no slot, no checksums, hot_standby off, no monitoring
```

### ✅ Good (baseline)
```
hot_standby = on
max_standby_streaming_delay = -1        # default sane
# monitor: pg_stat_replication
wal_level = replica           # needed for streaming
```

### ⚡ Better — safety
```
# enable synchronous replication on the money-critical DB:
synchronous_standby_names = 'ANY 1 (replica1, replica2)'
# + checksums (default in PG18) + replication slot:
-- SELECT * FROM pg_create_physical_replication_slot('replica1_slot');
```

### 🏆 Excellent — production stack
```
Patroni (or hosted equivalent) manages: leader election, automatic failover,
restart on node loss, health checks
+ physical slots for both replicas (no gap)
+ logical replication ONLY for specific needs (analytics sink / migration)
+ lag alerts (< 30s threshold), failover drills monthly
+ PITR from WAL archive continues working post-failover
```

## Failure Modes
- replication slot leak → WAL unbounded → disk full (watch !resolve)
- lag explosion during long transactions on primary
- sync replication can halt writes if quorum standbys are down (choose `synchronous_standby_names` wisely)
- Standby misconfigured to accept writes (promotion races)

## Observability
- pg_stat_replication (write_lag, replay_lag, flush_lag)
- slot fields (`pg_replication_slots`: restart_lsn, active)
- WAL/EIO counters in 18; alerts for lag > SLO

## Performance
- Measure first: EXPLAIN (ANALYZE, BUFFERS) for query shape; pg_stat_statements for hot queries (S-044/S-047). No index/cache without measurement per PERFORMANCE_ENGINE.
- p95/p99 before/after; one change at a time.

## Reliability
- Timeouts on DB/client, retry with jitter + idempotency, backup/PITR tested monthly (S-046), RPO/RTO defined.
- Failure: pool exhaustion -> shed load, replica lag -> read-your-writes check.

## Evidence
- PostgreSQL docs (streaming/logical, 18 parallel streaming) — VERIFIED; reconciles failover practices as ops-manual (SUPPORTED)