# Cell-Based Architecture

## Identity
- ID: architecture.patterns.cell-based
- Type: pattern
- Status: active, high-complexity
- Importance: medium (apply only at scale)

## Purpose
Divide the system into independent "cells" — each a fully self-contained stack inside a geographic/availability region — so any cell can operate when others fail. The cell becomes the unit of failure isolation.

## Core Concept
Each cell ships the full slice (load balancer + API + services + DB replicas) for a partition of users/regions. Cross-cell traffic is minimized; routing picks the right cell (consistently). A cell down = some users affected in that region only, not all.

```
[Cell A: region-west]  LB+API+app+DB  ← users in west
[Cell B: region-east]  LB+API+app+DB  ← users in east
```

## Activation Conditions
- multi-region / multi-AZ requirement with strict fault-domain isolation
- tier SLO (e.g., banking, messaging reliability) where regional failure must be containable
- users segmented by geography or org (natural cell boundaries)

## Do Not Activate When
- single-region requirement (cells = pure cost, Governor fires)
- small systems where DR is achieved by backup/restore instead

## Advantages
- true failure isolation per region
- DR and compliance (data residency) become per-cell
- latency from locality
- independent scaling per cell

## Disadvantages
- cross-cell data consistency hard (no global transactions)
- routing complexity (cell-aware authN, sticky mapping of users to cell)
- data duplication / cross-cell analytics headaches
- significantly harder ops (operating N full stacks)

## Failure Modes
- cell routing bug: user lands in wrong cell → data split
- hot regional imbalance → some cells overloaded
- cross-cell feature (analytics join on users from 2 cells) — unbuilt queries

## Security
- per-cell secrets, least-privilege
- routing keys validated — user→cell mapping is security-critical
## Performance
- per-cell latency; avoid cross-region calls in hot path
## Reliability
- the point: cell isolation; per-cell failover and DR tested
## Observability
- per-cell metrics mandatory; cell health dashboards are the ops contract

## Evolution Path
- Go cell-based only after a single region genuinely can't meet SLO/DR/compliance. Evolving from monolith: boundaries first, then region 2 as a full cell.

## Evidence
- Regional/cell architectures at large orgs (e.g., HSBC cell model) — INFERRED/SUPPORTED at extreme scale; not a default pattern