# Big-Bang Rewrite

## Identity
- Severity: HIGH

## Definition
Deciding to rewrite a legacy system entirely, in one project, with "clean architecture", instead of strangling it incrementally.

## Why it fails (the classic story)
- New system duplicates old with no real users, features drift
- Underestimated discoveries (business logic hidden in 10-year-old edge cases)
- No motivation to finish (old system keeps running)
- Team cultures blame each others' systems

## The counter-evidence
- Strangler fig (patterns/strangler-fig.md): incremental replacement preserves value; old remains until safe
- Rewrites are justified only for small tools where size is known: ≤ ~1-2K LOC, no deep couplings

## Decision rule
If system > 3-6 months of effort → strangler path:
1. Module map
2. New features into new side
3. Loud flag gateway
4. Migrate per data-slice

Costs: two-code parity, energy of double territory — but risk is rolled back per slice.

## Evidence
- Widely recorded failures (Joel Spolsky's classic; industry common) — VERIFIED