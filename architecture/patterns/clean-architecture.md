# Clean Architecture

## Identity
- ID: architecture.patterns.clean-architecture
- Type: pattern
- Status: active

## Purpose
Keep the business logic independent of frameworks, databases, and UI. Dependency rule: source code dependencies point INWARD toward entities/use cases.

## Core Concept
Concentric circles: Entities (business rules) ← Use Cases ← Adapters/Interface adapters ← Frameworks & Drivers. Inner circles know nothing of outer. Interfaces defined inside, implementations outside.

## Mental Model
A fortress: the core (domain) never sees the outside; the walls (interfaces) let the outside (framework, DB, UI) talk through gates (adapters).

## Activation Conditions
- long-lived products with complex business rules
- expected multiple UIs / DB swaps / heavy testing
- DDD-style modeling desire

## Do Not Activate When
- small CRUD apps: ceremony costs more than benefit (Governor)
- team not familiar with the pattern (learning curve risk)

## Advantages
- Testable domain without infra; framework-independent core; changeable UI/DB/API

## Disadvantages
- Boilerplate (interfaces, mappers, DTOs)
- Over-engineering risk for simple systems
- Mapper maintenance (model ↔ entity)

## Failure Modes
- Golden hammer: applying to trivial apps → cost > benefit
- Entities duplicated with ORM models → mapper drift
- Over-abstraction (interfaces with single impl)

## Trade-offs
- vs layered: +domain protection, −ceremony

## Security
- Validate at adapter boundary (input), enforce authz in use cases (not UI)

## Performance
- Mapper overhead minor; watch N+1 through repository interface (design queries in adapter)

## Scalability
- Clean structure scales in maintainability; runtime scaling is orthogonal (stateless core)

## Reliability
- Framework swap easier → resilience to vendor issues

## Observability
- Instrument at adapter boundaries (use case = span)

## Testing
- Domain tests (no DB), integration at adapters, contract tests

## Evolution Path
- From layered: introduce interfaces at service layer gradually

## Evidence
- Uncle Bob's Clean Architecture (VERIFIED as pattern concept; apply with judgment)