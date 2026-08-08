# DATABASE OPTIMIZATION — ROOT NEURON

## Identity
- ID: databases.optimization
- Type: root
- Domain: databases
- Status: active

## Purpose
The systematic route from "database slow" to "query proven fast": optimize in evidence order, handle read/write paths, profile at the right abstraction.

## Routing
- slow query → query-optimization.md (EXPLAIN / pg_stat_statements)
- engine tuning → performance-tuning.md (settings, vacuum, pools) — AFTER queries
- read pressure → caching/strategies + postgresql/replication (in that order!)
- write pressure → indexing + partitioning → sharding (last)

## Optimization order (critical, evidence-driven)
1. **Queries first** (they generate I/O; index/EXPLAIN)
2. **Schema second** (types, denormalization leverages, keys)
3. **Engine settings third** — only after measuring against queries
4. **Infra fourth**: replicas, cache, partition, shard

"Database is slow" almost always hides "a query is slow" or "pool exhausted" — diagnose before you size.

## Attention
- query-optimization: HOT (most common)
- performance-tuning: when pools/hits verified

## Evidence — methodology (SUPPORTED: SRE/DB community), tuning content VERIFIED per feature docs