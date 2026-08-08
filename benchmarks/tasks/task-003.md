---
title: Migration strategy for 40M-row table
domain: databases
bench: golden-task
---

# Task 03 — Migration strategy for 40M-row table

**Domain:** databases

## Scenario

PG table, 40M rows, needs a new NULL column + backfill + a partial unique index. Plan migration order, batched backfill without long locks, downtime profile, rollback.

## What a good answer contains (pass-bars)

ADD COLUMN / backfill / index phases isolated; concrete batch size; lock windows stated; rollback SQL planned; autovacuum/analyze scheduled.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `databases/postgresql/migrations -> playbooks/migration-lock`.
