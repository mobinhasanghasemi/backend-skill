---
title: Cache stampede protection
domain: caching
bench: golden-task
---

# Task 08 — Cache stampede protection

**Domain:** caching

## Scenario

Expiring hot key: 1ms becomes 400ms at TTL expiry. Solve with background refresh, single-flight, or early refresh; quantify the effect.

## What a good answer contains (pass-bars)

Early recompute + small jitter or single-flight mutex; bounded extra load on miss; measurable improvement.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `caching/strategies -> performance/saturation-scaling`.
