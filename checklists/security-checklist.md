# SECURITY CHECKLIST (pre-release)

Gate before anything is exposed. Apply to ANY change touching auth/data/external call.

## AuthN/AuthZ
- [ ] Password hashing Argon2id/bcrypt; no plaintext/fast hashes
- [ ] Session/token: HttpOnly + Secure + SameSite(w); expiry; server-side revoke
- [ ] MFA on admin/risky actions; login rate-limited (brute force)
- [ ] Object-level authZ finished: EVERY handler verifies ownership/tenant
- [ ] API: 401 vs 403 vs 404-blend consistent (no enumeration)
- [ ] Admin surface restricted (admin.md); no default creds

## Input/Output
- [ ] Validation at every boundary (schema/form); no raw SQL concatenation
- [ ] Output escaping all reflected content; XSS/CSRF middleware on
- [ ] Uploads: size/type whitelist; no path traversal; never execute
- [ ] Deserialization: safe loaders; no untrusted eval/pickle

## Data
- [ ] PII inventory + retention set; logs redacted (no creds/PII)
- [ ] Encryption at rest in place for classified data (KMS > keys); TLS enforced (HSTS)
- [ ] Secrets: none in code/repo/env; rotated on suspicion; gitleaks in CI

## App
- [ ] Debug off; version headers restricted; errors don't leak internals
- [ ] Dependency audit (pip-audit) clean; lockfiles committed
- [ ] Headers: CSP, X-Frame-Options (or config), referrer-policy
- [ ] SSRF: any outbound URL → allowlist + no redirect-follow unchecked

## Ops
- [ ] Cloud: buckets private (ACL/policy least privilege), no public keys
- [ ] Saas keys/API key per service least privilege; rotation script exists
- [ ] Log/observability: audit trail (who, what, when) enabled
- [ ] Incident runbook reachable (access-breach / secret-leak)

## After release (first weak window)
- [ ] Review IDOR suite on all new endpoints; re-run scans
- [ ] False paths confirmed disabled; deprecations public-metadata