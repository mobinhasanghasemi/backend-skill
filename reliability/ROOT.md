# RELIABILITY — ROOT NEURON

## Identity
- ID: reliability.root
- Domain: reliability
- Type: root
- Status: active
- Importance: critical

## Purpose
Make failures **visible, contained, and recoverable** — by contract (SLOs), by design (failure isolation), and by practice (drills). Reliability is a measured property, not a vibe.

## Activation
- production claims, on-call, RPO/RTO, backups, failover, incident analysis
- resilience design review (timeouts, pools, retries, fallbacks)
- deployment safety discussion

## Routing
```text
numeric promise      → slos.md (SLO/error budget)
incident happening   → incident-response.md (playbook)
deploy risk          → deployment.md (progressive delivery)
data loss threat     → backups-recovery.md (3-2-1, drills)
failure tolerance    → distributed-systems/* (timeout/breaker/outbox) + brain/failure-propagation
load resilience      → performance/saturation-scaling + api/rate-limiting
```

## The reliability triad
1. **Contract**: SLO with error budget — livable promise, alert only when budget burns
2. **Design**: dependency failures contained (isolation, pooling, timeouts); blast radius bounded
3. **Practice**: drills (restore, failover, chaos — **risk-based**, not calendar theater)

## Mandatory questions
- What is the failure that ends the service? What do we do inside 5, 15, 60 minutes?
- What's the blast radius of each component down? (map thanks: failure-propagation)
- Untested backup = no backup (drill or admit RPO/RTO unproven)
- How do we *know* it's degraded? (observability hooks)
- Can we roll back a bad release in minutes? (deployment.md)

## Common failure modes
- SLO written, nothing measures it → false confidence
- monitoring only "up/down" — no saturation/latency insight
- backup exists, restore never tested
- deploying big-bang with no rollback plan
- reliability theater: playing books but no drills

## Evidence
- Google SRE books/site-reliability-engineering (VERIFIED practice), error budgets; "Designing for Resilience" reports