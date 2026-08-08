# Building AI Agents on the Backend

## Identity
- ID: ai-backends.agents
- Type: concept
- Status: active
- Importance: medium-high

## Purpose
Agentic features (tool use, multi-step tasks, autonomy) — the engineering patterns, rails, guards, and costs. Agents are feature layers over LLMs, not magic: every tool the model can call is a public surface.

## The design shape
1. **Controller loop**: run model with system prompt → tool_schema → observe result → until done/fail/max_steps (5-10)
2. **Tool registry**: every tool = (name, schema, authorization, sandbox, no-op when off-scope)
3. **Guardrails at each boundary**:
   - tool_call must pass authZ (a customer tool only runs on customer's data!)
   - prompt injection: tool outputs treated as untrusted (parsed, escaped, limited size)
   - never pass the whole DB secret set as tool context
4. **Observability**: every step + action logged (trace) — audit trail for any agent action
5. **Concurrency/cost**: budget tokens per task; run async; circuit on provider

## AuthZ- in agents (critical — cross with security/authorization)
Every tool invocation = API call: verify identity + scope at EACH tool, not once per conversation. The model might "remember" another tenant's ids from context.

## Code tiers
### ❌ Bad
```python
result = run_agent(prompt, tools=[db_exec, email_send])   # db_exec executes raw SQL
# model can drop tables, email anyone; no sandbox; no budget (500 steps?)
```

### ✅ Good
```python
TOOLS = [
    Tool("invoice.get", args={"id": int}, 
        handler=lambda id: InvoiceService.get_visible_for(user, id)),  # authz per call!
    Tool("email.send_template", ...sandboxed..., concurrency_limit=2)
]
steps = await run_agent(prompt, tools=TOOLS, max_steps=8, budget_tokens=20_000)
```

### ⚡ Better
```
# tool outputs are data (not prompts): parse via JSON, size-limit, type-validate;
# red-zone tools (email, write) = human confirmation for send (2-step)
# timeouts per step, cancellation, then audit log: [step, tool, args, result]
```

### 🏆 Excellent
```
# per-tenant tool binding + quota; policy module (what a tool may do per role)
# metric: success rate, avg steps, cost, tool misuse attempts (monitor)
# e2e tests: wrap-up scenario golden set; adversarial set (prompt injection attempts)
# runbook: malformed-model-corner investigation (logs + replay)
```

## Failure modes
- agent tool = full-privilege (delete, bulk send, SQL fire!) 
- prompt injection into tools (untrusted doc content steers the agent)
- context size blowup (each step logs whole state; budget)
- no step cap; runaway loop; no early termination
- agents on shared state without locks (repo write races)

## Evidence
- Agent frameworks (OpenAI function/tool calling, LangChain agents — VERIFIED 2026), tool-sandbox best practice (SUPPORTED)