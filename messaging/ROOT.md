# MESSAGING & QUEUES — ROOT NEURON

## Identity
- ID: messaging.root
- Domain: messaging
- Type: root
- Status: active
- Importance: high

## Purpose
Move work asynchronously, decouple producers from consumers, and survive bursts — deliberately: queue choice, failure semantics, backpressure, ordering, and the death of "just use Redis for everything".

## Activation
- async tasks (email, image, export, notifications, webhook delivery)
- decouple services/events; event streams; heavy schedules
- "we should add a queue" — mandate SIMPLICITY_GOVERNOR & RELIABILITY review

## Routing
```text
async jobs in one stack → celery.md (or RQ/hourly)
event stream/kafka fanout → kafka.md
Redis pub/sub transient → nosql/redis (ephemeral!)
reliable guaranteed → outbox.md + kafka/celery (see distributed)
ordering + exactly-once-ish → kafka keys, idempotent consumers
```

## Choice ladder (honest)
1. **No queue** — synchronous is fine (function or HTTP), simplest
2. **In-process async** (asyncio.task) — fire & forget with bounded queues (rare but ok)
3. **Redis-based jobs** (Celery/RQ): volume manageable, near-realtime, teams know Redis already (default for Django vertical!)
4. **Kafka**: high-volume streams, retention/rebuild, order guarantees, multi-consumer — only when audit/product analytics demand real scale
5. **Specialists**: SQS (managed), RabbitMQ (classic broker), Google Tasks (eventual)

## The messaging contract (what every queue design must answer)
- **Durability**: job survives process/crashes? (broker persistence vs Redis volatile)
- **Idempotency**: consumer retries = same side effect; event_id dedupe (idempotency)
- **Retry/backoff**: task retries (bounded), DLQ or dead-letter queue
- **Ordering**: per-key (Kafka partition, Celery queue) vs global (expensive)
- **Backpressure**: rate producer vs queue depth; monitor lag
- **Security**: broker ACL, payload schema versioning (messaging/schemas)
- **Observability**: producer/consumer/in-flight per queue — SLO (messaging/slo)

## Common failure modes
- Redis as the "queue" for durable jobs (restart loses jobs!) — either accept loss or use real broker
- unbounded queue (memory/backlog explosion)
- consumer slower than producer → lag → freshness violations (brain/failure-propagation)
- no DLQ: one poison job stalls the queue
- no idempotency: repeated consumers = duplicates in customer side effects

## Security
- broker access limited (service accounts), payloads validated against schema at boundary; no PII in dead letters

## Evidence
- Broker comparison: VERIFIED via vendor docs (S-015 Celery, S-017 Kafka, S-018 RabbitMQ)
