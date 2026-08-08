# Deep Synchronous Chains

## Identity
- ID: architecture.anti-patterns.sync-chains
- Severity: HIGH

## Definition
A request passes through many synchronous network hops (A → B → C → D) to complete.

## Causal chain of damage
```
more hops
→ latency = sum of each
→ any downstream failure = whole request fails
→ retries amplify load
→ p99 grows the chain
```

## Symptom signals
- p95 much worse than p50 (one slow downstream pollutes everything)
- timeouts on request at the edge
- "why is order creation calling the search index synchronously?"

## Corrective
- **Async decoupling**: non-critical path → event/queue (event-driven)
- **BFF aggregation**: one hop instead of chain (bff.md)
- Read replicas for joins
- Caching hot data

## Defense in depth
Even when the chain is required: per-hop timeouts, circuit breakers, retry budget, queue backups.

## Evidence
- Cascade failures documented at scale (Google SRE; Amazon outages latent) — combine with failure-propagation