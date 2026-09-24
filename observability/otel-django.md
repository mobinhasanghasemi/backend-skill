# OTel Django — Tracing + Metrics + Logs

## Identity
- ID: observability.otel-django
- Domain: observability
- Type: procedure
- Status: active
- Importance: high
- Last Verified: 2026-08

## Purpose
Make Django observable with OpenTelemetry: one trace per request that links app → DB → cache → queue, with RED metrics and correlated logs.

## Core Concept
Instrument once at WSGI/ASGI middleware; propagate `traceparent`; export via OTLP to collector; never log PII.

## Activation Conditions
- Any prod Django/DRF service; S-055 relevant; when SLO or p95 budget exists

## Decision Rules
- SDK: `opentelemetry-django` + `opentelemetry-instrumentation-psycopg` + `opentelemetry-instrumentation-redis` + `celery` instrumentor (S-055).
- Tracing: sample `parentbased_traceidratio` 0.1 in prod, 1.0 on error; always sample slow (>p95).
- Metrics: RED per endpoint (`http.server.duration`, `db.client.connections`, `cache.hit_ratio`); exemplars link metric → trace.
- Logs: struct JSON, include `trace_id`/`span_id`, strip PII (S-078).

## Security
- No secrets/PII in attributes; filter `Authorization` header; S-078.

## Performance
- BatchSpanProcessor, 512 queue, 5s export; <1% CPU at 1k req/s (measure).

## Reliability
- Collector as sidecar; retry with backoff; no block on export failure; health check on `/healthz` excludes OTel.

## Evidence
- OTel Python SDK VERIFIED via S-055 (accessed 2026-08); logging hygiene via S-078.

## Code Tiers
<!-- executable -->
```python
# Django settings — OTel bootstrap (executable, verify SDK version)
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
DjangoInstrumentor().instrument(is_sql_commentor_enabled=True)
PsycopgInstrumentor().instrument(enable_commenter=True, commenter_options={})
```
