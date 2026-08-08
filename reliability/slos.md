# SLOs & Error Budgets

## Identity
- ID: reliability.slos
- Type: procedure
- Status: active
- Importance: high

## Purpose
Turn availability/latency promises into measurable, alertable contracts — and decide what to optimize by protecting the budget.

## Model (SLO → SLI → budget)
1. **SLI** — the measurement (e.g., p99 latency over 5 min; availability = good/total)
2. **SLO** — the promise (e.g., "p99 < 250ms 99.9% of the time over 30 days") — MUST be measurable, else it's a slogan
3. **Error budget** = 100% − SLO (e.g., 0.1% = 43 min/month of p99 violation allowance)
4. **Alert at budget burn** (fast + slow burn): alert on burn rate (e.g., 2% budget/hr over 6h, 5% over 1h), not on single bad sign
5. **Budget → action**: remaining budget decides whether new risk (feature/big change) is acceptable

## How to pick an SLO
- Start from user-visible experience (ticket booking must be < 2s), not from infra
- Define windows: 30-day rolling is standard; seasonal workloads need care
- Availability% alone is weak — pair with latency (p95/p99) and freshness (queue lag) where relevant
- One SLO per business-critical path (read/write flows), not per microservice

## Code tiers

### ❌ Bad
```python
# "we aim for 99.99%" — no SLI defined, no measurement, no alert; 
# 1% of requests failing at 12:00 is invisible until tickets
```

### ✅ Good
```python
SLI: requests good = status < 500 and latency < 250ms (p95)
SLO: 99.9% good over 30d     # budget: 43min/month
ALERT: burn > 10% of budget in 24h (fast) or > 50% in 7d (slow)
```

### ⚡ Better — burn-rate alerts
```python
# alert_fast = budget burned at 1day rate > X; alert_slow = 7d rate > Y
# both sexes defined — so a slow grind or a fast burst both page
```

### 🏆 Excellent
```text
- SLIs instrumented per endpoint in code (counters with outcome, latency histograms)
- error budget dashboards: remaining budget by month/week; review at every release
- degraded modes documented ("SLO META: when cache warm, we hold 99.95")
- postmortems use budget burn (was it our budget or someone else's?)
- SLOs renegotiated when infrastructure moves (migration = re-measure window)
```

## Failure modes
- SLO unreachable (99.99 on client network) → demoralizes, false alarms
- latency measured with p50 + made-up p99 sample
- alerting on every dip (no budget) → pager burnout
- no SLI → SLO unmeasurable

## Evidence
- Google SRE Book Ch.4 "Service Level Objectives" (VERIFIED), CRE lifecycle