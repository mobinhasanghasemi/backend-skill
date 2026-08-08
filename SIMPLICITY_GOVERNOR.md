# SIMPLICITY GOVERNOR

Every proposed component must justify its existence. This governor rejects unearned complexity. Apply it to every architecture output and every neuron recommendation.

## The five questions

For every component:

```text
1. Why does this exist?          (what requirement forces it?)
2. What requirement forces it?   (which constraint? be specific)
3. What complexity does it add?  (moving parts, config, failure modes)
4. What operational burden?      (on-call load, upgrades, debugging)
5. What failure modes?           (how does it break things?)
   + What simpler alternative was rejected — and why?
```

If the answers are weak → **DO NOT INTRODUCE THE COMPONENT.**

## Complexity budget

- Every distributed piece (queue, cache, replica, second DB, microservice, k8s) costs the same currency: debugging, alerts, configs, training, page-calls.
- Question each addition against the **current** requirements — not the roadmap.

## Default positions (unless constrained)

```text
application shape   → monolith (modular if predicted growth)
database            → single relational DB (PostgreSQL by default; see databases/ROOT)
caching             → none until measured read pressure
messaging           → none until async/decoupling is required
container platform  → single VM / simple deploy until scale demands
event sourcing      → not for CRUD
microservices       → not for small systems
kubernetes          → not for simple single-server
sharding            → only after partition + replica ceilings hit (measured)
multi-region        → only with a real geo/latency/DR requirement
```

## The "simplest correct" test

Given the constraints, find the minimal architecture that meets them. Then add only what's strictly necessary, in this order of escalation:

1. Monolith + single DB (single AZ if possible)
2. + read replicas (measured)
3. + cache (measured)
4. + queue for async work
5. + split services only at team/scale boundaries
6. + k8s only when ops justifies it

## Anti-arguments (what sounds good but isn't)

- "X company does it" — they have different constraints.
- "It's the future-proof choice" — you don't know the future; design for change instead.
- "It's only one more service" — one more service = one more failure domain.
- "We'll need it eventually" — build the thinnest path that supports evolution, not the full destination.

## Veto mechanics

- Governor vetoes a component → decision must be recorded with the *rejected* alternative and its reason (ADR).
- Override possible only when the requirement is explicit (user statement, compliance, measured constraint).
- Override path: show the requirement that forces the component.

## Relationship to other protocols

- `DECISION_ENGINE.md` — decision flow
- `ARCHITECTURE_LINTER.md` — violations (ARCH010 etc.)
- `brain/failure-propagation.md` — how each added component multiplies failure surface