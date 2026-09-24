# Migration Strategies (evolution)

## Identity — how to change an architecture, not just "upgrade"
- ID: architecture.evolution.migration-strategies
- Type: procedure
- Status: active
- Importance: medium

## Golden rule
- Every migration must have a **rollback** before it touches production (ARCH012)

## Strategy catalogue

1. **Strangler Fig** (patterns/strangler-fig) — incremental, lowest risk, prolonged dual-run
2. **Expand/Contract** (DB migrations, schema): 
   - `add new column nullable → backfill (batches) → write new code(old) → drop old`
   - never drop a column before all writers are off it
3. **Parallel run** — run old + new, compare outputs (report/analytics)
4. **Blue-green** — dual stacks + DNS, instant rollback
5. **Canary** — small% traffic brown first
6. **Feature flags** — switch capability without deploy (reliability/deployment.md)

## Move patterns for data

- **Efficient write-twice during overlap** (dual writes with careful ordering vs outbox)
- Verified backfill jobs (paginated, idempotent, resume)
- Retention decisions: when to purge old table (dedupe risk)

## Move patterns for services

- Extract capability → module boundary in monolith (warm) → wire through internal interface
- Then (if needed) expose as separate process behind same URL; strangle.

## Common migration failure
- Migrations as "big bang" (failure)
- Schema contract violations run longer (backwards comp breaks)
- No extraction rollback
- No observability on migration progress (% done, error rate)

## Timeline policies
- Each migration: owner, window, rollbacks, criteria "done", observability (progress/error)

## Evidence
- Standard practice per hundred orgs; SRE playbook migration patterns (SUPPORTED)