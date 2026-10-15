"""System Design curriculum seed data for SkillForge — expert level, interview-focused.

Sibling migration n3o4trend001_new_domains already seeds domain 'system-design'
with 4 modules (scalability, load-balancing, db-scale, microservices-design)
plus 20 thin starter questions. This pack attaches 6 deep-content modules
(37 lessons, 220+ questions, difficulty 1-10) onto those 4 existing modules —
no competing modules created.

Expected schema (curriculum_* tables):
  curriculum_domains   (slug PK, name, icon, description)
  curriculum_modules   (slug PK, domain_slug FK, name, order_index, description)
  curriculum_lessons   (id PK, module_id FK, slug, title, content, order_index,
                        estimated_minutes, has_visual)
  curriculum_questions (id PK, domain_slug, module_slug, lesson_id FK,
                        difficulty 1-10, qtype, prompt, choices JSON,
                        answer_index, explanation, company_tags JSON, created_at)

Usage:
  from app.adapters.outbound.system_design_seed import seed, CURRICULUM
  seed(session)      # idempotent ORM insert (deterministic uuid5 ids)
  python -m app.adapters.outbound.system_design_seed   # verify counts

All content is original — classic system design concepts explained in
SkillForge's own words, interview-first: every lesson ends with
"how would you design X?" style thinking, difficulty rising 1 to 10.
"""

from __future__ import annotations

import json
import sys


# ---------------------------------------------------------------------------
# Compact builders
# ---------------------------------------------------------------------------

def Q(prompt, choices, answer_index, difficulty, explanation, companies):
    """One MCQ. choices: exactly 4 strings. answer_index: 0-3."""
    assert len(choices) == 4, f"need 4 choices: {prompt[:40]}"
    assert 0 <= answer_index <= 3
    assert 1 <= difficulty <= 10
    return {
        "qtype": "mcq",
        "prompt": prompt,
        "choices": choices,
        "answer_index": answer_index,
        "difficulty": difficulty,
        "explanation": explanation,
        "company_tags": companies,
    }


def L(slug, title, theory_md, questions):
    assert 5 <= len(questions) <= 8, f"lesson {slug}: need 5-8 questions"
    diffs = [q["difficulty"] for q in questions]
    return {
        "slug": slug,
        "title": title,
        "theory_md": theory_md,
        "difficulty_min": min(diffs),
        "difficulty_max": max(diffs),
        "questions": questions,
    }


def M(slug, name, description, lessons):
    return {"slug": slug, "name": name, "description": description,
            "lessons": lessons}


MODULES = []


# ---------------------------------------------------------------------------
# DOMAIN
# ---------------------------------------------------------------------------

DOMAIN = {
    "slug": "system-design",
    "name": "System Design",
    "icon": "🏗️",
    "description": (
        "The interview round that decides senior offers. 6 modules, 37 lessons, "
        "220+ questions — from 'what is a load balancer' to designing Twitter, "
        "WhatsApp and URL shorteners, difficulty rising gradually 1 to 10."
    ),
}


# ---------------------------------------------------------------------------
# MODULE 1 — SCALABILITY BASICS (7 lessons)
# ---------------------------------------------------------------------------

_scalability = M("scalability-basics", "Scalability Basics",
"Vertical vs horizontal scaling, load balancing, stateless services, CAP theorem, "
"latency vs throughput, redundancy, and read/write scaling patterns.", [

L("vertical-vs-horizontal", "Vertical vs Horizontal Scaling",
"""## Two ways to grow

**Vertical scaling (scale up)** means making one server bigger: more CPU, more RAM,
faster disk. It is simple — no code changes — but it has a hard ceiling: there is a
biggest machine you can buy, and prices rise steeply near the top.

**Horizontal scaling (scale out)** means adding more servers and spreading the load.
There is no hardware ceiling, and one server dying doesn't kill you. But your software
must be designed for it: requests can land on any machine.

```
vertical:    [  BIG SERVER  ]            <- one box, one failure = outage
horizontal:  [LB] -> [s1] [s2] [s3]      <- add boxes as traffic grows
```

## The rule of thumb

Startups usually begin vertical (simple, cheap at small scale) and move horizontal
as traffic grows. Companies like Amazon and Google run almost everything horizontally.

## Interview line

"Vertical scaling is buying a bigger box; horizontal scaling is buying more boxes.
Horizontal has no ceiling but demands stateless, share-nothing design."
""",
[
Q("What does 'scaling vertically' mean?",
  ["Adding more servers behind a load balancer",
   "Adding CPU/RAM to a single server",
   "Splitting the database into shards",
   "Breaking the app into microservices"], 1, 1,
  "Vertical = scale UP one machine (bigger box). Horizontal = scale OUT (more boxes).",
  ["TCS", "Infosys", "Wipro"]),
Q("What is the main hard limit of vertical scaling?",
  ["It requires rewriting the application",
   "You eventually hit the biggest machine money can buy",
   "It only works for databases",
   "Load balancers don't support it"], 1, 2,
  "No matter the budget, a single machine has a maximum size — and cost per unit of power rises steeply near the top.",
  ["TCS", "Accenture"]),
Q("A single large server handling all traffic is an example of…",
  ["horizontal scaling", "a single point of failure",
   "eventual consistency", "sharding"], 1, 4,
  "One box = one failure takes everything down. Horizontal designs remove this SPOF.",
  ["Amazon", "Flipkart"]),
Q("Traffic doubles every 3 months for the foreseeable future. Which strategy is sustainable?",
  ["Keep buying a bigger server",
   "Horizontal scaling with load balancing",
   "Rewrite everything in a faster language",
   "Move the database to a bigger disk"], 1, 5,
  "Unbounded growth needs unbounded capacity — only horizontal scaling has no hardware ceiling.",
  ["Google", "Microsoft"]),
Q("Why does horizontal scaling usually require stateless application servers?",
  ["Stateless servers are written in faster languages",
   "So any server can handle any request without local session data",
   "Because databases cannot be stateless",
   "To reduce the number of servers needed"], 1, 7,
  "If server A holds your session in its memory and the next request lands on server B, you're logged out. Stateless servers push state to a shared store (Redis/DB).",
  ["Amazon", "Google"]),
Q("Your horizontally scaled service keeps logging users out randomly. Most likely root cause?",
  ["The load balancer is too slow",
   "Session state stored in individual servers' local memory",
   "The database is sharded",
   "CDN caching the login page"], 1, 9,
  "Classic symptom of stateful servers behind a load balancer. Fix: externalize sessions to Redis or use signed tokens (JWT).",
  ["Amazon", "Microsoft", "Flipkart"]),
]),

L("load-balancing-algos", "Load Balancing Algorithms",
"""## The traffic cop

A **load balancer (LB)** sits in front of your servers and spreads incoming requests
across them. Clients talk to one address (the LB); the LB picks a healthy server.

```
client -> [Load Balancer] -> server1
                         -> server2
                         -> server3
```

## Common algorithms

- **Round-robin** — requests go 1 → 2 → 3 → 1 → 2 → 3… Simple, fair when servers are equal.
- **Least connections** — send to the server with fewest active connections. Best for long-lived connections (WebSockets, video).
- **Weighted round-robin** — bigger servers get a bigger share (weights 3:2:1).
- **IP hash** — hash the client IP to pick a server. Same client → same server (cheap session affinity).
- **Least response time** — pick the currently fastest server.

## Health checks

The LB continuously pings servers. A dead server is pulled out of rotation automatically —
without this, users would hit dead servers half the time.
""",
[
Q("What does a load balancer do?",
  ["Stores user sessions permanently",
   "Distributes incoming requests across multiple servers",
   "Encrypts database backups",
   "Compresses images for the CDN"], 1, 1,
  "One public address in, N servers out — the LB spreads the load and hides failures.",
  ["TCS", "Infosys"]),
Q("With round-robin, 9 requests arrive at 3 healthy servers. How are they distributed?",
  ["All 9 go to the fastest server", "3, 3, 3 in rotation",
   "Randomly with no pattern", "9, 0, 0 until one fails"], 1, 3,
  "Round-robin cycles 1→2→3→1…, so 9 requests split evenly: 3 each.",
  ["Wipro", "Accenture"]),
Q("Servers have capacities in ratio 4:2:1. Which algorithm fits best?",
  ["Pure round-robin", "Weighted round-robin with weights 4:2:1",
   "IP hash", "Random"], 1, 4,
  "Weights match capacity so each server gets load proportional to what it can handle.",
  ["Amazon"]),
Q("Why is 'least connections' better than round-robin for WebSocket chat servers?",
  ["WebSockets use more bandwidth",
   "Connections live long, so counts diverge — least-connections balances actual load",
   "Round-robin doesn't work with TCP",
   "Least connections is always faster"], 1, 5,
  "With long-lived connections, round-robin can pile many active users on one server while another idles. Least-connections looks at real load.",
  ["Google", "Microsoft"]),
Q("IP hash gives cheap session affinity. What breaks it?",
  ["HTTPS traffic",
   "Adding or removing a server re-hashes many clients to different servers",
   "It only works for IPv6",
   "Databases can't store hashed IPs"], 1, 7,
  "The hash ring depends on the server set; membership changes remap clients. (Consistent hashing fixes this — see the Caching module.)",
  ["Amazon", "Flipkart"]),
Q("Why are health checks essential, not optional, on a load balancer?",
  ["They make responses faster",
   "Without them the LB keeps sending users to dead servers",
   "They encrypt traffic",
   "They reduce server cost"], 1, 9,
  "A server can die at any time. Health checks let the LB detect it in seconds and route around it — this is what makes the system self-healing.",
  ["Google", "Amazon", "Microsoft"]),
]),

L("stateless-stateful", "Stateless vs Stateful Services",
"""## The distinction that decides scalability

- **Stateful** server: remembers client data between requests (session in local memory, local file uploads).
- **Stateless** server: remembers nothing; every request carries what it needs, shared state lives in a DB/cache.

```
stateful:   req1 -> [s1: session X]   req2 -> must hit s1 again!
stateless:  req1 -> [any server] -> Redis/DB
            req2 -> [any server] -> Redis/DB
```

## Why interviews love this

"Design a system for 10x traffic" almost always starts with: make app servers stateless,
push sessions to Redis, uploads to object storage. Then you can add/remove servers freely.

## Sticky sessions: the crutch

LBs can pin a user to one server ("sticky sessions") so local state works. It helps
migration but creates uneven load, and a server crash still loses those sessions.

## JWT: stateless auth

A signed token carries the user identity; any server verifies the signature without a
DB lookup. Auth state travels with the request — beautifully stateless.
""",
[
Q("A stateless server…",
  ["never uses a database",
   "stores no client session data between requests",
   "cannot handle HTTPS",
   "runs only on one machine"], 1, 1,
  "Stateless = each request independent; shared state lives outside (DB/cache/token).",
  ["TCS", "Infosys"]),
Q("Why is stateless preferred when auto-scaling?",
  ["Stateless servers use less RAM",
   "New servers are useful immediately — no session migration needed",
   "Databases require it",
   "It makes code run faster"], 1, 3,
  "A fresh stateless server can take traffic in seconds. A stateful one needs its session data copied over first.",
  ["Amazon", "Google"]),
Q("Sticky sessions solve which problem?",
  ["Slow database queries",
   "Routing the same user to the same server so local session data works",
   "Encrypting traffic",
   "Balancing database load"], 1, 4,
  "The LB pins user→server. Works as a migration aid, but it's a crutch (see next question).",
  ["Wipro"]),
Q("Biggest downsides of sticky sessions?",
  ["They are expensive to license",
   "Uneven load + server crash loses those users' sessions",
   "They only work with HTTP/2",
   "They prevent using a CDN"], 1, 6,
  "Hot users pile on one server, and failover still drops sessions. External session stores are the real fix.",
  ["Microsoft", "Flipkart"]),
Q("Where should session state live in a properly scalable design?",
  ["In each app server's RAM",
   "In an external shared store like Redis or the database",
   "In the load balancer",
   "In browser localStorage only"], 1, 7,
  "Shared external state lets any server serve any request — the foundation of elastic scaling.",
  ["Amazon", "Google"]),
Q("JWT tokens help statelessness because…",
  ["they are encrypted with AES-256",
   "auth state travels with the request and any server can verify the signature",
   "they never expire",
   "they replace the database"], 1, 9,
  "No session lookup needed: the token itself is the credential, cryptographically verifiable by every server independently.",
  ["Microsoft", "Amazon"]),
]),

L("cap-theorem", "CAP Theorem",
"""## Pick two (and you don't get to skip the choice)

A distributed data store can guarantee only two of three:

- **C — Consistency:** every read sees the latest write.
- **A — Availability:** every request gets a (non-error) response.
- **P — Partition tolerance:** keeps working when the network splits.

Networks DO fail, so partitions happen — the real choice is **C vs A during a partition**.

```
partition!   [node A]  ✂  [node B]
  CP choice:  refuse writes (stay correct, some users get errors)
  AP choice:  accept writes (stay up, data may diverge, merge later)
```

## Real systems

- **CP:** etcd, HBase, ZooKeeper, traditional RDBMS clusters — "rather down than wrong."
- **AP:** Cassandra, DynamoDB, CouchDB — "rather stale than down," converge with eventual consistency.

## PACELC: the full picture

Even with NO partition, there's a **Latency vs Consistency** tradeoff: waiting for replicas
to agree is slower. So: **if Partitioned → choose A or C; Else → choose Latency or Consistency.**
""",
[
Q("CAP stands for…",
  ["Compute, API, Protocol",
   "Consistency, Availability, Partition tolerance",
   "Cache, Async, Persist",
   "Cluster, Agent, Proxy"], 1, 1,
  "The three guarantees — a distributed store can only fully provide two.",
  ["TCS", "Infosys"]),
Q("Why must every distributed system 'choose' regarding partitions?",
  ["Partitions are illegal in most countries",
   "Networks fail — splits will happen whether you plan for them or not",
   "Only startups face partitions",
   "Partitions only affect caching layers"], 1, 3,
  "You can't prevent network failures, so the system must have a defined behavior when nodes can't talk.",
  ["Amazon"]),
Q("A CP system during a network partition will…",
  ["serve stale data happily",
   "refuse or block some writes to stay consistent",
   "delete the minority side",
   "double its throughput"], 1, 4,
  "CP = consistency first: better to error than to risk divergent data.",
  ["Google", "Microsoft"]),
Q("An AP system during a partition will…",
  ["shut down immediately",
   "keep serving requests, possibly with stale data, and converge later",
   "lose all data permanently",
   "block until the partition heals"], 1, 6,
  "AP = availability first: take the write now, reconcile conflicts when the partition heals (eventual consistency).",
  ["Amazon", "Flipkart"]),
Q("A banking ledger should be…",
  ["AP — availability matters most",
   "CP — never show a wrong balance",
   "neither, banks don't need CAP",
   "eventually consistent only"], 1, 7,
  "Money demands correctness over uptime: better a failed transfer than a wrong balance.",
  ["Goldman Sachs", "Microsoft"]),
Q("PACELC extends CAP by adding…",
  ["the Price of servers",
   "the Latency vs Consistency tradeoff when there is NO partition",
   "support for Edge computing",
   "a fourth guarantee: Persistence"], 1, 10,
  "Even healthy networks force a choice: wait for replicas (consistent, slower) or answer fast (maybe stale).",
  ["Google", "Amazon"]),
]),

L("latency-throughput", "Latency vs Throughput",
"""## Two different "fasts"

- **Latency:** time to finish ONE request (e.g., 200 ms).
- **Throughput:** requests finished PER SECOND (e.g., 500 rps).

A system can have great throughput and terrible latency (a bus holds many people but is slow),
or vice versa.

## Little's Law

`concurrent_requests = throughput × latency`. Rearranged: with 100 concurrent users and
200 ms latency, throughput ≈ 100 / 0.2 = **500 rps**. Interviewers love this one-line math.

## Percentiles, not averages

Averages lie: one 10-second outlier barely moves the mean but ruins someone's day. Track
**p50** (median), **p99** (99% faster than this), **p999**. "p99 = 800 ms" means 1 in 100
users waits longer than 800 ms.

## Tail latency amplification

One user request fans out to 100 microservices, each p99 = 100 ms. Chance ALL 100 are fast:
0.99^100 ≈ **37%**. So the overall p99 is far worse than any single service's — slow tails
compound. Mitigations: hedged requests, timeouts, async paths.
""",
[
Q("Latency is…",
  ["requests per second",
   "time taken to complete a single request",
   "the number of servers",
   "bandwidth of the network"], 1, 1,
  "Latency = how long one request takes. Throughput = how many per second.",
  ["TCS"]),
Q("Throughput is…",
  ["time per request", "requests completed per second",
   "CPU temperature", "disk size"], 1, 2,
  "Throughput measures capacity; latency measures speed per request.",
  ["Infosys"]),
Q("100 concurrent users, average latency 200 ms. Approximate throughput? (Little's Law)",
  ["20 rps", "500 rps", "20,000 rps", "2 rps"], 1, 4,
  "throughput = concurrent / latency = 100 / 0.2s = 500 requests/sec.",
  ["Amazon", "Google"]),
Q("Why do we track p99 latency instead of just the average?",
  ["p99 is easier to compute",
   "Averages hide the worst experiences; p99 bounds what 99% of users feel",
   "Regulations require p99",
   "Average latency is always zero"], 1, 5,
  "One terrible outlier barely moves the mean. p99 tells you the experience of your unluckiest real users.",
  ["Microsoft", "Flipkart"]),
Q("You double the servers and throughput doubles, but latency is unchanged. Why?",
  ["The load balancer is broken",
   "Latency is per-request work; parallelism raises capacity, not per-request speed",
   "Latency always equals throughput",
   "Databases ignore extra servers"], 1, 7,
  "More lanes move more cars per hour, but each car still drives the same road at the same speed.",
  ["Google"]),
Q("A request fans out to 100 services, each with p99 = 100 ms. Why is the overall p99 much worse?",
  ["0.99^100 ≈ 37% — most requests hit at least one slow service; tails compound",
   "The services run sequentially",
   "p99 values add up to 10,000 ms",
   "Load balancers multiply latency"], 1, 10,
  "Tail latency amplifies across fan-out. Fixes: hedged requests (send backup, take first), tight timeouts, async.",
  ["Google", "Amazon"]),
]),

L("redundancy-spof", "Redundancy & Single Points of Failure",
"""## SPOF: the thing that ruins weekends

A **single point of failure** is any component whose death takes the system down:
one server, one database, one load balancer, one AZ.

## The fix: redundancy

Run **N+1** (or 2N) of everything critical. Two patterns:

- **Active-passive:** standby idles until failover. Simple, but the standby may be stale or
  misconfigured — and failover itself can fail (test it!).
- **Active-active:** all nodes serve traffic. Better utilization, harder to build (needs
  consensus/data sync).

```
active-active:   [LB] -> s1 ✓  s2 ✓   (both live)
active-passive:  [db-primary ✓]  [db-standby …] (promoted on failure)
```

## Even the LB is a SPOF

Fix with redundant LBs + floating virtual IP, DNS failover, or anycast. "Who watches the
watchers?" — redundancy all the way down.

## Chaos engineering

Netflix's **Chaos Monkey** randomly kills production instances. If redundancy is real,
nobody notices. It turns "we think failover works" into "we know."
""",
[
Q("A single point of failure (SPOF) is…",
  ["a server with one CPU",
   "any component whose failure takes the whole system down",
   "a bug in one line of code",
   "a database with one table"], 1, 1,
  "SPOF = no backup. Find them by asking 'what happens if this dies?' for every box in the diagram.",
  ["TCS", "Wipro"]),
Q("Active-passive vs active-active?",
  ["Active-passive is always faster",
   "Passive standby idles until failover; active-active nodes all serve traffic",
   "They are the same thing",
   "Active-active needs no load balancer"], 1, 3,
  "Active-active uses all capacity and fails over instantly; active-passive is simpler but wastes a standby.",
  ["Amazon"]),
Q("Why is active-passive failover considered risky?",
  ["It costs twice as much",
   "The standby may be stale/misconfigured, and the failover procedure itself can fail",
   "It doesn't work with SSDs",
   "It violates CAP theorem"], 1, 4,
  "An untested standby is a hope, not a plan. Game days and chaos drills exist for this.",
  ["Google"]),
Q("Your single database is a SPOF. Standard fix?",
  ["Buy a bigger server",
   "Replicas + automated failover (or multi-master)",
   "Delete old rows",
   "Add more indexes"], 1, 6,
  "Replicas give read scale + failover targets; automation promotes one in seconds.",
  ["Flipkart", "Microsoft"]),
Q("The load balancer itself is a SPOF. How do you fix that?",
  ["You can't — LBs never fail",
   "Redundant LBs with a floating virtual IP / DNS failover / anycast",
   "Remove the load balancer",
   "Use sticky sessions"], 1, 7,
  "Redundancy all the way down — even the traffic cop gets a backup.",
  ["Amazon"]),
Q("What is the point of Chaos Monkey (randomly killing production instances)?",
  ["To save money on servers",
   "To prove redundancy and failover actually work under real conditions",
   "To test the CI pipeline",
   "To punish bad code"], 1, 8,
  "It converts 'we believe failover works' into measured evidence — Netflix pioneered this.",
  ["Google", "Netflix", "Amazon"]),
]),

L("scaling-patterns", "Scaling Patterns: Read/Write Splitting",
"""## Know your ratio

- **Read-heavy** (Twitter, news sites: ~100:1 reads:writes) → scale READS: caches, read replicas, CDNs.
- **Write-heavy** (IoT ingestion, logging: writes dominate) → scale WRITES: sharding, batching, queues.

Design starts by asking the ratio — interviewers notice when you do.

## Read replicas

One primary takes writes; N replicas serve reads. Cheap read scale. The catch: **replication lag**
(replicas are milliseconds-to-seconds behind).

```
writes -> [primary] ~~replicate~~> [replica1] [replica2] -> reads
```

## Living with lag

- "I posted but can't see it" → route the author's own reads to primary briefly (**read-your-own-write**).
- **CQRS**: separate read models from write models entirely, each optimized independently.

## Write scaling

Writes can't be cached away — they must land somewhere. **Shard** them: partition by key
(user_id, device_id) so each shard takes a slice of writes.
""",
[
Q("Twitter's workload is…",
  ["write-heavy", "read-heavy (reads vastly outnumber writes)",
   "perfectly balanced", "neither"], 1, 2,
  "Timelines are read millions of times per tweet written — classic read-heavy.",
  ["Twitter", "Flipkart"]),
Q("Read replicas help most when the workload is…",
  ["write-heavy", "read-heavy", "CPU-bound", "offline batch"], 1, 3,
  "Replicas absorb reads; writes still funnel through the primary.",
  ["Amazon"]),
Q("A user posts a comment but doesn't see it on refresh. Likely cause?",
  ["The CDN is down", "Replication lag — the read hit a stale replica",
   "The load balancer crashed", "JWT expired"], 1, 5,
  "The write reached the primary; the replica serving the read hasn't caught up yet.",
  ["Facebook", "Microsoft"]),
Q("How do you fix 'read-your-own-write' with replicas?",
  ["Delete the replicas",
   "Briefly route that user's reads to the primary after their write",
   "Make replication synchronous for everyone",
   "Disable caching"], 1, 6,
  "A short stickiness window (or version check) guarantees users see their own actions.",
  ["Google", "Amazon"]),
Q("CQRS stands for and means…",
  ["Cached Query Result Store",
   "Command Query Responsibility Segregation — separate read and write models",
   "Continuous Query Replication Service",
   "Central Queue for Read Scaling"], 1, 7,
  "Writes go to a normalized model; reads come from denormalized views — each side optimized alone.",
  ["Microsoft"]),
Q("IoT platform ingesting 1M sensor writes/sec. Best write-scaling approach?",
  ["Add read replicas", "Shard writes by device_id across many nodes",
   "Bigger cache", "Vertical scaling forever"], 1, 9,
  "Writes must land somewhere — partitioning spreads them. Caches and replicas don't absorb writes.",
  ["Amazon", "Google"]),
]),
])

