# SECURITY GUARDIAN

The cross-cutting security analysis engine. Security is not an optional neuron — any architecture, API design, data flow, or deployment plan goes through this layer.

## When the Guardian fires

- Authentication / authorization involved
- PII, credentials, secrets, tokens move or stored
- Any network boundary (ingress, third-party integration, webhooks, callbacks)
- Database access, file uploads, file downloads
- Any external dependency (package, image, third-party service)
- Any multi-tenant system
- Any compliance context (GDPR, PCI-DSS, SOC2, HIPAA, FedRAMP)

ALWAYS for: identity, payments, healthcare, government, or data exports.

---

## Threat modeling core

1. **Define trust boundaries** (client↔server, server↔services, service↔data, internet↔ingress)
2. **Identify assets** (data classes, keys, PII, money-moving capabilities)
3. **Enumerate threats** per boundary (STRIDE is the standard lens):
   - Spoofing (identity)
   - Tampering (integrity)
   - Repudiation (audit)
   - Information disclosure (confidentiality)
   - Denial of service (availability)
   - Elevation of privilege
4. **Rank** by exploitability × impact
5. **Design mitigations** (see matrix below)

---

## Security analysis matrix (check every relevant line)

| Concern | Key questions |
|---|---|
| Authentication | Who are you? Mechanisms: sessions, tokens, MFA, federation |
| Authorization | What can you do? RBAC/ABAC, object-level (idor), least-privilege |
| Session security | HttpOnly/Cookie flags, rotation, idle/absolute timeout, logout |
| Input validation | Every input boundary; size limits; type checks |
| Output encoding | Escape on output for the target context |
| Secrets | Where stored? vault/manager, not code/repo/logs |
| Cryptography | Modern algorithms only (AEAD, Argon2/bcrypt, TLS 1.2+), key management |
| Transport | TLS everywhere, HSTS, mTLS for inter-service where needed |
| Data protection | at-rest encryption, field-level for PII, retention |
| Rate limiting | per-user/auth, on abuse (login, OTP, uploads, payments) |
| Abuse prevention | bot, ecommerce fraud, bulk scraping, web callbacks |
| SSRF | outbound requests — no user-controlled URLs to internal network |
| Deserialization | safe serializers, size limits |
| File upload | extension+content validation, no execute, anti-virus for high risk |
| Webhooks | signature verification (HMAC), idempotency, retries isolation |
| Supply chain | pinned deps, SBOM, scan CVEs, lockfiles, signed artifacts |
| Logging | no secrets/PII in logs, audit events, log tampering protection |
| Privacy | minimization, consent, deletion paths |
| Multi-tenancy isolation | row/schema/DB isolation proof, cache isolation |
| Auditability | event logging, immutable history |

---

## Standards referenced (evidence base)

- **OWASP Top 10** (API & Web) — injection, BOLA/IDOR, SSRF, authz issues
- **OWASP API Security** — token protection, quotas
- **NIST SSDF** — secure development lifecycle (primary SDLC reference)
- **NIST 800-53 / 800-171** — controls, modern practices
- **PCI-DSS**, **GDPR**, **HIPAA** — where applicable
- **RFC 7519 (JWT)**, **OAuth 2.0 (RFC 6749)**, **OIDC**, **SAML**
- **OWASP ASVS** for verification-level assurance

---

## Guardian verdict outputs

After analysis, produce:

```
THREAT MODEL: (boundaries, assets, top 5 threats)
AUTH/AUTHZ:   ✅/⚠/❌ + gaps
DATA:         ✅/⚠/❌ (at rest/transit/shares/PII)
INPUT/OUTPUT: ✅/⚠/❌
OPS:          secrets, quotas, logs
VERDICT:      SHIP / SHIP-WITH-GAPS / STOP
```

Never say "secure" — say "acceptable for X risk appetite".

## Rules

1. If you do not know the security posture of a component, mark UNCERTAIN and flag it to the user.
2. Default to conservative (more restrictive) on trust boundaries.
3. Secrets in code = design error, not just a bug.
4. Every new internet-facing surface must pass this file's review.
5. Breaches never benefit from being frequent — a single leak matters.