# Playbook: Stale Data / Cache-Bug

## Symptoms
- users report stale values (profile, stock, orders); dashboard mismatches; "deleted item still shows"

## Discipline ladder
1. **Iso plot**: WHERE is the staleness? (response body vs render vs exports) → find the layer: db row actual? read replicas (lag) vs cache (app) vs CDN/browser
2. **Read path**: identify entry producing stale READ (cache miss/hit key, TTL involved?)
3. **Write path**: invalidation flows: which update(s) did NOT invalidate this key? (registry in caching/invalidation — trace single step)
4. **Replicas**: read-your-write staleness (replicas lag) — tighten routing or accept documented delay

## Decisions (per found case)
| Root | Step |
|---|---|
| Cache TTL bound too long | shorten key-TTL or add event invalidation (caching/invalidation.md) |
| WRONG cache key (missing user/tenant) | fix key schema (tenant included!) |
| Update path missed invalidation | full write-path audit: all updaters of object must hit same invalidation function |
| Replication lag | for money-critical: read-your-writes rules (replicate sync for that path) |
| Cache never purged (deploy) | epoch-bump deployment step (caching/ROOT) |

## Short-term fix
- targeted purge: delete specific keys (deterministic!) vs global flush (other caches drop too) — if needing global, ok with the blast radius

## Long-term discipline
- key registry with invalidation map; integration test (write iteration → read fresh within <ML bearer); metrics vs staleness alert
- Cache correctness test in CI per critical key (write→read asserts fresh)