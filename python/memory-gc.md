# Python Memory & GC

## Identity
- ID: python.memory-gc
- Type: procedure
- Status: active
- Importance: medium-high

## Purpose
Understand why a Python service's memory grows, find the leak, provably fix it, and stop worrying about GC you don't own.

## The mental model (CPython)
- Refcounting deallocates eagerly; cycles need the **generational cycle collector** (can't collect cycles of `__del__`, keeps objects alive; free-threaded 3.13 has per-thread tracking)
- `gc.collect(0)` on scale/request-end is usually WRONG (collect the wrong gen at wrong time)
- The app's RSS ≠ tracked Python memory: C extentions (numpy, libs), thread stacks, allocator arena behavior (pymalloc) — investigate with tracemalloc FIRST (Python-level) and RSS second

## Leak hunting (the only reliable order)
1. **tracemalloc**: start early (or wrapper), capture snapshot at intervals, diff top allocations — shows LINE-LEVEL leaks by file
2. gc debug: `gc.set_debug(DEBUG_LEAK)`; find uncollectable cycles (`gc.garbage`), too-many-collectors
3. Heap inspection: objgraph (`show_most_common_types`, growing types)
4. Class-level: keep global caches/listeners; `functools.lru_cache` unbounded! Django: collectible query cache grows
5. Platform level: RSS vs `sum(f.size for f in gc.get_objects()...)` — split Python vs native
6. The fix: bounded caches, del in finally, context managers, weakrefs.

## Code tiers
### ❌ Bad
```python
user_cache[id] = file.read()          # global dict never cleaned → unbounded growth
# threads: Thread.start() in loop (each 8MB stack) → RSS climb
```

### ✅ Good
```python
from functools import lru_cache
@lru_cache(maxsize=512)               # bounded! eviction ≥ steady state
# or an explicit bounded cache (ordered dict pop oldest)
```

### ⚡ Better — diagnostic
```python
import tracemalloc; tracemalloc.start(30)
# ... run one operation ...
snap = tracemalloc.take_snapshot()
top = tracemalloc.StatisticsDiff.apply(snap_a, snap).top_by('lineno')[0]
# shows the leak line — fix precisely
```

### 🏆 Excellent
```text
# memory SLO graph (RSS by pod), alert on unbounded trend (obvious leak)
# request-scoped objects: request context + GC generation check every N requests
# load test soak overnight: RSS flatline = clean; growth = leak found
# large data: generators/iterators instead of list-of-lists; numpy/preallocate
```

## Failure modes
- "GC gonna fix it" (cycles and C-ext retainers don't)
- caching with ttl but without total size bound
- memory metric from only RSS (native vs python mix)
- async task leaks holding references (cache of coroutines)

## Evidence
- Python docs (gc/tracemalloc) VERIFIED; real-world memory leak playbooks (SUPPORTED)