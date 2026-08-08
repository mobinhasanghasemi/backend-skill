# Redis

## Identity
- ID: databases.nosql.redis
- Type: technology
- Status: active
- Importance: high
- Last Verified: 2026-08

## Purpose
Redis as: cache, session store, rate-limit counter, distributed lock, low-latency data structure server (queues/streams). Related to caching/ and distributed-locks.

## Version snapshot (2026-08)
- **8.0 GA May 2025** — Search/JSON/TimeSeries/vector modules are now **built-in** (no separate modules); licensing AGPLv3 (also RSALv2/SSPLv1 options); I/O threading; vector set (beta)
- current 8.x: 8.4.x (8.4.5), 8.6.0 released Feb 2026
- 7.x legacy (7.4 EOL approaching); always check your provider's matrix

## Core mental model
A single-threaded-per-command in-memory store (8.x introduced threaded I/O; commands still single-threaded for most) with sub-millisecond latency — for **working-set-in-RAM** data. Eviction strategies (LRU/LFU/TTL) shape it as a bounded cache; persistence (RDB snapshot / AOF) shapes it as a store (see failure modes).

## Activation
- cache layer, sessions, user quotas, rankings, locks, pub/sub, streams for small fan-out
- "we need something fast in front of DB"

## Do Not Activate When
- data must outlive memory w/o loss → other stores (remember: Redis durability has modes)
- strong transactional/relational queries → DB
- high namespace/billing logic

## Decision Rules
1. **Persistence**: choose per need — cache (no pers), sessions (AOF/ RDB?), money-critical = PostgreSQL, not Redis
2. **Eviction strategy** deliberately (allkeys-lru raises staleness; volatile-ttl…)
3. Keys have TTLs; namespaced keys; watch memory `maxmemory`
4. Cluster (sharding) when > RAM core / for throughput — plan failover & keys deltas
5. Locks: careful — see distributed-systems/distributed-locks (TTL + fencing!)
6. bg-save during load: prefers splitting WAL budget

## Failure modes (the classic trio)
- Node/OOM → keys lost → app thundering herd
- Persistence fragile across master promote (`no-eviction` collisions)
- Client retry storms on failover
- pub/sub loss on reconnection (streams for durable)

## Code Tiers — session-store evolution

### ❌ Bad
```python
r.set(f"session:{sid}", token)   # forever TTL, no namespace hygiene, no expiry
```
### ✅ Good
```python
r.setex(f"session:{sid}", 3600*24, token)   # expiry bound; TTL = logback worst case
```
### ⚡ Better — security + eviction discipline
```python
r.setex(f"sess:{uid}:{sid}", token, ex=7200)  # uid-ns, rotate sid & revoke
# periodic FULL scan isn't needed: server evicts by TTL (volatile-lru)
```
### 🏆 Excellent — production shape
```text
maxmemory-policy volatile-lru; each namespace TTL'd
AOF (everysec) OR RDB snapshots + dependent patterns (cache) vs durability
cluster for >RAN; client proxies handle slot routing; best-effort only
sessions rotated at login; rate-limit bucket atomic (INCR + EXPIRE lua)
locks with TTL+fence-token (see distributed-systems)
```
Wait — 👍 In each case the specifics (memory, policy, kind) exist per application context.

## Observability
- hits/misses (info), evicted_keys, memory/peak, latency percentile, failover events, key space advice

## Security
- TLS + AUTH / ACL roles (Redis 6+ ACL), no fallback to default
- never run on public port w/o TLS+auth

## Evidence
- Redis official docs (VERIFIED via source-S-016, accessed 2026-08); version facts from redis.io release notes