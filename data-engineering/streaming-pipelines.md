# Streaming Data Paths (for analytics)

## Identity
- ID: data-engineering.streaming
- Type: procedure
- Status: active
- Importance: medium

## Purpose
When data flows continuously (clicks, events, sensors) — make the stream trustworthy: at-least-once + idempotent consume into the warehouse, with sources preserved (replayable, retention).

## Streaming matrix (don't overbuild)
| Scale | Tool |
|---|---|
| simple events → warehouse | Kafka (produce) → batch drain (or small) |
| low volume | Websockets? No; POST to collector (API) + batch sink is fine |
| medium, need filtering/aggregates on the way | Kafka + Flink/debezium |
| high volume, single consumer | Kafka + consumer stream (Spark/Python) |

## The streaming axioms
1. **At-least-once** delivery — downstream must dedupe (`event_id` unique in target)
2. **Key = entity** (user) — keep per-entity ordering
3. **Retention** on brokers for replay (3-10 days) — makes death of producers recoverable
4. **Schema registry**: event schema versions + compatibility (protobuf/JSON-Schema)
5. **Freshness/backlog**: consumer lag monitored (queue > SLO → alert) — the #1 dead metric
6. **Input pipe to warehouse = idempotent sink** (see batch incremental)

## Code tiers
### ❌ Bad
# nightly full dump = database source stateless + no event log (spark):
# — "did D > rail?" — DB has only latest; changes lost / no lineage
```
### ✅ Good
# events → kafka topic (schema registry, IDs), consumer writes to
# staging table (key=event_id dedupe), dbt incremental marts daily
```
### ⚡ Better
# topic per domain; key = entity; retention 7-30d; lag alert < 10m
# consumer idempotency at the sink: event_id unique in target; replay bulletproof
# dead-letter + repair path (DLQ topic + replay tool)
### 🏆 Excellent
# stream processing windowed aggregates (Flink/ksql) for near-real charts,
# but analytical store remains batch (freshness set by SLO)
# tests proven: schema compatibility gate, event replay drill, lag chaos
```

## Failure modes
- stream into live-dashboards without storage (stateless = untraceable)
- no dedupe at sink (data duplicated in marts)
- unbounded lag = stale analytics + unbounded memory (backpressure!)
- consumers and schemas not versioned

## Evidence
- Kafka schema registry docs (VERIFIED), DW streaming practice (SUPPORTED)