# ARCHITECTURE REVIEW CHECKLIST

> For design review meet/code review of an architecture. Use as a walk-through; ⚠ items warrant a written exception (ADR).

## 1. Requirements & scope
- [ ] What is the functional requirement, stated as "user must be able to..."? (no invented half requirements)
- [ ] NFRs: availability %, latency budget, scale (now + 18mo), security class
- [ ] Which actors/apps/users? (frontend, mobile, 3rd-party, partners)

## 2. Simplicity (SIMPLICITY_GOVERNOR)
- [ ] Every cache/queue/microservice/K8s justified by measurement or requirement?
- [ ] Simplest option fails first? (monolith → split only with evidence)
- [ ] What do we STOP doing if we build this? (cost of upkeep explicit)

## 3. Data model & DB
- [ ] Schema matches domain? (data-modeling.md); N+1 eliminated?
- [ ] Transactions/isolation chosen per load (relational/transactions)
- [ ] Migration path zero-downtime? (django/migrations.md)
- [ ] Backup/restore defined (RPO/RTO) + practiced? (backups-recovery.md)

## 4. API design
- [ ] REST/GraphQL/gRPC trade-off made consciously? (api/ROOT)
- [ ] Errors structured (RFC 9457 type), idempotency on writes, pagination bounded
- [ ] Versioning policy chosen + documented (before launch!)

## 5. Security
- [ ] AuthN flows enumerated (login, 2FA, reset); brute-force throttled
- [ ] AuthZ at OBJECT level in every handler (IDOR suite in tests)
- [ ] Secrets: no env in code, rotation plan, scanning CI
- [ ] Input validation at every boundary; PII classification + retention (compliance-level data)
- [ ] Threat model for new trust boundaries (threat-modeling.md)

## 6. Reliability & failure
- [ ] Every external dependency: timeout + retry budget + fallback/circuit
- [ ] Failure cascade map drawn (which parts die when X dies)
- [ ] SLOs exist and alertable (error budgets)
- [ ] Rollback path for the next release is real (deploy/rollback playbook)

## 7. Performance
- [ ] Latency budget per path; profile evidence for claims
- [ ] DB: EXPLAIN for top queries; indexes justified
- [ ] Caching: pattern chosen + invalidation + tenant keys (never blind TTL)
- [ ] Load test with production-like data planned

## 8. Observability
- [ ] Traces on critical path, logs structured+correlated, metrics per endpoint (RED)
- [ ] Queue lag + DB health + cache hit metrics
- [ ] Alerting: symptom-based (SLO burn-rate), runbooks linked

## 9. Testing & delivery
- [ ] Unit+contract+IDOR+critical path covered; flaky-free
- [ ] CI/CD: gates (lint, type, tests, security), staged rollout
- [ ] Schema migrations expand/contract safe; rollback rehearsed

## 10. Post-review
- [ ] All ⚠ have an owner+date; decisions recorded in ADR (adr.md)
- [ ] Knowledge → this skill memory (genome/flag)