MODULES.append(_scalability)


# ---------------------------------------------------------------------------
# MODULE 2 — CACHING (6 lessons)
# ---------------------------------------------------------------------------

_caching = M("caching", "Caching",
"Why caches exist, cache-aside vs write-through vs write-behind, Redis/Memcached, "
"CDNs, and consistent hashing.", [

L("why-cache", "Why Cache? The Memory Hierarchy",
"""## Fast copies of slow data

A **cache** keeps frequently used data in fast storage so you don't recompute or
re-fetch it. The memory hierarchy shows why it matters:

```
L1 cache ..... ~1 ns
RAM .......... ~100 ns
SSD .......... ~100 µs
Network/DB ... ~1-50 ms
```

Each level is ~100-1000x slower than the previous. A cache hit can turn a 50 ms
database query into a 1 ms memory lookup.

## When caching shines

- **Hot data**: a small fraction of keys gets most reads (the 80/20 rule).
- **Slow to compute**: DB joins, ML inference, rendered pages.
- **Read-heavy, slowly changing** data.

## When it doesn't help

Every request unique (no repeat reads), or data changes faster than you can cache it.
Caching a write-heavy firehose just adds complexity.

## The thundering herd

Cache expires → 1000 requests miss at once → all hammer the DB → DB dies → cache
never refills. Mitigations: **staggered TTLs** (jitter expiry), **request coalescing**
(one request rebuilds, others wait), background refresh before expiry.
""",
[
Q("A cache stores…",
  ["permanent backups of the database",
   "frequently accessed data in fast storage",
   "user passwords securely",
   "compiled binaries"], 1, 1,
  "Cache = fast copy. RAM is ~1000x faster than a network DB round trip.",
  ["TCS", "Infosys"]),
Q("A DB query takes 50 ms; the same data from cache takes 1 ms. Speedup?",
  ["2x", "50x", "500 ms", "No speedup"], 1, 2,
  "50/1 = 50x faster — this is why caches are the first scaling lever.",
  ["Wipro"]),
Q("Caching helps most when…",
  ["every request is unique",
   "a small set of keys gets most reads and data changes slowly",
   "the database is already fast enough",
   "writes outnumber reads 100:1"], 1, 4,
  "Hot, slow-to-compute, slowly-changing data = ideal cache candidates.",
  ["Amazon", "Flipkart"]),
Q("When does caching NOT help?",
  ["Read-heavy workloads",
   "Every request asks for different data (no repeat reads)",
   "When the database is slow",
   "When traffic is high"], 1, 5,
  "No repeat reads = no hits = pure overhead. Know your access pattern first.",
  ["Google"]),
Q("Cache hit ratio of 95% means…",
  ["95% of the cache is full",
   "95 of every 100 requests are served from cache",
   "The cache is 95% faster",
   "95 servers are caching"], 1, 6,
  "Hit ratio = hits / total requests. 95% is excellent; the DB sees only 5%.",
  ["Microsoft"]),
Q("Thundering herd: cache expires and 1000 requests slam the DB at once. Best mitigation?",
  ["Delete the cache entirely",
   "Staggered TTLs / request coalescing / background refresh",
   "Add more application servers",
   "Make the TTL infinite"], 1, 8,
  "Spread out expiries (jitter), let one request rebuild while others wait, or refresh before expiry.",
  ["Amazon", "Google", "Netflix"]),
]),

L("cache-aside", "Cache-Aside (Lazy Loading)",
"""## The most common pattern

The application manages the cache explicitly:

```
read(key):
  value = cache.get(key)
  if value: return value            # HIT
  value = db.get(key)               # MISS
  cache.set(key, value, ttl=300)
  return value
```

On a miss, read the database, populate the cache, return. The cache fills **lazily** —
only with data someone actually asked for.

## Why it's popular

- **Resilient**: cache dies → app still works, just slower (falls back to DB).
- **No waste**: only requested data occupies cache memory.
- Simple to reason about.

## The catches

- **Stale data**: if something updates the DB directly, the cache holds the old value until TTL expires. Mitigate with short TTLs or explicit invalidation on write.
- **Cold start**: a fresh/restarted cache means every request misses → DB spike. Warm critical keys on deploy.
- **First-request penalty**: the first reader always pays the DB cost.
""",
[
Q("In cache-aside, on a cache miss the application…",
  ["returns an error",
   "reads the database, writes the result to cache, then returns it",
   "waits for the cache to refill itself",
   "restarts the cache server"], 1, 2,
  "Lazy loading: the app populates the cache on demand.",
  ["TCS", "Accenture"]),
Q("Who populates the cache in cache-aside?",
  ["The database trigger",
   "The application, lazily when data is requested",
   "A nightly batch job only",
   "The load balancer"], 1, 3,
  "No background magic — the app writes to cache on misses (and optionally invalidates on writes).",
  ["Infosys"]),
Q("Main staleness risk in cache-aside?",
  ["Cache servers overheat",
   "DB updated directly → cache serves old value until TTL/invalidation",
   "Keys are too long",
   "JSON is slow to parse"], 1, 5,
  "The cache doesn't know about out-of-band DB writes. Fix: invalidate on write or keep TTLs short.",
  ["Amazon", "Flipkart"]),
Q("Cold start problem and fix?",
  ["Cache is too cold physically — heat the datacenter",
   "Fresh cache = all misses hammer the DB; warm critical keys on deploy",
   "Cold data can't be cached",
   "Restart the database"], 1, 6,
  "Pre-load hot keys at startup so the first real users don't all miss at once.",
  ["Google"]),
Q("Why is cache-aside resilient to total cache failure?",
  ["Caches never fail",
   "The app falls back to the database — slower but correct",
   "The load balancer takes over caching",
   "DNS caches the responses"], 1, 7,
  "Cache is a pure optimization layer, not in the critical path. That's its beauty.",
  ["Microsoft", "Amazon"]),
Q("Two requests miss the same key simultaneously and both hit the DB. This is…",
  ["a security breach",
   "usually acceptable; at extreme scale, use per-key locking or request coalescing",
   "impossible — caches prevent it",
   "a reason to never use cache-aside"], 1, 8,
  "Duplicate DB work on rare races is fine for most; stampede protection matters only for hot keys.",
  ["Google"]),
]),

L("write-through-behind", "Write-Through vs Write-Behind",
"""## Three write strategies

**Write-through**: write to cache AND database synchronously. Reads always fresh.
Cost: every write pays both latencies.

**Write-behind (write-back)**: write to cache, acknowledge immediately, flush to DB
asynchronously (batched). Blazing writes — but a cache crash loses unflushed data.

**Write-around**: writes go straight to DB, bypassing cache; cache fills on later reads.
Good when written data is rarely re-read.

```
write-through:  app -> cache -> DB (wait for both)      [safe, slower]
write-behind:   app -> cache (ack!) ~~later~~> DB       [fast, risky]
write-around:   app -> DB (cache untouched)             [no pollution]
```

## Choosing

- Money/financial records → **write-through** (durability beats speed).
- Counters, analytics, session heartbeats → **write-behind** (speed, some loss OK).
- Write-once logs → **write-around** (don't pollute cache with data nobody re-reads).
""",
[
Q("Write-through guarantees…",
  ["the fastest possible writes",
   "cache and database stay consistent, at the cost of slower writes",
   "data is never persisted",
   "reads never hit the cache"], 1, 3,
  "Synchronous dual-write: you wait for both, so they can't diverge.",
  ["TCS", "Wipro"]),
Q("Biggest risk of write-behind?",
  ["Reads become slower",
   "Data loss if the cache crashes before flushing to the DB",
   "It doesn't work with Redis",
   "It requires schema changes"], 1, 4,
  "Acknowledged ≠ persisted. Power loss in the flush window loses writes.",
  ["Amazon"]),
Q("When is write-behind worth the risk?",
  ["Banking transfers",
   "Extremely write-heavy data where some loss is acceptable (counters, analytics)",
   "When reads are more important than writes",
   "Never — it's always wrong"], 1, 5,
  "Like counters: losing a few increments is invisible, but 10x write throughput is very visible.",
  ["Google", "Facebook"]),
Q("Write-around is best when…",
  ["writes are rarely re-read (write-once logs)",
   "you need the fastest reads",
   "the cache is empty",
   "using SQL databases"], 1, 6,
  "Skips cache pollution: why fill precious RAM with data nobody will ask for again?",
  ["Microsoft"]),
Q("Which strategy has the lowest write latency?",
  ["Write-through", "Write-behind", "Write-around", "Cache-aside"], 1, 7,
  "Write-behind acks after the cache write only — the DB flush happens later, off the critical path.",
  ["Amazon"]),
Q("A bank transfer must never be lost. Which write pattern?",
  ["Write-behind for speed",
   "Write-through — durability over speed",
   "Write-around",
   "No cache at all is the only option"], 1, 9,
  "Money = correctness first. Synchronous persistence to the DB before acknowledging.",
  ["Goldman Sachs", "Amazon"]),
]),

L("redis-memcached", "Redis & Memcached",
"""## In-memory key-value stores

Both keep data in **RAM**: sub-millisecond reads. The workhorses behind nearly every
large cache layer.

**Memcached**: dead simple, multithreaded, pure key→string. No persistence, no data structures.

**Redis**: single-threaded event loop (so fast it doesn't matter) + rich data structures:
strings, hashes, lists, sets, **sorted sets**, streams — plus persistence and pub/sub.

## Redis greatest hits

- **Sorted sets → leaderboards**: `ZADD game 1000 alice` keeps players score-ordered; `ZRANGE` reads the top 10 in O(log n).
- **Hashes → session/cart objects**: one key, many fields.
- **SET NX PX → distributed locks** (see the Distributed Lock lesson).
- **Streams → lightweight queues**.

## Persistence (Redis)

- **RDB**: periodic snapshots. Fast restart, may lose minutes of data.
- **AOF**: append-only log of writes. Durable, bigger files, slower restart.
- Many caches run Redis with persistence OFF (cache = disposable). Sessions/carts often want it ON.

## Eviction

When RAM fills: `allkeys-lru` evicts least-recently-used keys; `volatile-lru` only keys with TTL.
Pick by whether all keys are cache-like or some must never be evicted.
""",
[
Q("Redis and Memcached store data…",
  ["on spinning disks", "in RAM", "on tape", "in the browser"], 1, 1,
  "In-memory = microsecond-to-millisecond reads; the whole point of the tier.",
  ["TCS"]),
Q("Redis vs Memcached — Redis additionally offers…",
  ["only string values",
   "rich data structures (lists, sets, sorted sets, hashes), persistence, pub/sub",
   "multithreading",
   "a SQL interface"], 1, 3,
  "Memcached is deliberately minimal; Redis is a data-structure server.",
  ["Amazon", "Flipkart"]),
Q("Leaderboards are a classic Redis…",
  ["hash", "sorted set", "list", "bitmap"], 1, 4,
  "Sorted sets keep members ordered by score with O(log n) updates — perfect for rankings.",
  ["Google"]),
Q("RDB vs AOF persistence in Redis?",
  ["They are identical",
   "RDB = snapshots (fast restart, some loss); AOF = write log (durable, bigger)",
   "AOF is faster at everything",
   "RDB encrypts data"], 1, 5,
  "Snapshot vs journal — the eternal durability/speed tradeoff, now inside your cache.",
  ["Microsoft"]),
Q("Eviction policy allkeys-lru means…",
  ["delete random keys",
   "when full, evict the least-recently-used keys",
   "never evict anything",
   "evict the largest keys first"], 1, 7,
  "LRU approximates 'what will be needed soon' by 'what was needed recently'.",
  ["Amazon"]),
Q("Why not store web sessions in each app server's memory in production?",
  ["RAM is too expensive",
   "Lost on restart/deploy and breaks horizontal scaling — use Redis instead",
   "Sessions are too large",
   "It violates GDPR"], 1, 8,
  "Local sessions = stateful servers = the scaling problems from Module 1, lesson 3.",
  ["Google", "Microsoft"]),
]),

L("cdn", "CDNs: Caching at the Edge",
"""## Bringing content to the user

A **CDN (Content Delivery Network)** is a geographically distributed cache: hundreds of
edge locations (PoPs) around the world hold copies of your content. Users fetch from the
nearest edge instead of your origin server.

```
user (Mumbai) -> edge (Mumbai, 10 ms)   instead of   origin (Virginia, 250 ms)
```

## What belongs on a CDN

Static, cacheable, bandwidth-heavy: images, JS/CSS, fonts, videos, game downloads.
Netflix/YouTube would be impossible without CDNs — no origin can serve that bandwidth.

## How routing works

**Anycast DNS / Geo-DNS** directs each user to their nearest healthy edge. If an edge lacks
the file, it fetches from origin once ("origin pull"), caches it, and serves everyone after.

## Operations

- **TTL**: how long edges keep a file. Long TTL = fewer origin hits, slower updates.
- **Cache purge/invalidation**: force-drop a file everywhere for emergency updates.
- **Versioned filenames** (`app.v2.js`): the elegant trick — new deploys get new URLs, so old cached copies never conflict; no purge needed.
""",
[
Q("A CDN puts content…",
  ["only in one datacenter",
   "at edge locations close to users around the world",
   "inside the database",
   "on the user's phone permanently"], 1, 2,
  "Geography matters: 10 ms to Mumbai edge vs 250 ms to Virginia origin.",
  ["TCS", "Infosys"]),
Q("Best CDN candidates?",
  ["Live database queries",
   "Static assets: images, JS, CSS, video",
   "User passwords",
   "One-time tokens"], 1, 3,
  "Cacheable + bandwidth-heavy + rarely changing = CDN gold.",
  ["Wipro"]),
Q("How does a user reach the nearest CDN edge?",
  ["They type the edge address manually",
   "Anycast / Geo-DNS routing directs them automatically",
   "The browser guesses",
   "Via the database"], 1, 4,
  "DNS answers differently per region, steering users to close, healthy edges.",
  ["Amazon", "Cloudflare"]),
Q("When do you need a cache purge?",
  ["Every hour on schedule",
   "Emergency content update before TTL expiry",
   "When adding new users",
   "Never — purges don't exist"], 1, 6,
  "Purge = 'forget that file everywhere, now'. For routine deploys, prefer versioned filenames.",
  ["Google"]),
Q("Why do versioned filenames (app.v2.js) beat purging for deploys?",
  ["They are shorter",
   "New URL = new cache entry; old cached copies never conflict, no purge needed",
   "Browsers require versioning",
   "They use less bandwidth"], 1, 7,
  "Immutable assets + new names = CDN caching with zero invalidation headaches.",
  ["Facebook", "Netflix"]),
Q("Why is a CDN business-critical for video streaming?",
  ["Videos can't be compressed",
   "Bandwidth cost and latency at millions of concurrent viewers would crush any origin",
   "CDNs transcode video",
   "Users prefer edge locations aesthetically"], 1, 8,
  "Edge delivery turns an impossible origin bandwidth bill into a solvable caching problem.",
  ["Netflix", "YouTube", "Amazon"]),
]),

L("consistent-hashing", "Consistent Hashing",
"""## The problem it solves

Naive sharding: `server = hash(key) % N`. Add or remove one server → N changes →
**almost every key remaps** → all caches miss at once → thundering herd on the DB.

## The ring

Hash both servers and keys onto a circle (0 → 2^32). Each key belongs to the first
server **clockwise** from it. Adding a node only steals the keys on its own arc —
roughly **K/n keys move**, not all K.

```
        (s1)
       /    \\
   (s3) ---- (s2)     key K -> clockwise -> s2 owns K
```

## Virtual nodes

With few physical servers, arcs are uneven. Give each server many **virtual nodes**
(random points on the ring) — distribution smooths out beautifully.

## Where it lives

Amazon's **Dynamo**, **Cassandra**, **Riak**, and memcached client libraries all use it.
It's the standard answer to "how do cache/database nodes share keys without a coordinator?"

## Replication on the ring

Keep R copies: the key's owner plus the next R−1 clockwise nodes. A node dying still
leaves R−1 copies reachable.
""",
[
Q("What breaks with hash(key) % N when a server is added?",
  ["Nothing — it scales perfectly",
   "N changes so nearly every key remaps → mass cache misses",
   "Keys get encrypted",
   "The hash function stops working"], 1, 3,
  "Modulo depends on N; any membership change reshuffles everything. That's the pain consistent hashing removes.",
  ["Amazon", "Microsoft"]),
Q("In consistent hashing, adding one node remaps roughly…",
  ["all keys", "K/n keys (only its own ring segment)",
   "zero keys", "exactly 100 keys"], 1, 4,
  "Only the arc the new node takes over moves — minimal disruption, the whole point.",
  ["Google"]),
Q("Virtual nodes solve…",
  ["DNS resolution",
   "uneven key distribution when there are few physical servers",
   "slow hashing",
   "network partitions"], 1, 6,
  "Many random ring points per server → each server owns many small arcs → even split.",
  ["Amazon"]),
Q("Which real systems use consistent hashing?",
  ["MySQL and PostgreSQL",
   "Dynamo, Cassandra, Riak, distributed memcached clients",
   "React and Angular",
   "None — it's purely theoretical"], 1, 7,
  "It's the production-standard answer for coordinator-free key distribution.",
  ["Google", "Flipkart"]),
Q("How does a client find the right node for a key?",
  ["Asks a central master",
   "Hashes the key, walks the ring clockwise to the first node",
   "Broadcasts to all nodes",
   "Picks randomly"], 1, 8,
  "No coordinator needed — the ring math is deterministic and every client agrees.",
  ["Amazon"]),
Q("For replication factor R on the ring, copies live on…",
  ["random nodes",
   "the owner plus the next R−1 nodes clockwise",
   "the R biggest nodes",
   "only the coordinator"], 1, 9,
  "Clockwise successors = deterministic replica set; a dead node still leaves R−1 copies.",
  ["Microsoft", "Google"]),
]),
])

