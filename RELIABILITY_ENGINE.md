# RELIABILITY ENGINE

Availability, durability, resilience, failure propagation, and recovery. Reliability is engineered, not observed — every neuron's Reliability section must define behavior under failure, not just success.

## Core equations

```text
Availability = uptime / total time
          1 9   = 90%      → ~36.5 days downtime / year
          2 9   = 99%      → ~3.65 days
          3 9   = 99.9%    → ~8.76 hours
          4 9   = 99.99%   → ~52.6 minutes
          5 9   = 99.999%  → ~5.26 minutes

System availability ≈ product of component availabilities (serial path)
  → 0.999 × 0.999 × 0.999 ≈ 0.997 (3 nines of dependencies cost you one nine)
```

RPO (Recovery Point Objective) = max acceptable data loss; RTO (Recovery Time Objective) = max acceptable downtime. They dictate backup cadence & failover topology, not the other way around.

## Design-for-failure checklist

- Every component: what happens when it fails? (documented)
- Timeouts on every external call (connect, read, write) — no default-infinite
- Retries with exponential backoff + jitter, bounded
- Idempotency keys for non-idempotent operations
- Circuit breaker at the integration boundary
- Bulkheads (separate pools / queues per critical consumer)
- Health checks: liveness (is it alive) vs readiness (can it serve)
- Graceful degradation: degrade features, don't crash
- Dead letter path (unprocessed items visible, not silently dropped)
- Backpressure (consumer cannot keep up → push back, don't buffer unbounded)
- Observability of the failure itself (see observability/)

## Failure propagation thinking (the primary skill)

Model each failure's cascade:

```text
DB slow
  → requests wait
  → connection pool exhaustion
  → queue growth
  → latency → timeouts
  → client retries
  → extra load → DB more saturated
  → cascade (feedback loop)
```

Feedback loops amplify; detect and break them (retry ceilings, load shedding, circuit breakers, bulkheads).

## Redundancy patterns

| Pattern | Guarantee | Cost |
|---|---|---|
| Hot standby (sync replication) | zero-ish loss, fast failover | write latency, ops |
| Async replica | loss window, fast recovery | simpler |
| Multi-AZ / multi-region | geographic failure domain | network, latency, DR process |
| Read replicas | read scaling (not durability alone) | eventual consistency on reads |

## Recovery drills

- Restore from backup monthly (at least quarterly) — untested backup ≈ no backup
- Chaos tests: kill a node, kill a DB, cut network, kill a cache
- Document runbook per class of incident (playbooks/)

## Backup & DR neuron

- Full + PITR (WAL archiving for PG) or equivalent; verify restorability
- Encrypt backups; store off-site (different failure domain)
- Retention policy matched to compliance

## Availability anti-patterns

- ❌ 99.99% promise with single instance + nightly backups only
- ❌ Retry-forever loops (amplify failures)
- ❌ Load balancer without health-check-strip of dead nodes
- ❌ No capacity headroom for traffic spike (simulate)
- ❌ Relying on "the cloud will fix it" — design failure isolation yourself

## Interaction

- Reliability checks appear in every ROOT.md (RPO/RTO where relevant)
- Playbooks = procedure memory for incidents
- `brain/failure-propagation.md` = library of cascade models