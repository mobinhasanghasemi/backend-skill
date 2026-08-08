# Outbox Pattern

## Identity
- ID: distributed-systems.outbox
- Type: procedure
- Status: active
- Importance: high

## Purpose
Guarantee "business change + its event" commit **atomically**, then deliver the event reliably — without distributed transactions. The fix for "notification lost after order created" and for double-send races.

## Core model
1. In the SAME DB transaction: write the domain change AND an `outbox` row (event payload, id, type, status)
2. A relay worker polls outbox (or listens via logical replication / pg notify), publishes to queue/topic
3. Consumer idempotency: the event id dedupes (see api/idempotency.md)
4. Failure: relay retries with backoff; rows deleted/archived after ack; dead-letter rows → alert

## When to use (vs alternatives)
- Event MUST not be lost and ordering mostly preserved → outbox (+queue)
- Event fire-and-forget → plain enqueue is fine (lose tolerance)
- Exactly-once consumer → consumer-side idempotent (event id) — never rely on exactly-once delivery

## Code tiers

### ❌ Bad
```python
order.save()
notify_queue.enqueue(order.id)   # if enqueue fails (Redis down), notification lost forever
```

### ✅ Good
```python
with transaction.atomic():
    order.save()
    Outbox.create(event_type="order.created", payload=serialize(order))
# relay worker:
for ev in Outbox.unpublished(): publish(ev); mark_published(ev)
```

### ⚡ Better
```python
# relay with backoff + dead-letter + idempotent consumer:
# id = event_id; consumer INSERT ... ON CONFLICT DO NOTHING (or get-or-create)
# relay polls with batch size; after ack: delete/mark done (archive)
# NOTIFY/LISTEN (pg_notify) to wake relay instead of poll (low latency)
```

### 🏆 Excellent
```text
- outbox + consumer exactly-once enough: delivery idempotent (event_id), 
  consumer state store with key TTL
- ordering per aggregate (partition key = aggregate id)
- metrics: outbox lag, dead-letter rate, relay failures; alert on lag > N
- tests: crash mid-relay → no event lost, no duplicate side effect
- alternatives honestly considered: CDC (Debezium) for existing systems; 
  transactional emit in DB-proxied engines when available (some BQs do)
```

## Failure modes
- outbox table grows unbounded (archive job needed)
- relay without backoff → retry storm on dead broker
- consumer not idempotent → duplicates despite outbox
- event payload too large / schema drift (version payload + schema registry)
- publishing in a separate tx = same old race

## Security
- events carry data: authz at consume; redact PII per event schema; no secrets

## Evidence
- Transactional outbox pattern: SUPPORTED (Kleppmann DDIA); INFERRED elsewhere
