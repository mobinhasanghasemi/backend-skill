---
title: Redis invalidation on write
domain: caching
bench: golden-task
---

# Task 07 — Redis invalidation on write

**Domain:** caching

## Scenario

Django caches product prices; writes must invalidate and reads stay fresh. Choose invalidation policy (versioned key vs delete) + TTL; explain the naive failure at replicas.

## What a good answer contains (pass-bars)

Versioned key as the strong option; delete on write; no stale-serving path; cache-aside semantics explicit.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `caching/invalidation -> caching/strategies -> django/caching`.
