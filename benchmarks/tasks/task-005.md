---
title: Async worker with DLQ
domain: messaging
bench: golden-task
---

# Task 05 — Async worker with DLQ

**Domain:** messaging

## Scenario

Celery task emails via a flaky third-party API (503s). Design retry policy, backoff, output-side idempotency, and a visible dead-letter path.

## What a good answer contains (pass-bars)

Explicit backoff curve; bounded retries; DLQ queue named with rerun path; alert on DLQ growth; idempotency key per email.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `messaging/celery -> distributed-systems/timeouts-retries -> observability/metrics-recipes`.
