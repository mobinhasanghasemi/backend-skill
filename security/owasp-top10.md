# OWASP Top 10 → Backend Reality

## Identity
- ID: security.owasp-top10
- Type: concept-reference
- Status: active
- Importance: critical
- Source: OWASP Top 10 2021 (latest public major; check 2026 releases), CWE Top 25

## Purpose
The danger list mapped to the **backend**, not web pages: where each class actually bites in Django/FastAPI/microservices, and the fix in one line each.

## The list, backend-style

| # | Class | Backend reality | Defence |
|---|---|---|---|
| A01 | Broken Access Control | IDOR (#1!), missing ownership checks in every handler, cache leaks | authZ per object; scoped queries; tests per endpoint (authorization.md) |
| A02 | Cryptographic Failures | weak hashing, TLS gaps, tokens in logs | passwords-and-tokens.md, cryptography.md |
| A03 | Injection | SQLi via raw queries in Django (rare but real), NoSQL injection, template SSTI in | ORM/SQL parameters (always), never string-fmt SQL |
| A04 | Insecure Design | security misdesign: reset flows, OAuth bugs, business logic bypass | threat-modeling.md, logic tests, e2e adversarial suite |
| A05 | Security Misconfiguration | debug=True, default creds, permissive CORS, exposed schemas, dev builds | hardening checklist + security review per release |
| A06 | Vulnerable Components | outdated deps in pyproject (log4shell-family lessons) | dependency audit in CI: pip-audit/OSV, pin lockfiles |
| A07 | AuthN Failures | brute force, session theft, credential stuffing | rate limiting (auth first!), MFA, session hardening (authentication.md) |
| A08 | Integrity Failures | unsigned webhooks/deserialization (pickle!), unverified updates | HMAC (webhooks.md), safe serializers (never pickle untrusted) |
| A09 | Logging Failures | no audit trail, unmonitored suspicious behavior | logging-and-privacy.md, alerting |
| A10 | SSRF | server fetching user-provided URLs (proxies) | allowlist hosts, no redirect follow w/o checks, URL parse validation, timeouts |

## Extended backend list (beyond top 10)
- **XML/deserialization** (yaml.load full) — safe loaders
- **DoS via costly endpoints** (aggregations, heavy reports) — rate, complexity caps
- **Supply chain** in CI (docker images, actions) — pin everything, dependabot
- **PII over-exposure** — API returns full models; DTOs only (MIN* fields)
- **Race conditions in financial flows** (double-spend) — conflict/rich-lock

## Code tiers — one real CRUD repair

### ❌ Bad
```python
def update_profile(request, user_id):
    # no access check: any logged-in user can write ANY user
    u = User.objects.get(id=user_id)
    ...

### ✅ Good
    u = User.objects.get(id=user_id)
    if u != request.user and not request.user.is_staff: raise PermissionDenied()
```

### ⚡ Better — scoped + test
```python
u = User.objects.get(id=user_id, tenant=request.tenant)  # defense at query
# + endpoint test: user B updating A → 403/404
```

### 🏆 Excellent
```text
- IDOR regression suite in CI (every object endpoint tested cross-tenant)
- policy module single-point (authorization.md Excellent tier)
- security headers middleware; CORS allowlist; cookies Secure/SameSite
- dependency scanning CI gate; SBOM per release if compliance
```

## Security notes
- When in doubt: deny by default; log denied attempts; review config diffs

## Evidence
- OWASP Top 10 classes: VERIFIED via source-S-019 (owasp.org, accessed 2026-08)
