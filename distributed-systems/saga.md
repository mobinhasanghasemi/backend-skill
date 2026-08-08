# Saga Pattern

## Identity
- ID: distributed-systems.saga
- Type: procedure
- Status: active
- Importance: high (only when cross-service consistency truly needed)

## Purpose
Coordinating a multi-service business flow **without 2PC**: each step commits locally, and on failure the saga runs compensating actions to undo completed steps (eventually consistent outcome).

## Two styles
- **Choreography**: each service listens to events and acts/compensates (event-driven, decentralized)
- **Orchestration**: a coordinator service (saga executor) drives steps and compensations (explicit, easier to reason about, single point to monitor)

## When saga is right
- true cross-service business transaction (order → payment → inventory → shipping), money flows
- when a single DB can't span the writes (they live in different services)
- When NOT: if one service + one DB can hold the flow, DO THAT (sagas cost) — SIMPLICITY_GOVERNOR applies!

## Code tiers

### ❌ Bad
```python
order_svc.create(order); pay_svc.charge(card); ship_svc.schedule()  # sync chain
# if charge succeeds but ship fails: order stuck paid, no compensation
```

### ✅ Good — orchestrated with compensating txns
```python
try:
    oid = order_svc.create(order)
    cid = payment_svc.charge(oid, card)
    ship_svc.schedule(oid)
except PaymentFailed: order_svc.cancel(oid)
except ShippingFailed: payment_svc.refund(oid); order_svc.cancel(oid)
```

### ⚡ Better — async orchestration with state machine
```python
# saga stored in DB (state machine: created → charged → shipped | cancelled)
# each step enqueued (messaging), compensate enqueued on failure, 
# retries + dead-letter per step; manual operator dashboard for stuck sagas
```

### 🏆 Excellent
```text
- saga state machine table with transitions + idempotent step execution (step ids)
- compensations themselves idempotent and retried (refund once!)
- partial-failure drill: kill payment after order; verify refund path in staging
- metrics: saga duration, failure rate per step, stuck-saga alerting
- choreography note: use orchestrator when flow steps > 3 or compensation logic is complex
```

## Failure modes
- compensating actions not idempotent (double refund)
- saga without persistent state (restart = lost flow)
- compensating actions failing permanently (needs DLQ + human)
- using saga where a single DB transaction would do (cost/complexity)
- orchestration stepping through sync calls (latency, no async buffer)

## Evidence
- "Designing Data-Intensive Applications" Ch.9, microservices.io saga (VERIFIED)