MODULES.append(_caching)


# ---------------------------------------------------------------------------
# MODULE 3 — DATABASES AT SCALE (7 lessons)
# ---------------------------------------------------------------------------

_databases = M("databases-scale", "Databases at Scale",
"SQL vs NoSQL, sharding, replication, replication lag, Dynamo-style AP stores, "
"choosing the right database, and indexing at scale.", [

L("sql-vs-nosql", "SQL vs NoSQL",
"""## Two philosophies

**SQL (relational)**: fixed schema, ACID transactions, JOINs, decades of tooling.
PostgreSQL, MySQL. "The data must be correct and queryable in complex ways."

**NoSQL**: flexible schema, designed for horizontal scale, simpler access patterns.
Four flavors:
- **Document** (MongoDB): JSON-like docs.
- **Key-value** (DynamoDB, Redis): get/put by key, blazing fast.
- **Wide-column** (Cassandra): massive write scale, time-series.
- **Graph** (Neo4j): relationships as first-class data.

## Choosing (the interview answer)

- Need complex queries, JOINs, strong consistency, transactions → **SQL**.
- Need massive scale, flexible/evolving schema, simple lookups → **NoSQL**.
- The senior answer: **"it depends — what are the access patterns, consistency needs,
  and scale?"** Then: polyglot persistence (right DB per job).

## The myth

"NoSQL = no schema" really means the *database* doesn't enforce one — your application
still must. Schemaless ≠ structureless.
""",
[
Q("SQL databases enforce…",
  ["no structure at all",
   "a fixed schema plus ACID transactions",
   "only key-value access",
   "eventual consistency always"], 1, 1,
  "Schema + transactions + JOINs = the relational contract.",
  ["TCS", "Infosys"]),
Q("'Schemaless' in NoSQL really means…",
  ["data has no structure",
   "the DB doesn't enforce schema — the application must",
   "you can't store JSON",
   "schemas are illegal"], 1, 3,
  "Flexibility shifts responsibility to your code. Structure still exists.",
  ["Wipro"]),
Q("Choose NoSQL when…",
  ["you need complex JOINs",
   "you need massive horizontal scale with flexible schema and simple access patterns",
   "you have 100 rows",
   "you love writing SQL"], 1, 4,
  "NoSQL shines at scale-out simplicity; SQL shines at query expressiveness.",
  ["Amazon", "Flipkart"]),
Q("Choose SQL when…",
  ["schema changes daily and scale is 1B writes/sec",
   "you need complex queries, JOINs, strong consistency and transactions",
   "you hate schemas",
   "you only need key lookups"], 1, 5,
  "Relational is still the default for correctness-critical, query-rich workloads.",
  ["Goldman Sachs", "Microsoft"]),
Q("MongoDB's data model is…",
  ["tables and rows",
   "JSON-like documents grouped in collections",
   "pure key-value only",
   "graph edges"], 1, 6,
  "Document model: flexible per-document fields, nested structures natural.",
  ["Google"]),
Q("Can SQL databases scale horizontally?",
  ["Never, it's impossible",
   "Yes — via sharding and read replicas, but it's harder than with NoSQL built for it",
   "Only on Tuesdays",
   "Only with NoSQL plugins"], 1, 8,
  "Possible (Vitess, Citus, manual sharding) but operationally heavier than native-distributed stores.",
  ["Amazon", "Google"]),
]),

L("sharding", "Sharding: Splitting the Database",
"""## When one DB isn't enough

**Sharding** splits data across multiple database servers ("shards"), each holding a
subset. Unlike replicas (full copies), shards hold *different* data — total capacity grows.

## The shard key

Everything hinges on the **shard key**: the field used to route rows to shards
(e.g., `user_id % 4`).

A good shard key is:
- **High-cardinality** (many distinct values),
- **Evenly distributed** (no hotspots),
- **Aligned with queries** (most queries hit one shard).

## Range vs hash

- **Range sharding** (users A–M → shard1): great for range queries, risky hotspots.
- **Hash sharding** (hash(user_id) % N): even spread, terrible for range scans.

## The pain

- **Cross-shard JOINs** are expensive or impossible → denormalize, avoid.
- **Resharding** (changing shard count/key) means moving live data — the operation
  everyone dreads. Pick the key carefully up front.
- **Hotspots**: shard by `country` with 80% users in India → one shard melts.
""",
[
Q("Sharding means…",
  ["copying the full database to more servers",
   "splitting data across multiple servers, each holding a subset",
   "adding indexes",
   "compressing backups"], 1, 2,
  "Shards partition data (capacity grows); replicas copy data (redundancy grows).",
  ["TCS", "Accenture"]),
Q("A good shard key should be…",
  ["low-cardinality like boolean",
   "high-cardinality, evenly distributed, aligned with query patterns",
   "always the primary key",
   "a random UUID with no meaning"], 1, 3,
  "The key decides your scaling fate — hotspots and cross-shard queries both stem from it.",
  ["Amazon"]),
Q("Shard by country; 80% of users are in one country. What happens?",
  ["Perfect balance",
   "Hotspot — one shard overloaded while others idle",
   "Queries get faster",
   "Nothing, shards auto-balance"], 1, 5,
  "Skewed keys create skewed shards. Hash sharding or a finer key fixes it.",
  ["Flipkart", "Google"]),
Q("Range sharding vs hash sharding?",
  ["Identical in every way",
   "Range: good for range queries, hotspot-prone. Hash: even spread, bad for range scans",
   "Hash is always better",
   "Range is always better"], 1, 6,
  "Match the strategy to the query pattern — there's no universal winner.",
  ["Microsoft"]),
Q("Why are cross-shard JOINs a problem?",
  ["They are actually free",
   "Data lives on different machines — expensive network fan-out or impossible",
   "JOINs are deprecated",
   "Shards don't support SQL"], 1, 7,
  "Design away from them: denormalize, or colocate related data on the same shard.",
  ["Amazon", "Google"]),
Q("Why do companies dread resharding?",
  ["It's fun actually",
   "Moving live data risks downtime and data loss — plan the shard key early",
   "It requires new hardware",
   "Shard keys can't be changed by law"], 1, 9,
  "The most expensive database operation is the one you do twice. Choose once, choose well.",
  ["Uber", "Amazon"]),
]),

L("replication", "Replication: Copies for Safety & Scale",
"""## Copies with a purpose

**Replication** keeps copies of data on multiple servers. Two wins: **durability**
(survive a dead server) and **read scale** (spread reads).

```
writes --> [PRIMARY] --replicate--> [replica] [replica] <-- reads
```

## Sync vs async

- **Synchronous**: primary waits for replica ack before confirming. Safe (no lost writes),
  slower writes, and a slow replica stalls everything.
- **Asynchronous**: primary confirms immediately, replicas catch up. Fast, but a crash can
  lose the last milliseconds of writes. (The common production choice.)

## Failover

Primary dies → promote a replica. Needs **leader election** and **fencing** (ensure the
old primary is really dead — otherwise two primaries accept writes = **split-brain**,
divergent data, a very bad day).

## What replication does NOT do

Replicas don't scale **writes** — every write still goes through the primary. Write
scaling needs sharding (previous lesson).
""",
[
Q("Replication gives you…",
  ["more total storage capacity",
   "copies of data on multiple servers — durability + read scale",
   "faster CPUs",
   "automatic sharding"], 1, 2,
  "Copies, not partitions: same data, more places.",
  ["TCS", "Infosys"]),
Q("Risk of asynchronous replication?",
  ["Writes become very slow",
   "A primary crash can lose the most recent writes not yet replicated",
   "Replicas can't serve reads",
   "It requires 10x hardware"], 1, 3,
  "Speed (no waiting) traded for a small durability window. Most systems accept it.",
  ["Wipro"]),
Q("Cost of synchronous replication?",
  ["Data loss",
   "Higher write latency — the primary waits for replica acknowledgment",
   "It doesn't work",
   "Cheaper hardware"], 1, 4,
  "Durability you can feel in p99 write latency. Worth it for money; overkill for likes.",
  ["Goldman Sachs"]),
Q("Read replicas scale…",
  ["writes", "reads — writes still funnel through the primary",
   "storage capacity", "CPU speed"], 1, 5,
  "The #1 misconception. Write scaling = sharding.",
  ["Amazon", "Flipkart"]),
Q("During failover, 'fencing' ensures…",
  ["the fence is painted",
   "the old primary is truly dead/isolated so two primaries never accept writes",
   "replicas are fast",
   "backups are recent"], 1, 7,
  "Without fencing: split-brain — two primaries diverge, and merging is agony.",
  ["Google", "Microsoft"]),
Q("Split-brain in databases means…",
  ["the DBA has a headache",
   "two primaries accept writes concurrently → divergent, hard-to-merge data",
   "the server splits physically",
   "queries run twice as fast"], 1, 8,
  "The nightmare scenario replication is designed to avoid — hence quorum and fencing.",
  ["Amazon"]),
]),

L("read-replicas-lag", "Living with Replication Lag",
"""## The price of async

Replicas lag the primary by milliseconds to seconds. Consequences are user-visible:
"I posted, but my post isn't there!" (read hit a stale replica).

## Patterns that help

- **Read-your-own-write**: after a user writes, route *their* reads to the primary for a
  short window (or until their write's version appears on the replica).
- **Monotonic reads**: once a session sees version N, never show it anything older.
- **Version/timestamp checks**: clients send "I have v42"; replica serves only if ≥ v42,
  else redirect to primary.

## Why not read everything from primary?

That defeats the purpose — the primary becomes the bottleneck again. Use the primary
surgically: own-writes, critical reads; replicas for the bulk.

## Cache + replicas ordering

Check **cache first** (fastest), then replica, primary as fallback. Each layer absorbs
what it can; lag is handled by the read-your-write window.
""",
[
Q("Replication lag is…",
  ["the time to back up",
   "the delay before a replica has the latest writes",
   "network cable length",
   "query planning time"], 1, 3,
  "Async replication = replicas are always slightly behind. Design for it.",
  ["TCS"]),
Q("User-visible symptom of replication lag?",
  ["Faster page loads",
   "'I posted but I can't see it' — read served from a stale replica",
   "Louder fans",
   "Cheaper bills"], 1, 4,
  "The classic complaint. The write succeeded; the read just went to yesterday's copy.",
  ["Facebook", "Flipkart"]),
Q("How do you fix read-your-own-write with replicas?",
  ["Delete all replicas",
   "Briefly route that user's reads to the primary after their write",
   "Make everything synchronous",
   "Turn off the cache"], 1, 5,
  "A short stickiness window (or version check) guarantees self-consistency.",
  ["Google", "Amazon"]),
Q("Monotonic reads guarantee…",
  ["reads are always fast",
   "once a session sees version N, it never sees anything older",
   "writes are instant",
   "replicas never lag"], 1, 6,
  "No time-travel: your view of data only moves forward within a session.",
  ["Microsoft"]),
Q("Why not just send all reads to the primary and skip the complexity?",
  ["You should — always do that",
   "It recreates the bottleneck replicas were built to remove",
   "Primaries can't serve reads",
   "It violates CAP"], 1, 7,
  "Use the primary surgically (own writes, critical reads); let replicas carry the bulk.",
  ["Amazon"]),
Q("Sensible lookup order in a layered design?",
  ["Primary → replica → cache",
   "Cache → replica → primary (each layer absorbs what it can)",
   "Replica → cache → primary",
   "Random"], 1, 8,
  "Fastest/cheapest first; fall through only on miss. Lag handled by the own-write window.",
  ["Google"]),
]),

L("dynamo-style", "Dynamo-style: AP Databases",
"""## Amazon's Dynamo paper (2007)

Faced with Black Friday traffic, Amazon built **Dynamo**: always writable, no master,
**AP** in CAP terms. Ideas that now power Cassandra, Riak, and DynamoDB:

- **Consistent hashing** ring for key placement (see Caching module).
- **Vector clocks**: version stamps that detect *concurrent* writes (siblings) vs
  causal ones — the system keeps both and lets the app merge.
- **Quorum**: with N replicas, choose read quorum R and write quorum W.
  **R + W > N** ⇒ read and write sets overlap ⇒ strong consistency on demand.
  (E.g., N=3, R=2, W=2: every read sees the latest write.)
- **Sloppy quorum + hinted handoff**: write to *any* N healthy nodes; if the rightful
  owner is down, a neighbor holds the write ("hint") and replays it later. Writes
  basically never fail.

## Why a shopping cart loves Dynamo

Adding to cart must NEVER fail (lost sale!). Conflicts (two devices, offline edits)
merge later. Availability > momentary consistency — exactly Dynamo's bet.
""",
[
Q("Dynamo chooses which side of CAP?",
  ["CP", "AP — availability + partition tolerance, with eventual consistency", "Neither", "Both fully"], 1, 4,
  "Always writable, even partitioned; conflicts reconciled after.",
  ["Amazon"]),
Q("With N=3 replicas, which R, W gives strong consistency?",
  ["R=1, W=1", "R=2, W=2 (R+W > N, quorums overlap)",
   "R=3, W=3", "R=1, W=3"], 1, 5,
  "Overlap guarantees every read quorum includes at least one node with the latest write.",
  ["Google", "Microsoft"]),
Q("Vector clocks are used to…",
  ["encrypt data",
   "detect concurrent conflicting writes (siblings) vs causal ones",
   "compress keys",
   "elect leaders"], 1, 6,
  "Version vectors reveal 'these two writes didn't see each other' — then merge.",
  ["Amazon"]),
Q("Hinted handoff: the rightful owner node is down, so…",
  ["the write is dropped",
   "a healthy neighbor temporarily holds the write and replays it later",
   "the client retries forever",
   "the cluster shuts down"], 1, 7,
  "Sloppy quorum in action: durability without waiting for the sick node.",
  ["Google"]),
Q("Why is it called a 'sloppy' quorum?",
  ["It's poorly implemented",
   "It accepts writes from ANY N healthy nodes, not the designated owners",
   "It loses data randomly",
   "It only works on weekends"], 1, 8,
  "Strict quorums demand specific nodes; sloppy takes whoever's alive — maximum availability.",
  ["Amazon"]),
Q("Why is a shopping cart a great Dynamo use case?",
  ["Carts need strong consistency",
   "Adds must never fail (lost sale!); conflicts can merge later",
   "Carts are tiny",
   "Carts don't need durability"], 1, 9,
  "Availability-first with mergeable conflicts = the Dynamo sweet spot.",
  ["Amazon", "Flipkart"]),
]),

L("choosing-db", "Choosing the Right Database",
"""## The decision framework

Interviewers don't want a brand name — they want reasoning. Ask:

1. **Access patterns**: key lookups? complex JOINs? graph traversals? full-text?
2. **Consistency**: money (strong) vs likes (eventual)?
3. **Scale**: GBs or PBs? reads or writes heavy?
4. **Operational cost**: managed service vs self-hosted expertise?

## Cheat sheet

| Need | Reach for |
|---|---|
| Time-series metrics | Cassandra / InfluxDB (wide-column/TSDB) |
| "Friends of friends" | Graph DB (Neo4j) or adjacency lists |
| Full-text search | Elasticsearch/Solr (not MySQL LIKE) |
| Massive counters | Redis INCR / Cassandra counters |
| Complex queries + transactions | PostgreSQL |

## Polyglot persistence

Real systems use several: Postgres for orders, Redis for sessions/cache, Elasticsearch
for search, S3 for blobs. Right tool per job — with the operational cost that implies.

## The meta-answer

"It depends" is the start, not the answer. Follow with: "Given X scale, Y consistency,
Z queries, I'd pick ___ because ___."
""",
[
Q("Time-series metrics (CPU per server per second) → ?",
  ["PostgreSQL with JOINs", "Wide-column/TSDB like Cassandra or InfluxDB",
   "Redis sorted sets", "Neo4j"], 1, 3,
  "Append-heavy, time-ordered, huge volume — exactly what wide-column stores are built for.",
  ["Amazon", "Google"]),
Q("'Friends of friends' queries → ?",
  ["Full table scans",
   "Graph DB (Neo4j) or adjacency lists — relationships are the data",
   "Redis strings",
   "CSV files"], 1, 4,
  "Multi-hop traversals are a graph problem; relational JOINs explode combinatorially.",
  ["Facebook", "LinkedIn"]),
Q("Full-text product search → ?",
  ["MySQL LIKE '%shoe%'",
   "Elasticsearch/Solr — inverted indexes built for search",
   "MongoDB only",
   "DNS"], 1, 5,
  "LIKE scans every row; inverted indexes make search sub-second at scale.",
  ["Flipkart", "Amazon"]),
Q("Millions of increments/sec on counters → ?",
  ["PostgreSQL row locks",
   "Redis INCR or Cassandra counters — designed for hot counters",
   "File appends",
   "Application memory"], 1, 6,
  "Atomic increments on hot keys need purpose-built primitives, not contended rows.",
  ["Google"]),
Q("The senior interview answer to 'which database?' starts with…",
  ["'PostgreSQL, always'",
   "'It depends — what are the access patterns, consistency needs, and scale?'",
   "'Whatever is cheapest'",
   "'MongoDB, obviously'"], 1, 7,
  "Reasoning over brand loyalty. Then commit: 'Given X, I'd pick Y because Z.'",
  ["Google", "Amazon", "Microsoft"]),
Q("Polyglot persistence means…",
  ["using many programming languages",
   "using multiple database types, each for its strength",
   "translating the schema",
   "sharding by language"], 1, 8,
  "Postgres for orders + Redis for sessions + Elasticsearch for search = each job's best tool.",
  ["Netflix", "Uber"]),
]),

L("indexing-scale", "Indexing at Scale",
"""## What indexes buy (and cost)

An **index** (usually a B-tree) makes lookups/filters on a column fast: O(log n) instead
of full scans. But every index taxes **writes** (each INSERT/UPDATE touches every index)
and consumes storage.

## Key ideas

- **Covering index**: the query's columns are all in the index → answered without
  touching the table at all.
- **Selectivity**: indexing a boolean (2 values) rarely helps; indexing email does.
- **Too many indexes** on a write-heavy table kills write throughput — audit and drop
  unused ones (Postgres: `pg_stat_user_indexes`).
- **Full scans win** when fetching a large fraction of rows — the optimizer knows.

## At scale: the distributed twist

On sharded data, a **global secondary index** must itself be sharded or every query
becomes scatter-gather across all shards. Local secondary indexes (per-shard) are cheap;
global ones are a design decision with real cost.
""",
[
Q("An index speeds up…",
  ["backups", "lookups and filters on indexed columns",
   "network speed", "CPU clock"], 1, 2,
  "B-tree: O(log n) seeks instead of scanning every row.",
  ["TCS", "Infosys"]),
Q("The cost of an index is…",
  ["nothing — indexes are free",
   "slower writes and extra storage (every write updates every index)",
   "faster writes",
   "it deletes data"], 1, 4,
  "Read speed bought with write speed + disk. Index deliberately.",
  ["Wipro"]),
Q("A covering index…",
  ["covers the server physically",
   "answers the query from the index alone, no table lookup needed",
   "is always the primary key",
   "can't be used with WHERE"], 1, 5,
  "All needed columns in the index = zero heap fetches = fastest possible.",
  ["Amazon", "Microsoft"]),
Q("Too many indexes on a write-heavy table…",
  ["is fine, more is better",
   "kills write throughput — every write updates every index",
   "makes reads slower",
   "is required by law"], 1, 6,
  "Audit with pg_stat_user_indexes; drop what nothing queries.",
  ["Google"]),
Q("When does a full table scan beat using an index?",
  ["Never", "When fetching a large fraction of rows — random index hops cost more",
   "Only on Mondays", "When the table is empty"], 1, 7,
  "The optimizer compares: 5% of rows → index; 60% → just scan.",
  ["Oracle", "Microsoft"]),
Q("The hard part of global secondary indexes on sharded data?",
  ["They're impossible",
   "The index must be sharded too, or queries scatter-gather across all shards",
   "They're always free",
   "Shards don't support indexes"], 1, 8,
  "Local indexes are cheap; global ones are a real distributed-systems design decision.",
  ["Amazon", "Google"]),
]),
])

