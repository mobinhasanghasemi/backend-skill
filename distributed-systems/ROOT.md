# DISTRIBUTED SYSTEMS — ROOT NEURON

## Identity
- ID: distributed-systems.root
- Domain: distributed-systems
- Type: root
- Status: active
- Importance: high

## Purpose
The rules of systems with **multiple moving parts** (services, nodes, workers): failures are expected, coordination is software, and consistency is a choice with consequences — never the default.

## Activation
- multiple services/nodes/clients touch shared state
- retries, idempotency, queues, event streams, locks, transactions across services
- any "microservices" decision (pair with architecture/ROOT + SIMPLICITY_GOVERNOR)

## Routing
```text
retries/timeouts/calls   → timeouts-retries.md
events/bus               → messaging/ROOT  (kafka | celery)
shared writes            → idempotency (api/idempotency.md) + outbox.md
cross-service tx         → saga.md (NOT 2PC)
mutexes across nodes     → distributed-locks.md
dependency failures      → circuit-breaker.md (+ custody in reliability)
consistency/partitioning → distributed-systems/consensus.md thinking
```

## Core laws (the real ones)
1. **The network is unreliable** — every call may fail, hang, or deliver late; your code must survive each
2. **At-least-once is the default** — consumers must idempotent (or the outbox turns it into exactly-once enough)
3. **Consistency ≠ correctness** — choose per use-case: strong (single DB), eventual (replicas/cache), causal (sessions); pay the price consciously
4. **Time is not globally ordered** — never logic on wall clocks across nodes (for locks/tokens; use sequence/version/lamport where needed)
5. **Retries amplify** — every retry multiplies load on downstream; budget them (jitter + caps)

## Code tiers — the calling pattern
1. ❌ no timeout, no retry, direct call → hang/retry storm
2. ✅ timeout(s) + bounded retries with exponential backoff + jitter
3. ⚡ circuit breaker + fallback + idempotent retry (dedup key)
4. 🏆 whole-system view: budgeted concurrency, queues for acy, outbox, machinery/doc consistency, chaos-tested failure model

## Common failure modes
- retry storms (fail-echo loops — brain/failure-propagation)
- distributed monolith (synchronous services kneeling on every call — SIMPLICITY veto)
- 2PC wherever saga/outbox fits
- locks with TTL under long jobs (fencing missing)
- assumptions on clock/order in partitioned systems

## Security/reliability/performance
- untrusted message paths → authN on producers (see messaging), schema integrity
- cost balloons (per-call) — measure and set quotas
- reliability engine for failures (backup/DR per node)

## Evidence
- DDD & patterns catalog (Kleppmann "Designing Data-Intensive Applications" — VERIFIED concepts), CP/AP theory (Gilbert & Lynch proof — mathematical basis, stable)