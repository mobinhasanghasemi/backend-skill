# Playbook: Incident Command (the rock)

> For multi-hour/multi-service incidents: the structure that keeps order (reliability/incident-response.md)

## Activation
- > 15 min unresolved, or affects customers/critical flow → assemble

## Roles (1 person can wear 2 but NOT command+focus)
```
COMMANDER  : owns the decision log, priorities, "who's doing what"
OPERATIONS : doing the work (fix, test, investigate)
COMMS      : updates status page + stakeholders; 5-min rounds
SCRIBE     : the timeline (timestamps, changes, voices) ← the postmortem seed
```

## Loop (every 10-20 min)
1. What is the current UX? (status page text: impact)
2. What are we DOING about it right now?
3. What's the BLOCKER (missing access, tools, keys, unresponded page?)
4. Rollback or not? explicit decision + time

## The moves
- **First**: contain (rollback/shed) → then understand
- **Escalate**: schedule approvals (data changes, kill switches) — one call commander
- **Never**: silent change (all actions in timeline); heroes codeless; overrun (know when to hand over — fatigue at ~8-10h → two-dog watch)

## Exit checklist
- degradationstopped / recovered; customers notified incl. final-state
- DR follow-up (per incident type) queued; postmortem dates; timeline exported
- #lessons: see queued improve; metrics recorded (MTTD/MTTR this one)

## Team discipline
- Commander owns this file as the template; writers append like `incidents/2026-08-01-<x>.md`