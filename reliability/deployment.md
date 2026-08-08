# Deploying Safely (Change & Rollout)

## Identity
- ID: reliability.deployment
- Type: procedure
- Status: active
- Importance: high

## Purpose
Ship code every day without breaking users: small releases, staged rollout, instant rollback. Deployment safety IS reliability.

## The contract for safe deploys
1. **Small release units** (minor migrations + isolated deploys)
2. **Feature flags** for risky behaviors (instant kill without redeploy) (features/experiments)
3. **Staged rollout**: 1% → 10% → 50% → 100%, with health gates between (metrics dashboard, no alert)
4. **Rollback in minutes**: previous artifacts retained, DB migrations designed reversible
5. **Health checks**: readiness (traffic only to ready pods) + liveness (restart awareness)
6. **Automated rollback trigger**: error-rate threshold → auto stop rollout

## Migrations within deploy
- schema migrations released BEFORE code that reads them (expand → migrate → contract)
- backfill in batches (not one predatory UPDATE)
- blue/green or ring-based releases allow safe code-db interleaving

## Code tiers

### ❌ Bad
```python
# big-bang replace on the node, manual, no flags, no health
# "if it breaks we fix it live"
```

### ✅ Good
```python
# CI builds artifact → start 1 node → wait for health (readiness) → switch traffic
# rollback = previous build redeploy (still manual)
```

### ⚡ Better
```python
# K8s: Deployment strategy RollingUpdate (maxUnavailable 1, maxSurge 25%)
# pod readinessProbe/livenessProbe set; canary 1% via traffic mirror/weight
# feature flag flips: kill|launch without code release
```

### 🏆 Excellent
```text
- automated rollout: 1%→100% with SLO gates (error/latency) auto-aborting on breach
- rollback drills run quarterly (this quarter we rollback VIEW that repo's release)
- migration + code matrix documented: N-1 code supported during expand/migrate/contract
- release train calendar: risk windows known ahead; chaos-gated weekends
- deploy dashboard: every change to prod = deploy id + owner + auto health record
```

## Failure modes
- long-lived migrations > 30s holding locks during peak
- no readiness → traffic hits half-booted service (health: pod ready != started)
- flag toggles without tests (never tested path of new feature off)
- one click = whole prod (no rings) when activity skips

## Security/audit
- approvals & secrets correct per env; no prod deploys from laptops; audit trail of who deployed what

## Evidence
- Deployment strategies (blue/green, canary): SUPPORTED practice
