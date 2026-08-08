# Compliance for Backends

## Identity
- ID: security.compliance
- Type: concept
- Status: active
- Importance: medium-high (skip when no regulated data)

## Purpose
Know which obligations attach to the data you process (GDPR, PCI-DSS, SOC2, HIPAA, Iran/PDPA-adjacent regimes...) and build the control points that prove it — without turning the skill into a law library.

## The honest model
Compliance is **data-flow obligations**, not paperwork:
1. What data classes exist? (PII, payment, health, children, financial)
2. Which regime applies per class? (jurisdiction of user + processing)
3. What are the obligations per class? (consent, rights, retention, breach notice, audit, encryption)
4. Map obligation → engineering control → evidence artifact

## The control map (backend-relevant)

| Obligation | Engineering control |
|---|---|
| Lawful basis + consent | consent records table (who, when, what, version), withdrawal flow |
| Right of access/erasure | export endpoint (GDPR Art.15/17): full user data bundle + deletion job with propagation list |
| Data minimisation | DTOs, retention schedules, no full-document logging |
| Security of processing | encryption at rest/in transit, secrets hygiene, access logs, authZ per object |
| Breach notification (72h) | incident runbook with notification template + clock (playbooks/incident-response.md) |
| Records of processing | data inventory doc (classes, location, flows, retention) — maintained with schema changes |
| Third parties | DPA check in supplier flow; data-processing registry |
| Audit | SOC2 readiness: evidence = logging, monitoring, change control, incident records |

## Code tiers

### ❌ Bad
```python
# no consent record, no export, no deletion path, unlimited retention
# "we'll handle compliance later"
```

### ✅ Good
```python
class ConsentLog(models.Model): user FK, scope, version, granted_at, source
# user rights endpoints: GET /api/v1/users/me/data (export), DELETE /api/v1/users/me (erasure)
```

### ⚡ Better
```python
# export: async job (outbox) → archive bundle in S3 signed URL (72h TTL)
# erasure: soft-delete flag + purge job (anonymise) after grace; propagation table 
#   (which services/data stores hold copies — queue payloads, logs, backups TTL)
```

### 🏆 Excellent
```text
- data inventory owned per module (schema comment: PII class on every column)
- retention jobs: scheduled purge per class; backup TTL policy aligned
- consent versioning + re-consent flows; withdrawal stops processing (flag checks)
- audit logs: admin actions, access (read of PII), token issuance — immutable + SIEM
- privacy tests in CI: no PII in logs (regex assert), export covers declared tables,
  deletion cascades correctly (FOREIGN KEYs reviewed), DPIA notes in ADRs
```

## Anti-patterns
- encryption treated as compliance (it's a control, not the compliance itself)
- compliance team in a silo (controls must be coded); same for "legal said" without mapping
- deleting data you don't know you have (shadow copies in queues, analytics, backups)
- golden data retention: when in doubt keep nothing beyond need

## Evidence
- GDPR Art. 15-34 (VERIFIED text), PCI DSS 4.0 summary, SOC2 trust criteria, NIST SP 800-122 PII guide