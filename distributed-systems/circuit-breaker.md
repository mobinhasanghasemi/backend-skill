# Circuit Breaker

## Identity
- ID: distributed-systems.circuit-breaker
- Type: procedure
- Status: active
- Importance: medium (NOT a default for every call!)

## Purpose
Stop calling a dependency that is failing — fail fast locally instead of hanging/amplifying. **When it's needed**: dependency confirmed degraded (timeouts/5xx at a threshold), and calls are frequent enough to matter. When it's NOT needed: rare calls, internal-only, DB (its own pool/locking covers it) — a timeout+retry policy often suffices (see audit report: don't blanket-apply).

## Mechanics
- States: closed (calls pass) → open (fail fast, no calls) → half-open (probe one) → closed again
- Config: failure threshold (e.g., 50% of last 20), open duration (e.g., 30-60s), success to close (1 successful probe)
- Fallback: what happens in open state (cached value, queue, degraded response, error to user) — REQUIRED design decision
- Bulkhead option: separate pool/concurrency per dependency — complementary, not identical

## Code tiers

### ❌ Bad
```python
def get_geo(ip): return http_call(geo_service, timeout=10)  # no timeout, no break,
# failed dependency → every request waits 10s → pool exhausts → our service down too
```

### ✅ Good
```python
@circuit_breaker(fail_threshold=0.5, window=20, open_seconds=30)
def get_geo(ip): return http_call(geo_service, timeout=3)
# after threshold: calls fail in ~ms with CircuitOpenError
```

### ⚡ Better — fallback + half-open probes
```python
def geo_with_fallback(ip):
    try: return get_geo(ip)
    except (TimeoutError, CircuitOpenError): return CACHED_GEO.get(ip) or DEGRADED_GEO
# half-open: single probe decides re-open vs close (no thundering herd of probes)
```

### 🏆 Excellent
```text
- breakers per dependency per instance; metrics: open-state duration, probe results
- fallbacks tested (degraded path load test); circuit + retry + budget compose
  (retry within closed window; breaker opens after repeated failures)
- chaos drill: kill dependency → verify fast-fail + degraded UX, then recovery
- breaker on the CLIENT side of every integration; never in service-to-service both sides (double-trip)
```

## Failure modes
- blanket breaker on everything (noise, false opens on slow-but-working calls)
- fallback missing → open state returns errors instead of graceful
- breaker with too-short window (transient spike flips states rapidly)
- breaker opening on 4xx (client errors — never the circuit's fault)
- no metrics → nobody knows it opened

## Evidence
- Martin Fowler "CircuitBreaker" (VERIFIED); resilience libraries (pybreaker/tenacity/sentinel docs)