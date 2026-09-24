# Redis Ops — ACL, Eviction, Threading

## Identity
- ID: caching.redis-ops
- Domain: caching
- Type: technology
- Status: active
- Importance: high
- Last Verified: 2026-08

## Purpose
Run Redis 8 as cache without becoming a SPOF or a leak: ACL, eviction, TLS, I/O threading, and failover — complement to strategies/invalidation.

## Core Concept
Redis 8 merges modules (JSON, search, time series, vector) into OSS (S-050), but cache use stays classic: in-memory LRU with tenant-isolated keys. Ops corrects the failure modes: memory blow, cross-tenant leak, cold restart stampede.

## Activation Conditions
- Any Redis as cache/session/rate-limit; S-016/S-052 relevant

## Decision Rules
- ACL: one user per service `ACL SETUSER app on >pass ~app:* +@all -@dangerous`; TLS required; `rename-command FLUSHALL ""`.
- Eviction: `maxmemory-policy allkeys-lru` with `maxmemory` 70% of instance; monitor `evicted_keys`.
- Persistence for cache: `save ""` (no RDB) + `appendonly no` — cache is rebuildable; for session: `appendonly yes`.
- I/O threading: `io-threads 4` on 4+ vCPU (S-050); benchmark p99 before enabling.

## Security
- Per-tenant key prefix `tenant:{id}:...` (ARCH025); no PII in key; DB index per tenant if using logical DBs (deprecated, prefer prefix).

## Performance
- Pipeline + connection pool (psycopg-style via S-049 for DB, redis-py pool for Redis); measure hit ratio, not just latency.

## Reliability
- Replica + Sentinel or managed failover; client uses `single-flight` on miss to avoid stampede; on failover, accept miss storm with circuit to DB replica.

## Evidence
- Redis 8 GA and ACL VERIFIED via S-016/S-050/S-052 (accessed 2026-08).

## Confidence
VERIFIED
