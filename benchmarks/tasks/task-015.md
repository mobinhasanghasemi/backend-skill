---
title: Rate limiter design
domain: api
bench: golden-task
---

# Task 15 — Rate limiter design

**Domain:** api

## Scenario

Design per-API-key rate limiting in front of Django. Window algorithm, shared storage, distributed correctness, 429 semantics, Retry-After.

## What a good answer contains (pass-bars)

Token bucket or fixed-window stated; Redis-backed correctness on two nodes; 429 + Retry-After; user-vs-key separation.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `api/rate-limiting -> caching/strategies`.
