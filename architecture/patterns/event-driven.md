# Event-Driven Architecture

## Identity
- ID: architecture.patterns.event-driven
- Type: pattern
- Status: active

## Purpose
Components communicate by publishing/subscribing events (decoupled, asynchronous), so state changes flow without synchronous calls.

## Core Concept
Producer publishes event (order.created, user.updated); consumers subscribe; brokers (Kafka/RabbitMQ/pg notify) decouple. Systems react to what *happened*, not by calling.

## Mental Model
A town square with a public notice board: everyone reads notices (events) they care about; the post branch (producer) writes once.

## Activation Conditions
- workflows with many downstream reactions to a change (notify, analytics, search, email)
- demand for decoupling + resilience (producer doesn't await consumer)
- fan-out of the same fact

## Do Not Activate When
- simple linear request/response flows (adds complexity)
- ordering guarantee required client-visible w/o strong broker support
- no ops capability for brokers

## Structure
```
Event: {id, type, aggregate_id, occurred_at, payload, version}
Broker: topic per domain, partition for ordering
Consumer: idempotent processing (arch002!)
```

## Advantages
- Decoupling, independent evolution; scale producers/consumers independently; event replay (if stored); audit trail

## Disadvantages
- Eventual consistency; duplicate/out-of-order delivery; debugging across hops; schema evolution of events (versioning protocol); at-least-once confusion

## Failure Modes
- **Idempotency violations** (double processing)
- Out-of-order messages breaking business invariants
- DLQ ignored → silent data loss
- Event schema breaking consumers (versioned events; additive fields)

## Security
- Authz inside consumers (subscriber must re-check); injectable event payloads (validate); no secrets in events

## Performance
- Async = latency off the sync path; but broker throughput planning; backpressure

## Scalability
- Independent scaling; consumer groups; partitions = degree of parallelism & ordering scope

## Reliability
- Broker durability (replicated, acks config); retry/DLQ; schema registry; consumer lag SLO

## Observability
- Trace across pub/sub (correlation id propagated); consumer lag metrics; DLQ alerts

## Testing
- Contract tests on event schema; consumer tests with recorded events; failure tests (DLQ, out-of-order)

## Evolution Path
- Start sync + DB → extract events for integration; replace queued jobs where domain events fit

## Alternatives
- Request/response REST for most CRUD; choreographed vs orchestrated saga in distributed-systems/saga.md

## Evidence
- Event-driven literature, SOA/EDA (VERIFIED concept; pattern heavy ops)