"""Seed content: AWS — Module 1 (EC2 & Compute).

Part-file for the SkillForge curriculum seed. All content is original,
written for interview prep + AWS Solutions Architect Associate topics.
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
        id="aws-m1",
        domain_slug=DOMAIN_SLUG,
        slug="ec2-compute",
        name="EC2 & Compute",
        description=(
            "Virtual servers in the cloud: EC2 instances, AMIs, key pairs, "
            "security groups, EBS volumes, load balancers, auto scaling and "
            "pricing models. The heart of AWS compute."
        ),
        order_index=1,
        estimated_days=10,
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
# LESSONS — Module 1: EC2 & Compute
# ---------------------------------------------------------------------------

LESSONS = [
    CurriculumLesson(
        id="aws-m1-l1",
        module_id="aws-m1",
        slug="what-is-ec2",
        title="EC2 — Virtual Servers in the Cloud",
        content="""**EC2 (Elastic Compute Cloud)** gives you virtual machines — called
**instances** — that you can rent by the second. Think of it as ordering a
computer from a giant menu: pick CPU, RAM, storage and OS, and it is running
in about a minute.

```bash
# Launch an instance from the CLI (Ubuntu, t3.micro, in ap-south-1)
aws ec2 run-instances --image-id ami-0abcdef1234567890 \\
  --instance-type t3.micro --key-name my-key \\
  --security-group-ids sg-0123456789abcdef0
```

**Instance types** follow a pattern: `family + generation + size`.
- **General purpose** — `t3`, `m5` (balanced CPU/RAM; t3 is burstable, cheap).
- **Compute optimized** — `c5`, `c6g` (number crunching, gaming servers).
- **Memory optimized** — `r5`, `x1` (in-memory databases like Redis).
- **Storage optimized** — `i3`, `d2` (data warehouses, heavy disk I/O).
- **Accelerated** — `p3`, `g4dn` (GPUs for ML training).

The letter is the family, the number is the generation (bigger = newer),
and the suffix is the size (`nano` → `micro` → ... → `24xlarge`).

**Key idea for interviews:** EC2 is *resizable*. If traffic spikes, you do
not buy a server — you launch a bigger instance type or add more instances.
That elasticity is the whole point of the cloud.""",
        order_index=1,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m1-l2",
        module_id="aws-m1",
        slug="ami",
        title="AMIs — Golden Images",
        content="""An **AMI (Amazon Machine Image)** is a snapshot template used to
launch EC2 instances. It bundles the OS, installed software, and
configuration — so every instance launched from it is identical.

