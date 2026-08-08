---
title: Backup / RPO / RTO for payments DB
domain: databases
bench: golden-task
---

# Task 28 — Backup / RPO / RTO for payments DB

**Domain:** databases

## Scenario

1TB PG: pg_basebackup + WAL archiving, RPO, RTO, restore-test cadence, and per-tenant point-in-time restore for support tickets.

## What a good answer contains (pass-bars)

RPO/RTO concrete; full+WAL policy; restore drill on a schedule; per-tenant PITR supported.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `databases/postgresql/backup-restore -> reliability/backups-recovery`.
