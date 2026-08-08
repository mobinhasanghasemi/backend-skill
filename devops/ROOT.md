# DEVOPS — ROOT NEURON

## Identity
- ID: devops.root
- Domain: devops
- Type: root
- Status: active
- Importance: medium

## Purpose
Delivery engineering: CI/CD pipelines, artifacts, progressive rollout — the mechanism that makes change safe and reversible.

## Activation
- pipelines, CI/CD, release engineering, IaC/GitOps
- deploy process redesign, rollback mechanics

## Routing
```text
pipeline design      → ci-cd.md (gates, artifacts, verify-after-deploy)
rollout mechanics    → reliability/deployment.md (progressive delivery)
flake/CI debugging   → ci-cd.md (fail-fast gates)
```

## Non-negotiables
1. Every prod change is a reviewed artifact (SHA) with a locked config + migration id
2. Rollback = redeploy previous artifact (feature flags second lever)
3. Secrets never printed in CI logs (giteaks/pip-audit in the fail-fast gate)
4. Verify after deploy: synthetic + real-time SLO window

## Common failure modes
- CI too long → bypass
- prod-from-laptop (no pipeline) → no audit trail
- config drift CI vs prod
- migrations driven outside the pipeline

## Connections
- infrastructure (build/runtime), testing (gates), reliability (deployment), security (hardening)

## Evidence
- CI/CD and release practice: SUPPORTED practice (no single canonical doc)
