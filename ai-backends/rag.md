# RAG Pipeline Engineering

## Identity
- ID: ai-backends.rag
- Type: procedure
- Status: active
- Importance: high

## Purpose
Build retrieval-augmented generation that answers well within latency/cost: chunking, indexing, retrieval, rerank, and the eval loop that tells the truth.

## The pipeline (each stage affects quality — measure each)
1. **Ingest**: parse sources (markdown, PDF, DB rows) → clean → chunk
2. **Chunking**: split on semantic boundaries (headings/para); keep context overlap; sizes 300-1000 tokens typical, per use-case (retrieval quality vs fidelity); metadata per chunk (source, section, date, tenant, access scope!)
3. **Embed + index**: embedding model (must match at search!) → vector store (vector-databases.md)
4. **Retrieval**: top-k by similarity (+ keyword/hybrid BM25 fusion for recall), **metadata filters in the query** (tenant! access!) — pass filters from the request, never trust the model to invent
5. **Rerank** (optional but big win): cross-encoder rerank top-50 → top-5 — quality jump, latency cost
6. **Prompt**: system instruction + retrieved context (cite sources) + user question; context MUST respect access control
7. **Post**: answer with sources; answer-without-citation prompt; point-blank "I don't know"

## Quality gates (evals.md)
- golden question-set per domain: recall@5, answer correctness (LLM-judge/rubric)
- A/B: embedding model version, chunk size, top-k, rerank toggle — **measured**
- Latency budget: 95% under N s risk ($ streaming token shelf)

## Code tiers
### ❌ Bad
```python
# chunk by fixed 1000-char slices (cuts mid-sentence), no metadata,
# equals(...) on full doc, full-tenant pool: user B retrieves documents from tenant A!
```

### ✅ Good
```python
chunks = split_by_headings(doc)          # semantic, with headers overlap
VecStore.add(chunks, meta={"tenant": t, "source": url, "updated": iso})
# query:
hits = VecStore.search(embed(q), filters={"tenant": request.tenant}, k=8)
```

### ⚡ Better
```python
# hybrid: BM25 (keyword) ⊕ vector, rank fusion (RRF) → rerank cross-encoder → top5
# per-chunk ACL metadata; retrieval only within allowed scope (never model-provided)
# citation: hits carry source id; answer template cites `[1]..[k]`
```

### 🏆 Excellent
```text
# versioned embedder + re-embedding pipeline w/ backfill; chunk provenance crawling
# eval suite CI: recall + correctness + hallucination rate; A/B in tagging
# latency, token cost per request against SLO dashboard; cache
# security: PII in chunks redacted (embed full docs into scope), tenant isolation tested
# fallback: no-hit → model with "knowledge gap" response (no hallucination!)
```

## Failure modes
- chunking destroying semantics; huge doc embedded as 1 chunk
- filters not applied → cross-studio leak (critical)
- stale index (new data not embedded) — event pipeline
- retrieval as "find similar sentence" — no answer → model confabulates
- eval none: quality invisible

## Evidence
- RAG survey practice (2023-2026 VERIFIED concepts), LangChain/LlamaIndex pattern docs