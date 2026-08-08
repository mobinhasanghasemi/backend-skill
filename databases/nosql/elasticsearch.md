# Elasticsearch

## Identity
- ID: databases.nosql.elasticsearch
- Type: technology
- Status: active
- Importance: medium

## Purpose
Full-text search, faceting, aggregations over large text/field data — as a *specialty* engine, not a general-purpose database.
- Own cluster nodes; indexing = near-real-time; acceptable for search power

## Core model
Inverted indexes over analyzers (tokenization, stemming, synonyms); documents in indices; shards = lucene partitions; replicas = availability+read scaling. "Refresh interval" ~1s (NRT). Ops-heavy (the biggest real cost).

## Activation
- free-text search across millions of docs (product, log, content)
- faceting/aggregations on fields
- geolocation filtering
- log/metric analytics backing (the "search" side; not logs sink by default)

## Do Not Activate
- authoritative million-row CRUD by unique key (relational/Redis is better)
- transactional financial data (eventual, questionable repeatability)
- when a plain example (SQL LIKE / PG FTS + semicolon) already fine (check scale!)

## Decision Rules
1. **Source of truth stays elsewhere** (e.g., PostgreSQL); ES is a search **index/projection** fed via job/stream; never the only store of critical records
2. Schema: explicit mapping is maturity; no dynamic mapping surprises in prod
3. Shards: sizing math (per-shard ~30GB recommended-practice; too many shards harms)
4. Replicas for read scaling & node redundancy
5. Refresh time: configure per use case (logs: 5-30s OK; product search: faster)
6. Rate: never let indexer hog the ingest queue; backpressure

## Failure modes
- red cluster (shard replicas lost) → search outage
- mapping change (reindex! downtime budget)
- index bloat / field bloat (large-string fields blow memory)
- slow queries (heavy aggregations, poor routing) — design `_search` against the actual data distribution
- ingest bursts without backfill → heap pressure → GC pause

## Security
- HTTPS internal, authN (basic/X-Pack or reverse-proxy middleware), index-level access
- PII fields masked or excluded from indexing per policy

## Code: ingest path tiers
### ❌ re-index whole doc on every field change
### ✅ app → job → bulk POST to /index/_doc (batch bulks)
### ⚡ Better
- idempotent refresh per PK; transient exceptions retried; alias `read`/`write` for zero-downtime reindex
### 🏆 Excellent
```text
- default pipeline: versioned mappings + alias strategy
- bulk batching with size control; error/DLQ on ingest
- doc growth governance: index+lifecycle (hot/warm/cold, rollover by size)
- alarm: unassigned_shards, JVM heap, SLOW queries
- search side: `_track_total_hits` cap, size pages, field caps enabled
```

## Failure modes
- heap/shard dust; gc storms; alarms ignored; snapshot/restore untested
- reindex taking forever (plan data movement)

## Observability
- cluster_health, jvm, shard metrics, slow log, index rates

## Evidence
- Elastic docs (VERIFIED); "search index as projection" practice (SUPPORTED)