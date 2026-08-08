# ADR TEMPLATE

Copy this to a dated file under this project's adr/ (or the customer's)
when recording a decision. Fill all sections; keep it under 1 page.

---
# ADR-<number>: <title — verb-phrase outcome>

Status: proposed | accepted | superseded-by-ADR-<n>
Date: YYYY-MM-DD
Owner: <name>

## Context
Two to eight lines: the problem, constraints (scale, team, regulatory), why now.

## Alternatives
- <option A> — rejected because …
- <option B> — rejected because …
- (declared, honest — even the second best)

## Decision
What we chose, concretely (names, boundaries, invariants).
- invariant 1: …
- resource links: (neurons consulted)
- NOT allowed later without re-ADR: …

## Consequences
+ pros (measurable)
- cons / cost (including operational)
→ how we detect regression: (metric or test)

## Validation loop (filled after)
- criteria: <one measurable acceptance>
- result: <date + number>
---

Template notes: each row = ADR metadata. created: record learning (brain/domains).