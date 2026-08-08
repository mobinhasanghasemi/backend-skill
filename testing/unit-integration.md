# Unit & Integration Testing Guide

## Identity
- ID: testing.unit-integration
- Type: procedure
- Status: active
- Importance: critical

## Purpose
Fast, stable tests that prove the code does what it says — and that catch regressions before users do. (Two halves: micro unit, macro integration — here together as the everyday net.)

## Unit (in-process, 1-100ms)
- One function/class per test; dependencies mocked/faked
- Test the CONTRACT, not the implementation (rename a private field — tests stay green)
- Arrange-Act-Assert with reader-friendly naming: `test_invoice_totals_disable_vat`
- Grouped by behavior, not by file/random

```python
class TestRefundPolicy:
    def test_full_refund_after_14_days(self): ...
    def test_partial_refund_after_30_days(self): ...
    def test_no_refund_after_90_days(self): ...
```

## Integration tests (process-level, 10ms-1s)
- Test your app's MIXED parts: view+DB, repository+DB, external API (local stub)
- In-memory/fake vs real test DB (read your test plans honestly: fast fake = false security)
- Seed data explicitly; each test isolated (clear tables or transactional rollback)
- DB PostgreSQL: use a test-unique schema (Django: `conftest` fixture with transaction=True)

```python
def test_creating_order_writes_row(client, db):
    resp = client.post("/api/orders", json={...}, headers={AUTH: token})
    assert resp.status_code == 201
    assert Order.objects.filter(user=me, status="pending").exists()
```

## The two golden rules
1. **A failing test must know the bug** (assert on real outcomes — breach a domain error, not "no error occurred")
2. **Never trust a test you've never seen red** — run it broken once, verify it fails

## Test doubles — honest table
| Double | Use | Don't |
|---|---|---|
| Fake (real impl in-memory) | repository/queue | logic make them slower |
|Stub (fixed responses) | external API shape | masking logic |
| Mock (records calls) | verifying interaction | over-use (behavioral churn) |
| Spy | counting | same as critical |

## Failure modes
- mocks asserting implementation detail — refactor breaks tests
- tests that pass by accident (assert True with no outcome)
- missing rollback/isolation → cross-test pollution
- slow suite (ms->min snowball) — nobody runs it

## Evidence
- pytest/Django TestCase docs (VERIFIED); Kent Beck/TDD practice (VERIFIED)