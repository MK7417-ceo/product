"""Seed content: AWS — Modules 4-5 (IAM & VPC, RDS & Monitoring).

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
        id="aws-m4",
        domain_slug=DOMAIN_SLUG,
        slug="iam-vpc",
        name="IAM & VPC",
        description=(
            "Security and networking foundations: IAM users, policies and roles "
            "with least privilege, plus VPCs, subnets, gateways and NACLs vs "
            "security groups."
        ),
        order_index=4,
        estimated_days=10,
    ),
    CurriculumModule(
        id="aws-m5",
        domain_slug=DOMAIN_SLUG,
        slug="rds-cloudwatch",
        name="RDS & Monitoring",
        description=(
            "Managed databases and observability: RDS Multi-AZ, DynamoDB, read "
            "replicas, CloudWatch metrics/alarms/logs, CloudTrail auditing and "
            "cost optimization."
        ),
        order_index=5,
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
# LESSONS — Module 4: IAM & VPC
# ---------------------------------------------------------------------------

LESSONS = [
    CurriculumLesson(
        id="aws-m4-l1",
        module_id="aws-m4",
        slug="iam-basics",
        title="IAM Basics — Users and the Root Account",
        content="""**IAM (Identity and Access Management)** controls WHO can do WHAT
in your AWS account. The first rules:

1. **Lock the root account**: enable MFA on root, then never use it again.
   Create an admin IAM user/group for daily work.
2. **Users** = humans or apps needing long-term credentials.
3. **Groups** = attach policies to groups, put users in groups (never attach
   policies directly to users — unmanageable at scale).
4. **No sharing**: one IAM user per human. Ever.

```bash
# Create a developer user + add to group (CLI)
aws iam create-user --user-name anita
aws iam add-user-to-group --user-name anita --group-name developers
aws iam create-login-profile --user-name anita --password-reset-required
```

**Credential types:** console password (humans) vs access keys (CLI/SDK).
Rotate access keys regularly; prefer **roles** (temporary credentials) over
long-lived keys wherever possible.

