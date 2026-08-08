# PYTHON — ROOT NEURON

## Identity
- ID: python.root
- Domain: python
- Type: root
- Status: active
- Importance: high (primary language for this skill's vertical)

## Purpose
Python backend knowledge: async vs sync, typing, data structures, GC/memory, packaging, and the ecosystem patterns that 95% of backends need (FastAPI/Django/DRF, Celery, aiohttp, httpx).

## Routing
```text
async/sync + IO    → python/async-python.md
memory/GC          → python/memory-gc.md
typing & data      → python/typing-models.md
packaging/deps     → python/packaging.md
logging            → observability/logging-recipes (python idioms)
threads/processes  → python/threads-processes.md
flask/fastapi      → python/web-frameworks.md (framework reality)
```

## Python truths (2026)
- GIL: nums OK, true parallelism via multi-process; 3.13 free-threading is experimental — treat normally sync unless real trade-offs
- Async (asyncio) wins for I/O-bound: on the order of 10k concurrent connections on one box is realistic for I/O-bound workloads; CPU-bound stays sync (or processes)
- Type hints everywhere (mypy/pyright CI) — code justifies; runtime cost decreases (3.14+ ~zero overhead temp str etc.)
- Memory: GC is reference-counting + cycle collector; objgraph/tracemalloc are healer tools
- Packaging: pyproject.toml standard; uv/poetry for lockfiles; uv is fast main
- Watch performance myths: "async always faster" false; benchmark own case

## Django/FastAPI note
- FastAPI is a strong default for new thin pure APIs; choose Django wherever the full framework pays (admin, ORM, migrations, auth, CBVs, mature ecosystem) — see django domain ROOT for the mansion. No single right answer: decide per feature set.
- DRF: serializers + viewsets batteries; understand rest_framework features (versioning, throttle, filter)

## Common failure modes
- sync blocking call inside async handler (event loop stall) — call sync in threadpool
- double migrations, signals holding heavy I/O
- lazy imports at module scope (Global state)
- mutable default args (classic!), caching mutable state
- datetime naive vs aware — store UTC always

## Security/quality ties
- pydantic/dataclass validation at boundaries (python/typing-models)
- never `eval`/`pickle` untrusted (injection vector)
- linter+formatter+type CI trio: ruff + black/prettier + mypy

## Evidence
- Language facts: VERIFIED via S-005 (versions), S-008 (packaging); asyncio claims (S-007)
