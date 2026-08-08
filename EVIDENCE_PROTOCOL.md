# EVIDENCE PROTOCOL

Defines evidence classification, sourcing, and confidence calculus. Every factual claim in the knowledge base must carry a class; everything the brain asserts has a justification.

## Evidence Classes

| Class | Meaning | Example |
|---|---|---|
| **VERIFIED** | Directly confirmed from authoritative source (official docs, spec) — no ambiguity | "Django 5.2 is LTS until April 2028" |
| **SUPPORTED** | Strong corroboration from multiple credible sources, can't fully verify | "Most-REST APIs use HTTP status codes for errors" |
| **INFERRED** | Derived from established principles + reasoning (not directly observed) | "Sharding a Postgres DB will increase operational complexity" |
| **EXPERIMENTAL** | New, not production-proven, lab/benchmark only | "PostgreSQL 18 AIO = up to 3x read improvements in benchmarks" |
| **UNCERTAIN** | Can't verify, contradictory, or unknown | "Kafka 5.0 timeline unspecified" |
| **OUTDATED** | Was once true, superseded by version changes | "Django 4.2 supported" → now EOL 2026-04 |
| **DEPRECATED** | Officially no longer recommended | "MD5 password auth in PostgreSQL (deprecated in 18, SCRAM recommended)" |

Every neuron's Evidence section must list:

```markdown
What is claimed
Evidence class attached to each claim
Source reference — always `source-<ID>` pointing into `research/sources.md`, or a full URL with accessed-date when a new source is not yet registered
Version boundary if applicable
```

**Sourcing rule (hard gate):** `VERIFIED` / `SUPPORTED` without a `source-<ID>` (or full URL + access date) is a protocol violation, not evidence. Register every new external source in `research/sources.md` before citing it.

---

## Confidence Attribution

Confidence is not the same as evidence class alone. It has three components combined **conservatively**:

```text
confidence =
    f(source_authority)      official > community (never let community override, per NEURAL_ROUTING/LEARNING rules)
  + f(relationship_strength) # stable stated relationships > inferred
  + f(context_fit)           # how well the fact matches this scenario
  + validation               # has it been verified since?
```

- A single-source claim: max `SUPPORTED`
- A claim that contradicts a community trend: `UNCERTAIN`
- Never propagate confidence upward — parent neurons cannot inherit confidence from an uncertain child; the parent's own evidence gates it.

## Confidence levels of whole neurons

```text
VERIFIED      -> the neuron is consistent with at least one authoritative source, verified recently
SUPPORTED     -> consistent with irrefutable knowledge, though no per-claim citation
INFERRED      -> reasoning with explicit model
EXPERIMENTAL  -> marks: "pending production proof"
UNCERTAIN     -> has unanswered research / contradictions recorded IN the neuron
OUTDATED      -> marked: superseded section
DEPRECATED    -> kept as history for reasoning; marked "deprecated"
```

## Tending the evidence

- Every knowledge update: raise `Last Verified` at least month precision (e.g., `2026-08`).
- Every update touching a fact: check `research/sources.md` first, refresh the row's access date.
- New major version of tool → bump `Version Awareness` and **re-validate** all affected claims.
- Security advisories are highest-priority updates (own escalation path).

## Security/Official precedence

- For security, OWASP frameworks + tests rule. NIST SSDF is a primary reference for the secure development lifecycle.
- Treat official documentation as the top claim source in security.
- Golden rule: if security guidance from a standard conflicts with community opinion — the standard wins.

## Global rules

1. Any model creating a neuron MUST NOT invent API behavior, benchmark numbers, security guarantees, version capabilities, or citations. If unverifiable → mark UNCERTAIN.
2. Community claims (blogs/forums) always need a security-posture review and an official anchor, otherwise they are informational only.
3. If a fact cannot be rechecked, keep its `Last Verified` and treat it as the suspicious amber zone — downgrade confidence until re-verified.
4. Each evaluation: the outcome of a decision should be validated against the neuron's evidence — if the evidence turns out wrong, update the neuron (LEARNING_SYSTEM).