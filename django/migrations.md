# Safe Django Migrations (zero-downtime)

## Identity
- ID: django.migrations
- Type: procedure
- Status: active
- Importance: critical

## Purpose
Change the schema while users still use the system — the expand/migrate/contract rhythm in Django, with lockouts, backfills, and rollbacks handled.

## The expand → migrate → contract pattern
1. **Expand**: add nullable column/new table/index + `RunPython` only for NEW code (old code ignores)
2. **Migrate**: backfill data in batches (NOT one giant UPDATE; batch with keyset + sleep), then flip
3. **Contract**: drop the old column/table after the dual-write period (confirm both code paths gone)

## Django mechanics (the correct mental model)
- Migrations = sequential operations; `atomic = False` needed for table-altering ops on large tables (DDL locks!)
- PG: `ALTER TABLE ADD COLUMN` with DEFAULT is fast in PG11+ (no rewrite); PG11+ no full-time DDL blowup; but `NOT NULL` + DEFAULT on huge table = lock risks — add nullable, backfill, `SET NOT NULL` (contract)
- `RenameField`/reorder ops = reconstrained (with 500M rows: separate migrations)
- CI: `makemigrations --check` (no drift), migration tests run on fresh+prod-shape DB

## Code tiers
### ❌ Bad
```python
# migration that:
# 1) adds NOT NULL column without default on 500M rows (locks/rewrites)
# 2) or: RenameField (table rebuild on lock)
# 3) backfill in one UPDATE (hours of checker + locks)
```

### ✅ Good — expand/backfill/contract example
```python
# 0007: add nullable column (fast on PG)
AddField(Order, "external_id", models.UUIDField(null=True))
# 0008 (backfill job, not migration): batched keyset update
while rows := Order.objects.filter(ext_id=None).order_by("pk")[:1000]:
    for o in rows: o.external_id = make_id(o); o.save(update_fields=["external_id"])
# 0009: contract
   AlterField(Order, "external_id", null=False)     # PG fast now (rare nulls)
# DROP old col LAST, code already deployed
```

### ⚡ Better — zero-downtime patterns
```python
# - indexed_operations with separate backfill job (Celery) + idempotent reruns
# - keep old+new code N versions (deployments are horizonless)
# - read replicas during migrations (read path unblocked)
# - lock_timeout + statement_timeout on migration DB sessions
```

### 🏆 Excellent
```text
# migration drill (staging: copy prod shape 500M rows; migration in < 5m; soak test)
# CI assertNumQueries/migration count check; DB locking alert during tue release
# runbook: migration halted (lock) → checklist; rollback plan per migration file
# every migration = PR with: peak-of-scale data shape test, RTO note, dual-write period
```

## Failure modes
- long BACKFULL (single UPDATE)
- NOT NULL+default on big table
- adding FK causing check lock
- deploy order violation (code expects column before migration)
- dropping column still used by old nodes (dual-write window)

## Evidence
- Django migrations docs (VERIFIED); PG DDL lock behavior (postgresql neurons)