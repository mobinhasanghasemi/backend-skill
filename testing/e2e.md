# End-to-End & E2E Suite Management (E2E)

## Identity
- ID: testing.e2e
- Type: procedure
- Status: active
- Importance: medium-high (few, precious)

## Purpose
The crown of the pyramid: a handful of full-journey tests that prove major flows work from UI → API → DB → (workers). Expensive, flaky-prone — therefore few, synthetic-data-stable, and driven by user journeys.

## Which journeys deserve E2E
- critical selling flows: signup→pay→receive; create→publish→deliver; admin→invite
- auth boundaries: login, MFA, reset, logout
- transitions that cross processes: webhook→order→notification
Protect journey count (<10-20): E2E duplicates logic already covered at unit level.

## Engineering the stability
- **Test ordering independence** (each starts fresh state — seeded fixtures, unique names)
- **Deterministic**: fixed clocks, fixed seeds, no random sleeps — poll with timeout budgets
- **Isolate environment**: dedicated e2e env (or DB+run migrations on live), never shared
- **Retry policy**: flaky test = fix the test, not retry-run (retry only for infra blips, logged)
- **Budget**: e2e in nightly/PR-skip, or a fast "smoke subset" in merge gate

## Code pattern (Playwright/selenium-py + TestClient combo)
```python
def test_buyer_completes_purchase(test_env, browser):
    with_page_create(): sign_up(); add_to_cart(); checkout_with_card(...)
    # assert: order row exists with status=paid, webhook delivered=ok, 
    # then page shows receipt; db assertions AFTER ui flow
```
Stabilize: use 2 minimum sheets of the same app (frontend shell + direct API) for debugging.

## Failure modes
- suite that flakes → team ignores it → regressions leak
- dozens of e2e duplicating unit coverage (slow CI, wasted effort)
- tests hitting prod data (mutating customers!) — NEVER
- assertions only on UI text (defaults drift with copy)
- e2e as sole gate with 30-min runtime

## Evidence — the E2E discipline is standard industry praxis (Selenium/Playwright docs, Testing Pyramid (contrast)); keep count small