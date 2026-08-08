# Playbook: Queue Backlog / Worker Saturation

## Symptoms
- queue lag alert, freshness exceeding SLO; consumer CPU/memory pegged; message age growth

## The flow reflex
1. **Read the lags** per queue (age of oldest message vs lag count) — which queue, which worker pool
2. **Worker health**: are they running? crashes? (restart storms); tasks throwing immediately = poison queue (retries loop!) → DLQ check
3. **For poison message**: find via failed task log → task_id → payload (DLQ isolation: move/cancel, reprocess boundary-episode fix)
4. **Capacity**: steady backlog > workers can drain → add consumers/tune concurrency (bounded); if temporary spike, let backlog drain (with alert); if structural, re-architect (batch, dedupe, cheaper steps)

## Classic culprits (and fixes)
- **Dependency down** (external API): task retries entire storm → circuit/task-level backoff (celery.md); DLQ after retries
- **Slow task CPU**: optimize/pipeline; concurrency raised beyond host (thrash) — right-size
- **Unbounded job images** (each task long): chunk jobs + idempotency
- **Thundering herd on restart**: worker drain-wait strategy; queue backpressure (bounded)
- **Ordering/lag**: messages per entity in a single partition if order needed

## Mitigation ladder
1. stop producer additions (IF burst) — or expand pool
2. drain in batches with visibility (partial, no replay-reate)
3. monitor: lag → alert → task/MSR. Post: kill wasteful tasks; job ~forever > retriable chunks

## Verification
- lag → 0 approach; backlog drained; no duplicates (idempotence intact); measure before/after capacity

## Prevention
- queue common stress tests (poison, mass submit, replay); alert: lag 15m; worker health metric