---
title: Secrets committed in repo
domain: security
bench: golden-task
---

# Task 12 — Secrets committed in repo

**Domain:** security

## Scenario

Repo contains API keys, a DB password, and an AWS secret. Plan removal, storage shape, rotation, and a CI scan gate.

## What a good answer contains (pass-bars)

Immediate secret scan; rotate everything (assume breach); env/secret-manager storage not settings.py; CI gate documented.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `security/secrets -> devops/ci-cd -> security/ROOT`.