**Exam mantra:** "Root locked with MFA, policies on groups, humans get
users, apps get roles." """,
        order_index=1,
        estimated_minutes=25,
    ),
    CurriculumLesson(
        id="aws-m4-l2",
        module_id="aws-m4",
        slug="iam-policies",
        title="IAM Policies — JSON Permission Language",
        content="""Policies are JSON documents granting or denying actions on
resources:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:PutObject"],
    "Resource": "arn:aws:s3:::app-uploads/*",
    "Condition": {"IpAddress": {"aws:SourceIp": "203.0.113.0/24"}}
  }]
}
```

**Evaluation (memorize this):**
1. Default = **implicit deny**.
2. An explicit **Allow** overrides it.
3. An explicit **Deny beats ANY Allow** — anywhere (identity policy, resource
   policy, SCP, permissions boundary).

**Policy types:**
- **Managed** (AWS-managed or customer-managed) — reusable, versioned.
- **Inline** — embedded in one user/role; avoid except one-off cases.
- **Trust policies** — who can *assume* a role.

**Least privilege in practice:** start from AWS managed `ReadOnlyAccess`,
add only needed writes. **IAM Access Analyzer** flags unused permissions —
run it quarterly and trim.

**Interview trap:** "Policy allows S3, SCP denies S3. Result?" Denied —
SCPs (org-level guardrails) veto everything below them.""",
        order_index=2,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m4-l3",
        module_id="aws-m4",
        slug="iam-roles",
        title="IAM Roles — Temporary Credentials Done Right",
        content="""A **role** is an identity with permissions but no permanent
credentials — you *assume* it and get temporary keys (15 min–12 h).

```bash
# Assume a role (gets temp creds)
aws sts assume-role --role-arn arn:aws:iam::123:role/deployer \\
  --role-session-name ci-build
```

**The big three uses:**
1. **EC2/Lambda execution roles** — apps get AWS access with zero stored
   keys. (This is why Lambda "just works" with DynamoDB.)
2. **Cross-account access** — Account B's admin assumes a role in Account A.
   No credential sharing.
3. **Federation** — Google/Okta users assume roles via SAML/OIDC; employees
   never get IAM users.

**Trust policy** = who may assume; **permissions policy** = what they can do
once assumed. Both must allow.

**Instance profiles** are just the wrapper that lets EC2 assume a role —
in the console you "attach a role to an instance"; under the hood it is an
instance profile.

**Golden rule:** if you are embedding access keys in app config, you are
doing it wrong — reach for a role.""",
        order_index=3,
        estimated_minutes=25,
    ),
    CurriculumLesson(
        id="aws-m4-l4",
        module_id="aws-m4",
        slug="vpc-basics",
        title="VPC — Your Private Network",
        content="""A **VPC (Virtual Private Cloud)** is your isolated network slice
in a region. You define its IP range with **CIDR** notation:

```bash
aws ec2 create-vpc --cidr-block 10.0.0.0/16
# 10.0.0.0/16 = 65,536 IPs. /24 = 256 IPs. Bigger prefix = smaller network.
```

**Structure:**
- A VPC spans a **region**; **subnets** live in single **AZs**.
- Default VPC exists for quick starts — production uses custom VPCs.
- **DNS**: enable DNS hostnames + resolution so instances get names.

**CIDR math (interview favorite):**
- `10.0.0.0/16` → 65,536 addresses (65,531 usable; AWS reserves 5).
- `10.0.1.0/24` → 256 addresses.
- Subnets must not overlap, and must fit inside the VPC CIDR.

**Design habit:** one VPC per environment (dev/stage/prod) or per
workload, peered or connected via Transit Gateway. Never one giant
flat /16 for everything.""",
        order_index=4,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m4-l5",
        module_id="aws-m4",
        slug="subnets",
        title="Subnets — Public vs Private",
        content="""Subnets carve the VPC into AZ-aligned segments. The **route
table** decides public vs private:

- **Public subnet** — route table has `0.0.0.0/0 → Internet Gateway`.
- **Private subnet** — no IGW route; outbound via NAT gateway.

```bash
# Public subnet in ap-south-1a, private in ap-south-1b
aws ec2 create-subnet --vpc-id vpc-123 --cidr-block 10.0.1.0/24 \\
  --availability-zone ap-south-1a
aws ec2 create-subnet --vpc-id vpc-123 --cidr-block 10.0.2.0/24 \\
  --availability-zone ap-south-1b
```

**Classic 3-tier layout:**
- Public subnets (2 AZs): ALB, NAT gateways, bastion.
- Private app subnets (2 AZs): EC2/ECS workloads.
- Private data subnets (2 AZs): RDS, ElastiCache — no internet at all.

**Route tables** are attached per subnet; the **main** route table catches
subnets without an explicit association. **Subnet = AZ-locked**: an
instance's subnet determines its AZ forever.

**Exam line:** "Public = IGW route. Private = no IGW route. The route table
is the definition, not the name." """,
        order_index=5,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m4-l6",
        module_id="aws-m4",
        slug="nat-igw",
        title="Internet, NAT Gateways & Bastions",
        content="""How traffic enters and leaves the VPC:

- **Internet Gateway (IGW)** — the VPC's door to the internet. One per VPC,
  highly available by design, no bandwidth worries.
- **NAT Gateway** — lets *private* subnet instances reach the internet
  (updates, patches) while blocking inbound initiation. Managed, AZ-scoped
  (~$0.045/hr + data processing — the famous surprise bill).
- **Bastion host** — a hardened SSH jump box in a public subnet for admin
  access to private instances.

```bash
# NAT gateway needs an Elastic IP + public subnet
aws ec2 allocate-address --domain vpc
aws ec2 create-nat-gateway --subnet-id subnet-public-1a \\
  --allocation-id eipalloc-123
```

**Modern alternative:** skip bastions entirely — **Session Manager** gives
browser/CLI shell to private instances via IAM, no inbound ports, full
audit trail.

**Cost trap:** NAT Gateway data-processing charges add up fast for chatty
workloads. Alternatives: VPC endpoints (S3/DynamoDB are **free** via
gateway endpoints!), or consolidate NATs if AZ-redundancy allows.

**VPC endpoints** (PrivateLink) reach AWS services without internet: gateway
type (S3, DynamoDB — free) and interface type (most services — hourly +
per-GB).""",
        order_index=6,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m4-l7",
        module_id="aws-m4",
        slug="nacl-sg",
        title="NACLs vs Security Groups — Defense in Depth",
        content="""Two firewall layers, different jobs:

| | Security Group | NACL |
|---|---|---|
| Attached to | ENI (instance) | Subnet |
| Stateful | **Yes** | **No** |
| Rules | Allow only | **Allow + Deny**, numbered |
| Evaluation | All rules together | Lowest number first |

```bash
# NACL: block a malicious IP explicitly (SGs can't deny)
aws ec2 create-network-acl-entry --network-acl-id acl-123 \\
  --rule-number 90 --protocol -1 --rule-action deny \\
  --cidr-block 198.51.100.77/32 --ingress
```

**When NACLs shine:** subnet-level guardrails (block bad IPs for everything
in the subnet), compliance "deny lists". Day-to-day, SGs do the real work.

**Defense in depth, ordered:**
1. WAF / Shield at the edge (L7 attacks, DDoS).
2. NACL at the subnet (coarse deny lists).
3. Security group at the instance (precise allow lists).
4. OS firewall + app auth (last mile).

**Interview answer:** "SGs are stateful allow-lists at the instance;
NACLs are stateless numbered allow/deny at the subnet. Use both — SGs for
precision, NACLs for broad guardrails." """,
        order_index=7,
        estimated_minutes=25,
    ),
    # ---------------- Module 5: RDS & Monitoring ----------------
    CurriculumLesson(
        id="aws-m5-l1",
        module_id="aws-m5",
        slug="rds-basics",
        title="RDS — Managed Relational Databases",
        content="""**RDS** runs MySQL, PostgreSQL, MariaDB, Oracle, SQL Server —
and **Aurora** (AWS's cloud-native engine) — without you patching OSs or
managing backups.

```bash
# PostgreSQL, Multi-AZ, 100 GB gp3
aws rds create-db-instance --db-instance-identifier prod-db \\
  --engine postgres --db-instance-class db.r6g.large \\
  --allocated-storage 100 --multi-az --storage-type gp3
```

**What AWS handles:** provisioning, patching, automated backups (35-day
retention), OS maintenance. **What you handle:** schema, indexes, queries,
and *not* getting SSH (no host access — by design).

**Multi-AZ** = synchronous standby in another AZ for failover (availability,
not scaling). **Read replicas** = async copies for scaling reads.

**Aurora** deserves special mention: up to 5x MySQL / 3x Postgres
throughput, storage auto-scales to 128 TB, **backtrack** (rewind the DB to
a point in time), and Global Database (cross-region, <1s replication lag).

**Exam line:** "RDS Multi-AZ for failover, read replicas for scale, Aurora
when you need cloud-native performance." """,
        order_index=1,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m5-l2",
        module_id="aws-m5",
        slug="dynamodb",
        title="DynamoDB — Serverless NoSQL",
        content="""**DynamoDB** is serverless key-value/document storage: single-digit
millisecond latency at any scale, zero servers.

```bash
# Table with partition key user_id
aws dynamodb create-table --table-name sessions \\
  --attribute-definitions AttributeName=user_id,AttributeType=S \\
  --key-schema AttributeName=user_id,KeyType=HASH \\
  --billing-mode PAY_PER_REQUEST
```

**Data model:**
- **Partition key** (HASH) — required; determines the physical partition.
- **Sort key** (RANGE, optional) — enables rich queries within a partition.
- Wrong key design = hot partitions = throttling. **Key design IS the
  schema design** in DynamoDB.

**Capacity modes:**
- **On-demand** — pay per request; spiky/unpredictable.
- **Provisioned** — reserve RCU/WCU; steady traffic + auto scaling.

**Power features:** DAX (in-memory cache), Global Tables (multi-region
active-active), Streams (change feed → Lambda), TTL (auto-expire items —
free deletes!), transactions, point-in-time recovery.

**Interview trap:** "Why is my DynamoDB throttling?" → hot partition key
(everyone querying `status=active`), or exceeded provisioned throughput.
Fix: better key distribution, on-demand mode, or DAX.""",
        order_index=2,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m5-l3",
        module_id="aws-m5",
        slug="read-replicas",
        title="Read Replicas & Failover",
        content="""Scaling reads and surviving failures — two different tools:

**Read replicas (RDS):**
- Async replication (seconds of lag).
- **Promotable** to standalone (or to master in a failover you trigger).
- Up to 5 (MySQL/Postgres); Aurora: 15 with <10ms lag.
- Reporting/analytics offload; never for writes.

**Multi-AZ failover:**
- Synchronous standby, automatic DNS flip on failure (~1-2 min).
- You never talk to the standby directly.

```bash
# Promote a replica (planned failover / DR drill)
aws rds promote-read-replica --db-instance-identifier prod-replica-1
```

**Aurora specifics:** storage is distributed across 3 AZs with 6 copies;
a writer failure fails over to a reader in **~30 seconds**. **Aurora
Serverless v2** scales capacity in fine increments for variable workloads.

**Exam pattern:** "reporting queries slowing prod" → read replica.
"Survive AZ failure automatically" → Multi-AZ. "Global users, <1s writes
everywhere" → Aurora Global Database.""",
        order_index=3,
        estimated_minutes=25,
    ),
    CurriculumLesson(
        id="aws-m5-l4",
        module_id="aws-m5",
        slug="cloudwatch",
        title="CloudWatch — Metrics, Alarms, Logs",
        content="""**CloudWatch** is AWS's monitoring nervous system:

- **Metrics** — time-series numbers (CPU, latency, custom). 1-min (detailed)
  or 5-min granularity.
- **Alarms** — "if CPU > 80% for 5 min → notify / scale". States: OK,
  ALARM, INSUFFICIENT_DATA.
- **Logs** — central log aggregation with filter patterns and Insights
  (SQL-like queries over logs).
- **Events/EventBridge** — react to state changes (instance stopped →
  Lambda).

```bash
# Alarm: CPU > 80% for 2 periods → SNS topic
aws cloudwatch put-metric-alarm --alarm-name high-cpu \\
  --metric-name CPUUtilization --namespace AWS/EC2 \\
  --statistic Average --period 300 --threshold 80 \\
  --comparison-operator GreaterThanThreshold \\
  --evaluation-periods 2 --alarm-actions arn:aws:sns:...:ops
```

**Composite alarms** reduce noise (fire only if 3/5 children alarm).
**Anomaly detection** uses ML bands instead of static thresholds — great for
metrics with daily/weekly seasonality.

**Dashboards** stitch metrics into ops views. **Synthetics canaries**
(scripted API checks) catch outages before users do.

**Interview line:** "Metrics tell you WHAT, alarms tell you WHEN, logs tell
you WHY." """,
        order_index=4,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m5-l5",
        module_id="aws-m5",
        slug="cloudtrail",
        title="CloudTrail & Config — Auditing",
        content="""**CloudTrail** logs every API call in your account — WHO did WHAT,
WHEN, from WHERE. The security camera of AWS.

```bash
# Trail: all regions, log to S3, alert on root usage
aws cloudtrail create-trail --name org-trail \\
  --s3-bucket-name audit-logs --is-multi-region-trail \\
  --enable-log-file-validation
```

**Key practices:**
- **Multi-region trail** → one S3 bucket for everything.
- **Log file validation** → tamper-evident (digest files).
- **CloudTrail Insights** → ML detection of unusual API activity.
- Send to **CloudWatch Logs** for metric filters + alarms ("alert me on
  root login" is the classic).

**CloudTrail vs CloudWatch:** Trail = API audit log (control plane);
CloudWatch = metrics/logs of resources (data plane). Different jobs.

**AWS Config** records *configuration history* ("what did this SG look like
last Tuesday?") and evaluates **rules** ("all EBS volumes must be
encrypted") — compliance as code. Config + Security Hub = the governance
backbone.

**Exam answer:** "Trail for who-did-what, Config for what-does-it-look-like,
both feeding the SIEM." """,
        order_index=5,
        estimated_minutes=25,
    ),
    CurriculumLesson(
        id="aws-m5-l6",
        module_id="aws-m5",
        slug="cost-optimization",
        title="Cost Optimization — FinOps Basics",
        content="""Cloud bills are a design problem. The toolkit:

1. **Cost Explorer + Cost Anomaly Detection** — see spend, get alerted on
   spikes. Tag everything (`team`, `env`, `project`) or allocation is
   guesswork.
2. **Budgets** — "alert me at 80% of $5k" (or actually *stop* things via
   budget actions).
3. **Right-sizing** — Compute Optimizer flags idle/oversized instances.
4. **Graviton** — ARM instances, ~20-40% cheaper for compatible workloads.
5. **S3 lifecycle + Intelligent-Tiering** — covered in Module 2.
6. **Kill orphans** — unattached EBS, idle ELBs, old snapshots, forgotten
   NAT gateways.

```bash
# Find unattached (wasteful) EBS volumes
aws ec2 describe-volumes \\
  --filters Name=status,Values=available \\
  --query 'Volumes[*].[VolumeId,Size,CreateTime]'
```

**The FinOps loop:** visibility (tags, Explorer) → accountability (budgets
per team) → optimization (right-size, commitments) → repeat monthly.

**Interview answer:** "Tag-based visibility first, then right-size, then
commit (Reserved/Savings Plans) for the steady baseline, Spot for the
interruptible rest. Revisit monthly — architectures drift." """,
        order_index=6,
        estimated_minutes=25,
    ),
]


