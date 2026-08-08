---
title: Distributed lock for a nightly job
domain: distributed-systems
bench: golden-task
---

# Task 22 — Distributed lock for a nightly job

**Domain:** distributed-systems

## Scenario

Two workers must not run the same midnight job. Design a Redis lock: key, TTL, lease renewal, fencing, and behavior past expiry.

## What a good answer contains (pass-bars)

TTL + watchdog renewal; fencing token; consequences of lock expiry mid-job; Redis failure fallback.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `distributed-systems/distributed-locks -> distributed-systems/consensus`.
