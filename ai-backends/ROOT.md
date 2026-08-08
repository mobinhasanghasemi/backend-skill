# AI BACKENDS & RAG — ROOT NEURON

## Identity
- ID: ai-backends.root
- Domain: ai-backends
- Type: root
- Status: active
- Importance: high (the 2026 backend frontier)

## Purpose
Production AI features on the backend: RAG pipelines, LLM calls, agent tool-use, evals, costs — engineered like any other distributed system, with extra attack surface (prompt injection).

## Activation
- building features calling LLM APIs (openai/anthropic/self-hosted), embeddings, RAG, agents
- "should we add AI here", latency/cost of model calls, caching

## Routing
```text
RAG pipeline            → rag.md (ingest, retrieval, rerank, eval)
language model calls    → llm-calls.md (retries, timeouts, streaming, cost)
agents/tools            → agents.md (tool schema, sandboxing)
evaluation              → evals.md (the RAG/LLM loop)
semantic cache          → semantic-caching.md (or caching/ROOT)
vector store            → databases/nosql/vector-databases.md
```

## AI-backend truths (2026)
1. **LLM calls are slow, flaky, costly, and non-deterministic** — design defensively: timeouts, retries, fallbacks, caching of responses
2. **RAG quality is engineering**: chunking, retrieval, metadata filtering, rerank — not "model magic"
3. **Latency + cost**: token TTL, prompt length, batching, model tiering (fast cheap for casual, powerful for critical) — measure per feature
4. **Prompt injection is a security class**: untrusted content in the prompt can hijack the model — sandbox every model input/output (do not pass raw user/DB text to tools blindly!)
5. **Evals are the tests**: golden dataset + rubric for LLM quality — CI comparable
6. **Streaming** (SSE/WebSockets) is the default UX for long answers — backend chore: outbox, tokens, cancellation
7. Providers: OpenAI, Anthropic stable; self-hosted (vLLM etc.) for data residency/control — measure cost per request

## Do Not Activate
- pure classical backend (no AI involved)

## Common failure modes
- LLM call in hot request path (latency budget blowup) — async + cache
- prompt injection via user/attacker-controlled content; tool access opened to the model
- evals missing → regressions invisible (no metrics)
- cost surprises (no attempt/response size limits, no budget cap)
- vector store as secondary memory of product truth (recall + security)

## Security/Reliability ties
- SECURITY_GUARDIAN on any prompt + tool surface; RELIABILITY for LLM (cache/fallback/circuit)
- observability: per-call tokens, cost, latency, model version

## Evidence
- RAG/LLM engineering practice 2025-2026 (VERIFIED concepts — treat model/API details as amber per provider docs)