# INFRASTRUCTURE — ROOT NEURON

## Identity
- ID: infrastructure.root
- Domain: infrastructure
- Type: root
- Status: active
- Importance: medium-high

## Purpose
Router for how the backend is packaged and run: containers, orchestration, serverless — chosen from measured need, not fashion (SIMPLICITY_GOVERNOR veto on k8s).

## Activation
- packaging, deploying, running services (Dockerfiles, images, clusters)
- k8s/containers discussions, scaling the platform
- any proposal adding infrastructure complexity

## Routing
```text
package & run         → containers.md (Dockerfile contract, images)
orchestration         → kubernetes.md (when N, how to do it well)
simple deploys        → devops/ROOT (single VM estimates first)
```
## Mandatory posture
1. **Simplest container shape first** — single VM/docker-compose until measured need (SIMPLICITY_GOVERNOR)
2. Every image: pinned base, non-root, HEALTHCHECK, versioned artifact (git sha)
3. k8s costs a platform team: only adopt with justification + rollback path (ARCH010)

## Security Checks
- least-privilege RBAC, secrets never in manifests (External Secrets/Vault), networkPolicy, PSS defaults
- images scanned (trivy/grype) and signed in CI

## Reliability Checks
- resource requests/limits everywhere; readiness gates for rollouts; backup/dr for stateful components (velero/etcd backup)

## Performance Checks
- resources declared ("no throttling"); saturation metrics; skip claim numbers without measurement

## Evidence
- k8s/container best practices (VERIFIED via vendor docs); adoption gates per SIMPLICITY_GOVERNOR

## Children
infrastructure.containers, infrastructure.kubernetes

## Parent
- devops (delivery), security (SECURITY_GUARDIAN), reliability (failure/DR)