# LLM Evals (the QA of AI features)

## Identity
- ID: ai-backends.evals
- Type: discipline
- Status: active
- Importance: high

## Purpose
Prove the AI feature works — correctness, safety, cost — with a golden dataset and rubric in CI. Without evals, every prompt/model change is a mystery.

## The eval stack
1. **Golden set**: 50-300 curated cases (per feature): common, edge, adversarial (hallucination bait), multi-tenant, PII-sensitive
2. **Metric**, per case: answer correctness (LLM-judge/human rubric), groundedness (cites or ignores context), retrieval recall@k, style/tone if critical
3. **Runner**: pytest + model provider (staging key, budgeted) → report: score per metric, per case diffs
4. **Gates**: CI fails if known-case regresses (or confidence lowers) — this is the SLO measurement of the AI contract
5. **Both-sides**: eval LLM (judge model) itself needs validation (sample hand-checked)

## Quality measurement (per-case rubric, 0-5 scale)

| Score | Meaning |
|---|---|
| 5 | perfect, cited |
| 4 | correct, minor style |
| 3 | usable, missing detail |
| 2 | misleading |
| 1 | wrong (hallucinated) |

## Code tiers
### ❌ Bad
# no evals: prompt tweak ships → clients see garbage, blame back to "AI"
### ✅ Good
# datasets/evals.yaml (human in the loop): case,rag_context,expected_gist  
# eval_run.py: run case → answer → LLM-judge score vs expected → report, fail < 4.0 avg
### ⚡ Better
# nightly full eval + CI-slack gate; eval on: embedding/chunk/rerank A/Bs, 
# model version duels (v1 vs v2 in-flight)
### 🏆 Excellent
# golden set per product line; red-team set (injection, policy, PII) automated
# hallucinations slope tracked; cost-per-good-answer metric on dashboard
# eval overhaul ties: model upgrade CR governs with eval results attached

## Anti-patterns
- evals only on happy path ("will the answer area contain the word")
- hand-reviewing everything (no judging metric)
- eval dataset drift (cases stale with new product)
- judging on token similarity (BE semantic)

## Evidence
- LLM evals practice (2024-2026 VERIFIED concepts), OpenAI Evals/ragas docs