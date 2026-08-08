# Unbounded Queue

## Identity
- ID: architecture.anti-patterns.unbounded-queue
- Severity: HIGH (ARCH_EN6006)

## Definition
A queue/work buffer with no max size: producer can flood consumers.

## Failure chain
- memory growth → node OOM/kill
- backlog latency — messages age → staleness
- on recovery → thundering herd
- cost blow (cloud scale unused)

## Signals
- `queue depth` grows without lower bound
- time to dequeue not monitored
- delete consumer when slow

## Correct design
- bounded queue (max-depth); reject (drop) with alert, or shed
- consumers with backpressure; concurrency limited
- DLQ for poisoned
- alert on lag/depth thresholds

## Where it's naturally OK
- temporary in-memory session-bound queues with bound (e.g., node-replicated bounded)

## Evidence — SRE on queues; industry incidentpostmortems (SUPPORTED)