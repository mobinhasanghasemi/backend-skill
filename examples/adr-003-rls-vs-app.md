# ADR-003: RLS vs app-enforced tenant isolation

- **Status:** accepted
- **Date:** 2026-08-12
- **Owner:** security chapter
- **Context:** B2B SaaS, 400 tenants, shared PG, IDOR risk ARCH014. Requirement: cross-tenant leak = CRITICAL.
- **Alternatives:**
  - A) App-only checks — rejected: single missing `tenant_id` filter = leak; no defense in depth
  - B) Schema-per-tenant — rejected: migration overhead ×400, connection storm
- **Decision:** Row-Level Security (PG RLS) as second wall + mandatory app filter + `SET LOCAL app.tenant_id` per request + per-tenant cache keys (`{tenant}:...`) + tests: IDOR suite per endpoint + RLS bypass attempt
- **Consequences:** leak surface ×2 walls, RLS policy overhead ~3% (measured), migration adds `USING (tenant_id = current_setting(...))`
- **Validation:** `EXPLAIN` shows RLS qual · `SET LOCAL` test · cache key tenant isolation test · pg_stat_statements
- **Genome:** `+ RLS + tenant-aware app + tenant-isolated cache`
