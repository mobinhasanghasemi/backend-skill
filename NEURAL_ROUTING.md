# NEURAL ROUTING

How the AI decides which knowledge to activate for a given problem.

---

## The Routing Pipeline (mandatory for non-trivial questions)

```text
User Input
    │
    ▼
Intent Detection        ── what KIND of question? (decision / diagnostic / review / learning)
    │
    ▼
Problem Classification  ── which high-level problem? (storage / api / security / scale / ...)
    │
    ▼
Constraint Extraction   ── scale, budget, time, team, compliance, data sensitivity
    │
    ▼
Entity Extraction       ── named technologies, frameworks, components
    │
    ▼
Risk Detection          ── security / reliability / performance signals
    │
    ▼
Domain Detection        ── map problem → domain regions (see brain/domains.md)
    │
    ▼
Root Neuron Activation ── pick up domain ROOT.md files
    │
    ▼
Child Neuron Activation ── follow ROOT routing to specific neurons
    │
    ▼
Cross-Domain Traversal  ── follow relationship links (depends_on, integrates_with...)
    │
    ▼
Causal Reasoning         ── build cause→effect chains (brain/causal-graph.md)
    │
    ▼
Decision
```

---

## Domain Detection decisions table

Given the inputs, activate these domains:

| Input signal | Domains to activate (highest first) |
|---|---|
| "database", "schema", "SQL", "durability" | databases, caching (if reads), performance |
| "API", "endpoint", "error", "versioning", "contract" | api, security |
| "security", "auth", "authorization", "token", "secrets" | security |
| "performance", "slow", "latency", "profiling", "benchmark" | performance, databases/optimization |
| "scale", "traffic", "millions of users", "region" | distributed-systems, reliability |
| "distributed", "event", "queue", "stream", "saga" | messaging, distributed-systems, event-driven (architecture) |
| "reliability", "availability", "downtime", "RPO", "disaster" | reliability, observability |
| "monitoring", "logs", "metrics", "tracing", "alert" | observability |
| "testing", "test pipeline", "CI" | testing, devops |
| Django/Python entity | python, django (framework) + the cross domain for the actual problem |
| "docker", "k8s", "kubernetes", "deploy" | infrastructure, devops, cloud |
| "LLM", "rag", "prompt", "AI" | ai-backends, security (prompt safety) |
| "payment", "money", "multi-region" | distributed (double-activation with reliability) |
| unknown | probe questions: requirements? scale? data? team? |

Always **start conservative**: one domain ROOT at a time, add domains only when the problem demands.

---

## Constraint extraction (do this BEFORE activating neurons)

Ask (or infer from the prompt) the important constraints:

- Throughput and latency expectations
- Scale now vs in 18 months
- Consistency requirements (hard: money, inventory; soft: analytics, feed)
- Durability/permanence (financial records, audit)
- Security obligations (GDPR / PCI / SOC2 / HIPAA)
- Team size and expertise
- Operational capability (existing alerting, on-call)
- Budget
- Hard environmental constraints (cloud provider, region, legacy, connections)

If the constraints are absent, **state the missing information** in the answer, don't assume.

---

## Entity extraction → neuron map

When user mentions: `PostgreSQL`, `Django`, `Redis`, `Kafka`, `Kubernetes` → route to:

| Entity         | Primary neuron |
|----------------|----------------|
| PostgreSQL 18     | databases/postgresql/ROOT.md |
| Django 5/6        | django/ROOT.md |
| Django REST framework | django/drf.md |
| Redis             | databases/nosql/redis.md + caching/ROOT.md |
| Kafka             | messaging/kafka.md |
| Celery            | messaging/celery.md (and messaging/kafka.md) |
| Docker/K8s        | infrastructure/kubernetes.md |
| OpenTelemetry     | observability/tracing.md |
| JWT/OAuth         | security/authentication.md |
| RAG/LLM → ai-backends/ | ai-backends/rag.md |

For volume, don't chase every last entity. Prioritize by what governs the decision.

---

## Cross-domain traversal trigger

After reading a domain neuron, check its **Connected Neurons** list and hop ONLY if:

- a concept in the current scope interacts with it (e.g., isolation needs concurrency)
- the problem has a ripple effect (e.g., adding Kafka → failure analysis, observability)

End when returning to original domain with a complete decision.

---

## Routing Anti-Patterns (Do NOT)

- ❌ Reading the entire skill to find anything.
- ❌ Jumping to `microservices.md` because the word "scale" was used.
- ❌ Following every link; following the causal path only.
- ❌ Ignoring the security link for traffic-adjacent design.
- ❌ Directing the user to `playbooks/x` when the task is design (they're for incidents).