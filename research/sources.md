# SOURCES REGISTRY — verifiable evidence for the skill

> Every claim that carries `VERIFIED` / `SUPPORTED` in a neuron must trace to
> a row here (`source_id`, URL, accessed date, version scope). A row without
> a URL is not evidence. Refresh policy: fast-moving rows get re-checked
> when a neuron's `Last Verified` goes older than 6 months.

Access date for all rows: **2026-08-08** (snapshot); rows flagged `(needs refresh)` when next review is due.

| source_id | Topic | URL | Confidence | Scope notes |
|---|---|---|---|---|
| S-001 | Django docs (stable) | https://docs.djangoproject.com/en/stable/ | VERIFIED | API, models, settings; check per minor |
| S-002 | Django release schedule / LTS | https://docs.djangoproject.com/en/dev/internals/release-process/ | VERIFIED | LTS windows; refresh 2027 |
| S-003 | Django 5.2 release notes | https://docs.djangoproject.com/en/5.2/releases/5.2/ | VERIFIED | 5.2 features, deprecations |
| S-004 | Django REST Framework | https://www.django-rest-framework.org/ | VERIFIED | serializers, viewsets, throttling |
| S-005 | Python versions (devguide) | https://devguide.python.org/versions/ | VERIFIED | EOL/bugfix matrix; refresh annual |
| S-006 | PEP 703 — free-threaded | https://peps.python.org/pep-0703/ | SUPPORTED | experimental mode in 3.13+ |
| S-007 | Python asyncio docs | https://docs.python.org/3/library/asyncio.html | VERIFIED | event loop, tasks; sync-in-async hazards |
| S-008 | Python packaging guide | https://packaging.python.org/ | VERIFIED | pyproject, build backends |
| S-009 | uv documentation | https://docs.astral.sh/uv/ | VERIFIED | fast tooling (runtime moves fast) |
| S-010 | PostgreSQL current docs | https://www.postgresql.org/docs/current/ | VERIFIED | v18 features: uuidv7(), checksums |
| S-011 | PG server config (autovacuum) | https://www.postgresql.org/docs/current/runtime-config-autovacuum.html | VERIFIED | threshold defaults |
| S-012 | PG MVCC internals | https://www.postgresql.org/docs/current/mvcc.html | VERIFIED | snapshot isolation, SSI pointer |
| S-013 | pgvector | https://github.com/pgvector/pgvector | SUPPORTED | versioned repo — API moves |
| S-014 | psycopg 3 docs | https://www.psycopg.org/psycopg3/docs/ | VERIFIED | async, pool, binary params |
| S-015 | Celery documentation | https://docs.celeryq.dev/en/stable/ | VERIFIED | tasks, retries, prefork |
| S-016 | Redis docs (latest) | https://redis.io/docs/latest/ | VERIFIED | 8.x search/json/vector coverage |
| S-017 | Kafka documentation | https://kafka.apache.org/documentation/ | SUPPORTED | 4.x KRaft-only; version drift risk |
| S-018 | RabbitMQ docs | https://www.rabbitmq.com/docs | VERIFIED | quorum/classic queues |
| S-019 | OWASP Top 10 | https://owasp.org/Top10/ | VERIFIED | 2021 list current until refresh |
| S-020 | OWASP API Security Top 10 | https://owasp.org/www-project-api-security/ | VERIFIED | BOLA/IDOR A01 |
| S-021 | OWASP ASVS | https://owasp.org/www-project-ASVS/ | VERIFIED | assurance levels |
| S-022 | OWASP Password Storage Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html | VERIFIED | argon2id/bcrypt guidance |
| S-023 | OWASP Cheat Sheets (index) | https://cheatsheetseries.owasp.org/ | VERIFIED | auth, TLS, injection |
| S-024 | NIST SP 800-57 Part 1 | https://csrc.nist.gov/pubs/sp/800/57-part-1/r5/final | VERIFIED | key management (512-bit minimum note) |
| S-025 | RFC 8446 — TLS 1.3 | https://datatracker.ietf.org/doc/html/rfc8446 | VERIFIED | handshake, 0-RTT |
| S-026 | RFC 9457 — Problem Details | https://datatracker.ietf.org/doc/html/rfc9457 | VERIFIED | API error JSON shape |
| S-027 | RFC 7519 — JWT | https://datatracker.ietf.org/doc/html/rfc7519 | VERIFIED | claims, signature |
| S-028 | RFC 9562 — UUID v7 | https://datatracker.ietf.org/doc/html/rfc9562 | VERIFIED | time-ordered IDs |
| S-029 | RFC 9106 — Argon2 | https://datatracker.ietf.org/doc/html/rfc9106 | VERIFIED | memory-hard KDF |
| S-030 | RFC 9111 — HTTP caching | https://datatracker.ietf.org/doc/html/rfc9111 | VERIFIED | cache-control semantics |
| S-031 | Kubernetes docs | https://kubernetes.io/docs/home/ | VERIFIED | controllers, config, security |
| S-032 | Docker docs | https://docs.docker.com/ | VERIFIED | dockerfile, compose |
| S-033 | SRE Book (Google) | https://sre.google/srebook/table-of-contents/ | VERIFIED | error budgets, reliability theory |
| S-034 | DORA research reports | https://dora.dev/research/ | SUPPORTED | 2023/2024 elite findings |
| S-035 | Gitleaks (secrets) | https://github.com/gitleaks/gitleaks | VERIFIED | repo scanner (fast-moving) |
| S-036 | Semgrep docs | https://semgrep.dev/docs/ | VERIFIED | static rules for security/lint |
| S-037 | Django 6.0 release notes | https://docs.djangoproject.com/en/6.0/releases/6.0/ | VERIFIED | 6.0 features, deprecations; refresh per minor |
| S-038 | Django security releases | https://docs.djangoproject.com/en/stable/releases/security/ | VERIFIED | CVE advisories; check monthly |
| S-039 | Django async docs | https://docs.djangoproject.com/en/stable/topics/async/ | VERIFIED | async views, ORM async; still sync ORM core |
| S-040 | Django migrations docs | https://docs.djangoproject.com/en/stable/topics/migrations/ | VERIFIED | expand/contract, zero-downtime |
| S-041 | Python 3.14 release notes | https://docs.python.org/3.14/whatsnew/3.14.html | VERIFIED | template strings, subinterpreters |
| S-042 | Python typing (PEP 484) | https://typing.readthedocs.io/en/latest/ | VERIFIED | type hints, mypy; fast-moving |
| S-043 | pip / packaging | https://pip.pypa.io/en/stable/ | VERIFIED | pip, wheel, lockfile discipline |
| S-044 | PostgreSQL 18 release notes | https://www.postgresql.org/docs/18/release-18.html | VERIFIED | AIO, uuidv7, checksums; verify per minor |
| S-045 | PostgreSQL partitioning | https://www.postgresql.org/docs/current/ddl-partitioning.html | VERIFIED | declarative partitioning, pruning |
| S-046 | PostgreSQL replication | https://www.postgresql.org/docs/current/runtime-config-replication.html | VERIFIED | streaming, slots, lag |
| S-047 | PostgreSQL indexing | https://www.postgresql.org/docs/current/indexes.html | VERIFIED | btree, gin, partial, covering |
| S-048 | PostgreSQL RLS | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | VERIFIED | row-level security policies |
| S-049 | psycopg pool docs | https://www.psycopg.org/psycopg3/docs/advanced/pool.html | VERIFIED | pool, async pool, sizing |
| S-050 | Redis 8 GA announcement | https://redis.io/blog/redis-8-ga/ | VERIFIED | GA 8.0 May 2025 modules merged |
| S-051 | Redis Vector Sets | https://redis.io/docs/latest/commands/vadd/ | SUPPORTED | vector set beta; API may shift |
| S-052 | Redis ACL docs | https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/ | VERIFIED | ACL, users, TLS |
| S-053 | Kafka KRaft docs | https://kafka.apache.org/documentation/#kraft | VERIFIED | KRaft-only 4.x, no ZooKeeper |
| S-054 | RabbitMQ quorum queues | https://www.rabbitmq.com/docs/quorum-queues | VERIFIED | quorum vs classic trade-offs |
| S-055 | OpenTelemetry Python SDK | https://opentelemetry.io/docs/languages/python/ | VERIFIED | traces/metrics/logs SDK status |
| S-056 | Prometheus docs | https://prometheus.io/docs/ | VERIFIED | metrics, PromQL, alerting |
| S-057 | Grafana docs | https://grafana.com/docs/ | SUPPORTED | dashboards, Loki, Tempo |
| S-058 | Sentry Python SDK | https://docs.sentry.io/platforms/python/ | VERIFIED | error tracking, performance |
| S-059 | HashiCorp Vault docs | https://developer.hashicorp.com/vault/docs | VERIFIED | secrets, transit, rotation |
| S-060 | Let's Encrypt docs | https://letsencrypt.org/docs/ | VERIFIED | ACME, TLS automation |
| S-061 | OAuth 2.1 draft | https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13 | SUPPORTED | OAuth 2.1 consolidates best practices |
| S-062 | OIDC discovery | https://openid.net/specs/openid-connect-discovery-1_0.html | VERIFIED | OIDC discovery spec |
| S-063 | JWT best practices (RFC 8725) | https://datatracker.ietf.org/doc/html/rfc8725 | VERIFIED | JWT security considerations |
| S-064 | Pydantic docs | https://docs.pydantic.dev/latest/ | VERIFIED | validation, settings, v2 |
| S-065 | pytest docs | https://docs.pytest.org/en/stable/ | VERIFIED | fixtures, parametrize, plugins |
| S-066 | Factory Boy docs | https://factoryboy.readthedocs.io/en/stable/ | VERIFIED | factories for Django ORM |
| S-067 | httpx docs | https://www.python-httpx.org/ | VERIFIED | async HTTP client, timeouts |
| S-068 | Celery canvas & chords | https://docs.celeryq.dev/en/stable/userguide/canvas.html | VERIFIED | chain/group/chord, DLQ patterns |
| S-069 | S3 / MinIO docs | https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html | VERIFIED | presigned URLs, lifecycle |
| S-070 | Helm docs | https://helm.sh/docs/ | VERIFIED | charts, atomic upgrade, rollback |
| S-071 | GitHub Actions docs | https://docs.github.com/en/actions | VERIFIED | workflow, OIDC, caching |
| S-072 | GitLab CI docs | https://docs.gitlab.com/ci/ | VERIFIED | pipeline, DAG, environments |
| S-073 | RFC 9110 — HTTP semantics | https://datatracker.ietf.org/doc/html/rfc9110 | VERIFIED | methods, status, caching |
| S-074 | RFC 7807 superseded context | https://datatracker.ietf.org/doc/html/rfc9457#appendix-A | VERIFIED | RFC 7807 → 9457 migration |
| S-075 | NIST SSDF SP 800-218 | https://csrc.nist.gov/pubs/sp/800/218/final | VERIFIED | secure dev practices |
| S-076 | OWASP Cheat Sheet — CSRF | https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html | VERIFIED | CSRF token, SameSite |
| S-077 | OWASP CORS cheat sheet | https://cheatsheetseries.owasp.org/cheatsheets/Cross-Origin_Resource_Sharing_Cheat_Sheet.html | VERIFIED | CORS, preflight, allowlist |
| S-078 | OWASP Logging cheat sheet | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | VERIFIED | no PII/secrets in logs |
| S-079 | 12-Factor App | https://12factor.net/ | SUPPORTED | config, disposability, logs |
| S-080 | Google API Design Guide | https://cloud.google.com/apis/design | SUPPORTED | resource naming, error model |
| S-081 | Stripe API idempotency | https://docs.stripe.com/api/idempotent_requests | VERIFIED | Idempotency-Key pattern reference |
| S-082 | CloudEvents spec | https://github.com/cloudevents/spec | VERIFIED | event envelope for webhooks/outbox |

## How to cite from a neuron

```text
## Evidence
- Django ORM query plans and indexes: VERIFIED via source-S-001 (docs.djangoproject, accessed 2026-08)
- async loopholes: SUPPORTED (S-007, S-015)
```

Rules:
- Never write `VERIFIED` without a source-<ID> + access date.
- `SUPPORTED` = interpreted practice; `EXPERIMENTAL` = not reproduced here.
- If the URL became 404 during a refresh → flag and re-route the row; do NOT keep a dead URL in VERIFIED state.