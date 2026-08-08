# BACKEND ARCHITECT NEURAL

An AI-readable artificial engineering brain for backend architecture. Knowledge is stored as interconnected Markdown neurons. The AI dynamically routes through the graph, activates only relevant neurons, reasons causally, checks security/performance/reliability, and produces production-grade decisions with traces.

---

## How to use this skill

1. Start at `BRAIN.md` — the cognitive controller. It explains the pipeline, activation states, and reasoning trace.
2. Provide your problem. The AI runs:
   - **Perception** → classify the problem
   - **Route** → `NEURAL_ROUTING.md` decides which domains activate
   - **Activate** → domain ROOT neurons (e.g. `databases/ROOT.md`) provide routing rules and mandatory checks
   - **Traverse** → child neurons + cross-domain links (allowed connection types in `NEURON_PROTOCOL.md`)
   - **Reason** → `DECISION_ENGINE.md` + `SECURITY_GUARDIAN.md` + `PERFORMANCE_ENGINE.md` + `RELIABILITY_ENGINE.md`
   - **Validate** → `ARCHITECTURE_LINTER.md` + `VALIDATION_PROTOCOL.md`
   - **Produce** → recommendation with reasoning trace, alternatives, risks, next validation steps.

## Directory map

```text
backend-architect-neural/
├── BRAIN.md                    # central cognitive controller
├── README.md
├── NEURAL_ROUTING.md          # contextual path selection
├── NEURON_PROTOCOL.md         # neuron contract + relationship types
├── CODE_TIERS.md              # bad → good → better → excellent code ladders
├── RESEARCH_PROTOCOL.md       # how to deep-research before creating knowledge
├── LEARNING_SYSTEM.md         # how the brain saves and grows knowledge
├── EVIDENCE_PROTOCOL.md       # evidence classification + confidence
├── MEMORY_PROTOCOL.md         # semantic / episodic / procedural memory
├── DECISION_ENGINE.md         # decision protocol + conflict resolution
├── SECURITY_GUARDIAN.md       # cross-cutting security review
├── PERFORMANCE_ENGINE.md      # evidence-driven performance methodology
├── RELIABILITY_ENGINE.md      # availability, RPO/RTO, failure propagation
├── ARCHITECTURE_LINTER.md     # architecture anti-pattern lint rules
├── VALIDATION_PROTOCOL.md     # quality gates
├── SIMPLICITY_GOVERNOR.md     # complexity justification
├── ARCHITECTURE_GENOME.md     # architecture fingerprint / comparison
│
├── brain/                    # graph, routing tables, activation logic
│   ├── graph.md
│   ├── domains.md
│   ├── relationships.md
│   ├── routing.md
│   ├── activation.md
│   ├── causal-graph.md
│   ├── failure-propagation.md
│   ├── confidence.md
│   ├── memory.md
│   └── version-awareness.md
│
├── architecture/             # patterns, anti-patterns, evolution, system design
├── api/
├── databases/                # relational, postgresql, mysql, nosql, optimization
├── security/                 # cross-cutting security neurons
├── performance/
├── distributed-systems/
├── reliability/
├── observability/
├── testing/
├── python/
├── django/
├── messaging/
├── caching/
├── ai-backends/
├── multi-tenancy/
├── infrastructure/           # cloud, containers, kubernetes, deployment
├── devops/
├── data-engineering/
├── storage/
├── playbooks/                # diagnosis playbooks (slow-api, db-slow, ...)
├── checklists/               # architecture, security, performance reviews
├── adr/                      # architecture decision records (template)
└── research/                 # research log + recent verification notes
```

## Conventions

- Every domain directory contains a `ROOT.md` (controller neuron).
- Every neuron follows the contract in `NEURON_PROTOCOL.md` (goal: not a wiki page — an operational knowledge unit).
- Every claim carrier has an Evidence classification (VERIFIED / SUPPORTED / INFERRED / EXPERIMENTAL / UNCERTAIN).
- Version awareness is tracked in `brain/version-awareness.md`; framework neurons carry it inline.
- Mermaid diagrams are allowed when they add structure.
- Filename = neuron name. Folder = domain. The graph lives in the files, not in the directory layout.

## Status

Last updated: 2026-08. If you update knowledge, update the version matrix and mark `Last Verified`.