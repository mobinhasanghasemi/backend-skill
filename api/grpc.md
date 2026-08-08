# gRPC

## Identity
- ID: api.grpc
- Type: technology
- Status: active
- Importance: medium-high

## Purpose
High-performance, typed, contract-first RPC for internal services: Protocol Buffers, HTTP/2, streaming, auto-generated clients. Choose when performance/type-safety matter more than debuggability.

## Core concepts
- `.proto` definitions → code generation (types + stubs)
- Unary, server-streaming, client-streaming, bidi-streaming
- HTTP/2 multiplexing; protobuf binary encoding (vs JSON)
- Service mesh / load balancing with retries & deadlines

## When gRPC wins
- internal microservice communication (latency, throughput, typed contracts)
- streaming (telemetry, logs, data feeds)
NOT: public web/mobile API without grpc-web bridge, curl-debuggability matters, tiny scale (REST fine)

## Code tiers

### ❌ Bad
```python
# no proto, no deadlines:
# internal service call with HTTP JSON + retries in each client  # no type safety, hidden latency
```

### ✅ Good — proto + stubs + deadlines
```proto
service Payments { rpc Charge(ChargeRequest) returns (ChargeResponse); }
message ChargeRequest { string user_id = 1; int32 amount_cents = 2; }
```
```python
with grpc.insecure_channel("payments:50051") as ch:   # (TLS in prod!)
    stub.Charge(req, timeout=5)                       # explicit deadline
```

### ⚡ Better
```python
# interceptors: auth metadata, logging/tracing (opentelemetry), retry policy, 
# errors: gRPC status codes (UNAVAILABLE → retry, INVALID_ARGUMENT → no retry)
# health check (grpc.health.v1) wired to orchestrator
```

### 🏆 Excellent
```text
- proto versioned, buf lint + breaking-change check in CI
- TLS everywhere (mTLS between services); auth metadata injection
- streaming with backpressure; client-side deadlines + retry budget (avoid cascades)
- observability: per-method p50/p95, error rate, trailers for details
- load test with real protos (ghz)
- fallback strategy documented if infra doesn't support HTTP/2 end-to-end
```

## Failure modes
- no deadlines → cascading hang (thread/goroutine leak)
- binary errors invisible (map status to human-readable detail in trailers)
- versionless protos breaking consumers
- nginx without HTTP/2 support breaking calls silently

## Security
- mTLS, metadata auth, rate limits, no PII in debug logs

## Evidence
- gRPC concepts (protobuf, streaming): SUPPORTED practice (gRPC docs, not URL-pinned)
