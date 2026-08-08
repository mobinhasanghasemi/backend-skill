# ARCHITECTURE GENOME

A compact, comparable representation of an architecture. Enables before/after comparison, alternative evaluation, and progression tracking.

## Genome fields

```yaml
Style:            monolithic | modular-monolith | microservices | serverless | event-driven | ...
Language(s):      python/django, go, node...
Database:         postgresql | mysql | nosql | multi (with justification)
Cache:            none | redis | memcached | semantic | ...
Messaging:        none | queue | stream (rabbitmq/kafka/...)
Storage:          object-store | filesystem | s3 | ...
API style:        rest | graphql | grpc | websocket | webhooks
Authentication:   session | token | jwt | oauth2/oidc | api-key
Authorization:    none | rbac | abac | object-level
Deployment:       vm | containers | k8s | serverless | edge
Scaling:          vertical | horizontal | auto | elasticity
Consistency:      strong | eventual | read-after-write | ...
Observability:    logs | metrics | tracing | otel | dashboards
Security:         (tls, secrets, rate-limit, audit...)
Availability:     % target (with basis)
RPO/RTO:          numbers
```

## Comparison template (for candidate selection)

For candidate A vs B, table:

| Dimension | A | B |
|---|---|---|
| Complexity | ... | ... |
| Cost (dev) | ... | ... |
| Cost (ops) | ... | ... |
| Performance | ... | ... |
| Security | ... | ... |
| Reliability | ... | ... |
| Scalability | ... | ... |
| Operability | ... | ... |
| Migration | ... | ... |
| Failure modes | ... | ... |

## When the genome is used

- Before any big decision (evaluate + compare)
- After a decision (record the chosen genome — ADR helper)
- During evolution review (diff against genome history)

## Amending the genome

When the architecture evolves, diff old vs new:

```text
Old: postgres + no cache + monolith + vm
New: postgres + redis cache + modular monolith + containers
→ diff: +cache (why), +containers (why), +modularization (why)
```

Every diff line requires a constraint/evidence note. If a diff is unjustified, SIMPLICITY_GOVERNOR fires.