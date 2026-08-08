# Playbook: Migration Locking Prod

## Symptoms
- ALTER running long; `pg_locks` shows AccessExclusive; queries queue (wait_event Lock); dashboards: active_sessions spike, p99 rise

## Stop-the-bleed (fast)
1. **Identify the lock** (pg_locks + pg_stat_activity: who holds AccessExclusive, who waits)
2. **The safe move**: cancel the migration session if it's still harmless (DDL would have chained); wait time tracked
3. If cancellable: cancel gracefully (SIGINT), keep the preceding migration state intact (compiled but not applied)
4. If it's a long-running transaction holding the lock: terminate idle-in-transaction (never the app's main tx if avoidable) and let the DDL proceed — with monitoring

## Ask the three questions
- Was it **long-running write tx at all**? (blocking lock)
- Was it **big table DDL** (add NOT NULL + DEFAULT on 500M rows) → rollback impossible; it will finish 🕒. Better: stop the CALL (safe mode): pause migration job during it
- **CONCURRENTL a : add it with `lock_timeout` (fail fast) + `CREATE INDEX CONCURRENTLY` + `VACUUM FULL` alternative — post-mortem: use the rules from django/migrations.md and PG partitioning

## Root cause categories + gate
| Cause | Gate to add |
|---|---|
| NOT NULL + DEFAULT on huge table | expand/migrate/contract order |
| index building during peak | `CONCURRENTLY` + lock_timeout |
| transaction holding open too long | app code discipline (isolation.md) |
| DDL during peak load | maintenance window / `enforce on replica` |

## Post
- migration runbook recorded (steps+durations); ready-check: prod-shape staging rehearsal (PG21: amd64) — see migrations.md, lock-timeouts