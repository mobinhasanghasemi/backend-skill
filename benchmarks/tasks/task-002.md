---
title: DRF list pagination + filter whitelist
domain: api
bench: golden-task
---

# Task 02 — DRF list pagination + filter whitelist

**Domain:** api

## Scenario

Expose GET /api/v1/orders?status=paid&limit=50&before=... for a few million orders. Choose pagination, filter design, and indexing; state what changes at 50M rows.

## What a good answer contains (pass-bars)

Keyset favored for live data; index justified for the filter; no raw filter injection; growth answer mixes re-index + partition note.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `api/pagination -> api/rest -> databases/optimization/query-optimization -> django/drf`.
