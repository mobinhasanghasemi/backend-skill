# Celery (Django's Workhorse)

## Identity
- ID: messaging.celery
- Type: technology
- Status: active
- Importance: critical (Django vertical)

## Purpose
Reliable async and scheduled jobs for Django (Redis as broker): emails, exports, webhooks, retries, cron. Rules of life: idempotence, bounded retries, DLQ, monitoring.

## The Celery anatomy
- Producer: `task.delay/apply_async` (works from view/service)
- Broker: Redis (or RabbitMQ) holds the queue; worker consumes
- Results backend (optional): used only when you await results (avoid waiting in web requests!)
- Schedules: beat (cron-ish) — beware beat + multiple workers (idempotent jobs, unique lock)
- Extras: autoretry, time limits (soft/hard), acks_late, task_retry policy

## Lifeline rules
1. **Idempotent tasks**: same input + retry → same outcome as once; event_id dedupe (outbox.md bridge!) for payments/notifications
2. **Durability choice**: Redis broker (fast, restart may lose queued jobs barely — use ack_late);
   RabbitMQ for strong durability
3. **Retries**: bounded (max_retries), explicit retry backoff (task default), DLQ binding (dead letter task) for poison
4. **acks_late + worker_prefetch_multiplier=1**: job not lost on worker crash; no zombie reprocessing of big jobs
5. **Timeouts**: soft_time_limit kills runaway; hard kills process
6. **Beat tolerance**: `unique_lock` decorator per schedule; tasks must be runnable by cron too

## Code tiers
### ❌ Bad
```python
@app.task
def send_invoice(order_id):
    send_email(order_id)          # no retry policy, no ack_late: crash loses it;
    # duplicate run = double email; no DLQ; blocks full queue if email down
```

### ✅ Good
```python
@app.task(bind=True, max_retries=5, default_retry_delay=30, acks_late=True, soft_time_limit=300)
def send_invoice(self, order_id):
    try:
        invoice_service.send(order_id)
    except EmailDown as e:
        raise self.retry(exc=e)          # backoff (exp), 5 tries, then DeadLetter
    # retries: 30s,60s,...5x; soft kill 5min; worker recall after crash via acks_late
```

### ⚡ Better
```python
# idempotent: TaskResult.get_or_create(event_id); no double side effect
# prefetch=1: big jobs not duplicated on worker restart
# DLQ: task retries exhausted → task to dead-letter queue + alert
```

### 🏆 Excellent
```text
# every task: {idempotency key, timeout, retry policy, DLQ, metrics name}
# observability: queue depth, task duration histograms, retry rate per task
# outbox integration for business events; beat schedules documented + idempotent
# test: task retry test (inject failure 1st attempt), DLQ alarm drill, overload test
# alerts: queue lag > budget, task rate anomalies, DLQ non-zero
```

## Failure modes
- no `acks_late` → crash loses jobs silently
- retries without backoff → thundering herd
- poison DLQ + no alert → job forever stuck
- huge task bodies in message (payload bloat to broker) — pass IDs only!
- calling big DB work inside task w/o batching (memory)

## Evidence
- Celery official docs (VERIFIED via source-S-015, accessed 2026-08)
- Retry semantics from official FAQ — documented, not guessed