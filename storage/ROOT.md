# STORAGE (Files & Objects) — ROOT

## Identity
- ID: storage.root
- Domain: storage
- Type: root
- Status: active
- Importance: high (uploads, backups, media, large objects never touch DB blobs)

## Purpose
Where bytes live when not in a DB: object stores (S3/GCS/MinIO), files, signed access, lifecycle, and the rules that avoid "works on disk, breaks in cloud".

## Activation
- uploads/downloads/delivery, building report exports, backups (blob), media, attachments, static/CDN
Statements like "just store it in the DB as blob" — ROBOT veto

## Routing
- serving/upload flow → object-storage.md
- backups → reliability/backups-recovery.md
- static → served by nginx/CDN; media → object storage

## The prime directives
1. **Never BLOB in DB** (except tiny/AES) — DB bloat, backups explode, perf dies (relational/data-modeling: LOB depth)
2. **Object storage** for files: keys namespaced (tenant/prefix), versioning, lifecycle rules, signed URLs
3. **Uploads**: validate size/type at app layer + proxy limit; stream, never read full file into memory
4. **Delivery**: CDN + cache headers; signed URLs for private objects (TTL)
5. **Backup**: storage buckets need own backup policy (lifecycle/versioning), see DR doc
6. **Cost**: storage classes (hot→cold→archive); never forget delete-after retention

## Architectural truths
- Presigned URL patterns: client uploads straight to bucket (no app proxy) — S3 direct OR/Fire; uses tenant prefixes + signed ACL
- Objects > 5GB: multipart uploads; resumable (PlexT)
- Security: bucket ACL never public; policy allows only exact paths; checksums (ETag) verify

## Common failure modes
- files in DB / files on instance disk (lost on redeploy!)
- public bucket (leak + cost) — most common cloud gaffe
- file path encodes user id unescaped (path traversal)
- unbounded uploads (disk/DOS) — quota + mimetype whitelist

## Security gate
- bucket policy least privilege, no public, PII classification per prefix, audit of access

## Evidence
- Storage class selection (block/file/object): INFERRED guideline + SUPPORTED
