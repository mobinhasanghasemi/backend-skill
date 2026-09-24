# God Database

## Identity
- Type: anti-pattern
- Status: active
- Importance: medium
- ID: architecture.anti-patterns.god-database
- Severity: HIGH

## Definition
One monolithic shared database (or schema) that every service/team reads and writes through — the real integration point that survives decomposition.

## Signal
- A schema with tables from N teams
- DBAs gate every change; teams coordinate migrations
- one outage = all-failure blast

## Why it's a problem
- Coupling: any schema change touches everyone
- Scale: one write hotspot
- Security: cross-team privileges bloat
- Team autonomy: 0 (Conway violation)

## When it's acceptable
- small organization (1-2 teams), monolith (one team truly owns schema). "The database is only a god if no one owns it."

## Fix paths
- **Modular monolith**: keep one process, but per-module schemas/tables (module owns its tables)
- **Microservices**: per-service stores (data ownership)
- If kept: at least clear ownership boundaries + ACLs + per-team migration CI

## Detection
- 0 shared-domain tables; ownership unclear
- privileges granted globally

## Evidence
- Common production observation; Fowler/industry analysis (SUPPORTED)