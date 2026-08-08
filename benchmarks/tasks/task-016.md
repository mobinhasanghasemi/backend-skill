---
title: Logging without PII
domain: observability
bench: golden-task
---

# Task 16 — Logging without PII

**Domain:** observability

## Scenario

Structured logging for a payments service: fields, PII denylist, sampling for hot paths, correlation with traces.

## What a good answer contains (pass-bars)

Log format agreed; PII fields enumerated and dropped; per-endpoint sample rates; trace_id propagation.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `observability/logging-recipes -> security/logging-and-privacy`.
