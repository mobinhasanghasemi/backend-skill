# Data Warehouse Modeling (dbt, star semantics)

## Identity
- ID: data-engineering.warehouse
- Type: concept
- Status: active
- Importance: medium

## Purpose
Model warehouse data for fast, trustworthy reports: normalized facts + dimensions, incremental updates, and the semantic layer the business queries.

## Model levels (Kimball/dbt-standard)
```
raw (landing, near source)  →  staging (typed, deduped, cleaned)  →  
marts (facts + dimensions, business semantics) → reports/exports
```

## Facts vs dimensions (the mental model)
- **Fact**: measurements (orders rows: count, total, date, FK keys) — bulky, additive
- **Dimension**: attributes (user, product, region) — small, high cardinality
- Star schema joins: fact × dims — fast, predictable aggregations

## Incremental mechanics (the 2026 way)
- **Incremental model** (dbt): materialized='incremental', unique_key on natural key; `is_incremental()` → WHERE new watermark
- **Snapshots (SCD2)**: type-2 change history dims (audit, point-in-time)
- **Backfills**: rebuild partition with restore-from-source; never double count
- **Reconciliations**: (source sum == mart sum daily) gate for money

## Code tiers
### ❌ Bad
```sql
-- select * from prod.orders  (yesterday's full copy, no dedupe)
```

### ✅ Good
```sql
{{ config(materialized="incremental", unique_key="order_id") }}
SELECT order_id, total, user_id, created_at
FROM {{ source("replica", "orders") }}    -- replica, not prod writes
{% if is_incremental() and var("full_refresh", false) is false %}
WHERE created_at >= (select coalesce(max(creation_day), '1900-01-01') from {{ this }})
{% endif %}
```

### ⚡ Better
```yaml
# catalog.yml: 
#   orders_daily: description; tests: unique(order_id), not_null(...)
# timestamps: loaded_at server_time UTC; first of month contract
```

### 🏆 Excellent
```text
# semantic layer (dbt metrics / canvas): revenue, GMV with definitions frozen
# missing_or_delayed alerts if daily mart not refreshed by 06:00
# lineage: business question → upstream tables → source (visible chain)
# money reconciliation zero-diff daily; storage tiering; retention policy
# data quality dashboard: tests run/fail, freshness, coverage by owner
```

## Failure modes
- full scans on big fact tables (no partitioning/ordering)
- unique_key mistakes → duplicates with no error (!!!)
- metric defined in SQL per consumer (drifts across teams)
- no tests on marts (bugs live in the stakes)
- grain confusion: row-per-order vs row-per-item mixed in one fact table

## Evidence
- dbt docs + Kimball "The Data Warehouse Toolkit" (VERIFIED, SUPPORTED)