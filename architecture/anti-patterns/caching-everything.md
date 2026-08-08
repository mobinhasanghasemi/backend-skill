# Cache Everything

## Identity
- ID: architecture.anti-patterns.caching-everything
- Severity: MED

## Definition
Applying caching to every endpoint/query by default, without measuring where reads are hot.

## Its internal trap
- **Ever-chasing errors**: invalidations stream of bugs
- Stale data incidents on money paths (payments! orders!)
- Higher memory-cost infra for no actual benefit
- Complicates debugging (which version of truth did this serve?)

## Decision for cache
1. Measure: is this endpoint hot (req/s)? Is it expensive (DB time)?
2. Include: is stale acceptable (TTL bound) here?
3. Complexity available for invalidation?

Apply caching only to: (perf that earns costs).

## When caching is right (complement)
- hot showcase reads (product catalog), auth tokens/sessions, rate limit counters, templates
Use caching/strategies.md

## Evidence
- Common incidents; over-caching recognized (SUPPORTED); consistency risk teaching IS the official cache section