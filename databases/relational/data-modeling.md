# Data Modeling

## Identity
- ID: databases.relational.data-modeling
- Domain: databases
- Type: knowledge
- Status: active

## Purpose
The discipline of shaping a schema (tables, columns, constraints, keys) to reflect the *domain* and the *queries* — trade: correctness-first, then performance-sensitive.

## Core Concept
1. Identify **entities** (nouns) and **relationships** (verbs) from the domain
2. Build **normalized** model (3NF) with FKs and uniqueness making invariants expressible
3. After queries exist: **denormalize only hot* read paths* with a measured justification
   Optional: materialized views, generated columns, JSONB for document-like parts

## Mental Model
A museum that stores every original once (normalized), and hangs pre-organized exhibit copies (denormalized/projection) where foot traffic demands speed.

## Decision Rules
- Every column: type (Postgres: use correct types: uuid, timestamptz, numeric not float for money)
- **PK strategy**: for PG: `BIGINT GENERATED ALWAYS AS IDENTITY` (now prefer `uuidv7()` in PG18 for ordering) vs UUIDv4 (random index fragmentation trade) — decision table:
  - internal only: bigint identity
  - external exposure / security (avoid enum ID users) → uuid v7 (PG18 native) preferred
- **FKs**: balance — model integrity via FKs (catch coding errors), index feedback paths where queried
- **Timestamps**: audit columns (`created_at`, `updated_at`, soft-delete `deleted_at` considered — soft vs hard delete: audit column when needed, else hard)

## Code Tiers (the progression in schema craft)

### ❌ Bad — the typical-but-wrong move
```sql
-- No constraints: duplicate emails, orphan orders
CREATE TABLE users (id serial, email text);
CREATE TABLE orders (id serial, user_id int, total float);
-- float for money; orphanable user_id; dup emails guaranteed
```

### ✅ Good — correct integrity
```sql
CREATE TABLE users (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email TEXT NOT NULL UNIQUE);
CREATE TABLE orders (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users (id),
  total NUMERIC(14,2) CHECK (total >= 0),
  created_at timestamptz NOT NULL DEFAULT now());
CREATE INDEX ON orders (user_id);
```

### ⚡ Better — thinking about reads / scale
```sql
CREATE TABLE orders (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users (id) ON UPDATE CASCADE,
  total NUMERIC(14,2) NOT NULL CHECK (total >= 0),
  status TEXT NOT NULL DEFAULT 'pending'
      CHECK (status IN ('pending','paid','cancelled','refunded')),
  created_at timestamptz NOT NULL DEFAULT now());
-- composite index for the hot query "user's recent orders"
CREATE INDEX idx_orders_user_created
  ON orders (user_id, created_at DESC);
```

### 🏆 Excellent — production-shaped
```sql
-- PG18: uuidv7 keeps time ordering, external-safe ids
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT uuidv7(),
  user_id bigint NOT NULL REFERENCES users (id),
  total NUMERIC(12,2) NOT NULL CHECK (total >= 0),
  version INT NOT NULL DEFAULT 0,       -- optimistic locking for money paths
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','paid',...)),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);
-- partitioning-ready when rows grow (see partitioning.md)
```
Why Excellent: type-correct, ordered ids for index locality, defensive constraints, optimistic-lock column, ready-to-partition.

## Migration Guidance
- forward-only schema migrations with full rollback story (see django/migrations or raw SQL eval)
- backfill in batches with resumable state

## Failure Modes
- denormalization before measurement (inconsistent ghosts)
- FK keys with no supporting index → phantom slow joins
- Text-based enums vs proper types
- floating point for money

## Observability
- model-level: constraints → no anomaly; monitor FK-heavy keys
- metrics: row churn per table; HOT update; bloat

## Performance
- Measure first: EXPLAIN (ANALYZE, BUFFERS) for query shape; pg_stat_statements for hot queries (S-044/S-047). No index/cache without measurement per PERFORMANCE_ENGINE.
- p95/p99 before/after; one change at a time.

## Reliability
- Timeouts on DB/client, retry with jitter + idempotency, backup/PITR tested monthly (S-046), RPO/RTO defined.
- Failure: pool exhaustion -> shed load, replica lag -> read-your-writes check.

## Evidence
- Normalization theory VERIFIED; PG18 uuidv7 from release notes VERIFIED-SUPPORTED