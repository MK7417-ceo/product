"""Seed content: DBMS — Modules 4-6 (Transactions, Indexing & Optimization, Advanced).

All theory is original, written for SkillForge (interview-focused).
Precedence graphs, B+ tree height math, and lock-compatibility answers
were verified by hand while authoring.

Usage:
    from app.adapters.outbound.dbms_part_m4m5m6 import MODULES, LESSONS, QUESTIONS
"""

from __future__ import annotations

from app.domain.curriculum import (
    CurriculumLesson,
    CurriculumModule,
    CurriculumQuestion,
    validate_curriculum_question,
)

DOMAIN_SLUG = "dbms"

MODULES = [
    CurriculumModule(
        id="dbms-m4",
        domain_slug=DOMAIN_SLUG,
        slug="transactions",
        name="Transactions",
        description=(
            "ACID properties, transaction states, schedules, conflict and view "
            "serializability, lock-based protocols with 2PL, deadlocks, timestamp "
            "ordering, and MVCC — the concurrency-control core every interview probes."
        ),
        order_index=4,
        estimated_days=8,
    ),
    CurriculumModule(
        id="dbms-m5",
        domain_slug=DOMAIN_SLUG,
        slug="indexing-optimization",
        name="Indexing & Optimization",
        description=(
            "How indexes work (dense vs sparse), B+ trees with worked height math, "
            "clustered vs non-clustered indexes, hash indexing, cost-based query "
            "optimization and EXPLAIN, and the four join algorithms."
        ),
        order_index=5,
        estimated_days=7,
    ),
    CurriculumModule(
        id="dbms-m6",
        domain_slug=DOMAIN_SLUG,
        slug="advanced-topics",
        name="Advanced Topics",
        description=(
            "NoSQL data models (document, key-value, column-family, graph), the CAP "
            "theorem, replication vs sharding, and MongoDB modeling with a practical "
            "SQL-vs-NoSQL decision guide."
        ),
        order_index=6,
        estimated_days=5,
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


def _mkl(lid, module_id, slug, title, content, order_index, minutes=35):
    return CurriculumLesson(
        id=lid,
        module_id=module_id,
        slug=slug,
        title=title,
        content=content,
        order_index=order_index,
        estimated_minutes=minutes,
        has_visual=False,
    )


# ---------------------------------------------------------------------------
# MODULE 4 — TRANSACTIONS
# ---------------------------------------------------------------------------

_M4 = "dbms-m4"
_M4_SLUG = "transactions"

LESSONS_M4 = [
    _mkl(
        "dbms-m4-l1", _M4, "acid-properties", "ACID Properties",
        """## What is a transaction?

A **transaction** is a single logical unit of work — a sequence of database
operations that must be treated as all-or-nothing. The classic example is a
bank transfer: debit Rs. 5000 from account A **and** credit Rs. 5000 to
account B. Four properties, remembered as **ACID**, define what a transaction
guarantees:

**Atomicity** — all or nothing. Either every operation in the transaction
completes, or none of them take effect. If the system crashes after debiting
A but before crediting B, recovery must undo the debit. Money can never
appear or vanish halfway through.

**Consistency** — a transaction moves the database from one valid state to
another, preserving every rule: constraints, triggers, business invariants.
The transfer preserves "total money is conserved" and "no negative
balances". Note the split of responsibility: the DBMS enforces *declared*
constraints, but the *application* must write correct transaction logic.

**Isolation** — concurrent transactions must not interfere with each other.
If two transfers touch the same accounts at the same time, the final result
must be as if they ran one after another. Without isolation you get lost
updates and dirty reads (the next lessons dissect these).

**Durability** — once a transaction commits, its effects survive crashes,
power failures, everything. The DBMS delivers this with write-ahead
logging: committed changes reach stable storage before the commit is
acknowledged to the application.

## Interview tip

When asked "which property?", map the failure to the fix: a crash
mid-transfer fixed by rollback is **atomicity**; two transfers interleaving
safely is **isolation**; surviving a power cut after commit is **durability**;
money conserved across the transfer is **consistency**.
""",
        1,
    ),
    _mkl(
        "dbms-m4-l2", _M4, "transaction-states", "Transaction States",
        """## The life of a transaction

A transaction moves through a small set of states:

- **Active** — it is executing its operations.
- **Partially committed** — the last statement finished, but the commit
  record is not yet safely on disk. A crash *here* still means rollback.
- **Committed** — the commit record is durable. The effects are permanent.
- **Failed** — something went wrong (constraint violation, deadlock, crash).
- **Aborted** — after a failed transaction's changes are rolled back, it is
  as if it never ran. (Some textbooks add a final **terminated** state.)

The dangerous gap is between *partially committed* and *committed*: the work
is done, but durability is not yet guaranteed.

## Write-ahead logging (WAL)

The bridge across that gap is the **system log** plus one golden rule:
**log before data**. Before any changed data page is written to disk, a log
record describing the change is forced to stable storage. If the system
crashes, recovery replays the log — redoing committed transactions and
undoing the rest. WAL is what makes atomicity and durability *implementable*
rather than wishful thinking: the log is the source of truth, the data
pages are just a cache of it.

## Checkpoints

Replaying the entire log from the beginning of time would make recovery
unbearably slow, so the system periodically takes a **checkpoint**: flush all
dirty pages to disk and note the position in the log. Recovery then only
replays from the last checkpoint — this bounds recovery time after a crash.
""",
        2,
    ),
    _mkl(
        "dbms-m4-l3", _M4, "schedules", "Schedules",
        """## Serial vs concurrent schedules

When transactions run together, the DBMS interleaves their operations. That
interleaving is called a **schedule**. A **serial** schedule runs transactions
strictly one after another — safe but slow. A **concurrent** schedule
interleaves operations — fast but risky.

Why accept the risk? **Throughput**: while T1 waits on disk I/O, T2 can use
the CPU, and average response time drops. But interleaving can corrupt data.
The classic **lost update**: T1 and T2 both read balance = 100, both add 50,
both write 150. The correct answer is 200 — one update is silently lost.

## When is an interleaving safe?

A schedule is **serializable** if its final effect equals *some* serial
schedule. That is the gold standard of correctness for concurrency.

Three weaker guarantees concern reads of uncommitted data:

- **Recoverable**: if T2 reads data written by T1, T2 must commit *after*
  T1 commits. Otherwise T2 could commit based on data that later gets
  rolled back.
- **Cascadeless**: stronger — a transaction may only read *committed*
  values. Nobody ever sees uncommitted data, so one abort never forces
  others to abort in a cascade.
- **Strict**: strongest — a transaction may neither read nor *overwrite*
  uncommitted data. Strict schedules are automatically recoverable and
  cascadeless, and easy to implement (hold write locks till commit).

## The hierarchy

**Strict ⊂ cascadeless ⊂ recoverable.** A **dirty read** — reading a value
written by a not-yet-committed transaction — breaks all three when the
writer aborts. And note the split of concerns: *serializability* is about
the final effect; *recoverability* is about commit ordering. A schedule can
be perfectly serializable yet unrecoverable — correctness needs both.
""",
        3,
    ),
    _mkl(
        "dbms-m4-l4", _M4, "conflict-serializability", "Conflict Serializability",
        """## Conflicts and the precedence graph

Serializability is usually tested through **conflict serializability** — a
practical condition a DBMS can actually check.

Two operations **conflict** if they belong to *different* transactions,
touch the *same* data item, and **at least one is a write**. So read–write,
write–read, and write–write pairs conflict; **read–read never conflicts**
because order is irrelevant.

Build the **precedence graph**: one node per transaction, and an edge
Ti → Tj whenever an operation of Ti conflicts with a *later* operation of
Tj. The schedule is conflict-serializable **iff the graph has no cycle**.
A topological order of an acyclic graph gives an equivalent serial schedule.

## Worked example 1 (not serializable)

Schedule: `R1(A), W2(A), R2(B), W1(B)`

- R1(A) before W2(A): read–write conflict → edge **T1 → T2**.
- R2(B) before W1(B): read–write conflict → edge **T2 → T1**.

Cycle T1 ↔ T2 → **not conflict-serializable**. No serial order reproduces
both conflicts, so the interleaving is genuinely unsafe.

## Worked example 2 (serializable)

Schedule: `R1(A), W1(A), R2(A), W2(A)`

- Only conflict: W1(A) before R2(A) → edge **T1 → T2**. (R1(A) vs R2(A) is
  read–read — no edge; W1(A) vs W2(A) never occur adjacently across
  transactions in conflicting order... check: W1(A) before W2(A) is a
  write–write conflict → edge T1 → T2 as well.)

Still a single direction, no cycle → **conflict-serializable**, equivalent
to serial order T1 then T2. Intuition: any schedule can be transformed into
that serial order by repeatedly swapping *adjacent non-conflicting*
operations — and swapping non-conflicting operations never changes the
outcome.

## Limits

The graph ignores commits, aborts, and values — only the *order of
conflicting operations*. Hence conflict-serializability does **not** imply
recoverability; commit ordering needs a separate check. It is also
sufficient but not necessary for serializability — the next lesson shows a
serializable schedule no precedence graph can certify.
""",
        4,
    ),
    _mkl(
        "dbms-m4-l5", _M4, "view-serializability", "View Serializability",
        """## The exact condition

Conflict-serializability is sufficient but not necessary. **View
serializability** is the exact condition — harder to test, but it certifies
schedules the precedence graph rejects.

Two schedules are **view-equivalent** when:

1. Every read reads its value from the **same writer** in both schedules
   (a read with no preceding write reads the initial database value), and
2. The **final write** of every data item is performed by the **same
   transaction** in both.

A schedule is view-serializable if it is view-equivalent to *some* serial
schedule. Notice: this cares about *which values are actually observed*,
not about every conflicting pair.

## Blind writes — the source of the gap

A **blind write** writes an item the transaction never read
(e.g. `W2(A)` with no preceding `R2(A)` in T2). Blind writes create *fake*
conflicts: two writes conflict in the graph even when no transaction ever
observes their order.

## Worked example (view-serializable, NOT conflict-serializable)

Schedule: `R1(A), W2(A), R3(A), W1(A), W3(A)`

Precedence graph: R1(A)→W2(A) gives T1→T2; W2(A)→W1(A) gives T2→T1 —
a cycle → **not conflict-serializable**.

But compare against serial T1 → T2 → T3:

- R1(A) reads the *initial* value (nothing written before it) — same as
  serial. R3(A) reads the value written by W2(A), the latest writer before
  it — same as serial. Condition 1 holds.
- The final write of A is W3(A) by T3 in both — condition 2 holds.

So the schedule **is view-equivalent to T1;T2;T3** → view-serializable!
The cycle came from the blind write W2(A), which no read ever observed.

## The interview theorem

**Without blind writes, view-serializability implies
conflict-serializability.** Blind writes are the *only* source of the
difference between the two notions.
""",
        5,
    ),
    _mkl(
        "dbms-m4-l6", _M4, "locks-and-2pl", "Lock-Based Protocols & 2PL",
        """## Shared vs exclusive locks

The practical route to serializability is **locking**: a transaction must
hold a lock on an item before touching it. Two modes:

- **Shared (S)** — for reads. Many transactions may hold S on the same item
  simultaneously.
- **Exclusive (X)** — for writes. Nothing else coexists with it.

Compatibility matrix: S–S is compatible; **everything else conflicts**. If
T1 holds S(R) and T2 requests X(R), T2 **waits** until T1 releases.

## Two-phase locking

Raw locking still permits non-serializable schedules, so we add discipline:
**two-phase locking (2PL)**. Phase 1 (**growing**): the transaction may
*acquire* locks but release none. Phase 2 (**shrinking**): it may *release*
locks but acquire none. The instant between the phases — when the
transaction holds *every* lock it will ever need — is its **lock point**.

Why it works (proof sketch): order transactions by lock point. Take any two
*conflicting* operations from Ti and Tj. The later operation's transaction
could only acquire its lock after the earlier one released its conflicting
lock — i.e., after the earlier transaction's lock point... more precisely,
conflicting operations are always ordered the same way as their
transactions' lock points. So the execution is conflict-equivalent to the
serial schedule of lock-point order. **2PL guarantees
conflict-serializability.**

## Stricter flavors

- **Strict 2PL**: holds all *exclusive* locks until commit/abort. Nobody can
  read or overwrite uncommitted writes → schedules are cascadeless and
  recoverable. This is what most real systems use.
- **Rigorous 2PL**: holds *all* locks until commit → produces strict
  schedules.

The price of 2PL: **deadlocks** — T1 waits for T2's lock while T2 waits for
T1's. 2PL prevents non-serializability, not deadlocks. That is the next
lesson.
""",
        6,
    ),
    _mkl(
        "dbms-m4-l7", _M4, "deadlocks-timestamps-mvcc",
        "Deadlocks, Timestamps & MVCC",
        """## Deadlocks

2PL's flaw: **deadlock** — transactions waiting on each other's locks in a
cycle (T1 holds X(A) wants X(B); T2 holds X(B) wants X(A)). Unlike OS
deadlocks over fixed resources, the DBMS builds a **wait-for graph** and
*detects* cycles, then breaks them by aborting a **victim** (usually the
transaction with the least work invested).

**Prevention** schemes use timestamps (older = smaller timestamp = higher
priority), ensuring waits only ever go one direction in time:

- **Wait-die**: older requests a lock held by younger → older *waits*;
  younger requests one held by older → younger *dies* (aborts, restarts with
  the same timestamp). Old waits, young dies.
- **Wound-wait**: the mirror — older *wounds* (preempts/aborts) the younger
  holder; younger waits for older. Both are deadlock-free by construction.

## Timestamp ordering (no locks at all)

Assign each transaction a timestamp; abort any operation that arrives "too
late": a read of an item already written by a *younger* transaction, or a
write to an item already read/written by a younger one. Late = the
serialization order is already decided against you.

The **Thomas write rule** softens this for one case: if an *older*
transaction's write arrives *after* a younger transaction already wrote the
item, the write is simply **skipped** — it is obsolete anyway — instead of
aborting the transaction. (Sensible only for blind writes: nobody read the
value being skipped.)

## MVCC — versions instead of locks

**Multi-version concurrency control** never overwrites in place: each write
creates a **new version** stamped with the writer's timestamp, and each
reader sees the version that was current when *it* started. The headline
result: **readers never block writers, and writers never block readers** —
the reason PostgreSQL and InnoDB survive heavy mixed workloads. The cost is
storing old versions and cleaning them up (vacuuming) once no reader needs
them.
""",
        7,
    ),
]

QUESTIONS_M4 = [
    # ---- L1: ACID ----
    _mkq("dbms-m4-l1-q1", "dbms-m4-l1", _M4_SLUG, 4,
         "A database transaction is best described as:",
         ["Any single SQL statement executed by the DBMS",
          "A single logical unit of work whose operations are all-or-nothing",
          "A backup copy of the database taken before updates",
          "A lock held on a table during a long query"],
         1,
         "A transaction groups operations into one logical unit: either all of them take effect or none do. A single SQL statement may be part of a larger transaction, and transactions are about atomic execution, not backups or locks.",
         ("tcs", "infosys")),
    _mkq("dbms-m4-l1-q2", "dbms-m4-l1", _M4_SLUG, 5,
         "During a bank transfer, the system crashes after debiting account A but before crediting account B. On restart, the DBMS rolls back the debit. Which ACID property does this demonstrate?",
         ["Consistency", "Isolation", "Atomicity", "Durability"],
         2,
         "Rolling back a partially executed transaction so that none of its effects survive is atomicity — the all-or-nothing guarantee. Durability would apply only after commit; consistency is about valid states; isolation is about concurrency.",
         ("tcs", "wipro")),
    _mkq("dbms-m4-l1-q3", "dbms-m4-l1", _M4_SLUG, 6,
         "A transfer commits successfully. An hour later the power fails, but the transfer is still recorded when the system comes back. Which ACID property is this?",
         ["Atomicity", "Consistency", "Isolation", "Durability"],
         3,
         "Durability means committed effects survive any subsequent failure. The commit already happened, so atomicity's job is done; the guarantee that the committed data persists through the power failure is durability, delivered via write-ahead logging.",
         ("infosys", "accenture")),
    _mkq("dbms-m4-l1-q4", "dbms-m4-l1", _M4_SLUG, 7,
         "Two transfers on the same accounts run concurrently, and the final balances are exactly as if the transfers had run one after another. Which ACID property guarantees this?",
         ["Atomicity", "Consistency", "Isolation", "Durability"],
         2,
         "Isolation ensures concurrent transactions do not interfere — the outcome equals some serial execution. Atomicity covers crash-recovery of one transaction, durability covers post-commit survival, and consistency covers validity of states.",
         ("amazon", "tcs")),
    _mkq("dbms-m4-l1-q5", "dbms-m4-l1", _M4_SLUG, 8,
         "A buggy transfer debits account A twice but credits account B once, so the total money in the bank changes. Assuming the transaction committed, which ACID property was violated?",
         ["Atomicity", "Consistency", "Isolation", "Durability"],
         1,
         "Consistency requires each transaction to take the database from one valid state to another, preserving invariants like 'total money is conserved'. The transaction executed atomically and durably, but its logic broke a business invariant — a consistency violation the application (not just the DBMS) is responsible for.",
         ("microsoft", "amazon")),
    _mkq("dbms-m4-l1-q6", "dbms-m4-l1", _M4_SLUG, 9,
         "Which mechanism does the DBMS primarily use to guarantee durability?",
         ["Two-phase locking", "Write-ahead logging (log forced to stable storage before commit is acknowledged)", "Deadlock detection via wait-for graphs", "Query result caching"],
         1,
         "Write-ahead logging forces the commit record to stable storage before the commit is acknowledged, so recovery can redo committed work after any crash. Two-phase locking provides isolation/serializability, deadlock detection handles lock cycles, and caching is a performance feature — none of them make commits survive crashes.",
         ("google", "microsoft")),

    # ---- L2: Transaction States ----
    _mkq("dbms-m4-l2-q1", "dbms-m4-l2", _M4_SLUG, 4,
         "Which is the correct order of transaction states on the success path?",
         ["active → aborted → committed",
          "active → partially committed → committed",
          "active → failed → committed",
          "active → committed → partially committed"],
         1,
         "The success path is active (executing) → partially committed (finished executing, commit not yet durable) → committed (commit record safely on disk). Failed/aborted belong to the failure path, and partially committed always precedes committed.",
         ("tcs",)),
    _mkq("dbms-m4-l2-q2", "dbms-m4-l2", _M4_SLUG, 5,
         "A transaction has executed its last statement, but the commit record is not yet on stable storage. What state is it in?",
         ["Active", "Committed", "Partially committed", "Aborted"],
         2,
         "Partially committed means execution is complete but durability of the commit is not yet assured — a crash at this point still leads to rollback. It becomes committed only once the commit record is safely on disk.",
         ("infosys",)),
    _mkq("dbms-m4-l2-q3", "dbms-m4-l2", _M4_SLUG, 6,
         "A transaction hits a constraint violation mid-execution. After the DBMS rolls back all its changes, what state is it in?",
         ["Failed", "Aborted", "Partially committed", "Terminated"],
         1,
         "Failed means something went wrong; aborted means the failure was handled — changes rolled back, as if the transaction never ran. The rollback completing is what moves it from failed to aborted.",
         ("wipro",)),
    _mkq("dbms-m4-l2-q4", "dbms-m4-l2", _M4_SLUG, 7,
         "What is the golden rule of write-ahead logging?",
         ["Data pages are written before the log record",
          "The log record is forced to stable storage before the data page is written",
          "Checkpoints are taken before every commit",
          "Aborted transactions are never logged"],
         1,
         "WAL's golden rule is log-before-data: the record describing a change must be on stable storage before the changed page itself. That ordering is exactly what lets recovery redo committed work and undo the rest after a crash.",
         ("amazon",)),
    _mkq("dbms-m4-l2-q5", "dbms-m4-l2", _M4_SLUG, 8,
         "Why can a crash while a transaction is 'partially committed' still be rolled back safely?",
         ["Because partially committed transactions hold no locks",
          "Because the commit record never reached stable storage, so recovery treats it as uncommitted and undoes it using the log",
          "Because checkpoints prevent partial commits",
          "Because the buffer manager discards dirty pages automatically"],
         1,
         "Commitment is defined by the commit record reaching stable storage. Without it, recovery (via the WAL log) classifies the transaction as uncommitted and undoes its changes. Checkpoints only bound recovery time; they don't decide commit status.",
         ("microsoft",)),
    _mkq("dbms-m4-l2-q6", "dbms-m4-l2", _M4_SLUG, 9,
         "What is the primary purpose of a checkpoint?",
         ["To commit all active transactions immediately",
          "To flush dirty pages to disk and record a log position, bounding recovery time after a crash",
          "To delete the system log and start a fresh one",
          "To upgrade shared locks to exclusive locks"],
         1,
         "A checkpoint flushes dirty pages and marks the log position, so crash recovery replays only the log tail after the checkpoint instead of from the beginning of time. It does not commit transactions, delete the log, or touch locks.",
         ("google",)),

    # ---- L3: Schedules ----
    _mkq("dbms-m4-l3-q1", "dbms-m4-l3", _M4_SLUG, 4,
         "In concurrency control, a 'schedule' is:",
         ["The timetable for taking database backups",
          "An interleaved order of operations from concurrently executing transactions",
          "The priority order in which transactions acquire locks",
          "A plan for partitioning tables across disks"],
         1,
         "A schedule is the actual interleaving of reads/writes from concurrent transactions — the object whose correctness (serializability, recoverability) the theory analyzes. It has nothing to do with backups, lock priorities, or partitioning.",
         ("tcs",)),
    _mkq("dbms-m4-l3-q2", "dbms-m4-l3", _M4_SLUG, 5,
         "T1 and T2 both read balance = 100, both add 50, and both write back 150 instead of the correct 200. This phenomenon is called:",
         ["A dirty read", "A lost update", "A phantom read", "Cascading rollback"],
         1,
         "A lost update: two transactions read the same value, both modify it, and the second write silently overwrites the first — one update is lost. A dirty read involves reading uncommitted data; phantoms involve new rows appearing; cascading rollback involves aborts propagating.",
         ("infosys",)),
    _mkq("dbms-m4-l3-q3", "dbms-m4-l3", _M4_SLUG, 6,
         "A 'dirty read' occurs when:",
         ["A transaction reads data written by another transaction that has not yet committed",
          "Two transactions write the same item simultaneously",
          "A transaction reads a row twice and gets different values",
          "A committed transaction's writes are lost after a crash"],
         0,
         "A dirty read is reading uncommitted data — if the writer later aborts, the reader acted on data that never officially existed. Reading the same row twice with different results is a non-repeatable read; simultaneous writes are a write-write conflict.",
         ("wipro", "tcs")),
    _mkq("dbms-m4-l3-q4", "dbms-m4-l3", _M4_SLUG, 7,
         "Consider the schedule: W1(A), R2(A), C1, C2. Which property holds?",
         ["Recoverable only",
          "Cascadeless (but not strict)",
          "Strict",
          "None of recoverable, cascadeless, or strict"],
         0,
         "T2 reads A's uncommitted write, so the schedule is not cascadeless (and hence not strict). But T2 commits (C2) after T1 commits (C1), satisfying recoverability: no transaction commits based on data from a transaction that commits later. So it is recoverable only.",
         ("amazon",)),
    _mkq("dbms-m4-l3-q5", "dbms-m4-l3", _M4_SLUG, 8,
         "Consider the schedule: W1(A), R2(A), C2, C1. Which is true?",
         ["It is recoverable but not cascadeless",
          "It is cascadeless but not recoverable",
          "It is strict",
          "It is not even recoverable"],
         3,
         "T2 reads T1's uncommitted write and commits (C2) before T1 commits (C1) — so T2 commits based on data whose writer hasn't committed: not recoverable. Since recoverability is the weakest of the three, none of them hold.",
         ("microsoft",)),
    _mkq("dbms-m4-l3-q6", "dbms-m4-l3", _M4_SLUG, 9,
         "A schedule is conflict-serializable, but one transaction reads another's write and commits first. For full correctness the DBMS must additionally enforce:",
         ["Deadlock freedom", "Recoverability", "View serializability", "Strict two-phase locking"],
         1,
         "Conflict-serializability only constrains the order of conflicting operations — it says nothing about commit ordering. The schedule described is unrecoverable (a committer depending on an uncommitted writer), so recoverability must be enforced separately, e.g. via strict 2PL's lock retention.",
         ("google",)),

    # ---- L4: Conflict Serializability ----
    _mkq("dbms-m4-l4-q1", "dbms-m4-l4", _M4_SLUG, 4,
         "Two operations from different transactions on the same data item conflict when:",
         ["Both are reads",
          "At least one of them is a write",
          "Both are writes and nothing else",
          "They occur in the same transaction"],
         1,
         "Conflict needs: different transactions, same item, at least one write. That covers read-write, write-read, and write-write pairs. Read-read pairs never conflict since their order doesn't affect the outcome.",
         ("tcs", "infosys")),
    _mkq("dbms-m4-l4-q2", "dbms-m4-l4", _M4_SLUG, 5,
         "Schedule: R1(A), W2(A), R2(B), W1(B). What does the precedence graph contain?",
         ["A single edge T1 → T2",
          "A single edge T2 → T1",
          "Edges T1 → T2 and T2 → T1 (a cycle)",
          "No edges at all"],
         2,
         "R1(A) before W2(A) is a read-write conflict → edge T1→T2. R2(B) before W1(B) is a read-write conflict → edge T2→T1. The two edges form a cycle, so the schedule is not conflict-serializable.",
         ("tcs",)),
    _mkq("dbms-m4-l4-q3", "dbms-m4-l4", _M4_SLUG, 6,
         "Schedule: R1(A), W1(A), R2(A), W2(A). Is it conflict-serializable, and to which serial order is it equivalent?",
         ["Not conflict-serializable (cycle T1 ↔ T2)",
          "Conflict-serializable, equivalent to T2 then T1",
          "Conflict-serializable, equivalent to T1 then T2",
          "Conflict-serializable, equivalent to either order"],
         2,
         "Conflicts: W1(A) before R2(A) → T1→T2, and W1(A) before W2(A) → T1→T2. (R1(A) vs R2(A) is read-read: no edge.) All edges point one way, so the graph is acyclic and the schedule is equivalent to serial order T1 followed by T2.",
         ("wipro", "accenture")),
    _mkq("dbms-m4-l4-q4", "dbms-m4-l4", _M4_SLUG, 7,
         "Schedule: R1(X), R2(X), W3(X), W1(Y), W2(Y), W3(Y). Which is true?",
         ["Not conflict-serializable — cycle T1 → T3 → T1",
          "Conflict-serializable, equivalent to serial order T1 → T2 → T3",
          "Conflict-serializable, equivalent to serial order T3 → T2 → T1",
          "Not conflict-serializable — cycle T2 → T3 → T2"],
         1,
         "On X: R1(X)→W3(X) gives T1→T3; R2(X)→W3(X) gives T2→T3. On Y: W1(Y)→W2(Y) gives T1→T2; W1(Y)→W3(Y) gives T1→T3; W2(Y)→W3(Y) gives T2→T3. Every edge flows forward through T1→T2→T3 — acyclic — so the schedule is conflict-serializable and equivalent to T1, T2, T3 in that order.",
         ("amazon",)),
    _mkq("dbms-m4-l4-q5", "dbms-m4-l4", _M4_SLUG, 8,
         "Every conflict-serializable schedule is also:",
         ["Recoverable", "Cascadeless", "Serializable", "Deadlock-free"],
         2,
         "Conflict-serializability implies serializability by construction (the schedule is conflict-equivalent to the topological serial order). But it implies nothing about commit ordering: e.g. W1(A), R2(A), C2, C1 is conflict-serializable yet not recoverable. And serializability says nothing about deadlocks.",
         ("microsoft",)),
    _mkq("dbms-m4-l4-q6", "dbms-m4-l4", _M4_SLUG, 9,
         "Schedule: W1(A), R2(A), W2(B), R3(B), W3(A), R1(B). Is it conflict-serializable?",
         ["Yes, equivalent to T1 → T2 → T3",
          "Yes, equivalent to T2 → T1 → T3",
          "No — the precedence graph has a cycle T1 ↔ T2",
          "No — the precedence graph has a cycle T1 → T3 → T1"],
         2,
         "On A: W1(A)→R2(A) gives T1→T2; W1(A)→W3(A) gives T1→T3; R2(A)→W3(A) gives T2→T3. On B: W2(B)→R3(B) gives T2→T3; W2(B)→R1(B) gives T2→T1. Edges T1→T2 and T2→T1 form a cycle, so the schedule is not conflict-serializable.",
         ("google", "amazon")),

    # ---- L5: View Serializability ----
    _mkq("dbms-m4-l5-q1", "dbms-m4-l5", _M4_SLUG, 4,
         "Two schedules are view-equivalent when:",
         ["They contain exactly the same operations in the same order",
          "Every read reads from the same writer, and the final write of each item is by the same transaction",
          "Their precedence graphs are identical",
          "They use the same lock modes on every item"],
         1,
         "View-equivalence is about observed values, not operation order: (1) each read must see the value from the same writer (or the initial value), and (2) each item's last write must come from the same transaction. Same operations or same locks are not required.",
         ("tcs",)),
    _mkq("dbms-m4-l5-q2", "dbms-m4-l5", _M4_SLUG, 5,
         "Transaction T2 executes: W2(A), R2(B), W2(B). Which operation is a blind write?",
         ["W2(A), because T2 never reads A before writing it",
          "R2(B), because it reads before writing",
          "W2(B), because it follows R2(B)",
          "None — blind writes require three operations"],
         0,
         "A blind write writes an item the transaction never read. W2(A) has no preceding R2(A), so it is blind. W2(B) is not blind because T2 read B first via R2(B).",
         ("infosys",)),
    _mkq("dbms-m4-l5-q3", "dbms-m4-l5", _M4_SLUG, 6,
         "A schedule is view-serializable but NOT conflict-serializable. What must it necessarily contain?",
         ["At least one deadlock", "At least one blind write", "At least one dirty read", "At least four transactions"],
         1,
         "Blind writes are the only source of the gap: without blind writes, view-serializability implies conflict-serializability. A blind write creates graph conflicts no read ever observes, allowing a cycle in the precedence graph alongside view-equivalence to a serial schedule.",
         ("wipro", "accenture")),
    _mkq("dbms-m4-l5-q4", "dbms-m4-l5", _M4_SLUG, 7,
         "Schedule: R1(A), W2(A), R3(A), W1(A), W3(A). Is it conflict-serializable?",
         ["Yes, equivalent to T1 → T2 → T3",
          "Yes, equivalent to T2 → T3 → T1",
          "No — the precedence graph has a cycle T1 ↔ T2",
          "No — the precedence graph has a cycle T2 ↔ T3"],
         2,
         "R1(A) before W2(A) gives edge T1→T2 (read-write conflict), and W2(A) before W1(A) gives edge T2→T1 (write-write conflict). The cycle T1↔T2 means the schedule is not conflict-serializable.",
         ("amazon",)),
    _mkq("dbms-m4-l5-q5", "dbms-m4-l5", _M4_SLUG, 8,
         "For the schedule R1(A), W2(A), R3(A), W1(A), W3(A): is it view-serializable?",
         ["No — no serial schedule matches its reads",
          "Yes — it is view-equivalent to serial T2 → T1 → T3",
          "Yes — it is view-equivalent to serial T1 → T2 → T3",
          "Yes — it is view-equivalent to serial T3 → T2 → T1"],
         2,
         "Check against serial T1;T2;T3. Reads: R1(A) sees the initial value in both (nothing written before it); R3(A) sees W2(A)'s value in both (latest writer before the read). Final write of A is W3(A) by T3 in both. Both view-equivalence conditions hold, so it is view-serializable despite the conflict-graph cycle (caused by the blind write W2(A)).",
         ("microsoft",)),
    _mkq("dbms-m4-l5-q6", "dbms-m4-l5", _M4_SLUG, 9,
         "If a schedule contains NO blind writes and is view-serializable, then it is also:",
         ["Recoverable", "Conflict-serializable", "Strict", "Deadlock-free"],
         1,
         "This is the key theorem: blind writes are the only thing that lets a schedule be view-serializable without being conflict-serializable. With no blind writes, view-equivalence to a serial schedule forces an acyclic precedence graph. Recoverability and strictness are separate commit-ordering properties.",
         ("google",)),

    # ---- L6: Locks & 2PL ----
    _mkq("dbms-m4-l6-q1", "dbms-m4-l6", _M4_SLUG, 4,
         "T1 holds a shared (S) lock on row R. Which incoming request can be granted immediately?",
         ["T2 requests an exclusive (X) lock on R",
          "T2 requests a shared (S) lock on R",
          "T3 requests an exclusive (X) lock on a different row",
          "No request can ever be granted while T1 holds S(R)"],
         1,
         "Shared locks are compatible with other shared locks (S–S), so concurrent readers coexist. Any exclusive request conflicts with the held shared lock and must wait. (An X lock on a different row is unrelated to R and would be granted, but the question asks about row R.)",
         ("tcs",)),
    _mkq("dbms-m4-l6-q2", "dbms-m4-l6", _M4_SLUG, 5,
         "In two-phase locking, the two phases are:",
         ["Locking and unlocking, in any interleaved order",
          "Growing (may acquire, may not release) and shrinking (may release, may not acquire)",
          "Reading and writing",
          "Waiting and wounding"],
         1,
         "Phase 1 (growing): the transaction may acquire locks but must not release any. Phase 2 (shrinking): it may release locks but must not acquire any. Once it releases its first lock, no new lock may be taken — that discipline is what guarantees serializability.",
         ("infosys",)),
    _mkq("dbms-m4-l6-q3", "dbms-m4-l6", _M4_SLUG, 6,
         "T1 holds X(A) and requests X(B); T2 holds X(B) and requests X(A). Both wait forever. This is:",
         ["Livelock", "Starvation", "A deadlock", "A phantom read"],
         2,
         "Each transaction waits for a lock held by the other — a wait-for cycle, i.e. a deadlock. Livelock is active retrying without progress; starvation is indefinite postponement; a phantom read is about newly appearing rows.",
         ("wipro", "tcs")),
    _mkq("dbms-m4-l6-q4", "dbms-m4-l6", _M4_SLUG, 7,
         "How does strict 2PL differ from basic 2PL, and what does it buy?",
         ["It holds shared locks till commit; it prevents phantoms",
          "It holds all exclusive locks until commit/abort; schedules become cascadeless and recoverable",
          "It releases locks eagerly; it improves concurrency",
          "It uses timestamps instead of locks; it prevents deadlocks"],
         1,
         "Strict 2PL keeps every X lock until commit/abort, so no transaction can read or overwrite uncommitted writes — that makes schedules cascadeless (no cascading aborts) and recoverable. Rigorous 2PL goes further, holding all locks till commit for strict schedules.",
         ("amazon",)),
    _mkq("dbms-m4-l6-q5", "dbms-m4-l6", _M4_SLUG, 8,
         "Why does following 2PL guarantee conflict-serializability?",
         ["Because locks make transactions run one at a time",
          "Because conflicting operations end up ordered the same way as their transactions' lock points, giving a conflict-equivalent serial order",
          "Because deadlocks are impossible under 2PL",
          "Because 2PL forces all reads to happen before all writes"],
         1,
         "The lock-point argument: the later of two conflicting operations could only acquire its lock after the earlier released its conflicting lock, so conflicts are ordered consistently with lock-point order. The serial schedule in lock-point order is therefore conflict-equivalent to the execution. 2PL does not serialize execution, does not prevent deadlocks, and imposes no read-before-write rule.",
         ("microsoft",)),
    _mkq("dbms-m4-l6-q6", "dbms-m4-l6", _M4_SLUG, 9,
         "Which lock sequence by T1 violates two-phase locking?",
         ["lock-S(A), lock-X(B), unlock(A), unlock(B)",
          "lock-X(A), lock-X(B), unlock(B), unlock(A)",
          "lock-S(A), lock-X(B), unlock(A), lock-S(C)",
          "lock-S(A), unlock(A)"],
         2,
         "Acquiring lock-S(C) after unlock(A) released a lock violates the shrinking phase — once a transaction starts releasing, it may never acquire again. The other sequences acquire everything before releasing anything, which is valid 2PL.",
         ("google",)),

    # ---- L7: Deadlocks, Timestamps, MVCC ----
    _mkq("dbms-m4-l7-q1", "dbms-m4-l7", _M4_SLUG, 4,
         "How does a DBMS typically handle a lock deadlock?",
         ["It restarts the entire database server",
          "It detects the wait-for cycle and aborts a victim transaction, rolling it back",
          "It upgrades all shared locks to exclusive locks",
          "It ignores it — deadlocks resolve themselves over time"],
         1,
         "The DBMS maintains a wait-for graph, detects cycles, and breaks them by choosing a victim (usually the transaction with least invested work) and aborting it. Restarting the server or upgrading locks would not break the cycle; deadlocks never resolve on their own.",
         ("tcs",)),
    _mkq("dbms-m4-l7-q2", "dbms-m4-l7", _M4_SLUG, 5,
         "Under the wait-die scheme, an OLDER transaction T1 requests a lock held by a YOUNGER transaction T2. What happens?",
         ["T1 waits for T2",
          "T1 dies (aborts and restarts)",
          "T2 dies immediately",
          "Both abort"],
         0,
         "Wait-die: old waits, young dies. Since the requester T1 is older than the holder T2, T1 waits. (If the requester were younger, it would die instead.) The name is the mnemonic: the older transaction waits, the younger one dies.",
         ("infosys",)),
    _mkq("dbms-m4-l7-q3", "dbms-m4-l7", _M4_SLUG, 6,
         "Under the wound-wait scheme, an OLDER transaction T1 requests a lock held by a YOUNGER transaction T2. What happens?",
         ["T1 waits for T2",
          "T1 dies (aborts and restarts)",
          "T1 wounds T2 — T2 aborts and restarts, T1 gets the lock",
          "The lock is shared between them"],
         2,
         "Wound-wait is the mirror of wait-die: the older transaction preempts (wounds) the younger holder, which aborts and will restart. The younger transaction, had it been the requester, would have waited. Both schemes are deadlock-free because waits only go one way in timestamp order.",
         ("wipro",)),
    _mkq("dbms-m4-l7-q4", "dbms-m4-l7", _M4_SLUG, 7,
         "Under basic timestamp ordering, transaction T5 (older) tries to read item X after transaction T10 (younger) has already written X. What happens?",
         ["T5 reads the value and continues",
          "T5 aborts — the read arrived too late",
          "T10 aborts to let T5 read",
          "X is locked until T10 commits"],
         1,
         "Timestamp ordering enforces serialization in timestamp order. T5 reading after younger T10 wrote means T5's read is 'too late' — the serialization order is already decided against it — so T5 aborts (and restarts with a new timestamp). Timestamp ordering uses aborts, not locks.",
         ("amazon",)),
    _mkq("dbms-m4-l7-q5", "dbms-m4-l7", _M4_SLUG, 8,
         "Under timestamp ordering with the Thomas write rule, an OLDER transaction's write arrives after a YOUNGER transaction already wrote the same item. What happens?",
         ["The older transaction aborts",
          "The younger transaction aborts",
          "The obsolete write is skipped (ignored) and the transaction continues",
          "Both writes are applied in arrival order"],
         2,
         "The Thomas write rule: a late write from an older transaction is obsolete — no active transaction could have read a value it never wrote — so it is silently skipped instead of aborting the transaction. This is safe for blind writes and reduces unnecessary aborts.",
         ("microsoft",)),
    _mkq("dbms-m4-l7-q6", "dbms-m4-l7", _M4_SLUG, 9,
         "Under MVCC, a long-running read query executes while a concurrent transaction updates the same rows. What happens?",
         ["The reader blocks until the writer commits",
          "The writer blocks until the reader finishes",
          "The reader sees the older versions of the rows; neither blocks the other",
          "The reader sees a mix of old and new values"],
         2,
         "MVCC keeps multiple timestamped versions: the reader picks the version current when it started, so it sees a consistent snapshot while the writer creates new versions concurrently. Readers never block writers and writers never block readers — at the cost of storing old versions until no reader needs them.",
         ("google",)),
]


# ---------------------------------------------------------------------------
# MODULE 5 — INDEXING & OPTIMIZATION
# ---------------------------------------------------------------------------

_M5 = "dbms-m5"
_M5_SLUG = "indexing-optimization"

LESSONS_M5 = [
    _mkl(
        "dbms-m5-l1", _M5, "indexing-basics", "Indexing Basics",
        """## From full scan to index seek

Without an index, `WHERE email = 'a@x.com'` forces a **full table scan** —
read every row, test the condition. On 10 million rows, that is 10 million
checks. An **index** is a separate lookup structure mapping keys to row
locations, turning the scan into an **index seek**: jump straight to the
matching rows, typically in O(log n) page reads.

## Dense vs sparse

A **dense** index holds an entry for *every* key value. A **sparse** index
holds entries only for *some* values — e.g. one per data page — so it is
smaller, but locating a row takes an extra step of searching within the
page. Dense is faster per lookup; sparse is cheaper to store and maintain.

## The write-cost trade-off

Indexes are not free. Every INSERT, UPDATE, or DELETE on an indexed column
must update *each* index on the table. Five indexes make reads fly and
writes crawl — index design is a balancing act, not "more is better".

## When does an index NOT help?

**Selectivity**: the fraction of rows a predicate matches. An index on
`gender` (two values, ~50% each) rarely beats a full scan — the optimizer
will simply ignore it. Indexes shine on high-selectivity predicates: a few
matching rows out of millions.

Also, an index is usable only if the query can navigate it naturally.
`WHERE YEAR(dob) = 2000` usually *cannot* use an index on `dob`, because the
function wrapping the column defeats the lookup (such predicates are called
non-sargable). Prefer `WHERE dob >= '2000-01-01' AND dob < '2001-01-01'`.
""",
        1,
    ),
    _mkl(
        "dbms-m5-l2", _M5, "b-plus-trees", "B+ Trees",
        """## The workhorse index

The **B+ tree** is a balanced, multi-way search tree designed for disk:
each node is sized to one disk page, and with ~100 keys per node the tree
stays extremely shallow.

**Structure**: **internal nodes** store only *keys* — they are signposts
routing the search downward, holding no data. **All data lives in the leaf
level**: leaves hold keys plus pointers to the actual rows, and the leaves
are **linked together** left-to-right, so a range scan just walks the leaf
chain. (Contrast B-trees, which store data in internal nodes too — B+
trees keep internal nodes slimmer, so fanout is higher and the tree
shallower.)

**Order and fanout**: a B+ tree of order *n* gives internal nodes at most
*n* children (and *n*−1 keys), and at least ⌈n/2⌉ children (except the
root). Fanout = number of children per node.

## Worked height example

1,000,000 records, fanout 100, leaves packed full. The leaf level needs
1,000,000 / 100 = 10,000 leaf nodes. Their parents: 10,000 / 100 = 100
nodes. One root above them. Total: **3 levels** — root → internal → leaves.
Any lookup costs ~3 page reads. A binary tree over the same data needs ~20
levels → ~20 disk I/Os. That is why B+ trees beat binary trees on disk:
*fanout collapses height*, and height is what you pay for in disk seeks.

## Staying balanced

Deletions can **underflow** a node below minimum occupancy — the tree then
*borrows* a key from a sibling or **merges** with it, possibly shrinking the
height. Insertions that overflow a node **split** it, possibly growing the
tree. Through all of it the tree stays balanced: every leaf at the same
depth, always.
""",
        2,
    ),
    _mkl(
        "dbms-m5-l3", _M5, "clustered-vs-nonclustered",
        "Clustered vs Non-Clustered Indexes",
        """## Clustered: the table's physical order

A **clustered index** dictates the *physical order* of the table's rows on
disk — the table itself is stored sorted by the clustered key. Rows can only
be physically ordered one way, so a table gets **exactly one** clustered
index. In InnoDB/MySQL, the primary key *is* the clustered index; a table
with no primary key gets a hidden row-id cluster.

Because the clustered key defines where rows live, **choose it carefully**:
narrow, ever-increasing keys (auto-increment IDs) keep inserts appending at
the end; wide or random keys (UUIDs) cause page splits and fragmentation.

## Non-clustered: a separate structure

A **non-clustered (secondary) index** is a separate structure of sorted keys
plus a pointer (row locator) to each row. Lookup is two hops: find the key
in the index, then fetch the row. You can have many secondary indexes.

## Covering indexes

A **covering index** contains *every column the query needs*. An index on
`(dept, salary)` covers `SELECT salary FROM emp WHERE dept = 'X'` — the
engine answers from the index alone with **zero table lookups**, often the
single biggest easy win in query tuning. In Postgres EXPLAIN this appears
as an "Index Only Scan".

## Interview rules of thumb

One clustered index per table (usually the PK — narrow and monotonic);
secondary indexes on frequent filter and join columns; composite *covering*
indexes for your hottest queries. And remember the leftmost-prefix rule: an
index on `(last_name, first_name)` serves `WHERE last_name = ...` but not a
query filtering on `first_name` alone.
""",
        3,
    ),
    _mkl(
        "dbms-m5-l4", _M5, "hash-indexing", "Hash Indexing",
        """## O(1) equality lookups

A **hash index** feeds the key through a hash function h(key) → bucket
number, and stores entries in buckets. An equality lookup —
`WHERE id = 42` — is O(1) on average: hash, jump to the bucket, done. No
tree traversal at all.

## Static hashing and overflow

Collisions are inevitable: two keys landing in the same bucket. **Static
hashing** fixes the bucket count up front and handles overflow with
**chaining** — a full bucket links to **overflow buckets**. The flaw: as
data grows, chains lengthen and the "O(1)" quietly degrades toward a scan;
and the table cannot shrink when data is deleted. Static hashing works only
when you know the data size in advance.

## Extendible hashing

**Extendible hashing** adapts dynamically. A **directory** of 2^global_depth
pointers maps hash prefixes to buckets, and each bucket tracks its own
**local depth**. When a bucket overflows, it **splits** — and if its local
depth equals the global depth, the **directory doubles** first. Buckets
split and the directory grows (and shrinks) with the data; nothing is ever
fully rehashed.

## Hash vs B+ tree — the decisive comparison

**Hash indexes serve equality lookups; B+ trees serve equality *and* range
queries.** Hashing destroys order — `WHERE age BETWEEN 20 AND 30` or
`ORDER BY age` cannot use a hash index because adjacent keys scatter to
random buckets. That is why general-purpose databases default to B+ trees
and reserve hash structures for exact-match workloads.
""",
        4,
    ),
    _mkl(
        "dbms-m5-l5", _M5, "query-optimization", "Query Optimization",
        """## The cost-based optimizer

You write *what* you want in SQL; the **query optimizer** decides *how* —
which indexes to use, in which order to join, which algorithms to run. It is
**cost-based**: it estimates the cost (disk I/Os, CPU) of candidate plans
using table **statistics** — row counts, value distributions, histograms —
and picks the cheapest estimate.

## Selectivity drives the choice

The key estimate is **selectivity**: the fraction of rows a predicate
matches. `WHERE id = 42` has tiny selectivity — an index seek wins.
`WHERE status = 'active'` matching 60% of rows has poor selectivity — a
sequential scan beats millions of random index hops. When the optimizer
"ignores your index", poor selectivity is the first suspect.

## Reading EXPLAIN

EXPLAIN shows the chosen plan. Learn the verbs: **Seq Scan** = read the
whole table; **Index Scan** = walk the index, then fetch rows; **Index Only
Scan** = answer from the index alone (covering index); **Bitmap Heap Scan**
= combine several indexes. The cost numbers are the optimizer's *estimates*
in abstract units — good for comparing plans, not wall-clock predictions.
**EXPLAIN ANALYZE** actually *runs* the query and reports real row counts
and timings: the ground truth when estimates look suspicious.

## Stale statistics — the #1 real-world culprit

A bad plan usually means a bad *estimate*. After bulk loads or big deletes,
run **ANALYZE** (or let autovacuum do it) so cardinality estimates match
reality. An optimizer picking a nested-loop join for a million-row join
almost always means it *thought* the input was small.
""",
        5,
    ),
    _mkl(
        "dbms-m5-l6", _M5, "join-algorithms", "Join Algorithms",
        """## Where queries live or die

Joins dominate query cost. Four algorithms to know:

**Nested-loop join**: for each row of the outer table, scan the inner table
for matches. Cost ≈ |outer| × |inner| — brutal, *unless* the outer table
is tiny or the inner table has an **index on the join key** (then it is an
*indexed* nested loop, and excellent).

**Block nested-loop**: the refinement — load a *block* of outer rows into
memory at once, then scan the inner table once per block instead of once
per row. Fewer inner scans by a factor of the block size.

**Sort-merge join**: sort both inputs on the join key (skipping the sort if
already ordered), then merge in one linear pass like a zipper. Shines when
inputs are *already sorted* (e.g. via an index) or the result must come out
sorted — then the sort is free. Also handles non-equi conditions.

**Hash join**: the heavyweight champion for large equi-joins. **Build** a
hash table on the *smaller* relation, then **probe** it with each row of
the larger. Usually the fastest for big unsorted equi-joins with enough
memory — but it works **only for equality** conditions; `ON a.x > b.y`
cannot be hashed.

## Choosing — interview heuristics

Tiny outer table or indexed inner → nested loop. Already-sorted inputs or
sorted output required → sort-merge. Large unsorted equi-join → hash join.
Non-equi condition → sort-merge or nested loop (never hash).

Watch for the optimizer's mistake patterns: a hash join spilling to disk
(work memory exceeded) or a nested loop chosen on a bad row estimate — both
usually trace back to stale statistics or a query worth rewriting.
""",
        6,
    ),
]

QUESTIONS_M5 = [
    # ---- L1: Indexing Basics ----
    _mkq("dbms-m5-l1-q1", "dbms-m5-l1", _M5_SLUG, 4,
         "What is the difference between a full table scan and an index seek?",
         ["A full scan reads every row; an index seek jumps directly to matching rows via a lookup structure",
          "A full scan uses an index; an index seek reads every row",
          "They are two names for the same operation",
          "A full scan is always faster because it avoids index overhead"],
         0,
         "A full table scan checks every row, while an index seek navigates a lookup structure (key → row location) to reach only matching rows — typically O(log n) page reads instead of O(n). Scans win only when most rows match anyway.",
         ("tcs",)),
    _mkq("dbms-m5-l1-q2", "dbms-m5-l1", _M5_SLUG, 5,
         "What is the difference between a dense index and a sparse index?",
         ["Dense indexes are for numbers, sparse indexes are for text",
          "A dense index has an entry for every key value; a sparse index has entries only for some values",
          "A dense index is always clustered; a sparse index is always non-clustered",
          "Dense indexes cannot be updated; sparse indexes can"],
         1,
         "Dense = one entry per key value (faster lookups, larger). Sparse = entries only for some values, e.g. one per data page (smaller, but needs an extra step to find the row within the page).",
         ("infosys",)),
    _mkq("dbms-m5-l1-q3", "dbms-m5-l1", _M5_SLUG, 6,
         "A table has 6 indexes and INSERTs have become very slow, while SELECTs are fast. What is the most likely explanation?",
         ["The indexes are corrupted",
          "Every INSERT must update all 6 indexes, multiplying write cost",
          "SELECTs are locking the table during INSERTs",
          "The buffer pool is too small for 6 indexes"],
         1,
         "Indexes are maintained on writes: each INSERT/UPDATE/DELETE on an indexed column updates every affected index. Six indexes mean roughly six times the index-maintenance work per write — the classic read-vs-write trade-off of indexing.",
         ("wipro",)),
    _mkq("dbms-m5-l1-q4", "dbms-m5-l1", _M5_SLUG, 7,
         "Which column is the WORST candidate for an index?",
         ["email (unique per user)", "phone_number (nearly unique)", "gender (2 possible values)", "aadhaar_number (unique)"],
         2,
         "An index on a 2-valued column has terrible selectivity — a query matching one gender still reads ~50% of the table, so the optimizer will prefer a full scan anyway. Indexes pay off on high-selectivity (near-unique) columns like email or aadhaar_number.",
         ("accenture", "tcs")),
    _mkq("dbms-m5-l1-q5", "dbms-m5-l1", _M5_SLUG, 8,
         "The query WHERE YEAR(created_at) = 2024 cannot use the index on created_at. Why?",
         ["Indexes only work with string columns",
          "Wrapping the column in a function prevents the index lookup (the predicate is non-sargable)",
          "YEAR() is not a valid SQL function",
          "Indexes never help with date columns"],
         1,
         "An index is navigated by comparing raw key values; wrapping the column in YEAR() hides the key from the lookup, so the engine must compute the function per row. Rewrite as a range on the bare column: created_at >= '2024-01-01' AND created_at < '2025-01-01'.",
         ("amazon",)),
    _mkq("dbms-m5-l1-q6", "dbms-m5-l1", _M5_SLUG, 9,
         "A query on a 10M-row table filters on an indexed column, matches 40% of rows, and the optimizer chooses a sequential scan. Best explanation?",
         ["The optimizer has a bug",
          "The index is corrupted",
          "Poor selectivity: fetching 40% of rows via random index lookups costs more than one sequential pass",
          "The query is missing a LIMIT clause"],
         2,
         "With 40% selectivity, an index plan would do ~4M random page hops — far costlier than one sequential read of the table. The cost-based optimizer correctly judges the seq scan cheaper. This is normal behavior, not a bug or corruption.",
         ("microsoft", "google")),

    # ---- L2: B+ Trees ----
    _mkq("dbms-m5-l2-q1", "dbms-m5-l2", _M5_SLUG, 4,
         "In a B+ tree, what is the difference between internal nodes and leaf nodes?",
         ["Internal nodes hold data rows; leaves hold only keys",
          "Internal nodes hold only keys for routing; leaves hold keys plus data pointers and are linked together",
          "There is no difference — every node is identical",
          "Internal nodes are on disk; leaf nodes are in memory"],
         1,
         "Internal nodes are pure signposts (keys only), keeping fanout high. All data pointers live in the leaves, which are linked left-to-right so range scans walk the leaf chain without revisiting internal nodes.",
         ("tcs",)),
    _mkq("dbms-m5-l2-q2", "dbms-m5-l2", _M5_SLUG, 5,
         "In a B+ tree of order 6, what are the maximum children and maximum keys of an internal node?",
         ["6 children, 6 keys", "6 children, 5 keys", "5 children, 6 keys", "12 children, 11 keys"],
         1,
         "Order n means at most n children per internal node, and keys = children − 1, so 6 children and 5 keys max. (Minimum for non-root nodes is ⌈n/2⌉ children.)",
         ("infosys",)),
    _mkq("dbms-m5-l2-q3", "dbms-m5-l2", _M5_SLUG, 6,
         "A B+ tree has fanout 100 and stores 1,000,000 records with full leaves. How many levels (root to leaf) does the tree have?",
         ["2", "3", "4", "20"],
         1,
         "Leaf level: 1,000,000 / 100 = 10,000 leaf nodes. Their parents: 10,000 / 100 = 100 nodes. One root above them. That's 3 levels total, so any lookup costs ~3 page reads — versus ~20 for a binary tree.",
         ("wipro", "accenture")),
    _mkq("dbms-m5-l2-q4", "dbms-m5-l2", _M5_SLUG, 7,
         "A B+ tree of order 5 has height 3 levels (root, one internal level, leaves). What is the MINIMUM possible number of leaf nodes?",
         ["4", "6", "8", "10"],
         1,
         "Minimum children: root 2 (if it has children), non-root internal nodes ⌈5/2⌉ = 3. So 2 internal nodes × 3 children each = 6 leaf nodes minimum. (Maximum would be 5 × 5 = 25.)",
         ("amazon",)),
    _mkq("dbms-m5-l2-q5", "dbms-m5-l2", _M5_SLUG, 8,
         "Why do B+ trees beat binary search trees for disk-based databases?",
         ["B+ trees use less memory per key",
          "High fanout collapses the height (~3 levels vs ~20), so a lookup needs far fewer disk I/Os, and each node matches a disk page",
          "Binary trees cannot store duplicate keys",
          "B+ trees never need rebalancing"],
         1,
         "Disk I/O dominates: a lookup costs one I/O per level. Fanout ~100 gives height ~3 for a million records versus ~20 for a binary tree — roughly 7× fewer disk seeks. B+ trees absolutely do rebalance (splits/merges); they just keep every leaf at equal depth.",
         ("microsoft",)),
    _mkq("dbms-m5-l2-q6", "dbms-m5-l2", _M5_SLUG, 9,
         "In a B+ tree of order 4, a non-root internal node drops to 0 keys after a deletion. What must happen?",
         ["Nothing — 0 keys is always valid",
          "The node splits into two nodes",
          "Underflow: the node borrows a key from a sibling or merges with a sibling (possibly propagating upward)",
          "The whole tree is rebuilt from the leaves"],
         2,
         "Order 4 requires at least ⌈4/2⌉ − 1 = 1 key in a non-root internal node, so 0 keys is an underflow. The fix is redistribution (borrow from a sibling) or merging with a sibling, which can propagate up and even shrink the tree height. Splitting is for overflow, not underflow.",
         ("google",)),

    # ---- L3: Clustered vs Non-Clustered ----
    _mkq("dbms-m5-l3-q1", "dbms-m5-l3", _M5_SLUG, 4,
         "What is a clustered index?",
         ["An index stored on a remote cluster of machines",
          "An index that dictates the physical order of the table's rows on disk — one per table",
          "An index that can only be built on two columns together",
          "A temporary index created during query execution"],
         1,
         "A clustered index *is* the table's physical organization: rows are stored sorted by the clustered key. Since rows have exactly one physical order, a table can have only one clustered index.",
         ("tcs",)),
    _mkq("dbms-m5-l3-q2", "dbms-m5-l3", _M5_SLUG, 5,
         "How does a lookup via a non-clustered (secondary) index work?",
         ["It reads the row directly — one hop",
          "Two hops: find the key in the separate index structure, then follow its pointer to fetch the row",
          "It scans the whole table and filters",
          "It only works if a clustered index also exists"],
         1,
         "A secondary index is a separate structure of (key → row locator). The engine first seeks the key in the index, then does a second hop to fetch the actual row — which is why covering indexes (no second hop) are such a win.",
         ("infosys",)),
    _mkq("dbms-m5-l3-q3", "dbms-m5-l3", _M5_SLUG, 6,
         "In InnoDB/MySQL, what does the PRIMARY KEY become physically?",
         ["A non-clustered index", "The clustered index", "A hash index", "No index at all"],
         1,
         "InnoDB stores the table clustered by the primary key — the PK *is* the clustered index, so PK lookups fetch the row directly with no second hop. (A table without a PK gets a hidden row-id cluster.)",
         ("wipro",)),
    _mkq("dbms-m5-l3-q4", "dbms-m5-l3", _M5_SLUG, 7,
         "An index on (dept, salary) answers SELECT salary FROM emp WHERE dept = 'X' without touching the table. This index is called:",
         ["A sparse index", "A covering index", "A clustered index", "A bitmap index"],
         1,
         "It is covering: it contains every column the query needs, so the engine answers from the index alone (an 'Index Only Scan' in Postgres EXPLAIN). Sparse/dense describe entry density, not column coverage.",
         ("accenture", "amazon")),
    _mkq("dbms-m5-l3-q5", "dbms-m5-l3", _M5_SLUG, 8,
         "Why can a table have only one clustered index?",
         ["The SQL standard forbids more than one",
          "The table's rows have a single physical order on disk, and the clustered index defines it",
          "Clustered indexes cannot be updated",
          "Secondary indexes already provide the same benefit"],
         1,
         "Clustering = physical row order, and rows can only be physically sorted one way. You can have many secondary (non-clustered) indexes, but only one structure can define where the rows themselves live.",
         ("microsoft",)),
    _mkq("dbms-m5-l3-q6", "dbms-m5-l3", _M5_SLUG, 9,
         "Query: SELECT b FROM t WHERE a = 5. An index on (a) exists, but EXPLAIN shows a table lookup for column b. How do you eliminate the table lookup?",
         ["Add a separate index on (b)",
          "Build a composite covering index on (a, b)",
          "Make (a) the clustered index",
          "Partition the table by b"],
         1,
         "A covering index on (a, b) contains both the filter column and the selected column, so the query is answered from the index alone. A lone index on (b) doesn't help the a = 5 filter, and changing the clustered index doesn't remove the second hop.",
         ("google",)),

    # ---- L4: Hash Indexing ----
    _mkq("dbms-m5-l4-q1", "dbms-m5-l4", _M5_SLUG, 4,
         "How does a hash index answer WHERE id = 42?",
         ["It traverses a B+ tree from the root",
          "It hashes the key to a bucket number and jumps straight to that bucket — O(1) on average",
          "It scans all buckets until it finds id 42",
          "It binary-searches the sorted table"],
         1,
         "h(key) → bucket number gives direct access with no tree traversal, hence O(1) average for equality lookups. The trade-off is that hashing destroys key order, so range queries can't use it.",
         ("tcs",)),
    _mkq("dbms-m5-l4-q2", "dbms-m5-l4", _M5_SLUG, 5,
         "In static hashing, what happens when two keys hash to the same full bucket?",
         ["One key is discarded",
          "The table is immediately rehashed",
          "Overflow chaining: the bucket links to overflow buckets holding the extra entries",
          "The hash function is changed automatically"],
         2,
         "Static hashing handles collisions with chaining — full buckets link to overflow buckets. Nothing is discarded or rehashed automatically; the cost is that long chains degrade lookup performance.",
         ("infosys",)),
    _mkq("dbms-m5-l4-q3", "dbms-m5-l4", _M5_SLUG, 6,
         "What is the main weakness of static hashing?",
         ["It cannot handle equality lookups",
          "The bucket count is fixed, so overflow chains grow as data grows (and it cannot shrink) — performance degrades",
          "It requires the keys to be sorted",
          "It uses more disk seeks than a full table scan"],
         1,
         "Fixed bucket count is the flaw: growth lengthens overflow chains (degrading the O(1) toward a scan) and deletions can't return space. It works only when data size is known and stable up front.",
         ("wipro",)),
    _mkq("dbms-m5-l4-q4", "dbms-m5-l4", _M5_SLUG, 7,
         "In extendible hashing, when a bucket overflows and its local depth equals the global depth, what happens?",
         ["The bucket's entries are discarded",
          "The directory doubles (global depth increases by 1), then the bucket splits",
          "The entire table is rehashed with a new function",
          "The bucket merges with its neighbor"],
         1,
         "A directory of 2^global_depth pointers maps hash prefixes to buckets. When a bucket at local depth == global depth splits, the directory must double first so the two halves get distinct entries; then the bucket splits and local depths update.",
         ("accenture",)),
    _mkq("dbms-m5-l4-q5", "dbms-m5-l4", _M5_SLUG, 8,
         "Which query can a hash index NOT speed up?",
         ["WHERE id = 42", "WHERE email = 'a@x.com'", "WHERE age BETWEEN 20 AND 30", "WHERE ssn = '123'"],
         2,
         "Hashing destroys key order — adjacent ages scatter to random buckets — so range predicates (BETWEEN, <, >, ORDER BY) can't navigate a hash index. Equality lookups are exactly what hash indexes are for.",
         ("amazon", "microsoft")),
    _mkq("dbms-m5-l4-q6", "dbms-m5-l4", _M5_SLUG, 9,
         "Extendible hashing: global depth is 2 and a bucket with local depth 2 overflows and splits. What happens to the directory?",
         ["It stays the same size",
          "It doubles — global depth goes from 2 to 3",
          "It halves",
          "It is rebuilt from scratch"],
         1,
         "Because the splitting bucket's local depth (2) equals the global depth (2), the directory must double from 4 to 8 entries (global depth 2 → 3) before the split, so each half-bucket gets its own directory entry.",
         ("google",)),

    # ---- L5: Query Optimization ----
    _mkq("dbms-m5-l5-q1", "dbms-m5-l5", _M5_SLUG, 4,
         "What does a cost-based query optimizer do?",
         ["Always uses whatever index the DBA created most recently",
          "Estimates the cost of candidate execution plans using table statistics and picks the cheapest",
          "Executes every possible plan and keeps the fastest result",
          "Rewrites the query into a different SQL dialect"],
         1,
         "The optimizer never runs plans to compare them — it *estimates* I/O and CPU cost from statistics (row counts, histograms) and chooses the lowest estimate. Bad statistics therefore produce bad plans.",
         ("tcs",)),
    _mkq("dbms-m5-l5-q2", "dbms-m5-l5", _M5_SLUG, 5,
         "What is 'selectivity' of a predicate, and how does it affect index choice?",
         ["The number of indexes on the table; more indexes always win",
          "The fraction of rows matching the predicate; low selectivity (few rows) favors an index seek, high selectivity favors a scan",
          "The speed of the disk; faster disks need fewer indexes",
          "The number of columns in the SELECT list"],
         1,
         "Selectivity = matching rows / total rows. WHERE id = 42 matches almost nothing → index seek. WHERE status='active' matching 60% → the optimizer correctly prefers a sequential scan over millions of random index hops.",
         ("infosys",)),
    _mkq("dbms-m5-l5-q3", "dbms-m5-l5", _M5_SLUG, 6,
         "EXPLAIN shows 'Seq Scan on orders' for your query. What does that mean?",
         ["The query used an index to seek matching rows",
          "The query read the entire orders table row by row",
          "The query failed and fell back to a safe mode",
          "The orders table is locked"],
         1,
         "Seq Scan = sequential/full table scan: every row read and filtered. It's the right choice for low-selectivity predicates or tiny tables, and a red flag when you expected an index seek on a huge table.",
         ("wipro",)),
    _mkq("dbms-m5-l5-q4", "dbms-m5-l5", _M5_SLUG, 7,
         "A 10M-row table has an index on department, but WHERE department = 'Sales' (4M rows) uses a Seq Scan. Why is the optimizer right?",
         ["Indexes never work on text columns",
          "40% selectivity is poor: 4M random index lookups cost more than one sequential pass",
          "The table is too large for any index",
          "Seq Scan is always a bug"],
         1,
         "At 40% selectivity the index plan would do ~4M random page hops versus one sequential read — the cost model correctly prefers the scan. The optimizer isn't broken; the predicate just isn't selective enough for the index to pay off.",
         ("accenture", "amazon")),
    _mkq("dbms-m5-l5-q5", "dbms-m5-l5", _M5_SLUG, 8,
         "The optimizer picks a nested-loop join for a join that actually processes a million rows, and the query crawls. Most likely cause and fix?",
         ["The join condition is wrong; rewrite the ON clause",
          "Stale statistics made the optimizer underestimate the input size; run ANALYZE to refresh them",
          "The server needs more RAM; add memory",
          "Nested-loop joins are never chosen; the EXPLAIN output is fake"],
         1,
         "A nested loop for a huge join almost always means the optimizer *thought* the input was small — a cardinality misestimate from stale statistics after bulk loads/deletes. ANALYZE refreshes the stats so the cost model sees reality.",
         ("microsoft",)),
    _mkq("dbms-m5-l5-q6", "dbms-m5-l5", _M5_SLUG, 9,
         "What is the difference between EXPLAIN and EXPLAIN ANALYZE in Postgres?",
         ["EXPLAIN is for MySQL; EXPLAIN ANALYZE is for Postgres",
          "EXPLAIN shows the estimated plan; EXPLAIN ANALYZE actually executes the query and reports real row counts and timings",
          "EXPLAIN ANALYZE only works on SELECT statements",
          "There is no difference"],
         1,
         "EXPLAIN shows the optimizer's *estimates* without running anything; EXPLAIN ANALYZE executes the statement and shows actual rows, loops, and timing per node — the ground truth for diagnosing why an estimate (and thus the plan) went wrong. (Careful: it really runs the query, including writes.)",
         ("google",)),

    # ---- L6: Join Algorithms ----
    _mkq("dbms-m5-l6-q1", "dbms-m5-l6", _M5_SLUG, 4,
         "How does a nested-loop join work, and when is it a good choice?",
         ["It sorts both tables then merges; good for huge tables",
          "For each row of the outer table it scans the inner table; good when the outer table is tiny or the inner has an index on the join key",
          "It builds a hash table on both tables; good for any join",
          "It always reads both tables exactly once"],
         1,
         "Nested loop = outer row × inner scan, cost ≈ |outer| × |inner|. It's fine for a tiny outer input, and with an index on the inner join key (indexed nested loop) each inner 'scan' becomes a cheap index seek.",
         ("tcs",)),
    _mkq("dbms-m5-l6-q2", "dbms-m5-l6", _M5_SLUG, 5,
         "How does block nested-loop join improve on plain nested-loop join?",
         ["It sorts the outer table first",
          "It buffers a block of outer rows in memory, scanning the inner table once per block instead of once per row",
          "It uses a hash table instead of scanning",
          "It runs the loop on multiple CPU cores"],
         1,
         "Batching outer rows into memory blocks cuts inner-table scans by a factor of the block size. It's still O(|outer|×|inner|) work in the worst case, but with far fewer repeated I/Os.",
         ("infosys",)),
    _mkq("dbms-m5-l6-q3", "dbms-m5-l6", _M5_SLUG, 6,
         "When is sort-merge join the best choice?",
         ["When both inputs are already sorted on the join key (e.g. via indexes) or the result must be sorted — then the merge is one linear pass",
          "When there are no indexes at all",
          "When the join condition is an inequality",
          "Always — it is the fastest join for every case"],
         0,
         "Sort-merge's cost is dominated by sorting; if inputs arrive sorted (index order) or sorted output is required anyway, the sort is free and the merge is linear. It also handles non-equi conditions, unlike hash join.",
         ("wipro",)),
    _mkq("dbms-m5-l6-q4", "dbms-m5-l6", _M5_SLUG, 7,
         "How does a hash join work?",
         ["Sort both tables, then merge",
          "Build a hash table on the smaller relation, then probe it with each row of the larger relation; works for equi-joins",
          "Scan the inner table once per outer row",
          "Compare every pair of rows with a hash of the full row"],
         1,
         "Build phase: hash the smaller (build) relation's join keys into memory. Probe phase: stream the larger relation, hashing each key to find matches. Equality-only — a hash can't evaluate range conditions.",
         ("accenture",)),
    _mkq("dbms-m5-l6-q5", "dbms-m5-l6", _M5_SLUG, 8,
         "Join a 1-billion-row fact table with a 100-row dimension table (equi-join, no indexes). Which algorithm typically wins?",
         ["Sort-merge join", "Hash join, building the hash table on the 100-row table", "Plain nested-loop join", "Cartesian product with a filter"],
         1,
         "Hash join: the 100-row build side fits trivially in memory, and the billion-row probe side streams through once. Nested loop would do 10^11 inner probes; sort-merge would sort a billion rows pointlessly.",
         ("amazon", "microsoft")),
    _mkq("dbms-m5-l6-q6", "dbms-m5-l6", _M5_SLUG, 9,
         "The join condition is ON o.total > c.credit_limit (a non-equi condition). Which algorithm canNOT be used?",
         ["Nested-loop join", "Sort-merge join", "Hash join", "Block nested-loop join"],
         2,
         "Hash join requires equality to hash on — there is no single bucket for 'greater than'. Non-equi joins fall back to nested-loop (or block nested-loop) and sort-merge variants.",
         ("google",)),
]


# ---------------------------------------------------------------------------
# MODULE 6 — ADVANCED TOPICS
# ---------------------------------------------------------------------------

_M6 = "dbms-m6"
_M6_SLUG = "advanced-topics"

LESSONS_M6 = [
    _mkl(
        "dbms-m6-l1", _M6, "nosql-introduction", "NoSQL Introduction",
        """## Beyond the relational model

Relational databases assume a fixed schema and scale *up* (bigger machine).
When data is huge, schema-fluid, or access patterns are simple key lookups,
**NoSQL** ("not only SQL") trades some relational guarantees for scale and
flexibility. Four data models to know:

**Document** (MongoDB, CouchDB): data as JSON-like documents grouped in
collections. A user document can *embed* its addresses and recent orders —
stored in the shape you actually fetch. Schema is flexible: two documents
in one collection may have different fields.

**Key-value** (Redis, DynamoDB): the simplest model — a giant distributed
hash table. Blazing-fast lookups by key, often in-memory, with TTL expiry.
The natural home of caches, sessions, and counters.

**Column-family / wide-column** (Cassandra, HBase): rows with billions of
entries and *sparse* columns — each row can carry different columns. Built
for massive write throughput and time-series/event data spread across many
machines.

**Graph** (Neo4j): nodes and edges as first-class citizens. "Friends of
friends who bought X" is a graph traversal, not a five-table join — the
natural model for social networks, fraud rings, and recommendations.

## The common thread

**Flexible schema** — add a field without migrating the whole table — and
**horizontal scaling** designed in from day one. The price: weaker ad-hoc
querying (no universal JOIN) and consistency trade-offs (next lesson).
Choosing well means matching the *data shape and access pattern* to the
model — not chasing hype.
""",
        1,
    ),
    _mkl(
        "dbms-m6-l2", _M6, "cap-theorem", "CAP Theorem",
        """## Pick two

The **CAP theorem** (Brewer): a distributed data store can guarantee only
**two of three**:

- **Consistency** — every read sees the latest write (a single-copy
  illusion, also called linearizability),
- **Availability** — every request gets a (non-error) response,
- **Partition tolerance** — the system keeps working despite network splits
  between nodes.

In practice partitions *will* happen — networks fail — so partition
tolerance is effectively mandatory. The real decision is **CP vs AP**,
and it bites only *during* a partition:

**CP** — consistency over availability: during a partition the minority
side *refuses* requests rather than risk serving stale data. Examples:
**HBase**, **MongoDB** (primary-based — can't reach the primary, writes
stop), etcd/ZooKeeper. Right for money, inventory, anything where a wrong
answer is worse than no answer.

**AP** — availability over consistency: both sides keep serving, accept
conflicting writes, and **reconcile later** — *eventual consistency*.
Examples: **Cassandra**, **DynamoDB**, CouchDB. Right for shopping carts,
social feeds, anything where "always on" beats "always exact".

## Interview clarifications

(1) CAP constrains you *during partitions* — with a healthy network you can
have both C and A. (2) "Consistency" here is *not* ACID consistency; it is
the distributed-systems kind. The NoSQL world mostly chose AP — that is
what **BASE** describes: **B**asically **A**vailable, **S**oft state,
**E**ventually consistent — while traditional RDBMS chose consistency.
""",
        2,
    ),
    _mkl(
        "dbms-m6-l3", _M6, "replication-vs-sharding", "Replication vs Sharding",
        """## Two different bottlenecks, two different answers

**Replication** keeps *copies* of the same data on multiple nodes. The
classic setup is **primary-secondary**: all writes go to the primary, which
streams changes to secondaries; reads fan out to secondaries. What it buys:
**availability** (primary dies → promote a secondary), **read scaling**,
disaster recovery. What it doesn't: **writes don't scale** — every write
still hits the primary — and secondaries lag (**replication lag**), so
reads can be stale.

**Sharding** (horizontal partitioning) *splits* the data: each node holds a
different slice, chosen by a **shard key** (e.g. `user_id % N`). What it
buys: **write scaling** and unbounded data size — add shards, add
throughput. What it costs: cross-shard queries are expensive, rebalancing
is painful, and the shard key is a one-way door — choose badly and you're
stuck with it.

## The shard key is the whole game

A good shard key has **high cardinality** (many distinct values), **even
distribution**, and alignment with query patterns. The classic failure is
**hotspotting**: shard by auto-increment ID or timestamp and every new
write lands on the *same* newest shard while the rest sit idle. Fix: hash
the key or pick something naturally distributed like `user_id`.

## The one-liner

**Replication scales reads and buys availability; sharding scales writes
and buys capacity.** Need 10× read throughput? Replicas. One primary
drowning in writes? Shards. Need both? Sharded clusters where each shard is
itself replicated — exactly what production MongoDB/Cassandra deployments
look like.
""",
        3,
    ),
    _mkl(
        "dbms-m6-l4", _M6, "mongodb-and-choosing-nosql",
        "MongoDB Basics & Choosing NoSQL",
        """## MongoDB in relational terms

A MongoDB **database** holds **collections** (≈ tables), which hold
**documents** (≈ rows). Documents are BSON — binary JSON — so nesting is
natural: a user document can embed an array of addresses directly.

## Embed vs reference — the core modeling decision

**Embed** data that is accessed *together*, is one-to-few, and doesn't
change independently: addresses inside a user, line items inside an order.
One read fetches everything; no joins needed.

**Reference** (store an ObjectId, like a foreign key) when data is *many*,
*shared*, or updated independently: products referenced by thousands of
orders; comments that grow without bound (documents cap at **16MB** —
embedding an endless comment thread will hit the wall). Rule of thumb:
*embed for read-together, reference for write-apart.*

## When SQL wins

Complex ad-hoc joins across entities; multi-row **ACID transactions**
(money movement); rigid, stable schemas; strong consistency requirements;
and — honestly — when the data *fits* on one machine. Don't distribute
what doesn't need distributing.

## When NoSQL wins

Massive scale-out (read/write volume beyond one node); **flexible or
evolving schemas** (fifty product types, each with different attributes);
simple access patterns (key lookups, not six-table joins); high-throughput
event/time-series ingestion; and the polyglot reality — cache in Redis,
documents in MongoDB, graph in Neo4j, relational for the ledger.

The senior interview answer: it's not SQL *versus* NoSQL. It's matching the
data's shape, scale, and consistency needs to the store — and being able to
name what each choice *costs*.
""",
        4,
    ),
]

QUESTIONS_M6 = [
    # ---- L1: NoSQL Introduction ----
    _mkq("dbms-m6-l1-q1", "dbms-m6-l1", _M6_SLUG, 5,
         "Match each NoSQL type to its example system:",
         ["Document–Redis, Key-value–MongoDB, Column-family–Neo4j, Graph–Cassandra",
          "Document–MongoDB, Key-value–Redis, Column-family–Cassandra, Graph–Neo4j",
          "Document–Cassandra, Key-value–Neo4j, Column-family–MongoDB, Graph–Redis",
          "Document–Neo4j, Key-value–Cassandra, Column-family–Redis, Graph–MongoDB"],
         1,
         "The canonical mapping: MongoDB = document store, Redis = key-value store, Cassandra = column-family (wide-column) store, Neo4j = graph database. Interviewers love this exact matching question.",
         ("tcs",)),
    _mkq("dbms-m6-l1-q2", "dbms-m6-l1", _M6_SLUG, 6,
         "What does 'flexible schema' mean in a document database?",
         ["There is no way to query the data",
          "Documents in the same collection can have different fields; adding a field needs no table migration",
          "Every document must contain every field",
          "The schema is stored in a separate relational database"],
         1,
         "Flexible schema means each document carries its own shape — one user doc can have a 'phone' field while another doesn't, and introducing a new field is just writing it. No ALTER TABLE migration across millions of rows.",
         ("infosys",)),
    _mkq("dbms-m6-l1-q3", "dbms-m6-l1", _M6_SLUG, 7,
         "A social network needs 'friends of friends who like product X' queries over millions of users. The most natural data model is:",
         ["Key-value", "Document", "Graph", "Column-family"],
         2,
         "Friend-of-friend is a multi-hop relationship traversal — exactly what graph databases (Neo4j) model as first-class nodes and edges. In a relational or document store it becomes an expensive multi-join; in a graph store it's a native traversal.",
         ("wipro", "accenture")),
    _mkq("dbms-m6-l1-q4", "dbms-m6-l1", _M6_SLUG, 8,
         "An e-commerce site needs shopping-cart sessions for 1M concurrent users: sub-millisecond reads/writes by session ID, auto-expire after 30 minutes. Best fit?",
         ["Graph database", "Key-value store (e.g. Redis)", "Column-family store", "Relational database with joins"],
         1,
         "This is the textbook key-value workload: simple key-based access (session ID → cart), extreme speed, TTL expiry — Redis's home turf. No complex queries or relationships justify anything heavier.",
         ("amazon",)),
    _mkq("dbms-m6-l1-q5", "dbms-m6-l1", _M6_SLUG, 8,
         "A system ingests billions of sensor events per day with sparse, varying columns per device. Best fit?",
         ["Document database", "Key-value store", "Column-family / wide-column store (e.g. Cassandra)", "Graph database"],
         2,
         "Wide-column stores are built for exactly this: massive write throughput, billions of rows, sparse columns where each row carries different fields. Key-value can't model the per-device structure; documents would be heavier per write.",
         ("microsoft",)),
    _mkq("dbms-m6-l1-q6", "dbms-m6-l1", _M6_SLUG, 9,
         "A product catalog has 50 product types with wildly different attributes, each product is read as a whole object, and there are no complex joins. Why does a document database beat a relational one here?",
         ["Document databases are always faster at everything",
          "Hierarchical, read-together data with an evolving schema maps naturally to documents; relationally it forces sparse nullable columns or painful EAV tables",
          "Relational databases cannot store products",
          "Documents automatically create indexes"],
         1,
         "Fifty product types × different attributes means relationally you'd have hundreds of mostly-NULL columns or an entity-attribute-value mess. A document embeds each product's natural shape, fetched in one read, with schema evolving per document. The win is modeling fit, not raw speed.",
         ("google",)),

    # ---- L2: CAP Theorem ----
    _mkq("dbms-m6-l2-q1", "dbms-m6-l2", _M6_SLUG, 5,
         "The CAP theorem states that a distributed data store can guarantee only two of:",
         ["Consistency, Availability, Partition tolerance",
          "Correctness, Atomicity, Persistence",
          "Concurrency, Accuracy, Performance",
          "Clustering, Automation, Provisioning"],
         0,
         "CAP = Consistency (every read sees the latest write), Availability (every request gets a response), Partition tolerance (survives network splits). The 'pick two' framing is the single most-asked distributed-systems interview question.",
         ("tcs",)),
    _mkq("dbms-m6-l2-q2", "dbms-m6-l2", _M6_SLUG, 6,
         "Why is partition tolerance effectively non-negotiable in distributed systems?",
         ["Because partitions make systems faster",
          "Because network failures and splits will inevitably happen, so the system must be designed to survive them",
          "Because the CAP theorem requires choosing it",
          "Because partitions improve consistency"],
         1,
         "You can't opt out of networks failing. Since partitions are a matter of when, not if, real systems must tolerate them — making the practical choice CP vs AP during a split, not whether to handle partitions at all.",
         ("infosys",)),
    _mkq("dbms-m6-l2-q3", "dbms-m6-l2", _M6_SLUG, 7,
         "Which system is a CP example, and how does it behave during a network partition?",
         ["Cassandra — both sides keep accepting writes",
          "MongoDB — the side that can't reach the primary refuses writes rather than risk inconsistency",
          "Redis — it merges conflicting writes automatically",
          "DynamoDB — it becomes read-only everywhere"],
         1,
         "MongoDB is primary-based (CP): without the primary, a partition side stops accepting writes to avoid divergence. Cassandra and DynamoDB are the AP counterexamples — they keep serving on both sides and reconcile later.",
         ("wipro",)),
    _mkq("dbms-m6-l2-q4", "dbms-m6-l2", _M6_SLUG, 8,
         "Which pair correctly identifies AP systems and their partition behavior?",
         ["HBase and MongoDB — refuse writes on the minority side",
          "Cassandra and DynamoDB — both sides keep accepting writes and reconcile later (eventual consistency)",
          "Postgres and MySQL — single-node systems",
          "etcd and ZooKeeper — sacrifice availability for consistency"],
         1,
         "Cassandra/DynamoDB choose availability during partitions: every side stays writable, conflicts are reconciled afterward — eventual consistency. HBase/MongoDB/etcd are the CP side; single-node Postgres is outside CAP's scope.",
         ("accenture", "amazon")),
    _mkq("dbms-m6-l2-q5", "dbms-m6-l2", _M6_SLUG, 8,
         "An AP system keeps accepting writes on both sides of a network partition. What is necessarily sacrificed at that moment?",
         ["Partition tolerance", "Strong consistency — readers may see stale or divergent data until reconciliation", "Availability", "Durability"],
         1,
         "AP keeps availability + partition tolerance, so consistency is what gives: the two sides diverge and readers see stale or conflicting values until the partition heals and writes reconcile (eventual consistency).",
         ("microsoft",)),
    _mkq("dbms-m6-l2-q6", "dbms-m6-l2", _M6_SLUG, 9,
         "What does BASE stand for, and which side of the CAP trade-off does it describe?",
         ["Basic And Simple Entities — the CP philosophy",
          "Basically Available, Soft state, Eventually consistent — the AP philosophy behind many NoSQL systems",
          "Balanced ACID Storage Engine — the CA philosophy",
          "Binary And Structured Encoding — a storage format"],
         1,
         "BASE (Basically Available, Soft state, Eventually consistent) is the AP world's answer to ACID: stay available, accept temporary divergence, converge later. It's the design philosophy behind Cassandra, DynamoDB, and CouchDB-style systems.",
         ("google",)),

    # ---- L3: Replication vs Sharding ----
    _mkq("dbms-m6-l3-q1", "dbms-m6-l3", _M6_SLUG, 5,
         "What is database replication?",
         ["Splitting different data across different nodes",
          "Keeping copies of the same data on multiple nodes, for availability and read scaling",
          "Compressing the database to save disk",
          "Encrypting data at rest"],
         1,
         "Replication = copies of the same data on multiple nodes (typically primary-secondary). It buys availability (failover) and read scaling (reads fan out to secondaries) — but not write scaling, since all writes still go to the primary.",
         ("tcs",)),
    _mkq("dbms-m6-l3-q2", "dbms-m6-l3", _M6_SLUG, 6,
         "What is sharding, and what bottleneck does it solve?",
         ["Copying data to backup nodes; solves availability",
          "Splitting the dataset across nodes by a shard key; scales write throughput and data capacity",
          "Caching hot rows in memory; solves read latency",
          "Partitioning by time for archival; solves compliance"],
         1,
         "Sharding (horizontal partitioning) divides data by shard key so each node holds a slice — writes spread across nodes, and total capacity grows with shard count. It's the answer when one primary can't absorb the write load.",
         ("infosys",)),
    _mkq("dbms-m6-l3-q3", "dbms-m6-l3", _M6_SLUG, 7,
         "Reads from a secondary replica return data that is 2 seconds old. What is happening?",
         ["The secondary is corrupted",
          "Replication lag: writes go to the primary and propagate asynchronously, so secondaries are briefly stale",
          "The shard key is badly chosen",
          "The query is using the wrong index"],
         1,
         "In primary-secondary replication, secondaries apply the primary's changes asynchronously — that delay is replication lag, and reads from secondaries are eventually consistent. It's normal behavior, not corruption; applications needing fresh reads must read from the primary.",
         ("wipro", "accenture")),
    _mkq("dbms-m6-l3-q4", "dbms-m6-l3", _M6_SLUG, 7,
         "Which are properties of a GOOD shard key?",
         ["Low cardinality and monotonic increase",
          "High cardinality, even distribution across shards, and alignment with query patterns",
          "It must be the primary key of every table",
          "It should change with every query"],
         1,
         "A good shard key spreads writes evenly (high cardinality, uniform distribution) and matches how you query (so most queries hit one shard). Low-cardinality or monotonic keys are exactly what cause hotspotting.",
         ("amazon",)),
    _mkq("dbms-m6-l3-q5", "dbms-m6-l3", _M6_SLUG, 8,
         "A system shards by created_at timestamp. The newest shard is overloaded while older shards sit idle. Name the problem and the fix.",
         ["Replication lag — add more replicas",
          "Hotspotting — use a hashed or naturally distributed key (e.g. user_id) instead of a monotonic one",
          "Deadlock — use wound-wait",
          "Cache stampede — add a CDN"],
         1,
         "Monotonic keys (timestamps, auto-increment IDs) route all new writes to one shard: hotspotting. Hashing the key or choosing a naturally distributed attribute like user_id spreads writes evenly across shards.",
         ("microsoft",)),
    _mkq("dbms-m6-l3-q6", "dbms-m6-l3", _M6_SLUG, 9,
         "After adding 5 read replicas, read throughput is 10x but write throughput is unchanged. Why, and what would scale writes?",
         ["The replicas are misconfigured; fix them to scale writes",
          "Replication only scales reads — every write still goes to the single primary; writes scale via sharding",
          "Writes are blocked by read locks; use MVCC",
          "The primary needs a bigger machine (vertical scaling is the only option)"],
         1,
         "Replicas are copies: they absorb reads but every write still funnels through the primary. Write scaling needs the data itself split across nodes — sharding — so different nodes absorb different writes. (Each shard is then typically replicated for availability.)",
         ("google",)),

    # ---- L4: MongoDB & Choosing NoSQL ----
    _mkq("dbms-m6-l4-q1", "dbms-m6-l4", _M6_SLUG, 5,
         "In MongoDB terminology, what do 'collection' and 'document' correspond to?",
         ["Collection ≈ database, document ≈ table",
          "Collection ≈ table, document ≈ row (stored as BSON, binary JSON)",
          "Collection ≈ index, document ≈ query",
          "Collection ≈ shard, document ≈ replica"],
         1,
         "Database → collections → documents mirrors database → tables → rows, except documents are schema-flexible BSON that can nest arrays and sub-documents naturally.",
         ("tcs",)),
    _mkq("dbms-m6-l4-q2", "dbms-m6-l4", _M6_SLUG, 6,
         "A user profile is always fetched together with its addresses, and addresses are never shared between users. How should you model this in MongoDB?",
         ["Store addresses in a separate collection and join at query time",
          "Embed the addresses inside the user document",
          "Store addresses in Redis",
          "Duplicate the user inside each address"],
         1,
         "Embed for read-together, one-to-few, unshared data: one read fetches profile + addresses with no join. A separate collection would force application-level joins for data that's never accessed independently.",
         ("infosys",)),
    _mkq("dbms-m6-l4-q3", "dbms-m6-l4", _M6_SLUG, 7,
         "A product is referenced by 10,000 orders and its price changes daily. How should you model product data in MongoDB?",
         ["Embed the full product inside every order",
          "Reference it: store the product's ObjectId in orders, keep one product document",
          "Embed the product and update all 10,000 orders on every price change",
          "Store products as 10,000 separate collections"],
         1,
         "Reference for shared, frequently-updated data: one product document, orders hold its ObjectId. Embedding would duplicate the product 10,000 times and turn every price change into a 10,000-document update — the classic embed-vs-reference decision.",
         ("wipro", "accenture")),
    _mkq("dbms-m6-l4-q4", "dbms-m6-l4", _M6_SLUG, 8,
         "A blog embeds all comments inside the post document, but viral posts hit MongoDB's 16MB document limit. What is the right fix?",
         ["Increase the limit in the config file",
          "Reference comments instead (separate collection), or bucket them — unbounded growing arrays should not be embedded",
          "Split the post into 16MB chunks manually",
          "Switch to a relational database immediately"],
         1,
         "The 16MB limit is hard. Unbounded, independently-growing data (comments) is the textbook case for referencing: keep comments in their own collection (optionally bucketed by post + page). Embedding is for bounded, read-together data.",
         ("amazon",)),
    _mkq("dbms-m6-l4-q5", "dbms-m6-l4", _M6_SLUG, 8,
         "A bank ledger needs multi-row transfers with all-or-nothing guarantees and strong consistency. Which wins and why?",
         ["MongoDB — documents are faster",
          "A relational SQL database — multi-row ACID transactions and strong consistency are its home turf",
          "Redis — in-memory is always best for money",
          "Cassandra — eventual consistency is fine for ledgers"],
         1,
         "Money movement needs multi-row atomicity and strong consistency — exactly what relational ACID transactions guarantee. Eventual consistency (Cassandra) or single-document atomicity (MongoDB) would risk visible money appearing or vanishing.",
         ("microsoft",)),
    _mkq("dbms-m6-l4-q6", "dbms-m6-l4", _M6_SLUG, 9,
         "Catalog: 100M products across 50 types with different attributes each, read whole, schema evolves monthly, no complex joins. Which store and why?",
         ["Relational SQL — rigid schema keeps data clean",
          "Document database (e.g. MongoDB) — flexible per-document schema plus horizontal scale-out; relationally this forces sparse nullable columns or EAV pain",
          "Graph database — products are nodes",
          "Key-value store — products are values"],
         1,
         "Fifty evolving attribute sets with whole-object reads is the document sweet spot: each product carries its natural shape, schema evolves per document without migrations, and the store scales out horizontally. Key-value can't model the structure; graph adds nothing without relationship traversals.",
         ("google",)),
]


# ---------------------------------------------------------------------------
# Combined exports
# ---------------------------------------------------------------------------

LESSONS = LESSONS_M4 + LESSONS_M5 + LESSONS_M6
QUESTIONS = QUESTIONS_M4 + QUESTIONS_M5 + QUESTIONS_M6


# ---------------------------------------------------------------------------
# MODULE 6 — ADVANCED TOPICS
# ---------------------------------------------------------------------------

_M6 = "dbms-m6"
_M6_SLUG = "advanced-topics"

LESSONS_M6 = [
    _mkl("dbms-m6-l1", _M6, "nosql-introduction", "NoSQL Introduction",
"""## NoSQL Introduction

**NoSQL** ("not only SQL") databases trade the rigid table structure of relational
databases for flexible data models that scale horizontally with ease.

### The four types

- **Document stores** (MongoDB, CouchDB): data as JSON-like documents. A `users`
  collection holds documents like `{"name": "Asha", "orders": [...]}` — nested,
  schema-flexible.
- **Key-value stores** (Redis, DynamoDB): the simplest model — `GET`/`SET` by key.
  Blazing fast; used for caching, sessions, counters.
- **Column-family stores** (Cassandra, HBase): data grouped by columns, not rows.
  Great for massive write-heavy workloads (time-series, logs).
- **Graph databases** (Neo4j): nodes + relationships as first-class citizens.
  Perfect for social networks, fraud detection, recommendations.

### Why NoSQL exists

Relational scaling is mostly **vertical** (bigger server). Web-scale workloads need
**horizontal** scaling (more servers) — sharding a normalized schema across machines
is painful, but document/key-value models shard naturally.

> **Interview hook:** "NoSQL doesn't mean *no* SQL — it means *not only* SQL.
> The four types and one use-case each is the 30-second answer interviewers want."
""", 1, 35),
    _mkl("dbms-m6-l2", _M6, "cap-theorem", "CAP Theorem",
"""## CAP Theorem

Eric Brewer's **CAP theorem**: a distributed data store can guarantee at most
**two of three** properties simultaneously:

- **Consistency (C):** every read gets the latest write (all nodes agree).
- **Availability (A):** every request gets a (non-error) response.
- **Partition tolerance (P):** the system keeps working despite network splits.

### The punchline

In any real distributed system, **partitions happen** (networks fail), so P is
non-negotiable. The real choice is **CP vs AP**:

- **CP** (sacrifice availability): HBase, MongoDB (default), etcd/ZooKeeper.
  During a partition, some nodes refuse requests rather than serve stale data.
  Right for banking, inventory — correctness over uptime.
- **AP** (sacrifice consistency): Cassandra, DynamoDB, CouchDB. All nodes answer,
  but replicas may briefly disagree (**eventual consistency**). Right for carts,
  feeds, likes — uptime over perfect agreement.

### Eventual consistency

AP systems converge: given no new writes, all replicas eventually agree. Techniques
like **quorum reads/writes** (R + W > N) and **vector clocks** manage the trade-off.

> **Interview hook:** Draw the triangle, cross out one corner, and say "partitions
> are a fact of life, so it's really CP vs AP." Then give one example of each."
""", 2, 35),
    _mkl("dbms-m6-l3", _M6, "replication-vs-sharding", "Replication vs Sharding",
"""## Replication vs Sharding

Both scale databases horizontally, but they solve **different** problems.

### Replication — copies for safety and reads

- Every node holds a **full copy** of the data (replica set).
- **Primary-secondary:** writes go to the primary, replicate to secondaries;
  reads can fan out to secondaries → read scaling + failover.
- Solves: **availability** and **read throughput**. Does NOT increase write
  capacity or total storage.

### Sharding — split for writes and size

- Data is **partitioned** across nodes by a **shard key**
  (e.g. `user_id % 4`, or ranges of `order_date`).
- Each shard holds a *different* subset → total capacity and write throughput grow.
- Solves: **write scaling** and **data size**.

### The shard-key trap

A bad shard key causes **hotspotting**: e.g. sharding by `country` puts all of
India's traffic on one shard. Good keys distribute evenly *and* keep related
queries on one shard (avoid scatter-gather across all shards).

### In practice

Systems combine both: each shard is itself a replicated replica set
(MongoDB sharded clusters work exactly this way).

> **Interview hook:** "Replication = copies (reads + HA). Sharding = splits
> (writes + size). Shard key choice is the make-or-break decision.""
""", 3, 35),
    _mkl("dbms-m6-l4", _M6, "mongodb-basics-choosing-nosql", "MongoDB Basics & Choosing NoSQL",
"""## MongoDB Basics & Choosing NoSQL

### MongoDB in 60 seconds

- **Documents** (BSON, binary JSON) live in **collections**
  (≈ rows in tables, but schema-flexible).
- **Embedded vs referenced:** store related data *inside* the document
  (an order embeds its items) when accessed together; *reference* by `_id`
  when shared or unbounded (a user references thousands of orders).
- Query: `db.orders.find({status: "shipped"})`; index like SQL
  (`db.orders.createIndex({user_id: 1})`); aggregation pipeline ≈ GROUP BY on steroids.

### Decision guide: SQL vs NoSQL

| Choose SQL (PostgreSQL/MySQL) when… | Choose NoSQL when… |
|---|---|
| Complex joins & ad-hoc queries | Simple access patterns at huge scale |
| Strong consistency (ACID) required | Flexible/evolving schema |
| Well-defined, stable schema | Massive write throughput (logs, IoT) |
| Transactions across entities | Data naturally document/key-shaped |

### The honest middle

Most real systems are **polyglot**: PostgreSQL for orders/payments (ACID),
Redis for sessions/cache, Elasticsearch for search, a warehouse for analytics.
"Which database?" is always answered with "it depends on the access pattern."

> **Interview hook:** Never say "NoSQL replaces SQL." Say: "I match the database
> to the access pattern — ACID transactions stay relational; everything else is
> negotiable.""
""", 4, 40),
]

QUESTIONS_M6 = [
    _mkq("dbms-m6-l1-q1", "dbms-m6-l1", _M6_SLUG, 5,
         "Which NoSQL type does MongoDB belong to?",
         ["Key-value store", "Document store", "Column-family store", "Graph database"],
         1,
         "MongoDB stores JSON-like BSON documents in collections — the defining trait of a document store. Redis is key-value, Cassandra is column-family, Neo4j is graph.",
         ("tcs", "infosys")),
    _mkq("dbms-m6-l1-q2", "dbms-m6-l1", _M6_SLUG, 5,
         "A social-network 'friends' feature with deep relationship traversals ('friends of friends who liked X') is best served by:",
         ["A document store", "A key-value store", "A graph database", "A column-family store"],
         2,
         "Graph databases make relationships first-class: traversals are index-free hops between nodes. In a document store the same query becomes expensive multi-hop application joins.",
         ("amazon", "accenture")),
    _mkq("dbms-m6-l1-q3", "dbms-m6-l1", _M6_SLUG, 6,
         "Which workload is the classic fit for a key-value store like Redis?",
         ["Multi-table analytical reporting", "Session storage and caching", "Full-text search", "Complex financial transactions"],
         1,
         "Key-value stores do one thing extremely well: O(1) GET/SET by key. Sessions, caches, counters and leaderboards fit perfectly; anything needing joins, search, or transactions does not.",
         ("wipro", "tcs")),
    _mkq("dbms-m6-l1-q4", "dbms-m6-l1", _M6_SLUG, 6,
         "In MongoDB, embedding order items inside the order document (rather than a separate table) is preferred when:",
         ["Items are shared across many orders", "Items are always accessed together with their order", "The item list is unbounded (millions per order)", "You need joins across orders"],
         1,
         "Embed when data is accessed together — one read fetches everything, no joins. Reference instead when data is shared, unbounded (document size limits), or updated independently.",
         ("amazon", "microsoft")),
    _mkq("dbms-m6-l1-q5", "dbms-m6-l1", _M6_SLUG, 7,
         "A column-family store like Cassandra is preferred over a document store for:",
         ["Storing user profiles with nested preferences", "High-velocity time-series writes (sensor data, logs)", "Product catalogs with varied attributes", "Content management with rich text"],
         1,
         "Column-family stores are optimized for massive sequential writes partitioned by row key — the time-series/logs pattern. Document stores win when each record is a rich, independently-accessed object.",
         ("google",)),
    _mkq("dbms-m6-l1-q6", "dbms-m6-l1", _M6_SLUG, 8,
         "What does 'schema-flexible' mean in practice for a document store, and what is its main risk?",
         ["No indexes are possible; risk is slow reads", "Documents in one collection can have different fields; risk is inconsistent data without application discipline",
          "Tables are created automatically; risk is storage bloat", "Queries need no language; risk is vendor lock-in"],
         1,
         "Flexibility means evolving fields without migrations — but the database no longer enforces uniformity, so validation moves to the application. Teams that skip it accumulate dirty, inconsistent documents.",
         ("microsoft", "accenture")),
    _mkq("dbms-m6-l2-q1", "dbms-m6-l2", _M6_SLUG, 5,
         "The CAP theorem states a distributed store can guarantee at most two of:",
         ["Consistency, Availability, Partition tolerance", "Concurrency, Atomicity, Persistence", "Compression, Authentication, Privacy", "Correctness, Agility, Performance"],
         0,
         "Brewer's CAP: Consistency (all nodes see the same data), Availability (every request gets a response), Partition tolerance (works despite network splits). Pick two.",
         ("tcs", "infosys")),
    _mkq("dbms-m6-l2-q2", "dbms-m6-l2", _M6_SLUG, 6,
         "Why is the CAP choice in practice usually framed as CP vs AP rather than involving P?",
         ["P stands for performance, which is always tunable", "Network partitions are unavoidable in real systems, so P is effectively mandatory",
          "Consistency and availability are the same property", "The theorem was disproved for modern networks"],
         1,
         "Cables get cut and switches fail — partitions WILL happen. Since you can't opt out of P, the real design decision is what to sacrifice during a partition: consistency (CP) or availability (AP).",
         ("amazon", "wipro")),
    _mkq("dbms-m6-l2-q3", "dbms-m6-l2", _M6_SLUG, 6,
         "A banking ledger should prefer which CAP profile, and why?",
         ["AP, because uptime matters most", "CP, because serving stale balances is unacceptable",
          "CA, because partitions never happen in banks", "AP with strong consistency"],
         1,
         "Money demands correctness: a CP system refuses requests on the minority side of a partition rather than risk double-spends from stale balances. 'CA' is a myth — you can't choose away partitions.",
         ("accenture", "tcs")),
    _mkq("dbms-m6-l2-q4", "dbms-m6-l2", _M6_SLUG, 7,
         "What does 'eventual consistency' guarantee?",
         ["All replicas agree instantly on every write", "If writes stop, all replicas will eventually converge to the same value",
          "Reads are always served from a single master", "Conflicts are impossible"],
         1,
         "Eventual consistency is a liveness promise, not a safety one: the system guarantees convergence once updates cease — but makes no promise about how stale a given read is. Quorums and vector clocks bound the staleness.",
         ("google", "microsoft")),
    _mkq("dbms-m6-l2-q5", "dbms-m6-l2", _M6_SLUG, 7,
         "With replication factor N=3, which read/write quorum (R, W) gives strong consistency?",
         ["R=1, W=1", "R=2, W=2", "R=1, W=3", "R=3, W=1"],
         1,
         "Strong consistency needs R + W > N so every read overlaps every write's replica set. 2+2=4 > 3 works. (1,3) and (3,1) also satisfy it, but (2,2) keeps both reads and writes available with one node down.",
         ("amazon",)),
    _mkq("dbms-m6-l2-q6", "dbms-m6-l2", _M6_SLUG, 9,
         "A product manager asks for a globally distributed cart that is 'always available AND always consistent'. What is the correct engineering response?",
         ["Build it with a CP database in one region", "Explain it's impossible during partitions; propose AP with conflict resolution, or scoped consistency per cart",
          "Use two-phase commit across regions", "Cache everything in Redis"],
         1,
         "CAP says you can't have both during a partition — and cross-region partitions are routine. The honest design: AP with per-cart last-write-wins or CRDT merge (carts merge naturally), or CP with degraded availability. Naming the trade-off is the senior answer.",
         ("google", "microsoft")),
    _mkq("dbms-m6-l3-q1", "dbms-m6-l3", _M6_SLUG, 5,
         "What problem does replication primarily solve?",
         ["Write throughput beyond one machine", "Read scaling and high availability via full copies",
          "Unlimited total storage", "Automatic query optimization"],
         1,
         "Replicas are complete copies: they absorb read traffic and take over on failure. They don't add write capacity (writes still funnel through the primary) or storage.",
         ("tcs", "infosys")),
    _mkq("dbms-m6-l3-q2", "dbms-m6-l3", _M6_SLUG, 5,
         "What problem does sharding primarily solve?",
         ["Read-heavy analytics", "Write scaling and total data size via partitioning",
          "Backup and disaster recovery", "Schema migrations"],
         1,
         "Sharding splits data so each node owns a subset — aggregate write throughput and storage grow with node count. It's the answer when one machine can't hold or ingest the data.",
         ("wipro", "accenture")),
    _mkq("dbms-m6-l3-q3", "dbms-m6-l3", _M6_SLUG, 6,
         "In a primary-secondary replica set, where do writes go?",
         ["To any node, asynchronously merged later", "Only to the primary, then replicated to secondaries",
          "Directly to all nodes simultaneously", "To the secondary with lowest load"],
         1,
         "Single-primary replication funnels all writes through the primary for a total order, then streams them to secondaries. Multi-primary exists but pays for it with conflict resolution.",
         ("tcs", "amazon")),
    _mkq("dbms-m6-l3-q4", "dbms-m6-l3", _M6_SLUG, 7,
         "Sharding users by `country` causes one shard to hold 60% of traffic. This is called:",
         ["Replication lag", "Hotspotting", "Split-brain", "Write amplification"],
         1,
         "Hotspotting: a skewed shard key concentrates load on one node, defeating the purpose of sharding. Fix with a higher-cardinality key (e.g. user_id hash) — possibly at the cost of scatter-gather queries.",
         ("google", "microsoft")),
    _mkq("dbms-m6-l3-q5", "dbms-m6-l3", _M6_SLUG, 7,
         "A query needs data from 4 different shards. What is this called and why is it expensive?",
         ["Scatter-gather; it fans out to every shard and merges results",
          "Map-reduce; it requires Hadoop", "Two-phase commit; it locks all shards",
          "Replication; it duplicates the query"],
         0,
         "Scatter-gather hits all shards and merges — latency becomes the slowest shard, and it defeats shard locality. Good schema design keeps most queries single-shard via the shard key.",
         ("amazon",)),
    _mkq("dbms-m6-l3-q6", "dbms-m6-l3", _M6_SLUG, 8,
         "How do production MongoDB sharded clusters combine replication and sharding?",
         ["Each shard is itself a replica set", "Sharding replaces replication entirely",
          "Replication is only used for backups", "Each replica holds a different shard key"],
         0,
         "The standard topology: data is sharded across shard-replica-sets, and each shard is a 3-node replica set. You get write scaling from sharding AND failover from replication — the two techniques compose.",
         ("microsoft", "accenture")),
    _mkq("dbms-m6-l4-q1", "dbms-m6-l4", _M6_SLUG, 5,
         "In MongoDB, a 'collection' is closest to which relational concept?",
         ["A database", "A table", "A row", "An index"],
         1,
         "Collection ≈ table, document ≈ row, field ≈ column. The difference: documents are schema-flexible and can nest, while rows obey a fixed schema.",
         ("tcs", "infosys")),
    _mkq("dbms-m6-l4-q2", "dbms-m6-l4", _M6_SLUG, 6,
         "What does `db.orders.createIndex({user_id: 1})` do?",
         ["Sorts the collection permanently by user_id", "Builds a B-tree index on user_id for faster lookups",
          "Shards the collection by user_id", "Creates a unique constraint only"],
         1,
         "Same idea as SQL indexes: a B-tree over user_id so equality/range queries avoid full collection scans — at the usual write-amplification cost.",
         ("wipro", "accenture")),
    _mkq("dbms-m6-l4-q3", "dbms-m6-l4", _M6_SLUG, 6,
         "The MongoDB aggregation pipeline is most analogous to:",
         ["A primary key", "SQL GROUP BY with multiple stages (match, group, sort, project)",
          "A foreign key constraint", "A transaction log"],
         1,
         "An aggregation pipeline chains stages — $match (WHERE), $group (GROUP BY), $sort, $project (SELECT) — giving SQL-like analytics over documents.",
         ("amazon", "tcs")),
    _mkq("dbms-m6-l4-q4", "dbms-m6-l4", _M6_SLUG, 7,
         "When should you REFERENCE (not embed) related data in MongoDB?",
         ["Data is always read together", "The related data is large, shared, or unbounded",
          "You want the fastest possible reads", "The relationship is one-to-few and static"],
         1,
         "Embed for co-accessed, bounded, exclusive data. Reference when it's shared across parents, unbounded (would blow the 16MB document limit), or updated independently.",
         ("google",)),
    _mkq("dbms-m6-l4-q5", "dbms-m6-l4", _M6_SLUG, 8,
         "A fintech startup stores money transfers in MongoDB with multi-document updates and no transactions. What is the core risk?",
         ["Slow queries", "Partial updates: debit succeeds but credit fails, with no atomicity guarantee",
          "Document size limits", "Inability to index"],
         1,
         "Money movement needs ACID across documents. Without multi-document transactions (or a relational DB), a crash mid-update leaves the ledger inconsistent — the exact failure ACID exists to prevent.",
         ("microsoft", "amazon")),
    _mkq("dbms-m6-l4-q6", "dbms-m6-l4", _M6_SLUG, 9,
         "Your system uses PostgreSQL for orders, Redis for sessions, and Elasticsearch for search. An interviewer asks 'why three databases?' The strongest answer:",
         ["Microservices require it", "Polyglot persistence: each store matches its access pattern — ACID transactions, O(1) key lookups, and full-text search respectively",
          "It was cheaper", "One database cannot handle production load"],
         1,
         "Name the principle (polyglot persistence) and map each tool to its strength. Bonus: acknowledge the operational cost — three systems to run — and that you'd start with one until the access patterns diverge.",
         ("google", "microsoft")),
]

# Combined exports (standard interface for seed scripts)
LESSONS = LESSONS_M4 + LESSONS_M5 + LESSONS_M6
QUESTIONS = QUESTIONS_M4 + QUESTIONS_M5 + QUESTIONS_M6
