# MEMORY PROTOCOL

The brain remembers in three layers. This file defines which"memory" lives in which storage, and how the layers interact with every decision.

## The three memory layers

### 1. Semantic Memory — stable engineering knowledge
Where: the neuron files (`databases/`, `security/`, `api/` ...)
Content: facts, patterns, trade-offs, relationships — the durable model of the world.

Example:
```
PostgreSQL uses MVCC (multi-version concurrency control) to avoid writer-reader blocking.
```

Semantic memory is **version-aware** (`brain/version-awareness.md`), evidence-validated, and ever reviewed against this protocol.

### 2. Episodic Memory — project-specific history
Where: `adr/` (architecture decision records), `research/index.md`
Content: specific decisions, incidents, validation results, empirical observations from real systems.

Example:
```
Project Atlas chose PostgreSQL over MySQL due to need for partial indexes
and complex JSON aggregation — November 2025, ADR-014.
```

Episodic memory informs "what worked in similar circumstances" — used for priors, but never overrides semantic evidence (frequency != truth).

### 3. Procedural Memory — repeatable procedures
Where: `playbooks/` + `checklists/` + protocol files
Content: how-to-run steps: diagnose a slow query, do a blue-green deploy, run an incident.

Example:
```
Diagnosing a slow query:
1. reproduce
2. measure
3. EXPLAIN ANALYZE
4. inspect plan
5. change
6. benchmark again
```

## How to use the layers in a session

1. **Semantic layer first**: identify facts relevant to the task (activate neurons).
2. **Episodic layer bonus**: if the project has an ADR history, check for prior decisions that constrain this one.
3. **Procedural layer**: when the task is "fix incident x" → pull the playbook; when it's "review architecture" → pull the checklist.

## Memory hygiene

- Episodic records are permanent facts about the past — factual, timestamped, immutable.
- Semantic memory can be updated when evidence changes (mark the prior state OUTDATED).
- Procedural steps aim for environment-agnostic wording (no vendor-specific typos).
- Cleanup protocol lives in `LEARNING_SYSTEM.md` (knowledge hygiene).

## Notes on retention

- If an episodic record is 2+ years old for a fast-evolving tech, re-verify before relying on it.
- If a semantic record's evidence is stale (Last Verified too old), the user should run `brain/version-awareness.md` review.

---

## Memory & the Decision Engine

- Use episodic memory → warning signal (but make the user aware when past similar decisions had failed).
- Never let a memory override the evidence protocol: frequency-of-usage (common) ≠ correctness.
- New data enters via the save protocol only (`LEARNING_SYSTEM.md`).