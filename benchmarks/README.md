# SKILLBENCH — Golden-task benchmark for Backend Architect Neural

> Objective evidence of the skill's uplift. 32 golden tasks over the Django → DRF →
> PostgreSQL → Redis → Celery vertical plus cross-cutting security/reliability/infra.
> The suite is **static** (no runtime deps): each task is a self-contained prompt with
> an explicit rubric; "solutions" are graded by a human (or the reviewing model)
> against the pass-bars below, never by babysitting a fake API.

## Methodology

- **Baseline run**: solve each task with the model WITHOUT the skill (base-model
  temperature 0, fresh session).
- **With-skill run**: same task batches with the skill active (`SKILL.md` surfaced).
- **Scoring**: per task, six dimensions × {0, 0.5, 1} → rubric.md. Uplift =
  `Σ(with) − Σ(base)` normalized to 0–100.
- **Adoption gate**: `with ≥ baseline +15` → skill earns "validated" status.
  If a task's with-skill answer introduces an unverified API (no source-<ID> in
  `research/sources.md`), that dimension is capped at 0.5.

## Task map (33 tasks)

| # | Task | Domain | File |
|---|---|---|---|
| 1 | Payment transfer with idempotency | api / pg | tasks/task-001.md |
| 2 | DRF list endpoint pagination + filter whitelist | django | tasks/task-002.md |
| 3 | Migration strategy for 40M-row table | pg/migrations | tasks/task-003.md |
| 4 | N+1 → keyset + EXPLAIN plan | pg | tasks/task-004.md |
| 5 | Async worker retry with DLQ | celery | tasks/task-005.md |
| 6 | Outbox for events (webhook delivery guaranteed) | messaging | tasks/task-006.md |
| 7 | Redis cache invalidation on write | caching | tasks/task-007.md |
| 8 | Cache stampede protection | caching | tasks/task-008.md |
| 9 | API schema (OpenAPI) generator for DRF | api | tasks/task-009.md |
| 10 | OAuth2/OIDC integration decisions | security | tasks/task-010.md |
| 11 | Row-level security (RLS) vs app-enforced authz | security/multi-tenancy | tasks/task-011.md |
| 12 | Secrets handling in codebase | security | tasks/task-012.md |
| 13 | TLS/HTTPS posture on staging vs prod | security | tasks/task-013.md |
| 14 | Password reset flow | security | tasks/task-014.md |
| 15 | Rate limiting per user | api | tasks/task-015.md |
| 16 | Logging without PII | observability | tasks/task-016.md |
| 17 | Tracing + metrics for an API | observability | tasks/task-017.md |
| 18 | SLO + error budget | reliability | tasks/task-018.md |
| 19 | Incident runbook — queue backlog | reliability | tasks/task-019.md |
| 20 | Retry/backoff strategy | distributed-systems | tasks/task-020.md |
| 21 | Circuit breaker tuning | distributed-systems | tasks/task-021.md |
| 22 | Distributed lock for a nightly job | distributed-systems | tasks/task-022.md |
| 23 | Saga vs outbox for checkout | distributed-systems | tasks/task-023.md |
| 24 | Async vs threads in FastAPI | python | tasks/task-024.md |
| 25 | Type hints in a legacy module | python | tasks/task-025.md |
| 26 | Container image hardening | infra | tasks/task-026.md |
| 27 | K8s secrets for a DB password | infra | tasks/task-027.md |
| 28 | Backup / RPO / RTO for payments DB | databases | tasks/task-028.md |
| 29 | gRPC vs REST for an internal service | api | tasks/task-029.md |
| 30 | RAG cache + cross-tenant isolation | ai-backends | tasks/task-030.md |
| 31 | Eval design for an LLM endpoint | ai-backends | tasks/task-031.md |
| 32 | Contract testing harness | testing | tasks/task-032.md |
| 33 | Load test to find the ceiling | testing | tasks/task-033.md |

## Gate

```text
PASS  if Σ(with) / Σ(base) ≥ +15 points  AND  no unverified invented API
SKIP  if a task is out of the model's skillset (reported, not scored)
```