"""Seed content: AWS — Modules 2-3 (S3 & Storage, Lambda & Serverless).

Part-file for the SkillForge curriculum seed. All content is original.
Uses frozen dataclasses from app.domain.curriculum.
"""
from __future__ import annotations

from app.domain.curriculum import (
    CurriculumLesson,
    CurriculumModule,
    CurriculumQuestion,
    validate_curriculum_question,
)

DOMAIN_SLUG = "aws"

MODULES = [
    CurriculumModule(
        id="aws-m2",
        domain_slug=DOMAIN_SLUG,
        slug="s3-storage",
        name="S3 & Storage",
        description=(
            "Object storage at any scale: buckets, storage classes, versioning, "
            "lifecycle policies, security, static hosting and presigned URLs, "
            "plus CloudFront CDN."
        ),
        order_index=2,
        estimated_days=7,
    ),
    CurriculumModule(
        id="aws-m3",
        domain_slug=DOMAIN_SLUG,
        slug="lambda-serverless",
        name="Lambda & Serverless",
        description=(
            "Code without servers: Lambda functions, event triggers, API Gateway, "
            "cold starts, limits, Step Functions orchestration and serverless "
            "design patterns."
        ),
        order_index=3,
        estimated_days=7,
    ),
]


def _mkq(qid, lesson_id, module_slug, difficulty, prompt, choices, answer_index,
         explanation, company_tags):
    ch = tuple(choices)
    tags = tuple(company_tags)
    validate_curriculum_question("mcq", prompt, difficulty, ch, answer_index)
    return CurriculumQuestion(
        id=qid,
        domain_slug=DOMAIN_SLUG,
        module_slug=module_slug,
        lesson_id=lesson_id,
        difficulty=difficulty,
        qtype="mcq",
        prompt=prompt,
        choices=ch,
        answer_index=answer_index,
        explanation=explanation,
        company_tags=tags,
    )


# ---------------------------------------------------------------------------
# LESSONS — Module 2: S3 & Storage
# ---------------------------------------------------------------------------

