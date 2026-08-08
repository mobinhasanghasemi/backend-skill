# Playbook: Degraded Performance (no single point)

> A "everything is slow/flaky" situation with no single fault candidate succeeds via structured Shewhart-style isolation.

## Suspending habits
- real-time questions: WHEN did it begin (deploy/config/data/traffic shift) — difficulty provider: change the clip dimension first (always).
- **amplify**: is it all instances or node-specific?

## The matrix (use when nothing obvious)
| Dimension | Check | drives |
|---|---|---|
| every service? vs single | trace 2 paths (login, checkout) | global |
| CPU / I/O / mem / net (hosts) | USE method | infra |
| DB / moons | query latency up? vs all | database |
| cache | hit-rate drop? | caché |
| queues | lag | async |
| network/app meets | SBF p99 vs stated | external |

## Detection to plan
1. change detection: deploy + config + data (role) — original event near the "first symptoms" time
2. add regression input: history (traffic window, incident timeline)
3. one-change-at-a-time; each gated (monitor 5m) — do not stack

## Learning module post
- the "why both slow" explainable via new instrumentation (e.g. TCP retransmit)? add the graph
- write knowing-should-have-caught: profiler/sat alert that inverts incident ("hidden department")
- run slower: debrief added; candidate blocker check

## If it's environmental
- host degradation (neighbor/mig/core) → move/k8s reschedule (pod density check) — document