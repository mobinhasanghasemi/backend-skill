# REST API Design

## Identity
- ID: api.rest
- Domain: api
- Type: discipline
- Status: active
- Importance: critical

## Purpose
The dominant contract of web APIs: resources, methods, status codes, conventions — stamped with honesty about HATEOAS and versioning.

## Core concept
- **Resources** named by nouns; operations by HTTP methods (GET read, POST create, PUT/PATCH update, DELETE)
- Status codes as semantics (200/201/204/400/401/403/404/409/422/429/500)
- Headers carry metadata (cache, auth, rate limit, correlation-id)
- 1 API of today: JSON over HTTPS; versioning via URL or header (decision!)

## Activation
- new API; API review; contract style question
- When NOT: bulk streaming/binary heavy (→ protobuf=gRPC); heavy querying flexibility (→ GraphQL)

## Decision rules (trim)
1. Methods: PUT vs PATCH — PATCH for partial, PUT full replace (choose & document!)
2. Idempotent POST: use idempotency keys for non-idempotent writes (idempotency.md)
3. Pagination: cursor-based for live data, offset for simple lists — early decision
4. Sorting/filtering: whitelist fields — never pass raw to SQL
5. Validation on input → 422 with per-field errors; symmetric error shape everywhere

## Code tiers — the API endpoint ladder

### ❌ Bad
```python
@app.post("/order")
def create():
    # no idempotency, no validation, errors "unknown", interacts DB
    order = Order.objects.create(amount=request.json["amount"])  # unvalidated
    return {"ok": True}          # ambiguous status; no HATEOAS-ish signals
```

### ✅ Good
```python
class OrderSerializer(serializers.Serializer):
    amount = DecimalField()  # required, validated
    ...
@api_view(["POST"])
def create_order(request):
    s = OrderSerializer(data=request.data)
    s.is_valid(raise_exception=True)
    order = s.save(user=request.user)   # auth from context
    return Response(order.to_json(), status=201, headers={"Location": order.url})
```

### ⚡ Better
<!-- illustrative: IdemStore/transactional_create are shapes, not library calls -->
```python
# idempotency via header + rate limiting + uniform errors (problem+json)
@api_view(["POST"])
def create_order(request):
    key = request.headers.get("Idempotency-Key")
    if key and (existing := IdemStore.get(key)):
        return Response(existing, status=200)        # replay-safe
    s = Serializer(data=request.data); s.is_valid(raise_exception=True)
    order = transactional_create(s, idem=key)        # IdemStore within same tx (outbox note!)
    return Response(order.as_json(), status=201, headers={"Location": f"/orders/{order.id}"})
```

### 🏆 Excellent — production shape
```text
OpenAPI spec committed → generated client/types + contract tests agains the spec
Problem+JSON errors (RFC7807) with stable machine codes; per-field issues
idempotency: key hash stored with status; replay returns original
pagination: cursor (before/after) + limit; sort/filter whitelist
rate limits: per-API-key/user tokens (429 with Retry-After)
ETag/If-None-Match for GET evalability, conditional PATCH for multi-user edits
authz at object level in EVERY read/write handler (IDOR test suite, 401/403/404 blending)
p99 latency budget per endpoint declared + dashboards
```

## Anti-patterns
- 200-with-error-object ("success": false)
- unbounded GET /users (ARCH030)
- nesting every relation (shallow lists + detail links)
- PUT for reversible non-idempotent service action (external POST only)

## Version updates
## Performance
- Measure first: EXPLAIN (ANALYZE, BUFFERS) for query shape; pg_stat_statements for hot queries (S-044/S-047). No index/cache without measurement per PERFORMANCE_ENGINE.
- p95/p99 before/after; one change at a time.

## Reliability
- Timeouts on DB/client, retry with jitter + idempotency, backup/PITR tested monthly (S-046), RPO/RTO defined.
- Failure: pool exhaustion -> shed load, replica lag -> read-your-writes check.

## Evidence
- Fielding thesis/REST constraints (VERIFIED theory), API guidelines (REST SteveZ etc. — SUPPORTED practice)