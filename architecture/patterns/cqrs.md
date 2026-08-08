# CQRS

## Identity
- ID: architecture.patterns.cqrs
- Type: pattern
- Status: active — conditional

## Purpose
Separate the read path from the write path. Writes use commands (domain model), reads use dedicated optimized queries/read models.

## Core Concept
One logical system, two sides: Command model (business rules, writes) and Query model (denormalized read projections). Could be same DB (same tables for reads at times) or separate stores (with sync via events).

## Activation Condition
- hot reads shape wildly different from writes (reports, dashboards, reads at 100x write rate)
- complex domain writes with independent queries

## Do Not Activate
- CRUD with 1:1 read/write shape (adds second stack of traversal)
- single service, easily managed by the team

## Advantages
- Reads optimized freely (indexes, denormalization, projections); writes independent; scaling per side

## Disadvantages
- Two code paths; consistency between write & read (eventual, trickle); ops complexity if separate stores; DTO/query doubling

## Conflicts
- requires strong consistency on read-after-write? CQRS can hurt; design read model update fast or cache-write-through

## Failure Modes
- Read model drift (query no longer reflects domain rules)
- Duplicated logic in query side
- sync mechanisms (outbox/events) failing silently

## Security
- The read side must still enforce authz (query for tenant/data classes), both sides validated

## Performance
- The purpose: readings cheap; writes unblocked

## Scalability
- Scale query side independently (replicas); write side small

## Reliability
- Read model recreation from event stream; PITR for reads

## Observability
- Lag between write → read model; async sync monitoring

## Testing
- Property tests on projections; contract on read models

## Implementation Guidance
- Start with same-DB CQRS (query over separate materialized views/indexes); separate storage only when measured need

## Evidence
- CQRS (Young, Fowler) — VERIFIED concept; apply when the problem shape matches; not a silver bullet