**Why teams love AMIs:** bake your app + dependencies into one AMI ("golden
image"), then launch 50 identical servers in minutes. No more "works on my
machine" drift between environments.

```bash
# Create your own AMI from a running instance
aws ec2 create-image --instance-id i-1234567890abcdef0 \\
  --name "web-server-v2" --description "Nginx + app, hardened"
```

**AMI types:**
- **EBS-backed** — root volume is EBS; can stop/start; most common.
- **Instance-store backed** — root is ephemeral storage; cannot stop, only
  terminate; faster but data is lost on stop.

**Sharing:** AMIs can be private (your account), shared with specific
accounts, or public (AWS Marketplace). Copying an AMI to another region is
how you deploy the same image worldwide.

**Interview trap:** "Can you stop an instance-store backed instance?" No —
stopping requires persistent root storage, which only EBS-backed instances
have. You can only terminate and relaunch.""",
        order_index=2,
        estimated_minutes=25,
    ),
    CurriculumLesson(
        id="aws-m1-l3",
        module_id="aws-m1",
        slug="key-pairs",
        title="Key Pairs — SSH Access",
        content="""EC2 instances have **no password login by default**. You access them
with an SSH **key pair**: a public key AWS stores, and a private `.pem` file
you keep.

```bash
# Connect to your instance
chmod 400 my-key.pem            # private key must not be world-readable
ssh -i my-key.pem ubuntu@13.232.10.5
```

**Rules that interviewers love:**
1. You **choose the key pair at launch** — you cannot add a new key pair to a
   running instance via the console (you can manually edit
   `~/.ssh/authorized_keys`, but AWS will not do it for you).
2. **Lose the .pem?** For EBS-backed instances you can stop the instance,
   detach the root volume, attach it to another instance, inject a new key,
   and reattach. For instance-store, the key is gone forever.
3. Never commit `.pem` files to git. Ever.

**Best practice:** use **EC2 Instance Connect** or **Systems Manager Session
Manager** instead of raw SSH — no key management at all, and every session
is logged to CloudTrail.""",
        order_index=3,
        estimated_minutes=20,
    ),
    CurriculumLesson(
        id="aws-m1-l4",
        module_id="aws-m1",
        slug="security-groups",
        title="Security Groups — Virtual Firewalls",
        content="""A **security group** is a stateful virtual firewall attached to EC2
instances. Rules are simple:

- **Inbound** rules control what traffic can *reach* the instance.
- **Outbound** rules control what traffic can *leave* (default: allow all).
- **Stateful**: if you allow inbound on port 80, the response is automatically
  allowed out — no need for a matching outbound rule.
- **Default deny**: anything not explicitly allowed is blocked.

```bash
# Allow SSH from your IP and HTTP from anywhere
aws ec2 authorize-security-group-ingress --group-id sg-0123456789abcdef0 \\
  --protocol tcp --port 22 --cidr 203.0.113.5/32
aws ec2 authorize-security-group-ingress --group-id sg-0123456789abcdef0 \\
  --protocol tcp --port 80 --cidr 0.0.0.0/0
```

**Security group vs NACL (classic interview question):**
| | Security Group | NACL |
|---|---|---|
| Level | Instance (ENI) | Subnet |
| Stateful? | Yes | No (need both directions) |
| Rules | Allow only | Allow AND deny |
| Evaluation | All rules together | Lowest-numbered rule wins |

**Golden rule:** one security group per role — `web-sg` (80/443),
`app-sg` (8080 from web-sg), `db-sg` (3306 from app-sg). Reference other
security groups by ID instead of IP ranges so auto-scaled instances keep
working.""",
        order_index=4,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m1-l5",
        module_id="aws-m1",
        slug="ebs-storage",
        title="EBS — Block Storage Volumes",
        content="""**EBS (Elastic Block Store)** is network-attached disk for EC2 — the
"hard drive" of your instance. One EBS volume lives in **one Availability
Zone** and can attach to **one instance at a time** (except `io1`/`io2` with
Multi-Attach).

**Volume types:**
- **gp3 / gp2** — general purpose SSD; gp3 lets you tune IOPS separately
  (cheaper than gp2 for the same performance).
- **io1 / io2** — provisioned IOPS SSD; databases that need guaranteed
  throughput (io2: 99.999% durability).
- **st1** — throughput-optimized HDD; big data, logs (cannot be boot).
- **sc1** — cold HDD; cheapest, infrequent access (cannot be boot).

```bash
# Snapshot a volume (backups are incremental — only changed blocks stored)
aws ec2 create-snapshot --volume-id vol-0123456789abcdef0 \\
  --description "pre-deploy backup"
```

**Snapshots** are the killer feature: point-in-time backups stored in S3,
incremental forever. You can copy snapshots across regions for disaster
recovery, or create a bigger/faster volume from a snapshot to resize.

**Instance store** is the opposite: physically attached SSDs, extremely fast,
but **ephemeral** — data dies on stop/terminate. Use for caches and temp
files, never for anything you cannot lose.""",
        order_index=5,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m1-l6",
        module_id="aws-m1",
        slug="elb",
        title="Elastic Load Balancing",
        content="""An **Elastic Load Balancer** spreads incoming traffic across healthy
targets (EC2 instances, IPs, Lambda). It also does **health checks** and
stops sending traffic to sick instances.

**Three flavors (know all three for the exam):**
- **ALB (Application)** — Layer 7 (HTTP/HTTPS). Path/host-based routing
  (`/api/*` → backend, `/img/*` → CDN), WebSockets, user authentication.
  The default choice for web apps.
- **NLB (Network)** — Layer 4 (TCP/UDP). Ultra-low latency, millions of
  requests/sec, **static IP / Elastic IP**, preserves source IP. Gaming,
  IoT, anything latency-critical.
- **GWLB (Gateway)** — Layer 3; chains third-party virtual appliances
  (firewalls, IDS) transparently.

```bash
# Target group + ALB listener in one line each
aws elbv2 create-target-group --name web-tg --protocol HTTP --port 80 \\
  --vpc-id vpc-0123456789abcdef0
```

**Sticky sessions** (ALB) pin a user to one target — needed for apps that
keep session state locally (though stateless + ElastiCache is the better
design). **Cross-zone load balancing** spreads evenly across AZs (on by
default for ALB, off and paid for NLB).

**Interview line:** "ALB for HTTP smarts, NLB for raw speed and static IPs,
GWLB for security appliances." """,
        order_index=6,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m1-l7",
        module_id="aws-m1",
        slug="auto-scaling",
        title="Auto Scaling Groups",
        content="""An **Auto Scaling Group (ASG)** keeps the right number of EC2
instances running: it launches more when load rises and terminates extras
when it falls, always respecting your min/max/desired counts.

```bash
# ASG: 2 to 6 instances, target 50% CPU
aws autoscaling create-auto-scaling-group \\
  --auto-scaling-group-name web-asg \\
  --launch-template LaunchTemplateName=web-lt,Version=1 \\
  --min-size 2 --max-size 6 --desired-capacity 2 \\
  --vpc-zone-identifier "subnet-aaa,subnet-bbb"
```

**Scaling policies:**
- **Target tracking** — "keep CPU at 50%"; simplest, most common.
- **Step / simple scaling** — CloudWatch alarm → add N instances.
- **Scheduled** — "scale up every weekday at 9 AM" (predictable traffic).
- **Predictive** — ML forecasts daily/weekly patterns.

**Launch templates** (modern) replaced launch configurations: they define
AMI, instance type, key pair, security groups, user data. Versioned, so you
can roll back a bad deploy.

**Exam favorite:** ASG spans **multiple AZs** for high availability. If one
AZ fails, instances relaunch in the survivors. Combine ASG + ALB and you
have a self-healing web tier — the classic "highly available architecture"
answer.""",
        order_index=7,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="aws-m1-l8",
        module_id="aws-m1",
        slug="pricing-models",
        title="EC2 Pricing Models",
        content="""Picking the wrong pricing model is the #1 way teams burn money.
Four models:

1. **On-Demand** — pay per second, no commitment. Flexible, most expensive.
   Good for: spiky, unpredictable workloads.
2. **Reserved Instances (1 or 3 yr)** — up to 72% off for a commitment.
   Good for: steady-state apps, databases.
3. **Savings Plans** — like Reserved but flexible across instance
   families/regions; commit to $X/hour of usage.
4. **Spot Instances** — bid on spare capacity, up to 90% off — but AWS can
   reclaim them with **2 minutes notice**. Good for: batch jobs, CI,
   anything fault-tolerant.

**Dedicated Hosts / Dedicated Instances** — physical isolation for
compliance/licensing (BYOL). Most expensive.

```text
Interviewer: "Your nightly batch job takes 3 hours and can tolerate
interruptions. Cheapest option?"
You: "Spot Instances — up to 90% off, and a 2-minute interruption warning
is fine for a retryable batch job."
```

**Rule of thumb:** On-Demand for experiments, Reserved/Savings Plans for the
always-on baseline, Spot for everything interruptible. Right-size first —
half of cloud waste is oversized instances.""",
        order_index=8,
        estimated_minutes=25,
    ),
]


