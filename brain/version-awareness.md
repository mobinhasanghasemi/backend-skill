# brain/version-awareness.md

Global version matrix. Every technology neuron must stay consistent with this file; a change here invalidates the neuron's Version Awareness and triggers re-verification.

> **Knowledge freshness policy**: versions below were verified against official sources in **August 2026**. Always re-verify before basing a production decision on a version number.

## Runtime / frameworks

| Technology | Latest (2026-08) | LTS / support status | Notes |
|---|---|---|---|
| Python | 3.14.7 (Oct 2025) | 3.14 bugfix → Oct 2030; 3.13 bugfix → Oct 2029; 3.12 security → Oct 2028; 3.10 security → Oct 2026; 3.9 EOL | 3.15 due Oct 2026 (PEP 790). 3.14: template strings, subinterpreters; free-threading experimental |
| Django | 6.0.8 (Dec 2025) | **5.2 LTS → Apr 30, 2028**; 6.0 → Apr 2027; 6.1 (Aug 2026); 6.2 LTS (Apr 2027) | Django 6.0 supports Python 3.12–3.14. 4.2 EOL Apr 2026 |
| Django REST Framework | 3.17.2 (Aug 2026) | 3.17.0 added Django 6.0 + Python 3.14 support; dropped Py3.9 & coreapi | Feature-complete project; releases are small |

## Databases

| Technology | Latest (2026-08) | Support notes |
|---|---|---|
| PostgreSQL | 18.4 (Sep 2025 / 18.4 May 2026) | 18 EOL ~Nov 2030. 17 EOL ~Nov 2029. **18 features**: async I/O, B-tree skip scan, UUIDv7, virtual generated columns (default), OAuth authn, wire protocol 3.2, page checksums default, MD5 auth deprecated (use SCRAM), pg_upgrade keeps stats, temporal constraints |
| MySQL | 8.4 LTS / 9.x innovation | LTS 8.4 (2024–2032); 9.x innovation-track |
| Redis | 8.4.5 (Nov 2025) / 8.6.0 (Feb 2026) | 8.0 GA May 2025 — modules merged into OSS (JSON, time series, vectors); AGPLv3/RSALv2/SSPLv1 licensing; I/O threading. 7.4 EOL ~Nov 2026 (software) |

## Messaging

| Technology | Latest (2026-08) | Notes |
|---|---|---|
| Kafka | 4.0.x (Mar 2025) → 4.3.0 (Jun 2026) | **4.0: KRaft-only** (ZooKeeper removed), Java 17 brokers; Share groups early-access; upgrade via bridge 3.9 → 4.0 |
| RabbitMQ | 4.x | classic; check vendor for exact |

## Infrastructure

| Technology | Latest (2026-08) | Notes |
|---|---|---|
| Kubernetes | 1.36.3 (Apr 2026); 1.37 due Aug 26, 2026 | 3 latest minors supported: 1.34 (EOL Oct 2026), 1.35, 1.36 (EOL Jun 2027); 1.33 EOL Jun 2026. ~14-month support windows |

## Observability

| Technology | Status (2026-08) |
|---|---|
| OpenTelemetry traces | STABLE (GA) |
| OpenTelemetry metrics | STABLE |
| OpenTelemetry logs | **STABLE spec (Dec 2025 GA)**; language SDK status varies (Python = Development; Java = Stable) |
| OpenTelemetry baggage | Stable |
| OpenTelemetry profiles | evolving (experimental/development) — do NOT treat as stable |

## Security standards snapshot

| Standard | Status |
|---|---|
| OWASP Top 10 (API) | current |
| NIST SSDF (SP 800-218) | primary SDLC reference |
| OAuth 2.0 (RFC 6749) / OIDC | stable |
| PCI-DSS | v4.0.x |
| GDPR | in force |

## How to update this file

1. Research per RESEARCH_PROTOCOL (official docs first)
2. Update the matrix
3. Update affected neurons' Version Awareness sections
4. Bump the "verified" date here
5. Log the verification in research/index.md

## Amber zone

Anything not in this matrix or with an old verification date = amber. Never state amber facts as current truth.