# Django Settings & Deployment Hygiene

## Identity
- ID: django.settings
- Type: procedure
- Status: active
- Importance: high

## Purpose
Settings that are reproducible (env-driven), deployable (no DEBUG surprises), fast (cache/DB config), and auditable — the file that "runs anywhere" by accident is a trap.

## The settings contract
1. **Single base + env overrides**, not 15 diverging module copies: `settings.base.py` + `env.py` (reads env vars once, typed)
2. **12-factor**: everything configurable via environment (DB, cache, broker, keys, URLs) — but with sharp defaults for dev, fail-fast in prod (missing env = boot error)
3. **SECRET_KEY**: env-only, NEVER in code/repo; rotate on demand; independent per env
4. **DEBUG=False in prod, forever**: verify by boot test (assert not DEBUG in prod configuration)
5. **ALLOWED_HOSTS / CSRF_TRUSTED_ORIGINS / CORS_ORIGIN**: explicitly per env; no wildcard in prod (security/owasp-top10.md A05)
6. **Timezone/`USE_TZ=True`, `LANGUAGE_CODE`, static/media**: aware discussions; UTC storage, local display
7. **DATABASES**: environ host/port; pool discipline (databases/optimization); `CONN_MAX_AGE` tuned (5-60s) — with pgbouncer caution
8. **CACHES**: Redis via env; cache keys prefixed per env (no cross-env collisions)

## Server & deployment
- wsgi: gunicorn/uWSGI workers (2-4×cores) OR async ASGI+uvicorn for async views; container multi-stage
- Static/media: X-Forwarded handling, nginx/caddy or CDN; media = object storage (storage neurons)
- Health: `/health/` endpoint (DB, redis, worker) for LB/portal (reliability/deployment.md)
- Logging: settings LOGGING dict to JSON (observability/logging-recipes), request middleware with trace ids

## Code tiers
### ❌ Bad
```python
# settings.py with hardcoded DB creds, DEBUG hardcoded True hidden in dev only,
# ALLOWED_HOSTS = ["*"], SECRET_KEY in file, no env
```
### ✅ Good
```python
import os
SECRET_KEY = os.environ["SECRET_KEY"]          # fail fast
DEBUG = os.environ.get("DJANGO_DEBUG") == "1"
if not DEBUG and os.environ.get("ENV") == "prod":
    ALLOWED_HOSTS = [os.environ["HOSTNAME"]]
CSRF_TRUSTED_ORIGINS = [f"https://{H}"]
```
### ⚡ Better
```python
# pydantic-settings: typed Settings class, .env for dev, validation at import,
# per-env security assert() in prod config (allowed_hosts, debug ok, csrf)
# secret not required at import → start fail early, no silent defaults
```
### 🏆 Excellent
```
# per-env configs committed (base + env files w/ secrets in vault), env exports
# CI checks config load for each env (mock vault), settings linter 
# deploy: secrets injected, DEBUG enforced false, verification smoke (health path)
# config drift monitoring: hash of settings exported vs deployed hash
```

## Failure modes
- environments drift (dev/prod divergence → prod-only bugs)
- SECRET_KEY committed (repo scoped forever)
- ALLOWED_HOSTS mismatch with mesh/reverse proxy (400s)
- arbitrary env injection without enum (forgotten keys)
- prod booting with DEBUG (leaks everything)

## Evidence
- 12-factor (VERIFIED), Django deployment docs (VERIFIED)