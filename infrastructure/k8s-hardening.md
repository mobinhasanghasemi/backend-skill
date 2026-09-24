# K8s Hardening — PodSecurity, NetworkPolicy, Secrets

## Identity
- ID: infrastructure.k8s-hardening
- Domain: infrastructure
- Type: procedure
- Status: active
- Importance: high
- Last Verified: 2026-08

## Purpose
Harden Kubernetes workload so a compromised pod cannot move laterally or exfiltrate secrets — complement to containers/kubernetes.

## Core Concept
Least privilege at three layers: pod (no root, readonly FS), network (default deny), secrets (external manager, no env).

## Activation Conditions
- Any K8s deploy with PII/payment or multi-tenant; S-031 relevant

## Decision Rules
- PodSecurity `restricted`: `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, `seccompProfile: RuntimeDefault`.
- NetworkPolicy: default `deny-all` then allow `frontend→api:8000`, `api→postgres:5432` only; DNS egress allowed.
- Secrets: External Secrets Operator or SealedSecrets; never `envFrom` secret dump; mount as file, rotation via reloader.
- Image: distroless/python, `USER 65532`, `COPY --chown`, scan with Trivy in CI.

## Security
- RBAC least privilege per service account; no default SA; `automountServiceAccountToken: false` unless needed; S-031.

## Reliability
- PDB `minAvailable: 2` for API; liveness vs readiness probes separate; resource requests/limits set.

## Evidence
- K8s PodSecurity/NetworkPolicy VERIFIED via S-031 (accessed 2026-08).

## Code Tiers
<!-- data-only -->
```yaml
# NetworkPolicy default deny (data-only)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny}
spec: {podSelector: {}, policyTypes: [Ingress, Egress]}
```
