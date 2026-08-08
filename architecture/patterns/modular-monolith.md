# Modular Monolith

## Identity
- ID: architecture.patterns.modular-monolith
- Type: pattern
- Status: active, RECOMMENDED DEFAULT
- Importance: critical

## Purpose
One deployment unit, internally structured as clear modules with explicit boundaries and ownership.

## Core Concept
A single application process. Modules have their own models/schemas, communicate via **internal interfaces** (services/facades), never reach into each other's internals. The DB is shared but modules own their tables.

## Mental Model
One building, many offices with locked doors. You need a pass (module API) to enter — not just a key to the whole floor.

## Activation Conditions
- any new product that doesn't yet prove need for multiple deployable units
- a growing monolith that's becoming a boulder
- team growing beyond 1-2 squads within one codebase

## Do Not Activate When
- actual independent scaling/deployment of components is a measured requirement
- multiple teams with separate release trains and hard isolation needs
- compliance isolation mandates separate processes (rare, check)

## Structure
```
app/
  module_a/ (models, services, views, tests — self-contained)
  module_b/
  kernel/ (shared auth, config, base)
```
Interfaces: Python module imports → allowed; direct DB cross-module table access → forbidden.

## Advantages
- Simpler ops (one deploy), faster iteration, shared transaction/consistency (ACID inside the monolith!)
- Lower network risk (no distributed calls)
- Easier refactor: boundaries exist, ready to extract

## Disadvantages
- Single deploy unit = single blast radius for deploy (mitigate: canary/blue-green)
- Team conflicts if boundaries not enforced (Conway applies)
- DB shared — schema coupling can creep

## Failure Modes
- Boundary erosion → becomes boulder monolith
- Implicit DB coupling (module B reads module A's table) → hidden dependencies
- Deploy coupling: one module's change blocks all

## Trade-offs
- vs microservices: +simplicity, +consistency, −independent scale/deploy
- vs boulder monolith: +maintainability, −some upfront discipline

## Security
- Shared process = shared secrets/token scope; enforce module authz internally
- Future split → plan authz boundaries now (avoid god DB)

## Performance
- No network hops between modules (fast); watch for cross-module queries; index per module schema

## Scalability
- Scale by replicating whole unit (stateless modules); DB remains the limit (then replicas/split)

## Reliability
- Single unit → single failure domain per replica; DB is shared — replica/backup strategy central

## Observability
- Log module name in logs; trace per-module spans; module-level metrics

## Testing
- Module-level integration tests with internal interface contracts; contract-test the interfaces

## Evolution Path
- Add module boundaries → extract hottest module to a service when *measured* need (strangler-fig)

## Version Awareness
- Framework-agnostic. In Django: Django apps as modules.

## Evidence
- Widely used in production; common recommendation for products without per-component scale needs (VERIFIED pattern guidance; design-choice level).

## AI Instructions
- Default recommendation for most products. Only leave it with a measured reason.