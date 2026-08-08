# Cache Invalidation

## Identity
- ID: caching.invalidation
- Type: procedure
- Status: active
- Importance: critical

## Purpose
The discipline that keeps caches correct: versioned keys, event invalidation, and the honest limits of TTL.

## The hierarchy (strong to weak)
1. **Event-based invalidation** (write path): when stored data changes, delete/mark the derived keys. Deterministic freshness.
2. **Version-keyed keys**: keys include `{epoch}`; bump epoch on any change → old keys orphan naturally (GC via TTL).
3. **TTL with jitter**: bounds staleness; no exact consistency.
4. **No invalidation + short TTL**: survivable only when data changes rarely.

## The write-path discipline
```python
def update_product(pk, **fields):
    obj = Product.objects.get(pk=pk)
    for k, v in fields.items(): setattr(obj, k, v)
    obj.save()
    invalidate_product_keys(pk)      # must be in the SAME flow as the write
```
Invalidate after commit (post-commit hook) or via outbox → cache delete retried (outbox.md) so a failed cache delete can be retried.

## Stampede protection (the killer detail)
- Key expires → 100 parallel requests rebuild → DB bang
- Fixes: (a) single-flight (one rebuild, others wait/serve-stale), (b) probabilistic early expiry (background refresh before TTL), (c) jitter on TTL

## Code tiers
### ❌ Bad
```python
def update_order(order_id, data):
    order.save()                    # no invalidation
# consumers see stale order status until TTL; list views cache even older
```

### ✅ Good
```python
def update_order(order_id, data):
    with transaction.atomic():
        order.save()
        version = bump_order_version(order)     # one authoritative version
    cache.delete(f"order:v{version}:{order_id}")  # delete AFTER commit
```

### ⚡ Better — event-driven
```python
# after commit: outbox event "order_updated" →
# consumer job deletes/rebuilds ALL derived keys (dashboard, list, detail)
# job idempotent (safe re-run), no one-off cache.delete() forgotten in code paths
```

### 🏆 Excellent
```text
- key registry in repo: every cache key has owner + invalidation path (no orphan keys)
- integration test: write → cache reflects change within N ms
- metric: version drift (max age of served cached copies) to bound staleness
- chaos: force cache delete failure → outbox retry → still fresh eventually (proves design)
```

## Failure modes
- delete before commit (readers see pre-commit empty → mild, actually fine; DELETE after = safe)
- invalidation on write path but not on the second writer (multiple update sites)
- cache.clear() at release: mass invalidation on deploy = cold start
- version-free keys using "ID" only: immutable data cached forever after change

## Evidence
- Common invalidation patterns (VERIFIED as practice); consistent with outbox/DDD eventing (SUPPORTED)