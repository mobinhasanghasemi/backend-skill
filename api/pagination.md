# Pagination, Filtering & Sorting

## Identity:
- **ID: api.pagination
- Type: procedure
- Status: active

## Purpose
Serving potentially large lists safely and efficiently: bound a query, allow traversal, keep the API predictable, and avoid slow deep-offset jumps.

## Options
| Approach | When | Notes |
|---|---|---|
| **Offset/limit** | small sets (<10k), admin tools | O(N) skip; page drift on writes |
| **Cursor (keyset)** | live data, big tables | stable pages; order by unique+stable key |
| **Cursor (opaque token)** | most APIs | decouples, cache-safe, search |
| limit cap (100) • link header (next) or JSON envelope | |

Deep pagination pitfalls: `OFFSET 1000000` = slow scan; concurrent writes alter pages — keyset fixes.

## Code tiers

### ❌ Bad
```python
items = queryset[offset:offset+limit]  # unbounded by default, no keyset, no cap
# → deep offset scans, page drift on writes
```

### ✅ Good (DRF-style, capped)
```python
class LargeListPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100
# plus: "next"/"count" in response
```

### ⚡ Better — cursor pagination
```python
class CursorPagination2(CursorPagination):
    ordering = ("-created_at", "id")   # stable total order
```
keyset: `WHERE (created_at, id) < (:last_created, :last_id) ORDER BY ...` — O(1) pages, close on live writes.

### 🏆 Excellent — full stack
```python
# cursor + limits + filters validated
class CursorPagination ... ordering=("id",)  # unique+stable
@app("/items")
def items(request):
    filters = validate_filters(schema=ItemFilter, data=request.query)  # whitelist
    qs = Item.objects.filter(**filters)
    page = paginate(qs, cursor)
    return {"items": page, "cursor": page.next_cursor()}
# + Cache-Control or ETags on staleness-capable lists; our ops inverted
```

## Filtering/Sorting rules
- Whitelist filter fields (never user-triggered raw SQL ordering)
- Sorting keys must be index hand-holds (do not sort on N random cols)
- Expose count only when needed (COUNT(*) can be expensive)

## Failure modes
- unbounded lists (memory, DB event), cursor encoding breaks (token maturity), filters undisclosed to clients, invalid fields ignored silently instead of 422

## Security
- filters never allow visibility over scope (tenant leak via blind filter) — tie to authZ

## Observability
- pages: p95 of list endpoints, max page size, top filter field usage

## Evidence
- Pagination techniques (offset vs cursor): SUPPORTED practice
