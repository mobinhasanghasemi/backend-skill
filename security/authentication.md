# Authentication & Session Management

## Identity
- ID: security.authentication
- Type: discipline
- Status: active
- Importance: critical

## Purpose
Who is this? Prove identity reliably, manage sessions securely, rotate and revoke cleanly — without building your own crypto.

## Trust anchors (2026)
- **Password**: never store plaintext / fast digests → argon2id/bcrypt (OWASP password storage rules), see passwords-and-tokens
- **2FA/MFA**: TOTP (RFC 6238) or WebAuthn (FIDO2) for anything valuable
- **External IDP**: OIDC (authorization code + PKCE), SAML legacy; SSO = delegating trust well
- **Internal**: token-based sessions (free-form server-side) vs JWT stateless — decide by short-lived + revocation needs

## Code tiers

### ❌ Bad
```python
password = request.form["password"]
user = User.query.filter_by(email=...).first()
if user.password == password:      # plaintext compare!!! 
    login(user)
```

### ✅ Good
```python
from werkzeug.security import check_password_hash   # scrypt/argon2 under the hood
if not user or not check_password_hash(user.password_hash, password):
    raise LoginFailed                     # same error for both → no user enumeration
session.permanent = True; session["uid"] = user.id   # signed server-side session
```

### ⚡ Better — hardened flows
```python
# login throttling: per-IP+user slow down (rate limiting on auth endpoint)
# MFA required for admin/risk actions (TOTP/WebAuthn verified)
# session: httponly, samesite=Lax, secure; separate idle + absolute expiry
# refresh cycles when privilege changes; logout revokes server-side session id
```

### 🏆 Excellent
```text
- policy: argon2id tuned (m=19456KiB, t=2, p=1), TOTP/WebAuthn MFA advisory-required by role
- OIDC + PKCE flow with state/nonce verification (no open redirects!), audience check
- JWT path: short-lived (≤15m) + refresh rotation (refresh token reuse detection) 
- sessions: server-side store (Redis) for revoke-ability; timeout jitter; device fingerprints
- account enumeration resistant: uniform responses (401 vs 404 blended for common users)
- anomaly monitoring: impossible travel, new-device alerts, failed-login bursts
- audit: auth events (login, fail, logout, reset) all logged with user/resource/ip — SIEM reachable
```

## Failure modes (step back)
- compare with `==` (range timing) — always constant-time compare
- JWT in localStorage™ → XSS exfiltration; prefer HttpOnly cookies with CSRF guard
- no input validation on identifier field (SQLi vector in login!)
- password reset emails exposing enumeration ("no account with that email")
- session fixation on shared devices — regenerate on login

## Security guardrails
- no plaintext compares everywhere; use secrets.compare_digest / Werkzeug API
- nonce+state in OAuth always; redirect allowlist (open redirect = doc)
- tokens over headers, not URL query strings

## Evidence
- AuthN: VERIFIED via S-022 (password storage), S-027 (JWT); session practice SUPPORTED
