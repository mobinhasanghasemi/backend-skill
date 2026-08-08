# MVCC — Multi-Version Concurrency Control

## Identity
- ID: databases.postgresql.mvcc
- Type: mechanism
- Status: active

## Purpose
Understand how PostgreSQL achieves concurrent access without reader/writer blocking — and the consequences (bloat, vacuum, stale reads).

## Core Concept
Each update creates a **new row version** (tuple); old versions stay until obsolete. Readers see a consistent **snapshot** of committed state (their xmin horizon). Writers don't block readers; writers serialize via row locks when they contend.

## Mental Model
An editing history: every change writes a new page in the manuscript; readers see the version that was current at the moment they opened it (snapshot). Old pages are weeded out later by an archivist (vacuum).

## What MVCC buys
- readers never block writers, writers never block readers
- snapshot isolation semantics (repeatable reads within a tx)
- consistent historical view for long reports

## What MVCC costs (the real trade-offs)
- **dead tuples** → table bloat → vacuum needed (see vacuum.md)
- `UPDATE` = insert + delete → index write amplification
- HOT (Heap-Only Tuple) helps when indexes unchanged
- snapshots in old `idle in transaction` blocks → vacuum can't clean → bloat trap

## Isolation mapping (PG)
| SQL level | PG behavior |
|---|---|
| READ COMMITTED | new snapshot per statement |
| REPEATABLE READ | one snapshot for the whole tx |
| SERIALIZABLE | SSI (serializable snapshot isolation) — detects serialization anomalies, retry 40001 |

## Code Tiers — the concurrency pattern levels

### ❌ Bad — check-then-act, relying on "reads see latest"
```python
balance = SELECT balance FROM accounts WHERE id=1   # snapshot A
if balance >= 100:
    UPDATE accounts SET balance = balance - 100 ... # snapshot B (later)
```
Two readers both see 100 → both write 0 → lost update.

### ✅ Good — lock the row in the same tx (PG)
```python
with tx:
    row = SELECT ... FROM accounts WHERE id=1 FOR UPDATE
    # FOR UPDATE locks the current version; writer serializes here
    if row.balance >= 100: UPDATE ...
```

### ⚡ Better — optimistic with version column (no lock held long)
```sql
-- retry loop in app
UPDATE accounts SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = :expected;
-- 0 rows → someone else won → re-read, retry (bounded)
```

### 🏆 Excellent — choose per workload
- high-conflict money rows → `SELECT FOR UPDATE` (short txs, measured)
- low-conflict, read-heavy → optimistic version column
- report-level consistency → REPEATABLE READ snapshot; ALWAYS short transactions; watch idle-in-transaction (vacuum starvation)
- serialize on hot single row: advisory lock or row lock (never re-check later)

## Failure Modes
- long tx holding snapshot → bloat + vacuum starvation
- update-heavy tables w/o HOT → index bloat
- idling transactions keeping old versions alive

## Observability
- `pg_stat_user_tables.n_dead_tup`, `last_vacuum/autovacuum`, idle-in-transaction count, bloat query

## Evidence
- PostgreSQL MVCC docs (VERIFIED); vacuum behavior stable across 15-18