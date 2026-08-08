# CI/CD & Delivery Pipelines

# Identity
- id: devops.ci-cd
- Domain: devops
- Type: procedure
- Status: active
- Importance: high

## Purpose
Turn "commit → prod" into a fast, verified, repeatable pipeline that gates quality and can always roll back. CI is code: versioned, reviewed, deterministic.

## Pipeline anatomy
```
commit → [lint | type | test | build | security scans] → artifact (SHA) → 
        → [staging deploy + smoke + load] → prod gates → progressive rollout (1%…100%) → 
        → observability verify → done (or rollback)
```

### Fail-fast (first 3 min)
- uv sync frozen; ruff; mypy strict; pytest quick suite
- dependency audit (pip-audit) + secret scan (gitleaks) + SBOM

### Slow-but-true (staging)
- full suite (integration + contract), migration dry-run, e2e smoke, load slice
- release candidate = artifact id + config id + migration id locked

## The gates that matter
1. **green required** — any red = blocked (unless consciously waived w/ ticket)
2. **deploy permission**: prod deploy by merge to main (branch protection) or explicit approve — policy written
3. **verify after deploy**: synthetic (health + happy path) + real-time SLO monitor window (10-15 min)
4. **rollback = redeploy previous artifact** (feature flags second lever)

## Failure modes
- CI too long → bypass (5 min min) — measure CI runtime
- prod-from-laptop (no pipeline) — audit trail empty
- deploy pipeline drives migrations ahead (zero-downtime discipline: django/migrations.md)
- config drift (env between CI vs prod)
- secrets in CI logs (gate)

## Sample workflow (GitHub/GitLab CI)
```yaml
test: ...
  run: uv sync --frozen && uv run pytest -m "not e2e" -q
deploy-staging (on PR): ...
  run: docker buildx --build-arg GIT_SHA=${{ sha }} ...
deploy-prod (on main): 
  steps: approve → helm upgrade --atomic → verify /healthz
```
automated rollback: error rate threshold → `helm rollback --restart` (deployment.md)

## Evidence
- DORA elite practices (VERIFIED research corpus), GH Actions docs