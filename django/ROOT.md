# DJANGO — ROOT NEURON

## Identity
- ID: django.root
- Domain: django
- Type: root
- Status: active
- Importance: critical (the flagship vertical of this skill: Django + DRF + PostgreSQL + Celery + Redis)

## Purpose
Django-specific engineering: ORM patterns, safe migrations, DRF APIs, settings hygiene, caching, background jobs, admin, and the performance reality — with production discipline.

## Activation
- any Django project code: models, views, serializers, migrations, settings, admin, signals
- "this Django app is slow", "N+1", migration stuck, DRF API design

## Routing
```text
models/query perf   → orm.md (select_related, index, EXPLAIN bridge)
migrations          → migrations.md (zero-downtime expand/migrate/contract)
API layer           → drf.md (serializers, viewsets, throttle, pagination)
settings/deploy     → settings.md
background work     → messaging/celery.md (outbox, retries, idempotent jobs)
auth & permissions  → security/authentication.md + authorization.md (Django specifics)
admin               → admin.md (safe, read-only, actions)
caching             → django/caching.md (or caching/ROOT)
debugging slow      → performance/profiling.md + databases/optimization/ROOT
```

## Django truths (2026)
- **Django 5.2 LTS** (support until Apr 2028) — the production baseline; 6.x for new features (verify per version!)
- QuerySets are lazy — N+1 hides in serializers/templates; `select_related` (FK/O2O) vs `prefetch_related` (M2M/Reverse FK)
- **Migrations are the DB change tool**: safe = expand/migrate/contract with the DB (migrations.md)
- Signals: powerful, hard to test; avoid for business-critical side effects (prefer explicit service calls / outbox)
- Auth: Django built-in is good (password hashers, sessions); extend with JWT only when stateless needed (security/authentication.md)
- Admin: great tool, but it is a PUBLIC surface — restrict, read-only audit views for sensitive data
- Caching: per-view/per-template caching discipline (django/caching.md); Redis the default
- Logging/observability: integrate OTel (observability/*)

## Code tiers — a production Django view

### ❌ Bad
```python
def orders(request):
    return JsonResponse([{"user": o.user.username, ...} for o in Order.objects.all()])
# N+1 per order (user query each), unbounded list, no authZ, sync compute per row
```

### ✅ Good
```python
class OrderList(ListAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        return Order.objects.select_related("user").filter(customer=self.request.user)
```

### ⚡ Better
```python
# + pagination (cursor), + DRF throttling, + select_prefetch discipline,
# + serializer output DTO (never full model), + authZ policy module
```

### 🏆 Excellent
```
# queryset tuned to EXPLAIN; prefetch_related resolved; indexes on hot filters
# caching decorator on hot read view with invalidation (not blind TTL);
# async background work via Celery+outbox; full OTel trace; SLO per endpoint
# tests: contract + IDOR per endpoint (testing domain)
```

## Common failure modes
- N+1 in admin/serializers (order.track usage)
- migration locking prod tables at peak
- settings sprawl (12 settings files, env soup) — settings.md
- signals doing heavy work (DB hits in post_save during tests)
- admin exposed with default permissions
- DRF as God-layer doing business logic in views (service layer)

## Security
- Django security middleware defaults ON (CSRF, XSS, clickjacking); never disable casually
- SECRET_KEY env-only, never committed; DEBUG=False in prod ALWAYS
- authZ per object via policy (security/authorization.md); IDOR test suite

## Evidence
- Django docs 5.2 LTS + release process: VERIFIED via source-S-002 (accessed 2026-08)
- Practical Django patterns (two-scoops style): SUPPORTED (community practice, not official docs)