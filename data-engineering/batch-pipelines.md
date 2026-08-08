# Batch Pipelines (Airflow/dbt/Spark)

## Identity
- ID: data-engineering.batch-pipelines
- Type: procedure
- Status: active
- Importance: high

## Purpose
Scheduled data jobs done right: idempotent, incremental, testable, observable — the machine behind dashboards and ML features.

## Core laws (the batch Bible)
1. **Idempotent runs**: replay a day = same output (full-replace per partition or UPSERT on natural key; never blind append)
2. **Incremental by watermark**: `WHERE updated_at > last_watermark`; watermark stored with the run (retry-safe)
3. **Tests at each stage**:
   - source schema check (columns exist, types)
   - row/volume sanity (delta vs history — anomalies alert)
   - referential + money reconciliation (sum check source vs target daily)
4. **Observability**: DAG duration, record counts, freshness (source latest ts vs today), failures alerting; lineage (source → stage → mart)
5. **Deterministic**: run in CI on fixtures; no timezomes implicitly

## The dbt-shaped transform layer (2026 typical)
```
raw (landing) → staging (clean, typed, deduped) → marts (business semantic)
```
- `dbt test`: not_null, unique, relationships, accepted_values, custom data tests
- `dbt snapshots` for type-2 churn; `dbt run --select +model` incremental

## Code tiers
### ❌ Bad
```sql
CREATE TABLE weekly_orders AS SELECT ... FROM prod.orders;   # queries RUNNING PROD!
# no dedupe, no incremental, no tests, full daily
```

### ✅ Good
```dbt
{{ config(materialized='incremental', unique_key='order_id') }}
SELECT order_id, user_id, total, created_at
FROM {{ source('replica', 'orders') }}          -- replica! never prod
{% if is_incremental() %} WHERE created_at > (SELECT max(created_at) FROM {{ this }}) {% endif %}
-- + tests: unique/not_null on order_id
```

### ⚡ Better
```python
# DAG with retries (3, exponential), catchup=False, SLA alert (DAG run +2h)
# backfill runbook: `--full-refresh` uses partition-replace; freshness checks assert
```

### 🏆 Excellent
```text
# lineage (openlineage/dbt web) so report question → upstream defs
# reconciliation job: money tables = sum(source) == sum(target) ± drift, failing loudly
# two envs (dev/prod), CI test run on each PR (dbt compile+test)
# SLA per production report: freshness threshold alert; fatal on breech
# data quality metrics dashboard: tests, unique violations, reconciliation diffs
```

## Failure modes
- transformer query hits production (arch fire)
- idempotence assumed (duplicate rows hide in aggregates — money!)
- no freshness SLA (report silently stale)
- full-refresh on 1B rows as a habit
- data contract drift unprotected (schema changes break marts silently — schema tests!)

## Evidence
- dbt docs, Airflow docs (VERIFIED), Kimball modeling (SUPPORTED)