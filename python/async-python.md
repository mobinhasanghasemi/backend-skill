# Async Python (asyncio) Done Right

## Identity
- ID: python.async-python
- Type: discipline
- Status: active
- Importance: high

## Purpose
Write concurrency through asyncio that is fast, correct, and debuggable — without falling into the classic traps (blocking the loop, unbounded tasks, sync/async spaghetti).

## When async, when sync
- **Async wins**: many concurrent I/O waits (HTTP clients, DB round-trips, WebSockets, proxies) — 1 loop, 1000s connections
- **Sync wins**: CPU-bound (unless multi-process), simple CRUD pipelines, teams unfamiliar with async (correctness > fashion — SIMPLICITY_GOVERNOR)

## The three rules that prevent 80% of bugs
1. **Never block the loop** — no `time.sleep`, no `requests.get`, no sync ORM call inside a coroutine; use `await`, or offload: `asyncio.to_thread`, `run_in_executor`, worker pools
2. **Always await** — a forgotten `await` kicks a task into the void (or worse: unawaited coroutine warning); enforce with lint (ruff `ASYNC` rules, flake8-async)
3. **Bound parallelism** — `asyncio.gather(*)` on unbounded lists eats memory; use semaphore!

```python
sem = asyncio.Semaphore(10)
async def fetch_one(u):
    async with sem:
        return await client.get(u)

results = await asyncio.gather(*(fetch_one(u) for u in urls))
```

## Scaling & correctness
- DB: async drivers (asyncpg, aiosqlite) + pool; DON'T wrap sync pool (deadlock on high concurrency)
- Timeouts everywhere (`asyncio.wait_for`, per-client timeouts) — a hung await = stuck unit of work
- Task management: keep reference, `task.cancel()` on error, `gather(return_exceptions=True)` to contain
- Cancellation: understand `CancelledError` (BaseException in 3.8+); scope resource cleanup in `finally`
- Backpressure: bounded queues for producers (Queue(maxsize=...) raises when full) — never unbounded

## Code tiers

### ❌ Bad
```python
async def handle(ws):
    data = requests.get(url).json()      # blocks the whole loop for all users!
    rows = list(UserModel.objects.all()) # sync DB call blocking loop
```
### ✅ Good
```python
async def handle(ws):
    data = await asyncio.to_thread(requests.get, url)   # or httpx async client
    async with httpx.AsyncClient() as c: return (await c.get(url)).json()
```
### ⚡ Better
```python
# async driver end-to-end (asyncpg), bounded semaphore fan-out,
# timeouts per call (wait_for), error isolation via return_exceptions
```
### 🏆 Excellent
```
# structured: background task registry with health, graceful shutdown (cancel all),
# observability: async context (trace_id), gauges for pending tasks + semaphore waiters
# stress test: 1000 concurrent sockets, memory stable, loop blocked 0%
```

## Failure modes
- event loop blocked (the whale in the wading pool)
- unbounded concurrency (gather without semaphore)
- mixed sync/async Django (ORM inside async view) — documented per-case
- forgetting `await` (silent), no timeout (hangs)
- coroutine created but not awaited (leak of the object)

## Evidence
- asyncio docs + tutorial (VERIFIED semantics), uvloop discussions (benchmarked)