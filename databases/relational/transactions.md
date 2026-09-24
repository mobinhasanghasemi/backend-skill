# Transactions & ACID

## Identity
- ID: databases.relational.transactions
- Type: knowledge
- Status: active

## Purpose
Understand and use atomicity/consistency/isolation/durability precisely — and pick the right isolation level per workload.

## Core Concept
- **Atomicity**: all or nothing
- **Consistency**: invariants preserved
- **Isolation**: parallel transactions behave
- **Durability**: fsync'd commits survive crash
Use transactions for **multi-step invariants**, not as default for single statements.

## Mental Model
Independent unbroken snippet: readers and writers see either the before or after — never the middle.

## Isolation levels (table)
| Level | Anomaly prevented | Notes |
|---|---|---|
| Read uncommitted | (dirty read) may appear | PG maps to Read Committed |
| **Read committed** (PG default) | dirty reads | most common default |
| **Repeatable read** | non-repeatable reads | PG: consistent snapshot isolation |
| **Serializable** | serialization anomalies | PG 15+: real SSI (stricter than snapshot) |

PostgreSQL implements **snapshot isolation**: "repeatable read" shows a consistent snapshot; "serializable" adds SSI. Concurrent anomalies to design against: lost updates, read skew, write skew, phantoms.

## Decision Rules
- Financial/inventory writes: `SERIALIZABLE` where conflicts rare, else `REPEATABLE READ` + retry on 40001
- Reads that must see a consistent view → single transaction snapshot (SELECT without update is fine)
- Use PG advisory: SELECT `FOR UPDATE` explicitly before mutate-if-based decisions
- **Deadlock**: detect (log), re-run conflict (retry) — second killer
- Rows that must not be re-ordered... ensure update ordering

## Code Tiers

### ❌ Bad
```python
# check-then-act WITHOUT a transaction, or nested COMMIT per step:
balance = get_balance(user)                # read
if balance >= amount:
    insert_transfer(...)                  # two statements, not atomic
    update_balance(user, balance - amount)
```
Race conditions → double spend / lost update.

### ✅ Good — single critical section
```python
with db.transaction():
    locked = db.fetch_for_update("SELECT * FROM accounts WHERE id=%s", uid)
    #  [illustrative] real psycopg: cur.execute("SELECT ... FOR UPDATE", (uid,))
    if locked[0].balance < amount:
        raise InsufficientFunds
    db.execute("UPDATE accounts SET balance = balance - %s WHERE id=%s", amount, uid)
    db.execute("INSERT INTO transfers (...) VALUES (%s)", ...)
```
Why: `FOR UPDATE` serializes writers, all-within-commit.

### ⚡ Better — concurrency-safe with retry
```python
for attempt in range(3):
    try:
        with db.transaction(isolation="REPEATABLE READ"):
            if account.balance < amount: raise InsufficientFunds
            db.execute("UPDATE ... balance = balance - %s", ...)
            db.execute("INSERT INTO transfers (...) ...")
        break
    except SerializationError:  # 40001 in PG
        backoff_for(attempt)    # predictable conflict → retry
        continue
```

### 🏆 Excellent — money-grade
```python
for attempt in range(retries):
    try:
        with db.transaction(isolation="REPEATABLE READ", retry_on_serialization=True):
            account = get_account_for_update(user)      # FOR UPDATE
            if account.available < amount: raise InsufficientFunds
            balance.delta(account, -amount, ledger_id=tx.id)  # all in one tx
            ledger.record(tx, ...)
            outbox.publish(AccountBalanceChanged, account.id, ...)  # transactional outbox
        return tx.id
    except SerializationError as e:
        metrics.serialization_retries.inc(); sleep(backoff(attempt))
```
+ the outbox: side-effects (notifications) issued only in the SAME transaction — so they can't vanish or double.

## Version Awareness (PG 18)
- Isolation semantics stable (MVCC); `RETURNING OLD/NEW` new in 18 simplifies audit updates

## Failure Modes
- Transactions too long (lock held over HTTP wait) — connection timeouts → new deadlock
- Nested transaction misuse (commit inner too)
- Retry without `FOR UPDATE` = missed
- Sync HR call inside tx = pool block

## Security
- least-privilege users; no DDL grants to app role

## Observability
- `pg_stat_activity` wait/blocking; deadlock logs (23P)
- perf: commit throughput (fsync vs synchronous_commit options)

## Performance
- Measure first: EXPLAIN (ANALYZE, BUFFERS) for query shape; pg_stat_statements for hot queries (S-044/S-047). No index/cache without measurement per PERFORMANCE_ENGINE.
- p95/p99 before/after; one change at a time.

## Reliability
- Timeouts on DB/client, retry with jitter + idempotency, backup/PITR tested monthly (S-046), RPO/RTO defined.
- Failure: pool exhaustion -> shed load, replica lag -> read-your-writes check.

## Evidence
- PostgreSQL docs on isolation (VERIFIED)