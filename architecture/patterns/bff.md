# Backend-for-Frontend (BFF)

## Identity
- ID: architecture.patterns.bff
- Type: pattern
- Status: active
- Importance: medium
- **Type**: pattern
- **Status**: active
- Domain: architecture / api

## Purpose
Dedicated backend layer per client-type (mobile, web, desktop, third-party) that shapes data for its own client; hides upstream complexity and aggregates.

## Core Concept
Each interface gets its own BFF service which has its own API contract, transforms downstream responses (microservice/DB), does client-specific logic (pagination shape, field names, sessions), and is the owner of that client's experience.

```
mobile_client → mobile_BFF → (core services / DB)
web_client    → web_BFF    → (core services / DB)
```

## Trigger
- multiple distinct clients with differing data needs/permissions
- wanting to avoid one mega-API that serves everyone

## Do Not Activate When
- one simple client/API shared
- API gateway already handles aggregation; BFF duplication of work

## Advantages
- client-tuned contracts; auth isolation per client; simpler clients; velocity

## Disadvantages
- extra services per client (ops); duplication of logic; each BFF is another team bottleneck; risk of logic spread outside core

## Failure Modes
- BFF becoming a god-service (all core logic)
- duplicate invariants across BFFs (I validate in BFF too??)
- API shape churn in core because BFF changed

## Security
- BFF is a boundary: authN for its client; authZ still enforced in core (trust boundary document!)

## Performance
- BFF aggregation avoids client round trips; keep BFF lean (push aggregation to core/DB when heavy)

## Reliability
- BFF is a dependency of its client; needs SLOs; degrade gracefully when core slow

## Observability
- BFF spans (client call → downstream); per BFF latency/dependency graph

## Testing
- Contract tests per BFF against core; client simulator tests

## Evolution
- Start single API (no BFF); add BFF when second client type emerges with true need