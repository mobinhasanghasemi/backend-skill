# Row vs Schema vs Database — Tenant Isolation

## Identity
- ID: multi-tenancy.row-vs-schema-vs-db
- Domain: multi-tenancy
- Type: pattern
- Status: active
- Importance: critical
- Last Verified: 2026-08

## Purpose
Choose isolation model for B2B SaaS: row (shared table), schema-per-tenant, or database-per-tenant — with cost, leak blast radius, and migration trade-offs.

## Core Concept
Isolation = how strongly a missing `tenant_id` filter can leak. Row is cheapest, schema adds DDL isolation, DB adds physical isolation. Stronger isolation costs more in migrations, connections, and ops.

## Activation Conditions
- SaaS with >10 tenants, compliance requiring tenant wall, or IDOR risk (ARCH014)
- Decision: new SaaS data model or hardening existing shared-table model

## Do Not Activate When
- Single-tenant product or tenant count <5 with no compliance wall

## Decision Rules
- **Row (shared)** if tenants <1000, RLS possible, migration cost must stay low; enforce `tenant_id` + RLS second wall (S-048) + per-tenant cache keys (ARCH025).
- **Schema-per-tenant** if tenants 100–2000, need per-tenant extensions/backups, can afford `search_path` + migration fan-out.
- **Database-per-tenant** if tenants <100, regulatory per-tenant DB, or noisy-neighbor must be zero — accept connection pool × N and backup × N.

## Trade-offs
| Model | Leak resistance | Migration cost | Connection cost | Backup |
|---|---|---|---|---|
| Row | app bug = leak (needs RLS) | 1 migration | 1 pool | one |
| Schema | DDL isolates | N migrations (fan-out) | 1 pool + search_path | per-schema dump |
| DB | physical | N DBs | N pools | N |

## Security
- Row: RLS `USING (tenant_id = current_setting('app.tenant_id')::uuid)` (S-048) + app filter; test IDOR per endpoint; cache keys must embed tenant (ARCH025).
- Schema/DB: connection must set tenant context atomically; no `search_path` injection.

## Performance
- Row: add composite index `(tenant_id, id)` first; RLS qual ~3% overhead (measure EXPLAIN).
- Schema/DB: connection overhead dominates; use pgbouncer transaction mode.

## Reliability
- Row: one backup, RPO single; schema/DB: per-tenant PITR possible but restore drills × N.

## Evidence
- PG RLS docs VERIFIED via S-048 (accessed 2026-08); shared vs isolated trade-offs SUPPORTED via architecture/patterns/multi-tenant.md and S-048.

## Confidence
SUPPORTED

## Verification Status
Procedure validated against PG docs and existing multi-tenancy/ROOT.md.

## AI Instructions
Always ask tenant count, compliance class, and migration budget before recommending; default to row+RLS and justify stronger isolation explicitly per SIMPLICITY_GOVERNOR.

## Code Tiers
<!-- executable -->
```sql
-- row+RLS (defense in depth)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders USING (tenant_id = current_setting('app.tenant_id')::uuid);
-- app must: SET LOCAL app.tenant_id = '...'; SELECT * FROM orders; -- tenant already filtered
```

## Questions To Ask
1. Tenants now / 18mo?
2. Compliance: must tenants be physically separate?
3. Migration budget and ops team size?
