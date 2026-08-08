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