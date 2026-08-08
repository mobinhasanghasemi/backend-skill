# ARCHITECTURE PATTERNS — ROOT NEURON

## Identity
- ID: architecture.patterns
- Domain: architecture
- Type: root
- Importance: critical

## Routing table (which pattern for which situation)

| Situational need | Pattern to consult (1st) |
|---|---|
| enterprise/standard | layered |
| long-term DDD/project | clean | hexagonal |
| service splitting with data | modular-monolith then microservices |
| many teams, need to decouple at scale | microservices |
| async / event-heavy | event-driven |
| read/write asymmetry | cqrs |
| need full audit history | event-sourcing |
| bursty / scratch workloads | serverless |
| many teams on one big codebase | modular-monolith (2nd: microservices) |
| existing system → go to new | strangler-fig |
| multiple native/mobile apps | bff |
| multi-region hard isolation | cell-based |
| SaaS for multiple customers | multi-tenant |
| linear pipeline transformation | pipe-and-filter |
| legacy enterprise contract integration | soa |

## Mandatory questions for ANY pattern choice

1. What concrete requirement fails if we DON'T use this pattern?
2. What operational cost does this pattern introduce?
3. What is the migration path out of this pattern? (every pattern needs an exit)
4. Who maintains the glue?

## Common failure modes of pattern misuse
- pattern chosen from fashion not requirement (No Tech Hype)
- pattern adds complexity without paying for a broken requirement (Gov)
- exit path unexplored → locked in

## Evidence
Patterns → pattern literature (GoF-style), actively used; verify each choice against requirement.