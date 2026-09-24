# Django ORM Performance

## Identity
- ID: django.orm
- Type: discipline
- Status: active
- Importance: critical

## Purpose
Write Django querysets that are correct AND fast: kill N+1, use the right join, build indexes that serve the queries, and verify with EXPLAIN — not vibes.

## The N+1 family (the #1 Django sin)
| Pattern | Fix |
|---|---|
| `for o in Order.objects.all(): o.user.name` | `select_related("user")` (JOIN, FK/O2O) |
| `o.items.count()` in loop / M2M access | `prefetch_related("items")` (second query, gathered) |
| serializer field calling related | serializer `select_related`/`prefetch` on queryset |
| `count()`/`exists()` inside loop | aggregate ONCE (`annotate`, `Count`) |

## The query-shape toolbox
1. `values()`/`values_list()` for projection (no model instantiation)
2. `annotate()` (aggregate per row), `aggregate()` (whole set)
3. `only()`/`defer()` rare (serializers + index-only still better)
4. `iterator()` for streaming large sets (memory)
5. `.exists()` vs `.count()` vs `.all()` — exists skips fetching rows
6. `select_related` chains vs multiple `prefetch_related` — count round-trips

## Indexes for Django
- `db_index=True` / Meta.indexes — for **hot filters/joins** (data-modeling.md)
- Composite/functional indexes when WHERE uses `lower()`, etc. (indexing.md)
- FK fields: index where the query actually filters/orders (not automatically — audit report noted PG doesn't auto-index FK!)

## Code Tiers
<!-- executable -->
### ❌ Bad
```python  <!-- illustrative -->
def order_summaries(user_id):
    orders = Order.objects.filter(user_id=user_id)
    return [{"id": o.id, "user": o.user.email, "items": o.items.count()}
            for o in orders]
# 1 + N (user) + N (items count) = 1 + 2N queries!
```

<!-- executable -->
### ✅ Good
```python
orders = (Order.objects.filter(user_id=user_id)
          .select_related("user")
          .annotate(items_count=Count("items", distinct=True)))
# 2 queries total: one JOIN user, one COUNT GROUP BY — VERIFIED via S-001
```

<!-- executable -->
### ⚡ Better — query-shaped for the serializers
```python
# serializer needs: order + user + first 3 items
orders = orders.prefetch_related(
    Prefetch("items", queryset=Item.objects.order_by("-created_at")[:3]))
```

<!-- executable -->
### 🏆 Excellent — verified
```python
# 1. count queries before/after (assertion test: assertNumQueries!)
# 2. EXPLAIN (ANALYZE) the top queries; indexes on the filtered cols
# 3. performance test: 1000 orders < 10 queries total
# 4. cache only the hot path (caching/ROOT) — after query shape
from django.test import TestCase
class OrmTest(TestCase):
    def test_queries(self):
        with self.assertNumQueries(2):
            list(order_summaries(user_id=1))
```

## Failure modes
- `prefetch_related` on huge sets (second query huge — filter prefetch queryset)
- `Count` distinct explosion (join multiplication — check with `.query`)
- index on non-selective columns alone
- values() destroying serializer contract (test still green)
- `.iterator()` with prefetch (silently loads all) — documented Django gotcha!

## Evidence
- Django docs (querysets/prefetch) VERIFIED; EXPLAIN bridging (databases neurons)