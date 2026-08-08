# Distributed Tracing

## Identity
- ID: observability.tracing
- Type: procedure
- Status: active
- Importance: high

## Purpose
See a request's journey across services/DB/queues in one view: where time went, where it failed. Tracing is the only observability that answers "why is this ONE user's request slow".

## The model (OpenTelemetry)
- **Trace** = tree of **spans**. Span: `{name, start_time, duration, status, attributes, parent_id}`
- Context propagation: each span carries `trace_id`, `span_id` via headers (`traceparent`) in every downstream call (HTTP, gRPC, queue messages)
- Classify each span type: `CLIENT` (call), `SERVER` (handling), `INTERNAL` (work), `PRODUCER`/`CONSUMER` (queue)
- Collect: OTel SDK → OTLP → Collector → Jaeger / Tempo / Zipkin / Datadog
- **Why sampled**: full tracing % needs sampling at high RPS; retain 100% forever is not needed — sample hot paths 10-100%, errors always!

## Instrumentation recipe
1. Auto-instrumentation first (framework/HTTP libs/enqueue) — free basics
2. Then: DB queries, cache, external HTTP, serializers, queue job execution (each a span)
3. Custom attributes worth tracing: checkout tabs, retries, auth method, rate limit triggers
4. Verification: one synthetic call in staging shows full journey windows from start to end

## Code pattern

### ❌ Bad
```python
# no traces: support says "their request was slow"; nothing shows where
```

### ✅ Good
```python
with tracer.start_as_current_span("db.query") as span:
    span.set_attribute("db.system", "postgresql")
    span.set_attribute("db.query_text", sql[:200])
```

### ⚡ Better — automatic + manual
```python
# OTel auto-instrumentation wraps framework + repeat (DB/HTTP); 
# manual spans on business steps: "payment.authentication", "order.audit"
# trace.sampled: start errors always; 10% sample of normal traffic
```

### 🏆 Excellent
```text
# correlation: logs carry trace_id (find all logs of a single request in seconds)
# SLO latencies in traces, store-ignore keys, costly spans flagged
# cross-service propagation across queues (kafka headers, celery stub task id)
# trace leak detection: trace_id absent in outbound → test catches propagation bug
# postmortems glued to traces (instrumented incidents in the postmortem)
# sampling policy reviewed vs volume: drop harmless, keep errors + slow traces
```

## Failure modes
- instrumented but nothing propagates (fake traces without ids)
- sampling on errors default (errors uninteresting rarely same)
- traces only entry points (inner work hidden)
- too-heavy overhead — overhead measurement required at scale

## Evidence
- OpenTelemetry spec + "Distributed Systems Observability" (VERIFIED); Jaeger/Tempo docs