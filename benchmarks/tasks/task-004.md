---
title: N+1 to keyset EXPLAIN
domain: databases
bench: golden-task
---

# Task 04 — N+1 to keyset EXPLAIN

**Domain:** databases

## Scenario

Django endpoint listing accounts with orders is slow (classic N+1). Produce: repro query, EXPLAIN reading, the ORM fix, and a keyset vs OFFSET decision.

## What a good answer contains (pass-bars)

Real SELECT with JOIN; index suggestion; no OFFSET on deep pages; EXPLAIN (ANALYZE, BUFFERS); no invented function.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `django/orm -> databases/postgresql/query-planner -> performance/profiling`.
