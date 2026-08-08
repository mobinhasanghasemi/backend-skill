# Saturation, Scaling & Capacity

## Identity
- ID: performance.saturation-scaling
- Type: concept
- Status: active
- Importance: high

## Purpose
Understand when a system is actually at capacity (saturation) vs just busy, and scale correctly: up (vertical), out (horizontal), or split (partition/separate concerns).

## Core signals
- **Saturation**: high utilization + latency cliff (waiting). Utilization alone (70% CPU) is not failure; latency at p95 tells.
- **Headroom**: idle workers, queue depth, connection pool usage — the real "capacity" story
- **Bottleneck flow**: find the strand that constrains; scaling every other strand is waste
- **Little's law**: concurrency = RPS × latency. Rule of thumb: concurrency needed = RPS × p-latency (e.g., 100 rps × 200ms = 20 concurrent)

## Scaling ladder (measured first!)
1. **Vertical (up)**: more CPU/RAM on the box — cheap, one-node predicates
2. **Read replicas** (DB reads), caching the hot set — usually biggest IO win first
3. **Horizontal app replicas** behind LB — stateless == easy; needs session handling
4. **Queues** for spikes & async decoupling (not for latency)
5. **Sharding/partitioning** the DB (writes), time-partitioning for retention
6. **Cells/regions** (last, costly, real)

## Code tiers

### ❌ Bad
```python
# "scale to 20 pods" — for a single writer DB with 1 session; replicas unused
```

### ✅ Good — measure first
```python
# says load test: all nodes OK except DB at 95% utilization
# → fix is DB: read replicas or cache or query shape; not more pods
```

### ⚡ Better
```python
# autoscaling on queue depth / latency (NOT CPU%); schedules for predictable peaks
# read replicas serve hot reads; writes single-primary (avoid split-brain)
```

### 🏆 Excellent
```text
- capacity planning table (current peak + forecast peak + growth model) 
- saturation dashboards (utilization × latency), not just CPU graphs  
- scale triggers: latency-based autoscaling with min/max + cool-down
- data model: read-mostly → replicas; write-heavy → shard by tenant/region; 
  retention → time-partition drop; analytics → OLAP projection
- exit criteria documented before building (when to stop scaling up and shard)
```

## Failure modes
- scaling app but not DB (the eternal copy error)
- scaling everything when only one constraint is hot
- replicas with no lag monitoring / stale reads hitting users
- CPU-based autoscaling in GC/managed languages (heap bloat ≠ CPU)

## Evidence
- Little's Law & queueing theory (VERIFIED math); AWS re:Invent scaling patterns (supported)