# Semantic Caching (for LLM responses)

## Identity
- ID: ai-backends.semantic-caching
- Type: procedure
- Status: active
- Importance: medium (high when cost matters)

## Purpose
Skip identical-or-near-identical LLM prompts (embeddings similarity threshold) — the biggest cost/latency saver for AI features; requires care with correctness and tenant isolation.

## When worth it
- repeated questions (docs hopper: "why do I get this error") — great
- creative/new requests every time (unique, personalized) — not worth it
- correctness tolerance: semantic equivalence is approximate — must be justified per case

## The mechanics
1. Embed the user prompt (cheap) + store pairs {embedding, response} in vector store or exact-hash fallback
2. Similarity threshold: exact-hash (no risk) vs cosine > 0.95 (semantic catch); tune per case with manual IS-RECALL review
3. **Key = prompt + model + temperature + system instruction + parameters** (temperature>0 means variance: only deterministic cases)
4. Scope key by tenant (a customer's data in response must NEVER serve another tenant — key includes tenant!)
5. TTL: model-versioned + prompt-versioned, periodic decay (evals catch stale)
6. Reading: count cache-hit rate with the cost metric (saved $ per day)

## Code tiers
### ❌ Bad
```python
if (resp := cache.get(prompt_text)):                       # exact-hash only? misses,
return resp                                                # also: user-specific reps share cache = leak!
```

### ✅ Good
```python
embed(prompt) → sim = vector_search("llm:qcache", prompt_embed, k=1, min_sim=0.90)
if sim and sim[0].scope == tenant and not sim[0].params_differ(meta):
    return sim[0].answer            # key = (tenant, prompt-embed, params)
else: compute → cache.set(key)
```

### ⚡ Better
```python
# params in key: temperature=0 REQUIRED for cache-safety; system/tool prompts hashed
# scoped by tenant + feature + language; eviction: version bump on prompt/model
# hybrid: exact-hash fast path first, then semantic (two-layer)
```

### 🏆 Excellent
```text
# cache hit/dollar reports; A/B with and without cache (quality evals stay green)
# chaos: cache purge drill (backend collapses gracefully to full compute)
# monitoring: hit %, semantic false-positive rate (tuned guard), cache size budget
# security: never cache personal message content (opt-out per category)
```

## Failure modes
- threshold too loose (similar-prompts-give-different answers — cache wrong!)
- cache multi-tenant (leak!) or user's personal answers as public
- forget version key (model change → old responses served forever)
- caching non-deterministic asks (temperature > 0)

## Evidence
- Semantic cache implementations, Redis vector/Embedding docs (VERIFIED); correctness practice (tuned by trial)