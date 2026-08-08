# HTTP Caching & Conditional Requests

## Identity
- ID: api.http-caching
- Type: procedure
- Status: active
- Importance: high

## Purpose
Serve repeated GETs from caches (browser, CDN, gateway, app cache) — correct semantics with headers, not ad-hoc caching in code.

## Core mechanisms
- `Cache-Control`: max-age, s-maxage (CDN), must-revalidate, no-store (auth/PII!)
- `ETag` / `Last-Modified` + `If-None-Match` / `If-Modified-Since` → 304
- Vary on content-negotiation (Accept, Accept-Language, tenant!)
- Validation vs expiration: expiring (max-age) vs revalidating (ETag)
- POST responses: never cached by default (must: Vary + explicit)

## Code tiers

### ❌ Bad
```python
# no cache headers anywhere → every request hits DB, mobile API slow, CDN useless
# or: Cache-Control: no-store on public read API (perf lost)
```

### ✅ Good — explicit policy per endpoint
```python
response = Response(data, headers={
    "Cache-Control": "public, max-age=300",   # public list: 5 min
    "ETag": f'"{hash(payload)}"',
})
# user-specific: "private, max-age=60"; auth: "no-store"  (or Vary: Authorization)
```

### ⚡ Better — conditional requests
```python
etag = f'"{version_ts}-{user_id}"'   # cheap fingerprint
if request.headers.get("If-None-Match") == etag:
    return Response(status=304, headers={"ETag": etag})
# → 90% traffic saved on unchanged resources; 304 cheap
```

### 🏆 Excellent
```text
- cache policy matrix in code (per resource: public/private, TTL, revalidation)
- CDN: s-maxage + Vary per variant; purge & invalidation plan (key-based purges)
- write-path invalidates keys (cache keyed, not only in DB)
- stale-while-revalidate for resilience (serve stale during refresh)
- metrics: cache hit rate per endpoint, 304 ratio, cache coverage; chaos: purge drill
- tests: 304 flow, Vary correctness, private/user isolation (no cross-user leak!)
```

## Failure modes
- caching auth'd responses without Vary → cross-user data leak (CRITICAL!)
- Cache-Control missing on dynamic endpoints → user sees stale data
- cache invalidation never defined → stale forever or purged everything
- ETag weak vs strong semantics mixed (weak for correctness, strong for performance)

## Security
- auth responses: `Cache-Control: no-store` or `private` + Vary; never share cache keys across tenants

## Evidence
- HTTP caching semantics: VERIFIED via source-S-030 (RFC 9111)
