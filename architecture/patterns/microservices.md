# Microservices

## Identity
- ID: architecture.patterns.microservices
- Type: pattern
- Status: active — conditionally recommended
- Importance: critical

## Purpose
Independent deployable units per business capability, communicating over the network, each owning its data.

## Core Concept
Each service = its own DB/schema (data ownership!), its own deployment, its own lifecycle. Communication: HTTP/events. Contracts matter.

## Mental Model
A federation of small nations: each with own laws (schema), embassy (API), borders (network), and passport (auth).

## Activation Conditions
- multiple independent teams with independent release cadence
- measured need to scale specific components independently
- hard isolation (compliance, security) between domains
- polyglot needs

## Do Not Activate When
- single team, no independent scaling need → modular monolith (Governor)
- project has no ops capability for distributed debugging
- integration latency dominates (local function >> RPC)

## Advantages
- Independent deploy/scale per team
- Technology freedom per service
- Failure isolation (bounded blast radius)

## Disadvantages
- Distributed complexity (network, retries, partial failure, consistency)
- Data consistency pain (no ACID across services)
- Debugging across hops is harder
- More moving parts: registry, tracing, observability, contracts

## Failure Modes
- **Distributed monolith** (shared DB, sync call chains) — worst outcome (see anti-patterns)
- Chatty sync dependencies → latency & cascade
- Version drift in contracts → schema chaos
- Team-level Conway errors: teams split wrongly → every change crosses a network

## Trade-offs (triad)
- Performance: + horizontal scale, − per-call overhead, +tail-latency risk
- Security: + isolation, − larger attack surface, need mTLS/authz per hop
- Reliability: + bounded failure, − partial failures need handling everywhere (timeouts, circuit breakers, retries, idempotency)

## Scalability
- The point of the pattern — each service scales to its own demand
- Watch for: shared caches (boundedness), hot shared resources (DB), fan-out storms

## Reliability
- Requires discipline: timeouts, circuit breakers, bulkheads, health checks, per-service SLOs
- Saga for multi-service transactions (distributed-systems/saga.md)

## Observability
- **Non-negotiable**: distributed tracing (otel), per-service metrics/logs, correlation IDs, dependency graphs

## Security
- Zero-trust: each service authenticates/authorizes every hop (mTLS/OTLP), never trust internal network
- Secrets per service, least-privilege DB roles

## Testing
- Contract testing across boundaries (pact-style), consumer-driven
- Chaos testing for partial failures

## Migration Path
- Start modular monolith → extract hottest, most-independently-scaled service via strangler-fig; data first, then code

## Alternatives
- Modular monolith (default), cell-based architecture (for isolation at scale)

## Version Awareness
- Pattern stable; implementation practices evolve (see distributed-systems/, messaging/)

## Evidence
- Pattern literature: Newman "Building Microservices", Google SRE, production evidence (VERIFIED pattern; applied choices are decision-level)

## AI Instructions
- Run SIMPLICITY_GOVERNOR before recommending. If the user says "scale", ask: which resource? which component? — microservices rarely fix the real bottleneck
- Always pair with failure-model cards and observability requirement
- Remind: microservices solve *team and scale* problems, not code quality