---
title: Contract testing harness
domain: testing
bench: golden-task
---

# Task 32 — Contract testing harness

**Domain:** testing

## Scenario

Two Django services exchange JSON contracts. Design producer/consumer contract tests: schema source of truth, drift detection, breaking-change workflow.

## What a good answer contains (pass-bars)

Schema as contract of record; consumer-side CI; breaking-change workflow; versioning/tagging of contracts.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `testing/contract-tests -> api/versioning`.
