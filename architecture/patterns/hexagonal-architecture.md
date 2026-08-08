# Hexagonal Architecture (Ports & Adapters)

## Identity
- ID: architecture.patterns.hexagonal
- Type: pattern
- Status: active

## Purpose
Isolate the application core from external systems (DB, web, messaging) via **ports** (interfaces) and **adapters** (implementations). The app is the center; input/output both go through adapters.

## Core Concept
The application core defines ports (e.g., `OrderRepository`, `Notifier`). Adapters implement them (Postgres repo, SMTP notifier, REST controller, CLI). Swap adapters without touching core.

## Mental Model
A hub-and-spoke: the application core is the hub; via the spokes (ports), different vehicles (adapters: DB, queue, web, CLI) dock interchangeably.

## Activation Conditions
- applications integrating with many external systems (DB, payment, queue, email)
- high testability needs (swap DB to in-memory for tests)
- long-lived service with evolving infrastructure

## Do Not Activate When
- trivially small CRUD — ceremony outweighs value (Governor)
- team unfamiliar — risk of half-adapters everywhere

## Advantages
- Isolation from infra changes; excellent testability; clear input/output boundaries

## Disadvantages
- More interfaces/mapping; some duplication of models; adapter code volume

## Failure Modes
- Port interfaces morph with adapter needs (leak)
- Everything becomes a port → interface soup

## Trade-offs
- vs clean: same spirit, simpler (ports at app edges, without the formal layered circles of Clean Architecture)

## Security
- Adapters do input validation; core enforces authz; never trust adapter-provided user identity

## Performance
- Watch serialization boundary (repo DTO ↔ domain); bulk adapters for throughput

## Scalability
- Stateless core scales; adapters scale per type (stateless HTTP, queues)

## Reliability
- Swap adapters for degraded modes (fallback queue, mock payment)

## Observability
- One span per port execution; metrics on adapter latency

## Testing
- In-memory adapters; contract tests at ports

## Evolution
- From layered: add interfaces at service layer; from clean: compatible

## Evidence
- Ports & Adapters (Cockburn), DDD communities (VERIFIED concept)