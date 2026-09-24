# AI Guardrails — Prompt Injection, PII, and Evals

## Identity
- ID: ai-backends.guardrails
- Domain: ai-backends
- Type: procedure
- Status: active
- Importance: critical
- Last Verified: 2026-08

## Purpose
Ship LLM/RAG features without leaking tenants, secrets, or accepting injected instructions — with evals that block deploys.

## Core Concept
Layered guard: input scrub → tool allowlist → output filter → tenant isolation → eval gate. Treat prompt as untrusted input.

## Activation Conditions
- Any LLM call, RAG, agent tool-calling; complements ai-backends/ROOT + security

## Decision Rules
- Input: strip PII with allowlist NER, limit 4k tokens, deny `ignore previous instructions`, path traversal, and data exfiltration patterns (S-036 semgrep).
- Tools: allowlist only (`search_catalog` yes, `exec_sql` no); require human approval for side-effect tools; S-055 for tracing.
- Output: PII scrub, max length, JSON schema validation, no secrets/PII in logs (S-078).
- Tenant isolation: per-tenant vector namespace + RLS on retrieval + cache key includes tenant (ARCH025).
- Evals: 20 golden prompts (injection, PII, tenant leak) must pass 100% in CI (S-065 pytest).

## Security
- Prompt is untrusted boundary (OWASP LLM Top 10); treat as `security` domain always; S-019/S-020.

## Performance
- Scrub + filter <50ms p95; cache LLM responses per tenant+prompt hash with 5m TTL; S-055 metrics.

## Reliability
- Fallback: on filter fail → safe completion “I can’t do that”; DLQ for flagged prompts; alert on injection rate >1%.

## Evidence
- OTel Python VERIFIED via S-055, logging via S-078, semgrep via S-036, pytest via S-065 (accessed 2026-08).

## Code Tiers
<!-- illustrative -->
```python
# guardrails (illustrative — adapt to your LLM client)
def guarded_call(prompt, tenant_id):
    clean = scrub_pii(prompt)  # allowlist, S-078
    if is_injection(clean): raise GuardrailBlock("injection")
    res = llm.call(clean, tools=ALLOWLIST, tenant_id=tenant_id)
    return validate_schema(scrub_pii(res))
```