MODULES.append(_databases)


# ---------------------------------------------------------------------------
# MODULE 4 — MICROSERVICES (6 lessons)
# ---------------------------------------------------------------------------

_microservices = M("microservices", "Microservices",
"Monolith vs microservices, API gateway, service discovery, circuit breakers, "
"saga pattern, and event-driven architecture.", [

L("monolith-vs-micro", "Monolith vs Microservices",
"""## Definitions

- **Monolith**: one codebase, one deployable. Simple to build, test, and debug.
- **Microservices**: many small services, each owning its data and deploying independently,
  talking over the network.

## Why microservices (the real reasons)

Independent **deployability** (ship orders-service without touching payments),
independent **scaling** (scale the hot service, not everything), and **team autonomy**
(small teams own services end-to-end).

## The costs nobody mentions first

Network latency between services, distributed debugging ("which of 40 services failed?"),
data consistency across services (no more ACID JOINs), and serious observability needs.
Microservices turn compile-time problems into runtime problems.

## The pragmatic path

**Start with a monolith.** Extract services when boundaries are clear and pain is real.
Premature microservices = all the distributed pain with none of the scale to justify it.

## Conway's Law

"Organizations design systems that mirror their communication structures." Team topology
shapes architecture — plan both together.

## Anti-pattern: the distributed monolith

Services so tightly coupled they must all deploy together. You kept the network hops
and lost the independence — the worst of both worlds.
""",
[
Q("A monolith is…",
  ["many small services", "a single deployable codebase",
   "a database cluster", "a CDN"], 1, 1,
  "One repo, one deploy — simplicity is the monolith's superpower.",
  ["TCS", "Infosys"]),
Q("Microservices' main benefits?",
  ["Less code overall",
   "Independent deploy/scale per service and team autonomy",
   "No need for databases",
   "Free hosting"], 1, 3,
  "Ship and scale the hot parts independently; let small teams own services end-to-end.",
  ["Amazon", "Netflix"]),
Q("Microservices' main costs?",
  ["There are none",
   "Network latency, distributed debugging, cross-service consistency, observability burden",
   "They can't use HTTP",
   "They require mainframes"], 1, 4,
  "Compile-time problems become runtime problems. Budget for observability from day one.",
  ["Google", "Uber"]),
Q("Why start with a monolith?",
  ["Monoliths are trendier",
   "Simpler; extract services when boundaries are clear and pain is real",
   "Microservices are illegal for startups",
   "Databases forbid microservices"], 1, 5,
  "Premature distribution = all the pain, none of the scale to justify it.",
  ["Amazon", "Shopify"]),
Q("Conway's Law says…",
  ["code must be beautiful",
   "system design mirrors the organization's communication structure",
   "microservices are mandatory",
   "teams must be large"], 1, 7,
  "Team topology shapes architecture — design both together.",
  ["Microsoft"]),
Q("A 'distributed monolith' is…",
  ["a monolith on many servers",
   "microservices so tightly coupled they must deploy together — worst of both worlds",
   "a type of database",
   "a caching strategy"], 1, 8,
  "Network hops without independence: you paid the distributed tax for nothing.",
  ["Google", "Amazon"]),
]),

L("api-gateway", "API Gateway",
"""## The front door

An **API gateway** is the single entry point: it routes requests to the right service
and handles cross-cutting concerns — authentication, rate limiting, logging, TLS
termination — so services stay focused on business logic.

```
mobile/web --> [API Gateway] --> auth-service
                             --> orders-service
                             --> search-service
```

Popular: Kong, AWS API Gateway, NGINX-based, Envoy.

## Backend-for-Frontend (BFF)

Mobile and web need different payloads. A **BFF** is a per-client gateway shaping
responses for that client — one for iOS, one for web — instead of one-size-fits-all.

## Aggregation

Mobile asks for user + orders + recommendations → gateway fans out to 3 services,
merges, returns one response. Fewer round trips over slow mobile networks.

## Isn't the gateway a SPOF?

It's stateless, so run many behind a load balancer / anycast. Redundancy is easy
precisely because it holds no state.

## Timeouts

Gateway timeout must exceed downstream timeouts, with graceful degradation (return
partial data, not a 500) when a service is slow.
""",
[
Q("An API gateway sits…",
  ["inside the database",
   "between clients and microservices, routing requests",
   "on the user's phone",
   "in the CDN only"], 1, 2,
  "Single front door: route + auth + rate-limit + log, then forward.",
  ["TCS", "Wipro"]),
Q("Cross-cutting concerns handled at the gateway?",
  ["Business logic",
   "Auth, rate limiting, logging, TLS termination",
   "Database schema design",
   "CSS styling"], 1, 3,
  "Once at the edge beats reimplementing in 40 services.",
  ["Amazon"]),
Q("Backend-for-Frontend (BFF) means…",
  ["one gateway for everything",
   "per-client gateways shaping payloads for mobile vs web",
   "no backend at all",
   "frontend written in Go"], 1, 5,
  "Mobile wants tiny payloads; web wants rich ones. BFF serves each optimally.",
  ["Netflix", "Google"]),
Q("Isn't the gateway a single point of failure?",
  ["Yes, unavoidably",
   "It's stateless, so run many behind a LB/anycast — redundancy is easy",
   "Gateways never fail",
   "Remove it to be safe"], 1, 6,
  "Statelessness makes the gateway itself trivially horizontally scalable.",
  ["Microsoft"]),
Q("Request aggregation at the gateway helps mobile because…",
  ["mobile CPUs are slow",
   "one merged response replaces many slow-network round trips",
   "it reduces server count",
   "JSON is heavy"], 1, 7,
  "Fan out server-side (fast datacenter network), return one payload over the slow link.",
  ["Facebook"]),
Q("Gateway timeout vs downstream service timeout: the rule?",
  ["Gateway must be shorter",
   "Gateway timeout exceeds downstream, with graceful degradation on slowness",
   "No timeouts anywhere",
   "Equal timeouts everywhere"], 1, 8,
  "Never let a slow service hang the gateway forever — bound it, degrade gracefully.",
  ["Amazon", "Uber"]),
]),

L("service-discovery", "Service Discovery",
"""## The problem with hardcoded addresses

Services are ephemeral: autoscaling adds/removes instances, deploys replace them.
Hardcoded IPs die with the first deploy.

## The registry

A **service registry** (Consul, Eureka, etcd) maps service name → healthy instances.
Services register on startup, deregister on shutdown; health checks prune the dead.

## Two flavors

- **Client-side**: client queries the registry, picks an instance, calls it. (Smart client, e.g., Ribbon.)
- **Server-side**: client calls a router/LB, which resolves via the registry. (Dumb client; k8s Services work this way.)

## Kubernetes

A k8s **Service** gives a stable virtual IP + DNS name (`orders.default.svc`) with
built-in discovery and load balancing — most teams never hand-roll this anymore.

## Caching registry data

Clients cache registry entries with short TTLs for speed — but must handle staleness
(instance died since the cache entry). Combine with retries + health-aware LB.
""",
[
Q("Why can't services use hardcoded IPs?",
  ["IPs are too long",
   "Instances are ephemeral — autoscaling and deploys constantly change addresses",
   "DNS is faster",
   "It's illegal"], 1, 3,
  "Anything static breaks the moment an instance is replaced.",
  ["TCS"]),
Q("A service registry maps…",
  ["users to passwords",
   "service names to currently healthy instances",
   "URLs to HTML",
   "bugs to developers"], 1, 4,
  "The directory that answers 'where is orders-service right now?'",
  ["Amazon", "Google"]),
Q("Client-side vs server-side discovery?",
  ["Same thing",
   "Client queries registry directly vs calls a router/LB that resolves it",
   "One uses HTTP, other uses TCP",
   "Client-side is always better"], 1, 5,
  "Smart client vs dumb client — operational tradeoff, both common.",
  ["Netflix", "Microsoft"]),
Q("What feeds the registry so dead instances disappear?",
  ["Manual spreadsheets", "Health checks", "User reports", "Luck"], 1, 6,
  "Continuous probing prunes the dead — discovery is only as good as its health data.",
  ["Google"]),
Q("In Kubernetes, a Service provides…",
  ["a physical server",
   "a stable virtual IP + DNS name with built-in discovery and load balancing",
   "a database",
   "a CI pipeline"], 1, 7,
  "`orders.default.svc` just works — k8s absorbed this whole problem.",
  ["Google", "Microsoft"]),
Q("Clients caching registry entries must handle…",
  ["nothing — caches are perfect",
   "staleness: an instance may have died since the cached entry",
   "encryption",
   "schema migrations"], 1, 8,
  "Short TTLs + retries + health-aware balancing cover the gap.",
  ["Amazon"]),
]),

L("circuit-breaker", "Circuit Breaker & Resilience",
"""## Cascading failures: how one slow service kills everything

Service A calls B; B gets slow. A's threads pile up waiting → A exhausts its pool →
A's callers pile up → the whole system cascades down. One bad dependency, total outage.

## The circuit breaker

Like an electrical breaker: **closed** (traffic flows) → failures trip it **open**
(fail fast, don't call the struggling service) → after a timeout, **half-open**
(let one probe through; success closes it).

Libraries: Resilience4j, Polly, Hystrix (legacy).

## Supporting patterns

- **Timeouts on EVERY remote call** — no timeout = threads pile up forever.
- **Retries with exponential backoff + jitter** — naive immediate retries during an
  outage multiply load (retry storm). Back off: 1s, 2s, 4s… plus random jitter so
  clients don't retry in lockstep.
- **Bulkhead** — separate thread pools per dependency, so one slow dependency can't
  starve the others (named after ship compartments).
""",
[
Q("A cascading failure is…",
  ["a waterfall chart",
   "one slow service exhausts its callers' resources, toppling the whole system",
   "a database migration",
   "a UI bug"], 1, 3,
  "Failure propagates upward through thread-pool exhaustion — the classic microservices killer.",
  ["Amazon", "Netflix"]),
Q("When the circuit is OPEN, the breaker…",
  ["lets all traffic through",
   "fails fast without calling the struggling service",
   "restarts the service",
   "sends more traffic"], 1, 4,
  "Fail fast protects the caller AND gives the downstream room to recover.",
  ["Google", "Microsoft"]),
Q("Half-open state means…",
  ["the circuit is broken",
   "allow one probe request through; success closes the circuit",
   "half the servers are down",
   "the database is half full"], 1, 5,
  "A cautious toe back in the water before fully reopening.",
  ["Uber"]),
Q("Naive immediate retries during an outage cause…",
  ["faster recovery",
   "a retry storm — multiplying load on the already-struggling service",
   "better logs",
   "nothing bad"], 1, 6,
  "Backoff + jitter: wait longer each time, randomized, so clients don't march in lockstep.",
  ["Amazon", "Google"]),
Q("The bulkhead pattern…",
  ["is about ships literally",
   "isolates thread pools per dependency so one slow one can't starve the others",
   "increases bandwidth",
   "removes the need for timeouts"], 1, 7,
  "Compartmentalize failure — one flooded compartment shouldn't sink the ship.",
  ["Microsoft", "Netflix"]),
Q("The single most important resilience rule for remote calls?",
  ["Never call remote services",
   "Always set timeouts — unbounded waits pile up threads forever",
   "Use only UDP",
   "Retry infinitely"], 1, 9,
  "Every resilience pattern assumes bounded waits. No timeout = no bulkhead, no breaker can save you.",
  ["Google", "Amazon"]),
]),

L("saga-pattern", "Saga: Distributed Transactions",
"""## Why not 2PC?

Two-phase commit across microservices locks resources over the network and **blocks**
if the coordinator dies. It doesn't survive the realities of distributed systems
(more in the Advanced module).

## The saga idea

Break the transaction into a sequence of **local transactions**, each with a
**compensating action** (semantic undo):

```
book flight ✓ → book hotel ✓ → book car ✗
   → compensate: cancel hotel → cancel flight
```

## Two coordinations

- **Choreography**: each service emits events; the next listens and acts. No central brain.
- **Orchestration**: a central saga coordinator tells each service what to do next.

## The catches

- **No isolation**: other transactions can see intermediate states (flight booked, hotel
  not yet). Design UX and invariants for it.
- Compensations must be **idempotent and retryable** — they run during failures, the
  worst time for flakiness.
- When strong consistency is truly required and the scope is small, 2PC/a monolith
  may honestly be better. Sagas are for when you accept eventual consistency.
""",
[
Q("Why avoid 2PC across microservices?",
  ["It's too new",
   "It locks resources over the network and blocks if the coordinator fails",
   "It's too fast",
   "It doesn't support SQL"], 1, 4,
  "Distributed locks + single coordinator = fragile at scale. (Details in Advanced module.)",
  ["Amazon", "Google"]),
Q("Saga: book flight ✓, hotel ✓, car ✗. What happens?",
  ["Everything stays booked",
   "Compensating actions run: cancel hotel, cancel flight — semantic rollback",
   "The user is charged anyway",
   "The system crashes"], 1, 5,
  "No true rollback across services — instead, forward-correct with compensations.",
  ["Uber", "Microsoft"]),
Q("Compensating actions must be…",
  ["fast only",
   "idempotent and retryable — they execute during failures",
   "written in Java",
   "manual"], 1, 6,
  "They'll be retried amid chaos; 'cancel booking X' must be safe to run twice.",
  ["Amazon"]),
Q("Choreography vs orchestration in sagas?",
  ["Same thing",
   "Choreography: services react to each other's events. Orchestration: a central coordinator drives steps",
   "One is for dancing",
   "Orchestration is always wrong"], 1, 7,
  "Decentralized events vs centralized conductor — coupling vs visibility tradeoff.",
  ["Netflix"]),
Q("What does a saga NOT give you?",
  ["Atomicity of the overall outcome",
   "Isolation — others may observe intermediate states",
   "Durability",
   "Compensation"], 1, 8,
  "Design for visible in-between states (e.g., 'order processing', not 'order placed').",
  ["Google"]),
Q("When is a saga overkill?",
  ["Always — never use sagas",
   "When one service can do it all, or true strong consistency is required",
   "For e-commerce",
   "When you have more than 2 services"], 1, 10,
  "Don't pay the eventual-consistency price when a local transaction would do.",
  ["Microsoft", "Amazon"]),
]),

L("event-driven", "Event-Driven Architecture",
"""## Events vs commands

- **Command**: "place order" — a request, imperative, expects a result.
- **Event**: "order placed" — a fact about the past, broadcast to whoever cares.

Services publish events; interested services subscribe. Producers don't know consumers.

## Why it scales organizations

Add a fraud-check service? Subscribe to `order.placed` — zero changes to the order
service. Decoupling in *time* (async) and *space* (no direct calls).

## The consistency model

**Eventual**: order service commits, then inventory/search/recommendations update
seconds later. Design UX for it ("processing…").

## Sharp edges

- **Poison messages**: a message that always fails blocks the queue → **dead-letter
  queues** quarantine them for inspection.
- **Ordering**: within a partition keyed by entity (e.g., `order_id`), order is
  preserved; across keys, don't assume it.
- **Event sourcing**: store the event log as the source of truth; rebuild state by
  replay — the audit trail is free.

Brokers: Kafka (log), RabbitMQ (routing), SNS/SQS (managed).
""",
[
Q("An event vs a command?",
  ["Same thing",
   "Event = fact about the past ('order placed'); command = request ('place order')",
   "Events are synchronous",
   "Commands can't fail"], 1, 3,
  "Past-tense facts broadcast; imperative requests directed. The distinction shapes the architecture.",
  ["Amazon", "Uber"]),
Q("Pub/sub decouples producers and consumers in…",
  ["nothing — it's tightly coupled",
   "time (async) and space (producers don't know consumers)",
   "only space",
   "only time"], 1, 4,
  "Add consumers without touching producers — organizational scalability.",
  ["Google", "Netflix"]),
Q("Eventual consistency in practice: order placed, then…",
  ["everything updates instantly",
   "inventory/search update seconds later — design UX for 'processing'",
   "the order is lost",
   "events stop"], 1, 5,
  "Async propagation is the price of decoupling; make intermediate states explicit.",
  ["Amazon"]),
Q("Poison messages are handled with…",
  ["deleting the queue",
   "dead-letter queues — quarantine repeatedly-failing messages for inspection",
   "faster servers",
   "ignoring them"], 1, 6,
  "One bad message must not wedge the whole pipeline forever.",
  ["Microsoft"]),
Q("To preserve ordering for one entity's events…",
  ["use a global lock",
   "partition by entity key (e.g., order_id) so its events stay ordered",
   "send everything twice",
   "ordering is impossible"], 1, 7,
  "Per-key ordering is cheap; global ordering is expensive. Scope it right.",
  ["Kafka", "Amazon"]),
Q("Event sourcing stores as source of truth…",
  ["the latest snapshot only",
   "the append-only event log; state is derived by replay",
   "nothing — it's stateless",
   "the cache"], 1, 8,
  "Replay gives any past state + a free audit trail. (See also: Kafka retention.)",
  ["Google", "Uber"]),
]),
])

