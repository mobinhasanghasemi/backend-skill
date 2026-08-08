---
title: RLS vs app-enforced authz
domain: security
bench: golden-task
---

# Task 11 — RLS vs app-enforced authz

**Domain:** security

## Scenario

One PG schema, many tenants. Compare app-level tenant filter vs RLS policies; decide for a 50-tenant SaaS; list RLS bypass paths.

## What a good answer contains (pass-bars)

Tenant key propagation; policy syntax shown; superuser/extension bypass paths called out; decision table.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `multi-tenancy/ROOT -> databases/postgresql/rls -> security/authorization`.
