# Database as a Queue

## Identity
- ID: architecture.anti-patterns.database-as-queue (database-as-service)
- Severity: HIGH

## Definition
Using a relational DB's tables/rows (job = row) as a message/queue medium — polling tables, updating statuses.

## Why it's seen
- No extra infra; transactional coherence
- Familiar SQL

## Why it fails at scale
- Polling = extra load / database load
- Row-level locking between workers
- **ordering not guaranteed**
- Dead rows pile (bloat); no real backup
- Scaling workers bounded by DB contention
- No broker properties: ack, TTL, DLQ, retries

## When it's actually OK
- tiny volumes (e.g., a few hundred rows), admin background tasks, no strict time guarantees
- when the extra infra isn't justified (startup)

## When to move to a real broker
- volume growth, timeout realities, need ordering per entity, need DLQ, multiple consumers per work type

## Correct migration
messaging/celery.md: broker (RabbitMQ/SQS/Redis queue) + worker + DLQ.

## Detection
- Look for tables named `worker`, status-column polling loops

## Evidence
- Industry-observed pattern; "Don't use tables as queues" consensus (SUPPORTED)