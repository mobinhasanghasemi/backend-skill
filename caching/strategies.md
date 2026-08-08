# Cache Strategies (patterns)

## Identity
- ID: caching.strategies
- Type: concept
- Status: active
- Importance: high

## Purpose
Match the cache pattern to the data + access shape: read-heavy stable, read-mostly lists, user-scoped, derived aggregates — each with its trade-off made explicit.

## The patterns menu
| Pattern | Shape | How | Trade-offs |
|---|---|---|---|
| **Cache-aside (lazy load)** | read-heavy | app reads cache → miss → DB → set cache (TTL) | simple; first-hit cold; stampede risk |
| **Read-through** | same as aside but at data-fetch layer | lib fills cache transparently | consistency management |
| **Write-through** | write-frequent | update BOTH cache and store on write | cache write adds latency; consistency strong |
| **Write-behind** | write-throughput dive | queue flushes to DB | loses writes on crash (ack!) |
| **Refill (event-driven)** | business-derived | on domain event → rebuild key | event coverage = correctness |
| **Version/epoch key** | everything! | key includes epoch; bump epoch on change | stale reads to moment of bump |
| **Local+distributed (L1/L2)** | hot services | process cache + Redis | multi-node invalidation complicates (TTL short L1) |

## The decision flow
1. How stale can data be? (per business object: dashboards 5m, order status 0 — never cached)
2. Read rate vs write rate (cache only when read >> write, or user-identical reads)
3. Where's the hottest set? (top 5% of keys = 90% of reads — cache THAT)
4. What invalidation events exist? (domain events through outbox → rebuild on event)

## Code tiers
### ❌ Bad
```python
# blind TTL on user carts: put → timeout 900; the extension has zero cacheable value
# heavy: stampede rebuild every second
```

### ✅ Good — cache-aside with versioned key
```python
def get_catalog(tenant_id):
    key = f"catalog:v2:{tenant_id}"
    if c := cache.get(key): return c
    data = query_catalog(tenant_id)
    cache.set(key, data, timeout=600)
    return data
```
### ⚡ Better — event-based invalidation
```python
# on product update (service): cache.delete(f"catalog:v2:{tenant_id}")
# + short-timeout fallback if event missed (read side tolerant, catching staleness)
# singleflight/locking: only one rebuild (stampede guard)
```

### 🏆 Excellent
```text
# per-object, per-tenant keys documented; metrics: miss rate = logical freshness
# cache warm at deploy; chaos: Redis down → degrade to DB (measured latency hit)
# SLO: cache only if it pays p95 — else REMOVE it (simplicity)
```

## Failure modes
- write-through complexity mismatch (events missing → stale
- TTL = "best lunch" strategies (cargo)
- false confidence: hit rate 99% but only trivial data served from cache

## Evidence
- Cache-aside patterns (common knowledge VERIFIED); invalidation.md for the hard part