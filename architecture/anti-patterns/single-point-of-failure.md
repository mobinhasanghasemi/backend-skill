# Single Point of Failure (SPOF)

## Identity
- Severity: CRITICAL

## Definition
One component whose failure brings down the service (DB instance, one LB, one cache node, one broker, one region).

## Design rule
For every component in the genome, ask: **what happens if this dies?** If the answer is "everything dies", you have an SPOF.

## Typical SPOFs
- single web node (behind nothing)
- single DB instance (no replica, no failover)
- single broker/node
- single region/AZ
- one external dependency without failover (payment gateway)

## So
- Lint tip: ARCH001/ARCH011,
- Load balancer with health checks
- DB replication/failover topology
- Multi-AZ
- Dependency: circuit breaker + fallback

## The cost balance
Multipliers: a second region = the better answer for the 4–5 nines, but complexity jump — REQUIRE (that's why the governor asks)

## Evidence
- SRE books; SPOF incident history (VERIFIED concept)