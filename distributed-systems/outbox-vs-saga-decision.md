# Outbox vs Saga — Decision Tree

## Identity
- ID: distributed-systems.outbox-vs-saga-decision
- Domain: distributed-systems
- Type: pattern
- Status: active
- Importance: critical
- Last Verified: 2026-08

## Purpose
Choose correctly between transactional outbox (atomic local + eventual publish) and saga (multi-service transaction with compensation) — the most misapplied distributed pattern.

## Core Concept
Outbox = single DB atomicity, one service owns the truth, others react. Saga = N services each commit, compensations undo on failure. Use outbox when you can keep the write local; saga only when N services must commit.

## Decision Rules
- **Outbox** if: one service writes business + event atomically (payment + `payment_created`), consumers are idempotent, ordering per aggregate enough. Cost: relay + idempotency store (S-082).
- **Saga (orchestrated)** if: checkout touches `order` + `inventory` + `payment` in different services, each with its own DB, and failure needs compensation (e.g., `reserve → pay → confirm` with `cancelReservation`).
- **Saga (choreographed)** only if orchestration coupling is worse and team can handle event-versioning + dedupe + observability × N.
- Never 2PC; never “saga for single DB”.

## Trade-offs
| Pattern | Atomicity | Ops | Failure handling |
|---|---|---|---|
| Outbox | single DB tx | relay + DLQ | retry |
| Saga | eventual across N | orchestrator + compensation × N | compensating tx |

## Security / Reliability
- Outbox events carry minimal PII, CloudEvents envelope (S-082), idempotency key per event.
- Saga needs timeout + fencing token for compensations; S-068 for Celery orchestration.

## Evidence
- Outbox pattern SUPPORTED, CloudEvents VERIFIED via S-082; saga orchestration via S-068 (accessed 2026-08).

## Code Tiers
<!-- illustrative -->
```python
# outbox atomic (illustrative — adapt to your ORM)
with transaction.atomic():
    order = Order.objects.create(...)
    Outbox.objects.create(aggregate="order", event="order.created", payload={"order_id": order.id})
# relay (Celery) polls SELECT ... FOR UPDATE SKIP LOCKED and publishes
```

## Questions To Ask
1. How many DBs must commit atomically?
2. Can the write stay in one service?
3. What is the compensation cost?
