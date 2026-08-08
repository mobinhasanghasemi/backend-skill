# Playbook: Secret Exposed

> Priority: scope who saw it, rotate; then root-cause. Never minimize ("just code a fix").

## T-0 (minutes)
1. **Guess**: was it pushed to repo/CI logs/external? (check git history; GitHub secret scanning results; CI log)
2. **Rotate NOW** (No half: rotate the key/secret; invalid old; status "rotating" to all consumers)
3. **Notify**: security channel (informed) with redacted detail (not the secret itself!)

## Rotation concrete
| Secret type | Action |
|---|---|
| API signing key | swap signer (secret manager: version-2 active), grace window old key 24-48h (both valid), then old revoked (docs precisely in runbooks) |
| DB password | rotate in DB + app release config (2-deploy secret propagation), connection drain |
| Cloud provider key | deactivate + rotate; usage1 = cloud provider); access analysis risk |
| Access token (integration) | provider-level revoke + reissue (then**
check for use by consumer contracts!**

## Verification
- old secret test outside: fail auth; new works
- rebuild process: secrets out of repos (secrets.md), CI scan (gitleaks) + license, rotation calendar; key-ever-in-repo scanning of full history

## The chronic fix
- gitleaks workflow (block PR with secret-ish); .env never committed (gitignored + error in CI if found); the whole history scan in pipeline (BFG cleanup + force-push plan + de-authorize exceptions) — and the BIG rule: rotation plan for EVERY secret (roadmap!)