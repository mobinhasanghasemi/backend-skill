# DECISION ENGINE


The protocol for any significant architectural or technical decision. Used by `BRAIN.md` at the core decision stage.

## Decision pipeline (mandatory)

```text
Requirements        (what must be true when it ships)
Constraints         (budget, time, scale, team, compliance, environment)
Candidate Solutions (at least 2, at most 3–4 for readability)
Evidence            (attach the classes per candidate)
Trade-offs          (per candidate: complexity/cost/perf/security/rel/ops)
Risk Analysis       (per candidate)
Security Review     (SECURITY_GUARDIAN.md)
Performance Review  (PERFORMANCE_ENGINE.md — measured vs claimed)
Operational Review  (can this team run it? on-call load?)
Alternatives        (incl. "keep as is")
Decision → Rationale
Validation plan     (how to verify/track post-ship)
```

Rules:
- **No choosing by popularity** — a tech = popular ≠ right.
- **No premature distribution**: simple monolith + single DB first, unless a constraint (traffic, ingest rate, team boundaries) physically demands otherwise.
- Write the decision down (ADR template at `adr/template.md`).

## Counterfactual reasoning (always for major decisions)

For candidates A / B / C evaluate:

```text
complexity
cost (engineering + runtime)
performance
security
reliability
scalability
operational burden
developer experience
migration cost
failure modes
```

Plus: **What happens if we do NOT choose this?**

Example:

> We do not choose Kafka. → Writes stay synchronous. Peak load: 40 req/s, DB handles it. Correct.

## Reasoning trace (output format)

Every answer must be able to justify itself. See BRAIN.md "Reasoning Trace".

## Conflict resolution (experts disagree)

PROTOCOL:
1. Detect conflict (identify competing objectives)
2. Check evidence at each position
3. Check constraints (which objective matters per constraints?)
4. Compare risks
5. Compare operational cost
6. Determine context (who is the user? workload? data?)
7. DECIDE, and articulate the losing side's strongest argument

Example: security wants full panache (full re-auth on every request), performance wants cached auth. Constraint: money transfer API, must not rely on cached auth. Decision: re-auth, cache only low-risk reads.

## Interplay with the rest of the brain

- The **Simplicity Governor** gets a veto light: new distributed/dog complexity must justify itself.
- The **Architecture Linter** checks output.
- The **Failure Propagation** section (brain/failure-propagation.md) pre-checks the chosen topology.
- The **Architecture Genome** (`ARCHITECTURE_GENOME.md`) encodes the final decision compactly.

## When to use (and NOT)

Use: ≥1 non-trivial architectural choice; multi-tenancy; scale step; new datastore; security-sensitive design; anything where "it depends…" is tempting.

Don't over-engineer the process for: straightforward, non-risky, reversible, clearly-scoped choices.

## Rules of thumb on decisions

- If the answer inverts without evidence basis → flag.
- If you can't find an official source for a "53% faster" claim → mark UNCERTAIN.
- If a decision has a migration cost you can't quantify → say so.
- Never answer "It depends" alone — say on what.