# Kafka (Event Streams)

## Identity
- ID: messaging.kafka
- Type: technology
- Status: active
- Importance: medium (choose when real scale/order/retention is proven)

## Purpose
Event streaming for true scale: high-throughput fan-out, replay/retention, partition ordering. **Not the default** — a decision earned by volume/retention/order needs (see messaging/ROOT ladder).

## The Kafka mental model (2026)
- **4.x**: KRaft-only (ZooKeeper removed), Java 17 brokers; KRaft in production from 3.5+; upgrade path via bridge 3.9→4.0
- Topic → partitions → ordered within partition; **ordering only per key** (fairness vs cost trade)
- **Producer**: acks (0/1/all), idempotence (enable.idempotence=true — no duplicate messages from producer retries)
- **Consumer groups**: each partition assigned to one consumer; lag = freshness metric
- **Retention**: topics keep events N days/hours (replay!) vs Celery (consume & forget)
- **Schema**: schemas schema registry (Avro/JSON schema) — breaking changes = compatibility enforced

## When it earns its cost
- high-volume telemetry/events (100k/s+)
- replay/history (audit, projections, state reconstruction)
- multi-consumer fan-out (3+ independent consumers of the same stream)
- backpressure via consumer lag + transaction rebalancing
Otherwise: Celery (jobs) is simpler & cheaper (SIMPLICITY_GOVERNOR)

## Code tiers
### ❌ Bad
```python
# "we'll use Kafka for everything" → queue for emails/notifications,
# ops burden of a 4-node cluster; ordering promised globally (which is wrong — Kafka orders per partition only)
```

### ✅ Good
```python
# producer: events = business facts (idempotent producer, acks=all)
# consumer group: worker handles event idempotently (event_id)
# topic per domain; partition key = aggregate_id → order per entity
```

### ⚡ Better
```python
# consumer lag monitored (alert < 5m), DLQ topic per consumer
# retry with backoff via internal retry topics (KIP-666 future) or DLQ+job
# schema registry at boundary: forward/backward compatible msg
```

### 🏆 Excellent
```text
# confluent-kafka client; batch/linger tuned; compression (zstd/lz4)
# produce/consume latency metrics; producer-side circuit breaker or bounded queue for partition outage
# exactly-once: downstream idempotency (payments) — not exactly 'exactly' semantics
# rebalance protection (static membership, cooperative); chaos: kill broker → verify partitions reassigned
# partition count planned vs growth (repartition is complex!)
```

## Failure modes
- without idempotence producers duplicate on network retry (money!)
- wrong order expectation (cross-partition)
- consumer crash storm (rebalancing thrash — frequent restarts; cooperative)
- unbounded topic growth (retention job smoke)
- no schema registry: consumers break silently on field changes

## Evidence
- Kafka docs (KRaft 4.x VERIFIED), Confluent best practices (SUPPORTED)