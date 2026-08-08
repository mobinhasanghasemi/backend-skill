# Playbook: Capacity Crash (Peak Overload)

> When load (=2-5x normal) hits: the system degrades across everyone. First principle: preserve the SALIENT kernel (authenticated write path) and shed the rest.

## Immediate response
1. **Identify what broke**: error rate by endpoint; load vs saturation (which resource: CPU? connections? thread pool? queue?)
2. **Shed non-essential**: feature flags off (heavy reports, expensive endpoint); pause non-critical cron; scale out temporarily (cheap wins)
3. **Protect the core**: rate-limit aggressive consumers; cancel LEAN paths (metrics realtime backoff); DB connections preserved for vital calls
4. **Turn the knob**: kill = nothing; throttle (503 with Retry-After) vs queue growth—prefer early rejection (saturation-scaling.md)

## Search memory (cause by shape)
- **Launch / campaign / viral**: provisioned ahead via capacity-planning tables (DAU × peak multiplier); scale test (load-testing) validates BEFORE rush hour
- **Failure cascade**: upstream slows → our pool drains (error/echo); clients retry → amplification — to break: retry backoff + circuit (timeouts-retries.md)

## Post-incident protocol (12h)
- auto scale: trigger on queue depth + latency (they protect); capacity levers (replicas, workers) set and validated
- load-test replay with recorded traffic (production-shaped) — not post-cooked numbers
- SOC: record consumed (what helped/what helped little); final ADR

## Culture band checks
- DORA post-incident (blameless); no hero notes (roll instead)
- Simulate in staging; she queued predictions.