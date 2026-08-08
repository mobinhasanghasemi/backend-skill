---
title: Async vs threads in FastAPI
domain: python
bench: golden-task
---

# Task 24 — Async vs threads in FastAPI

**Domain:** python

## Scenario

Mixed workload: fast I/O + heavy CPU + blocking DB. Compare asyncio vs threads vs processes, the event-loop-blocking trap, DB pooling.

## What a good answer contains (pass-bars)

Async for I/O; threadpool for blocking libs; multiprocess for CPU; pool sizes; no async-in-sync footgun left unexplained.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `python/async-python -> python/threads-processes -> python/web-frameworks`.
