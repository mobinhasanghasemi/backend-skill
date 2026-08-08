# Strangler Fig Pattern

## Identity
- **ID**: architecture.patterns.strangler-fig
- Type: pattern/migration
- Status: active — high value for legacy

## Purpose
Gradually replace legacy system piece-by-piece by routing new traffic to the new system around the old one — cutting it piece by piece ("strangling").

## Concept
- Front → route to (new) or (legacy) based on feature path
- Old system stays until full replacement; then decommission
- Data migrated function-by-function with mapping

## Mental Model
A strangler fig vine grows around an existing tree and replaces it slowly — no instant big bang.

## Activation Conditions
- legacy monolith migration (GC → microservices, but usually to modular)
- evolution of architecture; risk of rewriting whole thing

## Do Not Activate When
- full rewrite is validated cheaper (small system, budget, brand) — big-bang rewrites are risky episodes; Governor vetoes them without measured justification.

## Advantages
- keep running legacy; incremental value; risk low (rollback per segment); confidence boost

## Disadvantages
- dual-run cost (both systems); temporary complexity routing; data sync across systems

## Method
1. Identify seams (bounded modules, entry points)
2. Route new requests through new impls incrementally
3. Feature-flag / gateway to switch
4. Migrate data per segment (ETL + dual write carefully)
5. Decommission legacy when done (last-mile cleanup)

## Failure Modes
- synchronized data drift (ETL behind)
- half-migrated business logic duplicated = divergent
- long-running zombie (never finish)

## Security
- Old/new both auth; flag-based switching edges

## Observability Considerations
- per-path split metrics (legacy vs new) — critical to prove no regression long-term

## Evidence
- Fowler strangler fig; industry practice VERIFIED