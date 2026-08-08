# TESTING — ROOT NEURON

## Identity
- ID: testing.root
- Domain: testing
- Type: root
- Status: active
- Importance: critical

## Purpose
Tests = executable evidence. They make change safe: refactors, migrations, deploys, permissions. Test choice must match risk: value per test-layer balance, not blanket coverage heroics.

## Activation
- writing tests, deciding what to test, when to TDD
- CI additions; bug reproduction
- coverage debates (coverage is a hint, not a goal!)

## Routing
```text
fast, many, in-process  → unit-integration.md
services collaborate    → unit-integration.md
API contract            → contract-tests.md
a user journey          → e2e.md
performance budget      → load-performance.md
attack suites           → security-testing.md
generative/scope        → unit-integration.md (factories/property)
```

## The pyramid truth
```
   e2e (few, slow, expensive)
  integration (some, medium)
 unit (many, ms-fast)
```
Trade: faster feedback at the bottom; higher fidelity at the top. Your prize: **fast safety net** — a unit test every microsecond, integration on boundaries, e2e on the crown (critical flows only).

## Coverage is evidence, not the goal
- 100% is meaningless when fragments test mocks of mocks
- assert real behavior: result values + states + side effects; test the wrong thing and green suite = false confidence
- Mutation-testing grade (mutmut) tells you if tests actually assert (advanced)
- mutation-tested: keep tests honest — break a line, see the suite cry

## How to test-train (From any legacy)
1. Bug → write regression test FIRST for the fix
2. Add per critical path: authZ (IDOR suite!), payment, migration
3. Test the seams, not the internals
4. Slow tests to CI nightlies, fast in push loop

## Failure modes (harsh truths)
- e2e religious volume while unit vig-suite absent (flaky suite you distrust)
- rewrite-then-refactor (tests dead)
- tests of implementation (mock everything → tests break on refactor)
- flaky suite disabled, chaos later
- coverage trophy hunting

## Security ties
- IDOR/authz tests non-negotiable per endpoint (security/authorization.md)
- tests against the PLAN (security), not just the happy path

## Evidence
- Test strategy (pyramid, layers): SUPPORTED practice
