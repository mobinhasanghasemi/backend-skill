# Django Caching & Performance

## Identity
- ID: django.caching
- Type: procedure
- Status: active
- Importance: high

## Purpose
Use Django's cache machinery deliberately: which layer (template, view, keys), what invalidation, what TTL — and never cache correctness away (per-user, per-tenant!).

## Cache layers in Django
1. **Per-view** (`@cache_page`): simplest; whole response; invalidation = cache.clear or key purge; auth'd pages need `vary` handling (private!)
2. **Template/fragment**: `{% cache %}` per block — cheap, coarse
3. **Low-level (Redis)**: `cache.set/get` for computed values (DB aggregations, expensive services)
4. **Query cache (select_related? no — memcached-style objects)**: cache serialized DTOs, not ORM objects (mutation risk)

## The invalidation truth
- TTL is the weakest form; **explicit invalidation** on writes (key versioning: `f"orders:{user_id}:{version}"`, bump on mutation) is what production needs
- **Cache keys must include scope** (user_id, tenant, version, locale) — shared keys = data leak! (security)
- Cold-start spike: pre-warm on deploy; stampede guard (lock acquire or per-key rebuild TTL)

## Code tiers
### ❌ Bad
```python
def product_list(request):
    return render(request, "x.html", {"products": Product.objects.all()})
# DB hit on EVERY request; caching added later "somewhere"
```
### ✅ Good
```python
def product_list(request):
    key = f"product_list:{request.LANGUAGE_CODE}:{page}"
    if cached := cache.get(key): return cached
    html = render(...db call...)
    cache.set(key, html, timeout=300)
    return html
```
### ⚡ Better
```python
# Cache-Control headers for browser/CDN (api/http-caching) + per-view TTL
# version baked in key (schema change = new key, no purge)
# + audit invalidation event hooks (order saved → delete/refresh order keys)
```
### 🏆 Excellent
```text
# cache strategy doc: view/cache levels chosen per profile; hit-rate dashboards
# stampede guard: rebuild-in-async + short-ttl graceful
# cache busting far-future for static; invalidation tests (edit → see new data)
# per-tenant keyspace isolation; cache warm on deploy (avoid cold start SLO crunch)
```

## Failure modes
- caching user-specific pages under public key (info leak!)
- TTL too long → stale UX complaints; no side-effect writes/refetch
- invalidation missing entirely (new code path deadkeys)
- query caching with mutable objects (corrupted state)

## Evidence
- Django cache docs (VERIFIED), caching/ROOT cross-refs