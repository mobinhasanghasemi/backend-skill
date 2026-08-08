# brain/activation.md

Attention model and inhibitory knowledge. Defines which neurons burn and which must be suppressed.

## Attention states

| State | Meaning | Example |
|---|---|---|
| ACTIVE | read fully | The DB-neuron when the whole task is about storage |
| SUPPORTING | read only the relevant section | Observability when discussing cache hit ratio |
| DORMANT | skip | Nothing in an auth task if it isn't a security concern |

## The four signals

1. semantic match — the three overlap
2. causal path — sits between problem and requirement
3. risk signal — security/reliability/compliance raises weight
4. constraint hit — constraints (team, scale, existing stack) force neuron relevance

Critical rule: When security is relevant, its weight can veto the router; e.g., sensitive data + caching → must read security-invalidation claims even if "it's just a cache".

## Attention weight fields

```
relevance      (degree of semantic/physical match)
importance     (domain importance of that neuron)
confidence     (evidence class)
connection_strength (weight: strong/medium/weak)
context_fit    (does environment fit the neuron's assumptions)
risk           (security/reliability criticality)
```

Sum > ACTIVE threshold → ACTIVE; > SUPPORTING → SUPPORTING; else DORMANT. Keep this a light intuition, not a math tool.

## Activation budget

- Don't exceed ~2 domains active + ~4 supporting unless the problem is genuinely cross-disciplinary (then 4+2).
- Each additional neuron costs reading, contradictions surface — be frugal.
- When the answer is simple, stay simple: activation of one ROBOT and one child is normal.

## Inhibition registry

Well-known "not for..." — the governor's knowledge. The task: when these are candidates, the router must run the inhibitor:

**Technology → discouraged for**

| Technology | Discourage when | Because | Suggested |
|---|---|---|---|
| microservices | single domain, no independent scaling, ≤1 team | adds coordination costs, ops | monolith |
| Kubernetes | single small server, small traffic | adds platform overhead | single VM/docker-compose |
| event-sourcing | basic CRUD, no agg that needs full history | replay/event-schema complexity | normal persistence |
| CQRS | single read model | doubles commands/reads behind a cache instead |
| distributed cache | cache complexity > value (cache <= few reads) | consistency + ops | direct DB + maybe read replica |
| kafka | <10k events/s and no ordering needs | ops burden (ZK, retention) | rabbitmq/queue table |
| multi-region | no user base reason | latency/licensing/DR cost | single-region + backups |
| sharding | writes within capacity of one node | rebalancing burden | scale-up / partition / replica |
| serverless | long-running jobs, warm start problems | cold start & costs for always-on | containers/VM |
| feature flag infra | flag count < 10 | complexity | env vars on deploy |

### When NOT to inhibit

- Compliance requires the tech regardless of size (e.g., audit logs with event store).
- User reported measured constraint (traffic, SLA) that actually demands it.
- Explicit engineering decision demands it (and the ADR records why).

## Inhibitor output

When someone proposes a component that the inhibitor flags:

```
WARN <component>: for <context> 
  reason: ...
  simpler alternative: ...
  condition to change this: ...
```

If the concern passes the inhibitor, activation happens normally.

## Attention updates during dialogue

- If the user reveals scale ("actually 50M rows") → reweight database ~ scalability.
- If user says "internal tool" → drop reliability/performance weights, raise simplicity.
- If user says "we have no ops team" → raise conservative (fewer components) weights.

Always re-check attention after a new constraint; the first state is provisional.