MODULES.append(_microservices)


# ---------------------------------------------------------------------------
# MODULE 5 — CLASSIC DESIGN PROBLEMS (6 lessons)
# ---------------------------------------------------------------------------

_classic = M("classic-problems", "Classic Design Problems",
"URL shortener, Twitter feed, WhatsApp chat, rate limiter, distributed lock, "
"Instagram — the exact problems asked at Amazon, Google, Meta, Flipkart.", [

L("url-shortener", "Design: URL Shortener (bit.ly)",
"""## The interview classic

**Requirements**: shorten long URLs; redirect fast; ~100:1 read:write ratio;
millions of URLs.

## The core trick: base62(counter)

Keep an auto-increment counter; encode it in **base62** (a–z, A–Z, 0–9):
ID 125 → `"cb"`. Short, no collisions ever, reversible.

Why not random hashes? Collisions need checking; counters don't collide.

## Scaling the counter

One counter = bottleneck + SPOF. Fixes:
- **Range-based**: each app server gets a block (server A: 1–1M, B: 1M–2M…).
- Or pre-generate IDs into a pool (a dedicated ID service).

## Storage & caching

- DB: `short_key → long_url` (+ created_at, owner). Key-value or SQL both fine.
- **Cache hot URLs** (the viral ones) in Redis — LRU handles it.
- Custom aliases: check availability, reserve the key.

## Analytics

Click counts: exact numbers need writes per click (expensive) — **approximate counters**
(write-behind) are the pragmatic answer.

## The 5-minute interview answer

"Counter + base62 for IDs, KV store for mapping, Redis cache for hot keys, rate-limit
creation, async analytics. Read-heavy, so cache hard."
""",
[
Q("A URL shortener's read:write ratio is typically…",
  ["1:1", "~100:1 read-heavy", "1:100 write-heavy", "0:0"], 1, 2,
  "Links are created once, clicked thousands of times — design for reads.",
  ["Amazon", "Google"]),
Q("Why base62(counter) instead of random hashes?",
  ["Hashes are longer",
   "Counters never collide and stay short; hashes need collision checks",
   "Base62 is encrypted",
   "Counters are random"], 1, 4,
  "Deterministic uniqueness beats probabilistic uniqueness for short codes.",
  ["Microsoft", "Flipkart"]),
Q("A single auto-increment counter becomes a bottleneck. Fix?",
  ["Remove the counter",
   "Range-based allocation per server, or a dedicated ID pool service",
   "Use longer URLs",
   "Shard by URL length"], 1, 5,
  "Distribute ID generation so no single machine serializes all creations.",
  ["Google", "Twitter"]),
Q("Which URLs should be cached?",
  ["All of them forever", "Hot/viral ones — LRU eviction handles the rest",
   "None — caching is unsafe", "Only custom aliases"], 1, 6,
  "A tiny fraction of links gets most clicks; LRU naturally keeps those hot.",
  ["Amazon"]),
Q("Custom alias 'sale' requested twice. Handle by…",
  ["allowing duplicates",
   "checking availability and reserving the key (unique constraint)",
   "appending random text silently",
   "deleting the first"], 1, 7,
  "Uniqueness on the short key is a hard requirement — enforce at write time.",
  ["Microsoft"]),
Q("Click analytics: exact or approximate counts?",
  ["Exact — always",
   "Approximate (write-behind counters) — exact per-click writes are too expensive",
   "No analytics needed",
   "Count in the browser"], 1, 9,
  "Nobody's business decision changes between 1,000,041 and 1,000,000 clicks.",
  ["Google", "Meta"]),
]),

L("twitter-feed", "Design: Twitter/X Feed",
"""## The fanout problem

**Requirements**: post tweets, follow users, home timeline (merged, ranked), millions of users.

## Push vs pull (the heart of the question)

- **Fanout-on-write (push)**: on tweet, write it into every follower's timeline cache.
  Reads are O(1) — but a celebrity with 100M followers turns one tweet into 100M writes.
- **Fanout-on-read (pull)**: on timeline request, fetch followees' recent tweets and merge.
  Cheap writes — but reads do the merging work every time.

## The industry answer: hybrid

Normal users → **push** (fast timelines). Celebrities → **pull** (their tweets are
merged at read time). This bounds the worst case while keeping common reads fast.

## Supporting pieces

- **Pagination**: cursor-based (by tweet ID/time), never OFFSET — tweets shift constantly.
- **Ranking**: separate retrieval (get candidates) from ranking (ML scores them).
- Storage: tweets in a wide-column/KV store keyed by user; timelines in Redis/cache.
""",
[
Q("Fanout-on-write means: on tweet…",
  ["the tweet is deleted",
   "it's pushed into every follower's timeline cache — reads become O(1)",
   "followers are notified by email",
   "the database is locked"], 1, 3,
  "Pay at write time for blissful read time. The classic push model.",
  ["Twitter", "Meta"]),
Q("Pure push breaks when…",
  ["users have no followers",
   "a celebrity with 100M followers tweets → 100M writes for one action",
   "tweets are short",
   "it's raining"], 1, 4,
  "The write amplification of mega-accounts is the canonical scaling problem here.",
  ["Twitter", "Google"]),
Q("Fanout-on-read means…",
  ["tweets are never stored",
   "timelines are computed at read time by merging followees' tweets",
   "users can't post",
   "everything is cached forever"], 1, 5,
  "Cheap writes, expensive reads — the mirror image of push.",
  ["Meta"]),
Q("The production hybrid approach?",
  ["Push for everyone",
   "Pull for everyone",
   "Push for normal users, pull for celebrities — bounds the worst case",
   "Random choice per tweet"], 1, 6,
  "Celebrities' tweets merge at read time; everyone else enjoys precomputed timelines.",
  ["Twitter", "Instagram"]),
Q("Why cursor-based pagination, not OFFSET, for timelines?",
  ["OFFSET is deprecated",
   "Tweets constantly insert at the top — OFFSET pages shift and skip/duplicate",
   "Cursors are shorter",
   "OFFSET doesn't work with Redis"], 1, 7,
  "Stable cursors (by ID/time) survive concurrent inserts; OFFSET doesn't.",
  ["Google", "Meta"]),
Q("In feed systems, retrieval vs ranking?",
  ["Same thing",
   "Retrieval gathers candidate tweets; a separate ML ranker orders them",
   "Ranking happens first",
   "Neither is needed"], 1, 9,
  "Two-stage: cheap candidate generation, then expensive scoring on hundreds, not millions.",
  ["Meta", "TikTok", "Google"]),
]),

L("whatsapp", "Design: WhatsApp / Chat System",
"""## Requirements

1:1 and group chat, real-time delivery, online presence, media sharing, message history.
Billions of messages/day.

## Real-time: WebSockets

**Persistent WebSocket connections** per user — no polling. A connection server can hold
millions of sockets (stateful! — needs careful load balancing and reconnection logic).

## Message flow

```
A sends -> [conn server] -> lookup B's server -> push via B's socket
                                        └─ B offline? store in DB/queue, deliver on reconnect
```

- **Online**: direct push over the socket. Acknowledge with delivery receipts (sent → delivered → read).
- **Offline**: persist to DB/message queue; deliver on reconnect, then mark delivered.

## Presence

"Online / last seen": heartbeat pings update **Redis with TTL**. Expired key = offline.
Simple, fast, self-cleaning.

## Media

Never in the DB: upload to **object storage** (S3) via presigned URL, store only the
pointer + thumbnail in the message record. Thumbnails generated async.

## The honesty point

**Exactly-once delivery is impossible** over unreliable networks. Use **at-least-once +
idempotency**: every message has an ID; receivers dedupe.
""",
[
Q("Why WebSockets instead of polling for chat?",
  ["Polling is illegal",
   "Persistent connections give real-time delivery with low overhead",
   "WebSockets use more battery",
   "Polling doesn't work on mobile"], 1, 3,
  "One open pipe beats thousands of 'anything new?' HTTP requests.",
  ["WhatsApp", "Meta"]),
Q("B is offline when A sends. What happens?",
  ["Message is lost",
   "Stored in DB/queue and delivered when B reconnects",
   "A is notified to retry manually",
   "It's sent by email instead"], 1, 4,
  "Durable store + deliver-on-reconnect = the offline story.",
  ["Telegram", "Google"]),
Q("Connection servers holding millions of sockets are…",
  ["stateless — trivial to scale",
   "stateful — needs sticky routing and careful reconnection handling",
   "impossible to build",
   "only for testing"], 1, 5,
  "The socket IS the state. Losing the server means mass reconnects (thundering herd — stagger them).",
  ["WhatsApp", "Discord"]),
Q("Presence (online/last-seen) via…",
  ["SQL JOINs",
   "Redis with TTL heartbeats — expired key means offline",
   "email pings",
   "blockchain"], 1, 6,
  "Self-cleaning and fast: no cron jobs needed to mark users offline.",
  ["Meta"]),
Q("Chat media (photos/video) should be…",
  ["stored as BLOBs in MySQL",
   "uploaded to object storage (S3); DB keeps only pointers + thumbnails",
   "emailed",
   "kept in RAM"], 1, 7,
  "Blobs bloat databases and bypass CDNs; object storage + CDN is the standard.",
  ["WhatsApp", "Telegram"]),
Q("Exactly-once message delivery is…",
  ["easy with TCP",
   "impossible over unreliable networks — use at-least-once + idempotent message IDs",
   "guaranteed by WebSockets",
   "a solved problem since 1990"], 1, 10,
  "Networks can duplicate or drop; dedupe by ID is the pragmatic answer. Say this in interviews.",
  ["Google", "Amazon"]),
]),

L("rate-limiter", "Design: Rate Limiter",
"""## Why

Protect APIs from abuse, scrapers, bugs, and cost blowups: "100 requests/minute per user."

## Algorithms

- **Token bucket**: bucket holds B tokens, refills at rate R. Each request takes one.
  Allows bursts up to B, then steady R. (Most popular.)
- **Leaky bucket**: requests queue and leak out at fixed rate — smooths bursts.
- **Fixed window**: counter per minute; simple but suffers **boundary spikes**
  (100 at 11:59:59 + 100 at 12:00:00 = 200 in 2 seconds).
- **Sliding window log/counter**: precise (log) vs cheap (counter) — accuracy/memory tradeoff.

## Distributed reality

Requests hit different servers → the counter must be **shared** (Redis: INCR + EXPIRE,
or Lua script for atomicity). Local counters per server are wrong.

## Where it lives

At the **API gateway** (edge) — reject early before work is done. Return headers:
`X-RateLimit-Limit`, `-Remaining`, `-Reset`, and **429 Too Many Requests** with
`Retry-After` when exceeded.
""",
[
Q("Rate limiting protects against…",
  ["slow internet",
   "abuse, scrapers, buggy clients, and cost blowups",
   "typos",
   "power outages"], 1, 3,
  "It's the bouncer at the API door — every public API needs one.",
  ["Amazon", "Cloudflare"]),
Q("Token bucket: tokens refill at rate R, burst capacity B. A request needs…",
  ["R tokens", "one token — bursts up to B allowed, then steady rate R",
   "B tokens", "no tokens"], 1, 4,
  "Burst-friendly but bounded: the best of both worlds, hence its popularity.",
  ["Google", "Stripe"]),
Q("Fixed window's flaw?",
  ["It's too complex",
   "Boundary spike: 100 requests at 11:59:59 + 100 at 12:00:00 = 200 in 2s",
   "It can't count",
   "It needs a database"], 1, 5,
  "Window edges allow 2x the intended rate. Sliding windows fix it.",
  ["Microsoft"]),
Q("Sliding window log vs counter?",
  ["Identical",
   "Log = precise per-request timestamps (memory heavy); counter = approximate (cheap)",
   "Counter is always better",
   "Log is always better"], 1, 6,
  "Precision costs memory. Most systems use the counter approximation.",
  ["Amazon"]),
Q("Why must distributed rate limiting use a shared store like Redis?",
  ["Redis is trendy",
   "Requests land on different servers — local counters would each allow the full quota",
   "It's faster",
   "Servers can't count"], 1, 7,
  "10 servers × 100/min local limit = 1000/min actual. Shared state or it's theater.",
  ["Google", "Uber"]),
Q("When limited, the API should return…",
  ["200 OK anyway",
   "429 Too Many Requests + Retry-After, with X-RateLimit-* headers",
   "500 error",
   "Nothing — drop silently"], 1, 8,
  "Standard headers let well-behaved clients back off gracefully.",
  ["Stripe", "GitHub", "Twitter"]),
]),

L("distributed-lock", "Design: Distributed Lock",
"""## Why local mutexes fail

`synchronized` / `Lock()` works inside ONE process. With 10 servers running a cron
"every minute," you need agreement across machines: run it exactly once.

## Redis recipe (the standard)

```
SET lock:job <unique-token> NX PX 30000
```
- **NX**: set only if absent (atomic acquire).
- **PX 30000**: auto-expire in 30s — a crashed holder can't block forever.
- **unique token**: so only the holder can release it (compare-and-del before DEL, via Lua).

## The fencing problem

Holder pauses (GC) past the TTL → lock expires → another acquires → BOTH think they
hold it. Fix: **fencing tokens** — a monotonic number issued with each lock; storage
rejects writes with stale tokens. (How Chubby/ZooKeeper-backed systems stay safe.)

## Redlock

Acquire on a **majority of independent Redis masters** within a time bound. Tolerates
minority failures. Debated by experts (Martin Kleppmann's critique is famous) — know
it exists, know the controversy.

## Better: avoid locks

Often you can sidestep: idempotent jobs + "claim a row" in the DB, or a real queue
(SQS/Kafka) instead of "exactly one runner."
""",
[
Q("A local mutex doesn't work across…",
  ["threads", "multiple servers/processes — it only guards one process",
   "functions", "lines of code"], 1, 3,
  "Distributed coordination needs a shared arbiter (Redis, ZooKeeper, DB).",
  ["Amazon", "Google"]),
Q("In SET key val NX PX 30000, NX means…",
  ["no expiry",
   "set only if the key does NOT already exist — atomic acquire",
   "execute 10 times",
   "non-blocking"], 1, 4,
  "The atomic check-and-set is the entire trick; without NX it's just a write.",
  ["Redis", "Microsoft"]),
Q("Why auto-expire (PX) the lock?",
  ["To save memory",
   "A crashed holder must not block the lock forever",
   "It's required by law",
   "To make it faster"], 1, 5,
  "Leases, not ownership: liveness over perfection.",
  ["Google", "Uber"]),
Q("Fencing tokens solve…",
  ["slow networks",
   "a paused-then-expired holder acting alongside the new holder — storage rejects stale tokens",
   "encryption",
   "leader election"], 1, 6,
  "Monotonic tokens make 'who's really the holder' decidable at the resource.",
  ["Amazon"]),
Q("Redlock acquires the lock on…",
  ["one Redis",
   "a majority of independent Redis masters within a time bound",
   "all databases",
   "the client"], 1, 7,
  "Majority agreement tolerates minority node failures. (Know Kleppmann's critique too.)",
  ["Redis", "Google"]),
Q("Often better than a distributed lock?",
  ["A bigger lock",
   "Idempotent jobs + DB row claiming, or a real queue — sidestep coordination",
   "No jobs at all",
   "More servers"], 1, 9,
  "The best lock is the one you don't need. Design it away when possible.",
  ["Amazon", "Stripe"]),
]),

L("instagram", "Design: Instagram (Media Feed)",
"""## Requirements

Photo/video sharing, feed, stories (24h expiry), explore. Media-heavy = bandwidth-heavy.

## Upload flow (async!)

```
client -> API -> presigned S3 URL -> client uploads directly to S3
   -> message queued -> workers generate thumbnails/sizes -> metadata in DB
```

Never block the user on processing. Thumbnails/sizes fan out via a **queue**.

## Feed

Same bones as Twitter (Module 5, lesson 2): follow graph → candidate generation →
**ML ranking**. Media makes it heavier: aggressive **CDN** usage for images/video,
multiple resolutions per upload.

## Stories

24-hour TTL: storage with **time-based expiry**, cheap cleanup. Viewed-state in Redis.

## The CDN point (say it in interviews)

"Instagram is a CDN company that happens to have an app." Images/video dominate cost
and latency — edge caching isn't optional, it's the architecture.

## Celebrity problem, again

Same hybrid push/pull fanout as Twitter for mega-accounts.
""",
[
Q("Instagram uploads should…",
  ["block until thumbnails finish",
   "go direct-to-S3 via presigned URL, with async workers generating sizes via queue",
   "be stored in MySQL BLOBs",
   "skip processing"], 1, 3,
  "Fast UX + resilient processing: the queue absorbs spikes.",
  ["Instagram", "Meta"]),
Q("Why generate thumbnails asynchronously?",
  ["It's trendier",
   "Blocking the upload on processing = slow UX and timeout risk under load",
   "Thumbnails are optional",
   "S3 requires it"], 1, 4,
  "User-perceived latency is sacred; heavy work goes to background workers.",
  ["Google"]),
Q("Stories' 24h expiry is best implemented with…",
  ["a daily cron deleting rows",
   "time-based TTL expiry on storage",
   "manual deletion",
   "never deleting"], 1, 5,
  "TTL = self-cleaning, no batch jobs, no missed rows.",
  ["Meta", "Snapchat"]),
Q("Why is CDN usage even more critical for Instagram than Twitter?",
  ["Tweets can't be cached",
   "Images/video dominate bandwidth and latency — edge delivery is the architecture",
   "CDNs are free",
   "Instagram invented CDNs"], 1, 6,
  "Media weight makes origin-serving economically and physically impossible at scale.",
  ["Meta", "Cloudflare"]),
Q("Feed generation for Instagram vs Twitter: core difference?",
  ["Completely different",
   "Same fanout bones + ML ranking, but media-heavy (resolutions, CDN, async processing)",
   "Instagram has no feed",
   "Twitter is harder"], 1, 7,
  "Recognize the pattern, then name the media-specific additions — that's senior thinking.",
  ["Meta", "Google"]),
Q("A celebrity posts; 50M followers. Feed fanout strategy?",
  ["Push to all 50M timelines synchronously",
   "Hybrid: pull/merge at read time for mega-accounts (same as Twitter)",
   "Don't show the post",
   "Email everyone"], 1, 8,
  "The pattern transfers across products — interviewers love when you connect them.",
  ["Instagram", "Twitter", "TikTok"]),
]),
])

