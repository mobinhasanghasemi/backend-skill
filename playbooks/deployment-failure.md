# Playbook: Deployment Gone Bad

> Fallback-first. If you can roll back the commit that changed the app/migration, DO THAT — speed beats heroics.

## Decision ladder (within 5 min)
1. What changed? (latest deploys, config, migration, secrets) — `git diff` last bad
2. **Rollback** the code: redeploy previous artifact (deploy pipeline: `--from-version`/helm revert). DB migrations: **do NOT revert blindly** — schema revert has its own risk (migrations.md runbook)
3. **Shed load** if symptom is capacity (regions, flags: disable the new feature)
4. Feature flags first: if the break is inside a flagged feature, kill the flag (no code change)

## The 3-phase discipline
- **Execute**: rollback code; re-prime caches; watch 15 min on metrics (error rate, p99, nightly)
- **Verify**: the failure signature is gone (same alert as trigger, not a different yellow)
- **Learn**: root-cause in the day(s) after; change the gate that allowed it (CI regression test, loadable deploy step, chaos)

## Common causes & their gates
| Cause | Gate that should have caught |
|---|---|
| Bedrock schema mismatch (migration/code ordering) | migrations.md order: code N vs M; memory CI test |
| Environment diff (prod vs staging config) | settings.md per-env tests in CI |
| Load regression at p99 | load test on each deploy/PR (load-performance.md) |
| Migrations locking prod | expand/migrate/contract (safe migrations) |
| Degraded dependency | integration test + circuit breaker behavior test |

## Rollback protocol (incident-response.md)
- Compose as artifacts: code-affix, config-affix, migration-affix — re-deploy produce set
- Never crash-with-investigation: hold — tell — sync to incident channel

## Post-rollback
- Move forward: fix + rerun (green → auto-advance); don't dwell in rollback state (hardened path, ticket)