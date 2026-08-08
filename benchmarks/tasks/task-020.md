---
title: Retry/backoff strategy
domain: distributed-systems
bench: golden-task
---

# Task 20 — Retry/backoff strategy

**Domain:** distributed-systems

## Scenario

Design retry policy for outbound calls: exponential backoff, jitter, max attempts, per-route budgets, and what must NOT be retried.

## What a good answer contains (pass-bars)

Formula explicit; jitter included; retry budget; non-idempotent calls not blindly retried; circuit interaction.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `distributed-systems/timeouts-retries`.
