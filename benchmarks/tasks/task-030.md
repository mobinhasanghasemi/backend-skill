---
title: RAG cache + cross-tenant isolation
domain: ai-backends
bench: golden-task
---

# Task 30 — RAG cache + cross-tenant isolation

**Domain:** ai-backends

## Scenario

An LLM endpoint summarizes documents. Design cache keying, and per-tenant isolation, and what must never enter cache.

## What a good answer contains (pass-bars)

Tenant-scoped cache; namespaces for embeddings; never cache secrets/private docs; leak test in CI.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `ai-backends/rag -> ai-backends/semantic-caching -> security/authorization`.
