---
title: TLS posture for public API
domain: security
bench: golden-task
---

# Task 13 — TLS posture for public API

**Domain:** security

## Scenario

Design TLS: version policy, ciphers, termination point (LB vs app), HSTS, certificate rotation/ACME.

## What a good answer contains (pass-bars)

TLS 1.3 for new, 1.2 fallback allow-listed; termination at the edge; HSTS; automated renewal; upgrade path documented.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `security/cryptography -> security/ROOT`.
