# API Error Design

## Identity
- ID: api.error-design
- Type: procedure
- Status: active
- Importance: critical

## Purpose
Errors are part of the contract, not an afterthought: machine-parseable, human-actionable, and never leaking internals.

## Core principle: Problem Details (RFC 9457, formerly 7807)
```json
{
  "type": "https://api.example.com/problems/order/insufficient-balance",
  "title": "Insufficient Balance",
  "status": 422,
  "detail": "Your balance 5.00 covers 3.00 of the 4.00 needed",
  "instance": "/orders/123",
  "errors": [{"field": "amount", "code": "min_value", "message": "..."}]
}
```
- `type` = stable machine-readable code/schema → clients can branch on it
- `detail` = human text; valid under logging rules (no secrets, no stack)

## Code tiers

### ❌ Bad
```python
return {"error": True, "message": "Order failed"}      # ambiguous, no code
# → clients if/else on string; 500 for everything; exception trace leaks
```

### ✅ Good
```python
raise ApiError(status=422, code="insufficient_balance", detail="...")
# centralized exception handler → JSON body with type/title/status/detail
```

### ⚡ Better — field-level machine codes
```python
raise ValidationApiError({
    "amount": "AMOUNT_MIN",     # machine code per rule
    "email": "EMAIL_INVALID",
})
# clients: per-field translation and retry guidance
```

### 🏆 Excellent
```text
- RFC 9457 Problem+JSON with stable type URIs per error category — documented in OpenAPI
- per-field error codes with messages for human UX; instance id = trace id (correlation!)
- 4xx: never retry unless 429/408; 5xx: retryable with backoff — documented to clients
- auth errors: 401 (no creds) vs 403 (forbidden) vs 401+no-op vs 404 for object hiding
- mock server from spec → clients test against real error shapes
- error log monitoring: top `type` values, alert on spikes (DORA-style CRITICAL)
```

## Failure modes
- 200 with "ok:false" (API successfully returns NOT success — clients must parse bodies)  
- stack traces/DB error text in responses (information leak!)  
- new error types without `type` URI → clients can't program  
- everything as 400 vs correct semantics (422 for validation, 409 conflicts)

## Security
- never echo DB exceptions, internal IDs, file paths; error pages too!

## Evidence
- Problem Details (RFC 9457): VERIFIED via source-S-026 (accessed 2026-08); per-field validation errors (SUPPORTED practice)
