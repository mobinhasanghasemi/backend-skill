# PERFORMANCE ENGINE

Evidence-driven performance engineering. No optimization without measurement; every claim split: measured / vendor-reported / estimated.

## Core cycle

```text
MEASURE
  ▼
PROFILE            (find the real bottleneck — not the suspected one)
  ▼
IDENTIFY BOTTLENECK
  ▼
HYPOTHESIS
  ▼
CHANGE (one at a time)
  ▼
BENCHMARK (same conditions)
  ▼
COMPARE
  ▼
VALIDATE (keep? revert?)
```

## Rules

1. **Profile first.** Requests may be slow due to DB, GC, network, lock, serialization — guesswork replaces profiling with waste.
2. **One change at a time.** Multiple changes => can't attribute the win.
3. **Stable conditions.** Profile with realistic (or at least known) load; warm caches vs cold matter.
4. **Percentile thinking** — p50, p95, p99, p999; means hide the real story (a single stray long task lifts the mean).
5. Never propagate "makes 10x faster" marketing numbers without /measurement.
6. Backpressure: if throughput can't keep up, latency curves upward nonlinearly. Distinguish latency-limited vs throughput-limited systems.

## Signals taxonomy

| Domain | Signals |
|---|---|
| CPU | util, per-process, scheduler, runnable queue |
| Memory | RSS, alloc pattern, GC (Python: objgraph/tracemalloc), swap |
| I/O | iops, queue depth, fsync cost, replica lag |
| Network | RTT, timeouts, retransmissions, connection churn |
| DB | query latency, seq scans, lock waits, pool waits, index/table bloat |
| App | middleware overhead, serialization, N+1, cache hit ratio (effective) |
| Queues | backlog age, consumer lag, DLQ growth |
| Async | event loop blocked, thread starvation |

## Techniques (when justified by PROFILIng)

- index (verify EXPLAIN change)
- cache (only hot reads; invalidation complexity)
- connection pooling
- async (blocking work off the event loop)
- batching (reduce RTT count)
- paging / pagination
- denormalization (schema trade-offs — see databases)
- compression (judged by CPU/bandwidth trade)
- precompute (rare reads of costly calcs)

## The measure-first principle for DBs

Never "static tune" the DB engine settings without load tests. Settings interact (RAM, work_mem, vacuum) — sequential change + measure, or you'll end at worse-than-before.

## p95/p99 rationale

- p50 tells normal user experience
- p95 19 of 20 requests
- p99, p999 reveal schedulers, GC and queue behavior
Latency budget decomposition — assign each hop (LB, app, DB, cache, downstream) budget.

## Backpressure / load shedding

- Unbounded work = memory blow-ups. Have a rejection policy: max concurrency, queue bound, drop-newest or shed trade.
- Circuit breaker + timeouts apply beyond APIs (see distributed-systems/).

## Anti-patterns

- Optimizing cache hits for reads the app rarely serves (measure)
- "This is 10x" benchmarks from vendor without reproduction
- Threads everywhere for IO (context-switch thrash instead)
- Crushing DB with a huge query to "save round trip"
- Tuning GC without profile numbers

## Interfacing

- Use `PERFORMANCE_ENGINE` inside DB/API decisions (not only standalone). Every neuron has a "Performance" section — write real logic there, not platitudes.