# SkillBench Report — 2026-08-27 (Harness Ready)

> **Status: HARNESS READY — live uplift run pending model execution.** This report is honest per `EVIDENCE_PROTOCOL.md`: we report what is measured vs what is prepared. No hallucinated scores.

## Integrity gates (measured, 2026-08-27)

| Gate | Command | Result |
|---|---|---|
| validate | `python tools/validate_neurons.py --max-warnings 0` | **PASS** — 251/251 contract |
| links | `python tools/check_links.py --strict` | **PASS** — 0 broken, 0 ambiguous |
| freshness | `python tools/freshness.py --days 400` | **PASS** — 528 markers in 182 files |
| routing parity | `python tools/check_routing_parity.py` | **PASS** — canonical `brain/routing.md` |

## Harness

- **Tasks:** 33 (`benchmarks/tasks/task-001…033`)
- **Rubric:** 6 dims × {0,0.5,1} = 6 pts/task → max 198 pts
- **Gate:** `Σ(with) ≥ Σ(base) +15` and no unverified API (S-xxx required) — `benchmarks/rubric.md:18`
- **Artifacts:** `examples/ADR-001…003` demonstrate traced decisions with genome diffs (proxy for task quality)

## What is ready for the live run

1. **Prompt pack:** each task is a standalone prompt with constraints (scale, team, compliance) — no runtime deps.
2. **Scoring sheet:** `benchmarks/rubric.md` + this report's `scorecard.csv` template (create on run: `task,base,with,delta`).
3. **Evidence binding:** any `VERIFIED` claim in a with-skill answer must have `source-S-xxx` from `research/sources.md` (82 rows, audited 2026-08-27) else D5=0.
4. **CI:** `.github/workflows/skill-ci.yml` will fail PRs that break gates — uplift gate can be added as 5th job once baseline is recorded.

## How to run the live uplift (15 minutes)

```bash
# 1) baseline (no skill)
#    for each task in benchmarks/tasks/*.md: solve with temperature 0, no skill files in context
#    score via rubric.md → base.csv

# 2) with-skill (skill active)
#    same tasks, but prepend SKILL.md + BRAIN.md + NEURAL_ROUTING.md to context,
#    follow routing → domain ROOT → neuron → engines
#    score via rubric.md → with.csv

# 3) uplift
python -c "import csv; b=sum(float(r['score']) for r in csv.DictReader(open('base.csv'))); w=sum(float(r['score']) for r in csv.DictReader(open('with.csv'))); print(f'uplift={w-b:.1f} gate={w-b>=15}')"
```

## Honest placeholder (not a claim)

| Task sample | Baseline (example) | With-skill (example) | Evidence |
|---|---|---|---|
| task-001 payment idempotency | 3.0/6 (no idempotency store) | 5.5/6 (outbox + Idempotency-Key + S-081) | Illustrative — do not cite as measured |

> **Do not cite placeholder as measured uplift.** The table above is shape, not result. The real numbers come from the live run.

## Next

- Run the harness with your chosen model (Claude, GPT, MiMo) and fill `benchmarks/scorecard.csv`.
- If uplift ≥15, this report upgrades to **VALIDATED**; if not, the delta pinpoints the weakest dimension (usually D2 security or D5 evidence) and the fix is a single neuron.

## Evidence

- Gates VERIFIED via tool execution 2026-08-27.
- Task design SUPPORTED via `benchmarks/README.md` and `benchmarks/rubric.md`.
- Harness readiness VERIFIED — no invented API, all source rows exist (S-001…S-082).
