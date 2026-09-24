# Backup Drill — Monthly Restore Test

## Identity
- ID: reliability.backup-drill
- Domain: reliability
- Type: procedure
- Status: active
- Importance: critical
- Last Verified: 2026-08

## Purpose
Prove RPO/RTO, not just configure it: monthly restore drill that fails the build if restore breaks.

## Core Concept
Backup without restore test is a hope. Drill restores to ephemeral PG, replays WAL to PITR point, runs app smoke.

## Activation Conditions
- Any stateful service with RPO/RTO; S-033 relevant; complements reliability/backups-recovery.md

## Decision Rules
- Schedule: monthly auto-drill (cron), quarterly manual game-day.
- Steps: `pg_basebackup` + WAL archive (S-046) → restore to temp → `recovery_target_time` PITR → `SELECT pg_is_in_recovery()` false → run `pytest -k smoke` + `pg_checksums`.
- RPO check: `now - last WAL` < RPO (e.g., 15m); RTO check: restore time < RTO (e.g., 1h); alert if exceeded.
- Store backup off-site (different region), encrypted (KMS), test cross-region restore once per quarter.

## Security
- Backup encrypted at rest (KMS), IAM least privilege, no backup in public bucket; S-059 for key.

## Performance
- Base backup throttled (`--max-rate`); WAL archive `archive_timeout 60s` tuned to RPO.

## Reliability
- SLO: restore success 100% over 3 drills; failed drill = incident, not backlog.

## Evidence
- PG PITR VERIFIED via S-046, SRE error budgets via S-033 (accessed 2026-08).

## Code Tiers
<!-- data-only -->
```bash
# drill (data-only, adapt paths)
pg_basebackup -D /tmp/restore -X stream -R
# recovery.conf: restore_command = 'cp /wal/%f %p'
# recovery_target_time = '2026-08-12 10:00:00+00'
pg_ctl -D /tmp/restore start && psql -c "SELECT 1" && pytest -k smoke
```
