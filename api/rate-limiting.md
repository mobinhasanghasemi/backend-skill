# Rate Limiting

## Identity
- Build: ID: api.rate-limiting
- Type: procedure
- Status: active
- Protection: critical

## Purpose
Protect shared resources (APIs, auth, uploads) from abuse: burst, slow-olio, runaway clients — while keeping legit traffic unaffected. Limit = permission for clients; design must be explicit.

## Core concepts
- **Identifier**: API key / user / IP (IP alone can punish shared NATs) 
- **Limit types**: fixed window (simple, edges), sliding window/log (fair), token bucket (burst-safe) — pick per endpoint
- **Response**: 429 with `Retry-After`; draft standard `RateLimit-*` headers
- **Deployment**: middleware-level at gateway (fast) + application check for business rules
- gate only what matters: auth endpoints/expensive endpoints; then whole API

## Code tiers

### ❌ Bad
```python
# no limit at all → auth endpoint brute-forced:
# 1000 requests/minute just passwords; or: DB write hammer
```

### ✅ Good — middleware (fixed window, Redis)
```python
bucket_key = f"rl:{scope}:{user_id}:{window_start}"
count = r.incr(bucket_key); r.expire(bucket_key, window)
if count > limit: raise RateLimitError(limit, retry_after)
```

### ⚡ Better
```python
# token bucket: smooths bursts, no false 429
# per-endpoint policies (login: 5/min/IP; writes: 100/min/user)
```

### 🏆 Excellent
```text
- RateLimit-* headers: RateLimit-Limit/Remaining/Reset (draft); Retry-After always
- key by API key when possible; per-IP fallback for anonymous; tenant-aware quota
- limits configurable per plan; enforced at edge (nginx/CDN) + app (defence in depth)
- 429 responses errors documented RFC7807 with Retry-After
- monitoring: 429 counts per bucket → alert abuse; allow temporary exemptions
```

## Failure modes
- IP-only limiting blocks legit office users (NAT)
- window reset burst (dead time at window edge)
- shared bucket degrading one umbrella of features into one client

## Notes
- decide down policy (keep mixing) explicitly; penalty pause vs limit
- load has a "hard limit" — clear communication in docs

## Observability
- metrics: rejected/s, bucket capacity vs usage alerts

## Evidence
- Rate limiting (token bucket / fixed window): SUPPORTED practice (algorithmic)
