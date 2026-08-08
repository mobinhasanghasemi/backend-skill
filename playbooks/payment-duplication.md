# Playbook: Payment Duplication / Out-of-Sync

> Money bugs are the highest severity class. Handle with the incident protocol from the first symptom.

## First suspicion — dedupe first
1. **Is it idempotency?** — same `Idempotency-Key` results changed? (api/idempotency.md)
   - key missing → replay protection absent; client retried on timeout → second charge
2. **Race**: check-then-act outside transaction (MVCC/transactions.md) or optimistic version unsupported
3. **Retries on the wire**: provider dedupe key reused / idempotency key hash collision namespaces
4. **At-least-once consumer**: events (outbox → charge/webhooks) not idempotent; false negatives on ack/loss

## Diagnosis data (money playbook)
- payment logs with request/charge id + key; provider dashboard duplicates; audit table

## Recovery
1. **Stop the bleed**: if consumer/idempotency path is broken, DISABLE (pause webhook processing + block the write path via flag) BEFORE anything else
2. **Reconcile**: fetch charge list vs DB rows per key; build the diff (double charges list, double refunds)
3. **Refund/void duplicates** via provider API (idempotent refund reference: refund != charge) — confirm with another human
4. **Fix root**: idempotency key guaranteed (idempotency.md): unique constraint + store with status; outbox; consumer dedupe

## Verification
- key_id imposed uniqueness: look at identity chaos — concurrency load test on the endpoint (simulate duplicate bursts)
- money tests suite carried into CI (idempotency + reconciliations)

## Aftermath for ADR
- when did the window open (bad progress), how many duplicate charges, how were they settled, what gate failed (idempotency tests not present?)? — the change to gates is the point.