# SECURITY — ROOT NEURON

## Identity
- ID: security.root
- Domain: security
- Type: root
- Status: active
- Importance: critical

## Purpose
Security as a design property, everywhere: authN, authZ, data protection, threat-driven reactivity, and compliance-aware logging. The SECURITY_GUARDIAN engine is the enforcement half; this domain holds the knowledge half.

## Activation
- any authN/authZ implementation or review
- where user input crosses a trust boundary (API, files, HTML, SQL, shell)
- secrets, encryption keys, tokens
- threat scenarios, incident understanding
- compliance/data-class work (GDPR, PCI-relevant flows)

## Do Not Activate When
- performance/feature questions (unless abuse vectors)

## Routing
```text
login/signup/sessions     → authentication.md
who-may-do-what           → authorization.md
password/auth storage     → passwords-and-tokens.md
web app attack surface    → owasp-top10.md (SQLi, XSS, CSRF, SSRF, IDOR...)
secrets in code/infra     → secrets.md
encryption needs          → cryptography.md
session/audit logs        → logging-and-privacy.md
early design              → threat-modeling.md
compliance (GDPR/SOC2… )  → compliance.md
```

## Mandatory posture (not slogans — checklists)
1. **AuthZ is per-object, in every handler** — IDOR is the #1 realistic bug (ARCH014)
2. **Defense in depth** on trust boundaries — validate input, escape output, least privilege
3. **Fail secure** — defaults deny; errors never leak internals
4. **Secrets never in code/repos/env logs** — rotating keys, vaulting
5. **Data class awareness** — PII/sensitive fields require policy (encrypt at rest, mask in logs)
6. **Assume breach when designing** — logging, anomaly, blast-radius discipline
7. Same supply chain hygiene — pinned lockfiles + dependency audit in CI

## Common failure modes (top backend security killers)
- IDOR / broken access control (most exploited class — ARCH014)
- secrets leaked in repos → take shape seriously
- unrestricted input to DB/SQL/ORM → injection
- insecure defaults (debug, permissive CORS, wsgi dev servers)
- tokens stored insecurely / in logs
- unscoped rate limits around auth
- S3/bucket permission misconfig (public writes)

## Validation / testing hooks
- static analysis (security scanners), dependency audit (pip-audit/OSV), SAST in CI
- DAST on staging; pentest contracts; fuzz parsers (fuzzing tools)
- authz tests per endpoint (IDOR suite) — testing domain
- threat model updates for each new module — done without blocking an entire codebase

## Evidence
- OWASP ASVS / API Top 10 (VERIFIED via S-020, S-021); CWE Top 25 (SUPPORTED, general industry lists)
- TLS 1.3 (VERIFIED via RFC 8446, source-S-025)