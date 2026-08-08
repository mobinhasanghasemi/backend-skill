# Playbook: Authentication Incident
> e.g. login breakage, session clear, brute-force, token leaks. Scope: SUSPECT + re-run happy path is not the aim; question is "is it malicious or broken?"

## Phase 1 — Stop the bleeding (5 min)
1. **Classify** (login rate failing? session/401? suspicious): check dashboards (auth endpoint error rate, rate limit p90, IP source)
2. **Brute-force burst?** — rate limit blocking (api/rate-limiting.md): vary per IP+credential+path; fallback: block IP ranges' chains (careful NOT to block all users — allow when clean)
3. **Token leak**: rotate your signing secret(s) NOW (JWT: swap signing key), invalidate sessions (session store flush), alert all consumers
4. **Stuck valid user**: whitespace/locale (email normalization — case/trim/UTR36); confirm not user-side

## Phase 2 — Confirm and isolate
- Threat model: who could craft this? (tokens, signatures) — validate signature in each path
- For session-break: which change broke (middleware, cache, secret rotation?, cookie attributes), roll it back (deployment-failure playbook)

## Phase 3 — Face & future
- Rotate exposed credentials; reset affected users (with secure link) — rate limited
- Revise token/session lifetime (15m access + refresh rotation)
- Rate-limit adds from events; IDOR audit guard

## Phase 4 — Postmortem input
- attack vs breakage disambiguation (what telemetry would have fire faster) — invest in anomaly dingdong: impossible travel, failed-login ramp, unusual token use

## Key metrics
- auth error rate (login), token-branch errors, rate-limit rejections