# MongoDB

## Identity
- ID: databases.nosql.mongodb
- Type: technology
- Status: active
- Importance: medium

## Purpose
Document-oriented store when documents ARE the object of storage: flexible schemas, nested data, keyed reads by document, geo. Choose honestly.

## Fresh awareness (2026)
- MongoDB 8.x current; details like versioning: check mongodb.com/docs (Last Verified: 2026-08 — treat exact minors as amber)
- Drivers; replica sets; sharded clusters

## Mental model
A filing cabinet of self-contained folders (documents) with their own structure; queries reach into fields; joins require $lookup (client-side escalation)

## Activation
- nested/document data as the domain shape
- rapid schema evolution w/o migration org
- app-local lookup by primary key; geo search
- document store pattern (product catalog, profile, config)

## Do Not Activate When
- transactional money flows (multi-doc ACID is **limited/at-your-risk** — MongoDB transactions exist since 4.0 but cost/scope)
- join-rich reporting / relationship graphs
- strong cross-collection invariants
- audit/row-level queries may outlive need

## Decision rules
1. Data model as documents-first; clearly separated read patterns
2. **Design schema for access patterns** (embed vs reference when hot)
3. Transactions exist — but multi-doc tx limited scope: know cost
4. Sharding only when insert/throughput outgrows replica set (plan zone/key)
5. Avoid $lookup-dependent hot paths
6. Global write concerns (ack) vs perf — choose by durability need

## Failure modes
- compounding $lookup chains (DB-bound client memory)
- denormalized drift (embedded vs referenced interplay)
- index fragmentation / hot index grows
- ops: autosplit, network partitions; replica set elections

## Security
-auth + TLS, least-privilege roles per app, no admin from app; field-level encryption available (enterprise)

## Perf/Obs/Reli
- indexEXPLAIN; metrics (opcounters, connections, cache)
- backups via managed (Atlas) / mongodump-per-restore tested

## Tiers

### ❌ This data is transactional ✓(catch)
```
products document nested → price floating; concurrent orders mutating doc → lost update
```
### ✅ Good Mine
```json
{ "_id": ObjectId, "sku": "A-1", "title": "...", "price": 12, "stock": { "warehouse_a":3 } }
```
indexes: sku unique, category; size
Wait– if you need price consistency + inventory: THAT's the signal relational was better.

### Citations decision
Use MongoDB where document-centric access is the pattern; the moment cross-doc invariants matter → PG JSONB/relational model.

## Evidence
MongoDB docs (VERIFIED basics); transactional capabilities (SUPPORTED w/ cost notes)