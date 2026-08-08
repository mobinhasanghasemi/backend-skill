---
title: K8s secrets for a DB password
domain: infra
bench: golden-task
---

# Task 27 — K8s secrets for a DB password

**Domain:** infra

## Scenario

Deploy Django on K8s: where the DB password lives (Secret vs external store), rotation, and RBAC for readers.

## What a good answer contains (pass-bars)

No secrets in repo YAML; externalized or in-cluster with tight RBAC; rotation strategy; audit trail.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `infrastructure/kubernetes -> security/secrets`.
