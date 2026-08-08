# Playbook: Memory Leak / RSS Growth

> Symptoms: memory graph climbs over time, pod restarts (OOM), latency degrade

## Triage ladder
1. **Is it Python-owned?** — `tracemalloc` snapshot diff (python/memory-gc.md) on a running pod (no restart!) vs `gc.get_objects()` counts
2. **Segregate** python vs native: `/proc/<pid>/smaps`, `py-spy dump`, `lsof` — large native = deps (numpy/deep libs), thread stacks
3. **Binding suspects**: global/lru_cache with unbounded max; caches; sessions; connection pools not closed (leaky stacks); background task queue (list grows)
4. **GC pressure**: slow growth of "pending" + many full collections — cycle leak (gc.set_debug)

## Once located (typical fixes)
- lru_cache(maxsize=) + eviction stats; request-scope rather than global
- close clients in `finally` / context manager; pool lifecycle correct
- batch jobs: drain streams (`iterator()` chunk), release in loop
- offload heavy C-allocators (read `allocation` via profiler) — or at least document native-heavy deps

## Verification hairline
- soak run overnight: RSS flatline ±5%
- memory assertions in CI (peak bound for the job); guard alarm (warning +30%)

## The white flame
- Avoid "GC will fix it" — verify with trace; commit the ADR (evidence numbers)