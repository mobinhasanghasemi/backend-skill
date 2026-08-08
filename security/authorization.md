# Authorization (AuthZ)

## Identity
- ID: security.authorization
- Type: discipline
- Status: active
- Importance: critical

## Purpose
"Who can do what, on which object" — enforced **per resource**, not just by endpoint. Broken access control is the #1 realistic OWASP class (BOLA/IDOR) — the top security bug developers ship.

## Layers (match the data)
1. **Authenticated?** → request principal (user/service)
2. **Role/plan tier** (admin/user/premium) — coarse
3. **Object-level** (ownership, tenant, membership) — the one people forget (ARCH014)
4. **Data-level**: column filtering (tenant-visible fields) for reads by policy

## Core designs
- **RBAC**: roles→permissions; simple until huge
- **ABAC**: attributes (role, tenant, resource owner, env) — flexible for SaaS
- **Open Policy Agent / OSLC equivalents** when rules grow; middleware vs in-handler choice per criticality
- **Decide in ONE module** (permission checkers), not scattered if-storms

## Code tiers

### ❌ Bad
```python
def get_order(request, order_id):
    order = Order.objects.get(id=order_id)      # no ownership check!
    return order                                # IDOR: any user reads any order
```

### ✅ Good
```python
def get_order(request, order_id):
    order = Order.objects.get(id=order_id, customer=request.user)  # scoped query!
    return order     # 404 for others — blending hides existence
```

### ⚡ Better — single permission point
```python
class OrderPolicy:
    @classmethod
    def can_edit(cls, user, order):   # central policy module, all flows use it
        return order.customer_id == user.id and not order.locked
# handlers: policy.check(...) → 403 / 404 blend per context
```

### 🏆 Excellent
```text
- authz: middleware + object-level checks absolutely everywhere (unit test per endpoint: 
  "user B cannot read user A's doc", "tenant C cannot query tenant D")
- tiered permissions (roles) + scoping filters in queries (queryset by user/tenant)
- securit_hash: `Vary on Authorization`; cache keys include scope
- tests in CI: IDOR suite, role matrix suite (every permission toggle tested)
- audit: denial logs (who tried, on what, blocked reason) aggregate for abuse detection
- upgrade path: RBAC→ABAC (policy-as-data) when rules exceed config maintenance
```

## Anti-patterns
- authz only in middleware, none in data layers (service bypass)
- `is_staff` boolean sprawl instead of roles
- caching at CDN that mixes authenticated responses
- 403 blanket hiding nothing (vs 404 keep secret 404 for existence)

## Failure modes
- IDOR in list endpoints & exports (mass data at risk)
- tenant leakage via shared cache keys (ARCH014)
- authz checks in JS client only — server must re-verify

## Security
- CHECK policies hard in DB? (PG RLS as last line) — document; unit tests always

## Evidence
- AuthZ / BOLA-IDOR: VERIFIED via source-S-020 (OWASP API Security Top 10)
