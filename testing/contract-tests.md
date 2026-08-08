# API Contract Tests

## Identity
- ID: testing.contract-tests
- Type: procedure
- Status: active
- Importance: high

## Purpose
Prove the API's contract (schemas, status codes, error shapes) never breaks silently — the same suite validates server AND pins clients (and feeds generated SDKs).

## Approaches (pick by ecosystem)
1. **OpenAPI-first + schema validation tests**: tests POST bodies against the spec, responses against spec → both contracts stay alive
2. **Pact-style consumer test**: client sends generated contract to server, runs provider test — for consumer-server teams
3. **Test client own client**: golden fixtures per response shape, fail CI on change

## Code pattern (pytest + DRF/Starlette)

### ❌ Bad
```python
# endpoints return shapes nobody tests: refactors silently change field name, 
# client app breaks in prod; or: contract only in docs nobody reads
```

### ✅ Good
```python
def test_todo_shape(resp):       # raw assertions on contract          ✔
    assert {k: v for k in resp["todo"]} == ["id","title","done","created"]
def test_error_contract(resp):
    assert resp.status_code == 422
    assert set(resp["errors"]) == {"field","code","message"}
```

### ⚡ Better — schema-driven
```python
import jsonschema
SPEC = load(openapi_spec)       # one true source in repo
for endpoint in SPEC: requests fixtures → resp valid per path schema (repr)
# + OpenAPI generation from Django REST (drf-spectacular) keeps spec commit-fresh
```

### 🏆 Excellent
```text
# contract for every error type (200s less, 422, 429, 409) with stable codes
# backward-compat tests: "v1 contract still passing v2 code" (versioning.md)
# CI: schema diff on PR (breaking change = human review gate)
# generated client from spec for languages used (TS/Go) — commit both
# consumer-driven: provider test against recorded consumer expectations
```

## Failure modes
- spec and code drift (fix via drf-spectacular + CI note)
- only happy paths covered (errors are contracts too)
- no one runs provider tests in CI

## Evidence
- OpenAPI tooling (drf-spectacular, fastapi) VERIFIED; consumer-driven contracts established (thought)