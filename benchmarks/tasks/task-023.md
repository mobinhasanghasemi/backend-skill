---
title: Saga vs outbox for checkout
domain: distributed-systems
bench: golden-task
---

# Task 23 — Saga vs outbox for checkout

**Domain:** distributed-systems

## Scenario

A checkout involving payment + inventory + shipping. Compare outbox event choreography vs saga orchestration; handle partial failure.

## What a good answer contains (pass-bars)

Compensation per step; ordering; recovery; idempotent compensations; choice justified for the load class.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `distributed-systems/saga -> distributed-systems/outbox`.
