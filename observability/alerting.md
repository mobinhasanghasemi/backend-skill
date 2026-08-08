# Alerting & On-Call Design

## Identity
- ID: observability.alerting
- Type: procedure
- Status: active
- Importance: high

## Purpose
Alerts that matter (rare, actionable, escalatable) and an on-call rotation that works — no noise, no dead pages.

## Design rules ("alert design" critical path)
1. **Every alert needs action**: if there's no runbook step, it's not an alert, it's a dashboard plot. (each rule → doc link)
2. **Alert on symptoms, not causes**: user-visible (error rate, latency, saturation, budget burn) — not single-entity causes that may self-heal
3. **Budget-style alerting**: error budget burn (fast/slow) instead of raw thresholds — fewer false pages, still catches grinds
4. **Multi-window absence**: alert when metric ABSENT (silent monitoring = no heartbeat)
5. **Alert content**: what, impact, link to runbook, escalation path, last 1h context (links to logs/traces)
6. **Page vs ticket**: page for user impact (billing, auth, data loss); ticket for degradation (queue lag, cache hits)

## On-call structure
- Balanced rotation (1 week, 2-person when big system), documented calendar, gap coverage
- Handover: masthead with top dashboards + top runbooks + incident channel links
- On-call guide: page handling steps (ack → check SLO → incident → review what more could fire)
- Burnout guard: alert sanity reviews (rate pages/human-month), alarm quota reduction program if > 2-3 pages per on-call day

## Classic alert shapes
| Rule | Type | When |
|---|---|---|
| Error budget burn > 5%/1h | page | immediate |
| p95 > SLO 5% in 10m | ticket | daily users |
| Queue lag > 10min | ticket | near-realtime feature |
| No heartbeat > 5m (instance/deploy) | page | infra |
| Auth failures spike > 3x baseline | page (security) | attack |

## Anti-patterns
- 500 alerts nobody resolves (static analysis warns "no owner")
- alert without runbook link
- on-call without dashboard, no escape hatches
- short windows (1-metrics → flapping)

## Evidence
- SRE Workbook Ch. 12 Alerting on SLOs (VERIFIED) + common alerting practice