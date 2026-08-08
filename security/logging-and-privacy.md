# Logging & Privacy

## Identity
- ID: security.logging-and-privacy
- Type: procedure
- Status: active
- Importance: critical

## Purpose
Log what is needed for debugging/audit — without storing data you must not keep. Privacy is a storage decision, not just a display concern.

## Core principles
1. **Classify data**: PII (names, emails, IPs, phone, location, credentials), sensitive (payment, tokens, health), operational (no personal data)
2. **Logs = storage too**: GDPR/SOC2 apply (retention, access, deletion); minimisation over encryption
3. **Never log**: passwords, tokens, session ids, raw payment data, full documents, secrets (secrets.md)
4. **Mask/redact**: PII in logs (email → `a***@domain`); configurable per data class
5. **Structured logs** (JSON, key-value) with stable field names — searchable, filterable

## Code tiers

### ❌ Bad
```python
logger.info(f"user {user.email} paid {order.amount} with card {card.number}")
# → PII + full card number in logs, forever
```

### ✅ Good
```python
logger.info("payment.completed", extra={"user_id": user.id, "order_id": order.id,
    "amount_cents": order.amount_cents, "payment_method": "card", "masked": True})
```

### ⚡ Better — structured + redaction layer
```python
class RedactingFormatter(logging.Formatter):
    PATTERNS = [re.compile(r"(card)[0-9]{4}"), re.compile(r"(password)=(\S+)")]
    def format(self, r):
        return self.PATTERNS_reduce(super().format(r))   # regex redact in one place
```

### 🏆 Excellent
```text
- structured JSON logs; correlation_id/trace_id on every record; consistent field names
- PII registry (which fields, where logged, retention); masks enforced by linter (no f-strings with user objects in logs)
- audit trail: who/when/what (auth, payment, admin ops) append-only, retention policy set
- SIEM/alerting on structured fields; privacy review per new log field
- tests: log redaction test asserts no PII in emitted records
```

## Failure modes
- f-string logging with user objects (repr leaks)
- logging exception stack traces containing query params with tokens
- forever-retention defaults; no access control on logs
- unstructured text logs (regex-soup, unsearchable)

## Security
- logs access = read access to PII: least-privilege, encryption at rest, egress controls

## Evidence
- Logging/privacy design: SUPPORTED (OWASP cheat-sheet family, S-023)
