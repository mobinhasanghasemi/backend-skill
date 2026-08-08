# MULTI-TENANCY — ROOT NEURON

## Identity
- ID: multi-tenancy.root
- Domain: multi-tenancy
- Type: root
- Status: active
- Importance: high (SaaS core)

## Purpose
SaaS isolation engineering: choose the tenant model by data class + cost, then enforce the isolation Y at every layer (DB, cache, queues, logs, background jobs, ML caches). Cross-tenant breach is a business-ending event.

## Tenant model decision
| Model | Isolation | Cost | Match |
|---|---|---|---|
| **Row-level (shared DB, tenant_id column)** | SQL-level filter + RLS | cheapest | most SaaS (pg huge) |
| **Schema per tenant** | schema namespace | medium ops | legal/regulatory data, max privacy |
| **DB per tenant** | full DB | expensive | large/enterprise data |
| Hybrid (pools per tier) | — | — | scalable growing store |

PostgreSQL: `tenants` table + `RETURNED tenant_id` policies; Django: middleware + scoped queryset

## The isolation checklist (where leaks happen)
1. **Query filter**: every query begins tenant_id (queryset manager default! policy!)
2. **Cache**: keys include tenant (caching/ROOT) — cross-tenant in Redis = leak
3. **Async**: every job payload carries tenant_id, and the worker's DB access scopes it (hard refactor of globals)
4. **Search/store**: ES/vector store metadata must include tenant filter (RAG leak!)
5. **Exports/file**: signed URLs per tenant; bucket prefixes (storage domain)
6. **Webhooks**: consumer identity per tenant
7. **Metrics**: never aggregate PII across tenants; the pipeline must carry k
8. **Admin/audit**: staff-scope = own tenant or superuser only

## Code tiers
### ❌ Bad
```python
def list_invoices(request):
    return Invoice.objects.all().order_by("-date")      # no tenant filter!
# user from tenant A sees tenant B's invoices (cache shared → leak double)
```

### ✅ Good
```python
class TenantMixin(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=PROTECT)
    class Meta: abstract = True; default_queryset_scope = "tenant"
# manager: .filter(tenant=request.tenant) default; DB RLS backstop
```

### ⚡ Better
```python
# PG RLS policy: tenant_id enforced in DB even if code forgets
# test suite: cross-tenant matrix (test per endpoint: B can't see A)
# cache keys: {tenant_id}:entity:id; jobs: tenant_id column; flag per async serialized
```

### 🏆 Excellent
```text
# isolation test: automated, exhaustive, in every release (IDOR suite for
# tenant to slug/session: tenant id in token context (never in URL on client surfaces)
# audit log tenant-aware; export DTOs per-tenant signed
# multi-tenant dashboards: cross-tenant metrics forbidden by policy + tests
# migration drill: tenant moves between models without data leak
```

## Failure modes
- tenant filter on authenticated views only (unauthorized epic)
- adapter caching shared keys
- Redis/ES/analytics sync among tenants
- tenant switcher in tests (bugs hidden)
- model where tenant is optional (null tenant → global leak)

## Security gate
- SECURITY_GUARDIAN: isolation guarantee = the architecture firewall; tests = chest check

## Evidence
- Tenancy models (shared/dedicated): SUPPORTED practice
