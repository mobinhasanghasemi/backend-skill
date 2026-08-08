# Safe Django Admin

## Identity
- ID: django.admin
- Type: procedure
- Status: active
- Importance: medium-high (the overlooked attack surface)

## Purpose
Use the Django admin productively and safely: per-model permissions, read-only audit views, safe actions, and zero accidental data loss.

## The admin reality
- Admin is a **public application** with default auth — abuse vector #1 (brute force, privilege escalation, data exposure)
- Default: any `is_staff` sees ALL models with full CRUD where registered — scope least privilege!
- Never register sensitive models blindly (Users list = PII export; billing in clear)
- Never use `list_editable` for critical fields without audit; `actions` require lifecycle guarantees

## Code tiers
### ❌ Bad
```python
admin.site.register(Order)      # full CRUD on orders for any staff, incl. amount edits
admin.site.register(User)       # raw password hash exposure + full PII listing
# no restrictions; default login; staff = superuser
```

### ✅ Good
```python
from django.contrib import admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "total", "created_at")
    list_filter = ("status",)
    readonly_fields = ("total", "created_at")    # read-only money
    search_fields = ("id", "customer__email")    # bound
    actions = ["mark_shipped"]                    # whitelisted only
    def has_delete_permission(self, request, obj=None): return False
```

### ⚡ Better — access control tiers
```python
# - custom UserAdmin with limited fields (no password hash shown)
# - group-based: sales-group can view but not edit; ops muted for audit
# - two-factor for ALL staff (security/authentication.md)
# - audit log middleware: who did what in admin (JSON log every change, model, pk)
```

### 🏆 Excellent
```
# sensitive models NOT in admin (service layer only); admin IP allowlist
# actions: confirmations + undo path; rate limit brute force (429) on /admin
# deploy checks: DRF?+ admin served only on corp networks where possible
# automated dashboard of staff activity weekly: reads of PII models flagged
# stage test: admin change path covered by contract tests
```

## Failure modes
- registering everything default (`admin.site.register(Model)` for all)
- me: staff role able to edit anything
- action delete without conditions
- exposing via admin: all models incl. tokens/secrets

## Evidence
- Django admin docs (VERIFIED)