# Kubernetes (production-reality)

## Identity
- ID: infrastructure.kubernetes
- Type: technology
- Status: active
- Importance: medium-high (adopt from measured need — SIMPLICITY_GOVERNOR)

## Purpose
Orchestration at scale: deploy, scale, heal, roll out — when you've actually outgrown docker-compose (measured!), not because "k8s is the way".

## When Y / When N
- Y: many services, multiple environments, scaling SLA, team the platform behind it
- N: single service/small team — a VM + systemd (or compose) is simpler, cheaper, fully adequate (SIMPLICITY_GOVERNOR veto!)

## Running k8s well (the real laws)
1. **Declarative everything**: everything = manifests in git (GitOps), no kubectl edit in prod
2. **Platform discipline**: namespaces per env, resource requests/limits (no throttling), storage class/encrypted PVC
3. **Liveness vs readiness**: liveness restarts rogue; readiness decides traffic; exec probes need care (side effect!); startupProbe for slow caches
4. **Rollouts**: Deployment strategy RollingUpdate (maxSurge/maxUnavailable), readiness gates; Karpenter/autoscaler tuned on saturation
5. **Secrets**: never in Deployment env; External Secrets Operator / Vault, rotate
6. **Security**: least-privilege RBAC, networkPolicy, non-root, PSS (Pod Security defaults <<= 2024 ruleChange), PodIdentity for cloud creds
7. **Observability**: kube-metrics (resource/util), events, OTel agents, node pools
8. **Upgrade world**: cluster upgrade cadence (k3s/alexs for small), backup etcd/app (velero), disaster drill

## Code tiers
### ❌ Bad
```yaml
apiVersion: apps/v1
kind: Deployment
  replicas: 3 {no resources} {no probes} {image latest} {run as root}
  # rolling update broken (no readiness → queue rebuild!), memory OOM chaos
```
### ✅ Good
```yaml
resources: { requests: {cpu: 250m, memory: 512Mi}, limits: {memory: 1Gi} }
livenessProbe: /healthz  ; readinessProbe: /readyz
strategy: { rollingUpdate: {maxUnavailable: 0, maxSurge: 1} }
imagePullPolicy: IfNotPresent  # tag = commit sha
```
### ⚡ Better
```yaml
# + securityContext: {runAsNonRoot, allowPrivilegeEscalation: false, readOnlyRootFilesystem}
# + secretRef from ExternalSecret; topologySpreadConstraints; PDB (Pod Disruption Budget),
# + nodeSelector per pool; HPA on latency/queue (not just CPU)
```
### 🏆 Excellent
```text
# GitOps (ArgoCD/Flux): every change via PR + auto-sync w/ health gates
# podDisruptionBudget + 2 replicas × AZ; zone-aware (topology spread)
# canary: traffic shift (Istio/Argo Rollouts) with SLO gate
# vertical pod autoscaler suggestions; cost reporting by namespace
# drill: node drain, dead pod, outage of zone — playbook; cluster env backup
# curated: PSP legacy removed — PodSecurity standards "restricted" default
```

## Failure modes
- running everything "just in k8s" before readiness — ops complexity eat teams
- no requests/limits: one hungry pod starves others (noisy neighbor)
- persistent volume + replica issue (RWX/RWO mistakes)
- no PDB: node drain kills all replicas (rolling out chaos)
- liveness killing app (crash-loop)
- RBAC permissive admin

## Evidence
- k8s docs & production-landscape (VERIFIED); GitOps maturity