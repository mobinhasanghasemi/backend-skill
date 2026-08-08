# PostgreSQL Row-Level Security (RLS)

## Identity
- ID: databases.postgresql.rls
- Type: discipline
- Status: active
- Importance: medium-high (multi-tenant backstops)

## Purpose
Enforce row visibility **inside the database**: every query (any code path) is filtered by policy — the safety net under application authZ. Use as the LAST LINE of defense, not the only one (authorization.md remains primary).

## Mechanics
```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY orders_tenant ON orders
  USING (tenant_id = current_setting('app.tenant_id')::bigint);
-- app sets: SET LOCAL app.tenant_id = ... inside the transaction
```
- policy forced for ALL users (even table owner) unless `FORCE`d explicitly
- `USING` (read filter) vs `WITH CHECK` (write constraint — violation = error!)
- `app.tenant_id` set per request (in the same transaction/connection): never leave default (deny cluster)
- superuser bypasses RLS — connect as least-privilege role

## When RLS wins
- any multi-tenant system: defense-in-depth so a forgotten filter can't leak rows
- migrations/background jobs run as specific tenant scope (defer scope)
- tests prove: selector WITHOUT setting → zero rows (deny by default)

## Code tiers
### ❌ Bad
# app-only filter (queryset), DB open: one SQL typo / future ORM path / script = leak
### ✅ Good
```sql
ENABLE ROW LEVEL SECURITY; -- + tenant policy with WITH CHECK
-- app sets scope per request (transaction), connection is short
```
### ⚡ Better
# per-tenant ROLES/permissions on JSONB needs careful docs; policy on SET missing
# fallback: policy that reads request context set once per tx (SET LOCAL)
### 🏆 Excellent
# per-table policies indexed (tenant_id index), EXPLAIN runs on RLS queries in tests
# CI: RLS isolation test suite (no-scope SELECT returns 0); roles mini-privilege
# docs in django models (TenantMixin docstring notes RLS backstop)

## Failure modes
- policy absent on new tables (RLS is opt-in per table!)
- owner-bypass (use restricted roles, not superuser/owner in app connections)
- tenant_id stored on a col without index (policy scans)
- secret scope leak (app never SET LOCAL before multi-query runs)

## Evidence
- PostgreSQL docs: row-security policies (VERIFIED)