# CODE REVIEW CHECKLIST

Focused on the backend skill's red lines. Check every reviewed diff (or at least: security rows always).

## Safety nets
- [ ] No secrets/keys/URLs/credentials in code; imports safe
- [ ] No blind `except:`; errors logged with context (no stack-only)
- [ ] Timeouts present on synchrony (HTTP/DB/queue); no infinite loops
- [ ] No mutable defaults, shared state across requests

## Async (Python)
- [ ] Sync calls NOT in async (unless to_thread); awaited everywhere
- [ ] No unbounded concurrency (sema/gather); graceful shutdown
- [ ] Timeouts on every await that touches network

## Domain & Integrity
- [ ] AuthZ: every modified handler object-scoped (current user/tenant)
- [ ] Transactions: money-flows atomic; no read-then-write races without lock/optimism
- [ ] DB: queries use indexes for filters (EXPLAIN if new/complex)
- [ ] Pagination + limits on all list endpoints
- [ ] Errors: machine parsable (Problem+JSON) + no PII in logs

## API & Contracts
- [ ] Idempotency on writes (POST): key header enforced; replay OK
- [ ] Inputs validated at boundary (serializer/schema); unknown fields rejected
- [ ] Contract: fields stable; new = additive (versioning policy)

## Async / background
- [ ] Task idempotency key; bounded retries (maxN + backoff/file): DLQ path exists
- [ ] Outbox for transactional events; nothing enqueued after commit crash-unsafe

## Testing
- [ ] Tests added/changed for the behavior (not just smoke)
- [ ] Regression test for the bug (fails without fix, passes with)
- [ ] IDOR test if auth touched (user B cannot read A)
- [ ] No random/flat timeouts in tests (deterministic)**

## Consent
- [ ] Dead code/sudden TS; TODO without owner is a review block
- [ ] ADR updated if design decision recorded