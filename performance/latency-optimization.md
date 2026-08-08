# Latency Optimization & Backpressure

## Identity
- ID: performance.latency-optimization
- Type: procedure
- Status: active
- Importance: high

## Purpose
Where latency comes from (queues, not just speed) and how to contract for it: budgets, tail control, backpressure, and capacity math.

## Mental model
Total latency = resource time (CPU, I/O) + **waiting time** (queues/locks/scheduling). At >60-70% utilization, queueing pushes latency nonlinearly (Little's Law: L = lambda·W). Hence the "knee": small load growth → big latency cliff. Never optimise resource time while the queue is the term.

## Latency budget method
1. Declare user-visible target (e.g., p95 < 250ms)
2. Break into hops (internet → LB → app → DB → serializers → app → back)
3. Allocate per hop with slack (85% used); each hop resigned daily by measurement
4. If any hop exceeds budget: fix THAT hop (profiling.md), not the whole chain

## Control toolbox
- Keep queue wait low: saturation monitoring, autoscaling vs throttle equilibrium
- **Backpressure**: reject or shed when saturated (503 early, queue-depth caps) — better than queueing to death (see RELIABILITY)
- Concurrency limits per dependency (semaphores) instead of unbounded pools
- Batching (DB batch inserts, single round-trips), connection reuse
- Read hot paths: cache (caching/ROOT), avoid N+1, denormalised projections
- Termination points: timeouts everywhere (connect/read), circuit breakers (see distributed)

## Code tiers

### ❌ Bad
```python
for item in items: save_one(item)        # 200 round-trips serial
```

### ✅ Good
```python
BulkCreate.atomic(items)                 # 1 round-trip (2 if RETURNING needed)
# (also enables: pagination, extension, retries)
```

### ⚡ Better — budget-first
```python
# DECLARED budget: p95 250ms = 30ms nginx+lb, 30ms app, 120ms DB, 50ms margin
# profile shows DB p95 180ms → dig into DATABASES (EXPLAIN), not container CPU
```

### 🏆 Excellent
```text
- SLO-backed budgets: alerts on hop p95 breach with owner; auto-budget per endpoint
- backpressure: saturation-based autoscaling/limiting (not just static max)
- load-test suite runs every sprint (blocking PRs at expected values)
- caches warmed on rollout; sample-trace always on; result in ADR
```

## Failure modes
- adding servers won't fix a single-slot DB hot spot
- unbounded queue = death spiral (backlog → TTL → user retries)
- p50 optimization while p95 drowns (focus on distributions, not mean)
- "it's fast locally on docker mac" vs prod reality

## Evidence
- Performance engineering classics: Little's law/queues (VERIFIED), backpressure patterns (Apache/Java guides; Docker docs; general)