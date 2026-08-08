# brain/failure-propagation.md

The library of failure cascade models — how a failure spreads to become an incident. The design phase must pre-compute cascades; the playbooks use them under incident.

## The canonical worth list

### 1. Database slowdown (the big one)

```
DB slowdown
  ↓
requests wait in pool
  ↓
connection pool exhaustion
  ↓
free queries blocked
  ↓
queue growth (job backlog)
  ↓
latency spikes
  ↓
client timeouts → retries
  ↓
additional load (retry storm) → DB overload → [feedback loop]
```

Break edges: monitor pool depth + query latency, reduce retry concurrency, add load shedding at API, circuit breaker on slow queries.

### 2. Dependency outage (downstream)

```
Downstream AMS down
  → upstream wait/timeout default-infinite
  → thread pool / event loop exhaustion
  → app slow for ALL users (not just the call)
  → cascading timeouts from your clients
```

Break edges: always timeout, circuit breaker, bulkhead the dependency into a pool, fallback response (cached/empty).

### 3. Queue backlog

```
Producer faster than consumer
  → queue length grows
  → age of messages (consumer lag) grows
  → freshness violation → user sees stale state
  → (if bounded) memory pressure; if unbounded, broker crash
  → catch-up burst on service recovery → thundering herd
```

Break edges: autoscaling consumers, DLQ, discard-oldest policy, backpressure from consumer, monitor lag.

### 4. Cache failure

```
Cache node down
  → cache miss storm (all reads → DB)
  → DB overload → cascades like (1)
  → cache stampede (all threads build the same key)
```

Break edges: cache multiAZ (or acceptible), copy-on-write cache loading with lock/single-flight, offload to replica (degraded mode), warm Gray.

### 5. Deployment failure

```
Bad version deployed
  → errors increase
  → rollback
  → if DB migration in deploy: lock/timeout
  → new version incompatible with old code mid-state (mixed version)
```

Break edges: canary + monitoring, DB migr forward-only, expand/contract.

### 6. Network partition

```
Split brain (two leaders)
  → conflicting writers
  → data divergence; then merge conflict resolution
  → read inconsistency
  → failover issues (standby can't measure primary)
```

Break edges: quorum, fencing tokens, clock discipline, operator scripts.

### 7. Traffic spike

```
Ads/campaign spike
  → 10x load
  → connection exhaustion
  → queue backlog
  → timeouts → retries → amplification
  → (or) cost spike (cloud) — monetary feedback loop
```

Break edges: capacity planning, autoscaling + headroom, SLO on backpressure, load test pre-spike.

## Detection of feedback loops

A loop if: failure →  repairs that add even more load. Ways to detect during design:

- trace each retry/backoff setting
- pool size × latency → overflow
- queue bound + growth
- consumer under-capacity

## Why this matters for design

Every component should have its own "failure card":

```
component: <name>
normal path: ...
failure: <what>
cascade: <what downstream>
loop: <does it amplify?>
breakpoint: <where do we cut the loop>
```

That's a **Bulkhead-and-Loop** blueprint for RELIABILITY and playbooks.

## Failure depth

Model down to: DB, cache, queue, dependency, config, deployment, network, clock, quota. Not every component is top criticism — high at ≤3 failure-critical ones (usually DB + dependency + deploy path).