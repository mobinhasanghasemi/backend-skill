# brain/memory.md

Operational map of how the three memory layers (MEMORY_PROTOCOL.md) are physically stored in this skill.

## Layer → file map

| Layer | Storage | Contents |
|---|---|---|
| Semantic | `neuron files` (every domain) | stable engineering knowledge |
| Episodic | `adr/*.md`, `research/index.md` | project decisions, incidents, measurements |
| Procedural | `playbooks/`, `checklists/`, protocols | repeatable workflows |

## The semantic memory structure

- Each neuron file is a unit of semantic memory with ID, evidence, confidence.
- The graph (brain/graph.md) is the index of how they connect.
- Version awareness (brain/version-awareness.md) is the memory's freshness clock.

## Episodic memory discipline

An ADR (adr/template.md) records:

```text
context:  why the decision mattered
decision: what was chosen (genome!)
rationale: evidence + constraints
alternatives rejected (and why)
consequences: what to watch
date, status (proposed/accepted/deprecated/superseded)
```

Episodic notes in research/index.md track: what was verified, when, and with which source. This makes the brain's "experience" traceable.

## Procedural memory discipline

Playbooks have a fixed structure (symptoms, causes, signals, investigation, mitigations, rollback, prevention) — so the procedure is self-contained and reusable. Checklists codify review procedures.

## How a session uses memory

1. **Semantic first** — to answer the question, per routing.
2. **Episodic** — when user mentions an existing project, look for its ADRs; when verifying a claim, check research/index.md for prior verification.
3. **Procedural** — for "do" tasks: playbook/checklist. Never improvise diagnosis when a playbook exists.

## Memory safety

- Don't treat episodic (one project) as semantic (general truth).
- Don't treat semantic as immutable: version change → re-verify.
- Records are permanent; corrections add a new note (append-only spirit), rather than deleting history — but neurons can be updated in place with versioned rationale.

## Example trace

```
User: "we're seeing slow API calls"
Semantic: performance ROOT → latency + profiling
Procedural: playbooks/slow-api.md → measure → profile → hypothesis → fix
Episodic: adr/017-* if this project has prior perf ADRs → check what was changed before
```