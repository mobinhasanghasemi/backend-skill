# Security Testing (App)

## Identity
- ID: testing.security
- Type: procedure
- Status: active
- Importance: high

## Purpose
Prove the security controls work: authz matrix, input validation, injection, and abuse thresholds — in automated suite (SAST/DAST in CI, manual pentest less often).

## The layers
1. **Unit/integration authz** (the MUST): every endpoint × role matrix — IDOR, 403 tests, tenant isolation; 404-blend check
2. **Input fuzzing/schema**: parameter types, length, encodings (URL, JSON, malformed); serializer level
3. **Secrets scanning** in CI (gitleaks) and dependency audit (pip-audit/OSV, GitHub dependabot)
4. **SAST** (semgrep/bandit): rules for injection/deserialization/untrusted eval
5. **DAST** (zaproxy/owsap): automated crawl config; SSRF checks, tar — integration in CI on staging
6. **Security reviews**: at architecture/ADR time (threat-modeling.md), features with data flows

## The cases worth writing (cost-benefit)
| Case | Test |
|---|---|
| IDOR | every object endpoint: user B attempts A's resource → 403/404 |
| Tenant isolation | cross-tenant filter query → 0 rows + 403 |
| AuthN | wrong/expired token 401; brute-force path → rate limit 429 |
| Injection | Fuzzed inputs to endpoints; no SQL executed via string |
| Uploads | path traversal, size limits, type sniff, no execution location |
| SSRF | config allowlist server fetches; test blocked host |
| Crypto | tampered ciphertext → error (cryptography.md) |
| Log/error | logs contain no PII (redaction test) |

## Code patterns
```python
def test_idor_cannot_read_others_invoice(self, api, user_a, user_b):
    r = api.get("/invoices/{invoice_b}", as=user_a)
    assert r.status_code in (403, 404)     # never 200!

def test_cross_tenant_query_blocked(...): 
    r = api.get("/orders", {"tenant": OTHER}, as=user_a)  #  depend on policy
```

## Failure modes
- security testing = only scanner report nobody reads (number-driven)
- DAST on prod (damage + false alarms)
- secrets scanning added AFTER leak (history)
- authz tests as the last checkbox (missing tokens → holes)

## Tooling advisory
- pip-audit + gitleaks + semgrep in every PR + nightly; manual pentest quarterly/annually for compliance
- Keep test-corpus alive together (like a mini pentest suite)

## Evidence
- SAST/DAST: SUPPORTED via S-035 (gitleaks) and S-036 (semgrep); OWASP S-023