def _q(qid, lid, diff, prompt, choices, ans, expl, tags):
    return _mkq(qid, lid, "ec2-compute", diff, prompt, choices, ans, expl, tags)


QUESTIONS = [
    # ---- L1: what-is-ec2 ----
    _q("aws-m1-l1-q1", "aws-m1-l1", 1,
       "What does EC2 stand for?",
       ["Elastic Compute Cloud", "Elastic Container Cluster",
        "Enterprise Compute Center", "External Cloud Compute"],
       0, "EC2 = Elastic Compute Cloud — resizable virtual servers in the cloud.",
       ("tcs", "infosys", "wipro")),
    _q("aws-m1-l1-q2", "aws-m1-l1", 2,
       "Which EC2 instance family is best for an in-memory cache like Redis?",
       ["c5 (compute optimized)", "r5 (memory optimized)",
        "i3 (storage optimized)", "p3 (accelerated computing)"],
       1, "Memory-optimized (r5, x1) instances pack the most RAM per vCPU — "
          "ideal for in-memory databases and caches.",
       ("amazon", "flipkart", "tcs")),
    _q("aws-m1-l1-q3", "aws-m1-l1", 3,
       "What does the 't3.micro' name tell you?",
       ["t = turbo, 3 vCPUs, micro region", "t3 family, 3rd generation, micro size",
        "3 TB storage, micro network", "Tier-3 support, micro billing"],
       1, "Family letter (t) + generation (3) + size (micro). t3 = burstable "
          "general-purpose, 3rd generation.",
       ("amazon", "accenture")),
    _q("aws-m1-l1-q4", "aws-m1-l1", 5,
       "Your API gets 10x traffic for 2 hours daily. Cheapest resilient design?",
       ["One xlarge On-Demand instance", "ASG with On-Demand baseline + Spot for spikes",
        "Biggest instance you can afford", "Reserved Instances for peak capacity"],
       1, "Cover the steady baseline with On-Demand/Reserved and let an Auto "
          "Scaling Group add Spot instances for the spike — cheap and elastic.",
       ("amazon", "swiggy", "razorpay")),
    _q("aws-m1-l1-q5", "aws-m1-l1", 7,
       "Why would you choose c6g over c5 for a CPU-bound workload?",
       ["c6g has more RAM", "c6g uses Graviton ARM chips — better price/performance",
        "c6g has GPUs", "c6g is Intel-based"],
       1, "c6g runs on AWS Graviton (ARM) processors, typically ~20-40% better "
          "price/performance than Intel-based c5 for compatible workloads.",
       ("amazon", "atlassian", "microsoft")),
    _q("aws-m1-l1-q6", "aws-m1-l1", 9,
       "A burstable t3 instance earns CPU credits. What happens when credits run out?",
       ["Instance terminates", "CPU is throttled to baseline performance",
        "Instance reboots automatically", "Nothing — credits are unlimited"],
       1, "T3 instances burst above baseline using earned credits; with zero "
          "credits they are throttled to baseline. Unlimited mode can borrow "
          "future credits for a surcharge.",
       ("amazon", "google")),
    # ---- L2: ami ----
    _q("aws-m1-l2-q1", "aws-m1-l2", 1,
       "What is an AMI?",
       ["A template (OS + software + config) used to launch EC2 instances",
        "An AWS billing report", "A type of load balancer",
        "A database backup format"],
       0, "AMI = Amazon Machine Image. Launch any number of identical instances "
          "from one golden image.",
       ("tcs", "infosys")),
    _q("aws-m1-l2-q2", "aws-m1-l2", 2,
       "Which statement about EBS-backed AMIs is TRUE?",
       ["They cannot be stopped", "Their root volume persists — instances can stop/start",
        "They are faster than instance-store", "They cannot be shared"],
       1, "EBS-backed AMIs use persistent EBS root volumes, so instances can be "
          "stopped and started. Instance-store roots are ephemeral.",
       ("amazon", "wipro", "cognizant")),
    _q("aws-m1-l2-q3", "aws-m1-l2", 3,
       "How do you deploy the same application image to eu-west-1 and ap-south-1?",
       ["Rebuild the image in each region", "Copy the AMI to the other region",
        "AMIs are global automatically", "Use S3 cross-region replication"],
       1, "AMIs are regional. Copy the AMI to each target region, then launch "
          "instances from the regional copy.",
       ("amazon", "accenture", "hcl")),
    _q("aws-m1-l2-q4", "aws-m1-l2", 5,
       "Can you STOP an instance launched from an instance-store backed AMI?",
       ["Yes, anytime", "No — only terminate; the root disk is ephemeral",
        "Yes, but data is lost", "Only with a support ticket"],
       1, "Instance-store roots live on ephemeral host storage. Stop requires a "
          "persistent root (EBS). Classic interview trap.",
       ("amazon", "microsoft", "oracle")),
    _q("aws-m1-l2-q5", "aws-m1-l2", 7,
       "Your golden AMI pipeline is slow because every build reinstalls packages. Best fix?",
       ["Use bigger instances", "Bake dependencies into the AMI once; keep app code in user data or EBS",
        "Stop using AMIs", "Use Spot instances"],
       1, "Bake the slow-changing layer (OS + dependencies) into the AMI; inject "
          "fast-changing app code at boot via user data. Fast builds, consistent base.",
       ("amazon", "flipkart", "swiggy")),
    _q("aws-m1-l2-q6", "aws-m1-l2", 9,
       "Why do teams version AMIs (web-v1, web-v2) instead of updating instances in place?",
       ["AMIs are cheaper", "Immutable infrastructure — rollbacks are instant and deploys are reproducible",
        "AWS requires it", "Instances cannot be updated"],
       1, "Immutable infrastructure: every deploy is a fresh, tested image. Bad "
          "deploy? Point the ASG back at web-v1 — instant rollback, zero drift.",
       ("amazon", "atlassian", "cred")),
    # ---- L3: key-pairs ----
    _q("aws-m1-l3-q1", "aws-m1-l3", 1,
       "How do you log in to an EC2 instance by default?",
       ["Username + password", "SSH with a private key (.pem) file",
        "AWS console password", "OAuth token"],
       1, "EC2 uses key pairs: AWS holds the public key, you keep the private "
          ".pem and SSH with it. No passwords by default.",
       ("tcs", "infosys")),
    _q("aws-m1-l3-q2", "aws-m1-l3", 2,
       "You lost your .pem file for a running EBS-backed instance. What can you do?",
       ["Nothing — terminate it", "Stop it, detach root volume, attach to another instance, inject a new key, reattach",
        "Download it again from the console", "Reset via IAM"],
       1, "AWS never stores your private key. The volume-detach dance lets you "
          "add a new public key to authorized_keys offline.",
       ("amazon", "wipro")),
    _q("aws-m1-l3-q3", "aws-m1-l3", 3,
       "Why does `ssh -i key.pem` fail with 'bad permissions'?",
       ["Wrong username", "The .pem is readable by others — chmod 400 it",
        "Port 22 closed", "Wrong region"],
       1, "SSH refuses keys that are group/world-readable. `chmod 400` restricts "
          "to owner-only.",
       ("amazon", "accenture")),
    _q("aws-m1-l3-q4", "aws-m1-l3", 5,
       "Can you change the key pair of a RUNNING instance from the AWS console?",
       ["Yes, anytime", "No — key pair is set at launch; edit ~/.ssh/authorized_keys manually instead",
        "Yes, with a reboot", "Only for Windows instances"],
       1, "Console key-pair selection happens only at launch. For running "
          "instances, add keys via authorized_keys (or use Session Manager).",
       ("amazon", "microsoft")),
    _q("aws-m1-l3-q5", "aws-m1-l3", 7,
       "Best practice to avoid managing SSH keys across a 200-instance fleet?",
       ["One shared .pem for all", "Systems Manager Session Manager — browser/CLI shell, no keys, CloudTrail logging",
        "Disable SSH", "Email keys to engineers"],
       1, "Session Manager gives audited shell access via IAM — no keys to "
          "rotate, leak, or lose, and every command is logged.",
       ("amazon", "phonepe", "razorpay")),
    _q("aws-m1-l3-q6", "aws-m1-l3", 9,
       "An auditor asks: 'who SSHed into prod last Tuesday?' With raw key pairs you cannot answer well. Why is Session Manager better?",
       ["It is faster", "Sessions are IAM-authenticated and logged to CloudTrail/S3 with user identity and commands",
        "It uses stronger encryption", "It works without internet"],
       1, "Shared .pem files give zero attribution. Session Manager ties every "
          "session to an IAM identity with a full audit trail.",
       ("amazon", "cred", "atlassian")),
    # ---- L4: security-groups ----
    _q("aws-m1-l4-q1", "aws-m1-l4", 1,
       "What is a security group?",
       ["A stateful virtual firewall controlling traffic to EC2 instances",
        "An IAM user group", "A VPN connection", "A billing alert"],
       0, "Security groups filter traffic at the instance (ENI) level with "
          "allow-only rules; return traffic is automatic (stateful).",
       ("tcs", "infosys", "wipro")),
    _q("aws-m1-l4-q2", "aws-m1-l4", 2,
       "Security groups are stateful. What does that mean?",
       ["Rules apply to all AZs", "If inbound is allowed, the response is automatically allowed out",
        "Rules sync across regions", "They remember deleted rules"],
       1, "Stateful = return traffic is auto-allowed. NACLs are stateless and "
          "need explicit rules in both directions.",
       ("amazon", "accenture", "hcl")),
    _q("aws-m1-l4-q3", "aws-m1-l4", 3,
       "Can a security group DENY traffic?",
       ["Yes, with deny rules", "No — allow rules only; everything else is implicitly denied",
        "Yes, but only outbound", "Only with a NACL attached"],
       1, "Security groups are allow-lists. Need an explicit deny? That is what "
          "NACLs (or WAF) are for.",
       ("amazon", "tcs", "cognizant")),
    _q("aws-m1-l4-q4", "aws-m1-l4", 5,
       "Your app tier should accept traffic ONLY from the web tier's auto-scaled instances. Best rule?",
       ["Allow 0.0.0.0/0 on port 8080", "Allow the web tier's security group ID as the source",
        "Allow the VPC CIDR", "Open port 8080 to the office IP"],
       1, "Referencing the source security group ID keeps working as instances "
          "scale in/out — IPs would go stale.",
       ("amazon", "flipkart", "swiggy")),
    _q("aws-m1-l4-q5", "aws-m1-l4", 7,
       "NACL rule 100 allows port 80, rule 50 denies all. A packet arrives on port 80. Result?",
       ["Allowed (port 80 matches)", "Denied — NACLs evaluate lowest-numbered rule first",
        "Allowed — allow beats deny", "Dropped randomly"],
       1, "NACLs are stateless and ordered: the lowest-numbered matching rule "
          "wins. Rule 50 denies everything before rule 100 is read.",
       ("amazon", "microsoft", "oracle")),
    _q("aws-m1-l4-q6", "aws-m1-l4", 9,
       "Design: web → app → db tiers. Which security group layout follows least privilege?",
       ["One SG for all, open all ports", "web-sg (80/443 world), app-sg (8080 from web-sg), db-sg (5432 from app-sg)",
        "Three SGs all open to 0.0.0.0/0", "No SGs, rely on NACLs"],
       1, "Tiered SGs referencing each other: each tier only talks to its "
          "neighbors, and the DB is unreachable from the internet.",
       ("amazon", "atlassian", "phonepe")),
    # ---- L5: ebs-storage ----
    _q("aws-m1-l5-q1", "aws-m1-l5", 1,
       "What is EBS?",
       ["Network-attached block storage for EC2 (a virtual hard drive)",
        "Object storage like S3", "A database service", "A CDN"],
       0, "EBS volumes attach to EC2 instances in the same AZ and persist "
          "independently of the instance.",
       ("tcs", "infosys")),
    _q("aws-m1-l5-q2", "aws-m1-l5", 2,
       "EBS snapshots are stored where, and how?",
       ["On the instance", "In S3, incrementally (only changed blocks)",
        "In Glacier only", "On a second EBS volume"],
       1, "Snapshots live in S3 and are incremental — the first is full, later "
          "ones store only changed blocks.",
       ("amazon", "wipro", "accenture")),
    _q("aws-m1-l5-q3", "aws-m1-l5", 3,
       "Can one EBS volume attach to instances in two different AZs?",
       ["Yes", "No — a volume lives in a single AZ (snapshot to move it)",
        "Yes, with Multi-Attach", "Only gp3 volumes"],
       1, "EBS is AZ-scoped. Take a snapshot and restore it in the other AZ to "
          "'move' data. (io1/io2 Multi-Attach is same-AZ only.)",
       ("amazon", "hcl", "tcs")),
    _q("aws-m1-l5-q4", "aws-m1-l5", 5,
       "Your database needs 10,000 provisioned IOPS. Which volume type?",
       ["gp3", "io2", "st1", "sc1"],
       1, "io1/io2 are provisioned-IOPS SSDs for latency-critical databases. "
          "gp3 is bursty general purpose; st1/sc1 are HDD (no boot).",
       ("amazon", "flipkart", "paytm")),
    _q("aws-m1-l5-q5", "aws-m1-l5", 7,
       "Why is gp3 usually cheaper than gp2 for the same workload?",
       ["It is slower", "gp3 decouples IOPS/throughput from size — you pay for baseline + only the IOPS you need",
        "gp3 has no snapshots", "gp3 is HDD"],
       1, "gp2 bundles IOPS with volume size (bigger disk = more IOPS). gp3 "
          "gives 3,000 IOPS free and lets you provision extra independently.",
       ("amazon", "microsoft", "swiggy")),
    _q("aws-m1-l5-q6", "aws-m1-l5", 9,
       "Disaster recovery plan: EBS volumes in ap-south-1. RTO 1 hour in eu-west-1. Best approach?",
       ["Manual copies", "Automated snapshots copied cross-region; restore volumes + relaunch from AMIs in eu-west-1",
        "EBS replication", "Instance store"],
       1, "Snapshots are the DR primitive: schedule them, copy cross-region, "
          "and rebuild. There is no live EBS cross-region replication.",
       ("amazon", "atlassian", "cred")),
    # ---- L6: elb ----
    _q("aws-m1-l6-q1", "aws-m1-l6", 1,
       "What does a load balancer do?",
       ["Stores files", "Distributes incoming traffic across healthy targets",
        "Runs databases", "Manages DNS"],
       0, "ELB spreads load and health-checks targets, sending traffic only to "
          "healthy ones.",
       ("tcs", "infosys")),
    _q("aws-m1-l6-q2", "aws-m1-l6", 2,
       "Which load balancer for HTTP path-based routing (/api/* vs /img/*)?",
       ["NLB", "ALB", "GWLB", "Classic"],
       1, "ALB operates at Layer 7 (HTTP) with host/path rules. NLB is Layer 4 "
          "raw TCP/UDP.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m1-l6-q3", "aws-m1-l6", 3,
       "You need a FIXED public IP in front of your load balancer. Which type?",
       ["ALB", "NLB (supports Elastic IPs / static IPs)", "GWLB", "None support it"],
       1, "NLB can be assigned Elastic (static) IPs per AZ. ALB uses dynamic "
          "DNS names — use Route 53 alias instead.",
       ("amazon", "hcl", "cognizant")),
    _q("aws-m1-l6-q4", "aws-m1-l6", 5,
       "What are ELB health checks for?",
       ["Billing", "Detecting unhealthy targets so traffic is routed only to healthy ones",
        "SSL termination", "Auto scaling policies"],
       1, "The LB pings a health path (e.g. /health); failing targets are "
          "drained. ASG can also replace them.",
       ("amazon", "tcs", "flipkart")),
    _q("aws-m1-l6-q5", "aws-m1-l6", 7,
       "Your app stores sessions in local memory. Users get logged out randomly behind an ALB. Fix?",
       ["Bigger instances", "Enable sticky sessions — or better, externalize sessions to ElastiCache/DynamoDB",
        "Use NLB", "Disable health checks"],
       1, "Requests land on different targets. Sticky sessions pin users; the "
          "robust fix is stateless app + shared session store.",
       ("amazon", "swiggy", "zomato")),
    _q("aws-m1-l6-q6", "aws-m1-l6", 9,
       "When would you pick GWLB over ALB/NLB?",
       ["For HTTP routing", "To transparently chain third-party virtual appliances (firewalls, IDS/IPS)",
        "For static IPs", "For WebSockets"],
       1, "GWLB (Layer 3) inserts security appliances into the traffic path "
          "without re-architecting routing.",
       ("amazon", "microsoft", "oracle")),
    # ---- L7: auto-scaling ----
    _q("aws-m1-l7-q1", "aws-m1-l7", 1,
       "What does an Auto Scaling Group do?",
       ["Backs up data", "Keeps the right number of EC2 instances running — scales out/in with load",
        "Updates software", "Monitors billing"],
       0, "ASG maintains min/desired/max counts, launching/terminating instances "
          "per policies and health checks.",
       ("tcs", "infosys")),
    _q("aws-m1-l7-q2", "aws-m1-l7", 2,
       "Simplest scaling policy for 'keep CPU around 50%'?",
       ["Step scaling", "Target tracking", "Scheduled scaling", "Manual"],
       1, "Target tracking: pick a metric + target, ASG does the math. Step "
          "scaling needs manual alarm thresholds.",
       ("amazon", "wipro", "accenture")),
    _q("aws-m1-l7-q3", "aws-m1-l7", 3,
       "Traffic spikes every weekday at 9 AM sharp. Best policy?",
       ["Target tracking", "Scheduled scaling", "Predictive only", "Manual intervention"],
       1, "Predictable patterns → scheduled scaling pre-warms capacity before "
          "the spike instead of reacting to it.",
       ("amazon", "hcl", "paytm")),
    _q("aws-m1-l7-q4", "aws-m1-l7", 5,
       "What defines WHAT gets launched by an ASG (AMI, type, SGs, user data)?",
       ["Scaling policy", "Launch template (versioned)", "CloudWatch alarm", "Target group"],
       1, "Launch templates are the versioned blueprint; policies decide WHEN "
          "to scale.",
       ("amazon", "tcs", "cognizant")),
    _q("aws-m1-l7-q5", "aws-m1-l7", 7,
       "For high availability, across how many AZs should an ASG span?",
       ["One (cheaper)", "At least two — so one AZ failure doesn't kill the fleet",
        "All regions", "AZs don't matter"],
       1, "Multi-AZ ASG relaunch failed instances in surviving AZs. Single-AZ "
          "is a single point of failure.",
       ("amazon", "flipkart", "phonepe")),
    _q("aws-m1-l7-q6", "aws-m1-l7", 9,
       "During a deploy, new instances fail health checks and the ASG keeps terminating/relaunching them in a loop. What saves you?",
       ["Bigger instances", "Instance protection + health check grace period + ELB health checks, and capped max",
        "Disable CloudWatch", "More subnets"],
       1, "Grace periods let instances boot before judgment; ELB checks catch "
          "app-level failure; max caps the blast radius. Then fix the AMI.",
       ("amazon", "atlassian", "swiggy")),
    # ---- L8: pricing-models ----
    _q("aws-m1-l8-q1", "aws-m1-l8", 1,
       "Which EC2 pricing is most expensive but most flexible?",
       ["Spot", "On-Demand", "Reserved", "Savings Plans"],
       1, "On-Demand: pay per second, zero commitment, highest rate. Flexibility "
          "costs money.",
       ("tcs", "infosys")),
    _q("aws-m1-l8-q2", "aws-m1-l8", 2,
       "Up to 90% discount, but AWS can reclaim with 2 minutes notice. What is it?",
       ["Reserved Instances", "Spot Instances", "Dedicated Hosts", "On-Demand"],
       1, "Spot = spare capacity at auction prices. Perfect for fault-tolerant "
          "batch/CI; terrible for databases.",
       ("amazon", "accenture", "wipro")),
    _q("aws-m1-l8-q3", "aws-m1-l8", 3,
       "A production database runs 24/7 for 3 years. Cheapest option?",
       ["On-Demand", "Spot", "3-year Reserved / Savings Plan (up to ~72% off)",
        "Dedicated Host"],
       2, "Steady-state + long horizon = commit. Reserved/Savings Plans reward "
          "predictability with deep discounts.",
       ("amazon", "hcl", "tcs")),
    _q("aws-m1-l8-q4", "aws-m1-l8", 5,
       "Nightly 3-hour ETL job, retryable, deadline 8 hours. Cheapest?",
       ["On-Demand", "Reserved", "Spot Instances", "Dedicated Host"],
       2, "Interruptible + flexible deadline = textbook Spot workload at up to "
          "90% off.",
       ("amazon", "flipkart", "dream11")),
    _q("aws-m1-l8-q5", "aws-m1-l8", 7,
       "Savings Plans vs Reserved Instances — key difference?",
       ["No difference", "Savings Plans apply flexibly across families/regions for a $/hr commitment; RIs lock to specific attributes",
        "Savings Plans are shorter", "RIs are cheaper always"],
       1, "Savings Plans trade a little max discount for flexibility — usage "
          "shifts, the discount follows.",
       ("amazon", "microsoft", "deloitte")),
    _q("aws-m1-l8-q6", "aws-m1-l8", 9,
       "Finance complains the AWS bill doubled with no traffic change. FIRST thing to check?",
       ["Open a support ticket", "Cost Explorer: find the service spike, then check for forgotten resources (EBS, NAT, idle instances)",
        "Buy Reserved Instances", "Move regions"],
       1, "Most 'mystery bills' are orphaned resources — unattached EBS volumes, "
          "idle NAT gateways, forgotten instances. Measure before optimizing.",
       ("amazon", "cred", "razorpay")),
]
