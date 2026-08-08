# Idempotency in APIs

## Identity
- Build: **ID: api.idempotency**
- Type: procedure
- Status: active
- Importance: critical

## Purpose
Clients retry safely (networks, timeouts, duplicates) — the same logical operation, once effective, returns the same result. Mandatory for writes with side effects (payments, orders, notifications).

## Core model
- **Idempotency key**: client-sends unique key header (`Idempotency-Key: uuid`); server keys stored safely with status+response
- Replayed key → same response (200/201 with original body), without re-executing
- Key scope per user+endpoint; TTL (24h typical); key hash not raw (privacy)
- Distributed systems: store in same DB/or transactional (row in idem table in one tx)

## Code tiers

### ❌ Bad
```python
@app.post("/charge")
def charge():
    result = gateway.charge(card, amount)   # twice if client retries → double charge!
    return result
```

### ✅ Good
```python
@app.post("/charge")
def charge(request, body):
    key = request.headers["Idempotency-Key"]
    if existing := Idempotency.get(key):     # store value incl. status
        return Response(existing.response, status=existing.status)  # replay (200/201)
    with transaction.atomic():
        res = gateway.charge(...)
        Idempotency.create(key=key, status=201, response=res)
    return res
```

### ⚡ Better — idempotency atomic with business effect (no double side-effect window)
```python
with transaction.atomic():
    # 1) idempotency row inserted first (INSERT ... ON CONFLICT DO NOTHING)
    # 2) gateway call with idempotent external key (Stripe-like: dedupe by "idempotency_key" server-side)
    # the DB is source of truth; the store never double-charges
```
- cover concurrent duplicate requests (unique constraint on key, retry)

### 🏆 Excellent — distributed + at-least-once end to end
```text
- idempotency keys have signed/opaque format (no PII), TTL, per-tenant bucket
- outbox + idempotent consumers (messaging/outbox) — 202 if applying, replay returns prior status
- tests: replay / concurrent duplicate / expired key / different key same POST
- metric: duplicate-rate, keys-created, replay-hit %
- contracts documented: "you MAY send Idempotency-Key: any non-empty string"
```

## When NOT needed
- pure reads (GET) unless side effects at storage
- naturally idempotent ops (PUT replace, DELETE not-found OK)

## Failure modes
- key not enforced for POST (double-side-effect) 
- idempotency state NOT durable (restart loses) 
- key collision across tenants — namespace keys!
- weak hashes (raw keys stored = privacy risk)

## Observability
- metrics: replay ratio, key-hit ms, conflicts

## Evidence
- Idempotency-Key pattern: SUPPORTED practice (API guides); no official RFC
