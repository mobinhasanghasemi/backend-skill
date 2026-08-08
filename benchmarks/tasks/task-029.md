---
title: gRPC vs REST for an internal service
domain: api
bench: golden-task
---

# Task 29 — gRPC vs REST for an internal service

**Domain:** api

## Scenario

A new internal service consumed by another team: weigh REST vs gRPC — protobuf versioning, streaming, tooling, learning cost.

## What a good answer contains (pass-bars)

Decision criteria make the trade-off explicit; protobuf schema evolution handled; gateway/compat story.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `api/grpc -> api/rest -> api/versioning`.
