# API — ROOT NEURON

## Identity
- ID: api.root
- Domain: api
- Type: root
- Status: active
- Importance: critical

## Purpose
Router for interface design: style choice (REST/GraphQL/gRPC/WebSockets), contract hygiene (versioning, errors, pagination, idempotency), and API security (authN, rate limits).

## Activation
- designing/evolving an API, endpoints, contracts
- client-contract issues (versioning, breakage)
- webhooks/realtime needs
- API security review

## Do Not Activate When
- pure internal data-layer questions
- UI/frontend topics

## Routing Rules
```text
style choice       → rest.md / graphql.md / grpc.md / websockets.md
versioned change   → versioning.md
pagination/filter  → pagination.md
error shape        → error-design.md
retry/idempotency  → idempotency.md + distributed retry neuron
abuse             → rate-limiting.md (+ security.guardian)
server-to-server   → webhooks.md
realtime           → websockets.md
cache headers      → http-caching.md
```

## Mandatory Questions (before any API shape)
1. Who calls it? (public? B2B? internal? mobile?)
2. Consistency/latency budget per flow
3. Volume & patterns (read heavy? writes from many clients?)
4. Evolution needs (versioning, deprecations)
5. Compliance/security class of the data the API exposes
6. Ops: thresholds, SLO per endpoint?

## API principles (professional design, guidance not mandate)
- **Semantic verbs** (REST) and consistent resources; error contracts (Problem Details)
- **Idempotency on write endpoints** (especially payments) — idempotency.md
- **Rate limiting** on abuse-prone surfaces (auth, writes, exports)
- **Versioning** policy decided EARLY; backward compatibility respected
- Observability: every endpoint has metrics (latency/error/saturation), trace + correlation id
- **Validation**: schema-level (OpenAPI) is both contract & docs & hub

## Common Failure modes
- breaking minor versions (silent clients)
- unbounded list endpoint (no pagination) — ARCH030
- sync-retry storms (no backoff) — ARCH002
- API as god-facade over every internal resource
- errors as "500 vs 200 with error payload" soup

## Security
- See SECURITY_GUARDIAN for boundary: authN flows, authZ per object, rate limits, no sensitive leaks in errors (IDs, stack)
- Webhooks: HMAC verify (webhooks.md)

## Observability / Reliability / Testing
- contract tests (testing/contract-tests.md), backward compat tests, load tests for p95 budget

## Evidence
- REST/GraphQL/API guidelines popular & mature (VERIFIED concepts; choice is workload — context wins)