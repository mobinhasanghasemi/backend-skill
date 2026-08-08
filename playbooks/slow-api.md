# Playbook: API Slow / High Latency

## Symptoms
- endpoint p95 climbing; timeouts; degraded UX; alerts on SLO burn

## Fast path
1. Is it ONE endpoint or all? → endpoint breakdown (UV trace: app_time vs db_time vs external time) — tracing.md
2. DB query time (the classic) → slow-database playbook + EXPLAIN
3. External dependency (payment/GPS/providers) → their p50/p95; circuit breaker? timeout budget
4. Serialization/queue in the app → profiler (py-spy) on the host
5. Cache misses / cold start (freshly deployed)?? → warm-up
6. Infra (CPU steal, throttling, iops) → infra metrics (USE)

## The 30-min rule
- You have a budget: find the >60% cost component FIRST (trace), fix THAT (index/timeout/cache), remeasure. Do not stack optimizations blindly.

## Common root causes
- N+1 in serializer (django/orm.md)
- unbounded list endpoint (pagination! cursor)
- blocking call in async handler (event loop stall) — async-python.md watchdog
- external call without timeout (dependency) — timeouts-retries.md
- GC/I/O spike: memory or disk pattern problems

## Verification
- Before/after trace to the same flow: end-to-end split reduced, p95 target in budget (latency-optimization.md)
- Add regression: assertion test on slow endpoint budget, monitoring alert (the burn)

## ADR
- record: what was rewired + measured gain (numbers, payloads, window)