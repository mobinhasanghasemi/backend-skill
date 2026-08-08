---
title: Outbox for webhook delivery
domain: messaging
bench: golden-task
---

# Task 06 — Outbox for webhook delivery

**Domain:** messaging

## Scenario

Order creation must reliably emit an event; delivery at-least-once without a distributed tx. Design the transactional outbox, dispatcher, and replays.

## What a good answer contains (pass-bars)

Event INSERT inside the SAME DB transaction; idempotent dispatcher; published-row cleanup; consumer deduplication; replay guard.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `distributed-systems/outbox -> databases/relational/transactions -> messaging/ROOT`.
