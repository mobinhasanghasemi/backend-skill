# PostgreSQL — ROOT NEURON

## Identity
- ID: databases.postgresql
- Type: technology-root
- Status: active
- Importance: critical
- Last Verified: 2026-08

## Purpose
Router and truth-center for PostgreSQL-specific knowledge: engine architecture, tuning, and ops.

## Version snapshot (2026-08)
- Current: **18.x** (18.0 Sep 2025; minor 18.4 May 2026; EOL ~Nov 2030)
- Themes: async I/O (AIO), B-tree skip scan, `uuidv7()`, virtual generated columns (now default), **OAuth authentication**, wire protocol 3.2, page checksums on by default, **MD5 auth deprecated** (use SCRAM), `pg_upgrade` preserves planner statistics, temporal constraints, `RETURNING OLD/NEW`
- Older: 17.x (EOL ~Nov 2029), 16.x (EOL ~Nov 2028)

## Activation Conditions
- "postgres", "psql", relational storage engine choice
- EXPLAIN, vacuum, replication, failover, backups (PG flavor)

## Do Not Activate When
- MySQL/SQLite-specific semantics (their neurons cover)

## Routing Rules
```text
transaction/isolation → relational/transactions + postgresql/mvcc + isolation.md
query slowness        → query-planner (EXPLAIN) + indexing
data freshness        → vacuum.md (bloat, autovacuum)
scale reads           → replication.md (read replicas, failover)
large tables          → partitioning.md
connection issues     → connection-pooling.md
crash/data loss       → backup-restore.md (WAL, PITR)
id design             → data-modeling (uuidv7 tip in PG18)
```

## Mandatory checks (whenever PG is in the stack)
- Backup & PITR verified? (restore drill!)
- Connection pooling in front of the app? (pool exhaustion = classic)
- `max_connections` vs pool size vs RAM
- Autovacuum on, bloat under watch
- `work_mem` realistic (sort/hash on large sets)
- Auth: SCRAM (MD5 deprecated in 18), TLS required, roles least-privilege
- Monitoring: `pg_stat_statements`, `pg_stat_activity`, `pg_stat_io`

## Decision rules (family-level guidance, not mandate)
PG is the default relational candidate when: rich SQL (partial indexes, JSONB, FTS, geospatial via PostGIS), strong consistency, advanced replication, extension ecosystem. MySQL alternative when: legacy/team expertise/cloud-managed MySQL mandate.

## Failure modes
- vacuum starvation (long-running idle-in-transaction)
- bloat (MVCC dead tuples) → query/IO regression
- connection exhaustion
- replication lag → stale reads / failover data loss window
- checkpoint storms, WAL growth unbounded
- long-running transactions blocking vacuum & locks

## Security
- TLS (SSL) enforcement; SCRAM auth (MD5 deprecated in 18)
- least-privilege roles; row-level security for tenancy (databases/postgresql/rls.md)
- encryption at rest (cluster/disk-level), data checksums default in 18
- pg_hba tight; no trust auth in prod

## Performance
- measure with EXPLAIN (ANALYZE, BUFFERS); pg_stat_statements for top queries
- PG18 AIO improves read-heavy workloads (benchmark reported up to 3× — treat as EXPERIMENTAL vendor claim until measured)
- index discipline (relational/indexing)

## Reliability
- WAL archiving + PITR, streaming replication + failover (pg_auto_failover/Patroni)
- sync vs async replication trade (durability vs latency)
- Regular restore drills (untested backup ≈ no backup)

## Observability
- pg_stat_statements, pg_stat_activity, pg_stat_io (18), pg_stat_replication (lag), pg_stat_user_tables (bloat-ish)
- query/error logs (pgAudit extension if needed)

## Evidence
- PostgreSQL official docs + release notes (VERIFIED via source-S-010, accessed 2026-08)
- Vendor benchmarks labelled EXPERIMENTAL/REPORTED, not reproduced here