LESSONS = [
    CurriculumLesson(
        id="aws-m2-l1",
        module_id="aws-m2",
        slug="s3-basics",
        title="S3 Basics — Buckets and Objects",
        content="""**S3 (Simple Storage Service)** is object storage: you put files
("objects") into containers ("buckets") and get unlimited scale, 99.999999999%
(11 nines) durability, and pay-per-GB pricing.

```bash
# Create bucket, upload, list
aws s3 mb s3://my-app-assets-2026
aws s3 cp logo.png s3://my-app-assets-2026/images/
aws s3 ls s3://my-app-assets-2026/images/
```

**Core concepts:**
- **Bucket names are globally unique** — `s3://photos` is taken forever.
- **Objects** = data + key (path-like name) + metadata. Max 5 TB per object.
- **Flat namespace**: there are no real folders; `images/logo.png` is just a
  key with slashes. The console fakes folders with prefixes.
- **Eventual consistency** is history — S3 now has **strong read-after-write
  consistency** for all operations.

**S3 vs EBS vs EFS (exam classic):**
| | S3 | EBS | EFS |
|---|---|---|---|
| Type | Object | Block (disk) | File (NFS) |
| Access | HTTP API, anywhere | One EC2, one AZ | Many EC2, multi-AZ |
| Use | Backups, static sites, data lakes | Boot disks, DBs | Shared app storage |

**Interview line:** "S3 for objects at planet scale, EBS for a server's disk,
EFS for shared POSIX files.""",
        order_index=1,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m2-l2",
        module_id="aws-m2",
        slug="storage-classes",
        title="S3 Storage Classes",
        content="""Not all data is equal — S3 charges less the slower you can
tolerate retrieval:

- **Standard** — frequent access; 11 nines durability.
- **Intelligent-Tiering** — auto-moves objects between frequent/infrequent
  tiers based on access patterns (small monitoring fee, no retrieval fee).
- **Standard-IA** — infrequent access, cheaper storage, retrieval fee.
- **One Zone-IA** — single AZ (less durable); reproducible data only.
- **Glacier Instant / Flexible / Deep Archive** — archive tiers; retrieval
  from milliseconds to 48 hours, cheapest storage on AWS.

```bash
# Upload straight to Infrequent Access
aws s3 cp backup.tar s3://my-bucket/ --storage-class STANDARD_IA
```

**Exam trap:** "cheapest storage for 7-year compliance logs never read" →
**Glacier Deep Archive** ($0.00099/GB-month). "Frequently accessed user
uploads" → Standard or Intelligent-Tiering.

**S3 Express One Zone** is the odd one: single-digit millisecond latency,
but single AZ — for latency-critical temp data, not durability.""",
        order_index=2,
        estimated_minutes=25,
    ),
    CurriculumLesson(
        id="aws-m2-l3",
        module_id="aws-m2",
        slug="versioning",
        title="Versioning & MFA Delete",
        content="""Enable **versioning** on a bucket and S3 keeps every version of
every object. Overwrite `report.pdf` and the old copy survives with a
version ID; "delete" just adds a **delete marker** (the data is still there).

```bash
aws s3api put-bucket-versioning --bucket my-bucket \\
  --versioning-configuration Status=Enabled
# List all versions, including delete markers
aws s3api list-object-versions --bucket my-bucket
```

**Why it matters:**
- Accidental overwrite/delete → restore the previous version in seconds.
- Required for **cross-region replication** and many compliance regimes.
- **MFA Delete** adds a hardware-token requirement to permanently delete
  versions — the ransomware/backdoor-admin defense.

**Costs:** every version is billed separately. A 1 GB file overwritten daily
for a year = 365 GB billed. Pair versioning with **lifecycle rules** that
expire noncurrent versions after N days.""",
        order_index=3,
        estimated_minutes=20,
    ),
    CurriculumLesson(
        id="aws-m2-l4",
        module_id="aws-m2",
        slug="lifecycle",
        title="Lifecycle Policies",
        content="""**Lifecycle rules** automate the data's journey: hot → cool →
archive → delete, with zero human toil.

```json
{
  "Rules": [{
    "ID": "logs-rule", "Status": "Enabled",
    "Filter": {"Prefix": "logs/"},
    "Transitions": [
      {"Days": 30, "StorageClass": "STANDARD_IA"},
      {"Days": 90, "StorageClass": "GLACIER"}
    ],
    "Expiration": {"Days": 365}
  }]
}
```

**Rules of the game:**
- Transitions have **minimum days**: 30 before Standard-IA/One-Zone-IA,
  and objects must live 30 days in IA before Glacier.
- Small objects (<128 KB) should not transition — minimum billable size
  makes it pointless.
- **Intelligent-Tiering** can replace hand-written rules for unpredictable
  access patterns.

**Interview answer:** "Lifecycle policies move data to cheaper classes on a
schedule and expire it — the set-and-forget cost optimizer.""",
        order_index=4,
        estimated_minutes=20,
    ),
    CurriculumLesson(
        id="aws-m2-l5",
        module_id="aws-m2",
        slug="s3-security",
        title="S3 Security — Policies and Access",
        content="""S3 breaches are almost always **misconfiguration**, not AWS bugs.
The controls:

1. **Block Public Access** (account + bucket level) — the big red switch.
   Leave it ON unless you truly need public reads.
2. **Bucket policies** — JSON attached to the bucket (who can do what).
3. **IAM policies** — attached to users/roles.
4. **ACLs** — legacy, avoid; disable with Object Ownership = BucketOwnerEnforced.
5. **Encryption**: SSE-S3 (AWS keys), SSE-KMS (your keys, audit trail),
   SSE-C (you bring keys), or client-side.

```json
// Bucket policy: HTTPS only
{"Effect": "Deny", "Principal": "*",
 "Action": "s3:*",
 "Resource": ["arn:aws:s3:::my-bucket/*"],
 "Condition": {"Bool": {"aws:SecureTransport": "false"}}}
```

**Evaluation logic (exam):** explicit **Deny beats any Allow**; default is
implicit deny. A request needs an Allow from *somewhere* and no Deny
*anywhere* (bucket policy, IAM, SCP, ACL).

**Presigned URLs** (next lesson) are the safe way to grant temporary access
without making anything public.""",
        order_index=5,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m2-l6",
        module_id="aws-m2",
        slug="static-hosting",
        title="Static Website Hosting & CloudFront",
        content="""S3 can host a static site directly — HTML/CSS/JS, no servers:

```bash
aws s3 website s3://my-site --index-document index.html \\
  --error-document error.html
aws s3 sync ./build s3://my-site
```

**But production sites add CloudFront**, AWS's CDN:
- **Edge locations** (400+ PoPs) cache content near users → fast globally.
- **Origin** can be S3, ALB, or any HTTP server.
- **OAC (Origin Access Control)** lets CloudFront read a *private* bucket —
  users can never hit S3 directly.
- Signed URLs/cookies for premium content.

**Cache behavior:** CloudFront caches by default; invalidate with
`create-invalidation` on deploy (`/*` costs after 1,000 free paths/month —
version your filenames instead: `app.v2.js`).

**Exam pattern:** "Global users, static content, HTTPS, private S3" →
**CloudFront + OAC + S3**. Every time.""",
        order_index=6,
        estimated_minutes=25,
    ),
    CurriculumLesson(
        id="aws-m2-l7",
        module_id="aws-m2",
        slug="presigned-urls",
        title="Presigned URLs & Multipart Upload",
        content="""A **presigned URL** grants temporary access to a private object —
no bucket policy changes, no IAM user for the downloader.

```python
# Python: URL valid 1 hour for one private object
url = s3.generate_presigned_url(
    "get_object",
    Params={"Bucket": "my-bucket", "Key": "invoice.pdf"},
    ExpiresIn=3600,
)
```

**Classic use case:** user uploads a profile photo *directly* to S3 —
backend generates a presigned **PUT** URL, browser uploads straight to S3,
backend never proxies gigabytes.

**Multipart upload** is for big files: split into parts (5 MB–5 GB each),
upload in parallel, S3 reassembles. Required for objects >100 MB via
console; the CLI does it automatically. Abort incomplete uploads with a
lifecycle rule or you pay for orphaned parts forever.

**S3 Transfer Acceleration** routes uploads through CloudFront edge
locations — big win for distant users uploading large files.""",
        order_index=7,
        estimated_minutes=25,
    ),
    # ---------------- Module 3: Lambda & Serverless ----------------
    CurriculumLesson(
        id="aws-m3-l1",
        module_id="aws-m3",
        slug="lambda-basics",
        title="Lambda — Functions Without Servers",
        content="""**Lambda** runs your code when something happens — no servers to
provision, patch, or pay for when idle. You pay per request + GB-seconds.

```python
# lambda_function.py — S3 event triggers thumbnail creation
import boto3
def lambda_handler(event, context):
    key = event["Records"][0]["s3"]["object"]["key"]
    print(f"New file: {key}")   # CloudWatch Logs picks this up
    return {"statusCode": 200}
```

```bash
aws lambda create-function --function-name thumbs \\
  --runtime python3.12 --role arn:aws:iam::123:role/lambda-role \\
  --handler lambda_function.lambda_handler \\
  --zip-file fileb://function.zip --timeout 30 --memory-size 512
```

**Key facts:**
- **Runtimes**: Python, Node, Java, Go, .NET, Ruby, custom.
- **Triggers**: S3, API Gateway, SQS, SNS, EventBridge (cron!), DynamoDB
  Streams, Kinesis.
- **15-minute max** execution; 10 GB memory; 250 MB deployment package
  (50 MB zipped direct, else S3).
- **/tmp** gives 512 MB–10 GB of ephemeral disk per invocation.

**Mental model:** Lambda = "run this function when X happens, bill me for
milliseconds used." Perfect for event-driven glue, APIs, and cron jobs.""",
        order_index=1,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m3-l2",
        module_id="aws-m3",
        slug="lambda-triggers",
        title="Lambda Event Sources & Triggers",
        content="""Lambda never polls — **event source mappings** push or pull
events into your function:

**Push (Lambda is invoked directly):** S3, SNS, API Gateway, EventBridge,
CloudWatch Alarms. The service calls Lambda; retries are the service's job.

**Pull (Lambda polls for you):** SQS, Kinesis, DynamoDB Streams, MSK. Lambda
long-polls the source; you configure **batch size** and **batch window**.

```bash
# SQS trigger: batches of up to 10 messages, 5s window
aws lambda create-event-source-mapping \\
  --function-name orders --event-source-arn arn:aws:sqs:...:orders-queue \\
  --batch-size 10 --maximum-batching-window-in-seconds 5
```

**Failure handling (interview gold):**
- **Async invocations** retry twice, then go to the **DLQ** (dead-letter
  queue) or on-failure destination.
- **SQS triggers**: failed batches return to the queue; after
  **maxReceiveCount**, messages move to the DLQ. Set the queue's
  **visibility timeout ≥ 6× Lambda timeout**.
- **Idempotency**: retries mean your function may run twice — design for it
  (DynamoDB conditional writes are the classic guard).

**EventBridge Scheduler / cron:** `rate(5 minutes)` or cron expressions —
the serverless cron replacement.""",
        order_index=2,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m3-l3",
        module_id="aws-m3",
        slug="api-gateway",
        title="API Gateway — Serverless Front Door",
        content="""**API Gateway** turns Lambda functions into real HTTPS APIs with
routing, auth, throttling, and caching.

```bash
# HTTP API (cheap, fast) vs REST API (full features)
aws apigatewayv2 create-api --name orders-api --protocol-type HTTP \\
  --target arn:aws:lambda:...:function:orders
```

**Two flavors:**
- **HTTP API** — 70% cheaper, lower latency; JWT/OAuth authorizers. Enough
  for most.
- **REST API** — usage plans + API keys, request validation, WAF
  integration, private endpoints.

**Stages** (`dev`, `prod`) version your API; **throttling** (default
10,000 rps) and **usage plans** protect backends from abuse. **Caching**
($$$) can slash Lambda invocations for hot GETs.

**Auth options:** IAM, Lambda authorizers (custom logic), Cognito user
pools, JWT. For service-to-service, IAM auth with SigV4 is the AWS-native
choice.

**Exam line:** "API Gateway + Lambda + DynamoDB" is the canonical
serverless web app — know it cold.""",
        order_index=3,
        estimated_minutes=25,
    ),
    CurriculumLesson(
        id="aws-m3-l4",
        module_id="aws-m3",
        slug="cold-starts",
        title="Cold Starts & Performance Tuning",
        content="""A **cold start** happens when Lambda must spin up a fresh
execution environment: download code, boot runtime, run init code. It adds
100ms–seconds of latency to that first request.

**What makes cold starts worse:** VPC attachment (ENI setup — much better
now with Hyperplane), large packages, Java/.NET runtimes, high memory
*reduces* it (more CPU allocated proportionally!).

**Mitigations:**
1. **Provisioned Concurrency** — keep N environments warm, always. Costs
   money even idle; the only guaranteed fix.
2. **Keep functions warm** — scheduled pings (hacky, works for low stakes).
3. **Shrink the package** — layers for deps, tree-shake, prefer Python/Node.
4. **SnapStart (Java)** — pre-initialized snapshots, near-zero cold starts.

```bash
aws lambda put-provisioned-concurrency-config \\
  --function-name checkout --qualifier prod \\
  --provisioned-concurrent-executions 10
```

**Memory tuning is free performance:** Lambda allocates CPU proportionally
to memory. Doubling memory from 512 MB to 1 GB often *halves* duration —
test with AWS Lambda Power Tuning (open-source Step Functions app).

**Interview takeaway:** "Cold starts hit latency-sensitive APIs; fix with
provisioned concurrency or SnapStart, and right-size memory — it buys CPU
too." """,
        order_index=4,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m3-l5",
        module_id="aws-m3",
        slug="lambda-limits",
        title="Lambda Limits & Quotas",
        content="""Know the hard numbers — interviews love them:

| Limit | Value |
|---|---|
| Max execution time | **15 minutes** |
| Memory | 128 MB – **10 GB** |
| Ephemeral storage (/tmp) | 512 MB – 10 GB |
| Deployment package | 50 MB zipped / **250 MB** unzipped |
| Concurrent executions (default) | **1,000** per region |
| Environment variables | 4 KB |

**Hitting the 15-minute wall?** You are using the wrong tool:
- Long batch → **Fargate/ECS** or EC2.
- Fan-out work → **SQS + Lambda** (each message = fresh 15 min).
- Orchestration → **Step Functions**.

**Concurrency:** the 1,000 default is a soft limit (raise via support).
**Reserved concurrency** caps a function (protect downstream DBs from
thundering herds); **provisioned concurrency** pre-warms.

**Layers** share code across functions (up to 5 layers, 250 MB total
unzipped with function code). Great for `boto3` upgrades, ffmpeg binaries,
or company SDKs.""",
        order_index=5,
        estimated_minutes=20,
    ),
    CurriculumLesson(
        id="aws-m3-l6",
        module_id="aws-m3",
        slug="step-functions",
        title="Step Functions — Serverless Orchestration",
        content="""**Step Functions** coordinate multi-step workflows as visual
**state machines** — no callback hell, with retries, branching, and human
approval steps built in.

```json
{
  "StartAt": "ProcessPayment",
  "States": {
    "ProcessPayment": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:...:function:pay",
      "Retry": [{"ErrorEquals": ["States.ALL"], "MaxAttempts": 3}],
      "Catch": [{"ErrorEquals": ["States.ALL"], "Next": "Refund"}],
      "Next": "ShipOrder"
    },
    "ShipOrder": {"Type": "Task",
      "Resource": "arn:aws:lambda:...:function:ship", "End": true},
    "Refund": {"Type": "Task",
      "Resource": "arn:aws:lambda:...:function:refund", "End": true}
  }
}
```

**Two flavors:**
- **Standard** — long-running (up to 1 year), exactly-once, billed per
  state transition. Order processing, ETL.
- **Express** — high-volume, short (5 min), at-least-once, per-invocation
  pricing. IoT ingestion, streaming.

**Why not just chain Lambdas?** Step Functions gives you a visual audit
trail, automatic retries with backoff, parallel branches, wait states, and
human-approval pauses — things you would hand-roll badly.

**SAA pattern:** "order → pay → ship, with rollback on failure" → Step
Functions Standard orchestrating Lambda tasks.""",
        order_index=6,
        estimated_minutes=25,
    ),
    CurriculumLesson(
        id="aws-m3-l7",
        module_id="aws-m3",
        slug="serverless-patterns",
        title="Serverless Design Patterns",
        content="""Putting it together — the patterns that recur in interviews:

**1. API + async worker:** API Gateway → Lambda (validate, 200 OK fast) →
SQS → worker Lambda. The user never waits for slow work.

**2. Fan-out:** SNS topic → N Lambda subscribers (thumbnails, search index,
notifications all react to one upload).

**3. EventBridge bus:** decoupled microservices publish events
(`order.placed`); consumers subscribe without knowing producers.

**4. Saga (distributed transactions):** Step Functions orchestrates
reserve-inventory → charge-card → ship, with compensating actions on
failure. No 2PC in serverless.

**5. Strangler fig:** API Gateway routes old paths to the monolith, new
paths to Lambda — migrate incrementally.

**Anti-patterns to name-drop:**
- Lambda calling Lambda synchronously (double billing, tight coupling).
- 15-minute ETL crammed into one function (use Fargate/Step Functions).
- Recursive S3 → Lambda → S3 loops (infinite billing — set up
  CloudWatch billing alarms!).

**Cost truth:** serverless is cheap at low scale and can surprise at high
scale — always model requests × duration vs. an always-on alternative.""",
        order_index=7,
        estimated_minutes=30,
    ),
]


