# Profiling & Finding Bottlenecks

## Identity
- ID: performance.profiling
- Type: procedure
- Status: active
- Importance: critical

## Purpose
A repeatable method to find where time actually goes — CPU, I/O, lock, network, GC — in an order that finds real wins fast.

## The ladder (evidence order)
1. **Tracing / APM first** (OpenTelemetry): which service/endpoint is slow? request-level breakdown
2. **Instrumentation**: per-request breakdown — DB time (pg_stat_statements), Redis, external calls, queue wait
3. **Profiler for CPU** (py-spy, cProfile) & **async profiling** (py-spy --idle for event loop)
4. **DB** — the usual suspect (EXPLAIN (ANALYZE, BUFFERS); databases/optimization/ROOT)
5. **I/O**: iostat/vmstat, strace, page faults — storage latency
6. **Network**: tcpdump latency splits, connection reuse, TLS handshake cost
7. **GC/memory**: allocations, pressure (see GC for Python; Rust/Go specifics)
8. **Infra**: CPU steal, throttling, noisy neighbors

## Code tiers

### ❌ Bad
```python
# guess-optimization: "it's probably the ORM" → rewrite everything
```

### ✅ Good
```python
# measure first:
#  1. APM says GET /orders p95 = 1.2s
#  2. trace breakdown: DB 0.9s / serialization 0.2s / HTTP 0.1s
#  3. hypothesis: N+1 in orders serializer → EXPLAIN confirms 300 queries
```

### ⚡ Better — structured search
```python
# py-spy top --pid <app>  → real CPU stack sampling in prod, no restart
# py-spy dump → what each thread is doing (blocked on? DB? lock?)
# DB: pg_stat_statements top by total_time; EXPLAIN the top-3
```

### 🏆 Excellent — budgeted & monitored
```text
- latency budget declared (e.g., API ≤ 200ms p95: 150ms app + 50ms slack)
- profiling sessions recorded (what, where, before/after numbers) in perf ADR
- load test with production-like data (real skew), not synthetic
- after each change: re-run the same trace — numbers in the ADR
- production: continuous profiling where affordable (py-spy on 1% samples)
```

## Failure modes
- profile wrong environment (docker overhead vs prod shape)
- micro-optimize before end-to-end (fixing a 1% call while 90% goes elsewhere)
- no baseline (can't tell if change helped)
- chasing tail events without understanding their share of traffic

## Evidence
- py-spy/OpenTelemetry docs (VERIFIED); profiling methodology (SUPPORTED — universal)