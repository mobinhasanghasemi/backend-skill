# Cryptography for Backends

## Identity
- ID: security.cryptography
- Type: concept
- Status: active

## Purpose
When to encrypt (at rest, in transit), which algorithms are correct in 2026, and how to store keys — without rolling your own crypto.

## Decisions map
- **In transit**: TLS 1.2+ (1.3 preferred) everywhere; HSTS; certificates via Let's Encrypt/managed
- **At rest (data)**: AES-256-GCM (auth encryption) via KMS (AWS/GCP KMS envelope encryption); DB-level via managed RDS/EBS for compliance; envelope = DEK per dataset + KEK in KMS
- **Passwords**: not encryption! → passwords-and-tokens.md (Argon2id)
- **Signatures**: webhooks HMAC-SHA256 (shared secret) — api/webhooks.md; JWT signing → HS256 (HMAC) or RS256/ES256 (public-key); prefer asymmetrical for multi-party
- **Key exchange**: never implement Diffie-Hellman/PFS yourself; use TLS
- **HSM/KMS** for high-value keys; local-LEMK anti-propagation setups only if auditable

## Code tiers

### ❌ Bad
```python
# password = AES encrypt + base64, same key hardcoded  — 'encryption' misuse!
# (attacker: decrypt everything; also keys the plaintext to memorize)
```

### ✅ Good — envelope with KMS
```python
from boto3 import client as kms
kms = ...
data_key_wrapped = kms.generate_data_key(...GenderId)
# store wrapped DEK + AES-GCM ciphertext + nonce
```

### ⚡ Better
```python
# per-record data keys: one DEK per dataset, wrap with KEK KMS
# AAD bound to record id (authenticate context!) (GCM AAD)
# rotation path: re-wrap data keys on KEK rotation (no re-encryption of payloads)
```

### 🏆 Excellent
```text
- algorithms pinned from audited libs (cryptography.io; pyca), no raw AES code
- KMS region replication; key policies least-privilege
- tests: wrong-key → AuthenticationError; tamper ciphertext → open/Authenticated
- key rotation calendar + drill; logs never contain keys
- cryptographic hygiene review each new data class
```

## Failure modes (recurring reality)
- AES-ECB (leaks patterns), hardcoded IV reuse, custom MAC
- choosing encryption for data that shouldn't be stored at all
- URLs/params carrying secrets

## Evidence
- RFC 8446 (TLS 1.3), NIST SP 800-57 key management, pyca/cryptography docs (VERIFIED)