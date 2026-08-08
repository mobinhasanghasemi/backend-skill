# Containers & Docker (production shape)

## Identity
- ID: infrastructure.containers
- Type: procedure
- Status: active
- Importance: high

## Purpose
Package services so they run identically everywhere — with small, lean, secure images and a runtime contract (health, signals, resources).

## The Dockerfile contract
1. **Multi-stage build** (deps → build → runtime); runtime image = slim (no compilers, no debuggers)
2. **Layer discipline**: COPY requirements first → pip install → COPY code (cache!) 
3. **Non-root user** in container; read-only rootfs where possible (security/hardening)
4. **Entrypoint = your app**: signal handling (SIGTERM → graceful drain, stop streaming) — Python: uvicorn/gunicorn handles; never PID 1 issues w/o init
5. **Resources**: resource request/limit declared (memory limit kills with nice OOM, no thrash), HEALTHCHECK (readiness per app)
6. **Provenance**: pin base image tag (digest); scan for CVEs in CIB (trivy/grype)

## .dockerignore: don't copy the world (tests, .git, envs, caches)

## Code tiers
### ❌ Bad
```dockerfile
FROM python:latest        # untagged base: builds change (floating)
COPY . /app               # whole repo incl. secrets/.git
RUN pip install -r requirements.txt   # unpinned?? + uv lock ignored
CMD python manage.py runserver --insecure   # dev server (no true shutdown); root user
```
### ✅ Good
```dockerfile
FROM python:3.12-slim-bookworm AS base
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen                     # locked, hash-pinned
COPY . .
# (no runserver! production via gunicorn/uvicorn)
CMD ["gunicorn", "app.wsgi:application", "--workers", "4", "--bind", "0.0.0.0:8000"]
```
### ⚡ Better
```dockerfile
FROM base AS build ...; FROM base AS runtime     # multi-stage
COPY --from=build /app/.venv /app/.venv
USER appuser
HEALTHCHECK CMD curl -f http://localhost:8000/healthz || exit 1
# resource limits: maximum declared; image ~ sessions, deps (trivy in CI)
```
### 🏆 Excellent
```text
# image: signed, SBOM generated, registry pull-once; version = git sha
# running: read-only fs except /tmp, --cap-drop all --no-new-privileges, 
# resource limits + namespaces, spy healthcheck, graceful SIGTERM test in CI
# multi-arch build (amd64/arm64) same digest
```

## Failure modes
- huge images (multi-GB) → slow deploys, cluster waste
- base tag drift (latest breakage)
- run as root; secrets baked in layer history (docker history!)
- container no health → LB sends traffic to dead
- logging to stdout fine; but never log secrets (logger)

## Evidence
- Docker best practices (VERIFIED), CNCF container standards