def _q(qid, lid, mslug, diff, prompt, choices, ans, expl, tags):
    return _mkq(qid, lid, mslug, diff, prompt, choices, ans, expl, tags)


QUESTIONS = [
    # ================= M2: S3 =================
    # ---- L1: s3-basics ----
    _q("aws-m2-l1-q1", "aws-m2-l1", "s3-storage", 1,
       "What is Amazon S3?",
       ["Virtual servers", "Object storage for files at massive scale",
        "A relational database", "A CDN"],
       1, "S3 = Simple Storage Service: buckets hold objects (files), "
          "unlimited scale, 11-nines durability.",
       ("tcs", "infosys", "wipro")),
    _q("aws-m2-l1-q2", "aws-m2-l1", "s3-storage", 2,
       "S3 bucket names must be:",
       ["Unique per region", "Globally unique across all AWS accounts",
        "Unique per AZ", "Anything — duplicates allowed"],
       1, "Bucket names live in a single global namespace — s3://photos is "
          "taken forever, by anyone.",
       ("amazon", "accenture")),
    _q("aws-m2-l1-q3", "aws-m2-l1", "s3-storage", 3,
       "Maximum size of a single S3 object?",
       ["5 GB", "5 TB", "1 TB", "Unlimited"],
       1, "5 TB per object (via multipart upload). Single PUT caps at 5 GB.",
       ("amazon", "tcs")),
    _q("aws-m2-l1-q4", "aws-m2-l1", "s3-storage", 5,
       "You need shared POSIX file storage mounted on 20 EC2 instances across AZs. Which service?",
       ["S3", "EBS", "EFS", "Instance store"],
       2, "EFS = managed NFS, multi-AZ, many-to-one. S3 is object (no POSIX), "
          "EBS is one-instance-one-AZ.",
       ("amazon", "flipkart", "microsoft")),
    _q("aws-m2-l1-q5", "aws-m2-l1", "s3-storage", 7,
       "S3 consistency model today?",
       ["Eventual for all ops", "Strong read-after-write consistency for all operations",
        "Strong only for new objects", "Depends on region"],
       1, "Since Dec 2020, S3 offers strong consistency for PUT/DELETE/LIST — "
          "no more eventual-consistency workarounds.",
       ("amazon", "atlassian")),
    _q("aws-m2-l1-q6", "aws-m2-l1", "s3-storage", 9,
       "A data lake needs: cheap storage, SQL queries in place, ML access. Best combo?",
       ["EBS + RDS", "S3 + Athena (serverless SQL) + SageMaker",
        "EFS + EC2", "DynamoDB only"],
       1, "S3 as the lake + Athena for ad-hoc SQL + SageMaker/EMR for ML is "
          "the canonical AWS analytics stack.",
       ("amazon", "swiggy", "dream11")),
    # ---- L2: storage-classes ----
    _q("aws-m2-l2-q1", "aws-m2-l2", "s3-storage", 1,
       "Cheapest S3 class for 7-year compliance archives never read?",
       ["Standard", "Glacier Deep Archive", "Intelligent-Tiering", "One Zone-IA"],
       1, "Deep Archive ≈ $0.00099/GB-month, retrieval in ~12-48h. Built for "
          "write-once compliance data.",
       ("tcs", "infosys")),
    _q("aws-m2-l2-q2", "aws-m2-l2", "s3-storage", 2,
       "What does S3 Intelligent-Tiering do?",
       ["Encrypts automatically", "Auto-moves objects between access tiers based on usage patterns",
        "Replicates globally", "Compresses objects"],
       1, "No manual rules: it watches access patterns and shifts objects "
          "frequently↔infrequently accessed tiers.",
       ("amazon", "accenture", "hcl")),
    _q("aws-m2-l2-q3", "aws-m2-l2", "s3-storage", 3,
       "Key risk of S3 One Zone-IA?",
       ["Higher cost", "Data lives in ONE AZ — AZ loss = data loss",
        "No versioning", "Slower uploads"],
       1, "One Zone-IA trades durability (single AZ) for ~20% savings. Only "
          "for easily reproducible data.",
       ("amazon", "wipro")),
    _q("aws-m2-l2-q4", "aws-m2-l2", "s3-storage", 5,
       "Retrieval times: Standard (ms), Glacier Flexible (minutes-hours), Deep Archive?",
       ["Milliseconds", "Seconds", "~12-48 hours", "1 week"],
       2, "Deep Archive retrieval: 12h standard, 48h bulk. Plan restores ahead "
          "— it is not for urgent access.",
       ("amazon", "tcs", "cognizant")),
    _q("aws-m2-l2-q5", "aws-m2-l2", "s3-storage", 7,
       "Why shouldn't 10 KB objects transition to Glacier?",
       ["Not allowed", "128 KB minimum billable size — tiny objects cost MORE in Glacier",
        "Too slow", "Encryption unsupported"],
       1, "S3 bills transitioned objects at minimum sizes/durations. Small "
          "objects in Glacier can cost more than Standard.",
       ("amazon", "microsoft")),
    _q("aws-m2-l2-q6", "aws-m2-l2", "s3-storage", 9,
       "Millions of objects, unpredictable access, must minimize cost without manual rules. Pick?",
       ["Standard", "Intelligent-Tiering (Archive tiers optional)",
        "Glacier Instant", "One Zone-IA"],
       1, "Intelligent-Tiering automates the whole lifecycle; enable the "
          "optional Archive tiers for deep savings on cold data.",
       ("amazon", "atlassian", "phonepe")),
    # ---- L3: versioning ----
    _q("aws-m2-l3-q1", "aws-m2-l3", "s3-storage", 1,
       "What does S3 versioning protect against?",
       ["DDoS", "Accidental overwrite/delete — every version is kept",
        "Slow uploads", "High bills"],
       1, "With versioning, overwrites create new versions and deletes add "
          "delete markers — nothing is truly gone.",
       ("tcs", "infosys")),
    _q("aws-m2-l3-q2", "aws-m2-l3", "s3-storage", 2,
       "You 'deleted' a file in a versioned bucket but need it back. What happened?",
       ["It's gone forever", "Only a delete marker was added — delete the marker to restore",
        "Check Glacier", "Contact AWS support"],
       1, "Deletes in versioned buckets are soft. Remove the delete marker and "
          "the object reappears.",
       ("amazon", "accenture")),
    _q("aws-m2-l3-q3", "aws-m2-l3", "s3-storage", 3,
       "What does MFA Delete add?",
       ["Faster deletes", "Requires an MFA token to permanently delete object versions",
        "Cheaper storage", "Auto-backup"],
       1, "MFA Delete demands a hardware token for version deletion — defense "
          "against rogue admins and ransomware.",
       ("amazon", "hcl", "wipro")),
    _q("aws-m2-l3-q4", "aws-m2-l3", "s3-storage", 5,
       "Versioning is ON. A 1 GB file is overwritten daily for a year. Billed storage?",
       ["1 GB", "~365 GB — every version is billed",
        "12 GB", "Free"],
       1, "Each version is a full billed object. Pair versioning with lifecycle "
          "rules expiring noncurrent versions.",
       ("amazon", "tcs", "deloitte")),
    _q("aws-m2-l3-q5", "aws-m2-l3", "s3-storage", 7,
       "Which S3 feature REQUIRES versioning to be enabled?",
       ["Static hosting", "Cross-region replication (CRR)", "Presigned URLs", "Lifecycle rules"],
       1, "CRR replicates versions — it cannot work without versioning on both "
          "source and destination buckets.",
       ("amazon", "microsoft", "oracle")),
    _q("aws-m2-l3-q6", "aws-m2-l3", "s3-storage", 9,
       "Compliance: 'no object version may ever be deleted, even by admins.' How?",
       ["MFA Delete", "S3 Object Lock (Compliance mode) — WORM, not even root can delete early",
        "Versioning", "Bucket policy deny"],
       1, "Object Lock Compliance mode = true WORM. MFA Delete still allows "
          "deletion with a token; Compliance mode does not.",
       ("amazon", "cred", "atlassian")),
    # ---- L4: lifecycle ----
    _q("aws-m2-l4-q1", "aws-m2-l4", "s3-storage", 1,
       "What do S3 lifecycle policies do?",
       ["Encrypt data", "Auto-transition objects to cheaper classes and expire them on schedule",
        "Replicate buckets", "Speed up uploads"],
       1, "Set-and-forget rules: 30d → IA, 90d → Glacier, 365d → delete, for "
          "example.",
       ("tcs", "infosys")),
    _q("aws-m2-l4-q2", "aws-m2-l4", "s3-storage", 2,
       "Minimum days before an object can transition to Standard-IA?",
       ["0", "30 days", "90 days", "1 year"],
       1, "30 days in Standard before IA/One-Zone-IA; then 30 more before "
          "Glacier. Small objects exempt from benefit.",
       ("amazon", "accenture")),
    _q("aws-m2-l4-q3", "aws-m2-l4", "s3-storage", 3,
       "Your lifecycle rule isn't moving 50 KB log files to Glacier. Why?",
       ["Glacier is full", "Objects under 128 KB aren't worth transitioning (minimum billable size)",
        "Logs can't transition", "Need versioning"],
       1, "Minimum billable object size for Glacier transitions is 128 KB — "
          "aggregate small logs first.",
       ("amazon", "wipro")),
    _q("aws-m2-l4-q4", "aws-m2-l4", "s3-storage", 5,
       "Unpredictable access patterns across 10M objects, no ops team to tune rules. Best?",
       ["Manual lifecycle rules", "S3 Intelligent-Tiering", "Glacier Deep Archive", "Standard"],
       1, "Intelligent-Tiering replaces hand-tuned rules with automatic tiering "
          "driven by actual access.",
       ("amazon", "flipkart", "swiggy")),
    _q("aws-m2-l4-q5", "aws-m2-l4", "s3-storage", 7,
       "How do you stop paying for failed multipart upload parts?",
       ["Nothing — they're free", "Lifecycle rule aborting incomplete multipart uploads after N days",
        "Delete the bucket", "Contact support"],
       1, "Aborted/failed multipart parts linger and bill. A lifecycle "
          "abort rule cleans them automatically.",
       ("amazon", "microsoft", "tcs")),
    _q("aws-m2-l4-q6", "aws-m2-l4", "s3-storage", 9,
       "Design a 7-year log retention: hot 30d, warm 1y, archive after, delete at 7y. Rule sketch?",
       ["One rule: expire at 7y", "Transitions: 30d→IA, 365d→Glacier, expiration 2555d — plus noncurrent-version expirations",
        "Manual moves", "Two buckets"],
       1, "Layer transitions + final expiration, and don't forget noncurrent "
          "versions if versioning is on.",
       ("amazon", "deloitte", "atlassian")),
    # ---- L5: s3-security ----
    _q("aws-m2-l5-q1", "aws-m2-l5", "s3-storage", 1,
       "First thing to check when an S3 bucket leaks data publicly?",
       ["Encryption", "Block Public Access + bucket policy allowing public reads",
        "Versioning", "Lifecycle rules"],
       1, "Nearly all S3 leaks are public-read bucket policies/ACLs. Block "
          "Public Access is the master switch.",
       ("tcs", "infosys", "wipro")),
    _q("aws-m2-l5-q2", "aws-m2-l5", "s3-storage", 2,
       "Bucket policy allows s3:GetObject for *, IAM policy denies it. A user requests an object. Result?",
       ["Allowed (bucket wins)", "Denied — explicit deny anywhere beats any allow",
        "Allowed (IAM wins)", "Depends on region"],
       1, "Evaluation: default implicit deny → need an allow somewhere → any "
          "explicit deny anywhere vetoes.",
       ("amazon", "accenture", "hcl")),
    _q("aws-m2-l5-q3", "aws-m2-l5", "s3-storage", 3,
       "SSE-KMS vs SSE-S3 — what does KMS add?",
       ["Speed", "Customer-controlled keys with CloudTrail audit of every decrypt",
        "Lower cost", "Bigger objects"],
       1, "SSE-S3 uses AWS-managed keys (free, simple). SSE-KMS gives you key "
          "control, rotation, and an audit trail.",
       ("amazon", "microsoft", "cognizant")),
    _q("aws-m2-l5-q4", "aws-m2-l5", "s3-storage", 5,
       "Force all S3 traffic to use HTTPS. How?",
       ["VPC endpoint", "Bucket policy denying s3:* when aws:SecureTransport is false",
        "Enable versioning", "Use CloudFront"],
       1, "A Deny with Bool SecureTransport=false blocks plain HTTP while "
          "allowing HTTPS — the textbook pattern.",
       ("amazon", "tcs", "phonepe")),
    _q("aws-m2-l5-q5", "aws-m2-l5", "s3-storage", 7,
       "Modern replacement for S3 ACLs?",
       ["Nothing", "Bucket policies + IAM, with Object Ownership set to BucketOwnerEnforced (ACLs disabled)",
        "More ACLs", "NACLs"],
       1, "AWS recommends disabling ACLs entirely and using policies — simpler, "
          "auditable, less foot-gun.",
       ("amazon", "atlassian", "cred")),
    _q("aws-m2-l5-q6", "aws-m2-l5", "s3-storage", 9,
       "Cross-account: Account B's role must read Account A's bucket. Minimum setup?",
       ["Make bucket public", "Bucket policy on A allowing B's role + IAM policy on B's role allowing s3:GetObject",
        "IAM policy only", "Bucket policy only"],
       1, "Cross-account needs BOTH sides: resource policy (bucket) trusting B, "
          "and identity policy (role) permitting the action.",
       ("amazon", "oracle", "deloitte")),
    # ---- L6: static-hosting ----
    _q("aws-m2-l6-q1", "aws-m2-l6", "s3-storage", 1,
       "Can S3 host a website?",
       ["No", "Yes — static sites (HTML/CSS/JS), no server code",
        "Yes — including PHP", "Only with EC2"],
       1, "S3 static hosting serves static assets. Dynamic backends need "
          "Lambda/EC2 behind it.",
       ("tcs", "infosys")),
    _q("aws-m2-l6-q2", "aws-m2-l6", "s3-storage", 2,
       "Why put CloudFront in front of S3 for a global site?",
       ["Cheaper storage", "Edge caching near users = fast worldwide + HTTPS + DDoS protection",
        "Bigger buckets", "More regions"],
       1, "CloudFront's 400+ edge locations cache content close to users and "
          "add TLS/WAF/Shield.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m2-l6-q3", "aws-m2-l6", "s3-storage", 3,
       "How should CloudFront access a PRIVATE S3 bucket?",
       ["Bucket public", "Origin Access Control (OAC) — CloudFront gets access, users can't hit S3 directly",
        "Presigned URLs only", "IAM user keys in CloudFront"],
       1, "OAC (successor to OAI) grants the distribution — and only the "
          "distribution — read access.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m2-l6-q4", "aws-m2-l6", "s3-storage", 5,
       "After deploy, some users see the old JS bundle. Cheapest reliable fix?",
       ["Invalidate /* every deploy", "Version filenames (app.v2.js) so each deploy is a new cache key",
        "Disable caching", "Bigger TTL"],
       1, "Invalidations cost after 1,000 free/month and take minutes. "
          "Fingerprinted filenames make caching correct by construction.",
       ("amazon", "flipkart", "swiggy")),
    _q("aws-m2-l6-q5", "aws-m2-l6", "s3-storage", 7,
       "Serve premium video to paying users only via CloudFront. How?",
       ["Public bucket", "Signed URLs / signed cookies — time-limited, validated at the edge",
        "IP whitelist", "Basic auth"],
       1, "CloudFront signed URLs/cookies embed expiry + policy; the origin "
          "stays private.",
       ("amazon", "microsoft", "hotstar")),
    _q("aws-m2-l6-q6", "aws-m2-l6", "s3-storage", 9,
       "Multi-region active-active static site with failover. Architecture?",
       ["One bucket", "S3 CRR to second region + CloudFront origin group (primary/failover) + Route 53 health checks",
        "Two CloudFronts", "EC2 instead"],
       1, "Replicate the bucket, let CloudFront fail over between origins, "
          "Route 53 handles DNS-level health.",
       ("amazon", "atlassian", "phonepe")),
    # ---- L7: presigned-urls ----
    _q("aws-m2-l7-q1", "aws-m2-l7", "s3-storage", 1,
       "What is a presigned URL?",
       ["A permanent public link", "A time-limited URL granting temporary access to a private object",
        "A shortened URL", "A CDN link"],
       1, "Signed with your credentials, expiring in minutes/hours — share "
          "private files without opening the bucket.",
       ("tcs", "infosys")),
    _q("aws-m2-l7-q2", "aws-m2-l7", "s3-storage", 2,
       "Best pattern for user profile-photo uploads?",
       ["Server receives file, uploads to S3", "Backend issues presigned PUT URL; browser uploads directly to S3",
        "Public bucket", "Email the photo"],
       1, "Direct-to-S3 via presigned URL: backend never proxies bytes, scales "
          "infinitely, cheaper.",
       ("amazon", "accenture", "swiggy")),
    _q("aws-m2-l7-q3", "aws-m2-l7", "s3-storage", 3,
       "Uploading a 20 GB video via S3. Which feature?",
       ["Single PUT", "Multipart upload — parallel parts, resume, required at scale",
        "Presigned URL only", "Glacier"],
       1, "Multipart splits into parallel parts with per-part retry; console "
          "auto-uses it above ~100 MB.",
       ("amazon", "wipro", "hcl")),
    _q("aws-m2-l7-q4", "aws-m2-l7", "s3-storage", 5,
       "A user in Australia uploads slowly to your Mumbai bucket. Fix?",
       ["Bigger bucket", "S3 Transfer Acceleration — upload via CloudFront edge network",
        "More IAM users", "Glacier"],
       1, "Transfer Acceleration routes through the nearest edge PoP over "
          "optimized AWS backbone — huge for long distances.",
       ("amazon", "tcs", "atlassian")),
    _q("aws-m2-l7-q5", "aws-m2-l7", "s3-storage", 7,
       "Can a presigned URL grant MORE permission than the signer has?",
       ["Yes", "No — it can only delegate a subset of the signer's own permissions",
        "Yes, with MFA", "Only for GET"],
       1, "Signing credentials bound the URL. A reader cannot mint a writer URL.",
       ("amazon", "microsoft", "cred")),
    _q("aws-m2-l7-q6", "aws-m2-l7", "s3-storage", 9,
       "Orphaned multipart parts are silently billing $400/month. Permanent fix?",
       ["Manual cleanup monthly", "Lifecycle rule: abort incomplete multipart uploads after 7 days",
        "Disable multipart", "Smaller files"],
       1, "Failed/interrupted multiparts leave billable parts. The abort rule "
          "is the set-and-forget fix.",
       ("amazon", "razorpay", "deloitte")),
    # ================= M3: Lambda =================
    # ---- L1: lambda-basics ----
    _q("aws-m3-l1-q1", "aws-m3-l1", "lambda-serverless", 1,
       "What is AWS Lambda?",
       ["Virtual servers", "Run code without provisioning servers — pay per request + compute time",
        "A database", "A CDN"],
       1, "Serverless functions: upload code, set a trigger, AWS runs it and "
          "bills milliseconds used.",
       ("tcs", "infosys", "wipro")),
    _q("aws-m3-l1-q2", "aws-m3-l1", "lambda-serverless", 2,
       "Maximum execution time of a Lambda function?",
       ["5 minutes", "15 minutes", "1 hour", "No limit"],
       1, "15 minutes hard cap. Longer work → Fargate/EC2, Step Functions, or "
          "fan-out via SQS.",
       ("amazon", "accenture")),
    _q("aws-m3-l1-q3", "aws-m3-l1", "lambda-serverless", 3,
       "Where does print()/console.log() output go?",
       ["Nowhere", "CloudWatch Logs — automatic log group per function",
        "S3", "Email"],
       1, "Lambda streams stdout to CloudWatch Logs. No logging setup needed.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m3-l1-q4", "aws-m3-l1", "lambda-serverless", 5,
       "Your function needs 10 GB of temp scratch space. Possible?",
       ["No — 512 MB fixed", "Yes — /tmp scales to 10 GB ephemeral storage",
        "Only with EBS", "Only with EFS"],
       1, "/tmp is configurable 512 MB–10 GB (ephemeral). For persistent "
          "shared files, mount EFS.",
       ("amazon", "flipkart", "dream11")),
    _q("aws-m3-l1-q5", "aws-m3-l1", "lambda-serverless", 7,
       "How does Lambda get permissions to write to DynamoDB?",
       ["Root keys in code", "An IAM execution role attached to the function",
        "Bucket policy", "It has full access by default"],
       1, "Every function assumes an execution role. Least privilege: only "
          "the DynamoDB actions it needs.",
       ("amazon", "microsoft", "phonepe")),
    _q("aws-m3-l1-q6", "aws-m3-l1", "lambda-serverless", 9,
       "Two teams share one AWS account. How do you prevent Team A's functions from reading Team B's secrets?",
       ["Nothing needed", "IAM roles per function + resource policies + separate KMS keys per team",
        "Separate regions", "Bigger functions"],
       1, "Defense in depth: least-privilege execution roles, secret ARNs "
          "scoped per team, KMS key policies.",
       ("amazon", "cred", "atlassian")),
    # ---- L2: lambda-triggers ----
    _q("aws-m3-l2-q1", "aws-m3-l2", "lambda-serverless", 1,
       "Which can trigger a Lambda function?",
       ["Only API Gateway", "S3, SQS, API Gateway, EventBridge, DynamoDB Streams, and more",
        "Only CloudWatch", "Only manually"],
       1, "Dozens of event sources. Push (S3/SNS) invoke directly; pull (SQS/"
          "Kinesis) are polled by Lambda.",
       ("tcs", "infosys")),
    _q("aws-m3-l2-q2", "aws-m3-l2", "lambda-serverless", 2,
       "SQS-triggered Lambda: where do repeatedly failing messages go?",
       ["Deleted", "Dead-letter queue after maxReceiveCount",
        "CloudWatch", "They retry forever"],
       1, "Configure a DLQ on the source queue; poison messages land there "
          "for inspection instead of looping.",
       ("amazon", "accenture", "swiggy")),
    _q("aws-m3-l2-q3", "aws-m3-l2", "lambda-serverless", 3,
       "SQS visibility timeout vs Lambda timeout — safe rule?",
       ["Equal", "Visibility timeout ≥ 6× Lambda timeout",
        "Visibility < timeout", "Doesn't matter"],
       1, "If visibility expires mid-processing, the message becomes visible "
          "and gets processed twice.",
       ("amazon", "wipro", "hcl")),
    _q("aws-m3-l2-q4", "aws-m3-l2", "lambda-serverless", 5,
       "Async Lambda invocations fail twice. Then what?",
       ["Lost forever", "Sent to on-failure destination / DLQ if configured",
        "Retried hourly", "Alert only"],
       1, "Async has built-in 2 retries; configure DLQ/SNS/SQS destination "
          "or failures vanish silently.",
       ("amazon", "tcs", "razorpay")),
    _q("aws-m3-l2-q5", "aws-m3-l2", "lambda-serverless", 7,
       "Why must SQS-driven Lambdas be idempotent?",
       ["They are slow", "At-least-once delivery: a message can be delivered (and processed) more than once",
        "They cost more", "SQS is unordered"],
       1, "Retries + visibility timeouts mean duplicates happen. Use "
          "conditional writes / dedupe keys.",
       ("amazon", "flipkart", "phonepe")),
    _q("aws-m3-l2-q6", "aws-m3-l2", "lambda-serverless", 9,
       "10,000 msgs/sec burst into SQS; downstream RDS maxes at 500 writes/sec. Protect the DB?",
       ["Bigger Lambda", "Reserved concurrency cap on the function + SQS buffering absorbs the burst",
        "More RDS", "Disable trigger"],
       1, "Reserved concurrency throttles Lambda; SQS queues the backlog. The "
          "DB never sees more than it can take.",
       ("amazon", "atlassian", "cred")),
    # ---- L3: api-gateway ----
    _q("aws-m3-l3-q1", "aws-m3-l3", "lambda-serverless", 1,
       "What is API Gateway for?",
       ["DNS", "Managed front door for APIs: routing, auth, throttling, caching",
        "Databases", "File storage"],
       1, "It turns Lambdas/EC2 into production HTTPS APIs with stages, keys, "
          "and usage plans.",
       ("tcs", "infosys")),
    _q("aws-m3-l3-q2", "aws-m3-l3", "lambda-serverless", 2,
       "HTTP API vs REST API — when is REST worth the extra cost?",
       ["Never", "Need usage plans/API keys, request validation, WAF, or private endpoints",
        "Always", "Only for SOAP"],
       1, "HTTP APIs cover ~most needs cheaper/faster. REST adds enterprise "
          "controls.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m3-l3-q3", "aws-m3-l3", "lambda-serverless", 3,
       "What are API Gateway stages?",
       ["EC2 sizes", "Named deployments (dev/stage/prod) of the same API",
        "Billing tiers", "Regions"],
       1, "Deploy once, promote through stages with separate throttling, "
          "logging, and variables.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m3-l3-q4", "aws-m3-l3", "lambda-serverless", 5,
       "Protect a public API from one abusive client without affecting others. How?",
       ["WAF only", "Usage plans + API keys: per-key throttling quotas",
        "Bigger Lambda", "CloudFront"],
       1, "API keys identify callers; usage plans set per-key rate/burst and "
          "monthly quotas.",
       ("amazon", "razorpay", "phonepe")),
    _q("aws-m3-l3-q5", "aws-m3-l3", "lambda-serverless", 7,
       "JWT authorizer vs Lambda authorizer — pick?",
       ["Always Lambda", "JWT for standard OAuth/OIDC tokens (cheap); Lambda authorizer for custom logic (DB lookups, weird schemes)",
        "JWT is slower", "No difference"],
       1, "JWT authorizers validate standard tokens without invoking Lambda — "
          "cheaper and faster for OIDC.",
       ("amazon", "microsoft", "atlassian")),
    _q("aws-m3-l3-q6", "aws-m3-l3", "lambda-serverless", 9,
       "Private microservices in a VPC must call each other via API Gateway without internet. Setup?",
       ["Public API", "Private REST API + VPC endpoint (PrivateLink) + resource policy",
        "HTTP API", "ALB instead"],
       1, "Private APIs are reachable only via interface VPC endpoints, locked "
          "down by resource policy.",
       ("amazon", "oracle", "deloitte")),
    # ---- L4: cold-starts ----
    _q("aws-m3-l4-q1", "aws-m3-l4", "lambda-serverless", 1,
       "What is a Lambda cold start?",
       ["Billing error", "Latency when AWS initializes a fresh execution environment",
        "A crash", "A deployment"],
       1, "First request (or scale-out) pays init cost: download code, boot "
          "runtime, run init code.",
       ("tcs", "infosys")),
    _q("aws-m3-l4-q2", "aws-m3-l4", "lambda-serverless", 2,
       "Which runtime generally has the WORST cold starts?",
       ["Python", "Java / .NET (JVM/CLR init is heavy)", "Node.js", "Go"],
       1, "JVM/CLR bootstrap dominates. Python/Node/Go start fast. SnapStart "
          "fixes Java.",
       ("amazon", "accenture")),
    _q("aws-m3-l4-q3", "aws-m3-l4", "lambda-serverless", 3,
       "Guaranteed way to eliminate cold starts for a latency-critical API?",
       ["More memory", "Provisioned Concurrency — pre-warmed environments, always ready",
        "Bigger package", "Fewer triggers"],
       1, "Provisioned concurrency keeps N environments initialized. It costs "
          "even when idle — the price of zero cold starts.",
       ("amazon", "wipro", "swiggy")),
    _q("aws-m3-l4-q4", "aws-m3-l4", "lambda-serverless", 5,
       "Why does increasing Lambda memory often REDUCE cost?",
       ["It doesn't", "CPU scales with memory — faster execution can lower GB-seconds billed",
        "AWS discounts it", "Less logging"],
       1, "Duration drops faster than the per-GB price rises. Power Tuning "
          "finds the sweet spot empirically.",
       ("amazon", "tcs", "flipkart")),
    _q("aws-m3-l4-q5", "aws-m3-l4", "lambda-serverless", 7,
       "What is SnapStart?",
       ["A debugger", "Pre-initialized Java snapshots that slash cold starts",
        "A deploy tool", "A test framework"],
       1, "SnapStart snapshots the initialized JVM; new environments restore "
          "the snapshot instead of booting.",
       ("amazon", "microsoft", "hcl")),
    _q("aws-m3-l4-q6", "aws-m3-l4", "lambda-serverless", 9,
       "P99 latency spikes only on deploys + traffic bursts, Python API. Cheapest mitigation?",
       ["Provisioned concurrency everywhere", "Trim package + move heavy init out of handler + warm critical paths; provisioned concurrency only for the P99-critical route",
        "Rewrite in Rust", "Bigger VPC"],
       1, "Surgical approach: optimize init code (runs once per environment), "
          "pay for provisioned concurrency only where P99 matters.",
       ("amazon", "atlassian", "phonepe")),
    # ---- L5: lambda-limits ----
    _q("aws-m3-l5-q1", "aws-m3-l5", "lambda-serverless", 1,
       "Lambda max memory?",
       ["1 GB", "10 GB", "128 MB", "Unlimited"],
       1, "128 MB – 10 GB in 1 MB steps. More memory = proportionally more CPU.",
       ("tcs", "infosys")),
    _q("aws-m3-l5-q2", "aws-m3-l5", "lambda-serverless", 2,
       "Default concurrent executions per region?",
       ["100", "1,000", "10,000", "Unlimited"],
       1, "1,000 concurrent (soft limit, raisable). Bursts above it get "
          "throttled (429).",
       ("amazon", "accenture")),
    _q("aws-m3-l5-q3", "aws-m3-l5", "lambda-serverless", 3,
       "Your video transcode takes 40 minutes. Can Lambda do it?",
       ["Yes", "No — 15 min max. Use Fargate/EC2/Batch",
        "Yes, with more memory", "Yes, with provisioned concurrency"],
       1, "Hard 15-minute ceiling. Long batch = containers or Batch, not "
          "Lambda.",
       ("amazon", "wipro", "hotstar")),
    _q("aws-m3-l5-q4", "aws-m3-l5", "lambda-serverless", 5,
       "What are Lambda Layers for?",
       ["Faster cold starts", "Share code/libraries across functions (up to 5 layers, 250 MB total)",
        "More memory", "VPC access"],
       1, "Put boto3 upgrades, ffmpeg, or company SDKs in a layer; functions "
          "stay small and consistent.",
       ("amazon", "tcs", "hcl")),
    _q("aws-m3-l5-q5", "aws-m3-l5", "lambda-serverless", 7,
       "Why set RESERVED concurrency on a function writing to a small RDS?",
       ["Speed", "Cap concurrent executions so the function can't overwhelm the DB's connection limit",
        "Cost", "Cold starts"],
       1, "Reserved concurrency is a throttle: 1,000 parallel Lambdas × DB "
          "connections = dead database.",
       ("amazon", "flipkart", "cognizant")),
    _q("aws-m3-l5-q6", "aws-m3-l5", "lambda-serverless", 9,
       "Deployment package is 300 MB unzipped with ML models. Options?",
       ["It just works", "Slim it (layers, /tmp download at runtime) or use container image (up to 10 GB)",
        "More memory", "Split into 2 functions"],
       1, "250 MB unzipped cap for zips; container images allow 10 GB. Or "
          "lazy-load models from S3 into /tmp.",
       ("amazon", "microsoft", "dream11")),
    # ---- L6: step-functions ----
    _q("aws-m3-l6-q1", "aws-m3-l6", "lambda-serverless", 1,
       "What are Step Functions for?",
       ["Databases", "Orchestrating multi-step serverless workflows as visual state machines",
        "DNS", "File storage"],
       1, "Coordinate Lambdas with retries, branching, waits, and human "
          "approvals — no callback spaghetti.",
       ("tcs", "infosys")),
    _q("aws-m3-l6-q2", "aws-m3-l6", "lambda-serverless", 2,
       "Standard vs Express workflows — when Express?",
       ["Long orders", "High-volume, short-duration event processing (IoT, streaming)",
        "Human approvals", "Exactly-once needed"],
       1, "Express: 5-min max, at-least-once, per-request pricing. Standard: "
          "up to 1 year, exactly-once semantics.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m3-l6-q3", "aws-m3-l6", "lambda-serverless", 3,
       "How do Step Functions handle a failing Lambda step?",
       ["Crash", "Retry with backoff + Catch to fallback states (e.g., refund)",
        "Ignore", "Restart workflow"],
       1, "Declarative error handling: Retry policies per error type, Catch "
          "routes to compensation logic.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m3-l6-q4", "aws-m3-l6", "lambda-serverless", 5,
       "Why not just have Lambda call the next Lambda directly?",
       ["It's faster", "Tight coupling + double billing + no visual trace + hand-rolled retries",
        "It's cheaper", "No reason"],
       1, "Chained Lambdas hide the workflow, double-bill idle waits, and "
          "make error handling miserable.",
       ("amazon", "swiggy", "razorpay")),
    _q("aws-m3-l6-q5", "aws-m3-l6", "lambda-serverless", 7,
       "Need a human manager to approve refunds over $500 in an order flow. How?",
       ["Email", "Step Functions Task Token / callback pattern — pause until human responds",
        "Polling Lambda", "SQS delay"],
       1, "Task tokens pause the execution for days/weeks; the approval API "
          "call resumes it. Built for humans-in-the-loop.",
       ("amazon", "atlassian", "phonepe")),
    _q("aws-m3-l6-q6", "aws-m3-l6", "lambda-serverless", 9,
       "Saga pattern for 'book flight + hotel, refund both if either fails.' Implement how?",
       ["2PC database", "Step Functions orchestrating each step with compensating actions on Catch",
        "One giant Lambda", "Manual ops runbook"],
       1, "No distributed transactions in serverless — choreograph forward "
          "steps and compensations explicitly.",
       ("amazon", "makemytrip", "cred")),
    # ---- L7: serverless-patterns ----
    _q("aws-m3-l7-q1", "aws-m3-l7", "lambda-serverless", 1,
       "API should return 200ms but order processing takes 30s. Pattern?",
       ["Bigger Lambda", "API Lambda validates → SQS → worker Lambda processes async",
        "EC2", "Wait in API"],
       1, "Decouple: respond fast, process async. The user never waits for "
          "slow work.",
       ("tcs", "infosys", "swiggy")),
    _q("aws-m3-l7-q2", "aws-m3-l7", "lambda-serverless", 2,
       "One upload must trigger thumbnails, search index, AND notifications. Pattern?",
       ["One big Lambda", "Fan-out: SNS topic → multiple Lambda subscribers",
        "Sequential calls", "EC2 cron"],
       1, "Publish once to SNS; each consumer subscribes independently. Add "
          "new consumers without touching producers.",
       ("amazon", "accenture", "hotstar")),
    _q("aws-m3-l7-q3", "aws-m3-l7", "lambda-serverless", 3,
       "Anti-pattern: Lambda synchronously invoking another Lambda. Why bad?",
       ["It's fast", "Double billing, tight coupling, timeout chaining — use SQS/Step Functions",
        "It's secure", "No issue"],
       1, "Caller pays while waiting; failures cascade; no visibility. Async "
          "handoff instead.",
       ("amazon", "wipro", "hcl")),
    _q("aws-m3-l7-q4", "aws-m3-l7", "lambda-serverless", 5,
       "Migrating a monolith to serverless gradually. Strategy?",
       ["Big bang rewrite", "Strangler fig: API Gateway routes new paths to Lambda, old to monolith",
        "Two apps forever", "Stop the monolith"],
       1, "Incremental strangulation de-risks migration — each route moves "
          "when ready, rollback is a route change.",
       ("amazon", "tcs", "flipkart")),
    _q("aws-m3-l7-q5", "aws-m3-l7", "lambda-serverless", 7,
       "S3 event → Lambda writes back to the SAME bucket/prefix. Danger?",
       ["None", "Infinite recursion → runaway billing. Filter prefixes / use separate buckets",
        "It's faster", "More durable"],
       1, "Self-triggering loops are the classic serverless billing horror "
          "story. Always set billing alarms.",
       ("amazon", "microsoft", "dream11")),
    _q("aws-m3-l7-q6", "aws-m3-l7", "lambda-serverless", 9,
       "Serverless bill exploded at scale. What do you model FIRST?",
       ["Nothing", "Requests × duration × memory vs always-on alternative; check chatty patterns (N+1 invokes, recursion)",
        "Blame AWS", "Delete functions"],
       1, "Serverless unit economics flip at scale. Model the math and hunt "
          "pathological patterns before re-architecting.",
       ("amazon", "razorpay", "atlassian")),
]
