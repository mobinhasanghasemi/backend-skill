# VALIDATION PROTOCOL


The quality gates that protect the knowledge base and the quality of answers. Two gates: the **Neuron Quality Gate** (for files) and the **Research Quality Gate** (for claims). Plus a final **Answer Check** before responding.

## Gate 1 — Neuron Quality Gate

Before a neuron counts as COMPLETE:

```
[ ] Clear identity (ID, domain, type, status, importance)
[ ] Clear purpose
[ ] Activation conditions
[ ] Non-activation conditions
[ ] Parent relationships
[ ] Child relationships
[ ] Cross-domain connections
[ ] Dependencies
[ ] Conflicts
[ ] Trade-offs
[ ] Security section
[ ] Performance section
[ ] Reliability section
[ ] Scalability section
[ ] Observability section
[ ] Failure modes
[ ] Anti-patterns
[ ] Version awareness
[ ] Evidence
[ ] Confidence
[ ] Verification status
[ ] AI instructions
[ ] Validation checklist
```

If any *critical* item is missing → not COMPLETE (WIP status). Apply the same gate when editing.

## Gate 2 — Research Quality Gate

Before a claim is published in the knowledge base:

```
[ ] Current official documentation checked
[ ] Relevant standard checked
[ ] Security guidance checked
[ ] Recent changes checked
[ ] Deprecations checked
[ ] Known limitations checked
[ ] Performance claims validated (measured vs claimed separated)
[ ] Conflicting recommendations investigated
[ ] Version boundaries identified
[ ] Evidence recorded
[ ] Confidence assigned
```

## Gate 3 — Answer Check (before replying)

- Does the answer satisfy the user's ACTUAL constraints (not assumptions)?
- Is the recommendation the simplest architecture that meets requirements? (SIMPLICITY_GOVERNOR)
- Does it carry the security/performance/reliability triad?
- Is evidence classified? Is a claim marked UNCERTAIN if unverified?
- Does the reasoning trace exist for non-trivial decisions?
- Are alternatives presented, not just a verdict?
- Does it tell the user how to validate before they ship?

## Escape hatches

- If the answer would violate a gate but the user demands it → produce the answer, label the gate violation explicitly (e.g., "⚠️ This recommendation skips timeout/idempotency validation — ARCH002 applies").
- If knowledge is missing → produce what's solid, mark gaps explicitly, and (per LEARNING_SYSTEM) propose research to fill them.

## The triage: security/perf/reliability triad

Every major recommendation gets one line per dimension (per spec #37):

```
CACHE:   Performance ↑ | DB load ↓ | complexity ↑ | stale-data risk ↑ | lost-write risk under multi-writer ⚠
```

If a dimension is damaged silently, that's a design defect.