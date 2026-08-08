# RELATIONAL DATABASES — ROOT NEURON

## Identity
- ID: databases.relational
- Type: root
- Status: active

## Purpose
Router for the relational family (PostgreSQL, MySQL, SQLite, MSSQL, Oracle): when they win, principles, and their shared mechanics.

## Activation Conditions
- relational data (references, joins, constraints)
- transactions (ACID), consistent reads
- structured queries

## Decision Rules (family level)

**Relational wins when:**
- data has meaningful relationships & joins
- transactions/consistency matter
- schema/constraints protect integrity (FK, unique, checks)
- queries vary (ad-hoc, flexible indexing)
- durability is a must (fsync-based)

**Consider NoSQL only when (relational fails):**
- very high write throughput w/ distributed key-value (cache/type.store)
- document shapes violate table schema churn (rare — PG JSONB now credibly covers)
- search/vector/media types, e.g., separate engine per concern (not instead of relational)

## Mandatory Questions (relational-specific)
1. Which engine? (PG/MySQL/SQLite by features: partial indexes, JSONB, full-text, geospatial, licensing, cloud)
2. Type volumes/retention before schema
3. What's the access path in 80% of queries? (design indexes around)

## Relational core principles
- **Normalization** (3NF) until a *measured* read path justifies denormalization
- **Transactions** for invariants that need atomicity
- **Queries** are the unit of performance (EXPLAIN is your doctor — with evidence)
- **Constraints enforce trust**; the application layer is a backstop, not a boundary

## Child Neurons
- data-modeling
- transactions (ACID, isolation)
- indexing (principles + access methods)
- performance via `optimization` parent

## Conflicts/Complements
- Complements: caching (reads), replication (availability), partitioning (size)
- Conflicts with: over-denormalization (write complexity), schema-less fashion (constraints loss)

## Failure Modes (family)
- lock waits / row lock escalation
- connection exhaustion
- slow migrations at scale
- index bloat / stale stats
- cascade of replays / replicas lag

## Observability
- slow query logs, lock waits, pool depth, replica lag, bloat metrics

## Evidence
- Relational theory mature (Codd normalization, isolation theory) — VERIFIED stable