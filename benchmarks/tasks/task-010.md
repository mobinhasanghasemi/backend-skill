---
title: OAuth2/OIDC client_credentials
domain: security
bench: golden-task
---

# Task 10 — OAuth2/OIDC client_credentials

**Domain:** security

## Scenario

B2B Django API: partners call with client_credentials. Cover token verification (JWKS), audience, scope-to-RBAC mapping, revocation, and rate-limit interplay.

## What a good answer contains (pass-bars)

JWKS fetched and validated; audience checked; scopes to RBAC; revocation honest (async noted); retry-safe 401.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `security/authentication -> security/authorization -> api/rate-limiting`.
