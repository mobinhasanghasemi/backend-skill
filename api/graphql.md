# GraphQL

## Identity
- ID: api.graphql
- Type: technology
- Status: active
- Importance: high

## Purpose
Client-defined queries over a typed schema: one endpoint, precise fields, rapid iteration. The cost: query complexity control, caching, and N+1 fighting at scale.

## Core concepts
- Schema + types + resolvers (fields), mutations, subscriptions
- Tools: Strawberry (Python), Apollo (JS), GraphQL Playground/Grafbase
- DataLoader for batch fetching (N+1!); complexity limits; persisted queries (APQ)

## When to choose
GOOD: mobile apps, heterogeneous clients, rapid product iteration, federated microservices (schema stitching)
NOT: simple CRUD (REST wins), heavy compute (queries fetch everything client asks), strict audit trails (REST + OpenAPI simpler)

## Code tiers

### ❌ Bad
```python
# resolver calling DB per child field → N+1: 
# orders: [order(...)] → item.user for each = 1000 queries
```

### ✅ Good — DataLoader (batch)
```python
user_loader = DataLoader(load_fn=batch_get_users)  # one IN query for N ids
@strawberry.field
def user(root, info):
    return info.context.user_loader.load(root.user_id)
```

### ⚡ Better — query cost control + depth limit + persisted queries
```python
# complexity limit: each field weight, reject > X — protects from "kill query"
# APQ: hashes of queries served without re-serializing — cache + audit
```

### 🏆 Excellent
```text
- schema-first design reviews (breaking changes tooling: schema diff CI)
- DataLoader discipline on every resolver; batching in DB layer
- complexity + rate limiting per client; persisted queries mandatory for prod
- metrics: per-query p95, resolver-level traces (Apollo tracing/OpenTelemetry)
- tests: schema snapshots, resolver unit tests, integration load tests
```

## Failure modes
- N+1 everywhere (lazy loader per field)
- no complexity control → expensive queries (bandwidth + CPU + DB)
- caching at HTTP level busted (POST bodies); use APQ + response cache directives
- subscription storms / no heartbeats
- schema churn without review

## Security
- field-level authz in resolvers (every field!), complexity cap, depth cap, no introspection in prod

## Performance
- Measure first: EXPLAIN (ANALYZE, BUFFERS) for query shape; pg_stat_statements for hot queries (S-044/S-047). No index/cache without measurement per PERFORMANCE_ENGINE.
- p95/p99 before/after; one change at a time.

## Reliability
- Timeouts on DB/client, retry with jitter + idempotency, backup/PITR tested monthly (S-046), RPO/RTO defined.
- Failure: pool exhaustion -> shed load, replica lag -> read-your-writes check.

## Evidence
- GraphQL core concepts: SUPPORTED practice (spec-based, no pinned URL; refresh on next release note)