MODULES.append(_classic)


# ---------------------------------------------------------------------------
# MODULE 6 — ADVANCED (5 lessons)
# ---------------------------------------------------------------------------

_advanced = M("advanced", "Advanced Topics",
"Kafka and event streaming, Raft consensus, distributed transactions (2PC), "
"observability, and gossip protocols.", [

L("kafka-streaming", "Kafka & Event Streaming",
"""## The distributed commit log

**Kafka** stores events in an append-only **log**, partitioned across brokers.
Unlike a queue, consumed messages are NOT deleted — they're retained (days/weeks)
for replay.

```
topic "orders" : [partition 0][partition 1][partition 2]
consumer group A: each consumer takes some partitions (parallel)
consumer group B: gets ALL messages too (broadcast across groups)
```

## Key mechanics

- **Partitions** = parallelism + per-key ordering (same key → same partition).
- **Consumer groups**: within a group, partitions split across consumers; across
  groups, everyone gets everything.
- **Retention**: old events stay — new consumers can replay history, debugging is sane.

## Kafka vs RabbitMQ

- **Kafka**: dumb broker, smart log — massive throughput, replay, event sourcing.
- **RabbitMQ**: smart broker — flexible routing, per-message acks, lower latency for small loads.

## Exactly-once?

Idempotent producers + transactions get you there *within Kafka*. End-to-end
across systems remains famously hard — say so in interviews.
""",
[
Q("Kafka stores consumed messages…",
  ["by deleting them immediately",
   "durably in an append-only log, retained for replay",
   "in RAM only",
   "nowhere"], 1, 3,
  "The log is the point: replay, new consumers, debugging — all free.",
  ["LinkedIn", "Uber"]),
Q("Partitions give Kafka…",
  ["encryption",
   "parallelism plus ordering per key",
   "smaller disks",
   "free monitoring"], 1, 4,
  "Same key → same partition → order preserved where it matters.",
  ["Netflix", "Amazon"]),
Q("Two consumer groups on one topic: each group gets…",
  ["half the messages",
   "ALL messages (broadcast across groups, split within a group)",
   "nothing",
   "only errors"], 1, 5,
  "Groups are independent subscriptions; partitioning parallelizes inside a group.",
  ["Uber", "Google"]),
Q("Kafka vs RabbitMQ, one line?",
  ["Identical",
   "Kafka: high-throughput replayable log. RabbitMQ: smart routing, per-message ack",
   "RabbitMQ is faster at everything",
   "Kafka can't persist"], 1, 6,
  "Log-centric vs broker-smart — pick by workload shape.",
  ["Microsoft"]),
Q("Why keep old events (retention)?",
  ["Waste of disk",
   "Replay for new consumers, reprocessing, debugging, event sourcing",
   "Regulations forbid deletion",
   "It speeds up writes"], 1, 7,
  "History is a feature: rebuild any derived state by replaying.",
  ["LinkedIn"]),
Q("End-to-end exactly-once delivery across systems is…",
  ["trivial",
   "famously hard — idempotent consumers + dedupe IDs is the pragmatic answer",
   "guaranteed by Kafka alone",
   "impossible to even approximate"], 1, 8,
  "Say the honest thing: at-least-once + idempotency, everywhere.",
  ["Google", "Amazon"]),
]),

L("raft-consensus", "Consensus: Raft",
"""## Why consensus exists

Who is the leader? Did everyone commit this write? In an unreliable network,
nodes must **agree** despite failures — that's consensus. It underpins etcd,
Consul, and Kubernetes' control plane.

## Raft in 60 seconds

- Nodes are **leader**, **follower**, or **candidate**.
- The **leader** receives all writes, replicates log entries to followers.
- Elections: followers time out → become candidates → request votes. Needs a
  **majority (quorum)** — two candidates can't both win a majority.
- Committed once on a majority = durable even if the leader dies.

## Partitions

Minority side can't reach majority → can't elect a leader → **stops**. Safe by
design: no split-brain, just unavailability on the small side.

## Why not "just use a database" for leader election?

Chicken-and-egg: the election mechanism must work *before* any DB is trustworthy.
Consensus IS the primitive — etcd/ZooKeeper sell it as a service.

## Paxos vs Raft

Same guarantees; **Raft was designed for understandability** (Diego Ongaro's thesis).
In interviews, describing Raft correctly beats name-dropping Paxos.
""",
[
Q("Consensus solves…",
  ["slow queries",
   "agreement among nodes despite failures (who leads? what committed?)",
   "CSS layout",
   "password strength"], 1, 4,
  "The foundation under leader election, config management, and commit protocols.",
  ["Google", "Amazon"]),
Q("In Raft, the leader…",
  ["does nothing",
   "receives all writes and replicates log entries to followers",
   "is elected every second",
   "stores no data"], 1, 5,
  "Single writer simplifies everything; followers are hot standbys with full logs.",
  ["Google"]),
Q("Why does Raft require a majority (quorum)?",
  ["Majorities are faster",
   "Two majorities always overlap — two leaders can't both win",
   "It's traditional",
   "Minorities are illegal"], 1, 6,
  "Overlap is the mathematical trick that prevents split-brain.",
  ["Microsoft", "Amazon"]),
Q("Network partition: the minority side…",
  ["elects its own leader and keeps writing",
   "can't reach majority → can't elect a leader → halts (safe, unavailable)",
   "deletes its data",
   "doubles throughput"], 1, 7,
  "Safe by design: unavailability beats divergence.",
  ["Google"]),
Q("Why not use a regular database for leader election?",
  ["You can — it's ideal",
   "Chicken-and-egg: election must work before any DB is trustworthy",
   "Databases are too fast",
   "It's too cheap"], 1, 8,
  "Consensus is the primitive; etcd/ZooKeeper exist precisely to provide it.",
  ["Amazon"]),
Q("Paxos vs Raft?",
  ["Raft is weaker",
   "Same guarantees; Raft was designed to be understandable",
   "Paxos is newer",
   "They solve different problems"], 1, 9,
  "Describe Raft well in an interview — clarity beats name-dropping.",
  ["Google", "Microsoft"]),
]),

L("distributed-tx", "Distributed Transactions & 2PC",
"""## Two-phase commit (2PC)

The classic: a **coordinator** asks all participants to **prepare** (vote yes/no),
then broadcasts **commit** or **abort**.

```
coordinator -> "prepare?" -> participants vote
coordinator -> "commit!"   -> everyone commits
```

## The fatal flaw

Coordinator crashes after "prepare" but before "commit" → participants **block**,
holding locks indefinitely, waiting for a dead coordinator. 3PC adds a pre-commit
phase but still blocks under partitions. This is why microservices avoid 2PC
(see the Saga lesson).

## When 2PC is honestly fine

Few participants, low latency, single datacenter — and systems like **Spanner**
that harden it with Paxos replication of the coordinator.

## The pragmatic alternative: transactional outbox

Write the business row AND the event row in **one local transaction**; a relay
process publishes the events afterward. Reliable messaging without distributed
coordination.

## Google Spanner: the exception

Globally consistent SQL via **TrueTime** (atomic clocks bounding clock uncertainty)
+ 2PC + Paxos. Proof that with enough engineering (and atomic clocks), you can
have your cake — most of us just buy the cake (managed Spanner).
""",
[
Q("2PC's two phases?",
  ["read and write",
   "prepare (vote) then commit/abort",
   "lock and unlock",
   "map and reduce"], 1, 4,
  "Everyone votes, then the coordinator decides for all.",
  ["Google", "Oracle"]),
Q("2PC's fatal flaw?",
  ["It's too fast",
   "Coordinator crash after prepare → participants block holding locks",
   "It doesn't work with SQL",
   "It's patented"], 1, 5,
  "Blocking on coordinator failure is why distributed systems moved on.",
  ["Amazon", "Microsoft"]),
Q("3PC vs 2PC?",
  ["3PC is always safe",
   "Adds a pre-commit phase; still blocks under partitions — not a real fix",
   "3PC is faster",
   "They're unrelated"], 1, 6,
  "More phases, same fundamental blocking problem.",
  ["Google"]),
Q("Transactional outbox pattern?",
  ["A bigger inbox",
   "Write business row + event row in ONE local transaction; a relay publishes events",
   "Delete the outbox",
   "Use 2PC anyway"], 1, 7,
  "Reliable 'DB + message' without distributed coordination — the pragmatic standard.",
  ["Uber", "Amazon"]),
Q("When is 2PC actually acceptable?",
  ["Never, ever",
   "Few participants, low latency, single DC — or hardened like Spanner",
   "Across continents with 100 services",
   "For caching"], 1, 8,
  "Scope it tightly or engineer it massively. Middle grounds suffer.",
  ["Google"]),
Q("Spanner achieves global consistency via…",
  ["luck",
   "TrueTime (atomic clocks) + 2PC + Paxos replication",
   "eventual consistency only",
   "a single giant server"], 1, 10,
  "Bounding clock uncertainty lets it order transactions globally — atomic clocks as a primitive!",
  ["Google"]),
]),

L("observability", "Observability: Metrics, Logs, Traces",
"""## The three pillars

- **Metrics**: numbers over time (request rate, error rate, latency histograms). Aggregatable, cheap, dashboard-friendly (Prometheus).
- **Logs**: discrete events with context ("order 42 failed: timeout after 2s"). Grep-able (ELK/Loki).
- **Traces**: one request's journey across services, with per-span timings. Find the slow span (Jaeger/Tempo).

## Methods

- **RED** (per service): Rate, Errors, Duration.
- **USE** (per resource): Utilization, Saturation, Errors.

## Correlation IDs

Propagate a request ID through every service call. Suddenly 40 services' logs stitch
into one story. Without it, distributed debugging is archaeology.

## Alert on symptoms, not causes

"Checkout success rate < 99%" (user pain) beats "CPU > 80%" (maybe fine). SLO-based
alerts page humans for what matters.

## Cardinality: the Prometheus footgun

A label per `user_id` = millions of time series = OOM. Keep label cardinality low
(service, endpoint, status — not user, not request ID).
""",
[
Q("Metrics vs logs?",
  ["Same thing",
   "Metrics = numbers over time (aggregatable); logs = discrete events with context",
   "Logs are faster",
   "Metrics can't be graphed"], 1, 3,
  "Different tools for different questions: 'how many' vs 'what happened'.",
  ["Google", "Datadog"]),
Q("Distributed traces show…",
  ["CPU temperature",
   "one request's path across services with per-span timings",
   "the git history",
   "database schema"], 1, 4,
  "Find the slow span instead of guessing which of 40 services is at fault.",
  ["Uber", "Netflix"]),
Q("RED method tracks per service…",
  ["Read, Edit, Delete", "Rate, Errors, Duration",
   "Red, Green, Blue", "Retries, Errors, Delays"], 1, 5,
  "The three numbers that describe any request-serving service.",
  ["Google"]),
Q("Correlation/request IDs let you…",
  ["skip authentication",
   "stitch logs across 40 services into one request's story",
   "make requests faster",
   "avoid load balancers"], 1, 6,
  "Propagate the ID everywhere; distributed debugging becomes tractable.",
  ["Amazon", "Microsoft"]),
Q("Better alert?",
  ["'CPU > 80%'",
   "'Checkout success rate < 99%' — alert on user-facing symptoms, not causes",
   "'Disk 50% full'",
   "'It's Tuesday'"], 1, 7,
  "SLO-based paging: humans wake for user pain, not for maybe-fine signals.",
  ["Google", "SRE"]),
Q("Prometheus label per user_id causes…",
  ["faster queries",
   "cardinality explosion — millions of series, OOM",
   "better security",
   "nothing bad"], 1, 8,
  "Low-cardinality labels only (service/endpoint/status). This mistake has killed many clusters.",
  ["Grafana", "Uber"]),
]),

L("gossip-failure", "Gossip Protocols & Failure Detection",
"""## Rumors that scale

**Gossip**: each node periodically exchanges state with a few random peers. Information
spreads exponentially — like rumors — reaching thousands of nodes in ~log(n) rounds,
with no central coordinator.

## Failure detection

If nobody has heard from node X recently, suspect it, then declare it dead. Used by
Cassandra and Consul for cluster membership.

## Phi-accrual: smarter timeouts

Fixed timeouts ("no heartbeat in 5s = dead") false-positive on slow networks.
**Phi-accrual** models the normal heartbeat arrival distribution and computes suspicion
level φ — adaptive to actual network conditions (Cassandra's implementation).

## Anti-entropy

Background reconciliation so replicas converge: compare **Merkle trees** (hash trees)
to find differing ranges efficiently, then sync only those. Gossip spreads membership;
anti-entropy repairs data.

## What gossip is NOT for

Membership and metadata — not the data path itself. Cassandra gossips about *who's
alive and what schema version*; actual reads/writes use direct coordination.
""",
[
Q("In gossip protocols, nodes…",
  ["report to a central master",
   "periodically exchange state with random peers — info spreads exponentially",
   "never communicate",
   "use only broadcasts"], 1, 4,
  "Rumor-style dissemination: no coordinator, ~log(n) rounds to converge.",
  ["Amazon", "Apple"]),
Q("Gossip-based failure detection: node X is declared dead when…",
  ["an admin says so",
   "no peer has heard from X recently (suspect, then confirm)",
   "X sends a goodbye message",
   "CPU is high"], 1, 5,
  "Absence of heartbeats across the gossip network = presumed failure.",
  ["Cassandra", "Consul"]),
Q("Phi-accrual improves on fixed timeouts by…",
  ["being simpler",
   "modeling normal heartbeat distribution — suspicion adapts to network conditions",
   "using bigger timeouts",
   "removing timeouts"], 1, 6,
  "Adaptive suspicion beats '5 seconds means dead' on real networks.",
  ["Cassandra"]),
Q("Anti-entropy with Merkle trees…",
  ["heats the servers",
   "efficiently finds differing data ranges between replicas, then syncs only those",
   "encrypts gossip",
   "elects leaders"], 1, 7,
  "Compare hash trees top-down; descend only into differing branches.",
  ["Amazon", "Riak"]),
Q("Why use gossip instead of a central registry for membership?",
  ["Gossip is slower",
   "No SPOF; scales to thousands of nodes without a coordinator bottleneck",
   "Central registries are illegal",
   "Gossip uses less code"], 1, 8,
  "Membership itself must survive the failures it's tracking.",
  ["Google"]),
Q("Cassandra uses gossip for…",
  ["storing all user data",
   "cluster membership + schema versions — not the data path itself",
   "query execution",
   "client connections"], 1, 9,
  "Right tool per plane: gossip for membership, direct coordination for data.",
  ["Apple", "Netflix"]),
]),
])

