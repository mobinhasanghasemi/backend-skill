# Distributed Monolith

## Identity
- ID: architecture.anti-patterns.distributed-monolith
- Status: active — forbidden
- Severity: CRITICAL

## Definition
A set of services that cannot run/deploy/scale independently because they share the DB, shared code, or sync calls — only the *deployment* is distributed.

## Symptoms
- Every service talks to a shared database/schema
- Change to model affects every consumer
- **Network calls are needed even for trivial unit functions**
- Heavy synchronous call chains; no independent failure
- Scaling one thing still requires coordinating many depoyments

## Why it's a trap
Feels like "modern architecture" (many services) while carrying all the cost (network, ops, consistency) and none of the benefit (independence).

## Causes
- Split services without data ownership discipline
- Team structure cut ignores Conway
- Time pressure → pragmatic shared DB

## Fix
1. **Data ownership first**: each service owns its tables; cross reads via API or event
2. Async contracts for coupling
3. Extract incrementally (strangler-fig)

## Detection (observability)
- DB middleware sees many service principals
- Percentage of cross-service sync calls > 25%

## Evidence
- Widely documented (Martin Fowler "Microservices" essay; modern migration reports) VERIFIED