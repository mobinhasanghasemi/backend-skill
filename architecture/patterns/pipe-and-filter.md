# Pipe and Filter

## Identity
- ID: architecture.patterns.pipe-and-filter
- **ID**: architecture.patterns.pipe-filter
- Type: pattern
- Status: active

## Purpose
Process data through a chain of independent processing stages (filters) connected by pipes (data channels).

## Core Concept
- **Filter**: single transformation unit; each takes input, outputs transformed
- **Pipe**: the connection; simplest form — a queue/hand-off between filters
Pipeline: `read → validate → normalize → enrich → write`

## Activation Conditions
- linear data transformations (ETL, media processing)
- images/video/text pipeline steps are independent
- where the sequence is fixed, stages discrete

## Do Not Activate
- stateful loops/new control structures; interactive flows
- processing where ordering between stages must be strict

## Advantages
- each stage individually testable; parallelizable; swappable stages; readable

## Disadvantages
- fixed topology; latency accumulates; staging duplicates data

## Failure Modes
- a slow stage backs the whole pipeline up (no backpressure design)
- stateful stage bug breaks assumption (filters pure)

## Security
- validate between un-trusted stages (decode boundaries)

## Performance
- parallel lanes when stages independent (split/merge); else the slowest filter dominates

## Reliability
- stage restart granularity; DLQ per stage

## Observability
- per-stage timing/count metrics; logs at handoffs

## Testing
- unit filters; integrate pipeline with fixtures; chaos (crash mid-pipeline recoverability)

## Evidence
- Classic pattern (Pipes&Filters, Op/Unix), stream processors follow this; VERIFIED