MODULES.append(_advanced)


# ---------------------------------------------------------------------------
# CURRICULUM assembly + attachment to sibling's seeded system-design domain
# ---------------------------------------------------------------------------

CURRICULUM = {"domain": DOMAIN, "modules": MODULES}

# Sibling migration n3o4trend001_new_domains seeds domain 'system-design' with
# 4 modules. The 6 deep-content modules below attach to those existing modules —
# no competing modules are created.
SIBLING_DOMAIN_SLUG = "system-design"
MODULE_MAP = {
    "scalability-basics": "scalability",
    "caching": "load-balancing",
    "databases-scale": "db-scale",
    "microservices": "microservices-design",
    "classic-problems": "scalability",
    "advanced": "microservices-design",
}


import uuid as _uuid
from datetime import datetime, timezone as _tz


def _lesson_id(slug):
    return str(_uuid.uuid5(_uuid.NAMESPACE_URL, "skillforge:sd:lesson:" + slug))


def _question_id(lesson_slug, idx):
    return str(_uuid.uuid5(
        _uuid.NAMESPACE_URL, f"skillforge:sd:question:{lesson_slug}:{idx}"))


def _now_iso():
    return datetime.now(_tz.utc).isoformat()


def _as_sql_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (list, dict)):
        v = json.dumps(v, ensure_ascii=False)
    return "'" + str(v).replace("'", "''") + "'"


