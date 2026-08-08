# Distributed Locks

## Identity
- ID: distributed-systems.distributed-locks
- Type: procedure
- Status: active
- Importance: medium (used rarely, feared correctly)

## Purpose
Mutual exclusion across processes/nodes — for the narrow cases a DB constraint or single-node queue can't solve. A distributed lock is an operational tool with sharp edges: use it only when a row lock/unique constraint/queue won't do.

## Before you lock (cheaper alternatives)
- DB unique constraint (the real fix for "two workers duplicate X")
- DB row lock `SELECT ... FOR UPDATE` (same service, same DB — no DLock needed!)
- Single-consumer queue (worker per partition)
- Optimistic concurrency (version column)

## The real requirements (Redlock-level caution)
1. **TTL/lease**: lock expires — the holder may outlive it → fencing token mandatory if writes happen
2. **Fencing token**: monotonically increasing token per acquire; the resource rejects writes with stale token
3. **Renewal**: heartbeat extends lease under long jobs (or fail)
4. **Safe acquire**: SET NX EX — atomic; never get+set separately (race)
5. **Same-key → same node**: consistent hashing/partitioning prevents split-brain storms
6. **Timeout on all client ops** — no hang on Redis outage

## Code tiers

### ❌ Bad
```python
if r.get(lock_key): sleep; # race: two workers both see free → both lock
r.set(lock_key, 1)          # no TTL, no fencing: holder crash = permanent lock
```

### ✅ Good
```python
ok = r.set(lock_key, token, nx=True, ex=30)
if not ok: retry_backoff()
try: critical_section()
finally: r.delete(lock_key)  # but only if token matches (compare-and-delete)
```

### ⚡ Better — lease + fencing
```python
token = uuid4()
while True:
    if r.set(lock_key, token, nx=True, ex=30): break
    sleep(random 0.1-0.5)
renew_thread(lock_key, token, every=10)          # heartbeat
try:
    do_write_with_fencing(token)                  # resource verifies token freshness
finally: lua_compare_and_delete(lock_key, token)  # atomically
```

### 🏆 Excellent
```text
- prefer single-node DB row lock when same DB: no TTL subtleties (rollback-safe)
- DLock layer wrapped in one module: acquire(critical(), renew, fencing) 
- metrics: lock wait time, stale-lock rate, renewal failures
- chaos test: kill a holder mid-job → verify no corruption, lock reacquired
- never lock for > seconds; if > minutes, question design (async better)
```

## Failure modes
- no TTL: holder crash → permanent lock
- TTL too short: live holder loses lock → two holders → fencing saves writes
- redis failover: lock lost → double-execution (fencing token still protects the data)
- using distributed lock to serialize DB writes that a unique constraint handles (overkill)
- unlock without token check: worker A unlocks worker B's lock

## Evidence
- Redis SET NX docs, Redlock design page incl. its critics (VERIFIED; advice: prefer fencing over belief in perfect mutex)