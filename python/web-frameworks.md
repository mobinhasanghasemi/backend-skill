# Python Web Frameworks & Servers (FastAPI/Flask + ASGI/WSGI)

## Identity
- ID: python.web-frameworks
- Type: technology
- Status: active
- Importance: high (choosing and running the web layer)

## The 2026 honest map
| Stack | Choose when |
|---|---|
| **Django (+DRF)** | full framework: admin, ORM, migrations, auth, batteries; team Django-literate (see django/ROOT) |
| **FastAPI** | pure APIs, async by design, Pydantic-in contract, OpenAPI out; event-driven services; greenfield |
| Flask/FastAPI-lite | small internal services, maximum control, no batteries needed |
| Starlette (raw) | WebSockets/middleware-heavy custom paths — need fine control |

## Async: ASGI vs WSGI reality
- uvicorn (ASGI) serves FastAPI; gunicorn+uvicorn workers for prod (or uvicorn multi-worker)
- Django 4.1+ has ASGI (async views) but ORM sync — know the trade (async-python.md)
- WSGI (gunicorn sync workers) still the Django/Flask default — scale via workers = processes, not threads

## The production serving stack
1. Dev: uvicorn --reload
2. Prod: workers = (2-4) × cores for sync; async single loop per process + load; NEVER `--reload` in prod
3. Ingress: nginx/caddy in front (TLS, static, buffering) — one reverse proxy with sane timeouts
4. Timeouts: proxy + app + DB all coordinated (reliability/deployment.md); graceful shutdown drains connections

## Code tiers — a production FastAPI service

### ❌ Bad
```python
@app.get("/items")
def items():  return db.query(...)          # sync ORM call in async route → loop block!
```

### ✅ Good
```python
@app.get("/items")
async def items(session: Annotated[AsyncSession, Depends(get_session)]):
    return await session.execute(select(Item).limit(50))   # async end-to-end
```

### ⚡ Better — boundaries clean
```python
# pydantic schemas at boundaries; service layer pure sync/async; 
# dependencies via Depends; OpenAPI auto; tests with httpx AsyncClient
```

### 🏆 Excellent
```
# structured: settings model, lifespan for pool/startup, health endpoints, 
# middleware: tracing (OTel), request id, rate limit; error handler RFC7807
# per-route async/sync declared; performance: profiling dashboard; 
# deploy: uvicorn workers managed, graceful shutdown 30s drain
```

## Failure modes
- sync work in async routes (loop stall — see async-python.md)
- thread-unsafe settings (global mutable config read after fork)
- uvicorn --workers N with shared in-memory state (sticky nothing!)
- frameworks stacked without need (Django for tiny internal = overkill)

## Evidence
- FastAPI/Django/uvicorn docs (VERIFIED); ASGI/WSGI spec