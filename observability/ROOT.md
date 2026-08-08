# OBSERVABILITY — ROOT NEURON

## Identity
- ID: observability.root
- Domain: observability
- Type: root
- Status: active
- Importance: critical

## Purpose
The production eyes: logs, metrics, traces, structured events — so any behavior, failure, or regression is provable from measurements, not from guessing in meetings.

## Three pillars + events (the OTel model)
1. **Logs** — records: what happened, when, where (structured, correlated → tracing ids)
2. **Metrics** — counters + histograms: how much, how often, latency distributions (DS for dashboards/alerts)
3. **Traces** — request journey across services: children spans with begin/end + attributes, latency breakdown (the only way to see distributed paths)
(+ events: correlated single-change records — deploy, config, anomalies)

## The instrument-then-ask order
1. Service must emit (request start: method, path, user scope, trace id)
2. Real latencies recorded (histograms, not only totals)
3. DB calls traced (query text, timings, rows)
4. External calls traced (dependency endpoint, status, latency)
5. Queues traced (enqueue, dequeue, work)

Instrument by default: HTTP success/failure by endpoint, DB time per query shape, dependency calls, queues, background jobs, cache hits/misses.

## Routing
```text
logs               → logging-recipes.md
metrics/deriving   → metrics-recipes.md
distributed paths  → tracing.md
pages/alerts       → alerting.md
incident           → reliability/incident-response.md
```

## Metric maturity ladder (honest)
1. no observability: struggles to know "what broke"
2. app + infra metrics (CPU, memory, endpoints) — dashboards exist
3. + error budgets + tracing on critical paths — root-cause times shrink
4. + event correlation & SLOs — reliability analytics; every incident root-caused in the data

## Common failure modes
- "we monitor" = dashboards nobody looks at or alerts that only fire after hours
- sampling drops the tail; alerting on 1 event (noise)
- correlation ids missing → logs trace not searchable
- no structured logs (regex-app — slow, fragile)
- instrumentation countless and conflicting (N dashboards)

## Integration with security/reliability
- audit events (security/logging-and-privacy.md); incident playbooks consume observability
- availability reporting: dashboards must match SLOs (reliability/slos.md) — not the other way

## Evidence
- OTel spec & "Site Reliability Engineering" (VERIFIED concepts); practice standard in SRE