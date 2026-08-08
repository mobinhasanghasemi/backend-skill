# Security: Passwords & Token Storage

## Identity
- ID: security.passwords-and-tokens
- Type: discipline
- Status: active

## Purpose
Store secrets (user passwords, API tokens, session keys) so leaks do not become field days: hash with memory-hard functions, parameterized formats, rotation everywhere.

## Hashes — the only correct approach
- Password: **Argon2id** (memory-hard, params configurable) — Python: `argon2-cffi`, Django uses it? Django defaults to PBKDF2 sha256! consider switching to Argon2 or bcrypt.
- Legacy: upgrade on login (hash check both then save new)
- Never: MD5/SHA1/SHA256-raw (fast = brute-force). Even SHA-512-raw is weak!
- Tokens (API keys, session): store **only the hash** of token (e.g., SHA-256 of the key — random high-entropy keys are OK to hash fast; use `secrets.token_hex(32)`), show plaintext once

## Code tiers

### ❌ Bad
```python
user = {"password": request.form["password"]}     # plaintext — HE
```

### ✅ Good
```python
from argon2 import PasswordHasher
ph = PasswordHasher()
user.password_hash = ph.hash(password)             # salted per-password
assert ph.verify(user.password_hash, password)     # constant-verify
```

### ⚡ Better — parameterized & rotating
```python
# argon2 id: memory_cost=64MB class-default; parameters in config, migration path
# verify-old → rehash-save on successful login (password upgrades over time)
# tokens: API token = secrets.token_urlsafe(32); DB stores only sha256(token)
```

### 🏆 Excellent
```text
- password policy: length > minimum (NIST: ≥12) + breach check (Have I Been Pwned range API),
  no silly character requirements (NIST guidance)
- password reset: rate-limited, short-lived, single-use tokens; _delete_ username sources enumeration
- tokens: TTL + rotation + scoping (least privilege tokens); server-side revokability (hashed index exists)
- never log passwords or password hashes; sanitize in traces
- annual rotation drills: key-rotation DRI documented
```

## Failure modes
- MD5 SHA1 raw hashes (mass crack + rainbow)
- salting via naive per-site constant (identical prefixes visible)
- hash upgrade never happens over years
- tokens stored raw in DB (DB leak = all tokens)

## Evidence
- OWASP Password Storage Cheat Sheet (VERIFIED — Argon2id preferred)