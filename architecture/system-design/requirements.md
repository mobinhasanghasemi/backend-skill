# Requirements as a design input

## Identity / Purpose
Convert the user's need into a bounds declaration the architecture can test.

## Categories

| Class | Examples | Effect on design |
|---|---|---|
| Functional | create order, remind, quota | modules, APIs |
| Performance | p95 < 200ms; 10k req/s | caching, async, pools |
| Availability | 99.9%, RPO(≤5m), RTO≤15m | replicas, backups, DR |
| Scalability | 10x in 6mo | headroom, decoupling |
| Security | PCI, GDPR, secrets | SECURITY_GUARDIAN gate |
| Operational | no ops team, 24h on-call | simplicity bias |

## Requirements pitfalls
- assumed vs stated (the user didn't say, the design assumed)
- "future-proof" (unverifiable) — convert "future" into "the system must be able to change without rewrite"
- Sc.is not SLAs: document the target serialization of "fast enough"

## Elicitation questions (first editor)
1. What's the request rate now? In 12 months?
2. Read:write ratio?
3. Where's the data source? Sensitive?
4. What if it's down 5 minutes?
5. What notifications do operators need?

## Output
A one-paragraph Requirement Lock + the acceptance criteria that the architecture must satisfy (SMART).

## Evidence
— Agile / shifting-left view; VERIFIED practice