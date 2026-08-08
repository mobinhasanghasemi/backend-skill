---
title: Payment transfer with idempotency
domain: api
bench: golden-task
---

# Task 01 — Payment transfer with idempotency

**Domain:** api

## Scenario

A Django bill-system endpoint POST /api/v1/transfers moves money between accounts. Operators re-send requests on timeout. Design the idempotency contract: key source, storage, replay semantics, error shape, and where a transfer must NOT be retried.

## What a good answer contains (pass-bars)

Idempotency-Key honored; replay returns the original result; amount checked under write lock in the same transaction; double-spend impossible; 409/422 error shape.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `api/rest -> api/idempotency -> databases/relational/transactions -> distributed-systems/outbox`.
