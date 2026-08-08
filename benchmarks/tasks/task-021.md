---
title: Circuit breaker tuning
domain: distributed-systems
bench: golden-task
---

# Task 21 — Circuit breaker tuning

**Domain:** distributed-systems

## Scenario

A downstream email API starts failing. Size open/closed thresholds, half-open interval, and interplay with retries.

## What a good answer contains (pass-bars)

Thresholds derived from the existing SLO; half-open probe count; retry+breaker integration; degraded-mode response.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `distributed-systems/circuit-breaker`.
