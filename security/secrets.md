# Secrets Management

## Identity
- ID: security.secrets
- Type: procedure
- Status: active
- Importance: critical

## Purpose
Keep keys, tokens, passwords, certificates **out of code, out of repos, out of logs** — with rotation that actually happens.

## Core rules (non-negotiable)
1. Never in source, README, `.env` committed, Docker image layers, CI logs
2. Use env injection via secret manager (config time), not bake at build
3. Rotate on demand (p1 rotation: when leaked = incident pipeline)
4. Least privilege: dedicated tokens per service/environment, scoped

## Tooling tiers (choose by infra)
- Local dev: `.env` (gitignored) + `python-dotenv`; don't ship `.env.example` with real values
- Prod (managed): AWS Secrets Manager / GCP Secret Manager / Azure Key Vault / Vault / Doppler
- Git: `.gitignore` + **secret scan in CI** (gitleaks / trufflehog) — even for past history (BFG history rewrite)
- Kubernetes: Secrets + external secrets operator (sync from vault-manager)
- Rotation: scheduled lambda/cron rotate; support from services (DB password via secret manager, auto-rotation in AWS RDS)

## Code tiers

### ❌ Bad
```python
DB_PASSWORD = "Sup3rS3cret!"    # in settings.py committed to repo
```

### ✅ Good
```python
# settings.py
DB_PASSWORD = os.environ["DB_PASSWORD"]        # fail fast if missing
# .env gitignored; CI injects the right value
```

### ⚡ Better
```python
from vault import Client; secrets = vault.get("/prod/billing")   # managed, audited
# app reads at boot with cache + health check on secret availability
```

### 🏆 Excellent
```text
- enum in config as env identifiers, no values anywhere
- secret versioning: rollback support; rotation script cycled (DB creds rotate in prod)
- gitleaks in CI; secret scanning of git history; leak response runbook in 15 min
- per-service IAM role (no cross-account secrets sharing)
- secrets never in logs (filter middleware), never in error pages
- revoke+rotate drill recorded in ops runbooks
```

## Failure modes
- committed .env (one bad push = breach)
- secrets in build arguments (docker history leaks! use build-arg-free)
- same key across prod/staging (blast radius)
- unrotatable secrets (service account keys w/ no rotation path — deprecate)

## Evidence
- OWASP Secrets Management challenges, CNCF docs, gitleaks/trufflehog docs (VERIFIED)