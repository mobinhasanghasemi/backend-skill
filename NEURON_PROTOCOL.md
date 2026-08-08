# NEURON PROTOCOL

Every knowledge file is a **neuron**. Neurons are connected into a knowledge graph. This file defines the contract every neuron MUST satisfy.

---

## Standard Neuron Contract

```markdown
# <Neuron Name>

## Identity
- ID: <dotted path: e.g. database.postgresql>
- Domain: <primary domain>
- Type: <technology | pattern | principle | procedure | mechanism | competency>
- Status: <active | pending-verification | deprecated | experimental>
- Importance: <critical | high | medium | low>
- Last Verified: <date>

## Purpose
What this neuron exists to compute.

## Core Concept
The essential idea, in 3-5 sentences. No fluff.

## Mental Model
The core visual/tactile model that makes it intuitive.

---

## Activation Conditions
List precise conditions under which an agent SHOULD read this neuron.

## Do Not Activate When
List the cases where reading this neuron is WRONG / misleading (negative knowledge).

---

## Parent Neurons
Dotted paths of encompassing concepts.

## Child Neurons
Dotted paths of more specific neurons.

## Connected Neurons
Cross-domain links with relationship type.

## Dependencies
What must exist first (tools, concepts, compilers).

## Influences
What this neuron affects downstream (architecture, choices, behavior).

## Conflicts
What contradicts this neuron (and under what circumstances).

## Complements
Enjoys cooperation.

---

## Decision Rules
Concrete "if ... then ..." rules. The money section.

## Trade-offs
Each main option with its advantages AND drawbacks. Explicit.

## Benefits
Audience-visible upside.

## Costs
Audience-visible downside (money, time, ops).

---

## Risks
Failure scenarios this neuron introduces.

## Failure Modes
How this thing breaks in production, in ordered severity.

## Anti-Patterns
Ways this neuron gets misapplied.

---

## Security
Security-if next section (threat model, data exposure...).

## Performance
Performance characteristics + measurement cautions.

## Scalability
How to keep working as tail grows.

## Reliability
Availability, durability, RPO/RTO, failure isolation.

## Observability
Explicit signals (metrics/logs/traces/events) to watch for this neuron.

## Testing
How to verify behavior (test techniques, golden paths, failure tests).

---

## Implementation Guidance
Short, concrete, actionable steps (not code dump, or example code block).

## Code Tiers (optional but expected for practical neurons)
A 4-tier sample ladder for the neuron's main behavior — `CODE_TIERS.md` defines:

```markdown
## Code Tiers
### ❌ The common bad way
(subtle **MISTAKEN** sample — realistic failure)
### ✅ Good
(minimal, correct per context)
### ⚡ Better
(meaningful upgrade — e.g. query optimization, security hardening,
   efficiency, observability)
### 🏆 Excellent
(production-grade for the context — includes error handling, observability,
   bounded resources)
```

Samples must stay context-realistic (Django domain uses Django/Python, DB neurons use SQL, infra uses YAML/manifests)
The AI must never see a tier as "the one allowed move" — tiers are didactic gradients. The choice is context-driven; a low-tier sample may be right for a tiny system with no traffic.

## Migration Guidance
If applying this to an existing system — how.

## Evolution Path
How this neuron should evolve over time (versions, replacements).

## Version Awareness
Current version facts + version matrix.

## Evidence
What verifies its claims (with classification).

## Confidence
<VERIFIED | SUPPORTED | INFERRED | EXPERIMENTAL | UNCERTAIN> + trailing.

## Verification Status
how this was checked.

---

## AI Instructions
Meta-rules for an AI consuming this neuron.

## Reasoning Triggers
Prompts that should cause this neuron to activate — for a human scanning.

## Questions To Ask
The questions that must be asked of the user before applying.

## Validation Checklist
A short point-form verification this neuron is aligned with its region ROOT.

## Notes
free-form (allowed but optional)
```

The contract is iterative — a ROOT.md can use a **condensed** form but must keep each heading that matters for routing.

---

## Neural Connection Types

| Type | Meaning |
|---|---|
| depends_on | activation/discovery required first |
| requires | hard dependency (missing = lost) |
| influences | affects the shape of another |
| causes | causal effect (positive or "leads to failure") |
| mitigates | protects against failure/side effect |
| protects_against | security defense |
| conflicts_with | trade-off adversary |
| complements | works cooperatively |
| alternative_to | replacement choice — compare |
| specializes | is a narrower version of |
| generalizes | broader concept |
| implements | realizes an interface |
| integrates_with | interfaces with (positive) |
| scales_with | capacity relationship |
| constrained_by | must respect constraints |
| observed_by | instrumentation |
| validated_by | piece of evidence/verification |
| evolves_into | later version |
| replaced_by | superseded |
| deprecated_by | removed |

## Connection expression choices

```markdown
## Connected Neurons
- `database.postgresql` —→ `performance.query` (influences)
- `database.postgresql` ∿ `security.data-protection` (protects_against)
```

Use descriptive wording; the type table above is a DSL, not strict.

---

## ID conventions

```text
<domain>.<leaf>.<granularity>
database.indexing
postgresql.mvcc
api.versioning
security.oauth2
```

---

## Quality gate (NEURON completion check)

Before marking a neuron complete:

- [ ] Has Identity (ID available?)
- [ ] Purpose stated as computation
- [ ] Activation + Non-activation conditions explicit
- [ ] Parent / Child / Connected neurons exist (even <empty>)
- [ ] Dependencies, Conflicts, Trade-offs present
- [ ] Security, Performance, Reliability, Scalability, Observability brain-sections present
- [ ] Failure modes + anti-patterns
- [ ] Versioning awareness
- [ ] Evidence + Confidence + Verification Status
- [ ] AI Instructions / Triggers / Probe Questions
- [ ] No hallucinated claims (verified or marked UNCERTAIN)
- [ ] Cross-links non-broken

If any *critical* item is missing → do not mark COMPLETE; mark WIP.

## ROOT.md contract

ROOT.md must contain (in addition to the standard contract):

- **Routing Rules**: keyword → child neuron map
- **Mandatory Questions** to ask before answering
- **Risk Checks**, **Security Checks**, **Performance Checks**, **Reliability Checks**
- **Evidence Requirements** (what verification the domain needs)
- **Common Failure Modes of the domain overall**
- **Attention weights** — which children to prefer

ROOT is a *router*, so its "Implementation Guidance" is a routing decision tree rather than steps.