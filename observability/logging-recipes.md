# Logging Recipes (Structured Logging)

## Identity
- ID: observability.logging-recipes
- Type: procedure
- Status: active
- Importance: high

## Purpose
Logs that can answer questions, not archives of prose: structured fields, correlation, no PII noise, and sampling that preserves signal.

## The recipe (for any stack)
1. **Format**: JSON lines (one object per line). Fields (stable): `ts, level, logger, msg, trace_id, span_id, service, env, version`
2. **Levels**: DEBUG off in prod; INFO for high-value events (start/end of flows); WARN for externally observed anomalies; ERROR for app faults that need intervention (not just bad-input handled)
3. **Correlation**: trace_id is the spine — every request/worker logs it; every downstream call ships it (headers + queue metadata)
4. **Sensitive data**: never log PII/passwords/tokens/cookies/full payment (security/logging-and-privacy.md); redact at source
5. **Context**: business semantic info (order_id, customer_id, tenant, endpoint) for analytics WITHOUT personal data
6. **Volume control**: debug via `DEBUG` on demand (feature flag), sample INFO traces; never delete ERRORs

## Code tiers

### ❌ Bad
```python
print("user logged in " + user.email)      # unstructured f-string, PII, no ids
```

### ✅ Good
```python
logger.info("login.success", extra={"user_id": u.id, "method": "oidc"})
# → JSON line with all context; searchable without PII
```

### ⚡ Better
```python
# middleware injects trace_id + request_id into every record's context
# any log call reuses them — all logs everywhere correlate automatically
```

### 🏆 Excellent
```text
- central log pipeline (OTel collector → ElasticSearch/Loki/Clickhouse) with
  retention by level, storage quotas, tenant isolation
- log queries documented (top N errors, trace view from id), used postmortals
- alerts FROM logs only for rare high-signal cases (unexpected ERROR patterns)
- test: redaction test asserts jo PII in emitted records (regex suite)
- sampling policy: 100% of errors/traces for slow endpoints; 1-10% of hot
```

## Failure modes
- logs as the only observability (no metrics/traces): long debug sessions
- INFO noise kills error signal, alerts on the wrong thing
- f-string + window lines in prod (double cost)
- correlation missing → searching by customer impossible

## Evidence
- OTel logging conventions, 12-factor logs (VERIFIED), ELK/Loki best practices