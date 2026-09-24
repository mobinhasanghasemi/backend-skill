# Connection Pooling

## Identity
- ID: databases.postgresql.connection-pooling
- Type: ops-mechanism
- Status: active

## Purpose
Control how many DB connections exist at all, whose they are, and what happens when a page spike arrives. The layer that converts "DB connection exhaustion" into "graceful queue".

## Core Concept
Each app process holding a Postgres connection = backend process + memory + `max_connections` slot. Pools (PgBouncer in transaction mode, or app-level pools like Django DB pool/HikariCP) reuse a small set of live connections across many logical requests.

## Mental Model
A valet: hundreds of drivers (requests) share 20 parked cars (connections) by handing keys (check-out) and returning them (check-in). No pool = every driver buys a new car (and the garage collapses when 500 arrive).

## Version notes
- PostgreSQL server handles 100 'open' connections easily but 1000 = trouble; pool multiplier is the correct answer.
- PgBouncer **transaction mode** allows sharing across concurrent transactions (drops session state like `SET` / temp tables — know your app)
- Newer: PgBouncer and managed (RDS Proxy, CloudSQL) — same idea

## Decision Rules
1. `pool_size = max_connections × node_count` must respect server `max_connections` (leave headroom for admin/backups)
2. Pool's **wait** is graceful; exhaustion at the DB is not
3. Long transactions/`idle in transaction` block pool (return early; watch idle)
4. For Django: `CONN_MAX_AGE` + pool for asyncio/DRF; watch threads vs connections

## Code Tiers

### ❌ Bad — no pool, too many connections
```python
# server.ml max_connections=100; 4 app nodes × 64 (all connections) 
# → "sorry, too many clients already" during spike; restart suicide
```

### ✅ Good — one pool per service (Psycopg or SQLAlchemy)
```python
from psycopg_pool import ConnectionPool
pool = ConnectionPool( // min idle 2, max 20, conninfo=..., open=False)
pool.open()  # startup
```

### ⚡ Better — sizing & health
```python
pool = ConnectionPool(
  conninfo=os.environ["DATABASE_URL"],
  min_size=2, max_size=20,
  timeout=10,             # wait instead of surprise
  check=ConnectionPool.check_connection,
)
# health: active/idle pool gauges; slow query guard (statement_timeout)
```

### 🏆 Excellent — production regimen
```text
PgBouncer (transaction mode) in front: pool=100→ app pools of ~10
  + `max_connections` overhead: 90% pool + admin + monitoring slot
  + statement_timeout & idle_in_transaction_session_timeout at DB
  + pool depth/queue dashboard; alerts: pool wait > 50ms
  + failover: two poolers / DNS to primary
  Docker/K8s: sidecar connectivity counting
```

## Failure Modes
- pool too big for max_connections → errors at boot
- pooled app keeping huge transactions open (pool starvation → latency)
- connection leak (pool timeout / never release after exception)
- `SET` session state across transaction-mode reuse → bugs

## Security
- TLS (sslmode=require) over pooled, least-priv user for app
- admin conns separate

## Observability
- pool depth gauges, wait queue ms, timeouts; server: pg_stat_activity counts by state (active/idle-in-tx)

## Performance
- Measure first: EXPLAIN (ANALYZE, BUFFERS) for query shape; pg_stat_statements for hot queries (S-044/S-047). No index/cache without measurement per PERFORMANCE_ENGINE.
- p95/p99 before/after; one change at a time.

## Reliability
- Timeouts on DB/client, retry with jitter + idempotency, backup/PITR tested monthly (S-046), RPO/RTO defined.
- Failure: pool exhaustion -> shed load, replica lag -> read-your-writes check.

## Evidence
PostgreSQL docs (max_connections), PgBouncer docs (VERIFIED); sizing numbers are context-dependent (SUPPORTED)