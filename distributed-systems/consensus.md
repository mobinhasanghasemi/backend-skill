# Consensus (Distributed Agreement)

## Identity
- ID: distributed-systems.consensus
- Type: concept
- Status: active
- Importance: medium (rare & risky)

## Purpose
When multiple nodes must AGREE on a value/order (leader election, distributed transaction commit, coordination of failover) — consensus = the machinery behind "who is the leader".

## Facts (speak precisely)
- **No consensus = no guarantees** — async models can't guarantee exactly-once outcomes (FLP)
- **Paxos** — the theoretical core (difficult to implement correctly)
- **Raft** — both comprehensible and industrialized: leader election + log replication (etcd, Consul, TiDB IDs)
- **Paxos/Raft scope**: small group (3-5), low throughput writes (system metadata, not user data!)
- ZooKeeper = consensus-as-a-service (config, naming, leaders, locks)
- Quorum (majority) tolerates minority node failure, not "idempotent crash"

## Use-when / avoid
- USE: elect a leader, metadata consensus, config distribution, HA control plane
- AVOID: adding Raft for ordinary business data (DB replication handles most)  
  — lock/option simpler; SIMPLICITY_GOVERNOR veto unless measured need

## Safety principles applied to a leader registry
1. Quorum on write — majority ack, not last writer wins
2. Lease-time for leader (heart-beat with jitter) — fencing token for data writes (distributed-locks.md)
3. Never read quorum-less (twilight zones)

## Code tiers (pseudo — choose a library, don't implement!)
### ❌ Bad: hand-crafted "elect leader" via hostname sorting without consensus (two nodes both write!)
### ✅ Good: `etcd` lease to hold leadership: 
   election.campaign() → renew lease (TTL 5s) → critical writes
### ⚡ Better: leader + fencing token (vote id) on external writes, 
   re-elect on expiry (raft-on-etcd), metrics on leadership transitions
### 🏆 Excellent: control-plane via etcd; data-plane remains single-writer DB
   (no distributed anything in data path); failover drill monthly; fencing everywhere

## Failure modes
- leader split (both think they own → fence via monotonic token)
- consensus server down = whole plane down (HA tier design!)
- quorum loss (3-node cluster: 2 of 3 okay; split brain = quorum-less fails safe)
- confusion: "consensus" as magic fix for ordering perfectionism

## Security
- etcd: TLS + auth; write-prevent on data-path direct access (blast radius)

## Evidence
- Raft paper + Raft USENIX talk (VERIFIED, 2014+), etcd FAQ