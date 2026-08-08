---
title: Eval design for an LLM endpoint
domain: ai-backends
bench: golden-task
---

# Task 31 — Eval design for an LLM endpoint

**Domain:** ai-backends

## Scenario

Design an evaluation suite for a summary endpoint: golden set, rubric-based metrics, offline vs online checks, regression gate.

## What a good answer contains (pass-bars)

Golden set + per-example rubric; regression threshold in CI; no hand-waving about quality.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `ai-backends/evals -> testing/unit-integration`.
