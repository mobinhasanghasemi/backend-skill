# Python Threads & Processes

## Identity
- ID: python.threads-processes
- Type: discipline
- Status: active
- Importance: medium

## Purpose
Choose the right parallelism: threads (I/O overlap, GIL-bound for CPU), processes (true parallelism), executors (offload sync work) — with lifecycle, pools, and state sharing done safely.

## Decision table (honest)
| Need | Tool |
|---|---|
| Many concurrent I/O waits | asyncio (async-python.md) or threads |
| CPU-bound on many cores | multiprocessing / ProcessPoolExecutor / subprocess |
| Offload blocking libs from async loop | asyncio.to_thread / run_in_executor |
| Shared mutable state | Avoid; DB/queue/cache as boundary; lock + queue only when needed |
| Isolated heavy jobs | separate worker (Celery) — never in-process |

## The rules that prevent the classic deadlocks
1. **GIL reality**: threads don't speed CPU work (1 thread per core for CPU in Python); use processes for CPU
2. **Pool lifecycle**: ThreadPoolExecutor as context manager, or explicit shutdown — leaked pools = thread leak
3. **Never `thread.start()` bare in loops** — bounded pools; tasks that fail inside must be checked (`future.result()` or `add_done_callback`)
4. **Cross-thread state**: queue.Queue for messaging; `threading.Lock` around critical sections — but prefer immutables
5. **Processes**: only pickle-able args, proper entry (`if __name__ == "__main__"`), no global shared memory confusion

## Code tiers
### ❌ Bad
```python
while jobs: threading.Thread(target=work, args=(jobs.pop(),)).start()  # unbounded,
# failure invisible, join never awaited, GIL thrash, no pool
```
### ✅ Good
```python
with ThreadPoolExecutor(max_workers=16) as pool:      # bounded, joined on exit
    futures = [pool.submit(work, j) for j in jobs]
    for f in as_completed(futures): handle_result(f.result())  # exceptions surface
```
### ⚡ Better
```python
# process pool for CPU-bound chunks with chunking (results map), 
# queue-based dispatch (thread-safe), timeouts on get()
# metrics: pool size, active workers, queue depth; error routing to DLQ
```
### 🏆 Excellent
```
# workload shaped: async for I/O fan-out, process/workers for CPU, 
# rate limiting per pool, observability (latency/throughput per pool),
# graceful shutdown: drain queue, cancel pending, join with timeout, escalate
```

## Failure modes
- CPU work in threads (GIL thrash — often slower than serial)
- pool exhaustion from nested submissions (deadlock pattern)
- unbounded thread creation (memory + scheduler thrash)
- shared mutable list between threads (race → corruption)
- forgotten futures (exceptions silently eaten)

## Evidence
- Python concurrency docs (VERIFIED), concurrent.futures semantics