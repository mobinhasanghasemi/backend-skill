# Serverless

## Identity
- ID: architecture.patterns.serverless
- Type: pattern
- Status: active — conditional

## Purpose
Run functions/containers on-demand: cold start to execution, pay per invocation, no server management.

## Core Concept
FaaS (AWS Lambda, Cloud Functions) or managed services; auto-scales to zero; cost = invocations × duration; stateless functions, state in external stores.

## Activation Conditions
- bursty/spiky or irregular workloads (webhooks, cron, image processing)
- event-driven triggers (S3, storage events, queues)
- no ops team for server management
- cost model matches: low steady usage, spiky usage

## Do Not Activate When
- always-on high traffic steady (container = cheaper & stable)
- low-latency requirements (cold start ceiling: tens–hundreds ms; handled with warm keepalive or container)
- long-running processes (jobs > platform limit (e.g., 15 min), websockets, streaming)
- stateful workloads

## Advantages
- Zero ops, auto-scale, cost-matches-usage, fast iteration

## Disadvantages
- Cold starts, cost uncertainty at scale-off, vendor platform constraints (timeouts, exec time), harder local debugging, platform lock-in

## Failure Modes
- Cold start storms under spikes (thundering herd)
- Unscheduled bill explosion (recursion in code!)
- Function timeout = is lost state/partial
- Hot-prime second run fails (concurrency limits)

## Trade-offs
- vs containers: +no servers, −platform cap & cold start
- vs VM: +elastic, −limits

## Security
- Least-privilege IAM; user input only via validated events; secrets via platform secret store (not env in code); Lambda dry-run trick

## Performance
- cold vs warm: measure p99 with cold-start; memory size affects CPU; keep functions lean

## Scalability
- Auto scale per invocation; but careful: concurrency limits, downstream quotas (DB connection storms from many instances)

## Reliability
- Retry semantics (event-driven = at-least-once), DLQ; lambda max retries; plan for duplicate invocations

## Observability
- Always on: logs (platform), tracing (otel), cold-start metric (initDuration)

## Evolution Path
- Start FaaS for spiky event paths; keep always-on API on containers; hybrid normal fine

## Evidence
- Serverless practice mature; AWS SAM/Serverless patterns (VERIFIED concept; constraints change fast — check platform limits each deploy)