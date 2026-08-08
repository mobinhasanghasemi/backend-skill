# brain/causal-graph.md

The brain does not store only associations — it stores **causality**: cause → effect chains, including negative side-effects. This file documents the canonical causal paths across domains.

## Canonical couplings (positive)

```
Retrieval caching
  ↓
repeated reads served from memory
  ↓
DB read pressure falls
  ↓
DB contention falls
  ↓
latency of DB-dependent paths falls
```

```
Index on hot predicate
  ↓
plan switches from seq scan to index scan
  ↓
per-read IO drops
  ↓
rows served per-second rises
```

```
Queue decouples producer/consumer
  ↓
fast burst absorbed
  ↓
degradation becomes lag not error
  ↓
user-visible failures drop
```

```
Replication (read replicas)
  ↓
read pressure off primary
  ↓
primary write capacity preserved
```

## Negative couplings (must be modeled)

```
Caching introduces
  ↓
invalidation complexity
  ↓
stale data risk
  ↓
consistency violations tractable only sometimes → user-visible error
```

```
Microservices modularity
  ↓
but: network partition
  ↓
partial failure
  ↓
retry storms
  ↓
global degradation
```

```
Event-driven decoupling
  ↓
but: ordering assumptions
  ↓
two consumers read in different order
  ↓
data incoherence / dedupe gaps
```

## Feedback loops to detect

The failure-propagation file (brain/failure-propagation.md) documents loops; recognition here:

- Retry loop (client retry × server timeout): load × fail echo
- Connection-pool exhaustion loop
- Replica lag → read-your-write returns stale → user retries → more reads
- Deadlock starvation.

The causal form: a *positive feedback* loop; break at one of its edges (backoff caps, circuit, timeout, shed).

## The 2-step causal trace format

For a decision:

```
fact: X
causal chain: X → A → B → C
side effects (negative): X → D (consistency cost)
```

Writing the chain forces noticing nonobvious effects.

## Causal graph use in reasoning

1. For every candidate in a decision → write 2 chains (positive + negative).
2. For each chain, locate where to cut it (mitigations).
3. The decision must have cheap mitigations for its hardest negative chain (else reject candidate).

## Adding new causal edges

Rules (from relationships.md): a causal edge needs a mechanism, not word co-occurrence. If you can't explain *why* A→B, the edge is inference-grade and must be marked INFERRED.