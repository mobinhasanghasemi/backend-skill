# BACKEND ARCHITECT NEURAL

<p align="center">
  <a href="https://github.com/mobinhasanghasemi/backend-skill">
    <img src="https://img.shields.io/badge/GitHub-Repo-blue?logo=github" alt="GitHub">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
  </a>
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Status Active">
  <img src="https://img.shields.io/badge/Last%20Updated-2026--08-brightgreen" alt="Last Updated">
</p>

An **AI-readable artificial engineering brain for backend architecture**. Knowledge is stored as interconnected Markdown **neurons**. An AI dynamically routes through the graph, activates only the relevant neurons, reasons causally, checks security / performance / reliability, and produces production-grade decisions with reasoning traces.

This repository is a **pure knowledge pack** — no runtime dependencies, no build step for the core. It is designed both for **direct consumption by AI agents** (Claude, ChatGPT, Codex, MiMoCode, …) and for **human study** as a reference library.

**Repository:** `https://github.com/mobinhasanghasemi/backend-skill`

---

## Table of Contents

- [Repository](#repository)
- [What is this project?](#what-is-this-project)
- [Quick Start](#quick-start)
  - [Option A — Use it as an Agent Skill (recommended)](#option-a--use-it-as-an-agent-skill-recommended)
  - [Option B — Read it yourself](#option-b--read-it-yourself)
- [Deployment Guide — Host it as a Docs Site](#deployment-guide--host-it-as-a-docs-site)
  - [Option 1: GitHub Pages (zero-cost, simplest)](#option-1-github-pages-zero-cost-simplest)
  - [Option 2: Vercel](#option-2-vercel)
  - [Option 3: MkDocs (professional docs site)](#option-3-mkdocs-professional-docs-site)
  - [Option 4: Docusaurus](#option-4-docusaurus)
- [Directory Map](#directory-map)
- [Core Protocols & Engines](#core-protocols--engines)
- [Knowledge Domains](#knowledge-domains)
- [Playbooks](#playbooks)
- [Checklists](#checklists)
- [Integrity Tools](#integrity-tools)
- [Contributing](#contributing)
- [License](#license)

---

## Repository

```
https://github.com/mobinhasanghasemi/backend-skill
```

Clone it:

```bash
git clone https://github.com/mobinhasanghasemi/backend-skill.git
cd backend-skill
```

---

## What is this project?

**Backend Architect Neural** is a structured backend-engineering knowledge base organized as a neural network of Markdown files. Every file is a **neuron** that defines its own *purpose*, *activation conditions*, *relationships*, and *decision rules*. The project covers:

- **25+ knowledge domains** — from Django, PostgreSQL, and Redis to security, reliability, and AI backends.
- **150+ neuron files** with a strict schema (`NEURON_PROTOCOL.md`).
- **16 incident playbooks** for production troubleshooting.
- **4 checklists** — architecture, security, code review, and release.
- **3 integrity tools** — link checker, neuron validator, and evidence freshness reporter.
- **Decision engines** — security, performance, reliability, and simplicity governors.

The core is **language-agnostic for AI consumption**: it works with any agent that can read Markdown and follow the routing rules in `NEURAL_ROUTING.md`.

---

## Quick Start

### Option A — Use it as an Agent Skill (recommended)

Give your agent the following context. The agent will read `SKILL.md` as its entry point, then activate only the neurons relevant to your question.

**Prompt to give your agent:**

> You have access to a backend-engineering knowledge base. The source is this GitHub repository:
>
> `https://github.com/mobinhasanghasemi/backend-skill`
>
> **Install/load instructions:**
> 1. Clone the repo: `git clone https://github.com/mobinhasanghasemi/backend-skill.git`
> 2. Read `SKILL.md` first — it is the activation surface and tells you how to behave.
> 3. Read `BRAIN.md` once — it is the central cognitive controller (the meta-chain).
> 4. For any question, follow `NEURAL_ROUTING.md` to decide which domain to activate.
> 5. Load ONLY the matching domain `ROOT.md` (e.g. `databases/ROOT.md`), then the best-matching child neuron. Never load an entire domain tree.
> 6. Apply the engines by default: `SECURITY_GUARDIAN.md`, `SIMPLICITY_GOVERNOR.md`, `PERFORMANCE_ENGINE.md`, `RELIABILITY_ENGINE.md`.
> 7. Label every factual claim with an evidence class (VERIFIED / SUPPORTED / INFERRED / EXPERIMENTAL / UNCERTAIN) per `EVIDENCE_PROTOCOL.md`.
> 8. For production incidents, pull the matching playbook from `playbooks/`.

You can phrase it as a one-liner to your agent:

> Load the backend skill from `https://github.com/mobinhasanghasemi/backend-skill.git` (clone it, read `SKILL.md` + `BRAIN.md`, then follow `NEURAL_ROUTING.md` to answer my question).

### Option B — Read it yourself

1. Start at `BRAIN.md` — the cognitive controller. It explains the pipeline, activation states, and reasoning trace.
2. Pick a domain from the table below and open its `ROOT.md` for the routing map.
3. Drill into the specific neuron files you need.

```text
How to route your question:
  "database / schema / SQL"        → databases/ROOT.md
  "API / endpoint / versioning"    → api/ROOT.md
  "security / auth / tokens"       → security/ROOT.md
  "slow / latency / profiling"     → performance/ROOT.md
  "Django / DRF / migrations"      → django/ROOT.md
  "docker / k8s / deploy"          → infrastructure/ROOT.md
  "reliability / RPO / disaster"   → reliability/ROOT.md
  "chronic incident"               → playbooks/
```

---

## Deployment Guide — Host it as a Docs Site

The core is plain Markdown, so it can be hosted anywhere. Below are four ways to turn it into a browsable website.

### Option 1: GitHub Pages (zero-cost, simplest)

You have two paths: **live rendering** of the Markdown (fastest) or a **real docs site** (see Option 3/4).

#### Path A — Auto-deploy with GitHub Actions (recommended)

Create `.github/workflows/deploy.yml` in the repo:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "."
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

Then:

1. Create the file above at `.github/workflows/deploy.yml`.
2. Go to the repo → **Settings → Pages** → Source: **GitHub Actions**.
3. Every push to `main` redeploys automatically.
4. Your site will be at `https://<username>.github.io/backend-skill/`.

#### Path B — Manual enable

1. Repo → **Settings → Pages**.
2. Under **Branch**, pick `main` and folder `/ (root)`.
3. **Save**. The site appears at `https://<username>.github.io/backend-skill/`.

> **Note:** GitHub Pages renders raw Markdown unless you use a generator (MkDocs/Docusaurus). For a polished site, use Option 3 or 4.

### Option 2: Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub.
2. **Add New Project** → select the `backend-skill` repo.
3. Build & Output Settings: Framework Preset → **Other**; leave Output Directory empty.
4. Click **Deploy**.

### Option 3: MkDocs (professional docs site)

[MkDocs](https://www.mkdocs.org/) turns Markdown into a clean, searchable site.

**Prerequisites:** Python 3.9+ and pip.

```bash
pip install mkdocs mkdocs-material
```

Create `mkdocs.yml` in the repo root:

```yaml
site_name: Backend Architect Neural
site_description: AI-readable backend engineering knowledge base
site_author: Mobin Hasanghasemi
repo_url: https://github.com/mobinhasanghasemi/backend-skill
repo_name: backend-skill
edit_uri: edit/main/docs/

theme:
  name: material
  language: en
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.highlight
    - search.suggest
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed
  - pymdownx.tasklist
  - toc:
      permalink: true

nav:
  - Home: README.md
  - Brain:
      - NEURAL_ROUTING.md
      - NEURON_PROTOCOL.md
      - brain/graph.md
      - brain/domains.md
  - Architecture: architecture/ROOT.md
  - API: api/ROOT.md
  - Databases: databases/ROOT.md
  - Security: security/ROOT.md
  - Performance: performance/ROOT.md
  - Reliability: reliability/ROOT.md
  - Observability: observability/ROOT.md
  - Django: django/ROOT.md
  - Python: python/ROOT.md
  - Distributed Systems: distributed-systems/ROOT.md
  - Messaging: messaging/ROOT.md
  - DevOps: devops/ROOT.md
  - Infrastructure: infrastructure/ROOT.md
  - Caching: caching/ROOT.md
  - Testing: testing/ROOT.md
  - AI Backends: ai-backends/ROOT.md
  - Multi-tenancy: multi-tenancy/ROOT.md
  - Storage: storage/ROOT.md
  - Data Engineering: data-engineering/ROOT.md
  - Playbooks: playbooks/
  - Checklists: checklists/
  - ADR: adr/
  - Research: research/index.md
```

**Build & serve locally:**

```bash
mkdocs build
mkdocs serve     # http://localhost:8000
```

**Deploy to GitHub Pages:**

```bash
mkdocs gh-deploy
```

This builds the site to the `gh-pages` branch; GitHub Pages serves it automatically.

### Option 4: Docusaurus

[Docusaurus](https://docusaurus.io/) is a React-based docs generator by Meta.

**Prerequisites:** Node.js 18+.

```bash
npx create-docusaurus@latest backend-skill-docs classic --typescript
cd backend-skill-docs
```

1. Copy (or symlink) the Markdown files into `docs/`.
2. Edit `docusaurus.config.ts` to set the site title and `url`/`baseUrl`.
3. Add the nav structure in `sidebars.ts`.
4. Deploy to GitHub Pages:

```bash
GIT_USER=<YourGitHubUsername> npm run deploy
```

---

## Directory Map

```text
backend-skill/
├── README.md                    # this file — guide + deployment tutorial
├── SKILL.md                     # agent activation surface (entry point)
├── BRAIN.md                     # central cognitive controller ("the brain")
├── LICENSE                      # MIT license
│
├── NEURAL_ROUTING.md            # contextual path selection
├── NEURON_PROTOCOL.md           # neuron contract + relationship types
├── CODE_TIERS.md                # bad → good → better → excellent ladders
├── RESEARCH_PROTOCOL.md         # deep-research before creating knowledge
├── LEARNING_SYSTEM.md           # how the brain saves and grows knowledge
├── EVIDENCE_PROTOCOL.md         # evidence classification + confidence
├── MEMORY_PROTOCOL.md           # semantic / episodic / procedural memory
│
├── DECISION_ENGINE.md           # decision protocol + conflict resolution
├── SECURITY_GUARDIAN.md         # cross-cutting security review
├── PERFORMANCE_ENGINE.md        # evidence-driven performance methodology
├── RELIABILITY_ENGINE.md        # availability, RPO/RTO, failure propagation
├── SIMPLICITY_GOVERNOR.md       # complexity justification
├── ARCHITECTURE_LINTER.md       # 35 architecture anti-pattern rules
├── VALIDATION_PROTOCOL.md       # quality gates
├── ARCHITECTURE_GENOME.md       # architecture fingerprint / comparison
│
├── brain/                       # graph, routing, activation, memory
│   └── graph.md, domains.md, relationships.md, routing.md,
│       activation.md, causal-graph.md, failure-propagation.md,
│       confidence.md, memory.md, version-awareness.md
│
├── architecture/                # patterns, anti-patterns, evolution, system design
├── api/                         # rest, graphql, grpc, websockets, webhooks, versioning
├── databases/                   # relational, postgresql, mysql, nosql, optimization
├── security/                    # authentication, authorization, OWASP, crypto
├── performance/                 # profiling, latency, saturation
├── reliability/                 # SLOs, backups, deployment, incident response
├── observability/               # logs, metrics, tracing
├── distributed-systems/         # timeouts, circuit breaker, saga, outbox, locks
├── messaging/                   # celery, kafka, queues
├── django/                      # orm, drf, migrations, settings, admin
├── python/                      # async, typing, memory, packaging
├── infrastructure/              # containers, kubernetes
├── devops/                      # ci-cd, release engineering
├── caching/                     # strategies, invalidation
├── testing/                     # unit, integration, e2e, load, security
├── ai-backends/                 # rag, llm-calls, agents, evals
├── data-engineering/            # batch, streaming, warehouse
├── multi-tenancy/               # SaaS isolation patterns
├── storage/                     # object storage, files
├── playbooks/                   # 16 incident runbooks
├── checklists/                  # architecture, security, code review, release
├── adr/                         # architecture decision records (template)
├── research/                    # research log + evidence registry
├── tools/                       # check_links.py, validate_neurons.py, freshness.py
├── agents/                      # openai.yaml (agent skill metadata)
│
├── .gitattributes
└── .mimocode/                   # MiMoCode configuration
```

---

## Core Protocols & Engines

| File | Purpose |
|------|---------|
| `BRAIN.md` | Central cognitive controller — the meta-chain and reasoning trace |
| `NEURAL_ROUTING.md` | Router — decides which domains activate for a given problem |
| `NEURON_PROTOCOL.md` | Neuron contract — the standard schema every knowledge file follows |
| `CODE_TIERS.md` | Code ladder — teaching samples from bad → excellent |
| `DECISION_ENGINE.md` | Decision protocol — candidate evaluation + conflict resolution |
| `SECURITY_GUARDIAN.md` | Security review engine — applies to every design |
| `PERFORMANCE_ENGINE.md` | Performance methodology — measure first, then optimize |
| `RELIABILITY_ENGINE.md` | Availability, RPO/RTO, failure propagation |
| `SIMPLICITY_GOVERNOR.md` | Rejects unearned complexity |
| `ARCHITECTURE_LINTER.md` | 35 machine-checkable anti-pattern rules (ARCH001–ARCH035) |
| `VALIDATION_PROTOCOL.md` | Neuron, research, and answer quality gates |
| `EVIDENCE_PROTOCOL.md` | Evidence classes (VERIFIED / SUPPORTED / INFERRED / …) |
| `LEARNING_SYSTEM.md` | How the brain saves and grows knowledge |
| `MEMORY_PROTOCOL.md` | Three memory layers (semantic / episodic / procedural) |
| `RESEARCH_PROTOCOL.md` | Deep-research discipline before creating knowledge |
| `ARCHITECTURE_GENOME.md` | Compact, comparable architecture representation |

---

## Knowledge Domains

| Domain | Covers |
|--------|--------|
| **architecture/** | patterns, anti-patterns, evolution, system design |
| **api/** | REST, GraphQL, gRPC, WebSocket, webhooks, versioning, errors |
| **databases/** | PostgreSQL, MySQL, NoSQL, optimization, data modeling |
| **security/** | authN, authZ, OWASP Top 10, cryptography, compliance |
| **performance/** | profiling, latency optimization, scaling |
| **reliability/** | SLOs, backups, recovery, incident response |
| **observability/** | tracing, logs, metrics, OpenTelemetry |
| **distributed-systems/** | timeouts, circuit breaker, saga, outbox, consensus, locks |
| **messaging/** | Celery, Kafka, queue design |
| **django/** | ORM, DRF, migrations, settings, caching, admin |
| **python/** | async, typing, memory, packaging |
| **infrastructure/** | containers, Kubernetes |
| **devops/** | CI/CD, release engineering |
| **caching/** | strategies, invalidation |
| **testing/** | unit, integration, contract, e2e, load, security |
| **ai-backends/** | RAG, LLM calls, agents, evals, semantic caching |
| **data-engineering/** | batch, streaming, warehouse |
| **multi-tenancy/** | SaaS tenant isolation models |
| **storage/** | object storage, files, signed URLs |

---

## Playbooks

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
| `incident-command.md` | Incident command |

---

## Checklists

| Checklist | Purpose |
|-----------|---------|
| `architecture-review.md` | 57-question architecture review |
| `security-checklist.md` | 38-item pre-release security gate |
| `code-review-checklist.md` | 40-item backend code review |
| `release-checklist.md` | 25-step production deploy |

---

## Integrity Tools

Three Python scripts keep the knowledge base honest (in `tools/`):

| Tool | Purpose |
|------|---------|
| `check_links.py` | Reports broken/ambiguous Markdown links |
| `validate_neurons.py` | Validates neuron schema (ID, Type, H1, H2); fails on zero files |
| `freshness.py` | Flags stale or future-dated evidence markers |

Run them:

```bash
python tools/check_links.py
python tools/validate_neurons.py
python tools/freshness.py
```

---

## Contributing

Contributions are welcome. When adding or editing knowledge:

1. Follow the neuron contract in `NEURON_PROTOCOL.md`.
2. Classify every factual claim per `EVIDENCE_PROTOCOL.md` (register sources in `research/sources.md`).
3. Add the 4-tier code samples per `CODE_TIERS.md` where relevant.
4. Run the integrity tools before submitting.
5. Record significant decisions in `adr.md`.

---

## License

This project is licensed under the [MIT License](LICENSE). See the file for details.

---

<div align="center">
  <sub>Built for the backend engineering community</sub>
  <br>
  <sub>Copyright © 2026 Mobin Hasanghasemi</sub>
</div>