def _q(qid, lid, mslug, diff, prompt, choices, ans, expl, tags):
    return _mkq(qid, lid, mslug, diff, prompt, choices, ans, expl, tags)


QUESTIONS = [
    # ================= M4: IAM & VPC =================
    # ---- L1: iam-basics ----
    _q("aws-m4-l1-q1", "aws-m4-l1", "iam-vpc", 1,
       "First security step for a new AWS account?",
       ["Create 10 users", "Enable MFA on root, then stop using root",
        "Open all ports", "Disable CloudTrail"],
       1, "Root is god-mode. MFA-lock it, create admin IAM users/groups for "
          "daily work, never touch root again.",
       ("tcs", "infosys", "wipro")),
    _q("aws-m4-l1-q2", "aws-m4-l1", "iam-vpc", 2,
       "Best practice for granting permissions to 20 developers?",
       ["Attach policies to each user", "Attach policies to a group; put users in the group",
        "Share one admin user", "Use root"],
       1, "Groups scale; per-user policies become unmanageable and drift.",
       ("amazon", "accenture")),
    _q("aws-m4-l1-q3", "aws-m4-l1", "iam-vpc", 3,
       "An app on EC2 needs S3 access. Best credential approach?",
       ["Access keys in code", "IAM role via instance profile (temporary credentials)",
        "Root keys", "Shared IAM user"],
       1, "Roles give temporary, auto-rotated credentials. Embedded keys leak "
          "and never rotate.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m4-l1-q4", "aws-m4-l1", "iam-vpc", 5,
       "An employee leaves. Fastest way to revoke ALL their access?",
       ["Delete their laptop", "Deactivate/delete the IAM user (kills keys, console, group memberships)",
        "Change the password", "Nothing needed"],
       1, "Deleting/deactivating the user invalidates everything at once. "
          "Also rotate any shared secrets they knew.",
       ("amazon", "microsoft", "cognizant")),
    _q("aws-m4-l1-q5", "aws-m4-l1", "iam-vpc", 7,
       "Why is 'one IAM user per human' a rule, not a suggestion?",
       ["Cost", "Attribution: shared credentials destroy audit trails (who did what?)",
        "Speed", "AWS limits"],
       1, "CloudTrail logs the IAM identity. Shared users make incident "
          "response and compliance impossible.",
       ("amazon", "atlassian", "cred")),
    _q("aws-m4-l1-q6", "aws-m4-l1", "iam-vpc", 9,
       "Design onboarding for 200 engineers with SSO (Okta). IAM users for all?",
       ["Yes", "No — federate via SAML/OIDC: Okta users assume roles, zero IAM users to manage",
        "Root for all", "One shared user"],
       1, "Federation = single identity source, instant deprovisioning, no "
          "long-lived AWS credentials per human.",
       ("amazon", "deloitte", "oracle")),
    # ---- L2: iam-policies ----
    _q("aws-m4-l2-q1", "aws-m4-l2", "iam-vpc", 1,
       "What is an IAM policy?",
       ["A password rule", "A JSON document granting/denying actions on resources",
        "A network rule", "A backup schedule"],
       1, "Policies are the permission language: Effect + Action + Resource "
          "(+ Condition).",
       ("tcs", "infosys")),
    _q("aws-m4-l2-q2", "aws-m4-l2", "iam-vpc", 2,
       "Policy evaluation order?",
       ["Allow wins", "Implicit deny → explicit allow → explicit deny wins over everything",
        "First match wins", "Random"],
       1, "Default deny; an Allow permits; any explicit Deny (identity, "
          "resource, SCP, boundary) vetoes all Allows.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m4-l2-q3", "aws-m4-l2", "iam-vpc", 3,
       "SCP denies s3:*, identity policy allows s3:GetObject. Result?",
       ["Allowed", "Denied — SCPs are org-level guardrails that veto everything below",
        "Allowed in some regions", "Depends on MFA"],
       1, "Service Control Policies cap the maximum permissions in an OU — "
          "even admins cannot exceed them.",
       ("amazon", "hcl", "deloitte")),
    _q("aws-m4-l2-q4", "aws-m4-l2", "iam-vpc", 5,
       "Practical least-privilege workflow for a new microservice?",
       ["AdministratorAccess", "Start from ReadOnlyAccess, add only needed writes; trim quarterly via Access Analyzer",
        "No policy", "Root"],
       1, "Grow permissions from minimal, and let Access Analyzer find the "
          "unused ones to remove.",
       ("amazon", "tcs", "phonepe")),
    _q("aws-m4-l2-q5", "aws-m4-l2", "iam-vpc", 7,
       "Inline vs managed policies — when is inline acceptable?",
       ["Always", "Rarely — one-off exceptions; managed policies are reusable and versioned",
        "Never", "Only for root"],
       1, "Inline policies die with the identity and can't be reused. Managed "
          "= versioned, auditable, attachable.",
       ("amazon", "microsoft", "atlassian")),
    _q("aws-m4-l2-q6", "aws-m4-l2", "iam-vpc", 9,
       "A role's trust policy allows Account B, permissions policy allows S3. B's admin gets AccessDenied. Why?",
       ["Wrong region", "B's side also needs an identity policy allowing sts:AssumeRole on that role ARN",
        "S3 is down", "MFA required"],
       1, "Cross-account = both sides must allow: trust policy (resource side) "
          "AND the assumers' identity policy.",
       ("amazon", "oracle", "cred")),
    # ---- L3: iam-roles ----
    _q("aws-m4-l3-q1", "aws-m4-l3", "iam-vpc", 1,
       "What is an IAM role?",
       ["A user group", "An identity with permissions but no permanent credentials — assumed for temporary access",
        "A password", "A server"],
       1, "Roles are assumed via STS for temporary keys. No long-lived secrets "
          "to leak.",
       ("tcs", "infosys")),
    _q("aws-m4-l3-q2", "aws-m4-l3", "iam-vpc", 2,
       "How does an EC2 instance get AWS permissions without stored keys?",
       ["It can't", "Instance profile → assumes an IAM role; SDK gets temp creds automatically",
        "Root keys", "Environment variables only"],
       1, "Attach a role to the instance (via instance profile); the metadata "
          "service vends rotating credentials.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m4-l3-q3", "aws-m4-l3", "iam-vpc", 3,
       "Trust policy vs permissions policy on a role?",
       ["Same thing", "Trust = WHO can assume it; permissions = WHAT they can do after assuming",
        "Trust is for users", "Permissions are for groups"],
       1, "Both must allow. Trust without permissions = assume but do nothing; "
          "vice versa = cannot assume at all.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m4-l3-q4", "aws-m4-l3", "iam-vpc", 5,
       "CI pipeline deploys to AWS. Best credential handling?",
       ["Long-lived keys in repo", "OIDC federation: GitHub Actions assumes a role — no stored secrets at all",
        "Root keys in CI", "Shared IAM user"],
       1, "OIDC federation mints short-lived creds per run. Zero secrets in "
          "the repo, zero rotation toil.",
       ("amazon", "atlassian", "swiggy")),
    _q("aws-m4-l3-q5", "aws-m4-l3", "iam-vpc", 7,
       "You find AWS access keys committed to a public GitHub repo. Immediate steps?",
       ["Ignore", "Deactivate/delete the keys NOW, audit CloudTrail for misuse, rotate everything exposed",
        "Delete the repo", "Change region"],
       1, "Assume compromise: kill the keys first, then forensicate. Bots scan "
          "GitHub for keys within minutes.",
       ("amazon", "cred", "microsoft")),
    _q("aws-m4-l3-q6", "aws-m4-l3", "iam-vpc", 9,
       "Multi-account landing zone: developers need read-only everywhere + admin in dev. Design?",
       ["IAM users per account", "SSO + permission sets: ReadOnly role in all accounts, Admin role only in dev — assumed via SSO",
        "Root everywhere", "One account"],
       1, "Identity Center permission sets map job functions to roles per "
          "account — one login, scoped access.",
       ("amazon", "deloitte", "oracle")),
    # ---- L4: vpc-basics ----
    _q("aws-m4-l4-q1", "aws-m4-l4", "iam-vpc", 1,
       "What is a VPC?",
       ["A virtual server", "Your isolated private network in an AWS region",
        "A database", "A billing account"],
       1, "VPC = your own IP space (CIDR) spanning a region, carved into "
          "AZ-local subnets.",
       ("tcs", "infosys")),
    _q("aws-m4-l4-q2", "aws-m4-l4", "iam-vpc", 2,
       "How many IP addresses in 10.0.0.0/16?",
       ["256", "65,536 (65,531 usable — AWS reserves 5)", "16", "1 million"],
       1, "A /16 has 2^16 addresses. AWS reserves the first 4 + last 1 in "
          "every subnet.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m4-l4-q3", "aws-m4-l4", "iam-vpc", 3,
       "Can two subnets in one VPC have overlapping CIDRs?",
       ["Yes", "No — subnets must not overlap within a VPC",
        "Yes, in different AZs", "Only /24s"],
       1, "Overlapping CIDRs break routing. Plan non-overlapping blocks per "
          "subnet up front.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m4-l4-q4", "aws-m4-l4", "iam-vpc", 5,
       "You need 4 subnets x 500 hosts each. Which VPC CIDR fits?",
       ["10.0.0.0/24", "10.0.0.0/22", "10.0.0.0/16", "10.0.0.0/28"],
       2, "500 hosts need /23 (512 addrs) per subnet; 4 subnets need /21. "
          "Only /16 (65,536) fits — /22 has just 1,024.",
       ("amazon", "cisco", "cognizant")),
    _q("aws-m4-l4-q5", "aws-m4-l4", "iam-vpc", 7,
       "Why separate VPCs per environment instead of one big VPC?",
       ["Cost", "Blast-radius isolation: a bad route/SG change in dev can't touch prod",
        "Speed", "AWS requires it"],
       1, "Network-level isolation beats hoping nobody fat-fingers a route "
          "table in the shared VPC.",
       ("amazon", "atlassian", "phonepe")),
    _q("aws-m4-l4-q6", "aws-m4-l4", "iam-vpc", 9,
       "Two VPCs need private connectivity (no internet). Options?",
       ["IGW", "VPC peering (same/different region) or Transit Gateway for hub-and-spoke at scale",
        "NAT", "Public IPs"],
       1, "Peering for few VPCs; Transit Gateway when the mesh grows — one "
          "hub instead of N² peerings.",
       ("amazon", "microsoft", "oracle")),
    # ---- L5: subnets ----
    _q("aws-m4-l5-q1", "aws-m4-l5", "iam-vpc", 1,
       "What makes a subnet 'public'?",
       ["Its name", "Its route table has 0.0.0.0/0 → Internet Gateway",
        "Being in AZ-a", "Having many IPs"],
       1, "Public/private is defined by the route table, not the name. No IGW "
          "route = private.",
       ("tcs", "infosys")),
    _q("aws-m4-l5-q2", "aws-m4-l5", "iam-vpc", 2,
       "A subnet is locked to:",
       ["A region", "Exactly one Availability Zone",
        "All AZs", "One instance"],
       1, "Subnets are AZ-scoped. Instances inherit their subnet's AZ — "
          "that's why multi-AZ needs multiple subnets.",
       ("amazon", "accenture")),
    _q("aws-m4-l5-q3", "aws-m4-l5", "iam-vpc", 3,
       "Classic 3-tier layout — where does the ALB go?",
       ["Private app subnets", "Public subnets (it needs internet-facing IPs)",
        "Data subnets", "No subnets"],
       1, "Load balancers face the internet from public subnets; targets live "
          "privately behind them.",
       ("amazon", "wipro", "hcl")),
    _q("aws-m4-l5-q4", "aws-m4-l5", "iam-vpc", 5,
       "RDS instances should live in:",
       ["Public subnets", "Private data subnets with no internet route — reachable only from app SGs",
        "On-premises", "The default VPC"],
       1, "Databases never need inbound internet. Private subnets + SG "
          "referencing the app tier = least privilege.",
       ("amazon", "tcs", "flipkart")),
    _q("aws-m4-l5-q5", "aws-m4-l5", "iam-vpc", 7,
       "What is the 'main' route table?",
       ["The biggest one", "The default table for subnets with no explicit association — be careful what you put there",
        "The IGW table", "A billing table"],
       1, "Unassociated subnets silently inherit main. Explicitly associate "
          "every subnet to avoid surprises.",
       ("amazon", "cognizant", "deloitte")),
    _q("aws-m4-l5-q6", "aws-m4-l5", "iam-vpc", 9,
       "You need per-AZ private subnets sharing one NAT gateway to save cost. Trade-off?",
       ["None", "Cheaper, but AZ failure of the NAT's AZ kills outbound for all AZs — HA vs cost",
        "Faster", "More secure"],
       1, "One NAT = single AZ dependency. Per-AZ NATs cost more but survive "
          "AZ failure. Classic trade-off question.",
       ("amazon", "atlassian", "swiggy")),
    # ---- L6: nat-igw ----
    _q("aws-m4-l6-q1", "aws-m4-l6", "iam-vpc", 1,
       "What does an Internet Gateway do?",
       ["Filters packets", "Connects the VPC to the internet (highly available, managed)",
        "Assigns IPs", "Runs DNS"],
       1, "One IGW per VPC; attach it and add 0.0.0.0/0 routes to make subnets "
          "public.",
       ("tcs", "infosys")),
    _q("aws-m4-l6-q2", "aws-m4-l6", "iam-vpc", 2,
       "Private instances need OS patches (outbound internet) but no inbound. What?",
       ["IGW on private subnets", "NAT Gateway in a public subnet + route from private subnets",
        "Bastion", "Nothing"],
       1, "NAT = outbound-only internet. Private subnets route 0.0.0.0/0 to "
          "the NAT; nothing can initiate inbound.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m4-l6-q3", "aws-m4-l6", "iam-vpc", 3,
       "Cheapest way for EC2 to reach S3 privately (no NAT data charges)?",
       ["NAT Gateway", "Gateway VPC endpoint for S3 — free, private",
        "Internet Gateway", "Direct Connect"],
       1, "Gateway endpoints for S3/DynamoDB are free and never touch the "
          "internet. Always use them.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m4-l6-q4", "aws-m4-l6", "iam-vpc", 5,
       "NAT Gateway bill is shockingly high. Likely cause?",
       ["Too many AZs", "Chatty workloads paying per-GB data processing — consider VPC endpoints or consolidation",
        "Too many instances", "Wrong region"],
       1, "NAT charges hourly + per-GB processed. Endpoints bypass it for AWS "
          "services entirely.",
       ("amazon", "razorpay", "cred")),
    _q("aws-m4-l6-q5", "aws-m4-l6", "iam-vpc", 7,
       "Modern replacement for SSH bastion hosts?",
       ["Bigger bastion", "Systems Manager Session Manager — IAM-auth shell, no inbound ports, full audit",
        "More key pairs", "VPN only"],
       1, "No jump boxes to patch, no keys to manage, every command logged to "
          "CloudTrail/S3.",
       ("amazon", "phonepe", "atlassian")),
    _q("aws-m4-l6-q6", "aws-m4-l6", "iam-vpc", 9,
       "VPC endpoint types — gateway vs interface?",
       ["Same", "Gateway: S3/DynamoDB only, free. Interface (PrivateLink): most services, hourly + per-GB",
        "Interface is free", "Gateway is slower"],
       1, "Use gateway endpoints wherever offered (free); interface endpoints "
          "for everything else private.",
       ("amazon", "microsoft", "oracle")),
    # ---- L7: nacl-sg ----
    _q("aws-m4-l7-q1", "aws-m4-l7", "iam-vpc", 1,
       "Security group vs NACL — level?",
       ["Both instance-level", "SG: instance (ENI). NACL: subnet.",
        "Both subnet-level", "SG: region"],
       1, "SGs protect instances; NACLs guard whole subnets. Layer them.",
       ("tcs", "infosys")),
    _q("aws-m4-l7-q2", "aws-m4-l7", "iam-vpc", 2,
       "NACLs are stateless. Consequence?",
       ["Faster", "You must allow return traffic explicitly (ephemeral ports 1024-65535)",
        "Cheaper", "No rules needed"],
       1, "Unlike SGs, NACLs need inbound AND outbound rules — responses don't "
          "get a free pass.",
       ("amazon", "accenture")),
    _q("aws-m4-l7-q3", "aws-m4-l7", "iam-vpc", 3,
       "Block one malicious IP for an entire subnet. Which tool?",
       ["Security group", "NACL deny rule (SGs can't deny)",
        "IAM policy", "WAF only"],
       1, "Explicit denies are NACL territory. SGs are allow-only.",
       ("amazon", "wipro", "hcl")),
    _q("aws-m4-l7-q4", "aws-m4-l7", "iam-vpc", 5,
       "NACL rule numbers 100 (allow 443) and 200 (* deny). HTTPS packet arrives. Result?",
       ["Denied", "Allowed — lowest-numbered matching rule wins",
        "Random", "Dropped silently always"],
       1, "NACLs evaluate in rule-number order; first match decides. Number "
          "your rules with gaps (100, 200) for inserts.",
       ("amazon", "tcs", "cisco")),
    _q("aws-m4-l7-q5", "aws-m4-l7", "iam-vpc", 7,
       "Default NACL vs custom NACL?",
       ["Same", "Default allows all in/out (like an open door); custom denies all until you add rules",
        "Custom allows all", "Default denies all"],
       1, "Custom NACLs start closed — you build up. Default NACL starts open "
          "— tighten it or replace it.",
       ("amazon", "cognizant", "deloitte")),
    _q("aws-m4-l7-q6", "aws-m4-l7", "iam-vpc", 9,
       "Layered defense for a public web app — order from edge inward?",
       ["SG → NACL → WAF", "WAF/Shield (edge) → NACL (subnet) → SG (instance) → OS/app",
        "NACL only", "WAF only"],
       1, "Defense in depth: each layer catches what the outer missed, with "
          "increasing precision inward.",
       ("amazon", "atlassian", "phonepe")),
    # ================= M5: RDS & Monitoring =================
    # ---- L1: rds-basics ----
    _q("aws-m5-l1-q1", "aws-m5-l1", "rds-cloudwatch", 1,
       "What is Amazon RDS?",
       ["NoSQL store", "Managed relational database service (MySQL, Postgres, Aurora...)",
        "File storage", "A queue"],
       1, "RDS handles provisioning, patching, backups. You handle schema and "
          "queries. No SSH to the host.",
       ("tcs", "infosys", "wipro")),
    _q("aws-m5-l1-q2", "aws-m5-l1", "rds-cloudwatch", 2,
       "RDS Multi-AZ is primarily for:",
       ["Read scaling", "Automatic failover / high availability",
        "Backups", "Cheaper storage"],
       1, "Multi-AZ = synchronous standby for failover. Read scaling is what "
          "read replicas are for.",
       ("amazon", "accenture")),
    _q("aws-m5-l1-q3", "aws-m5-l1", "rds-cloudwatch", 3,
       "What is Aurora?",
       ["A cache", "AWS's cloud-native relational engine — up to 5x MySQL throughput, auto-scaling storage",
        "A NoSQL DB", "A backup tool"],
       1, "Aurora separates compute and storage (6 copies across 3 AZs), "
          "scales storage to 128 TB automatically.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m5-l1-q4", "aws-m5-l1", "rds-cloudwatch", 5,
       "Can you SSH into an RDS instance?",
       ["Yes, with the key pair", "No — managed service, no host access by design",
        "Yes, via bastion", "Only Aurora"],
       1, "No host access is the trade for managed patching/backups. Need OS "
          "control? Run the DB on EC2 yourself.",
       ("amazon", "microsoft", "oracle")),
    _q("aws-m5-l1-q5", "aws-m5-l1", "rds-cloudwatch", 7,
       "Aurora Backtrack — what is it?",
       ["A backup", "Rewind the database to a point in time (seconds ago) without restoring from backup",
        "A replica", "A log"],
       1, "Backtrack moves the DB clock backward in-place — perfect for "
          "'oops' recovery without a restore window.",
       ("amazon", "flipkart", "swiggy")),
    _q("aws-m5-l1-q6", "aws-m5-l1", "rds-cloudwatch", 9,
       "Global SaaS needs <1s cross-region writes with MySQL compatibility. Pick?",
       ["RDS Multi-AZ", "Aurora Global Database — dedicated replication, typical <1s lag, fast failover",
        "Read replicas", "DynamoDB"],
       1, "Global Database uses storage-layer replication (not binlog), so "
          "lag stays minimal and failover is fast.",
       ("amazon", "atlassian", "phonepe")),
    # ---- L2: dynamodb ----
    _q("aws-m5-l2-q1", "aws-m5-l2", "rds-cloudwatch", 1,
       "What is DynamoDB?",
       ["SQL database", "Serverless NoSQL key-value/document store, single-digit ms at any scale",
        "File system", "Cache only"],
       1, "No servers, no patching. Design the keys right and it scales "
          "infinitely.",
       ("tcs", "infosys")),
    _q("aws-m5-l2-q2", "aws-m5-l2", "rds-cloudwatch", 2,
       "DynamoDB partition key + optional sort key. Why does key design matter so much?",
       ["It doesn't", "Keys determine data distribution — bad keys cause hot partitions and throttling",
        "Keys cost money", "Keys are optional"],
       1, "There is no query optimizer to save you. Key design IS schema "
          "design in DynamoDB.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m5-l2-q3", "aws-m5-l2", "rds-cloudwatch", 3,
       "On-demand vs provisioned capacity?",
       ["Same price", "On-demand: pay per request (spiky). Provisioned: reserve throughput (steady + cheaper)",
        "On-demand is slower", "Provisioned is serverless"],
       1, "Match the mode to the traffic shape; provisioned + auto scaling "
          "wins for predictable loads.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m5-l2-q4", "aws-m5-l2", "rds-cloudwatch", 5,
       "Your table throttles though total throughput is under limits. Likely cause?",
       ["Too much data", "Hot partition — one key gets most traffic; redistribute keys or use DAX/write sharding",
        "Too few items", "Wrong region"],
       1, "Throughput is per-partition. A celebrity key (status=active) "
          "saturates its partition while others idle.",
       ("amazon", "flipkart", "dream11")),
    _q("aws-m5-l2-q5", "aws-m5-l2", "rds-cloudwatch", 7,
       "Sessions must auto-expire after 24h with zero cleanup code. How?",
       ["Cron Lambda", "DynamoDB TTL — items auto-delete after the timestamp, free",
        "Manual deletes", "Smaller table"],
       1, "TTL deletes are free and automatic — the classic session/cart "
          "expiry pattern.",
       ("amazon", "swiggy", "zomato")),
    _q("aws-m5-l2-q6", "aws-m5-l2", "rds-cloudwatch", 9,
       "Need strongly consistent multi-item writes across tables (order + inventory). DynamoDB can?",
       ["No", "Yes — TransactWriteItems gives ACID transactions across items/tables",
        "Only with RDS", "Eventual only"],
       1, "DynamoDB transactions provide all-or-nothing writes — with the "
          "throughput cost transactions carry.",
       ("amazon", "microsoft", "razorpay")),
    # ---- L3: read-replicas ----
    _q("aws-m5-l3-q1", "aws-m5-l3", "rds-cloudwatch", 1,
       "What are RDS read replicas for?",
       ["Failover", "Scaling READ traffic (reporting, analytics) off the primary",
        "Backups", "Writes"],
       1, "Async copies serve reads. Writes still go to the primary. "
          "Failover is Multi-AZ's job.",
       ("tcs", "infosys")),
    _q("aws-m5-l3-q2", "aws-m5-l3", "rds-cloudwatch", 2,
       "Read replica lag means:",
       ["No lag ever", "Replicas may be seconds behind — don't read-your-write from them",
        "They are faster", "They store more"],
       1, "Async = eventual. Critical reads (just wrote, now read) must hit "
          "the primary.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m5-l3-q3", "aws-m5-l3", "rds-cloudwatch", 3,
       "How many read replicas for RDS MySQL / Aurora?",
       ["1 / 1", "5 / 15", "Unlimited", "0"],
       1, "RDS: up to 5 async replicas. Aurora: up to 15 with <10ms typical "
          "lag (storage-layer replication).",
       ("amazon", "hcl", "tcs")),
    _q("aws-m5-l3-q4", "aws-m5-l3", "rds-cloudwatch", 5,
       "Can you promote a read replica to standalone?",
       ["No", "Yes — promote-read-replica detaches it into an independent DB",
        "Only Aurora", "Only with downtime"],
       1, "Promotion is the DR drill: replica becomes writable standalone. "
          "Plan for the brief I/O suspension.",
       ("amazon", "cognizant", "deloitte")),
    _q("aws-m5-l3-q5", "aws-m5-l3", "rds-cloudwatch", 7,
       "Aurora failover time vs RDS Multi-AZ?",
       ["Same", "Aurora ~30s (reader promotion), RDS Multi-AZ ~1-2 min (DNS flip)",
        "Aurora slower", "Both instant"],
       1, "Aurora's shared storage means failover is just reader promotion — "
          "no storage to remount.",
       ("amazon", "flipkart", "phonepe")),
    _q("aws-m5-l3-q6", "aws-m5-l3", "rds-cloudwatch", 9,
       "Analytics team runs heavy reports crushing prod OLTP. Best fix preserving freshness?",
       ["Bigger primary", "Aurora read replica (or RDS replica) for analytics — isolate workloads",
        "Cache everything", "More connections"],
       1, "Workload isolation: OLTP on primary, OLAP on replicas. Aurora "
          "replicas share storage so lag is tiny.",
       ("amazon", "atlassian", "swiggy")),
    # ---- L4: cloudwatch ----
    _q("aws-m5-l4-q1", "aws-m5-l4", "rds-cloudwatch", 1,
       "What is CloudWatch?",
       ["A database", "AWS monitoring: metrics, alarms, logs, dashboards, events",
        "A CDN", "IAM tool"],
       1, "The observability hub — numbers (metrics), thresholds (alarms), "
          "text (logs), reactions (events).",
       ("tcs", "infosys")),
    _q("aws-m5-l4-q2", "aws-m5-l4", "rds-cloudwatch", 2,
       "CloudWatch alarm states?",
       ["Up/Down", "OK, ALARM, INSUFFICIENT_DATA",
        "Red/Green", "On/Off"],
       1, "INSUFFICIENT_DATA (not enough points yet) trips up beginners — "
          "don't treat it as OK.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m5-l4-q3", "aws-m5-l4", "rds-cloudwatch", 3,
       "Where does Lambda's print() output go?",
       ["Nowhere", "CloudWatch Logs — automatic log group per function",
        "S3", "SNS"],
       1, "Zero-config logging. Add structured JSON logs and query with "
          "CloudWatch Logs Insights.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m5-l4-q4", "aws-m5-l4", "rds-cloudwatch", 5,
       "Alert fatigue: 50 alarms fire during one outage. Fix?",
       ["More alarms", "Composite alarms — fire the parent only when the pattern matches",
        "Delete alarms", "Email filters"],
       1, "Composite alarms express 'the site is down' instead of 50 "
          "symptoms. Alert on symptoms, page on causes.",
       ("amazon", "phonepe", "razorpay")),
    _q("aws-m5-l4-q5", "aws-m5-l4", "rds-cloudwatch", 7,
       "Metric has daily seasonality; static thresholds false-alarm nightly. Better?",
       ["Higher threshold", "Anomaly detection — ML bands adapt to the pattern",
        "More datapoints", "Disable nights"],
       1, "Anomaly detection learns the shape (daily/weekly) and alarms on "
          "deviation, not absolute values.",
       ("amazon", "microsoft", "swiggy")),
    _q("aws-m5-l4-q6", "aws-m5-l4", "rds-cloudwatch", 9,
       "'The API is down' — but all infra alarms are green. What's missing?",
       ["More metrics", "Synthetics canaries — scripted user journeys that catch user-visible breakage",
        "More logs", "Bigger instances"],
       1, "Infra-green ≠ user-healthy. Canaries probe the real user path "
          "(login → checkout) continuously.",
       ("amazon", "atlassian", "cred")),
    # ---- L5: cloudtrail ----
    _q("aws-m5-l5-q1", "aws-m5-l5", "rds-cloudwatch", 1,
       "What does CloudTrail log?",
       ["CPU metrics", "Every AWS API call — who did what, when, from where",
        "Application logs", "Billing only"],
       1, "The audit camera: management events (and optionally data events) "
          "for forensics and compliance.",
       ("tcs", "infosys")),
    _q("aws-m5-l5-q2", "aws-m5-l5", "rds-cloudwatch", 2,
       "CloudTrail vs CloudWatch — difference?",
       ["Same", "Trail = API audit log (control plane). CloudWatch = resource metrics/logs (data plane).",
        "Trail is faster", "Watch is cheaper"],
       1, "Trail answers 'who changed the security group?'; CloudWatch "
          "answers 'why is CPU at 100%?'.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m5-l5-q3", "aws-m5-l5", "rds-cloudwatch", 3,
       "How do you prove CloudTrail logs weren't tampered with?",
       ["Trust AWS", "Enable log file validation — digest files detect tampering",
        "Encryption", "Versioning"],
       1, "Validation writes signed digests; any modification breaks the "
          "chain. Required for serious audits.",
       ("amazon", "hcl", "deloitte")),
    _q("aws-m5-l5-q4", "aws-m5-l5", "rds-cloudwatch", 5,
       "'Alert me if anyone logs in as root.' How?",
       ["Impossible", "CloudTrail → CloudWatch Logs metric filter on root usage → alarm → SNS",
        "IAM policy", "GuardDuty only"],
       1, "The classic pipeline: Trail captures, metric filter counts, alarm "
          "pages. Set it up day one.",
       ("amazon", "tcs", "cognizant")),
    _q("aws-m5-l5-q5", "aws-m5-l5", "rds-cloudwatch", 7,
       "What does AWS Config add on top of CloudTrail?",
       ["Nothing", "Configuration history + compliance rules ('is this SG compliant right now?')",
        "Faster logs", "Cheaper storage"],
       1, "Trail = event stream; Config = state timeline + rule engine. "
          "'What changed?' vs 'Is it compliant?'",
       ("amazon", "microsoft", "oracle")),
    _q("aws-m5-l5-q6", "aws-m5-l5", "rds-cloudwatch", 9,
       "Incident: 'which IAM role assumed at 3 AM modified prod SGs from an unusual IP?' Data sources?",
       ["CloudWatch metrics", "CloudTrail (API calls with identity + IP + time) + GuardDuty findings for anomaly context",
        "VPC Flow Logs only", "Billing"],
       1, "Trail gives the who/when/where; GuardDuty adds 'this IP is a known "
          "threat' context. Correlate both.",
       ("amazon", "atlassian", "phonepe")),
    # ---- L6: cost-optimization ----
    _q("aws-m5-l6-q1", "aws-m5-l6", "rds-cloudwatch", 1,
       "First step of AWS cost optimization?",
       ["Buy Reserved Instances", "Visibility: tag resources, use Cost Explorer to see WHERE money goes",
        "Delete everything", "Change region"],
       1, "You can't optimize what you can't see. Tags (team/env/project) "
          "make spend attributable.",
       ("tcs", "infosys")),
    _q("aws-m5-l6-q2", "aws-m5-l6", "rds-cloudwatch", 2,
       "Find wasted EBS volumes via CLI. Which filter?",
       ["In-use", "status=available (unattached volumes bill you for nothing)",
        "Encrypted", "gp3"],
       1, "'Available' = detached but billing. Snapshot-then-delete is the "
          "cleanup.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m5-l6-q3", "aws-m5-l6", "rds-cloudwatch", 3,
       "Your Java app runs fine on x86. Why try Graviton (ARM)?",
       ["Faster always", "~20-40% better price/performance for compatible workloads",
        "More RAM", "Required by AWS"],
       1, "Graviton c6g/m6g/r6g instances are simply cheaper per unit of "
          "work for most Linux workloads.",
       ("amazon", "hcl", "flipkart")),
    _q("aws-m5-l6-q4", "aws-m5-l6", "rds-cloudwatch", 5,
       "Bill spiked 3x overnight with no deploy. Most likely?",
       ["Price increase", "Orphaned/forgotten resources or a runaway process — check Cost Anomaly Detection + top services",
        "Currency change", "More users always"],
       1, "Mystery spikes are usually accidents: recursive Lambda, forgotten "
          "NAT/ELB, crypto-miner breach. Investigate, don't just pay.",
       ("amazon", "razorpay", "cred")),
    _q("aws-m5-l6-q5", "aws-m5-l6", "rds-cloudwatch", 7,
       "AWS Budgets vs Cost Anomaly Detection?",
       ["Same", "Budgets: thresholds you set (80% of $X). Anomaly Detection: ML spots unusual spend automatically",
        "Budgets are ML", "Anomaly is manual"],
       1, "Budgets = guardrails you define; Anomaly Detection = ML watchman "
          "for what you didn't predict.",
       ("amazon", "deloitte", "tcs")),
    _q("aws-m5-l6-q6", "aws-m5-l6", "rds-cloudwatch", 9,
       "FinOps monthly loop — correct order?",
       ["Buy → hope", "Visibility (tags/Explorer) → accountability (budgets per team) → optimization (right-size, commit) → repeat",
        "Delete → rebuild", "Ignore"],
       1, "Culture + process beats one-off cleanup. Monthly cadence keeps "
          "architecture drift from re-inflating the bill.",
       ("amazon", "atlassian", "swiggy")),
]
