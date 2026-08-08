# Django REST Framework (DRF) API Layer

## Identity
- ID: django.drf
- Type: discipline
- Status: active
- Importance: critical

## Purpose
Design robust DRF APIs: serializers as contracts, viewsets as discipline, pagination/throttling/versioning wired — while keeping business logic in services (not views).

## The DRF contract stack
1. **Serializers** = validation + representation: `ModelSerializer` for basics, explicit `fields`, nested read-only carefully (N+1!), `create/update` in serializer vs service call
2. **Views/Viewsets**: `ModelViewSet` default excluded operations (custom mixins), `get_queryset` scoping per user/tenant
3. **Pagination**: PageNumber/Cursor (api/pagination.md) — never unbounded
4. **Throttling**: per-user/per-IP scopes (api/rate-limiting.md)
5. **Versioning**: URL or header policy decided (api/versioning.md) — drf versioning built-in
6. **Errors**: uniform Problem+JSON (api/error-design.md) — DRF exception handler override
7. **OpenAPI**: drf-spectacular generation + contract tests (testing/contract-tests.md)

## Service layer pattern (the missing 3rd layer)
Thin view → service that owns rules + transactions:
```python
class OrderService:
    @transaction.atomic
    def create(self, user, data) -> Order:
        order = Order(user=user, **data)
        order.save()
        Outbox.create("order.created", order)   # outbox.md
        return order
```
Views = serialization + authZ; services = domain rules; models = data.

## Code tiers
### ❌ Bad
```python
class OrderViewSet(ModelViewSet):           # exposes delete/create/list with NO
    queryset = Order.objects.all()          # scoping: any user lists/edits all orders!
    serializer_class = OrderFullSerializer  # returns full model incl. internal fields
```

### ✅ Good
```python
class OrderViewSet(ReadOnlyModelViewSet):   # narrowed
    serializer_class = OrderOutSerializer
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).select_related("user")
```

### ⚡ Better
```python
# - permission policy + object-level checks (authorization.md policy module)
# - throttling scopes (anon login > user ops), pagination fixed (cursor)
# - serializer output DTO: explicit fields (never full model), computed at service
```

### 🏆 Excellent
```text
# - contract tests + OpenAPI auto-generated + page response envelope stable
# - idempotency keys on writes (POST charge w/ key header) — api/idempotency.md
# - error shape RFC9457 with machine codes; trace_id in errors + logs
# - load test p95 budget; caching decorators on the read paths that earn it
# - services tested unit; views integration; contract frozen between versions
```

## Failure modes
- ModelViewSet default = full curl surface (BOLA!)
- serializer exposing internals (`fields = "__all__"` on sensitive)
- no throttling on auth/write endpoints
- versioning ignored ("we'll just change JSON")
- business logic in views (untestable, coupling to HTTP)

## Evidence
- DRF official docs (VERIFIED via source-S-004); drf-spectacular docs (VERIFIED, repo)