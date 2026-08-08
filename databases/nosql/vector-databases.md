# Vector Databases & Semantic Search

## Identity
- ID: databases.nosql.vector-databases
- Type: technology-special
- Status: active
- IMPORTANCE: high (AI era)
- Last Verified: 2026-08

## Purpose
Store and index high-dimensional embeddings for **similarity search** — the retrieval machinery under RAG and recommendation systems. Not a system-of-record for business data.

## Core concept
Embeddings (float vectors, e.g., 768–4096 dims) + index for approximate nearest neighbor (ANN: HNSW, IVF) + filters. Engines: pgvector (PostgreSQL extension!), Redis (vector set beta / search), Elasticsearch dense vectors, Qdrant/Weaviate/Milvus, FAISS (library, not service). pgvector is often the pragmatic first choice (keeps one DB), graduating to dedicated engines at scale.

## Activation
- AI retrieval, RAG, semantic search, dedup, recommendations by embedding
- hybrid (vector + keyword) search

## Do Not Activate When
- exact-match or keyword-only search without embeddings
- relational data whose queries are exact SQL

## Decisions (2026)
- **Start with pgvector in the existing PostgreSQL** (single infra, transaction-safe with other data, filters join): perfect for many MVPs
- Dedicated vector DB when: huge corpora (>100M vectors), heavy workload, need HNSW tuning isolation, complex metadata filtering at scale — migrate when measured
- **Cost**: ANN is approximate; exactness needs brute-force (kNN) — define recall expectations
- Indexing strategy affects writes: HNSW build/memory; IVFLAT coarse-to-fine
- Hybrid search (BM25 keyword + vector) is the production favorite for quality (reciprocal rank fusion)
- RAG quality relies on chunking + metadata filtering accuracy, not just the DB

## Tiers

### ❌ naive
```python
# brute-force all pairs in Python per query → O(N) => not scalable
```

### ✅ Good
```sql
-- pgvector
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops);
SELECT content FROM docs
ORDER BY embedding <=> $1 LIMIT 10;   -- cosine distance
```

### ⚡ Better
```text
- filtered search: dataset_id AND/OR tenant_id in query → partial index on filter, 
  "hybrid" with BM25 rank fusion
- async embeddings pipeline (queue) with idempotent re-embed
```

### 🏆 Excellent
```text
- versioned embedder (model version in metadata); re-embedding jobs with backfill checkpoints
- evaluation: golden query set + recall@k measured at pipeline CI
- dedicated engine when measured (p99 QPS, corpus size))
- observability: index build status, QPS, recall drift monitor
```

## Security
- embeddings can leak content — avoid embedding PII w/o policy; access control at query layer (tenant filter mandatory badge)

## Failure modes
- wrong metric (cosine vs dot vs L2) → recall waste
- unfiltered similarity leaking cross-tenant data (ARCH014!)
- model drift: old embeddings + new model mixing
- HNSW memory blowup on big corpus (measured recall vs memory)

## Evidence
- pgvector docs, Redis 8 vector set beta docs, Elastic/vector research (VERIFIED existence; choices are measurement-driven)