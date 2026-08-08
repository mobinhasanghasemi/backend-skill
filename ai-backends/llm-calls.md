# LLM Calls in the Backend (timeouts, cache, streams, cost)

## Identity
- ID: ai-backends.llm-calls
- Type: procedure
- Status: active
- Importance: high

## Purpose
The HTTP client rules for model endpoints: don't hang, don't thrash, don't blow the budget, don't lose the stream.

## The call contract
1. **Timeout**: LLM APIs vary wildly in tail latency — client.connect=5s, read=30-60s (stream: idle per chunk); in async services: non-blocking client
2. **Retries**: LLM does error periodically (429 / 5xx / timeout) — 2-3 retries, exponential **jitter**; 429: back off more + respect Retry-After
3. **Idempotency**: some providers support request id/original — dedupe when non-idempotent (double charge risk!)
4. **Caching**: identical requests → cache **exact-response cache** (key = model,temperature,keystring hash) — massive cost/qps win; semantic cache (embeddings) for open-ended (ai/semantic-caching)
5. **Streaming**: SSE/WebSocket preferred for UX; keep token budgets; enforce max_tokens; handle client disconnect (cancel upstream!)
6. **Fallback chain**: primary model → cheaper/faster along fallback on error or timeout
7. **Metrics**: per-call: tokens, latency, cost ($), error rate, model version — into pricing summaries

## Code tiers (OpenAI-style pseudo)
### ❌ Bad
```python
completion = openai.chat.completions.create(...)   # no timeout, no retry; server down = 30s hang × N users
```

### ✅ Good
```python
client = OpenAI(timeout=(5.0, 30.0))     # connect/read timeouts
try:
    r = client.chat.completions.create(model=..., messages=..., max_tokens=1_024)
except (openai.Timeout, openai.RateLimitError) as e:
    raise RetryLater(e)                   # caller retries w/ backoff (timeouts-retries.md)
```

### ⚡ Better
```python
# retries 3 + jitter; same-input cache (response_cache GET before call)
# tokens: remember max_tokens budget per feature; stream=True + iterate chunks
# 429: exponential backoff + Retry-After honor; circuit break (distributed-systems/circuit-breaker)
```

### 🏆 Excellent
```text
# cost: token + price metrics per model; budget alerts (e.g., $/day/model)
# encrypted_providers abstraction (model registry), allowlist; per-tenant quota
# cache invalidation on model upgrade (model-version key), eval-verified cache
# test with mocked provider: deterministic; chaos: 429 storm drill → fallback chain proven
# prompt versioned (schema_templates), diff in CI (prompt governance)
```

## Failure modes
- single shared key, no quota (someone's bug costs company's account)
- unbounded prompt (context storage maybe) — truncate data, count tokens before send
- streaming client disconnect leaks cost (abort!)
- caching with temperature>0 (non-deterministic sensitive)

## Evidence
- OpenAI/Anthropic API docs (VERIFIED specifics may evolve — check), patterns community (SUPPORTED)