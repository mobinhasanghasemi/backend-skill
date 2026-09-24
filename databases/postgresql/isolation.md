# Isolation Levels (PostgreSQL flavor)

## Identity
- ID: databases.postgresql.isolation
- Type: theory-mechanism
- Domain: databases

## Purpose
The precise behavior of read/write concurrency under each isolation level — an operational companion to transactions.md with PG-specific semantics (snapshot behavior, serialization anomalies, FOR UPDATE).

## The PG isolation table
| Level | Snapshot | Anomalies possible | Typical cost |
|---|---|---|---|
| READ COMMITTED | new per **statement** | non-repeatable read, (phantom) secondary read | ~0 |
| REPEATABLE READ | one snapshot per **transaction** (transaction ID plus xmin horizon) | write skew (two txs read same rows, write conflicting cols are allowed!) | + |
| SERIALIZABLE | SSI (predicate locks) | none under SERIALIZABLE; more conflicts → 40001 | ++ retries |

## PG-specific facts (VERIFIED)
- PG's REPEATABLE READ ≠ strict repeatable-read of the SQL standard: it's **snapshot isolation** — allows *write skew* (two writes both resulting from same snapshot)
- SERIALIZABLE = SSI; serializable anomaly detection at commit — app must RETRY on `40001` (serialization_failure)
- `SELECT ... FOR UPDATE` takes real row locks at the MVCC version level — used inside repeatable-read txs honestly
- READ COMMITTED default for PG (vs MySQL's REPEATABLE READ default) — a common cross-DB bug source

## Code Tiers

### ❌ Bad — wrong level assumption
```python
# app-level: set SERIALIZABLE for everything → worse throughput, ptree retry storms!
```

### Core guidance
- Financial two-step: REPEATABLE READ + FOR UPDATE + retry
- Reports: REPEATABLE READ snapshot; reads (no writes) safe
- Transaction-length discipline: keep txs short (locks held)

### ⚡ Better — hybrid strategy
```python
with isolation REPEATABLE READ:
    r = SELECT FOR UPDATE OF wallet WHERE uid=%s
    if r.amount < spend: raise
    UPDATE wallet SET amount = amount - %s
# concern: retry 40001 handled; deadlocks logged (23505- 40P01)
```

### 🏆 Excellent — money-grade with contention
```text
- reduce hot-row contention (partition rows by numeric mod, or advisory lock per customer)
- deadlock retry with jittered backoff on the transaction level
- PG18: NEW/OLD in RETURNING — audit updates now natural
- telemetry: transaction duration bucket, conflict/retry rates
```

## Observability
- pg_stat_database xact_commit/xact_rollback; conflict counters; deadlock log (23P)

## Performance
- Measure first: EXPLAIN (ANALYZE, BUFFERS) for query shape; pg_stat_statements for hot queries (S-044/S-047). No index/cache without measurement per PERFORMANCE_ENGINE.
- p95/p99 before/after; one change at a time.

## Reliability
- Timeouts on DB/client, retry with jitter + idempotency, backup/PITR tested monthly (S-046), RPO/RTO defined.
- Failure: pool exhaustion -> shed load, replica lag -> read-your-writes check.

## Evidence
- PostgreSQL isolation docs (VERIFIED)