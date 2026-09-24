# RESEARCH INDEX — external facts & evidence registry

> Purpose: browseable registry of external knowledge captured, verified,
> and dated (audit Phase 1: fact checking). Fix claims drift by refresh.

## How to record a claim
```
[claim id] Brief Claim
- source: URL (source name)
- verified: YYYY-MM-DD | access: YYYY-MM-DD
- confidence: VERIFIED | SUPPORTED | INFERRED | EXPERIMENTAL
- scope: applies only under...
```

## Registry (add rows; keep chronological note per domain)
- (res-001) Django 5.2 LTS support window (until Apr 30, 2028); 6.x branches
  source: djangoproject.com/releases (VERIFIED 2025-12; check yearly)
- (res-002) Python 3.14 release Oct 2025; 3.13 bugfix to Oct 2029; EOL matrix
  source: python.org/dev/peps/ (VERIFIED; refresh 2026-10)
- (res-003) PostgreSQL 18: native uuidv7(), checksums default, AIO benchmarks
  source: postgresql.org/docs/18 (VERIFIED 2025; re-check per minor)
- (res-004) MongoDB 8.x: transactions exist (4.0+); JSONB vs document modeling
  source: mongodb.com/docs (VERIFIED 2026-08; minors amber)
- (res-005) Redis 8 (2025): built-in Search/JSON/TimeSeries/vector; licensing
  AGPLv3/RSALv2/SSPLv1; I/O threading, vector set beta
  source: redis.io/docs (VERIFIED 2026-08)
- (res-006) Kafka 4.x: KRaft-only brokers, Java 17, bridge 3.9→4.0 upgrade
  source: kafka.apache.org/documentation (VERIFIED 2026-06; check at minor)
- (res-007) OWASP Top 10 2021 classes; CWE Top 25 (check 2026 refresh)
  source: owasp.org/www-project-top-ten/ (VERIFIED concept set)
- (res-008) TLS 1.3 RFC 8446; NIST SP 800-57 key management
  source: rfc-editor.org; nist.gov (VERIFIED)
- (res-009) Problem Details RFC 9457 (former 7807) for API errors
  source: rfc-editor.org/rfc/rfc9457 (VERIFIED)
- (res-010) 3-2-1 backup rule; AWR/Kimball modeling; DORA 2023 elite findings
  source: multi (drift risk; treat as SUPPORTED guidance)
- (res-011) Redis vector set beta; pgvector current docs (embedding ops list)
  source: redis.io / github.com/pgvector/pgvector (VERIFIED 2026-08)
- (res-012) Django 6.0.8 / DRF 3.17.2 / Python 3.14.7 version matrix 2026-08
  source: docs.djangoproject.com + devguide.python.org + djangoproject.com (VERIFIED 2026-08, S-037/S-038/S-041)
- (res-013) PG 18.4 partitioning / RLS / replication + psycopg pool
  source: postgresql.org/docs/18 + psycopg.org (VERIFIED 2026-08, S-044/S-045/S-046/S-048/S-049)
- (res-014) Redis 8 GA + ACL + vector sets
  source: redis.io/docs + redis.io/blog/redis-8-ga (VERIFIED 2026-08, S-050/S-051/S-052)
- (res-015) OTel Python SDK stable + Prometheus + Grafana
  source: opentelemetry.io + prometheus.io (VERIFIED 2026-08, S-055/S-056)
- (res-016) Vault + gitleaks + semgrep secret scanning
  source: developer.hashicorp.com + github.com/gitleaks + semgrep.dev (VERIFIED 2026-08, S-059/S-035/S-036)
- (res-017) S3 presigned URLs + lifecycle + Helm + GitHub Actions
  source: docs.aws.amazon.com + helm.sh + docs.github.com (VERIFIED 2026-08, S-069/S-070/S-071)
- (res-018) OAuth 2.1 draft + OIDC + JWT best practices (RFC 8725)
  source: datatracker.ietf.org + openid.net (VERIFIED 2026-08, S-061/S-062/S-063)

## Re-verify Log (quarterly drills)

| Date | Neurons re-verified | Sources | Outcome |
|---|---|---|---|
| 2026-08-27 | 10 new guardrail neurons + 14 patched anti-patterns | S-048/S-055/S-069/S-050/S-031 | All VERIFIED; 223/233 contract now passing |
| 2026-08-27 | Multi-tenancy RLS + cache isolation | S-048/S-052 | RLS qual 3% overhead confirmed (EXPERIMENTAL until measured in prod) |

## Refresh policy
- fast-moving (versions, limits, SDKs): re-check at research gate when neuron
  Last Verified > 6 months. Update the neuron + this index in the same note.

## Verification rules
1. Only a date+URL access makes a claim "VERIFIED" (audit gap closure)
2. Unverified → mark VERIFIED only after files/HTML read (WebFetch / docs page)
3. Experimental (benchmarks) = label EXPERIMENTAL until reproduced