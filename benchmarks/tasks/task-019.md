---
title: Incident runbook — queue backlog
domain: reliability
bench: golden-task
---

# Task 19 — Incident runbook — queue backlog

**Domain:** reliability

## Scenario

Write the first 30 minutes of an incident runbook for 'orders delayed' (queue backlog + slow hot index). Prioritized actions.

## What a good answer contains (pass-bars)

Containment before root-cause; index add under lock; backlog drain plan; rollback ready; business-impact notification.

## Scoring

Apply `rubric.md` (dimensions D1–D6). Expected activation path: `playbooks/queue-backlog -> playbooks/slow-database`.
