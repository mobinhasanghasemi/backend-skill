# Playbook: Database Down / Slow

> Procedure playbook — run top-down; do not skip steps.

## Symptoms
- app timeouts/500s on DB-connected endpoints; pool exhaustion errors ("too many clients"); slow queries across the board; PG reads stalled

## Fast triage (first 10 min)
1. Confirm scope: one endpoint, one node, or all DB users? → dashboards (metrics-recipes)
2. DB basic health: `SELECT 1`, load, connections: `pg_stat_activity` (active / idle-in-transaction), locks: `pg_locks` (long blockers)
3. Resources: CPU/memory/disk (iostat); WAL growth (disk full?)
4. Recent deploys / migrations / data changes → roll back if the collision is there
5. incident channel + status page (incident-response.md)

## Likely causes & specific action
| Signal | Action |
|---|---|
| active queries long (EXPLAIN shows seq scans) | kill/analyze; index the hot query (query-optimization.md) |
| `idle in transaction` wall | terminate with SIGTERM PIN; wake the app (idle-in-tx = vacuum deadly!) |
| Connections exhausted | bulkhead: reduce pool, kill stuck txns; pgbouncer pooled mode |
| Disk 100% (WAL bloat!) | log cleanup + archive; replication slot stuck (replication.md) |
| CPU pegged with simple queries | replicas pressure (fail over) or autoscaler; check lookups explosion |

## Long-term (post-triage)
- Replay proof: pg_stat_statements top query list (plan each), add the missing index (EXPLAIN measured)
- autovacuum proper (vacuum.md); connection budget table (connection-pooling)
- chaos drill: failover path tested in staging before "DR faithful"
- ADR: write down what changed (query, connection, replica) — one finding, one incremental test

## Rollback
(replicate deletion: re-apply plan only when argument carries new EXPLAIN+bihai data); else record time-based service delay

## Prevention
- Slow query regressions in CI (auto_explain / pg_stat snapshot); SLO on DB latency