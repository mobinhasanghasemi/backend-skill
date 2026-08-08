# CACHING — ROOT NEURON

## Identity
- ID: caching.root
- Domain: caching
- Type: root
- Status: active
- Importance: high

## Purpose
Make hot reads fast and cheap — in the right order (after the query is sound), with invalidation designed, not accidental TTL. Cache is an optimization, not a feature: SIMPLICITY_GOVERNOR requires the justification.

## Activation
- "reads are slow", "same data fetched repeatedly", "DB load"
- adding a cache layer decision (justify!)

## Routing
```text
strategy choice  → strategies.md (read-through, write-through, cache-aside)
invalidation     → invalidation.md (TTL vs events vs versioning)
Django layer     → django/caching.md
browser/CDN      → api/http-caching.md (headers)
Redis infra      → databases/nosql/redis.md
```

## The caching order (many get this backwards)
1. **Make the query right** (index + N+1 fix) — caching fast wrong data is a trap
2. **Consider replicas** (read scaling first)
3. **Then cache** what's still hot: per-key, deliberate TTL + invalidation
4. Never cache per-request/user data under shared keys (leak! + architecture anti)

## The cache contract
- **Key design**: `{domain}:{entity}:{id}:{version}:{tenant}` — version bumps on schema change (no purge!), tenant embedded (no leak!)
- **TTL**: correctness >> freshness; TTL = tolerance of staleness, NOT the invalidation strategy
- **Invalidation**: explicit on writes (delete/update event) beats generic cache.clear() (nuclear)
- **Stampede**: k hot key rebuilds collapse (build in one, lock, or stagger TTL jitter)
- **Hit rate is not goal**: 99.9% hit rate on zero-value data is noise; goal = correct data + p95 SLO

## Common failure modes
- caching BEFORE query fix (masks N+1 forever, confuses debugging)
- unbounded TTLs on user/tenant data (stale users land in everyone else's)
- invalidation shotgun (`cache.clear()`) — kills performance + neighbors
- cache thundering herd at expiration hour (identical TTLs!)
- no metrics (miss-aware)

## Security
- per-tenant keys, no PII in keys, redis auth nets (DATABASE ACL), environment separation

## Evidence
- Cache strategy decisioning: SUPPORTED practice; HTTP semantics per source-S-030
