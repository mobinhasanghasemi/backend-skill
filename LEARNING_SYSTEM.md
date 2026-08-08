# LEARNING SYSTEM

How this brain acquires, verifies, saves, and grows knowledge over time. The goal: **never save hallucinations, never let uncertainty masquerade as fact, and keep the graph coherent.**

---

## The Neuron Save Protocol

```text
DISCOVER   →  something new (from user, docs, web, measurement, reasoning)
  │
  ▼
VERIFY     →  apply RESEARCH_PROTOCOL pipeline; confirm against official sources
  │
  ▼
CLASSIFY   →  evidence class (VERIFIED / SUPPORTED / INFERRED / EXPERIMENTAL / UNCERTAIN)
  │
  ▼
NORMALIZE  →  obey NEURON_PROTOCOL contract; language = operational knowledge unit
  │
  ▼
CONNECT    →  declare parents, children, connected neurons, relationship types
  │
  ▼
SCORE      →  confidence via EVIDENCE_PROTOCOL (source + relationship + context fit)
  │
  ▼
SAVE       →  write the neuron file; record Last Verified date
  │
  ▼
REVIEW     →  run NEURON quality gate; if fails, fix (or mark WIP)
```

---

## Entry points for new knowledge

| Source | How the brain should react |
|---|---|
| Official docs read during research | Author it → VERIFIED, save |
| Production incident (episodic) | Author a playbook section or ADR note |
| Team choice ("we picked X because") | Memory (episodic) with explicit project tag |
| New framework version | Update Version Awareness; search for breaking changes |
| New security advisory | Must update related security neuron + mark `needs_action` |
| Repeated community claim without evidence | HOLD; do not save as fact until verified |

---

## Neuroplasticity — strengthening and weakening connections

Connections are refinable:

| Signal | Effect |
|---|---|
| Evidence validated | strengthen (confidence level up) |
| Repeatedly useful across sessions | connection weight up |
| Contradiction found | mark conflict; confidence down OR bifurcate |
| Deprecation / replacement | mark obsolete path; link replaced_by |
| Observed failure of the practice in practice | add failure mode, possibly lower confidence |

Rules:

- Evidence quality **always** beats frequency (do not cement by popularity)
- When a connection weakens, note `Confidence: DECREASED` in the neuron
- Never delete a neuron's history — the ADR and research log preserve the record; deprecated neurons get `Status: deprecated` and live on as memory

---

## Knowledge hygiene — periodic cleanup

Targets:

```text
🕳 duplicates        → consolidate or link
⚠ contradictions     → find, document, decide
💔 broken references → fix links (relative paths) 
💀 dead neurons      → mark deprecated or remove with record
🧠 outdated info     → replace, note old version in Version Awareness
⚠ weak evidence     → downgrade classification
🧩 missing connections → add
🔍 missing security/performance sections → require
```

Version matrix: `brain/version-awareness.md` is where this force is registered.

---

## The three kinds of memory — into the system

| Kind | Storage |
|---|---|
| Semantic (stable engineering) | neurons (this tree of knowledge) |
| Episodic (project-specific decisions) | `adr/` + `research/` notes |
| Procedural (repeatable workflows) | this file's playbooks |

---

## Anti-patterns of learning

- ❌ Saving a claim without evidence (EVIDENCE_PROTOCOL passes)
- ❌ Saving a claim the model "feels is right" with no source
- ❌ Updating dates than content to fake freshness
- ❌ Copying a list from the internet without arguing
- ❌ Creating parallel neuron + graph entry that sunset the old one — always update the graph

---

## Example save

```
DISCOVER: Django 6.0 released Dec 2025.
VERIFY: djangoproject/download (2026-08-verified) → active; 5.2 remains LTS until April 2028.
CLASSIFY: VERIFIED.
NORMALIZE: update django/version-awareness.md matrix.
CONNECT: django.ROOT overrides.
SCORE: confidence high (official source, no contradiction).
SAVE: edit neuron + version-awareness.md; Last Verified 2026-08.
```

Save done.