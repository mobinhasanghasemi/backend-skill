# brain/confidence.md

Confidence is the brain's epistemic honesty. It must propagate **conservatively**: a low-confidence node must never produce a high-confidence conclusion without independent evidence.

## Confidence input model

```text
source confidence     → evidence class (VERIFIED/SUPPORTED/INFERRED/EXPERIMENTAL/UNCERTAIN)
relationship confidence → how well-established the edge is (strong/medium/weak)
context fit           → does the neuron's assumptions hold for this scenario?
validation            → has it been re-verified recently? (Last Verified)
```

## Propagation rules

1. **Conservative chaining**: conclusion confidence ≤ weakest input along the chain. A chain of [VERIFIED → INFERRED → VERIFIED] is INFERRED overall.
2. **No inheritance upward**: a parent neuron's confidence isn't raised by a confident child (the parent must earn it).
3. **Contradiction drops confidence** of both claims and records the conflict.
4. **Old evidence decays**: Last Verified older than ~1yr in fast-moving domains → downgrade one step (or mark amber).
5. **Repetition ≠ confidence**: a claim repeated across files doesn't get stronger (LEARNING_SYSTEM).

## Assigning final confidence to a decision

Combine the decision's inputs:

```text
verified facts        (high, but not auto-equal to correctness of choice)
inferred reasoning    (medium)
assumption            (low)
user-provided constraint (depends: if verified by user - take their word)
```

Result is a **decision confidence** the AI should express: `Confidence: high (facts verified) / medium (mix) / low (assumptions)`.

## How to express in answers

- State each material fact's class inline: `(VERIFIED)` / `(SUPPORTED)` / `(INFERRED)` / `(UNCERTAIN)`.
- When a recommendation depends on an unverified assumption, say so and give the validation step that would raise confidence.
- Never phrase an INFERRED as a fact. "This will cut latency 3x" → must have `EXPERIMENTAL`/`REPORTED` label.

## Confidence table for neurons

| Neuron state | Meaning | Handling |
|---|---|---|
| VERIFIED | recent authoritative source | rely fully |
| SUPPORTED | consistent with established knowledge | rely with minor caution |
| INFERRED | reasoning | rely only with explanation |
| EXPERIMENTAL | new/benchmark | treat as option, not fact |
| UNCERTAIN | contradictory/unknown | state explicitly, offer verification plan |

## Updating confidence

- New evidence → raise (record what changed + date).
- Re-verification after version change → re-run research gate, update Version Awareness.
- Contradiction found → split the claim (two variants) or downgrade.