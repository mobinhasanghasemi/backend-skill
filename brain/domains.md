# brain/domains.md

Index of the 20 domain regions and their trigger signals. Each domain is a folder with a ROOT.md.

## Domain table

| ID | Path | Type | Typical triggers |
|---|---|---|---|
| architecture | architecture/ | patterns & evolution | "how to structure", pattern choice, evolution |
| api | api/ | interface | REST/GraphQL/versioning/environments/webhooks |
| databases | databases/ | storage & models | persistence, data, SQL, transactions |
| security | security/ | cross-cutting | auth, encryption, ALL perimeter decisions |
| performance | performance/ | cross-cutting | latency, profiling, throughput |
| distributed-systems | distributed-systems/ | cross-cutting | consistency, retries, partitions, GUARANTEES |
| reliability | reliability/ | cross-cutting | availability, failure, RPO/RTO |
| observability | observability/ | cross-cutting | metrics, tracing, logs, alerting |
| testing | testing/ | RO goal | testing strategy, tooling |
| python | python/ | language | python env, GIL, asyncio, packaging |
| django | django/ | framework | django runtime, ORM, DRF |
| messaging | messaging/ | broker | queues, streams, DLQs |
| caching | caching/ | cross-cutting | caching strategy, invalidation |
| ai-backends | ai-backends/ | modern concern | LLM, RAG, vector, agents |
| multi-tenancy | multi-tenancy/ | cross-cutting | tenant isolation, B2B SaaS |
| infrastructure | infrastructure/ | base | containers, k8s, deploy, serverless |
| devops | devops/ | ops | CI/CD, IaC, GitOps |
| data-engineering | data-engineering/ | pipelines | batch, stream processing |
| storage | storage/ | cross-cutting | object storage, files, archiving |
| real-time | (in api/) | arrays | websockets, events |

## Activation hints per domain

- **architecture** — activates whenever a "system" or "solution" is designed or reviewed
- **security** — activates with **any** datastore/credential/API/perimeter mention. Non-negotiable.
- **performance** — activates on "slow", "scaling", "latency", "optimiz."
- **distributed-systems** — activates when multiple (nodes/services/clients) need coordination; retries, idempotency, consistency, consensus.
- **reliability** — activates for prod-grade claims, RPO/RTO, backups, HA.
- **observability** — activates when the design touches production runtime.

## Overlap policy

Each concern stays in its primary domain. Cross-domain logic lives as **links** not copies (see `brain/relationships.md`). If knowledge fits two domains, it lives in the higher-specificity one and links to the sibling.

## Domain updates

Add a new region only when it passes the simplicity governor (a topic can't be served by link + existing ROOT). Then: create ROOT.md, add to graph, add to table here, add to version-awareness (if tech), add route entries in `NEURAL_ROUTING.md`.