# Playbook: Webhook Failures

## Symptoms
- failed deliveries rising; dead-letter (DLQ); customer complaints of missing notifications/events

## Diagnosis
1. **Which consumers?** — delivery stats: success %, retry average, status codes (5xx? 401? 404?)
2. **Signatures**: failures 401/403 = secret mismatch or clock skew (HMAC verify — time sync!) → verify secret rotation + system time
3. **Payload errors** (400): schema drift — consumer declares v1, you ship v2 breaking; check version in payload + consumer upgrade status
4. **Timeouts/5xx**: consumer under load — exponential backoff already? max attempts? DLQ story

## Recovery ladder (webhooks.md gives the design)
- Replay: our DLQ/outbox replay endpoint → redeliver event (idempotent consumer dedupes)
- If ordered events: replay in order (event_time asc, consumer verifies monotonic)
- High burst: interdelivery pacing (deliver to consumer at tolerated rate)

## Hard cases
- **Consumer lost data**: audit: confirm event has no PII; republish from outbox snapshot (if consumer supports idempot)
- **Signature mismatch inside shared secret rotation**: 24h grace (accept old then new then old-ok) — standard rotation window
- Permanent 4xx (invalid store URL): deliver, alert, operator fixes endpoint

## Prevention
- delivery tests (success/fail/rotation), dead-letter coverage (consumer "no ack" test), metrics: delivery %, avg retry, DLQ depth; scene retrace in postmortem

## Rollback story
- redeliver comes from outboxes (event raw kept) — the queue contract does not lose