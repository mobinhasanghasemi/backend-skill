# brain/routing.md

The routing tables used to translate a problem into activated neurons. This is the processing layer.

## Routing rules (keyword/topic → domain)

| Topic pattern | Activation |
|---|---|
| `transaction`, `consistency`, `atomic` | database.relational + database.postgresql.transactions |
| `query slow`, `index`, `EXPLAIN`, N+1 | databases/optimization + postgresql.query-planner |
| `design`, `structure`, `overview` | architecture/ROOT + patterns |
| `coupling`, `splitting services`, `scale-out` | architecture.patterns.microservices, distributed |
| `authn`, `login`, `token`, `jwt`, `session` | security.authentication + oauth-oidc |
| `authz`, `permission`, `role`, `ACL`, `IDOR` | security.authorization |
| `secrets`, `credentials`, `vault` | security.secrets |
| `crypto`, `encrypt`, `signature`, `TLS` | security.cryptography |
| `rate limit`, `throttle` | api.rate-limiting + security |
| `idempotency`, `retry`, `backoff` | distributed-system.idempotency + retry |
| `circuit breaker`, `timeout` | distributed.circuit-breaker |
| `queue`, `celery`, `background job` | messaging.queues + django.background-jobs |
| `event`, `message bus`, `pub/sub`, `stream` | messaging.streams |
| `saga`, `compensation`, `distributed tx` | distributed.sag.cas |
| `prediction`, `RAG`, `LLM`, `agent`, `prompt` | ai-backends.ROOT (+security) |
| `vector`, `embedding`, `similarity` | ai-backends + databases/nosql/vector |
| `availability`, `SLO`, `RPO/RTO`, `failover` | reliability.ROOT |
| `monitoring`, `metrics`, `tracing`, `otel` | observability.ROOT |
| `docker`, `k8s`, `container`, `deploy` | infrastructure + devops |
| `Ci/cd`, `pipeline`, `gitops` | devops.ROOT |
| `backup`, `restore`, `PITR` | reliability.backup-disaster-recovery |
| `DTO`, `input validation`, `ORM` | python/django as applicable |
| `webhook`, `outbound integration` | api.webhooks + security.webhooks |
| `websocket`, `channel`, `real-time` | api.websockets |

### Branching logic (ROOT decision trees)

Archetypes:

1. **"I have problem X"** → activation on X's domain first; when the problem *ripples*, follow the domain's Connected Neurons.
2. **"Which DB?"** → databases ROOT; mandatory questions (workload, consistency, scale) gate candidates.
3. **"Should I microservice?"** → architecture ROOT + SIMPLICITY_GOVERNOR; pattern activation only after check.
4. **"System is slow"** → performance ROOT first (measure each time), conversations with profiling neuron.
5. **"Design this API"** → api ROOT + api.rest/graphql + security guard.
6. **"Design system with AI"** → ai-backends ROOT + security + money/latency.

### Fallback

If no routing rule matches, fall to **general** problem-solving: requirements → constraints → simplest solution → iterate.