# ANTI-PATTERNS — ROOT NEURON

## Identity
- ID: architecture.anti-patterns
- Type: knowledge of antipatterns
- Domain: architecture

## Purpose
Catalog the ways architectures fail — the negative knowledge that complements pattern knowledge. An anti-pattern is a recognizable, recurring structure that *feels* like a solution but compounds failure.

## Using this knowledge (AI Instructions)
When conflicts arise on a design, or a proposal shows a pattern, cite the anti-pattern:

```
⚠ anti-pattern: distributed-monolith
   signal: services share a DB, sync call chains
   fix: (data ownership first, then async/queue)
```

## All-known entries
| Anti-pattern file | TL;DR |
|---|---|
| distributed-monolith.md | services w/o isolation — worst of both worlds |
| god-database.md | everyone writes to one DB = hidden coupling |
| database-as-queue.md | using the DB as a job queue |
| sync-chains.md | long synchronous dependency trees |
| caching-everything.md | cache all endpoints without measurement |
| premature-optimization.md | optimize every path, or without profile |
| single-point-of-failure.md | one node with no redundancy |
| unbounded-queue.md | memory queue growing without end |
| big-bang-rewrite.md | rewrite the whole system at once (strangler instead) |

## Detection workflow

1. Compare architecture_genome against any components list
2. For each heuristic: (ARCH-lint as accelerator)
3. Verify with evidence (logs, metrics) before asserting

## Failure horizon
Anti-patterns map to real incidents; each file states where each arises (see playbooks/)