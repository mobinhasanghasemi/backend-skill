# PERFORMANCE — ROOT NEURON

## Identity
- ID: performance.root
- Domain: performance
- Type: root
- Status: active
- Importance: critical

## Purpose
Latency and throughput engineering: **measure first, then optimize** — the #1 rule. Every optimization is a hypothesis until measured.

## Activation
- "slow", "high latency", "timing out", "maxed CPU", "DB slow"
- capacity planning, load tests, tuning
- Any claim about performance improvements

## Routing
```text
find the bottleneck   → profiling.md (profiler + flamegraphs + tracing)
DB slow              → databases/optimization/ROOT (EXPLAIN first)
API slow             → api + caching + load test
scaling reads        → caching/ROOT → replicas → sharding
scaling writes       → queues, partitioning, materialized projections
"how fast can it be" → profiling + capacity-planning.md (architecture)
```

## The performance law (non-negotiable)
1. **Measure** — profile, trace, benchmark; numbers from YOUR system, not folklore
2. **Hypothesize** — name the bottleneck mechanism (CPU? I/O? lock? network? GC?)
3. **Change one thing** — re-measure; record before/after
4. **Never guess twice** — if hypothesis fails, profile deeper, don't stack configs

## Cross-cutting attention
- p95 > p99 > max in reporting (max lies); latency distributions matter
- throughput: RPS per node, saturation (utilization% vs latency cliff — the "knee")
- tail latency from queuing (head-of-line), garbage collection, network
- measured gains must be labeled: `EXPERIMENTAL` until reproduced

## Common failure modes
- premature optimization (perf before correctness) — SIMPLICITY_GOVERNOR veto
- micro-optimizing the wrong layer (SQL loop vs N+1 fix)
- load tests not matching production data shape/volume (skew!)
- optimizing without instrumentation → invisible
- latency budgets ignored (no SLO → no target)

## Security/reliability ties
- perf changes = reliability risk (pool sizes, timeouts) — check RELIABILITY engine
- DoS surfaces (costly queries) — SECURITY_GUARDIAN

## Evidence
- Methodology standard (profiling-first, supported universally); specific tools VERIFIED in neurons