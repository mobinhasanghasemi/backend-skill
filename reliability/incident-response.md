# Incident Response & Postmortems

## Identity
- ID: reliability.incident-response
- Type: procedure
- Status: active
- Importance: critical

## Purpose
When the system is down: contain fast, communicate clearly, coordinate without chaos — then postmortem so it doesn't just happen again silently.

## First 5 minutes (the golden ritual)
1. **Freeze**: stop blind changes ("everyone stop editing")
2. **Can you roll back?** — is there a recent deploy? (rollback first if yes)
3. **Assemble**: incident lead + comms person + 1-3 engineers
4. **Status page update** (even "investigating")
5. **Timeline discipline**: every action logged with a timestamp (the postmortem spine)

## Containment steps (in order of preference)
- **Rollback** the release (best, fastest) — deployment.md ensures this is possible
- **Shed load**: block traffic to the bad pod, kill the heavy query, disable the feature flag
- **Scale down** bad actors: queue pause, consumer stop
- **Isolate**: point traffic around the broken component (feature flag set)
- Only then: root-cause (debug) with the system stable — write the story, not the blame

## The incident channel structure
```
now: <timestamp> <action> <who> <effect>
next: !!pause — hold changes
```

## Postmortem (blameless, 5 why's root-cause)
- timeline (from logs/timestamps — not memory)
- impact: users, SLO budget burned, revenue/care
- cause chain (why → why → why; include the systemic 'our tests missed X')
- detection: how long before alarm? (improve observability)
- actions: PALL (Prevention), P-Det (Detection), PRB (Recovery), each an owner+date
- loop: verify actions deployed after the incident; one-month re-check

## Code tiers — the ops mindset (from bad to excellent)
1. ❌ "all hands on deck" with no lead, no rollback, changes mid-incident
2. ✅ rollback-verified + status page + timeline in channel
3. ⚡ automated rollback, feature flags for instant kill, runbook lookup (SOPS repo)
4. 🏆 game days: storm drill pre-trained responders; MTTR measured; postmortem culture

## Failure modes
- heroics compete with diagnosis; no single timeline
- postmortem blame-culture → the real causes stay hidden
- no rollback capability → hours invented
- actions never followed up (the "TO DO later" ghost)
- status updates not issued (customers blind)

## Evidence
- Google SRE Book Ch.14 "Managing Incidents", blameless postmortems (VERIFIED)