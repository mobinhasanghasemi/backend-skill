# Failure Injection & Chaos Testing (risk-based)

## Identity
- ID: reliability.chaos-testing
- Type: procedure
- Status: active
- Importance: medium (dose it, don't worship it)

## Purpose
Prove resilience claims by safely breaking things in controlled environments — the difference between "designed to be resilient" and "verified resilient". Dose = risk-based, never a calendar ritual alone.

## The honest framing
- Start in staging/clean room: kill a DB node, a consumer, a dependency call
- Prioritize: the failure paths with highest impact × likelihood (see failure-propagation)
- Frequency: episodic game days (quarterly) + automated smoke of "lifesavers" (rollbacks, restores) in CI
- Scope: restore drills monthly (cheap), full DR quarterly, chaos on prod only with SOMA approval + flags to abort instantly

## The ladder
1. **Configuration chaos**: read-only test, rolling restart (operator errors)
2. **Dependency chaos**: stop a Redis/Mongo/queue/dependency; assert fallback/degraded path (circuit breaker opens)
3. **Data chaos**: latency injection (tc netem/toxiproxy), DB throttle, disk full, clock skew
4. **Process chaos**: kill replicas mid-request, kill the queue consumer, kill the app pod
5. **Region chaos** (rare): failover to DR region (annual), documented

## Post-chaos discipline
- One finding = one tracked improvement + owner
- Re-run after fixes; regression gate: the chaos test becomes part of CI (like restore test)
- Never chaos where the test itself would damage the service (only safe failures)

## Anti-patterns
- chaos marathon in prod without abort/reset button (responsibility breach)
- chaos without observers (no metrics capture during the game)
- chaos results unreviewed (no improvement loop)
- catalog of "we know it fails" — must fix or document accepted risk

## Example session (60 min)
1. Choose one path: "payment webhook consumer"
2. Kill consumer → 20 min; observe: queue growth, alerts fire, no data loss
3. Restore → consumer replays → verify idempotent delivery (dedupe)
4. Report: detection time, recovery time, what we enabled next ("missing alarm on queue lag")

## Evidence
- Principles of chaos engineering (VERIFIED; Netflix, Google) — and risk-based application guidance