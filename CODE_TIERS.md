# CODE TIERS — Teaching Samples That Guide, Never Command

A neuron's `Code Tiers` section wins nothing if it lectures. It wins everything if the AI, reading those 4 samples, understands the **building spectrum** of the pattern: why minimal is fine, what raises the bar, and what "production" really means. The AI is never told "do this"; it is shown trajectories and decides based on context (load, security class, team size).

## The 4 tiers, defined

| Tier | Label | Goal | Yardstick |
|---|---|---|---|
| ❌ Bad | the common misstep | show the failure eagerly | realistic; the AI should be able to say "I know why this is wrong" without explanation |
| ✅ Good | acceptable baseline | correctly meets the spec | clear, minimal, correct for the described context |
| ⚡ Better | meaningful improvement | one quality jump | at most 2 changes: e.g., query optimization + security or + observability |
| 🏆 Excellent | production-grade | the ceiling for the context | measured, bounded, observable, fault-tolerant, documented |

Rules of the ladder:
1. Samples differ in **architecture**, not in cosmetics.
2. Each tier states the **reason** it's where it is.
3. The ladder is per-context: the "Bad" of "two-phase commit over a queue" differs from the "Bad" of "retrying a POST without idempotency".
4. Tiers are not swords. The AI may deliberately pick ✅ (or even ❌) for a toy system with a one-month horizon — and must say why.

## Example ladder (Python, retry pattern — from distributed-systems/timeouts-retries.md)

```python
# ❌ Bad — not idempotent-aware, no cap, blocks synchronously
for attempt in range(100):            # unbounded-ish
    try:
        charge(customer, amount)
    except PaymentError:
        time.sleep(2)                 # no jitter, no backoff growth

# ✅ Good — bounded backoff per sane default
for attempt in range(3):
    try:
        pay(customer, amount, idempotency_key=order.id)
        break
    except PaymentError:
        time.sleep(min(2 ** attempt, 60))
```

```python
# ⚡ Better — same + jitter, exponential truncated, logs covered
for attempt in range(5):
    try:
        pay(customer, amount, idempotency_key=order.id)
        break
    except PaymentError as e:
        backoff = random.uniform(0, min(2**attempt, 60))
        log.warning("payment failed attempt=%s sleep=%.0f", attempt, backoff)
        time.sleep(backoff)

# 🏆 Excellent — circuit breaker, quota, budgets, telemetry
@circuit("payment", fail_threshold=5, open_after=30)  # per payment-API
def pay_safely(order):
    for attempt in range(limit_via_budget()):           # per-request retry budget
        with tracer.start_span("payment.call") as s:
            try:
                return pay_client.pay(order, idempotency_key=order.id)
            except PaymentError as e:
                s.record_exception(e); metrics.payment_retries.inc()
                sleep(backoff_with_jitter(attempt))
    raise PaymentError("exhausted retry budget")
```

Every tier is one genuine architectural trait upward: idempotency (Good), bounded backoff (Better), circuit+budget+budget telemetry (Excellent). Real point: each tier maps a specific failure mode it eliminates.

## When to include the section

| Neuron | Include tiers? |
|---|---|
| Implementation-flavored (rest API, query optimization, django orm, caching, rate-limit, webhook, background jobs…) | YES — the heart of it |
| Pure concept (CAP, MVCC, consensus) | YES, but symbolic latent (proof-of-concept tiny SQL/why) |
| ROOT neurons / routers | NO (they route, not implement) |

## Language of the samples

- Django/API domain → Python/Django
- Databases → SQL + a snippet of ORM where relevant
- Infra → YAML/Dockerfile/kubectl
- Distributed → pseudocode when the concept is language-agnostic — preference real language snippets

## The "no constraint" clause (the most important rule)

1. **No tier is mandatory.** The AI decides the appropriate level for the actual context (load, team time, risk).
2. **No neuron can say "must/always use X".** Recommended: "for context A, X historically performs well; for context B, Y's trade-offs correct".
3. The AI is free to produce the badge-tier solution with explicit trade-off reasoning — that's enlightenment, not disobedience.

## Sample-neuron guarantee

Code samples MUST NOT hallucinate API names/behavior. They always match the neuron's version-awareness and documented evidence. If a sample would require an unverified API — mark `ⓘ illustrative, API name indicative — verify`.

## Snippet labels

Every code fence in a neuron carries an implicit label:

- `<!-- executable -->` — real-language, runnable against the documented stack (Django ORM, psycopg, celery…). Must not contain invented helpers.
- `<!-- illustrative -->` — concept sample; invented helpers (e.g. `db.fetch_for_update`, `IdemStore`) are allowed but MUST be flagged in a comment or preceding line so no consumer treats them as real API.
- `<!-- data-only -->` — real SQL/config/probes (e.g. `pg_stat_user_tables`, `EXPLAIN`): literal, no pseudocode.

When in doubt, mark illustrative. The SkillBench rubric penalizes unlabelled invented API in `executable` samples.