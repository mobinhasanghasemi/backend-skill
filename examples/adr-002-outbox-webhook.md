# ADR-002: Transactional outbox for webhook delivery

- **Status:** accepted
- **Date:** 2026-08-11
- **Owner:** payments team
- **Context:** Webhook POST must be at-least-once; crash between DB commit and HTTP call caused lost events (1.2% under load test). Ordering per aggregate required.
- **Alternatives:**
  - A) Dual write (DB+HTTP) — rejected: no atomicity, lost events
  - B) Change-data-capture (Debezium) — rejected: ops heavy for current scale
- **Decision:** Outbox table in same PG tx (`outbox` insert + business write atomic) → Celery relay polls `SELECT ... FOR UPDATE SKIP LOCKED` → POST with timeout+retry+jitter+circuit breaker → idempotent consumer (`Idempotency-Key` + `event_id` unique) → DLQ after 5 retries
- **Consequences:** zero lost events (verified by chaos), +1 table + relay job, at-least-once duplicates handled by idempotency
- **Validation:** kill -9 relay mid-batch → replay correct · duplicate POST → 200 replay · DLQ alert fires
- **Genome:** `+ transactional outbox + celery/redis + idempotency store + dlq`
