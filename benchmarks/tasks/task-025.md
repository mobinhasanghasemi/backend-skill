---
title: Type hints in a legacy module
domain: python
bench: golden-task
---

# Task 25 — Type hints in a legacy module

**Domain:** python

## Scenario

A 15-year-old financial wrapper: add typing incrementally, pydantic at boundaries, mypy in CI. Plan a migration without rewriting everything.

## What a good answer contains (pass-bars)

Boundary-first; stubs where needed; CI mypy; no big-bang rewrite; runtime safety net of validation models.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `python/typing-models -> python/packaging -> testing/unit-integration`.
