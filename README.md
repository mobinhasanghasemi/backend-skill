# BACKEND ARCHITECT NEURAL

**An AI-native backend engineering knowledge base.**

Organized as a neural knowledge graph — every file is a **neuron** with a defined purpose, activation conditions, and causal relationships. Built for AI agents (Claude, ChatGPT, Cursor, Codex, MiMoCode, and others) to dynamically activate only the relevant knowledge, apply quality gates, and produce production-grade decisions with reasoning traces.

```
Repository: https://github.com/mobinhasanghasemi/backend-skill
```

---

## Table of Contents

- [What is this?](#what-is-this)
- [How it Works — Neural Architecture](#how-it-works--neural-architecture)
  - [Cognitive Pipeline](#cognitive-pipeline)
  - [Routing & Activation](#routing--activation)
  - [The 4 Quality Engines](#the-4-quality-engines)
  - [Evidence Protocol](#evidence-protocol)
  - [Code Tiers](#code-tiers)
  - [Architecture Linter](#architecture-linter)
- [What's Inside](#whats-inside)
  - [Knowledge Domains](#knowledge-domains)
  - [Protocols & Engines](#protocols--engines)
  - [Brain](#brain)
  - [Playbooks](#playbooks)
  - [Checklists](#checklists)
  - [Integrity Tools](#integrity-tools)
- [Installation](#installation)
- [How the Agent Should Use It](#how-the-agent-should-use-it)
- [Strengths & Current Limitations](#strengths--current-limitations)
- [License](#license)

---

## What is this?

This is a **pure Markdown knowledge base** with zero dependencies. It's called "Neural" because it's modeled as a brain:

- **Neurons** = individual Markdown files, each containing a focused piece of backend knowledge.
- **Root neurons** (`ROOT.md`) = routers that tell the agent which child neurons to read.
- **Graph** = explicit connections between neurons (`depends_on`, `influences`, `conflicts_with`, etc.).
- **Engines** = always-on quality layers that filter every decision through security, simplicity, performance, and reliability lenses.
- **Evidence** = every claim carries a confidence label (VERIFIED / SUPPORTED / INFERRED / EXPERIMENTAL / UNCERTAIN), preventing hallucination.

The agent never reads the whole tree. It follows the graph, activating only the neurons relevant to the question.

---

## How it Works — Neural Architecture

### Cognitive Pipeline

When the agent receives a question, it follows this pipeline (defined in `BRAIN.md`):

```
USER INPUT
    │
    ▼
PERCEPTION              ← parse problem, language, scope
    ▼
PROBLEM CLASSIFICATION  ← what kind of problem is this?
    ▼
CONSTRAINT EXTRACTION   ← scale, budget, team, compliance, deadlines
    ▼
RISK DETECTION          ← early suspicions (security, reliability, latency)
    ▼
DOMAIN DETECTION        ← which regions fire?
    ▼
ROOT NEURON ACTIVATION  ← read domain ROOT.md only
    ▼
CHILD NEURON ACTIVATION ← read only relevant children
    ▼
CROSS-DOMAIN TRAVERSAL  ← follow Connected Neurons
    ▼
CAUSAL REASONING        ← build cause→effect chains (positive AND negative)
    ▼
CANDIDATE GENERATION    ← at least 2 options, rarely more than 3
    ▼
TRADE-OFF ANALYSIS      ← complexity/cost/security/performance/ops
    ▼
RISK ANALYSIS           ← failure propagation, feedback loops
    ▼
SECURITY REVIEW         ← SECURITY_GUARDIAN.md
    ▼
PERFORMANCE REVIEW      ← PERFORMANCE_ENGINE.md
    ▼
RELIABILITY REVIEW      ← RELIABILITY_ENGINE.md
    ▼
SIMPLICITY GOVERNOR     ← does complexity justify itself?
    ▼
VALIDATION              ← check against ARCHITECTURE_LINTER.md
    ▼
FINAL ARCHITECTURE      ← recommendation + reasoning trace + risks
    ▼
OUTPUT                  ← explain EXACTLY why this decision
```

### Routing & Activation

Defined in `NEURAL_ROUTING.md` and `brain/routing.md`. The agent decides which domain to activate based on keyword matching:

| Input | Domain activated |
|-------|-----------------|
| "database", "schema", "SQL" | `databases/ROOT.md` |
| "API", "endpoint", "versioning" | `api/ROOT.md` |
| "security", "auth", "token" | `security/ROOT.md` |
| "slow", "latency", "profiling" | `performance/ROOT.md` |
| "Django", "DRF", "migration" | `django/ROOT.md` |
| "docker", "k8s", "deploy" | `infrastructure/ROOT.md` |
| "reliability", "RPO", "disaster" | `reliability/ROOT.md` |
| "LLM", "RAG", "agent" | `ai-backends/ROOT.md` |

Three attention states: **ACTIVE** (read fully), **SUPPORTING** (read relevant sections), **DORMANT** (skip). The agent never exceeds ~2 active + ~4 supporting domains.

### The 4 Quality Engines

These are always-on and filter every decision:

| Engine | File | Function |
|--------|------|----------|
| **Security** | `SECURITY_GUARDIAN.md` | Threat modeling, authN/authZ, data protection, OWASP, compliance |
| **Simplicity** | `SIMPLICITY_GOVERNOR.md` | Rejects unearned complexity. Default positions: monolith, single DB, no cache until measured |
| **Performance** | `PERFORMANCE_ENGINE.md` | Measure first, then optimize. No optimization without profiling |
| **Reliability** | `RELIABILITY_ENGINE.md` | SLOs, error budgets, failure propagation, RPO/RTO, backup drills |

### Evidence Protocol

Every factual claim in the knowledge base carries one of these labels (defined in `EVIDENCE_PROTOCOL.md`):

| Class | Meaning |
|-------|---------|
| **VERIFIED** | Confirmed from an official authoritative source |
| **SUPPORTED** | Strong corroboration from multiple credible sources |
| **INFERRED** | Derived from established principles + reasoning |
| **EXPERIMENTAL** | New, not production-proven (lab/benchmark only) |
| **UNCERTAIN** | Can't verify, contradictory, or unknown |
| **OUTDATED** | Was once true, superseded by version changes |
| **DEPRECATED** | Officially no longer recommended |

This prevents the agent from presenting unverified or hallucinated information as fact.

### Code Tiers

Practical neurons include a 4-tier code ladder (defined in `CODE_TIERS.md`):

| Tier | Label | Purpose |
|------|-------|---------|
| ❌ | Bad | The common misstep — realistic, shows the failure it causes |
| ✅ | Good | Minimal correct approach |
| ⚡ | Better | One meaningful quality upgrade (perf/security/observability) |
| 🏆 | Excellent | Production-grade — measured, bounded, observable, fault-tolerant |

The agent picks the appropriate tier based on context (a toy system may be fine with ✅ or even ❌).

### Architecture Linter

`ARCHITECTURE_LINTER.md` defines 35 machine-checkable anti-pattern rules (ARCH001–ARCH035):

| Severity | Approx. count | Examples |
|----------|---------------|---------|
| CRITICAL | 5 | Secrets in code (ARCH017), SQL injection (ARCH031), cross-tenant cache leak (ARCH025) |
| HIGH | 14 | No timeout (ARCH001), no idempotency (ARCH002), no invalidation strategy (ARCH003) |
| MED | 15 | N+1 (ARCH007), no pagination (ARCH030), no circuit breaker (ARCH032) |
| LOW | 1 | SELECT * (ARCH035) |

---

## What's Inside

### Knowledge Domains

| Directory | Covers | Files |
|-----------|--------|-------|
| `architecture/` | Patterns, anti-patterns, evolution, system design | ~5 |
| `api/` | REST, GraphQL, gRPC, WebSocket, webhooks, versioning, errors, pagination, idempotency, rate-limiting | 12 |
| `databases/` | PostgreSQL, MySQL, NoSQL, query optimization, data modeling, indexing | ~10 |
| `security/` | AuthN, authZ, OWASP, cryptography, secrets, threat modeling, compliance | 9 |
| `performance/` | Profiling, latency optimization, saturation & scaling | 4 |
| `reliability/` | SLOs, backups, deployment, incident response, chaos testing | 6 |
| `observability/` | Tracing, logs, metrics, OpenTelemetry | ~2 |
| `distributed-systems/` | Timeouts, circuit breaker, saga, outbox, consensus, distributed locks | 6 |
| `messaging/` | Celery, Kafka, queues | 3 |
| `django/` | ORM, DRF, migrations, settings, caching, admin | 6 |
| `python/` | Async, typing, memory, GC, threads, packaging, web frameworks | 6 |
| `infrastructure/` | Containers, Kubernetes | 2 |
| `devops/` | CI/CD, release engineering | 2 |
| `caching/` | Strategies, invalidation | 3 |
| `testing/` | Unit, integration, contract, e2e, load, security | 6 |
| `ai-backends/` | RAG, LLM calls, agents, evals, semantic caching | 6 |
| `data-engineering/` | Batch, streaming, warehouse | 4 |
| `multi-tenancy/` | SaaS tenant isolation models | ~1 |
| `storage/` | Object storage, files, signed URLs | 2 |

> File counts are approximate; the repository continues to evolve.

### Protocols & Engines

| File | Purpose |
|------|---------|
| `SKILL.md` | Activation surface — the entry point for the agent |
| `BRAIN.md` | Central cognitive controller — the meta-chain and reasoning trace |
| `NEURAL_ROUTING.md` | Router — decides which domains activate for a given problem |
| `NEURON_PROTOCOL.md` | Neuron contract — the standard schema every knowledge file follows |
| `CODE_TIERS.md` | Code ladder — bad → good → better → excellent teaching samples |
| `DECISION_ENGINE.md` | Decision protocol — candidate evaluation + conflict resolution |
| `SECURITY_GUARDIAN.md` | Always-on security review engine |
| `PERFORMANCE_ENGINE.md` | Performance methodology — measure first, then optimize |
| `RELIABILITY_ENGINE.md` | Availability, RPO/RTO, failure propagation |
| `SIMPLICITY_GOVERNOR.md` | Rejects unearned complexity |
| `ARCHITECTURE_LINTER.md` | 35 machine-checkable anti-pattern rules (ARCH001–ARCH035) |
| `VALIDATION_PROTOCOL.md` | Neuron, research, and answer quality gates |
| `EVIDENCE_PROTOCOL.md` | Evidence classes (VERIFIED / SUPPORTED / INFERRED / …) |
| `LEARNING_SYSTEM.md` | How the brain acquires, verifies, and saves new knowledge |
| `MEMORY_PROTOCOL.md` | Three memory layers (semantic / episodic / procedural) |
| `RESEARCH_PROTOCOL.md` | Deep-research discipline before creating knowledge |
| `ARCHITECTURE_GENOME.md` | Compact, comparable architecture representation |

### Brain

| File | Purpose |
|------|---------|
| `brain/graph.md` | Global neuron graph in Mermaid — the canonical topology |
| `brain/domains.md` | Domain definitions |
| `brain/relationships.md` | Relationship types between neurons |
| `brain/routing.md` | Keyword-to-domain routing tables |
| `brain/activation.md` | Attention model, activation budget, inhibition registry |
| `brain/causal-graph.md` | Cause → effect chains (positive and negative) |
| `brain/failure-propagation.md` | 7 canonical failure cascade models |
| `brain/confidence.md` | Confidence propagation rules |
| `brain/memory.md` | Memory management |
| `brain/version-awareness.md` | Global version matrix (Python 3.14, Django 6.0, PostgreSQL 18, etc.) |

### Playbooks

16 incident runbooks in `playbooks/`:

| Playbook | Use case |
|----------|----------|
| `slow-api.md` | API latency — diagnose and fix |
| `slow-database.md` | Slow database queries |
| `memory-leak.md` | Memory leak root cause |
| `deployment-failure.md` | Failed deployment |
| `migration-lock.md` | DB migration lock |
| `queue-backlog.md` | Queue backlog |
| `capacity-spike.md` | Sudden traffic spike |
| `degraded-performance.md` | Degraded performance |
| `access-breach.md` | Access breach |
| `secret-leak.md` | Secret leakage |
| `auth-incident.md` | Authentication incident |
| `payment-duplication.md` | Duplicate payments |
| `stale-data.md` | Stale data |
| `webhook-failure.md` | Webhook failure |
| `replica-failover.md` | Replica failover |
| `incident-command.md` | Incident command structure |

### Checklists

| Checklist | Items | Purpose |
|-----------|-------|---------|
| `architecture-review.md` | 57 | Full architecture design review |
| `security-checklist.md` | 38 | Pre-release security gate |
| `code-review-checklist.md` | 40 | Backend code review |
| `release-checklist.md` | 25 | Production deploy steps |

### Integrity Tools

Python scripts in `tools/` that keep the knowledge base honest:

| Tool | Function |
|------|----------|
| `check_links.py` | Reports broken or ambiguous Markdown links |
| `validate_neurons.py` | Validates neuron schema (ID, Type, H1, H2); fails on zero files |
| `freshness.py` | Flags stale or future-dated evidence markers |

---

## Installation

This is a **pure Markdown skill** — nothing to install or compile.

**Recommended way:**

```bash
git clone https://github.com/mobinhasanghasemi/backend-skill.git
```

Then give the cloned folder as context/knowledge to your AI agent (Claude, ChatGPT, Cursor, Codex, etc.).

Alternatively, you can directly tell the agent:

```
Use this skill: https://github.com/mobinhasanghasemi/backend-skill
```

---

## How the Agent Should Use It

1. **Read `SKILL.md`** — the activation surface. It tells the agent what this skill is and when to use it.
2. **Read `BRAIN.md`** — the central cognitive controller. Understand the pipeline and the 10 non-negotiables.
3. **For any question, follow `NEURAL_ROUTING.md`** to decide which domain to activate.
4. **Load ONLY the matching domain `ROOT.md`** (e.g. `databases/ROOT.md`), then the best-matching child neuron. Never load an entire domain tree.
5. **Always apply these engines:**
   - `SECURITY_GUARDIAN.md` — security review every time
   - `SIMPLICITY_GOVERNOR.md` — reject unearned complexity
   - `PERFORMANCE_ENGINE.md` — measure before optimizing
   - `RELIABILITY_ENGINE.md` — model failure scenarios
6. **Label every factual claim** with an evidence class (VERIFIED / SUPPORTED / INFERRED / EXPERIMENTAL / UNCERTAIN) per `EVIDENCE_PROTOCOL.md`.
7. **Use code tiers** per `CODE_TIERS.md` — show the trajectory from bad to excellent, let context decide.
8. **Run the architecture linter** (`ARCHITECTURE_LINTER.md`) on the design before finalizing.
9. **Produce a reasoning trace** per `DECISION_ENGINE.md` — PROBLEM, DETECTED DOMAINS, ACTIVATED NEURONS, EVIDENCE, CONSTRAINTS, CANDIDATES, REJECTED OPTIONS, RISK ANALYSIS, TRADE-OFF MATRIX, DECISION, VALIDATION NEXT.
10. **For production incidents**, pull the matching playbook from `playbooks/`.

---

## Strengths & Current Limitations

### Strengths

- **Neural architecture** — a graph with causal relationships, not flat docs. The agent activates only relevant neurons, saving context and producing focused answers.
- **Routing system** — `NEURAL_ROUTING.md` + `brain/routing.md` give precise domain selection, so the agent never wastes context on irrelevant knowledge.
- **4 always-on quality engines** — security, simplicity, performance, and reliability filters baked into every decision.
- **Evidence protocol** — 7-level evidence classification prevents hallucination; every claim is labeled.
- **Code tiers** — a 4-level teaching ladder (❌ → ✅ → ⚡ → 🏆) with real code samples.
- **Architecture linter** — 35 machine-checkable anti-pattern rules, each with severity and fix direction.
- **16 playbooks** — production incident runbooks the agent can follow step-by-step.
- **Version awareness** — `brain/version-awareness.md` tracks exact versions and support timelines for the major tools.
- **Failure propagation models** — 7 canonical failure cascades in `brain/failure-propagation.md`.
- **Integrity tooling** — 3 Python scripts validate links, neuron structure, and evidence freshness.
- **Zero dependencies** — pure Markdown. No build step, no runtime, no package manager.

### Current Limitations

- **Verification dates** — some `Last Verified` dates reference future or unconfirmed versions; verify before relying on a version number in production.
- **Source registry** — `research/sources.md` is largely empty; evidence claims should link to verifiable sources.
- **Agent packaging** — `agents/openai.yaml` targets OpenAI; there is no equivalent packaging for Claude, MiMoCode, or Codex (though `SKILL.md` works with most agents).
- **Neuron completeness** — some neurons are missing required sections from the strict `NEURON_PROTOCOL.md` contract.
- **No automated answer tests** — the integrity tools validate the files, but there is no benchmark verifying the agent's answers.

---

## License

MIT License — see [LICENSE](LICENSE).

---

<div align="center">
  <sub>Built for the backend engineering community</sub>
  <br>
  <sub>Copyright © 2026 Mobin Hasanghasemi</sub>
</div>