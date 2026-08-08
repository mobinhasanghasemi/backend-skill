# brain/relationships.md

Relationship registry. This file documents the allowed graphs, typical strengths, and how a relationship should influence reasoning.

## Relationship types (canonical)

| Type | Value | Example instance |
|---|---|---|
| depends_on | A's truth needs B | `database.mvcc` depends_on `database.transactions` |
| requires | hard prerequisite | `database.replication` requires `database.configured-failover` |
| influences | A shapes B's behavior | `api.rest` influences `api.error-design` |
| causes | A creates B | `database.index` provokes `btree-write-overhead` |
| mitigates | A reduces failure B | `distributed.retries` mitigates `network transient failure` |
| protects_against | A defends B | `security.authn` protects `api` |
| conflicts_with | trade-off | `cache` conflicts with `consistency` |
| complements | works together | `rabbitmq` complements `saga` |
| alternative_to | replaceable | `kafka` alternative_to `rabbitmq` (workload) |
| specializes | subconcept | `btree` specializes `index` |
| generalizes | broadens | `index` generalizes `btree` |
| implements | concrete device | `k8s deployment` implements `zero-downtime` pattern |
| integrates_with | inter-op | `django.orm` integrates_with `postgresql` |
| scales_with | elasticity | `read-replicas` scale_with `read work` |
| constrained_by | bounds | `encryption` constrained_by `db-function` |
| observed_by | telemetry | `db slow queries` observed_by `pg_stat_statements` |
| validated_by | proof | `indexclause` validated_by `EXPLAIN ANALYZE` |
| evolves_into | growth | `monolith` evolves_into `modular-...` |
| replaced_by | superseded | `zookeeper` replaced_by `kraft` |
| deprecated_by | removed | `MD5 auth` deprecated_by `SCRAM` (PostgreSQL 18) |

## Relationship strength

Each connection carries a weight hint:

- **strong**: immediately relevant (e.g., `django.orm` ↔ `database.postgresql` when coding Django)
- **medium**: relevant under conditions (`indexing` ↔ `cache` when reads hot)
- **weak**: rarely relevant (e.g., `websockets` ↔ `data-engineering`)

Neurons should state strength in the Connected Neurons block (`strong`/`medium`/`weak`).

## Structure requirement

Every neuron's `Connected Neurons` must list 3–6 cross-domain links (not more) to keep the graph sparse-but-connected. A list of 15 links defeats routing (attention dilution).

## Known specific edges (select, but canonical)

| From | To | Type |
|---|---|---|
| database.postgresql | performance.query-optimization | influences (strong) |
| api.idempotency | distributed.retry | complements |
| cache.strategy | consistency | conflicts (staleness) |
| ai.prompt-injection | security | special (guard) |
| reliability.dr | database.backup | depends |
| multi-tenant.isolation | security.authorization | depends |
| observability.otel | distributed.tracing | implements? |
| devops.canary | reliability | mitigates |

## Modeling new relationships

When adding a neuron: for each new relationship ask — "what is the *causal* mechanism?"; if none, it's noise; drop it. Record only causal/semantic edges.

## Graphs with special semantics

- **Failure edges**: when A's failure → B's failure (see `brain/failure-propagation.md`); mark with `⚠`.
- **Consistency edges**: query-after-cache-read staleness; eventual semantics (mark `eventual`).