# Security: Threat Modeling

## Identity
- ID: security.threat-modeling
- Type: procedure
- Status: active
- Importance: high

## Purpose
Find attacks BEFORE code: enumerate assets, actors, trust boundaries, attack surfaces — then decide mitigations proportional to risk. A design-time discipline, not a ceremony.

## Method (light, fits any flow)
1. **Scope**: system + data flows (data at rest, in transit, processed)
2. **Assets**: what's worth attacking (PII, payments, admin, API keys)
3. **Actor map**: users- tenants, admins, services, attackers (before/after authN)
4. **Trust boundaries**: draw diagram with boundary lines (internet→API, API→DB, webhook→router, third-party)
5. **Threat per boundary** via STRIDE (Spoof, Tamper, Repudiation, Info disclosure, DoS, Elevation) → list with: entry point, actor, impact, likelihood
6. **Mitigations**: countermeasures mapped; accept/transfer/eliminate; verify each with test
7. **Maintain**: re-run on each feature/migration/upstream change (ADR triggers)

## STRIDE by backend component (quick table)
| Component | Typical threats |
|---|---|
| API authentication | Spoof (stolen tokens), brute force, session accepting |
| Object endpoints | Tamper via IDOR, Elevation |
| DB layer | Injection, access control bypass |
| Queue/worker | Tampered messages, replay, poison jobs |
| Webhook delivery | Spoofed events (HMAC!), Reject (tampered), replay |
| Logs | Sensitive disclosure (PII), repudiation (no trail) |
| Infra (containers/CI) | Supply-chain poisoning, credential theft (secrets.md) |

## MINIMUM viable model
- Payload of changes diagram: data flow at file level; list all "trust boundary crossings"
- For each crossing: "what can go wrong" 5-8 bullets; score OWASP Risk (Impact×Likelihood); assign owner+milestone
- Add to ADR (adr.md) for recorded decisions
- Gate: no crossing without check/validation/authN/authZ

## Code tiers

### ❌ Bad
"No threat model" → feature ships thinking; bug found later in prod by attacker.

### ✅ Good
```text
# change diagram: User CLI → API (auth, TOTP) → DB → (batch job) → report S3
# boundary #2 (API→DB): injection, IDOR, quoted mask; boundary #4 (job): link of keys
```

### ⚡ Better — scored & PR-linked
```text
# each finding: {id, surface, attack, impact:Med/High, likelihood, mitigation, tests}
# new feature PR includes a threat-model-review diff (threat-modeling.md applies) OR admission documented
```

### 🏆 Excellent
```text
- threat library (per boundary canonical table reuses across features) with owner
- adversarial tests per accepted threat (chaos/story per scenario)
- framework: OWASP Threat Dragon / OWASP SAMM…; effort budgeted (e.g., 30-60 min per feature)
- annual review: models vs breached/Surprise (so the process learns)
```

## Failure modes
- Infinity cross-team ceremonies (anti: strict scope, offline-first notes)
- Models on paper only (no test linkage)
- Blame-oriented culture (fear → no honest models)
- Missing when it matters (Payment/Core changes))

## Security
- Trust boundaries mapped precisely; secrets never crossed in diagrams harmlessly

## Evidence
- STRIDE/PASTA threat modeling: SUPPORTED (OWASP framework family, S-023)
