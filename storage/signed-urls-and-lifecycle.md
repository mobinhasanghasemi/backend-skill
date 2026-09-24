# Signed URLs and Lifecycle — Object Storage

## Identity
- ID: storage.signed-urls-and-lifecycle
- Domain: storage
- Type: procedure
- Status: active
- Importance: high
- Last Verified: 2026-08

## Purpose
Serve private files (invoices, avatars) without proxying through app: presigned URLs + lifecycle + bucket policy that cannot become public.

## Core Concept
App never streams bytes. It mints a time-boxed signed URL (HMAC over verb+key+expiry) that the client fetches directly from S3/MinIO. Bucket stays private; lifecycle deletes temp objects.

## Activation Conditions
- Private file download/upload, export files, image variants; any `storage/` decision

## Decision Rules
- Use presigned GET (5–15 min) for downloads; presigned POST for uploads with `content-length-range` and `content-type` allowlist.
- Never make bucket public; enforce Block Public Access + bucket policy `Deny` on `s3:GetObject` without valid signature.
- Lifecycle: temp prefix `tmp/` expire 24h; multipart abort after 3d; versioning on for audit, lifecycle on noncurrent versions.

## Security
- Sign with STS-limited role, not root; include `tenant_id` in key (`tenant/{id}/...`) and verify on mint; log mint events; scan uploads with content-type + magic-byte check; S-069.

## Performance
- Presign is local HMAC (µs); no DB; CDN signed cookies for repeated reads if hot.

## Reliability
- Upload: client → presigned POST → S3 event → queue → virus scan → mark ready; retry on 503 with backoff; lifecycle never deletes “ready” prefix.

## Evidence
- S3 presigned/lifecycle VERIFIED via S-069 (accessed 2026-08); pattern SUPPORTED.

## Confidence
VERIFIED

## Verification Status
Reviewed against S3 docs and storage/ROOT.md.

## Code Tiers
<!-- executable -->
```python
# presigned GET (boto3) — app mints, S3 serves
url = s3.generate_presigned_url('get_object',
    Params={'Bucket': bucket, 'Key': f"tenant/{tenant_id}/invoices/{file_id}.pdf"},
    ExpiresIn=600)  # 10 min
```
