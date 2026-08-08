# Backups, Recovery & DR

## Identity
- ID: reliability.backups-dr
- Type: procedure
- Status: active
- Importance: critical

## Purpose
Turning "we should have a backup" into a **proven recovery capability**: RPO/RTO contractual, restores practiced, disasters planned.

## The fundamentals (3-2-1 plus)
- 3 copies / 2 media/types / 1 offsite (cloud region = ok)
- RPO: how much data we accept losing (minutes?) → drives backup frequency + replication sync
- RTO: how fast we restore service → drives restore path & warm standby
- **Untested backup = no backup** — restore test monthly/quarterly (risk-scaled per data class)
- Immutable backups (protect against ransomware & operator error); retention policy = storage budget

## Two families of DB backup (see postgresql/backup-restore for PG details)
- **Logical** (pg_dump) — small, portable, easier to move/transform
- **Physical** (basebackup + WAL) — PITR, faster bulk, required at scale
- Managed (RDS/CloudSQL): built-in snapshots + automated PITR; still test restores!

## Service & infra backup
- app code: git forever (yes that's a backup); config as code (IaC)
- file/object storage: versioned buckets + bucket replication; deletion rules
- secrets: vault-managed (can't backup by copying; use manager export)
- message queues: replayability by design (event log / outbox), not "back up the broker"

## Code tiers

### ❌ Bad
```python
# "we take a full pg_dump nightly at 3am" — nobody ever restored it
# → DR: "we push the button, wait and see"
```

### ✅ Good
```python
# nightly: pg_basebackup (full) + continuous WAL archive to S3
# RPO: PITR to min of loss; RTO: restore = new replica rebuild (30-60 min)
```

### ⚡ Better — automated restore test
```python
# CI/monthly cron: restore to a scratch instance, run CHECKPOINT + query assertions,
# report "last verified restore: <timestamp>" on the DR dashboard
```

### 🏆 Excellent
```text
- per-data-class: RPO/RTO documented + restoration path written (DR doc for the app)
- automated monthly restore drill with pass/fail gate; quarterly full DR (region failover)
- backups immutable (Vault/S3 Legal Hold), monitored: last-backup-age alert
- restore time budget = RTO (load test restore big data sets)
- chaos: ransomware drill (delete DB → restore from immutable); regional switch test
```

## Failure modes
- backup everywhere, restore never tested
- WAL archive not monitored (gap = RPO broken silently)
- "backup" = replicating the DB (read replica is NOT a backup — it shares failure modes)
- RPO=0 but replication only within region (region loss kills both)
- deleting backups too early (compliance lock boxes)

## Evidence
- 3-2-1 as standard practice (VERIFIED/SUPPORTED), PG docs on basebackup/PITR; AWS DR prescriptive guidance