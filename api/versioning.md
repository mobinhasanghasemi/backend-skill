# API Versioning

## Identity
- ID: api.versioning
- Type: procedure
- Status: active
- Importance: high

## Purpose
Let APIs evolve without breaking clients: policy BEFORE traffic, mechanism-simple, escape hatches explicit.

## Mechanisms (compare)
| Approach | Pros | Cons |
|---|---|---|
| **URL path** `/v1`, `/v2` | visible, simple, cache/web bug survives | URL debt, infinite versions col |
| Accept header / content-version | clean URI | hidden, clients misconfiguring |
| Query param `?v=2` | quick | cache keys pollution, undocumented |
| Semantic version commit messages | simplest | no server enforcement |

## Decision rules (help the AI, not dictate)
- **URL path is the default for most teams** (visibility beats neatness)
- Prefer document+encouragement: doc contract + `Deprecation` headers + sunset date strategy
- **contract work: additive changes inside a version** (add fields, not change meaning)
- Breaking changes → new major; keep old up to N months (deprecation policy!) — decide with business
- Problem: unknown headers — plan B

## Code tiers

### ❌ Bad
```python
# silently changed field semantics; clients break
# /users returns {"name":...} then {"full_name":...}
```

### ✅ Good — heard URL version
```python
path("api/v1/orders", include(...))
# new behavior → api/v2/orders; v1 kept (timeboxed)
```

### ⚡ Better — headers + sunset
```python
response.headers["Sunset"] = "2027-06-01T00:00:00Z"
response.headers["Deprecation"] = "true; date=milestone"
# client sees, logs, tests fail after date
```

### 🏆 Excellent
```text
- version SELECTED by requirement (who calls, how often can we break clients)
- OpenAPI: each version has its own spec; contract tests pinned per version
- docs: migration guide + diffs published
- deprecation dashboard: traffic per version (metrics) — retire old majors when traffic ~ 0
- proactive: evolve inside the JSON contract first (add optional fields)
```

## Failure modes
- version per subs substantially → implementation/graph town
- never-removing old versions → surface drift
- breaking silently during "minor event"
- too many version numbers (every tweak)

## Observability
- gauge last-used per version; monitor migration; alert on <1 old calls

## Evidence
- Industry consensus URL-path-first (SUPPORTED-STRONG); O'Reilly/BFS guidance consistent