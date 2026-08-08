# Python Packaging & Dependencies

## Identity
- ID: python.packaging
- Type: procedure
- Status: active
- Importance: medium

## Purpose
Deterministic, reproducible, auditable Python projects: dependencies locked, build=config-as-code, CI-sane.

## The 2026 defaults
- `pyproject.toml` (single source) + lockfiles
- **pip** for minimal; **uv** (fast) or poetry/pipenv for lockfiles; pypi mirror regions
- **Lock everything**: exact versions + transitive hashes (uv.lock), reproducible container builds
- **Reproducibility**: same lock in dev/CI/prod (no `pip install -r requirements.txt` without lock)
- Environment: `virtualenv`/`.venv` in repo, devcontainer/poetry core
- Maturity: don't juggle 3 tools; pick 1 (uv, right-sized)

## Security: supply chain
- dependency audit on every lock change: `pip-audit` (OSV), `uv pip audit`
- mut approval for major versions (policy), pinned actions-by-hash in CI
- alert on CVEs in CI; dependency review PRs (GitHub)
- never `pip install` from code; binaries from trusted sources

## Code tiers
### ❌ Bad
```python
# requirements.txt with loose pins ("django>=4.2"), no lockfile,
# "python -m pip install -r requirements.txt" works ≠ reproducible
```
### ✅ Good
```python
# pyproject.toml: requires-python = ">=3.12"; dependencies = ["django==6.0.8", ...]
# uv lock → uv.lock committed: exact, hash-pinned, single source
```
### ⚡ Better
```python
# uv sync (lock) in CI + prod Docker multi-stage (dev deps in build stage only)
# dev extras: [dependency-groups]: dev (pytest, ruff, mypy)
# security: uv lock hashes verifiable offline
```
### 🏆 Excellent
```text
# build stages: base → build deps (compilers) → app (no build tools)
# audit quorum: pip-audit in CI, alert on critical; weekly @ upgrade dry-run
# license checks (discarding non-permissive), SBOM export for compliance
# reproducibility test: clean container + lock → identical wheel set
```

## Failure modes
- unpinned/unlocked dependencies (works today, breaks tomorrow at upgrade)
- security or license surprises (dependency drift)
- mixing system-wide python with project venv (contamination)
- prod image containing build+debug deps (larger, risky)

## Evidence
- pip/uv/pyproject docs (VERIFIED)