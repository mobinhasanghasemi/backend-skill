# MySQL — ROOT NEURON

## Identity
- ID: databases.mysql
- Type: technology-root
- Status: active
- Importance: high
- Last Verified: 2026-08

## Purpose
MySQL-specific knowledge: when it's the better fit than PostgreSQL, engine/backup/tuning details, version reality.

## Version snapshot (2026-08)
- **8.0** widely deployed (extended support end ~Apr 2026 for LTS)
- **8.4 LTS** — current LTS (support through 2032)
- **9.x innovation releases** (9.0+; also 9.3 etc.) — short-support innovation track, X LTS per 2 years
- Aurora/MySQL managed offerings share the core

## Activation
- "mysql", "mariadb", existing MySQL infra
- InnoDB specifics: MVCC, `innodb_*` settings, buffer pool, redo

## Do Not Activate
- PostgreSQL-specific (their neurons)
- unless migrating ask which base maintained

## Decision Rules (guidance-level, not mandate)
- MySQL strong when: **team expertise, managed service ecosystem (RDS), page-compression, InnoDB layout for OLTP**; community/enterprise support
- Real high-write OLTP: MySQL + InnoDB + JSONB not; but PG still real all-round
- Partitioning (RANGE/LIST), read replicas (async), full-text (has myisam/innodb FTS; weaker than PG FTS), no partial indexes (mostly), no native GIN/GiST equivalents
- JSON column (MySQL 5.7+) has JSON functions but fewer indexing/expr options vs PG

## Hard MySQL specifics (VERIFIED)
- Default isolation: **REPEATABLE READ** (differs from PG's READ COMMITTED default!)
- `innodb_buffer_pool_size` core knob (70-80% RAM typical for DB-dedicated)
- DDL locking behaviors (older DDL blocked; 8.0+ online DDL improved — verify per version!)
- **Replication**: async (default) → gtid; semi-sync; group replication/InnoDB Cluster: bitbook
- Backup: mysqldump logical; **Percona XtraBackup** physical (InnoDB crash-safe)
- `max_connections` ~ per core guidance; use proxy (ProxySQL)

## Common failure modes
- buffer_pool mis-sized → reads hit disk
- default REPEATABLE READ + long txn → undo growth
- DDL lock waits
- replica lag via long transactions / huge DDL
- lost async replication data (failover window) — document RPO!

## Security
- TLS, least-privilege, user roles, audit log
- password hashing (MySQL caching_sha2_password 8+)

## Performance / Observability
- performance_schema; slow query log; sys schema
- measure with EXPLAIN ANALYZE (8.0+) before tuning

## Related
- backup-restore: mysqldump/XtraBackup; PITR via binlog
- no partitioning.lang == (RANGE/LIST/HASH; NOT automatic time)
- multi-tenancy: RLS N/A (no RLS) — isolation via schema/DB per tenant mostly

## Evidence
- MySQL docs (VERIFIED), version matrix in brain/version-awareness.md