# Premature Optimization

## Identity
- Type: anti-pattern
- Status: active
- Importance: medium
- ID: architecture.anti-patterns.premature-optimization
- Severity: MED

## Definition
Optimizing code paths, infrastructure, or architecture for hypothetical problems (Fast until measured).

## Key quote — Knuth
"We must be careful not to optimize prematurely" (then with `profile` before and after.)

## Why it's harmful
- Effort invisible (dev ignores it)
- Complexity rises; maintainability falls
- Wrong purposes optimized (fine, a slow path nobody uses)
- Hard to revert later (cached decision)

## The right discipline (PERFORMANCE_ENGINE)
1. Measure baseline (percentiles, load)
2. Identify hot spot
3. Choose the simplest optimization for *that* bottleneck
4. Benchmark same conditions
5. Only ship if the numbers exist and the simplicity checks out

## Unexpected
- "N+1 is slow" — that's a real hot path (not premature) if it hits DB per iteration
- Indexing hot queries — real optimization, good practice

## Evidence — Knuth/Knuth lesson "about preventing" (VERIFIED aphorism, method official in perf culture)