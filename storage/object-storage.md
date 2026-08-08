# Object Storage Patterns (S3-compatible)

## Identity
- ID: storage.object-storage
- Type: procedure
- Status: active
- Importance: high

## Purpose
Objects (images, files, exports, backups) in managed storage: keys, uploads (direct/presigned), delivery (signed URLs), lifecycle and cost — ramped patterns bad → excellent.

## Core patterns
1. **Isolation**: separate bucket per tenant-class or enforced prefix policies (tenant_id) — no cross-tenant paths; a bucket is a wall; do not share across tenants
2. **Keys**: `tenant/{uuid}/uploads/…` — paths are a namespace; define early
3. **Upload**: presigned PUT (server grants URL, client streams directly, size/mimetype validated server-side at grant)
4. **Access**: presigned GET with expiry (TTL), may require user auth (gateway checks token)
5. **Integration**: media served via CDN + cache headers; DB stores only object key
6. **Cost lifecycle**: S3 lifecycle → cold after N days, delete after M; storage classes

## Code tiers
### ❌ Bad
```python
def upload(request):
    data = request.FILES["file"].read()      # whole file in RAM!
    s3.upload_bytes(key=data, data)          # size unlimited, no type check
    return url_to_private_file(key)          # no expiry — permanent readable URL
```
### ✅ Good
```python
def request_upload_endpoint(request):
    key = f"{request.tenant.uid}/{uuid4().hex}"
    signed = s3.generate_presigned_url("put_object", Params={"Bucket": B, "Key": key}, ExpiresIn=600)
    storage_keys.create(owner=request.user, tenant=..., key=key, content_type=...)
    return {"url": signed, "key": key}   # client streams directly
# download: generate presigned GET (TTL 300s), check owner authz in endpoint
```
### ⚡ Better — verified
```python
# server-side checks: size max (config), mime whitelist, scanning for malware hook
# multipart/resumable for >100MB; CDN/cache (Cache-Control max-age on GET via CDN)
# object deletion: lifecycle or explicit soft-delete rows gate + confirm prompt
# monitor: transfer bytes, latency, hit rate (CDN), bucket error rate
```
### 🏆 Excellent
```text
# open: signed uploads + stats; lifecycle audit (bucket inventory weekly)
# ransomware defense: versioning + immutable bucket policy + object lock (delete-protect)
# PII: never store unsuspended personal docs without policy (classification meta tag)
# tests: presigned access denied when unauthorized (IDOR against storage!)
# cross-region replication for durability-class only vs cost
# failing fast: bucket name/bind mapping in code (env-aware)
```

## Failure modes
- 10GB DB blob (backup die)
- public bucket no login
- presigned without expiry (eternal link)
- tenant isolation via only-app-connector (miss a path = leak)
- server streams whole file memory (OOM)

## Security
- authz check per object; never store secrets/PII in keys/paths; admin access via IAM least

## Evidence
- Object storage semantics (S3-style): SUPPORTED practice
