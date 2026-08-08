# Playbook: AuthN/AuthZ Breach Scenario (detection & demonstration)

## When to use
- user reports data access incident, or detection (403 anomalies) suggests cross-tenant/cross-user access — IDOR suspicion (OWASP A01/BOLA)

## The straight course
1. **Scope** immediate: disable any suspected handling path (feature flag), preserve log evidence (they are the memory) — do not go silent, open incident (incident-response.md)
2. **Check the three leaks** (isolation docs):
   - scoped query missing: endpoint with `filter(owner=...)`? (django/orm.md)
   - cache shared across users (cache key lacks user scope)
   - webhook/background job not carrying tenant id (payload/consumer scope)
3. **Prove**: fetch logs/traces for that user/foreign user; or reproduce on staging with two test users

## Restrict/clean
- patch: add scopings everywhere (policy module in one place — authorization.md)
- cache: purge shared keys after validation, introduce tenant keys
- revoke exposed sessions/tokens; rotate secrets if event paths exposed them

## Hardening (permanently)
- **IDOR test suite** added to CI for every object endpoint (testing/security-testing.md)
- threat model update with the trust boundary discovered (threat-modeling.md)
- capacity to audit: object-level logging now part of access paths dispatcher

## Verdict matters (blame-free)
- postmortem after: what rules should have caught it (who forgot WHERE); make the gate — a counter “object-level test per endpoint” regression — permanent