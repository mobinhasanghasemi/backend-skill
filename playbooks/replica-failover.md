# Playbook: Replica Failure / Failover Gap

## Symptoms
- replica lag massive, replica down, primary failover test fails

## Primary-first medicine
1. Is the **primary** healthy/current? (pg_stat: age of WAL, sync status; xmin)
2. **Lag**: if replicas lag: find blocker (long tx on primary, WAL archiving stall, replication slot missing) — `pg_walsummary`/slot status
3. **Failover test failure**: the path was stale (blocked networks/scripts); document & retry

## Paths to fix
| Case | Action |
|---|---|
| Replica lag accelerates | primary loading (replica read routing of big query) → terminate runaway (EXPLAIN first!) |
| Slot falling behind | WAL growth warning → archive/sequence fix + housekeeping (replication.md) |
| Standby cannot connect (auth) | replication role + `replication` user/SSB — credentials hygiene (secrets) |
| Swift multi-primary | not: go single-primary (fencing); the split - prevention: applications write one endpoint only |

## Failover decision
- **Manual failover**: when primary irrecoverable in window: promote standby (minutes, surgical, RPO/TO)
- **Auto**: only if health signals are robust (automation can lie); else manual-floor
- During failover: **write-enable only after replication resumed**, advertise new primary on the DNS/proxy configs — detect two primaries (heartbeat fences) and act

## Post
- Upgrade standbys cleared, RPO/RTO table, drills recorded (backup/chaos lesson)
- Monitoring: lag + health per node; page on both directions

## Evidence
PG replication/dr drift guides (VERIFIED in equivalents: see postgresql/replication.md)