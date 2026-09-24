# Capacity Planning (rough math before architecture)

## Identity
- ID: architecture.system-design.capacity-planning
- Type: procedure
- Status: active
- Importance: medium

## Purpose
Produce order-of-magnitude numbers that distinguish "fine on one box" from "needs real scale out" — so the design isn't guessing.

## The math
1. Traffic: RPS = daily_users × requests_per_day / 86400 × peak_multiplier(3-5x)
2. Storage: rows ≈ rate × retention; bytes/row × rows = GB/yr
3. Throughput:
   - DB: read QPS limits ~ 10k-100k/s for single node (PG shared buffers), write TPS bounded by commit time; ~ 1-5k/s writes/node
   - Redis single node: 100k ops/s
   - Kafka: 100k-1M msg/s per node (GPU-though)
4. Connections: pool max ≈ nodes × pool_size; connections vs RAM

## The rough formulas
```
QPS from DAU: DAU × per-user-actions/day ÷ 86400 × peak-mult
Storage/yr: avg_bytes/record × records/day × 365 (add index 1.5x)
Memory for cache (if needed): working set selected!
  if cache size > RAM → rethink (LRU won't help))
DB write capacity: ≈ #writes × write-cost; node limits → scale strategy
Queue: backlog = capacity(t) - produce(t) → confirm bounded
```

## Units / honesty
- Always label "rough" (order-of-magnitude) and include ±5x
- Don't quote "100k internal users" if 4x real
- Use measured from the early perf tests when available

## Output
A capacity table per tier:
```
| Tier | Current | 6mo | 1yr | Bottleneck |
```

## When
- any system design with scale claims
- upgrade decisions (load test, headroom)

## Evidence — standard practice availability engineering (SUPPORTED)