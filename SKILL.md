---
name: backend-architect-neural
description: Backend architecture, design, building, review and incident remediation for Python/Django/DRF/PostgreSQL/Redis/Celery/queues services. Use when designing APIs and data models, migrations and schema changes, caching and async queues, backend performance (slow queries, N+1), reliability, security review of backend code, or service boundaries and SLOs for existing or new backends.
---

# SKILL.md — Backend Architect Neural (v2)

> **The activation surface.** Follow the router (`NEURAL_ROUTING.md`) for routing; the engines below for quality protocols and the security lens. Read the minimum, load only the matching neurons.

## Name
Backend Architect Neural — design, build, review, and remediate backends (Python/Django/DRF/PostgreSQL/Redis/queues) with decision engineering.

## Description (activation hooks)
- Backend architecture & design (monolith vs services, API design, data models, queues, caching, migrations)
- Building/operating Django/DRF/PostgreSQL/Celery/Redis services; writing and reviewing backend code
- Performance/reliability/security of existing backends; slow queries, N+1, leaks, incidents
- Any prompt mentioning: backend, API, database, service boundary, queue, cache, schema, migration, SLO, incident

## When NOT to engage
- pure frontend/UI, design/CSS, SEO, DevOps-only hosting, gaming/embedded without backend relevance — back them off, keep the "backend only" lens unless asked.

## The protocol (mandatory when active)
1. **Read `BRAIN.md`** — the cognitive chain (perception → constraints → routing → causal reasoning → decision → validation). Do not skip.
2. **Read `NEURAL_ROUTING.md`** for domains; load only the neuron that matches (progressive disclosure — limited context).
3. **Engines active by default**: `SECURITY_GUARDIAN.md` (always), `SIMPLICITY_GOVERNOR.md` (complexity), `PERFORMANCE_ENGINE.md` (claims), `RELIABILITY_ENGINE.md` (failure). Load a specific engine file only when its lens matters.
4. **Every claim**: evidence label (VERIFIED / SUPPORTED / INFERRED / EXPERIMENTAL / UNCERTAIN) per `EVIDENCE_PROTOCOL.md`; never pitch unproven.
5. **Code Tiers**: use `CODE_TIERS.md` (bad→good→better→excellent) by context, not maximum.
6. Answer structure: decision trace + code tier + verification steps (per `DECISION_ENGINE.md`).

## Structure (progressive, one domain per read)
```
README.md               intro & index
BRAIN.md                the meta-chain (read once)
NEURAL_ROUTING.md       domain router
*.md (root)             engines & protocols: SECURITY_GUARDIAN, SIMPLICITY_GOVERNOR,
                        PERFORMANCE_ENGINE, RELIABILITY_ENGINE, DECISION_ENGINE,
                        VALIDATION_PROTOCOL, EVIDENCE_PROTOCOL, NEURON_PROTOCOL,
                        CODE_TIERS, ARCHITECTURE_LINTER, LEARNING_SYSTEM, MEMORY_PROTOCOL
<domain>/ROOT.md        domain entrypoints (django, api, databases, caching, messaging,
                        performance, reliability, security, architecture, python, storage,
                        observability, testing, ai-backends, data-engineering, devops,
                        distributed-systems, infrastructure, multi-tenancy)
<domain>/**             neurons: concept/procedure bodies
playbooks/              runbooks for failure modes  (e.g. playbooks/slow-api.md)
checklists/             gates: architecture / security / release / code review
research/               external facts + evidence registry (research/sources.md)
adr/ + adr.md           decision journal
```
**Read the minimum**: question → domain `ROOT.md` (routing) → best-matching neuron → playbook if incident. Never load an entire domain tree at once.

## Integrity tooling
- `tools/` scripts keep the skill honest: `check_links.py` (broken/ambiguous links), `validate_neurons.py` (schema + contract coverage, fails on zero files), `freshness.py` (evidence dates).
- Run the relevant one when available; never block work on tool unavailability — flag violations instead.

## Tuning / maintenance
- Errors found in the docs are edits (LEARNING_SYSTEM / LEARNING protocol). New neurons need {identity, activation, code}; keep the three templates (root / concept / procedure).