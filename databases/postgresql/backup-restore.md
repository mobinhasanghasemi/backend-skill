# Backup, Restore & Point-in-Time Recovery

## Identity
- ID: databases.postgresql.backup-restore
- Domain: databases / reliability
- Type: ops-neuron
- Status: active
- Importance: critical

## Purpose
Guarantee recoverability as a **measured capability** (RPO/RTO), not an assumption. Backup that was never restored equals "no backup" — the skill's #1 reliability claim.

## Core Concept
- **Base backup** (pg_basebackup / cloud snapshot) = cluster state at time T
- **WAL archiving** = every change since; combined → **Point-In-Time Recovery (PITR)**: restore base + replay WAL to any moment
- Wal-g / pgBackRest / Barman for archive management; managed cloud (RDS PITR) built-in
- RPO (max lost) and RTO (max down) defined per data class BEFORE tools are chosen

## Tiers

### ❌ Untested "backup"
```bash
# daily dump via cron; never tested restore; no WAL archiving
pg_dump > daily.sql   # restore = last 24h loss, op "worked" never verified
```

### ✅ Working basebackup + WAL
```
wal_level = replica (replica/replica? wal_level 'replica' for 15/16/17; prob 18)
archive_mode = on, archive_command = 'wal-g wal-push %p'
pg_basebackup -D /backup/base/$(date +%F) -P -X stream
```

### ⚡ Better — automated, monitored
```
pgBackRest config: stanza, retention; daily full/incr + WAL push continuous
5/minute: pg_basebackup into staging, apply WAL, SELECT check → alert if fails
RPO check: how far WAL lags backup completion; surfaced in dashboards
```

### 🏆 Excellent — recovery-ready regime
```text
1) RPO/RTO documented per workload (e.g., financial: RPO ≤5m)
2) Continuous WAL archiving (pgBackRest / Barman), verified restore
   drill monthly (auto in staging: restored DB answers the app's read queries)
3) Restore time measured & budgeted (x GB restore = X min)
4) Tested PITR to arbitrary time (played "recover to yesterday 13:37")
5) DR object: backups off-node (object store / other region), encrypted
6) 3-2-1: three copies, two media, one offsite
7) Data verification query after every drill (row counts, checksums)
```

## Decision rules
1. pg_dump for small systems / logical per-table exports — but for prod durability: basebackup + WAL
2. RPO drives WAL qty (sync level…); RTO drives restore path (stay in same cloud/region, warm standby)
3. Encrypt backups (WAL too); keys separate
4. Retain per compliance (PCI/SOC: 12 mo+, etc.)
5. Logical backup (dump) ALSO — for zero-version-migration path

## Failure modes
- WAL archive gap (slot monitored false → archive missing → can't PITR) — validate with periodic `pg_waldump`/check
- backup storage single-region (DR test = region down)
- never-restored backup (feature "we never test restores")
- PITR timestamp runaway (WAL replay slow on big stage)

## Observability
- last successful base / archive age, WAL bytes archived/h, restore drill results, retention quotas

## Evidence
- PostgreSQL docs (backup strategies, PITR) — VERIFIED; 3-2-1 practice (SUPPORTED).