def _iter_rows():
    """Yield (kind, dict) for every lesson and question, mapped to the
    sibling's already-seeded system-design modules."""
    order_per_module = {}
    for m in CURRICULUM["modules"]:
        sib = MODULE_MAP[m["slug"]]
        order_per_module.setdefault(sib, 100)
        for les in m["lessons"]:
            lid = _lesson_id(les["slug"])
            order_per_module[sib] += 1
            yield ("lesson", {
                "id": lid,
                "module_slug": sib,
                "slug": les["slug"],
                "title": les["title"],
                "content": les["theory_md"],
                "order_index": order_per_module[sib],
            })
            for qi, q in enumerate(les["questions"]):
                yield ("question", {
                    "id": _question_id(les["slug"], qi),
                    "lesson_id": lid,
                    "module_slug": sib,
                    "qtype": "mcq",
                    "difficulty": q["difficulty"],
                    "prompt": q["prompt"],
                    "choices": q["choices"],
                    "answer_index": q["answer_index"],
                    "explanation": q["explanation"],
                    "company_tags": q["company_tags"],
                })


def emit_sql(out=None):
    """Emit INSERTs against the real curriculum_* tables.

    Lessons attach to the sibling's already-seeded system-design modules via a
    module_id subselect; questions carry domain/module slugs + lesson_id.
    Safe to run after migration n3o4trend001_new_domains.
    """
    out = out or sys.stdout
    ts = _now_iso()
    for kind, r in _iter_rows():
        if kind == "lesson":
            out.write(
                "INSERT INTO curriculum_lessons "
                "(id, module_id, slug, title, content, order_index, "
                "estimated_minutes, has_visual) "
                "SELECT %s, m.id, %s, 30, 0 FROM curriculum_modules m "
                "WHERE m.slug = %s AND m.domain_slug = %s;\n"
                % (_as_sql_value(r["id"]),
                   ", ".join(_as_sql_value(r[k]) for k in
                             ("slug", "title", "content", "order_index")),
                   _as_sql_value(r["module_slug"]),
                   _as_sql_value(SIBLING_DOMAIN_SLUG)))
        else:
            out.write(
                "INSERT INTO curriculum_questions "
                "(id, domain_slug, module_slug, lesson_id, difficulty, qtype, "
                "prompt, choices, answer_index, explanation, company_tags, "
                "created_at) VALUES (%s);\n"
                % ", ".join([
                    _as_sql_value(r["id"]),
                    _as_sql_value(SIBLING_DOMAIN_SLUG),
                    _as_sql_value(r["module_slug"]),
                    _as_sql_value(r["lesson_id"]),
                    str(r["difficulty"]),
                    _as_sql_value(r["qtype"]),
                    _as_sql_value(r["prompt"]),
                    _as_sql_value(r["choices"]),
                    _as_sql_value(r["answer_index"]),
                    _as_sql_value(r["explanation"]),
                    _as_sql_value(r["company_tags"]),
                    _as_sql_value(ts),
                ]))
    out.flush()


def seed(session=None):
    """Insert the deep system-design content pack.

    Uses the real SQLAlchemy models (app.adapters.outbound.models).
    Attaches lessons/questions to the sibling's seeded 'system-design' domain.
    Idempotent on lesson/question ids (deterministic uuid5) — skips existing.
    Returns counts dict.
    """
    from app.adapters.outbound.models import (
        CurriculumLessonModel, CurriculumQuestionModel, CurriculumModuleModel,
    )
    counts = {"lessons": 0, "questions": 0, "skipped": 0}
    mod_ids = {}
    for m in CURRICULUM["modules"]:
        sib = MODULE_MAP[m["slug"]]
        if sib not in mod_ids:
            mod = session.query(CurriculumModuleModel).filter_by(
                slug=sib, domain_slug=SIBLING_DOMAIN_SLUG).one()
            mod_ids[sib] = mod.id
    for kind, r in _iter_rows():
        if kind == "lesson":
            exists = session.query(CurriculumLessonModel).filter_by(
                id=r["id"]).first()
            if exists:
                counts["skipped"] += 1
                continue
            session.add(CurriculumLessonModel(
                id=r["id"], module_id=mod_ids[r["module_slug"]],
                slug=r["slug"], title=r["title"], content=r["content"],
                order_index=r["order_index"], estimated_minutes=30,
                has_visual=False))
            counts["lessons"] += 1
        else:
            exists = session.query(CurriculumQuestionModel).filter_by(
                id=r["id"]).first()
            if exists:
                counts["skipped"] += 1
                continue
            session.add(CurriculumQuestionModel(
                id=r["id"], domain_slug=SIBLING_DOMAIN_SLUG,
                module_slug=r["module_slug"], lesson_id=r["lesson_id"],
                difficulty=r["difficulty"], qtype=r["qtype"],
                prompt=r["prompt"],
                choices=json.dumps(r["choices"]) if r["choices"] else None,
                answer_index=r["answer_index"], explanation=r["explanation"],
                company_tags=json.dumps(r["company_tags"]),
                created_at=datetime.now(_tz.utc)))
            counts["questions"] += 1
    session.commit()
    return counts


def verify_counts():
    modules = CURRICULUM["modules"]
    lessons = sum(len(m["lessons"]) for m in modules)
    mcqs = sum(len(les["questions"]) for m in modules for les in m["lessons"])
    per_module = {m["slug"]: (len(m["lessons"]),
                              sum(len(les["questions"]) for les in m["lessons"]))
                  for m in modules}
    narrow = [les["slug"] for m in modules for les in m["lessons"]
              if les["difficulty_max"] - les["difficulty_min"] < 4]
    unmapped = [m["slug"] for m in modules if m["slug"] not in MODULE_MAP]
    return {"modules": len(modules), "lessons": lessons, "mcqs": mcqs,
            "total_questions": mcqs,
            "per_module": per_module, "narrow_lessons": narrow,
            "unmapped_modules": unmapped}


if __name__ == "__main__":
    c = verify_counts()
    print("modules:", c["modules"])
    print("lessons:", c["lessons"])
    print("mcq questions:", c["mcqs"])
    print("TOTAL questions:", c["total_questions"])
    print("\nper module (lessons, mcqs) -> sibling module:")
    for m in CURRICULUM["modules"]:
        nl, nq = c["per_module"][m["slug"]]
        print(f"  {m['slug']:20s} lessons={nl:2d} mcqs={nq:3d} -> {MODULE_MAP[m['slug']]}")
    assert not c["narrow_lessons"], c["narrow_lessons"]
    assert not c["unmapped_modules"], c["unmapped_modules"]
    print("\nOK: all lessons span >= 4 difficulty points, all modules mapped.")
