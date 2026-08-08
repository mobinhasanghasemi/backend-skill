# Load & Performance Testing

## Identity
- ID: testing.load-testing
- Type: procedure
- Status: active
- Importance: high

## Purpose
Prove the system handles expected peak traffic and degrades sanely: latency budgets, saturation, and the failure cliff — measured before users experience it.

## The honest sequence
1. **Define behavior**: peak RPS, concurrency, data size, read/write split (from capacity planning, NOT imagination)
2. **Production-like data**: right volumes + realistic skew (top-1% users/tenants) — synthetic-uniform data lies
3. **Test types**:
   - **Smoke** (single-run sanity)
   - **Load** (expected peak sustained — find latency, errors at budget)
   - **Stress** (beyond peak → find the cliff: saturation point, queue growth, GC, connection exhaustion)
   - **Soak** (hours: leaks, GC, slow growth, DB bloat day-shape)
4. **Assertions**: latency targets (p50/p95/p99), error % (0-1%), behavior degrade plan (when rejected → what)
5. **Environment reality**: test on same stack versions, network profile; never be fooled by dev machine

## Tooling (choose by stack)
- Python: locust (scriptable), k6 (JS), Gatling (rich ts)
- Server-side measurement: profile + DB stats + metrics during the run (tracing sampling)
- Deploy: run in cloud test env, NOT local

## Code pattern
```python
from locust import HttpUser, task, between

class Buyer(HttpUser):
    wait_time = between(0.8, 1.5)
    @task(10)  def list_products(self): self.client.get("/products") 
    @task(1)   def checkout(self): self.client.post("/checkout", json=PAYLOAD)
```
Then: capture metrics (per endpoint histogram), compare to SLO, write ADR with before/after.

## Failure modes
- load test ≠ real data / no database warmup (planner stats off! run ANALYZE first)
- 30s runs meaning nothing (steady-state & ramp matter)
- only throughput, no latency assertion
- spike of all endpoints at once (mix realistic: read/write/cache ratio)
- fix ignored (no owner for the perf report)

## Evidence
- locust/k6 docs (VERIFIED), performance testing practice (SUPPORTED)