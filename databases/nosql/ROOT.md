# NoSQL — ROOT NEURON

## Identity
- ID: databases.nosql
- Type: root
- Domain: databases
- Status: active

## Purpose
Router for non-relational stores: when the relational model genuinely fails, which NoSQL family fits, and what consistency/ops you trade.

## The honest frame
Most "NoSQL needs" are actually: (a) cache — see caching/, (b) wrong schema — see PG JSONB, (c) specialty engines (search, vector, time-series) — see below. Choose correctly.

## Families (decision table)
| Family | Engine here | Fits when | Costs |
|---|---|---|---|
| Key-value / cache | Redis (nosql/redis.md) | hot value lookup, sessions, counters | memory, eviction, durability choice |
| Document | MongoDB (nosql/mongodb.md) | flexible schemas, documents = ownership, reads by doc key | consistency trade; join poor |
| Search | Elasticsearch (nosql/elasticsearch.md) | free-text, facets, aggregations | consistency of writes; ops |
| Vector | vector-databases.md | embeddings similarity (AI) | engine per needs |
| Time-series | (not here; extend) | sensor/telemetry append-heavy | retention; pg time-scale possible |
| Wide-column | (Cassandra etc.) — optional node | high-write-Shard-dispo | ops burden heavy |

## Routing Rules
```text
"cache/session/rate-counter"   → redis
"document, flexible schema"    → mongodb
"full-text search/facets"      → elasticsearch
"vector/AI/RAG"                → vector-databases
"feature cases"                → review need; relational + JSONB usually covers
```

## Mandatory questions (NoSQL candidates)
1. Do we actually NEED it? (Governor: does a PG/MySQL instance fail the requirement?)
2. What does consistency allow? (eventual OK?)
3. Who operates it? (Java Ops: ETLS vs PG)
4. Write throughput vs Index rebuild
5. Data growth + retention
6. Is the required query expressible?

## Common NoSQL failure modes
- Trying to make it relational ("many-to-many in Mongo" pain)
- Losing transactions thinking they didn't matter (money flows proved they do)
- Caching storage requirements wrongly (validity/exetting)
- Ops spiral (search cluster sizing, vector index refresh)

## Security
- each engine: TLS, authN roles, ingest validation (no injection—key mangling), PII flags

## Evidence
- Engine choice framework; "document" and "search" families (SUPPORTED/VERIFIED per family neuron)