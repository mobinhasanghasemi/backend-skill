---
title: Container image hardening
domain: infrastructure
bench: golden-task
---

# Task 26 — Container image hardening

**Domain:** infrastructure

## Scenario

Dockerfile for a Django API: non-root user, minimal base, multi-stage build, no secrets, image scan, cache-friendly layering.

## What a good answer contains (pass-bars)

Multi-stage; minimal base; non-root USER; no ARG/ENV secrets; cache ordering; scanning in CI.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `infrastructure/containers -> security/secrets -> devops/ci-cd`.
