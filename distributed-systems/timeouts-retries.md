# Timeouts, Retries & Backoff

## Identity
- ID: distributed-systems.timeouts-retries
- Type: procedure
- Status: active
- Importance: critical

## Purpose
Calls between components fail. Design the failure response: how long we wait, how often we retry, and how we avoid turning a single failure into outage-everywhere.

## Contract of any call
1. **Timeout** — connect + total deadline; without one, the caller waits forever (and its threads/requests pile up)
2. **Retry policy** — *when* retry makes sense (5xx, Idempotent-Key-able 4xx?), how many, with **exponential backoff + jitter** (jitter breaks thundering herds)
3. **Cap** — max retries per request; the system retries at call level, not thread naps
4. **Budgets** — global retry budget (e.g., 10x steady state); clients stop retrying when downstream is confirmed degraded
5. **Idempotency keys** — retry still safe: same key, same result (api/idempotency.md), late arrival reusable

## Code tiers
### ❌ Bad
```python
try: result = call()            # no timeout: hangs forever
except: time.sleep(5)           # fixed sleep: herd
        call()                  # infinite retry loop forever
```

### ✅ Good
```python
for attempt in range(3):
    try: return call(timeout=3.0)
    except TimeoutError as e: 
        if attempt == 2: raise
        time.sleep(min(0.5 * (2 ** attempt), 8))    # exponential, capped
```
(plus jitter, unless you like herd.)

### ⚡ Better — jitter + budgets
```python
sleep = min(cap, base * 2**attempt) * random.uniform(0.5, 1.5)  # jitter
# per-callee budget: not retrying the same broken service beyond X/min
```

### 🏆 Excellent
```text
- deadlines: call with total deadline (connect + read + margin), for queue depth too
- retry header: Retry-After respected from 429/503, custom "service degrading" (dry)
- circuit breaker when budget (failure rates) exceeds threshold (circuit-breaker.md)
- idempotency everywhere writes occur (charges, orders) — double-charge proof
- backpressure: if we're saturated, reject early (503) — don't queue more
- visibility: retry metrics (rate, budget used, jitter), alert on abnormal retry rates
- chaos: injected partial failures (black clients, lag) to prove the policy
```

## Failure modes
- timeout = forever (default hang) — first and most common killer
- fixed-interval retries during outage → thundering herd + amplification sheets
- retry on 4xx (never changes) — waste
- retry without idempotency on writes → duplicates (payments!)
- timeout shorter than one DB query (false negatives)
- no global budget → retries kill the service they fight

## Rules
- timeouts are per component, not config magic; document per dependency in code
- retry = probabilistic (service down) — measure, cap, alert
- layered: connection pool, circuit breaker, budget — each one has its role

## Evidence
- AWS/Google retry guidance, "Designing Data-Intensive Applications" Chapter 8 (VERIFIED)