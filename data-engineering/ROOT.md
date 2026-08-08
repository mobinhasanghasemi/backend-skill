# DATA ENGINEERING — ROOT NEURONON

## Identity
- ID: data-engineering.root
- Domain: data-engineering
- Type: root
- Status: active
- Importance: medium (when data products matter)

## Purpose
The data path for product + analytics: pipelines (batch/stream), warehouses, quality, and privacy — so reporting and ML features are built on trustworthy data, not copies piled in a corner.

## Activation
- ETL/ELT, data warehouse/lake, dashboards/analytics sources
- sync from prod DB to warehouse, event streams for analytics
- "we need data science/ML" (pair: AI backends)

## Routing
```text
batch pipelines   → batch-pipelines.md (airflow/dbt)
streaming         → streaming-pipelines.md (Kafka streams → warehouse)
warehouse         → warehouse.md (modeling: star schema, incremental)
analytics on prod → NEVER prod load! (replica/warehouse)
dataset privacy   → security/logging-and-privacy.md + compliance.md
```

## Law one
**Never query the production OLTP DB for analytics/dashboards** — replicas/read followers (databases/postgresql/replication), then warehouse for heavy. ANALYTICS queries kill the airline on booking day: that's ARCH031 in the wild.

## Batch fundamentals
- Idempotence: load = full snapshot per partition or UPSERT with a dedupe key (never blind append)
- Watermarks and backfill: runbooks for reprocessing (from timestamp)
- Watermarks & backfill: runbooks for reprocessing (from timestamp)
- Testing: pipeline data contract tests (schema + counts) + reconciliation (source vs target count for money tables: the reconciliation must be in pipeline)

## Code tiers on the pipeline (airflow/dbt pseudo)
### ❌ Bad
# raw SQL dump weekly; replaces whole tables; no dedupe → double counting
### ✅ Good
# airflow: daily dbt job; source: replica snapshot; incremental imports (app-side idempotent)
# dbt: tests not null, unique, relationship; backfill
### ⚡ Better
# dbt staging/model layers (stg → models → marts); incremental materialization; partition pruning
# observability: freshness tests per table (insights "last_loaded" asserts)
### 🏆 Excellent
# orchestration SLA: pipeline p95 < SLO; runs recorded audit; lineage landscape
# reconciliation vs source for header/payment rows daily: zero diff = gate
# streaming: kafka → Flink/materialized views → warehouse (at-least-once + idempotent sink)
# retention policy, privacy rules (PII in data lake = violation of controls)

## Anti-patterns
- warehouse := "dump prod DB into bigquery" (no model, no tests)
- pipeline with internal failure storms (retries without idempotence)
- no owner for a table (failed schema drifts)
- dashboards against prod (fail its own load test)

## Evidence
- dbt/airflow docs (VERIFIED), warehouse modeling standard (Kimball) supported