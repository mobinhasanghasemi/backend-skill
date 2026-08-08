# Onion Architecture

## Identity
- ID: architecture.patterns.onion
- Type: pattern
- Status: active

## Purpose
Dependency-based layering where inner layers (Domain Model, Domain Services) are purity islands; the Application layer orchestrates, outer Infrastructure adapts. Dependencies point inward; interfaces (repository, notification) defined in application, implemented in infra.

## Core Concept
Same dependency rule as Clean (this is its DDD-flavored sibling): domain entities → domain services → application services → infrastructure (outer shell).

## Mental Model
An onion: peel layers outward (infra) to reach the pure core.

## Activation
- DDD team with rich domain, CQRS pairs well (commands write domain, queries read models)

## Do Not Activate When
- CRUD-only; the multiplicity of layers = overhead

## Advantages / Disadvantages
+ Domain purity, testable, structured for DDD.
− Layer ceremony, discipline required.

## Failure Modes
- Entities never interact with DB → lazy-loading N+1
- Nebula of application services doing glue work

## Trade-offs
- vs hexagonal: same essence; onion organizes by dependency direction more prescriptive

## Security
infra implements permission ports; domain never sees security artifacts

## Performance
- mapping layers; batch operations in application layer

## Scalability / Reliability
- stateless core; infra adapters

## Observability
- app-layer span boundaries

## Testing
- domain tests pure; app layer unit; adapters integration

## Evidence
- Onion Architecture (Palermo'08) — VERIFIED concept; mature practice literature