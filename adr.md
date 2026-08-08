# ADR — Architecture Decision Records

> Append-only decision journal: every significant choice gets a record. Reference in ADRs, GENOME, and incident reports.

## Decision form (fill for each ADR)
- **ADR-xxx**: title (one sentence, outcome language)
- **Status**: proposed | accepted | superseded (ref)
- **Date**; **Owner**
- **Context** (2-8 lines: why this decision now)
- **Alternatives** (2-3 rejected, with reason each)
- **Decision** (what we chose; details as needed)
- **Consequences** (pros/cons/trade-offs) + how we notice regression (metric/test)
- **Validation loop**: measurement/acceptance criteria and its result (filled later)

## Rules
1. Every architecture change (cache, queue, services, schema, isolation) → ADR
2. Update on supersede (link the old ID); do not edit history (memory.md)
3. Decisions affecting: policy, security, money, availability — mandatory
4. Group by domain dirs for readability: `adr/` root + index (chronological table)

## Index (placeholder — add rows as decisions land)
| ADR | Title | Date | Status |
|---|---|---|---|
| (adr-001) | Example: cache strategy for catalog | 2026-08-08 | proposed |

## The journaling rhythm
- after each design/review: write or update; the ENGINE and LEARN keep ADRs in sync
- before an explosion event: "if we didn't write an ADR for that, we didn't decide"