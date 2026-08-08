# Metrics Recipes

## Identity
- ID: observability.metrics
- Type: procedure
- Status: active
- Importance: high

## Purpose
Measure what matters (not everything): counters/gauges/histograms, RED/USE patterns, threshold dashboards, and alerts that drive the right action.

## The essentials
- **RED** (for requests): Rate (RPS), Errors (error rate), Duration (latency histogram) — per endpoint
- **USE** (for resources): Utilization %, Saturation (queue length), Errors — per component (CPU, memory, connections, disk work)
- **Business metrics**: orders/min, checkout success, renewal rate — successful product IT visible
- Histograms for latency: p50/p90/p99 (p99 matters more than mean); don't average latencies (gauss lie)
- Label discipline: keep cardinality low (endpoint, tenant/plan counts small) — high-cardinality labels = DB blowup

## Code pattern

### ❌ Bad
```python
# no metrics; or timers as "seconds per call" grep-able somewhere
```

### ✅ Good
```python
from prometheus_client import Counter, Histogram
REQ = Counter("http_requests_total", "", ["endpoint", "status_code"])
LAT = Histogram("http_request_duration_seconds", "", ["endpoint"], buckets=...)
REQ.labels(path, "500").inc(); LAT.labels(path).observe(dt)
```

### ⚡ Better
```python
# queue metrics: queue_depth, age (lag), consumer count/width
# DB: pg_stat_activity active, idle_in_transaction; cache hit rate
# SLO-based: error_budget consumed, good/bad ratio per SLI (reliability/slos.md)
```

### 🏆 Excellent
```text
# dashboards answer questions: how is revenue? (product metrics)
# alert on error budget + saturation (queue length) — not raw CPU
# retention + storage tiering (7 days hot, 10y raw)
# metrics exported via OTel → Prometheus/Grafana; SLOs as multi-window burn rates
# every endpoint counted — handler decorator centrality (no missed path)
```

## Failure modes
- no dashboards → ghosts
- hip-hop label: `user_id` in metric label (cardinality leak!)
- p50-only latency (misses p99 spikes)
- counter reset vs gauge semantics (wrong type = misleading)
- bypass SLO dashboard (metrics don't match promises)

## Evidence
- RED/USE methodology (Google/Booking tr)+ Prometheus docs (VERIFIED)