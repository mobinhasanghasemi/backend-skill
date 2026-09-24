# ARCHITECTURE LINTER


Machine-checkable architecture violations. When the brain produces a design, or when reviewing an existing system, run these rules. Each rule: name, trigger, why, severity, fix direction.

## Rule list

| ID | Violation | Severity |
|---|---|---|
| ARCH001 | External network call **without timeout** | HIGH |
| ARCH002 | Retry **without idempotency analysis** | HIGH |
| ARCH003 | Cache **without invalidation strategy** | HIGH |
| ARCH004 | Critical path **without observability** (metrics/tracing) | HIGH |
| ARCH005 | Sensitive operation **without authorization check** | CRITICAL |
| ARCH006 | **Unbounded queue** (memory/backlog) | HIGH |
| ARCH007 | Database query **inside iteration** (N+1) | MED |
| ARCH008 | Microservice **without independent responsibility** | HIGH |
| ARCH009 | Distributed component **without failure model** | HIGH |
| ARCH010 | Kubernetes **without operational justification** | MED |
| ARCH011 | Critical state **without backup strategy** | HIGH |
| ARCH012 | **No migration rollback strategy** | HIGH |
| ARCH013 | Abuse-prone endpoint **without rate limiting** | HIGH |
| ARCH014 | Cross-tenant data access **without isolation analysis** | CRITICAL |
| ARCH015 | Synchronous chain with **excessive failure propagation** | HIGH |
| ARCH016 | **No timeouts on DB/queue/HTTP clients** | HIGH |
| ARCH017 | Secrets **in code/repo/env-logs** | CRITICAL |
| ARCH018 | Direct client→DB access without service layer/authz | HIGH |
| ARCH019 | No health/readiness on ingress target | MED |
| ARCH020 | Trusting user-supplied content for file paths/URLs (SSRF/path traversal) | CRITICAL |
| ARCH021 | Over-normalized read-heavy hot path (query explosion) | MED |
| ARCH022 | Event-sourcing / CQRS without event-schema migration plan | MED |
| ARCH023 | Webhook/outbound integration without signature verification | HIGH |
| ARCH024 | Distributed lock / semaphore without TTL & fencing | MED |
| ARCH025 | Multi-tenant shared cache with cross-tenant keys | CRITICAL |
| ARCH026 | No capacity headroom for peak traffic | MED |
| ARCH027 | No DR / RPO/RTO defined for stateful service | HIGH |
| ARCH028 | Untested backup (never restored) | MED |
| ARCH029 | Sync HTTP calls in hot path with unlimited parallel fan-out | MED |
| ARCH030 | No pagination/cursor on unbounded list endpoint | MED |
| ARCH031 | Direct user input concatenated into SQL/HTML/shell | CRITICAL |
| ARCH032 | No circuit breaker around flaky dependency | MED |
| ARCH033 | Logging PII/credentials | HIGH |
| ARCH034 | Global mutable state in async context | MED |
| ARCH035 | `SELECT *` / unbounded columns in production queries | LOW |
| ARCH036 | Prescriptive **"must/always use X" without context** — violates Influence, never command (BRAIN.md:116) | MED |

## Severity semantics

- CRITICAL: security/consistency compromise → block
- HIGH: likely incident or data loss → fix before ship
- MED: incident risk under specific conditions → plan
- LOW: quality/maintainability → backlog

## Review flow

```
Run rules against design (or existing system)
  → output list of violations with IDs
  → for each: severity + mitigation + accepted-risk decision
  → record decisions in ADR if non-trivial
```

## Limitations

This is a heuristic linter. It flags patterns with a **causal link** to incidents; it does not prove correctness. Absence of violations ≠ secure/reliable architecture. Treat findings as triggers for evidence review, not absolute verdicts.