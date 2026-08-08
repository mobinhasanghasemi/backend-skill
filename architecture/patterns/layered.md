# Layered Architecture

## Identity
- ID: architecture.patterns.layered
- Type: pattern
- Status: active — classic default

## Purpose
Structured dependency flow: Presentation → Application → Domain → Data (top-down). Each layer depends on the one below.

## Core Concept
Classic N-tier: controllers (HTTP) → services (use cases) → repositories/data. One-directional dependencies; lower layers know nothing of upper.

## Mental Model
An office tower: reception (web), floors of departments (business), basement of records (DB).

## Activation Conditions
- enterprise apps with conventional web/DB architecture
- teams familiar with the shape
- Django/Spring/ASP.NET style projects — matches framework conventions

## Do Not Activate When
- need for testability that pure layers don't give (dependencies in one direction only, DB-agnostic domain) → hexagonal
- rich domain logic needing isolation from framework (DDD)

## Advantages
- Simple to understand, wide tooling support, straightforward to teach
- Matches frameworks (Django views→services→ORM)

## Disadvantages
- Domain gets pushed down to the bottom (data model becomes the domain)
- Repository abstraction leaks ORM details
- Hard to test the upper layers without the framework

## Failure Modes
- Layer-skipping (views hit repositories) — drift
- DTO soup (duplication of models)
- Big service layer = god classes

## Trade-offs
- vs hexagonal: +simpler, −domain coupling to infra

## Security
- Put authz at application layer; never trust UI constraints

## Performance
- N+1 risks at repository boundary; page services query-shape

## Scalability
- Scales as a unit (stateless web + scaled DB)

## Reliability
- Standard: stateless web tier, DB redundancy

## Observability
- Log at service boundary; middleware timing per layer

## Testing
- Unit test services with mocked repos; integration per layer

## Evolution Path
- Can evolve to hexagonal as domain grows complex (same shape, inverted dependencies)

## Evidence
- Classical architecture literature (VERIFIED as pattern)