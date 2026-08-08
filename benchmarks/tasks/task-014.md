---
title: Password reset flow
domain: security
bench: golden-task
---

# Task 14 — Password reset flow

**Domain:** security

## Scenario

Web API password reset: token generation, storage, expiry, delivery, brute-force prevention, and lockout-vs-DoS safety.

## What a good answer contains (pass-bars)

CSPRNG tokens; single-use; short expiry; rate limited; account existence not enumerable; no global lockout on login.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `security/passwords-and-tokens -> security/authentication`.
