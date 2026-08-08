# RELEASE CHECKLIST (production deploy)

## Pre-deploy
- [ ] CI green: lint, types, tests, contract, security scans (pip-audit, gitleaks)
- [ ] Migration plan: expand → backfill → contract verified; rollback path defined
- [ ] Feature flags: risky new behavior flag-gated & tested off
- [ ] Load/peak check: anticipated traffic within tested limits (load tests)
- [ ] Version/commit pinned; artifact built from locked deps
- [ ] Release note: changes, screenshots, runbook links, contact

## Deploy (staged)
- [ ] Green first 5% (smoke: health, happy path e2e)
- [ ] XOF: monitor error rate + p99 + SLO burn on primary dashboards
- [ ] Escalate: 10% → 50% → 100% with 15-min windows; HOLD on alerts
- [ ] DB migration applied before code when schema expands (order!)

## Post-deploy
- [ ] All critical alerts silent for 30 min (error, p99, queue lag, replicas)
- [ ] Backfill/queue tasks drained (no block)
- [ ] Cache prewarmed (if cold-start known); CDN purge done (if any)
- [ ] Verification: public path (login→action→logout) live manually
- [ ] Rollback artifact tagged; rollback owner named

## Quick rollback trigger
- [ ] Error rate x2 baseline OR p99 breach sustained 5m → ROLLBACK NOW