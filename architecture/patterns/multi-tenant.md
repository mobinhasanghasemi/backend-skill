# Multi-Tenant Architecture

## Identity
- Type: pattern
- Importance: medium
- ID: architecture.patterns.multi-tenant
- Domain: multi-tenancy (detailed neuron there)
- Status: active

## Purpose
One application serving multiple customers (tenants) with data isolation and shared infrastructure.

## Concept
Determine **isolation level** per data: shared table w/ tenant_id / schema-per-tenant / DB-per-tenant. Full analysis in multi-tenancy/ROOT + databases/postgresql/rls.md (RLS as DB backstop).

## Activation Conditions (high-level)
- SaaS for multiple customers
- any request honoring a tenant context

## Do Not Activate When
- single-tenant private deployments (isolation not needed)

## Critical checklist (top of mind)
1. IDOR/tenant leak prevention — every query scoped by tenant (ARCH014, ARCH025!)
2. cache: keys must be tenant-scoped (ARCH025)
3. background jobs: tenant context preserved
4. backups: per-tenant sensitive (or restore per tenant)
5. observability: tenant dimension (cost, quota)
6. billing boundaries

## Trade-offs of models
| Model | Cost | Isolation | Scale |
|---|---|---|---|
| shared | low | low | high |
| schema | med | med | med |
| db-per | high | high | low-ish |

## Failure Modes
- cross-tenant data leak (CRITICAL — ARCH014)
- per-tenant quota misuse
- migration per tenant (schema changes × tenants)
- noisy neighbor (shared)

## Security — the isolation is the security; read multi-tenancy/ROOT BEFORE designing.
## Performance — index tenant id high; columnar stats per tenant; request budgets per tenant
## Reliability — one tenant's states don't take others down (black neighborhoods in shared)
## Observability — per tenant metrics; alert cross-tenant anomaly

## Evolution Path — start shared table with strong RLS; move tenants up only when measured

## Evidence — SaaS multi-tenancy patterns (VERIFIED); isolation decisions per scale