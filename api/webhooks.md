# Webhooks

## Identity
- ID: api.webhooks
- Type: procedure/realtime
- Status: active
- Importance: high

## Purpose
Event-driven notifications to external systems. Contract: we POST, they get called. Reliability is ours; acknowledgment is theirs.

## Core components
1. **Event schema** — stable fields + version
2. **Signature/HMAC** — security-critical (verify authenticity!)
3. **Retry policy** — exponential backoff, max attempts, dead-letters
4. **Idempotent payload** — event_id + dedupe on consumer
5. **Ordering** — at-least-once vs ordered per entity (seller async)

## Code tiers

### ❌ Bad
```python
# fire-and-forget: requests.post(webhook_url, json=event)  # lost on failure, no retry
```

### ✅ Good — worker + retries
```python
# enqueue to queue (outbox), deliver via worker with retry backoff,
# verify HMAC signature with secret; non-2xx → retry index
```

### ⚡ Better — structured delivery
```python
payload = {"event_id": str(uuid4()), "type": "order.paid",
           "version": 2, "data": {...}, "sent_at": iso}
signature = hmac(secret, payload_bytes).hexdigest()
# headers: X-Event-ID, X-Webhook-Signature
# retry: exponential 1m→2m→…→cap; DLQ after 24h
# delivered endpoint must return 2xx with body {received: true}
```

### 🏆 Excellent
```text
- outbox pattern: event written in same tx as business change → guarantee delivery
- consumer idempotent (event_id stored; dedupe window)
- replay API for consumers; event catalog docs
- delivery metrics: success%, p50/p95 latency, dead-letter rate, avg retries
- paywall: secured endpoint with quota per consumer (they throttle us) and tenant isolation
- tests: signature mismatch, duplicate delivery, retry storm, ordering when needed
```

## Failure modes
- no HMAC verification → attacker sends fake events  
- no idempotency → duplicate side effects  
- infinite retries → load storms on unhealthy consumer
- no DLQ → silent lost events

## Security
- HMAC verification with constant-time compare (`hmac.compare_digest`), secret rotation via Vault (S-059), no secret in logs (S-078).

## Performance
- Batch worker with `FOR UPDATE SKIP LOCKED`, backoff jitter, DLQ after cap; p95 delivery <2s at 100 req/s (measure).

## Reliability
- Outbox guarantee (same tx), retry budget, DLQ alert, replay API; RPO 0 for events, RTO = relay lag.

## Evidence
- Webhook retry/HMAC patterns: SUPPORTED practice (third-party API guides) — HMAC verified via S-069 (accessed 2026-08).

