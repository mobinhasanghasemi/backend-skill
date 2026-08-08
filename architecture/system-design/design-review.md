# Design Review

## Identity / Purpose
The structured review the brain runs on any produced architecture. Combines the Genome, the LINTER, and checklists.

## Process (in order)
1. **Genome** — obtain the architecture fingerprint (Start)
2. **Gate way**: SIMPLICITY_GOVERNOR says every component passes the 5 questions
3. **Security check** — SECURITY_GUARDIAN: threat model + per-component authN/authZ + data categories
4. **Perf check** — are the numbers ESTIMATED or MEASURED? can we show the budget?
5. **Reliability check** — failure cards exist? RPO/RTO stated? backups tested? rollback?
6. **Obs check** — every critical path instrumented; SLOs; alerts exist
7. **Linter** — run ARCH001..035; record exceptions as ADRs
8. **Rollback plan** for migrations
9. **Test plan** linkage (integration/load/chaos)

## Output format

```
✅ PASS / ⚠ WATCH / ❌ FAIL per section
+ stated residual risks
+ next validation steps (load test at X, etc.)
```

## When to use
- every architecture design deliverable
- infra changes (database, brokers, k8s)
- every major ADR review

## Related
- checklists/architecture-review.md — the longer manual
- ARCHITECTURE_LINTER — the rules
- VALIDATION_PROTOCOL — gates