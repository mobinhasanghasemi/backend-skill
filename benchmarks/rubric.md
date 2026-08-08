# RUBRIC — SkillBench scoring

One table you score EVERY task, both runs (base & with-skill):

## Dimensions (each 0 / 0.5 / 1 — half-points allowed)

| # | Dimension | 0 | 0.5 | 1 |
|---|---|---|---|---|
| D1 | Correctness | hallucinated behavior / wrong primitives | mostly right, one conceptual slip | exactly right for the stated context |
| D2 | Security | open by default (IDOR, missing auth, untrusted input) | checks the obvious | threat-conscience full trace |
| D3 | Simplicity | over-engineered, contradictory layers | acceptable but extra moving parts | minimal for the context, named why |
| D4 | Operability | no ops signals, no pain points | partial | deployable, monitored, debuggable |
| D5 | Evidence | invented API / version claim | SUPPORTED practice (no pin) | VERIFIED with source-S-<ID> or real URL |
| D6 | Code validity | fake syntax/API that never runs | plausible, minor tweaks needed | runs for the status quo stack in task |

## Verdict bands

- **0–2**: rewrite; identify the missing principle (usually a single neuron).
- **2–4**: acceptable, room to improve; encourage better-tier trade-offs.
- **4–6**: production-shaped; flag if any use of `must/always` slipped in.

## Extract

```text
task-XXX base  = ... /6
task-XXX with  = ... /6
delta          = +... (gate needs ≥ +15 over all tasks / 33)
```

## Anti-cheat

- Reusing answers between the two runs = task voided (run base first).
- Any answer containing an API/bibliography not in `research/sources.md` → D5=0
  automatic, plus annotation in the report.
- If a prompt requires a real framework + the model chose a borderline-but-labeled
  `illustrative` helper: count D6=0.5 (allowed), never 1 on invent-ed symbols.