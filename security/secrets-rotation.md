# Secrets Rotation — Vault, Scanning, and CI Gates

## Identity
- ID: security.secrets-rotation
- Domain: security
- Type: procedure
- Status: active
- Importance: critical
- Last Verified: 2026-08

## Purpose
Never have a long-lived secret in code/env/logs; rotate automatically and catch leaks in CI.

## Core Concept
Secrets live in Vault/KMS, short TTL, injected as files, rotated without restart via reloader. CI fails on leak.

## Activation Conditions
- Any credential, API key, DB password, JWT signing key; S-035/S-059 relevant

## Decision Rules
- Store in Vault (S-059) with dynamic DB creds (TTL 1h) or KV v2 with rotation 30d; inject via ESO + reloader, mount as file not env.
- Rotate JWT keys with `kid` header, 2 active keys overlap 24h; DB passwords via Vault dynamic, no static prod password.
- CI: `gitleaks` (S-035) + `semgrep` (S-036) + `pip-audit` on every PR; block on high; pre-commit hook `detect-secrets`.
- Logs: scrub `Authorization`, `password`, `secret` via allowlist logger filter (S-078).

## Security
- Least privilege per service Vault policy; audit log on read; break-glass procedure documented.

## Reliability
- Rotation: dual-key window, health check after reload, rollback to previous version in Vault.

## Evidence
- Vault VERIFIED via S-059, gitleaks via S-035, semgrep via S-036, logging via S-078 (accessed 2026-08).

## Code Tiers
<!-- data-only -->
```yaml
# ExternalSecrets (data-only, verify API version)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata: {name: db-creds}
spec:
  refreshInterval: 1h
  target: {name: db-password}
  dataFrom: [{extract: {key: prod/db/app}}]
```
