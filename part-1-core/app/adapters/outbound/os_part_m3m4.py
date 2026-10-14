"""Seed content: Operating Systems — Modules 3-4 (Synchronization, Memory Management).

Original theory + placement-style MCQs for SkillForge's OS curriculum.
All numerical answers (page faults, EAT, Banker's safety) recomputed by hand.
"""

from __future__ import annotations

from app.domain.curriculum import (
    CurriculumLesson,
    CurriculumModule,
    CurriculumQuestion,
    validate_curriculum_question,
)

DOMAIN_SLUG = "operating-systems"

MODULES = [
    CurriculumModule(
        id="os-m3",
        domain_slug=DOMAIN_SLUG,
        slug="synchronization",
        name="Synchronization",
        description=(
            "Coordinating concurrent processes: race conditions, the three "
            "critical-section requirements, Peterson's solution, mutexes and "
            "spinlocks, semaphores, the classic synchronization problems, and "
            "deadlock — the four Coffman conditions, prevention, avoidance "
            "with the Banker's algorithm, detection and recovery."
        ),
        order_index=3,
        estimated_days=10,
    ),
    CurriculumModule(
        id="os-m4",
        domain_slug=DOMAIN_SLUG,
        slug="memory-management",
        name="Memory Management",
        description=(
            "How the OS manages RAM: contiguous allocation and fragmentation, "
            "paging with worked address-translation examples, page-table "
            "structures, segmentation, virtual memory and demand paging, page "
            "replacement algorithms with hand-computed fault counts, thrashing "
            "and the working-set model, and the TLB with effective-access-time "
            "numericals."
        ),
        order_index=4,
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
# LESSONS
# ---------------------------------------------------------------------------

LESSONS = [
    # ============================ MODULE 3 ============================
    CurriculumLesson(
        id="os-m3-l1",
        module_id="os-m3",
        slug="race-conditions",
        title="Race Conditions",
        content="""## The concurrent counter

Imagine two threads sharing one integer, `count = 0`. Each thread runs `count++`
a thousand times. Run them one after another and you get 2000. Run them at the
same time and you might get 2000 — or 1973, or 1841. Every run can differ.

## Why: `count++` is three steps

In machine code, `count++` becomes:

```
LOAD  R, count    # copy memory into a register
ADD   R, 1        # increment the register
STORE R, count    # write it back
```

Now interleave two threads: both LOAD the value 5, both ADD to get 6, both
STORE 6. Two increments happened, but the counter moved by one. That vanished
increment is a **lost update**, and the bug is called a **race condition** —
the final result depends on the uncontrolled timing (the "race") between the
threads.

## Races need shared mutable state plus no ordering

Two ingredients are required: threads share something writable, and nothing
forces an order on their accesses. Remove either — give each thread its own
copy of the data, or serialize access with a lock — and the race disappears.
Note that a race needs no true parallelism: on a single CPU, a timer interrupt
can suspend a thread between LOAD and STORE, and the incoming thread then sees
the half-updated state.

## The takeaway

Any read-modify-write on shared data (`count++`, `balance = balance - amount`,
appending to a shared list) is a race unless it is protected. Locks,
semaphores, and atomic instructions exist to close the gap between the read
and the write so that no interleaving can sneak in.
""",
        order_index=1,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="os-m3-l2",
        module_id="os-m3",
        slug="critical-section-requirements",
        title="Critical Section Requirements",
        content="""## The critical section

The **critical section** is the chunk of code that touches shared data — the
part where a race could happen. Every correct solution for protecting it must
satisfy three requirements.

## 1. Mutual exclusion

If one process is executing in its critical section, no other process may be
in its critical section. This is the safety property: at most one at a time,
always. Example: two threads updating a bank balance — mutual exclusion
guarantees the balance is never read while a half-finished update is in flight.

## 2. Progress

If no process is in its critical section and some processes want in, the
choice of who enters cannot be postponed indefinitely — and a process in its
**remainder** (non-critical) section must not block the others. Example of a
violation: strict alternation forces the order P0, P1, P0, P1… If P0 finishes
its work and idles in its remainder section, P1 waits forever for a turn that
will never matter. P0 is outside its critical section yet blocks P1: progress
violated.

## 3. Bounded waiting

After a process requests entry, there must be a bound on how many times other
processes may enter before it gets its turn. This is the fairness property: it
rules out starvation, where a process keeps losing the race to enter and waits
forever while others stream through.

## Why all three matter

Mutual exclusion alone is easy (a simple flag almost does it) but can starve
or freeze processes. Progress keeps the system moving; bounded waiting keeps it
fair. Peterson's solution, mutexes, and semaphores are all judged against
exactly these three requirements.
""",
        order_index=2,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="os-m3-l3",
        module_id="os-m3",
        slug="petersons-solution-hardware",
        title="Peterson's Solution & Hardware Support",
        content="""## Peterson's solution: software-only, two processes

Before hardware helped, Peterson devised a pure-software protocol for two
processes using two shared variables: `flag[2]` (intent) and `turn` (whose
turn it is). Process Pi runs:

```
flag[i] = true;      # "I want to enter"
turn = j;            # "but you go first"
while (flag[j] && turn == j)
    ;                # wait
# critical section
flag[i] = false;     # "I'm done"
```

If Pj is not interested, Pi walks in. If both are interested, `turn` breaks
the tie — whoever set `turn` last waits. It satisfies all three requirements:
mutual exclusion (the turn check), progress (an uninterested process never
blocks), and bounded waiting (once Pi yields the turn, Pj can enter at most
once before Pi).

## Hardware support: test_and_set

Software protocols are subtle, so hardware offers an **atomic** instruction:
`test_and_set(&lock)` reads the lock and writes `true` in one indivisible
step, returning the old value. A spinlock becomes:

```
while (test_and_set(&lock))
    ;   # busy-wait
# critical section
lock = false;
```

The atomicity closes the check-then-set gap that makes plain boolean locks
racy. `compare_and_swap(&x, expected, new)` is the generalization: it writes
`new` only if `x` still equals `expected`, reporting success — the basis of
lock-free programming.

## One honest caveat

Peterson's proof assumes every core observes memory operations in program
order. Modern CPUs and compilers reorder independent writes, so a core might
see `turn = j` before `flag[i] = true`, breaking the protocol. Real systems add
**memory barriers** (fences) to restore ordering.
""",
        order_index=3,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m3-l4",
        module_id="os-m3",
        slug="mutex-locks-spinlocks",
        title="Mutex Locks & Spinlocks",
        content="""## Mutex: acquire and release

A **mutex** (mutual-exclusion lock) is the everyday synchronization primitive.
The contract is tiny:

```
acquire();   # if locked, the caller blocks until it is free
# critical section
release();   # wake one waiter
```

Every `acquire()` must be paired with exactly one `release()`, on every path —
including error paths (hence try/finally or RAII guards). Acquiring twice
without releasing deadlocks a non-recursive mutex; forgetting `release()`
locks everyone out forever.

## Spinlock: busy-waiting instead of blocking

A **spinlock** protects the same way but waits differently: instead of
sleeping, the thread loops testing the lock (`while (test_and_set(&lock));`).
Spinning burns CPU, so when is it acceptable? Two conditions: the critical
section is **short** (the wait will be brief) and the machine has **multiple
CPUs** (the holder can actually run and release the lock while we spin). On a
single CPU, spinning while the holder waits for this very CPU is pure waste —
blocking wins.

## Choosing between them

Use a mutex (blocking) for long or unpredictable waits: the waiter sleeps and
the CPU does useful work. Use a spinlock inside kernels for tiny critical
sections (a few instructions updating a queue), where a context switch would
cost more than the wait itself. Many real mutexes are **adaptive**: spin
briefly, then fall back to blocking — cheap when the wait is short, polite
when it is not.
""",
        order_index=4,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="os-m3-l5",
        module_id="os-m3",
        slug="semaphores",
        title="Semaphores",
        content="""## wait() and signal(): the counter idea

A **semaphore** S is an integer with two atomic operations (historically called
P and V):

- `wait(S)`: try to take one unit — decrement S; if S would go below zero, block.
- `signal(S)`: return one unit — increment S, waking a waiter if any.

The operations are indivisible: no two threads can interleave inside a
`wait()`.

## Binary vs counting

A **binary** semaphore (0 or 1) behaves like a lock: initialize to 1, `wait`
to enter, `signal` to leave. It differs from a mutex in ownership — any thread
may signal a binary semaphore, while only the holder should release a mutex.
A **counting** semaphore tracks multiple identical resources: initialize it to
the resource count (say 5 printers). Each `wait()` takes one printer; each
`signal()` returns one. When S hits 0, further waiters block until a printer
comes back.

## No busy waiting: block and wakeup

The textbook implementation avoids spinning:

```
wait(S):
    S.value--
    if S.value < 0:
        block this thread on S.queue
signal(S):
    S.value++
    if S.value <= 0:
        wake one thread from S.queue
```

A neat consequence: when threads are blocked, `S.value` goes negative, and
its magnitude equals the number of waiting threads. Blocked threads consume no
CPU — the OS parks them and wakes them precisely when a unit frees up. That
makes semaphores the right tool for coordinating producers with consumers or
managing pools of identical resources.
""",
        order_index=5,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m3-l6",
        module_id="os-m3",
        slug="classic-synchronization-problems",
        title="Classic Synchronization Problems",
        content="""## 1. Producer–consumer (bounded buffer)

A producer inserts items into a buffer of N slots; a consumer removes them.
Two constraints: the producer must wait when the buffer is **full**, the
consumer when it is **empty**, and only one thread may touch the buffer at a
time. Solution: three semaphores — `mutex = 1` for exclusive access,
`empty = N` counting free slots, `full = 0` counting filled slots. The producer
does `wait(empty); wait(mutex); insert; signal(mutex); signal(full)`. Order
matters: taking `mutex` before `empty` can deadlock (producer holds the mutex
while blocked on a full buffer, freezing the consumer that would free a slot).

## 2. Readers–writers

Many readers may read a shared database simultaneously, but a writer needs
exclusive access. The "first" solution lets readers in freely (the first reader
locks out writers, the last reader lets them back in) but starves writers if
readers keep arriving. The "second" solution flips the preference and can
starve readers. Real systems pick a policy — or use fair queuing.

## 3. Dining philosophers

Five philosophers sit around a table with five chopsticks, one between each
pair. To eat, a philosopher needs **both** adjacent chopsticks. If all five
grab the left chopstick simultaneously, each holds one and waits forever for
the right — the textbook deadlock. Fixes include: pick up both chopsticks
atomically, number the chopsticks and always take the lower-numbered first
(breaks circular wait), or allow at most four philosophers at the table.

## The pattern

Each problem pairs a real coordination need with the right primitive: counting
semaphores for pools of slots, mutexes for exclusive regions, ordering rules
to break wait cycles.
""",
        order_index=6,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m3-l7",
        module_id="os-m3",
        slug="coffman-conditions",
        title="Deadlock: The Four Coffman Conditions",
        content="""## Deadlock, via dining philosophers

Five philosophers, five chopsticks. All grab the left chopstick at once; each
now waits for the right one, which a neighbor holds. Nobody eats, nobody gives
up — the system is **deadlocked**: a set of processes each waiting for a
resource held by another member of the set, forever.

## The four necessary conditions (Coffman, 1971)

Deadlock can occur **only if all four hold simultaneously**:

1. **Mutual exclusion** — resources are non-sharable. A chopstick can be held
   by only one philosopher at a time.
2. **Hold and wait** — a process holds resources while requesting more. Each
   philosopher grips one chopstick and reaches for the second.
3. **No preemption** — resources cannot be forcibly taken away. Nobody may
   snatch a chopstick from another's hand; it must be released voluntarily.
4. **Circular wait** — a cycle exists in the wait-for relation. Philosopher 0
   waits on 1, 1 waits on 2, …, 4 waits on 0: a closed loop.

## Why "necessary" matters

Each condition is required — remove any single one and deadlock becomes
**impossible**, no matter what the processes do. That is the whole basis of
deadlock prevention: number the chopsticks and force everyone to take the
lower-numbered first, and a wait cycle can never form (condition 4 dies).
Allow the waiter to snatch a chopstick (preemption), and condition 3 dies.
The conditions are a checklist: to prove a system deadlock-free, it suffices
to show one of them never holds.
""",
        order_index=7,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="os-m3-l8",
        module_id="os-m3",
        slug="deadlock-handling",
        title="Deadlock Handling: Prevention, Avoidance & Recovery",
        content="""## Prevention: kill a Coffman condition structurally

Design the system so one condition can never hold: require processes to
request **all** resources upfront (kills hold-and-wait), allow preemption of
resources, or impose a global ordering on resources and force requests in that
order (kills circular wait). Prevention is simple but rigid — upfront
allocation wastes resources a process may never need.

## Avoidance: the Banker's algorithm

Avoidance keeps the conditions but examines each request: grant it only if the
resulting state is **safe** (some order exists in which every process can
finish). It needs each process's maximum claim upfront.

**Worked example.** Resources A=10, B=5, C=7. Allocation and Max:

```
        Alloc      Max       Need (= Max - Alloc)
P0      0 1 0      7 5 3     7 4 3
P1      2 0 0      3 2 2     1 2 2
P2      3 0 2      9 0 2     6 0 0
P3      2 1 1      2 2 2     0 1 1
P4      0 0 2      4 3 3     4 3 1
```

Available = Total − allocated = (10,5,7) − (7,2,5) = (3,3,2). Safety check:
P1's need (1,2,2) ≤ (3,3,2) → finishes, Available becomes (5,3,2). Then P3
(0,1,1) → (7,4,3). Then P4 (4,3,1) → (7,4,5). Then P0 (7,4,3) → (7,5,5). Then
P2 (6,0,0). All finish, so **P1, P3, P4, P0, P2** is a safe sequence and the
state is safe. A request is granted only if a safe sequence still exists
after tentatively granting it.

## Detection and recovery

If prevention and avoidance are too costly, let deadlocks happen: periodically
build a wait-for graph and look for cycles (detection), then recover by
killing processes or preempting resources until the cycle breaks.
""",
        order_index=8,
        estimated_minutes=40,
    ),
    # ============================ MODULE 4 ============================
    CurriculumLesson(
        id="os-m4-l1",
        module_id="os-m4",
        slug="contiguous-allocation-fragmentation",
        title="Contiguous Allocation & Fragmentation",
        content="""## Loading programs into RAM

In the simplest scheme each process occupies one **contiguous** block of
physical memory. Two flavors: **fixed partitions** (memory divided into
equal-size slots at boot; a process takes a whole slot) and **variable
partitions** (each process gets exactly the block size it asks for, wherever
it fits).

## Internal vs external fragmentation

Fixed partitions waste space **inside** the allocation: a 5 KB process in a
16 KB slot leaves 11 KB of slack nobody can use — **internal fragmentation**.
Variable partitions fit exactly, so there is no internal waste — but as
processes come and go, free memory shatters into small scattered holes
between allocated blocks. Total free space may be plenty, yet no single hole
fits the next process — **external fragmentation**.

## Placement strategies

For variable partitions, where to put a new process? **First fit** takes the
first hole that fits (fast, decent). **Best fit** takes the smallest fitting
hole (leaves tiny unusable slivers). **Worst fit** takes the largest hole
(leaves the biggest leftover). Simulations long ago showed first fit is
usually the pragmatic winner.

## Compaction

External fragmentation can be cured by **compaction**: slide all allocated
blocks to one end so the scattered holes merge into one big free region. It
works, but everything moves — expensive, and it requires relocation hardware
so programs still run after their addresses change. This cost is a big reason
real systems moved to paging, which eliminates external fragmentation by
design.
""",
        order_index=1,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="os-m4-l2",
        module_id="os-m4",
        slug="paging-basics",
        title="Paging Basics",
        content="""## Pages and frames

**Paging** chops both the process's logical memory and physical RAM into
fixed-size blocks: a block of logical memory is a **page**, a block of
physical RAM is a **frame**. Pages and frames are the same size (typically
4 KB). A process's pages can live in any frames, in any order — no contiguity
needed, so external fragmentation disappears.

## The page table

The OS keeps a **page table** per process: entry `i` holds the frame number
currently storing page `i`. The MMU translates every logical address by
splitting it into `(page number, offset)` and looking up the frame.

## Worked example

Page size = 1024 bytes. Logical address 3012:

```
page number = 3012 / 1024 = 2        (integer division; 2 x 1024 = 2048)
offset      = 3012 - 2048 = 964
```

Suppose the page table maps page 2 → frame 5. Then:

```
physical address = frame x page_size + offset
                 = 5 x 1024 + 964
                 = 5120 + 964 = 6084
```

The page number is replaced by the frame number; the offset passes through
unchanged. In binary this is trivial: with a 1024-byte page the low 10 bits
are the offset and the rest are the page number.

## The remaining cost

The last page of a process is rarely full: if the final page holds 964 bytes of
a 1024-byte page, 1024 − 964 = 60 bytes are wasted in that page. On average the
last page is half full, so paging trades external fragmentation for internal
fragmentation averaging **half a page** per process — the reason page size is
a careful tradeoff.
""",
        order_index=2,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m4-l3",
        module_id="os-m4",
        slug="page-table-structures",
        title="Page Table Structures",
        content="""## The problem: page tables get huge

With 32-bit addresses and 4 KB pages, a process has 2^32 / 2^12 = 2^20 pages.
At 4 bytes per entry, a flat page table costs 2^20 × 4 = **4 MB per process** —
just for the table, even if the process uses a few kilobytes. Three classic
structures tame this.

## Hierarchical (multilevel) paging

Break the table into smaller tables. In the classic two-level scheme the
20-bit page number splits into 10 + 10 bits: the outer table has 2^10 = 1024
entries pointing to inner tables, each with 1024 entries. The outer table is
only 4 KB, and inner tables are allocated **only for address regions the
process actually uses**. A sparse address space needs just a handful of inner
tables instead of the full 4 MB.

## Hashed page tables

For address spaces beyond 32 bits, even multilevel tables need too many
levels. A hashed page table hashes the virtual page number into a bucket;
each bucket holds a chain of (virtual page, frame) pairs. Table size scales
with memory actually used, not with address-space size — but collisions mean
lookups walk a chain.

## Inverted page tables

Flip the indexing: **one entry per physical frame**, each recording which
(process, page) occupies that frame. Size depends on RAM, never on address
space — ideal for 64-bit systems. The price: finding the frame for a given
page needs hashing, and sharing one frame between two processes is awkward
because a single entry can record only one virtual owner.

## Rule of thumb

Small address space → flat or two-level. Huge (64-bit) address space →
hashed or inverted. Sparse usage → multilevel wins by allocating tables
lazily.
""",
        order_index=3,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m4-l4",
        module_id="os-m4",
        slug="segmentation",
        title="Segmentation",
        content="""## Memory the way programmers see it

A program is not a flat bag of bytes — it is logical units: the main code,
functions, the stack, the heap, global data. **Segmentation** gives each such
unit its own **segment**: a variable-size region identified by a segment
number. A logical address is the pair `(segment number, offset)`.

## The segment table

Each process has a segment table; entry `i` holds two values:

- **base**: the segment's starting physical address
- **limit**: the segment's length

Translation: look up the segment, check `offset < limit` (otherwise the MMU
raises a trap — this is hardware memory protection), then
`physical = base + offset`. Example: segment 2 has base 4300, limit 600;
address (2, 500) → 4800. Address (2, 800) → trap, because 800 ≥ 600.

## Segmentation vs paging

The deep difference is **visibility**: segments mirror program structure the
programmer and compiler see (so protection and sharing are natural per
logical unit — share the code segment, keep stacks private), while pages are
invisible fixed-size blocks the OS manages behind the scenes. The cost of
that visibility: variable-size segments suffer **external fragmentation**,
just like variable partitions — free memory shatters into scattered holes.
Modern x86 actually does both in sequence: segmentation first (logical →
linear address), then paging (linear → physical).
""",
        order_index=4,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="os-m4-l5",
        module_id="os-m4",
        slug="virtual-memory-demand-paging",
        title="Virtual Memory & Demand Paging",
        content="""## Running programs bigger than RAM

**Virtual memory** separates what the programmer sees (a huge logical address
space) from what exists (limited RAM). Only the active pages live in memory;
the rest wait on disk. A 2 GB program runs fine on a 512 MB machine because it
never needs all 2 GB at once.

## Demand paging: load lazily

A **lazy swapper** (demand pager) never loads a page until it is first
touched. Program start is instant, and pages that are never accessed never
cost disk I/O. Each page-table entry carries a **valid/invalid bit**: valid
means the frame number is usable now; invalid means the page is not resident
and touching it triggers a **page fault**.

## Page-fault handling, step by step

1. The MMU traps to the OS.
2. The OS checks the access is legal (an illegal address → terminate the
   process, the familiar segmentation fault).
3. Find a free frame (or evict some page to make one).
4. Schedule a disk read bringing the page in; the faulting process sleeps.
5. When the disk interrupts, update the page table: frame number in, valid
   bit set.
6. **Restart the faulted instruction** — this time it finds the page and
   completes normally.

## A neat trick: copy-on-write

`fork()` would be slow if it copied every page. Instead, parent and child
share all frames marked read-only; the first write to a shared page faults,
and only then does the OS copy that single page. Pages that are never written
— most of them — are never copied at all.
""",
        order_index=5,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m4-l6",
        module_id="os-m4",
        slug="page-replacement-algorithms",
        title="Page Replacement Algorithms",
        content="""## When there is no free frame

On a page fault with every frame occupied, the OS must evict some page to
make room (writing it back first if modified). The choice of victim decides
how many future faults occur.

## FIFO and Belady's anomaly

**FIFO** evicts the page loaded longest ago — simple, but blind to reuse.
Reference string `7, 0, 1, 2, 0, 3, 0, 4` with 3 frames: 7(f), 0(f), 1(f),
2 evicts 7(f), 0 hit, 3 evicts 0(f), 0 evicts 1(f), 4 evicts 2(f) — **7
faults**. (f = fault.) Stranger still is **Belady's anomaly**: with FIFO,
more frames can mean *more* faults. On `1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5`,
3 frames give 9 faults but 4 frames give 10. FIFO evicts by age, not by future
usefulness, so extra frames can evict exactly the wrong pages.

## Optimal: the unreachable ideal

**Optimal** evicts the page whose next use is farthest in the future (or
never). On the first string: 7(f), 0(f), 1(f), 2 evicts 7 — never used again
(f), 0 hit, 3 evicts 2 — never used again (f), 0 hit, 4 evicts 3 (f) — **6
faults**. It needs knowledge of the future, so it cannot be implemented; it
is the yardstick every real algorithm is measured against.

## LRU: the practical approximation

**LRU** evicts the page unused for the longest time, betting the recent past
predicts the near future. On the first string: 7(f), 0(f), 1(f), 2 evicts 7
— least recently used (f), 0 hit, 3 evicts 1 — LRU among {2,0,1} (f), 0 hit,
4 evicts 2 — LRU among {2,3,0} (f) — **6 faults**, matching Optimal here.
Real systems approximate LRU with reference bits and the clock (second-chance)
algorithm, since exact LRU bookkeeping is expensive.
""",
        order_index=6,
        estimated_minutes=40,
    ),
    CurriculumLesson(
        id="os-m4-l7",
        module_id="os-m4",
        slug="thrashing-working-set",
        title="Thrashing & Working Set",
        content="""## When paging collapses

**Thrashing** is the state where the system spends more time moving pages
between RAM and disk than executing processes: nearly every memory access
faults, the CPU idles waiting on the disk, and throughput falls off a cliff.
The usual cause is too high a **degree of multiprogramming** — so many
processes share RAM that each holds fewer frames than it actively needs, and
they steal frames off each other in a vicious cycle.

## The working-set model

A process's **working set** W(t, Δ) is the set of pages it referenced in the
last Δ time units — its current locality. As the program moves between phases
(initialization, main loop, cleanup), the working set slides along with it.
The OS can estimate it with reference bits and a timer.

## Using working sets to fight thrashing

The rule is simple: give each process enough frames to hold its working set.
The OS detects trouble when **the sum of all working sets exceeds the
available frames** — the processes physically cannot keep their localities
resident, so thrashing is inevitable. The cure is to **suspend (swap out) one
or more processes**, shrinking demand until the survivors fit comfortably.
A related adaptive scheme is **page-fault-frequency control**: if a process's
fault rate climbs above an upper threshold it is frame-starved (grant more
frames); below a lower threshold it hoards idle frames (reclaim some).
""",
        order_index=7,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="os-m4-l8",
        module_id="os-m4",
        slug="tlb",
        title="TLB: Translation Lookaside Buffer",
        content="""## Caching translations

Every memory access needs address translation, and walking the page table in
RAM on each access would double memory traffic. The **TLB (translation
lookaside buffer)** is a small, very fast associative cache inside the MMU
holding recently used page-table entries. A **TLB hit** translates instantly;
a **miss** pays for a page-table walk in RAM (one access per table level)
plus the data access itself.

## Effective access time

Let h = hit ratio, m = memory access time, and ignore the TLB's own lookup
time for a first approximation. A hit costs one memory access; a miss costs
two (page table, then data):

```
EAT = h × m + (1 − h) × 2m
```

**Worked example:** h = 90%, m = 100 ns → EAT = 0.9 × 100 + 0.1 × 200 =
90 + 20 = **110 ns**. Including a TLB lookup time t: hit costs t + m, miss
costs t + 2m (single-level table).

## Why it matters

Hit ratios in practice sit around 95–99%, so translation overhead stays near
zero — the TLB is what makes paging affordable. Each extra page-table level
adds one more memory access to the miss penalty, which is another reason
architectures keep tables shallow. On context switches the TLB is flushed
(or tagged with an **ASID** — address-space identifier — so entries from
different processes can coexist without confusion).
""",
        order_index=8,
        estimated_minutes=30,
    ),
]


# ---------------------------------------------------------------------------
# QUESTIONS
# ---------------------------------------------------------------------------

QUESTIONS = [
    # ==================== M3-L1: Race Conditions ====================
    _mkq("os-m3-l1-q1", "os-m3-l1", "synchronization", 3,
         "Two threads run at the same time and the final result of the program changes depending on which thread runs first. What is this called?",
         ["A race condition", "A deadlock", "Thrashing", "A page fault"], 0,
         "A race condition is when the outcome depends on the uncontrolled order (timing) of concurrent execution. Deadlock is threads stuck waiting on each other, while thrashing and page faults are memory-management phenomena.",
         ["tcs", "infosys"]),
    _mkq("os-m3-l1-q2", "os-m3-l1", "synchronization", 3,
         "The statement `counter++` is NOT atomic because:",
         ["It compiles to separate load, increment, and store instructions",
          "The CPU cannot add numbers",
          "It needs a page table entry",
          "It always causes a deadlock"], 0,
         "In machine code counter++ becomes load → add → store. Between these instructions another thread (or an interrupt) can interleave and read the same stale value, which is exactly what creates the race.",
         ["wipro", "tcs"]),
    _mkq("os-m3-l1-q3", "os-m3-l1", "synchronization", 4,
         "`counter` starts at 5. Process P1 and process P2 each execute `counter++` once, concurrently. Which final values are possible?",
         ["Only 7", "Only 6", "Both 6 and 7 are possible", "Any value between 5 and 7"], 2,
         "If the two increments run serially with no interleave, both updates survive and the result is 7. If both load 5 before either stores, one update is lost and the result is 6. The interleaving decides, so both 6 and 7 are possible.",
         ["amazon", "tcs"]),
    _mkq("os-m3-l1-q4", "os-m3-l1", "synchronization", 5,
         "A shared variable is updated by 100 threads, each adding 1 exactly once. The programmer expected 100 but the program prints 97. The best explanation is:",
         ["A race condition caused lost updates",
          "The CPU skipped three additions",
          "A deadlock stopped three threads",
          "Integer overflow"], 0,
         "Lost updates happen when two threads load the same value and store back nearly identical results, so some increments vanish. This is the classic symptom of a data race on an unprotected counter — a deadlock would hang, not print a smaller number.",
         ["amazon", "microsoft"]),
    _mkq("os-m3-l1-q5", "os-m3-l1", "synchronization", 6,
         "Which of the following guarantees that a single machine instruction updating shared memory is free from races?",
         ["That the instruction is atomic in hardware (e.g. test_and_set)",
          "That the variable is declared volatile",
          "That the program has only one thread per core",
          "That interrupts are rare"], 0,
         "Only a hardware-guaranteed atomic instruction executes indivisibly from every other CPU's point of view. volatile only stops compiler caching, threads on different cores still race, and rare interrupts can still interleave at the worst moment.",
         ["google", "microsoft"]),
    _mkq("os-m3-l1-q6", "os-m3-l1", "synchronization", 7,
         "On a single-CPU system, a race on a shared variable can still occur because:",
         ["A timer interrupt can switch processes in the middle of a non-atomic update",
          "Two instructions truly execute at the same instant",
          "The cache makes all variables private",
          "Single-CPU systems cannot run two processes"], 0,
         "True parallelism is impossible on one CPU, but preemption is not: a timer interrupt can suspend a process between the load and the store of counter++, and the incoming process then modifies the half-updated state. That interleaving is enough for a race.",
         ["google", "amazon"]),
    # ==================== M3-L2: Critical Section Requirements ====================
    _mkq("os-m3-l2-q1", "os-m3-l2", "synchronization", 3,
         "Mutual exclusion means:",
         ["If one process is in its critical section, no other may be in theirs",
          "Every process must enter the critical section eventually",
          "Waiting time is bounded",
          "Critical sections must be short"], 0,
         "Mutual exclusion is the core safety property: at most one process inside its critical section at a time. Eventual entry relates to liveness, bounded waiting is a separate fairness requirement, and length is a performance concern.",
         ["tcs", "infosys"]),
    _mkq("os-m3-l2-q2", "os-m3-l2", "synchronization", 4,
         "The 'progress' requirement says:",
         ["A process outside its critical section must not block others from entering theirs",
          "Every waiting process enters within a fixed time",
          "Only one process may run at a time",
          "The critical section must finish quickly"], 0,
         "Progress means the decision about who enters next cannot be postponed indefinitely, and crucially a process stuck in its remainder section must not prevent others from entering. It is about not blocking, not about time bounds — that is bounded waiting.",
         ["wipro", "accenture"]),
    _mkq("os-m3-l2-q3", "os-m3-l2", "synchronization", 4,
         "Bounded waiting means:",
         ["There is a limit on how many times other processes can enter before a waiting process gets its turn",
          "The critical section has a maximum length",
          "A process waits at most one context switch",
          "Waiting processes consume no CPU"], 0,
         "Bounded waiting is the fairness property: after a process requests entry, only a bounded number of other processes may enter before it does. It rules out starvation of a process that keeps losing the race to enter.",
         ["infosys", "tcs"]),
    _mkq("os-m3-l2-q4", "os-m3-l2", "synchronization", 5,
         "Two processes use strict alternation: a shared `turn` variable forces P0, P1, P0, P1... entry order. Which requirement does this violate?",
         ["Progress", "Mutual exclusion", "Bounded waiting", "None — it is a perfect solution"], 0,
         "Mutual exclusion holds and bounded waiting holds, but progress is violated: if P0 idles in its remainder section, P1 waits forever for a turn that never matters. A process outside its critical section is blocking another.",
         ["amazon", "google"]),
    _mkq("os-m3-l2-q5", "os-m3-l2", "synchronization", 6,
         "A proposed solution keeps a boolean `interested[i]` per process. P0 sets interested[0]=true, then waits while interested[1] is true. If P1 crashes (never runs again) while interested[1] is true, P0 waits forever. This violates:",
         ["Progress", "Mutual exclusion", "Bounded waiting", "Atomicity"], 0,
         "P1 is effectively stuck in its non-critical section forever, yet it blocks P0 from entering. The progress requirement explicitly forbids a process outside its critical section from blocking others.",
         ["microsoft", "google"]),
    _mkq("os-m3-l2-q6", "os-m3-l2", "synchronization", 7,
         "Peterson's solution satisfies bounded waiting because:",
         ["Once a process yields the turn, the other process can enter at most once before it",
          "The critical section is very short",
          "It uses a hardware atomic instruction",
          "It disables interrupts"], 0,
         "In Peterson's algorithm, when Pi wants to enter it sets flag[i]=true and turn=j. If Pj is also interested, Pj enters at most once — when done it must set the turn back — so Pi waits for at most one critical-section entry. No hardware atomics or interrupt tricks are involved.",
         ["google", "amazon"]),
    # ==================== M3-L3: Peterson's & Hardware ====================
    _mkq("os-m3-l3-q1", "os-m3-l3", "synchronization", 4,
         "Peterson's solution is designed for:",
         ["Exactly two processes", "Any number of processes", "Only kernel threads", "Only single-CPU systems"], 0,
         "The classic Peterson's algorithm coordinates two processes using the shared variables flag[2] and turn. Extensions like the tournament algorithm generalize it to n processes, but the textbook solution is two-process.",
         ["tcs", "infosys"]),
    _mkq("os-m3-l3-q2", "os-m3-l3", "synchronization", 4,
         "The hardware instruction test_and_set(&lock):",
         ["Atomically sets lock to true and returns its old value",
          "Sets lock to false after a delay",
          "Tests the lock without modifying it",
          "Disables interrupts and returns"], 0,
         "test_and_set is indivisible: it writes true into the memory word and returns what was there before, as one uninterruptible hardware operation. Seeing false returned means you acquired the lock; true means someone else holds it.",
         ["wipro", "accenture"]),
    _mkq("os-m3-l3-q3", "os-m3-l3", "synchronization", 5,
         "In Peterson's solution, process Pi sets flag[i] = true and turn = j before entering. The flag[i] = true means:",
         ["Pi wants to enter its critical section",
          "Pi is inside its critical section",
          "Pj is inside its critical section",
          "Pi gives up its turn"], 0,
         "flag[i] signals intent: 'I want in.' The wait loop (while flag[j] && turn == j) then lets Pi in if Pj is not interested, or if Pj politely yielded the turn. Intent plus turn-taking together give mutual exclusion with progress.",
         ["infosys", "tcs"]),
    _mkq("os-m3-l3-q4", "os-m3-l3", "synchronization", 6,
         "A spinlock built on test_and_set avoids races fundamentally because:",
         ["The read-and-write happen as one indivisible hardware operation",
          "Spinning is faster than blocking",
          "The compiler reorders the loop safely",
          "Locks are stored in registers"], 0,
         "The race on a plain boolean lock comes from the gap between checking the lock and setting it. test_and_set closes that gap in hardware — no other core can slip an operation between the read and the write, so two CPUs can never both believe they acquired it.",
         ["amazon", "microsoft"]),
    _mkq("os-m3-l3-q5", "os-m3-l3", "synchronization", 7,
         "compare_and_swap(&x, expected, new) atomically sets x to new only if x equals expected, and reports success. A lock acquire using CAS typically:",
         ["Retries in a loop until the swap succeeds",
          "Succeeds on the first try always",
          "Blocks the process in the kernel",
          "Requires disabling interrupts"], 0,
         "CAS returns whether the swap happened, so acquisition is written as while(!compare_and_swap(&lock, 0, 1)) — a spin loop that retries until this CPU wins the race. Like test_and_set it is a busy-wait construction done entirely in user space.",
         ["google", "amazon"]),
    _mkq("os-m3-l3-q6", "os-m3-l3", "synchronization", 8,
         "Peterson's solution is correct on paper but can fail on a modern multicore CPU unless memory barriers are used, because:",
         ["The CPU/compiler may reorder the flag and turn writes so the other core sees them out of order",
          "Modern CPUs cannot run two processes",
          "Peterson's needs a GPU",
          "Flags must be stored on disk"], 0,
         "Peterson's correctness assumes sequential consistency — every core sees memory operations in program order. Real CPUs and compilers reorder independent writes for speed, so a core might observe turn=j before flag[i]=true, breaking the protocol. Memory barriers restore the required ordering.",
         ["google", "microsoft"]),
    # ==================== M3-L4: Mutex & Spinlocks ====================
    _mkq("os-m3-l4-q1", "os-m3-l4", "synchronization", 3,
         "When a thread calls acquire() on a mutex that is already locked, it:",
         ["Waits (blocks) until the mutex is released",
          "Crashes the program",
          "Skips the critical section",
          "Releases the mutex itself"], 0,
         "That is the contract of a mutex: acquire() on a held lock puts the caller to sleep until the holder calls release(). It never crashes, never skips the protected code, and only the holder should release.",
         ["tcs", "infosys"]),
    _mkq("os-m3-l4-q2", "os-m3-l4", "synchronization", 4,
         "The key difference between a spinlock and a mutex is:",
         ["A spinlock busy-waits in a loop; a mutex blocks the waiting thread",
          "A spinlock can be held by two threads",
          "A mutex cannot protect shared data",
          "Spinlocks are implemented in Python"], 0,
         "Both give mutual exclusion, but the waiting strategy differs: a spinlock loops testing the lock (burning CPU), while a mutex deschedules the waiter so the CPU can do other work.",
         ["wipro", "accenture"]),
    _mkq("os-m3-l4-q3", "os-m3-l4", "synchronization", 5,
         "Busy-waiting (spinning) is acceptable when:",
         ["Critical sections are short and the machine has multiple CPUs",
          "Critical sections are long and there is one CPU",
          "The lock is always contended",
          "Threads never sleep"], 0,
         "Spinning pays off only if the wait is brief (short critical section) and the holder can actually run concurrently to release it (another CPU). On a single CPU, spinning while the holder waits for this CPU is pure waste — blocking wins.",
         ["amazon", "google"]),
    _mkq("os-m3-l4-q4", "os-m3-l4", "synchronization", 5,
         "Which acquire/release usage is correct?",
         ["acquire(); /* critical section */ release(); — always paired, even on error paths",
          "acquire(); acquire(); release();",
          "release(); /* critical section */ acquire();",
          "Only call acquire(); release is optional"], 0,
         "Every acquire must be matched by exactly one release, including exception and error paths (hence try/finally or RAII guards). Double-acquire deadlocks a non-recursive mutex, reversed order protects nothing, and a missing release locks everyone out forever.",
         ["infosys", "tcs"]),
    _mkq("os-m3-l4-q5", "os-m3-l4", "synchronization", 6,
         "On a single-CPU system, a high-priority thread spinning on a lock held by a ready lower-priority thread causes:",
         ["Priority inversion — the spinner never yields so the holder never runs",
          "A page fault storm",
          "Automatic deadlock detection",
          "Faster lock handoff"], 0,
         "The spinning thread burns the only CPU, so the lower-priority holder never gets scheduled to release the lock — a classic priority-inversion livelock. On a single CPU, spinning is harmful whenever the holder cannot run concurrently; blocking lets the holder proceed.",
         ["microsoft", "google"]),
    _mkq("os-m3-l4-q6", "os-m3-l4", "synchronization", 7,
         "An adaptive mutex spins briefly and then blocks. This design is motivated by:",
         ["Avoiding a costly context switch when the wait is very short, while not wasting CPU on long waits",
          "Making deadlocks impossible",
          "Removing the need for atomic instructions",
          "Guaranteeing bounded waiting"], 0,
         "A context switch costs microseconds; if the holder releases within a few spins, spinning was cheaper than sleeping. If the lock stays held, continued spinning wastes the CPU, so the mutex falls back to blocking. It is a performance hybrid, not a correctness fix.",
         ["google", "amazon"]),
    # ==================== M3-L5: Semaphores ====================
    _mkq("os-m3-l5-q1", "os-m3-l5", "synchronization", 3,
         "For a semaphore S, wait(S) and signal(S) do:",
         ["wait decrements S (blocking if needed); signal increments S",
          "wait increments S; signal decrements S",
          "Both increment S",
          "Both block the caller"], 0,
         "The classic P/V operations: wait (P) tries to take a unit — decrementing, and blocking if S is already 0; signal (V) returns a unit by incrementing, possibly waking a waiter. They are inverses of each other.",
         ["tcs", "infosys"]),
    _mkq("os-m3-l5-q2", "os-m3-l5", "synchronization", 4,
         "A binary semaphore differs from a mutex mainly in:",
         ["Ownership: any thread may signal a binary semaphore, but only the holder should release a mutex",
          "A binary semaphore allows two holders",
          "A mutex cannot block",
          "Binary semaphores cannot be initialized to 1"], 0,
         "Both are 0/1, but a mutex has an owner — only the thread that locked it may unlock it. A binary semaphore is just a counter; any thread can signal it, which is more flexible but also easier to misuse.",
         ["wipro", "accenture"]),
    _mkq("os-m3-l5-q3", "os-m3-l5", "synchronization", 4,
         "A counting semaphore guarding 5 identical printers should be initialized to:",
         ["5", "1", "0", "-5"], 0,
         "A counting semaphore is initialized to the number of available resource units. Each wait() takes one printer (5 to 4 to ...), each signal() returns one. Initializing to 1 would serialize access to a single printer; 0 would block everyone forever.",
         ["infosys", "tcs"]),
    _mkq("os-m3-l5-q4", "os-m3-l5", "synchronization", 5,
         "S is a binary semaphore initialized to 1. A thread executes wait(S); wait(S); — the second wait:",
         ["Blocks, because S is now 0",
          "Succeeds, because binary semaphores are re-entrant",
          "Crashes the OS",
          "Increments S back to 1"], 0,
         "The first wait decrements 1 to 0. The second wait finds S=0 and blocks, since a non-recursive binary semaphore has no notion of ownership. This is why acquiring the same lock twice without release deadlocks the thread.",
         ["amazon", "tcs"]),
    _mkq("os-m3-l5-q5", "os-m3-l5", "synchronization", 6,
         "In the bounded-buffer producer-consumer, the correct producer order is wait(empty); wait(mutex); ... signal(mutex); signal(full);. If a student writes wait(mutex); wait(empty); instead, what can happen?",
         ["Deadlock: the producer can hold the mutex while blocked on a full buffer, freezing the consumer",
          "A race on the buffer",
          "The buffer overflows",
          "Nothing — the order does not matter"], 0,
         "With a full buffer, the producer blocks inside wait(empty) while still holding mutex. The consumer needs mutex to remove an item and signal empty — but mutex is held. Circular waiting: deadlock. Taking empty first guarantees a free slot exists before grabbing the mutex.",
         ["google", "amazon"]),
    _mkq("os-m3-l5-q6", "os-m3-l5", "synchronization", 7,
         "A semaphore is implemented with block/wakeup (no busy waiting). When three threads are blocked in wait(S), the value of S is:",
         ["-3", "0", "3", "Undefined"], 0,
         "In the blocking implementation, wait() decrements first and blocks if the result is negative, so S = -(number of waiting threads) = -3. signal() increments and wakes one waiter when the result is <= 0. The negative value conveniently counts the wait queue.",
         ["microsoft", "google"]),
    # ==================== M3-L6: Classic Problems ====================
    _mkq("os-m3-l6-q1", "os-m3-l6", "synchronization", 4,
         "In the bounded-buffer (producer-consumer) problem with a buffer of size N, the producer must wait when:",
         ["The buffer is full (all N slots occupied)",
          "The buffer is empty",
          "A consumer is running",
          "The mutex is 0"], 0,
         "The producer's constraint is 'no free slot': it waits on the empty semaphore when the count of free slots is 0 (buffer full). Waiting on an empty buffer is the consumer's problem; the mutex only serializes the actual insert.",
         ["tcs", "infosys"]),
    _mkq("os-m3-l6-q2", "os-m3-l6", "synchronization", 4,
         "The readers-writers problem requires:",
         ["Many readers may read simultaneously, but a writer needs exclusive access",
          "Only one reader at a time",
          "Writers may write while readers read",
          "Readers and writers take turns strictly"], 0,
         "Reading is non-mutating, so concurrent readers are safe. Writing mutates state, so a writer must exclude all readers and other writers. Any scheme allowing a writer alongside readers risks torn, inconsistent reads.",
         ["wipro", "accenture"]),
    _mkq("os-m3-l6-q3", "os-m3-l6", "synchronization", 5,
         "In the dining-philosophers problem with 5 philosophers and 5 chopsticks, deadlock occurs when:",
         ["Every philosopher picks up the left chopstick at the same time and then waits for the right one",
          "One philosopher eats alone",
          "A philosopher thinks too long",
          "Chopsticks are numbered"], 0,
         "If all five grab their left chopstick simultaneously, each holds one and waits for the right — which is held by the neighbor. That is circular wait with all four Coffman conditions, so nobody ever eats. Numbering chopsticks is actually a fix, not the problem.",
         ["amazon", "tcs"]),
    _mkq("os-m3-l6-q4", "os-m3-l6", "synchronization", 6,
         "For a bounded buffer of size N, the semaphores are initialized as:",
         ["mutex = 1, empty = N, full = 0",
          "mutex = 0, empty = 0, full = N",
          "mutex = N, empty = 1, full = 1",
          "mutex = 1, empty = 0, full = N"], 0,
         "mutex=1 serializes buffer access; empty=N counts free slots (initially all N are free); full=0 counts filled slots (initially none). The producer waits on empty and signals full; the consumer does the reverse. Swapping empty and full would block consumers forever.",
         ["google", "microsoft"]),
    _mkq("os-m3-l6-q5", "os-m3-l6", "synchronization", 7,
         "The 'first' readers-writers solution (readers preferred) can starve writers because:",
         ["A continuous stream of arriving readers keeps readcount > 0, so the writer's wait never ends",
          "Writers are slower than readers",
          "The mutex is unfair",
          "Readers hold the writelock"], 0,
         "In the first solution the first reader locks out writers and the last reader lets them in — but if new readers keep arriving before readcount hits zero, the writer waits indefinitely. Starvation comes from the arrival pattern, not from speed or mutex fairness.",
         ["google", "amazon"]),
    _mkq("os-m3-l6-q6", "os-m3-l6", "synchronization", 7,
         "A system has 4 identical disk drives shared by processes. The most natural primitive to manage them is:",
         ["A counting semaphore initialized to 4",
          "A binary semaphore initialized to 1",
          "A mutex per process",
          "Peterson's solution"], 0,
         "Identical interchangeable resources map exactly to a counting semaphore whose initial value equals the resource count (4). A binary semaphore or mutex would allow only one drive at a time, wasting three drives; Peterson's is a two-process mutual-exclusion protocol, not a resource counter.",
         ["microsoft", "accenture"]),
    # ==================== M3-L7: Coffman Conditions ====================
    _mkq("os-m3-l7-q1", "os-m3-l7", "synchronization", 4,
         "Deadlock is possible only if all four Coffman conditions hold. They are:",
         ["Mutual exclusion, hold and wait, no preemption, circular wait",
          "Starvation, livelock, thrashing, paging",
          "Mutual exclusion, preemption, sharing, waiting",
          "Priority, scheduling, blocking, signaling"], 0,
         "The four necessary conditions are mutual exclusion (non-sharable resources), hold and wait (holding resources while requesting more), no preemption (resources cannot be forcibly taken), and circular wait (a cycle of processes each waiting on the next). All four must hold simultaneously for deadlock.",
         ["tcs", "infosys"]),
    _mkq("os-m3-l7-q2", "os-m3-l7", "synchronization", 4,
         "In the dining-philosophers deadlock, 'circular wait' means:",
         ["Each philosopher waits for a chopstick held by the next philosopher, forming a cycle",
          "Philosophers eat in a circle",
          "Chopsticks are passed around",
          "Each philosopher waits for the same single chopstick"], 0,
         "Circular wait is a cycle in the wait-for relation: philosopher i holds chopstick i and waits for chopstick i+1 held by philosopher i+1, all the way around. Sitting in a circle is just seating; the wait cycle is the deadly structure.",
         ["wipro", "tcs"]),
    _mkq("os-m3-l7-q3", "os-m3-l7", "synchronization", 5,
         "A philosopher holding one chopstick while waiting for the second demonstrates:",
         ["Hold and wait", "No preemption", "Mutual exclusion", "Circular wait"], 0,
         "Hold and wait means a process holds allocated resources while requesting additional ones. (No preemption is that nobody can snatch the chopstick; mutual exclusion is that a chopstick cannot be shared; circular wait needs the whole cycle, not one philosopher.)",
         ["infosys", "accenture"]),
    _mkq("os-m3-l7-q4", "os-m3-l7", "synchronization", 6,
         "'A resource cannot be forcibly taken away from the process holding it' is the:",
         ["No-preemption condition", "Mutual-exclusion condition", "Hold-and-wait condition", "Progress requirement"], 0,
         "No preemption means the OS will not snatch a resource from its holder — it must be released voluntarily. Mutual exclusion is about non-sharability, hold-and-wait is about requesting while holding, and progress is a critical-section liveness property unrelated to deadlock.",
         ["tcs", "wipro"]),
    _mkq("os-m3-l7-q5", "os-m3-l7", "synchronization", 7,
         "Numbering the chopsticks and forcing every philosopher to pick up the lower-numbered one first breaks which condition?",
         ["Circular wait", "Mutual exclusion", "Hold and wait", "No preemption"], 0,
         "A global ordering on resources makes a wait cycle impossible: in any cycle, some philosopher would have to wait for a lower-numbered chopstick while holding a higher one, which the rule forbids. The other three conditions still hold — breaking just one is enough to make deadlock impossible.",
         ["amazon", "google"]),
    _mkq("os-m3-l7-q6", "os-m3-l7", "synchronization", 8,
         "If a system guarantees that at least one Coffman condition NEVER holds, then:",
         ["Deadlock is impossible in that system",
          "Deadlock is still possible but rare",
          "Starvation becomes impossible too",
          "Livelock is impossible"], 0,
         "The four conditions are jointly necessary — deadlock requires all four simultaneously. Negating any one (allowing preemption, imposing a resource ordering) removes the possibility entirely. Starvation and livelock are separate liveness issues and can still occur.",
         ["google", "microsoft"]),
    # ==================== M3-L8: Deadlock Handling ====================
    _mkq("os-m3-l8-q1", "os-m3-l8", "synchronization", 4,
         "Deadlock prevention differs from deadlock avoidance in that prevention:",
         ["Designs the system so at least one Coffman condition can never hold",
          "Detects cycles at runtime",
          "Lets deadlock happen and then recovers",
          "Uses the Banker's algorithm"], 0,
         "Prevention attacks the conditions structurally (for example, require all resources upfront to kill hold-and-wait). Avoidance (the Banker's algorithm) allows the conditions but carefully grants requests to stay in safe states; detection lets deadlock occur and then finds and breaks it.",
         ["tcs", "infosys"]),
    _mkq("os-m3-l8-q2", "os-m3-l8", "synchronization", 5,
         "The Banker's algorithm is a technique for:",
         ["Deadlock avoidance", "Deadlock prevention", "Deadlock detection", "Deadlock recovery"], 0,
         "The Banker's algorithm grants or denies each resource request based on whether the resulting state is safe — the textbook avoidance strategy. Prevention restructures the rules; detection looks for existing cycles; recovery kills or rolls back processes.",
         ["wipro", "accenture"]),
    _mkq("os-m3-l8-q3", "os-m3-l8", "synchronization", 6,
         "Using the lesson's tables: Max[P2] = (9, 0, 2) and Allocation[P2] = (3, 0, 2). The Need row for P2 is:",
         ["(6, 0, 0)", "(12, 0, 4)", "(3, 0, 2)", "(6, 0, 2)"], 0,
         "Need = Max - Allocation = (9-3, 0-0, 2-2) = (6, 0, 0). P2 may still request up to 6 more units of resource A and nothing of B or C.",
         ["amazon", "tcs"]),
    _mkq("os-m3-l8-q4", "os-m3-l8", "synchronization", 7,
         "Using the lesson's example: Available = (3, 3, 2) and Allocation[P1] = (2, 0, 0). When the safety algorithm finishes P1, the new Available is:",
         ["(5, 3, 2)", "(3, 3, 2)", "(1, 3, 2)", "(5, 5, 4)"], 0,
         "A finished process releases everything it holds: Available = (3,3,2) + Allocation[P1] = (3+2, 3+0, 2+0) = (5, 3, 2). This reclaimed resource is what lets the safety check proceed to P3 next.",
         ["google", "amazon"]),
    _mkq("os-m3-l8-q5", "os-m3-l8", "synchronization", 8,
         "Which of the following is a valid safe sequence for the lesson's example (Available = (3, 3, 2))?",
         ["P1, P3, P4, P0, P2", "P0, P1, P2, P3, P4", "P2, P0, P1, P3, P4", "P4, P3, P1, P0, P2"], 0,
         "Trace it: P1 needs (1,2,2) <= (3,3,2) and releases to (5,3,2); P3 needs (0,1,1) -> (7,4,3); P4 needs (4,3,1) -> (7,4,5); P0 needs (7,4,3) -> (7,5,5); P2 needs (6,0,0) fits. Every other option starts with a process whose Need exceeds (3,3,2): P0 needs (7,4,3), P2 needs (6,0,0), P4 needs (4,3,1).",
         ["microsoft", "google"]),
    _mkq("os-m3-l8-q6", "os-m3-l8", "synchronization", 8,
         "P1 (Need = (1, 2, 2)) requests (1, 0, 2) when Available = (3, 3, 2). Should the OS grant it?",
         ["Yes — the request is within Need and Available, and the resulting state is safe",
          "No — it exceeds P1's Need",
          "No — it exceeds Available",
          "No — granting any request is unsafe"], 0,
         "The request passes both pre-checks: (1,0,2) <= Need (1,2,2) and <= Available (3,3,2). Tentatively granting gives Available (2,3,0), from which the safety algorithm still completes (P1 -> P3 -> P4 -> P0 -> P2), so the state stays safe and the request is granted.",
         ["amazon", "google"]),
    # ==================== M4-L1: Contiguous Allocation ====================
    _mkq("os-m4-l1-q1", "os-m4-l1", "memory-management", 3,
         "Internal fragmentation is:",
         ["Wasted space inside an allocated partition that the process cannot use",
          "Wasted space scattered between partitions",
          "A corrupted page table",
          "Disk fragmentation"], 0,
         "With fixed-size partitions, a process smaller than its partition leaves unusable slack inside the allocation — internal to the partition. Scattered free holes between allocations are external fragmentation.",
         ["tcs", "infosys"]),
    _mkq("os-m4-l1-q2", "os-m4-l1", "memory-management", 3,
         "External fragmentation is:",
         ["Free memory split into small non-contiguous holes, none big enough for a waiting process",
          "Wasted space inside a process's own partition",
          "Fragmentation of the disk only",
          "A full memory with no free space"], 0,
         "External fragmentation means plenty of total free memory exists, but it is chopped into scattered holes between allocated blocks, so a large process still cannot fit. Compaction — shuffling processes together — is the classic cure.",
         ["wipro", "tcs"]),
    _mkq("os-m4-l1-q3", "os-m4-l1", "memory-management", 4,
         "Fixed partitions suffer mainly from ____, while variable partitions suffer mainly from ____.",
         ["Internal fragmentation; external fragmentation",
          "External fragmentation; internal fragmentation",
          "Paging; segmentation",
          "Thrashing; Belady's anomaly"], 0,
         "Fixed partitions waste space inside each oversized slot (internal). Variable partitions fit each process exactly, so no internal waste — but over time the free space shatters into small scattered holes (external).",
         ["infosys", "accenture"]),
    _mkq("os-m4-l1-q4", "os-m4-l1", "memory-management", 5,
         "Which allocation strategy tends to leave the largest leftover holes?",
         ["Worst fit", "Best fit", "First fit", "Next fit"], 0,
         "Worst fit deliberately places each process in the largest available hole, leaving behind the largest possible remainder — the idea being the leftover stays usable. Best fit leaves tiny slivers; first fit is fast and decent in practice.",
         ["amazon", "tcs"]),
    _mkq("os-m4-l1-q5", "os-m4-l1", "memory-management", 6,
         "Compaction reduces external fragmentation by:",
         ["Moving allocated processes together so free space merges into one large hole",
          "Splitting processes into pages",
          "Compressing process data",
          "Killing waiting processes"], 0,
         "Compaction relocates every allocated block toward one end of memory, coalescing all the scattered free holes into a single contiguous region. It is expensive — everything moves — which is one reason paging replaced it.",
         ["google", "microsoft"]),
    _mkq("os-m4-l1-q6", "os-m4-l1", "memory-management", 7,
         "A system uses fixed partitions of 8 KB. Processes of sizes 3, 5, 7, 2 KB arrive, one per partition. Total internal fragmentation is:",
         ["15 KB", "8 KB", "23 KB", "17 KB"], 0,
         "Each process wastes partition minus size: (8-3) + (8-5) + (8-7) + (8-2) = 5 + 3 + 1 + 6 = 15 KB of unusable slack inside the four partitions.",
         ["amazon", "google"]),
    # ==================== M4-L2: Paging Basics ====================
    _mkq("os-m4-l2-q1", "os-m4-l2", "memory-management", 3,
         "In paging, a 'page' is ____ and a 'frame' is ____.",
         ["A fixed-size block of a process's logical memory; a fixed-size block of physical memory",
          "A variable-size segment; a disk block",
          "A page-table entry; a TLB entry",
          "Physical memory; logical memory"], 0,
         "Pages and frames are the same size; pages live in the process's logical address space, frames are the slots in physical RAM. The page table maps each page to the frame currently holding it.",
         ["tcs", "infosys"]),
    _mkq("os-m4-l2-q2", "os-m4-l2", "memory-management", 4,
         "Page size is 1024 bytes. Logical address 3012 lies in which page, at what offset?",
         ["Page 2, offset 964", "Page 3, offset 12", "Page 2, offset 1012", "Page 3012, offset 0"], 0,
         "Page number = 3012 / 1024 = 2 (integer division; 2 x 1024 = 2048), offset = 3012 - 2048 = 964. The offset always fits within one page (0 to 1023 here).",
         ["wipro", "accenture"]),
    _mkq("os-m4-l2-q3", "os-m4-l2", "memory-management", 4,
         "A 16-bit logical address with 4 KB pages splits into:",
         ["4 bits page number, 12 bits offset",
          "12 bits page number, 4 bits offset",
          "8 bits page number, 8 bits offset",
          "16 bits page number, 0 bits offset"], 0,
         "4 KB = 2^12 bytes, so 12 bits address every byte within a page (offset). The remaining 16 - 12 = 4 bits select among 2^4 = 16 pages. Offset bits always equal log2(page size).",
         ["infosys", "tcs"]),
    _mkq("os-m4-l2-q4", "os-m4-l2", "memory-management", 5,
         "The page table's job is to:",
         ["Map each page number to the frame number holding it",
          "Store the contents of every page",
          "Count page faults",
          "Translate disk addresses"], 0,
         "A page table is an array indexed by page number; each entry holds the corresponding frame number plus protection and valid bits. The MMU uses it to translate logical to physical addresses on every memory access.",
         ["amazon", "tcs"]),
    _mkq("os-m4-l2-q5", "os-m4-l2", "memory-management", 6,
         "Page size 1024 bytes. The page table maps page 2 to frame 5. Logical address 3012 translates to physical address:",
         ["6084", "5076", "2048", "3012"], 0,
         "From the earlier split: page 2, offset 964. Physical address = frame x page_size + offset = 5 x 1024 + 964 = 5120 + 964 = 6084. The page number is replaced by the frame number; the offset passes through unchanged.",
         ["google", "microsoft"]),
    _mkq("os-m4-l2-q6", "os-m4-l2", "memory-management", 7,
         "Paging eliminates external fragmentation, but the last page of a process is rarely full. On average, internal fragmentation per process is:",
         ["Half a page", "One full page", "Zero — paging has none", "One byte"], 0,
         "The leftover in the last page is uniformly distributed between 0 and page_size, so average waste is page_size / 2. This is why page size is a tradeoff: bigger pages mean bigger average internal waste but smaller page tables.",
         ["google", "amazon"]),
    # ==================== M4-L3: Page Table Structures ====================
    _mkq("os-m4-l3-q1", "os-m4-l3", "memory-management", 4,
         "A hierarchical (multilevel) page table exists to:",
         ["Avoid keeping one giant flat page table in memory for every process",
          "Make addresses longer",
          "Replace the TLB",
          "Store pages on disk"], 0,
         "A 32-bit address space with 4 KB pages needs 2^20 entries (~4 MB) per process as a flat table. Multilevel paging breaks it into smaller tables so only the parts covering actually used address regions need memory.",
         ["tcs", "infosys"]),
    _mkq("os-m4-l3-q2", "os-m4-l3", "memory-management", 5,
         "32-bit addresses, 4 KB pages, 4-byte page-table entries. A single-level page table needs:",
         ["4 MB", "4 KB", "16 MB", "1 MB"], 0,
         "Pages per process = 2^32 / 2^12 = 2^20 (about one million). Each entry 4 bytes gives 2^20 x 4 = 4,194,304 bytes = 4 MB. That per-process cost is exactly why multilevel tables exist.",
         ["amazon", "wipro"]),
    _mkq("os-m4-l3-q3", "os-m4-l3", "memory-management", 5,
         "Hashed page tables are typically used for:",
         ["Address spaces larger than 32 bits",
          "Embedded systems with tiny memory",
          "Processes with exactly one page",
          "Replacing segmentation"], 0,
         "With 64-bit address spaces, even multilevel tables need too many levels. A hashed page table hashes the virtual page number into a bucket chain, so its size scales with memory actually used rather than address-space size.",
         ["google", "microsoft"]),
    _mkq("os-m4-l3-q4", "os-m4-l3", "memory-management", 6,
         "An inverted page table differs from a regular one because:",
         ["It has one entry per physical frame, not one per virtual page",
          "It is stored on disk",
          "It has one entry per process",
          "It cannot be cached in a TLB"], 0,
         "Inverted means one entry per frame, each storing which (process, page) currently occupies that frame. Table size depends on RAM size, not address-space size — great for 64-bit systems — but lookups need hashing and page sharing is awkward.",
         ["amazon", "google"]),
    _mkq("os-m4-l3-q5", "os-m4-l3", "memory-management", 7,
         "With 32-bit addresses, 4 KB pages, and a two-level scheme splitting the page number into 10 + 10 bits:",
         ["Each level has 1024 entries",
          "Each level has 2048 entries",
          "The outer table is 4 MB",
          "Pages are 10 bytes"], 0,
         "10 bits index 2^10 = 1024 entries at each level (10 + 10 + 12 = 32 bits total). The outer table is just 1024 x 4 bytes = 4 KB, and inner tables are allocated only for used regions.",
         ["microsoft", "google"]),
    _mkq("os-m4-l3-q6", "os-m4-l3", "memory-management", 8,
         "In an inverted page table system, two processes sharing one physical page (e.g. shared library) is awkward because:",
         ["One frame entry can record only one (process, page) owner",
          "Shared libraries are forbidden",
          "The TLB cannot cache shared pages",
          "Frames cannot hold code"], 0,
         "Each inverted-table entry describes a single frame's single virtual mapping. A frame shared by two virtual pages needs two virtual-to-physical mappings, which one entry cannot hold — implementations work around it with extra structures, but it is inherently clumsy compared to per-process tables.",
         ["google", "amazon"]),
    # ==================== M4-L4: Segmentation ====================
    _mkq("os-m4-l4-q1", "os-m4-l4", "memory-management", 3,
         "A segment is:",
         ["A logical unit of a program, such as code, data, or stack",
          "A fixed 4 KB block of RAM",
          "A disk partition",
          "A CPU register"], 0,
         "Segmentation mirrors how programmers think: a program is a set of logical units (main code, functions, stack, heap, data), each a segment of variable size. Fixed 4 KB blocks are pages — that is paging, not segmentation.",
         ["tcs", "infosys"]),
    _mkq("os-m4-l4-q2", "os-m4-l4", "memory-management", 4,
         "Each entry of a segment table contains:",
         ["Base address and limit (length) of the segment",
          "Page number and frame number",
          "Two segment names",
          "A disk block address"], 0,
         "Base is where the segment starts in physical memory; limit is how long it is. The MMU checks offset < limit (else trap) and computes physical = base + offset. Page/frame pairs belong to page tables.",
         ["wipro", "accenture"]),
    _mkq("os-m4-l4-q3", "os-m4-l4", "memory-management", 5,
         "A logical address is (segment 2, offset 800). The segment table says segment 2 has limit 600. What happens?",
         ["A trap to the OS — the offset exceeds the segment's limit",
          "Physical address = base + 800 is used",
          "The offset wraps around to 200",
          "The segment is extended to 800"], 0,
         "The limit check is a hardware protection mechanism: offset >= limit means the program touched memory outside its segment, so the MMU traps instead of computing an address. No wraparound or silent extension ever happens.",
         ["amazon", "tcs"]),
    _mkq("os-m4-l4-q4", "os-m4-l4", "memory-management", 5,
         "The fundamental difference between segmentation and paging is:",
         ["Segmentation is visible to the programmer (logical units); paging is invisible (fixed-size blocks)",
          "Segmentation uses fixed-size blocks",
          "Paging is visible to the programmer",
          "They are identical mechanisms"], 0,
         "Segments correspond to meaningful program structure the user and compiler see; pages are arbitrary fixed-size chunks the OS uses behind the scenes. That is why segmentation gives natural protection and sharing per logical unit while paging gives simple, fragmentation-free allocation.",
         ["infosys", "tcs"]),
    _mkq("os-m4-l4-q5", "os-m4-l4", "memory-management", 6,
         "Segmentation's main memory-management drawback is:",
         ["External fragmentation — variable-size segments leave scattered holes",
          "Internal fragmentation inside fixed pages",
          "It needs a TLB for every segment",
          "Segments cannot be protected"], 0,
         "Like variable partitions, variable-size segments placed and removed over time shatter free memory into non-contiguous holes — external fragmentation. Internal fragmentation in fixed pages is paging's issue, and segments absolutely can carry per-segment protection bits.",
         ["google", "microsoft"]),
    _mkq("os-m4-l4-q6", "os-m4-l4", "memory-management", 7,
         "Modern x86 processors combine segmentation with paging. The translation order is:",
         ["Segmentation first (logical to linear), then paging (linear to physical)",
          "Paging first, then segmentation",
          "Both happen simultaneously in one step",
          "Segmentation replaces paging"], 0,
         "The x86 MMU first applies the segment's base+limit to get a linear address, then pages that linear address to physical RAM. Two translation stages in that order — segmentation shapes the programmer's view, paging manages the physical frames.",
         ["google", "amazon"]),
    # ==================== M4-L5: Virtual Memory & Demand Paging ====================
    _mkq("os-m4-l5-q1", "os-m4-l5", "memory-management", 4,
         "Virtual memory's headline benefit is:",
         ["Programs larger than physical RAM can run",
          "RAM becomes faster",
          "Disks become unnecessary",
          "Programs use less CPU"], 0,
         "By keeping only the active pages in RAM and the rest on disk, a process's logical address space can far exceed physical memory size. Nothing about RAM speed, disk removal, or CPU usage changes.",
         ["tcs", "infosys"]),
    _mkq("os-m4-l5-q2", "os-m4-l5", "memory-management", 4,
         "In a page-table entry, the valid/invalid bit tells the MMU:",
         ["Whether the page is currently in physical memory (valid) or not",
          "Whether the page contains code or data",
          "Whether the page is on disk or deleted",
          "The page's priority"], 0,
         "Valid means the frame number in the entry is usable right now; invalid means the page is not resident (either swapped out or never allocated — the OS distinguishes via auxiliary info). An access to an invalid page triggers a page fault.",
         ["wipro", "accenture"]),
    _mkq("os-m4-l5-q3", "os-m4-l5", "memory-management", 5,
         "The correct order of page-fault handling is:",
         ["Trap -> check the access is legal -> find a free frame -> read the page from disk -> update the page table -> restart the instruction",
          "Restart the instruction -> read from disk -> trap",
          "Kill the process -> free all frames",
          "Update the page table -> trap -> read from disk"], 0,
         "The MMU traps; the OS first verifies the address is legal (illegal means terminate the process — the familiar segmentation fault); then it finds or evicts a frame, schedules the disk read, fixes the page table, and restarts the faulting instruction so it executes cleanly this time.",
         ["amazon", "tcs"]),
    _mkq("os-m4-l5-q4", "os-m4-l5", "memory-management", 6,
         "A 'lazy swapper' (demand pager):",
         ["Loads a page into memory only when it is first accessed",
          "Swaps out the entire process at load time",
          "Preloads all pages before the program starts",
          "Never uses the disk"], 0,
         "Lazy means doing work only when forced. Demand paging never brings in a page until a fault demands it, so programs start instantly and pages that are never touched never cost disk I/O. Eager loading would be the opposite.",
         ["google", "microsoft"]),
    _mkq("os-m4-l5-q5", "os-m4-l5", "memory-management", 7,
         "Copy-on-write (used in fork()) means:",
         ["Parent and child initially share the same physical pages read-only; a page is copied only when one of them writes to it",
          "The child gets no memory",
          "All pages are copied immediately at fork",
          "Writes are forbidden after fork"], 0,
         "fork() would be expensive if it copied everything upfront. With copy-on-write, both processes share frames marked read-only; the first write to a shared page faults, and only then does the OS copy that single page and mark it writable-private. Most pages (like code) are never written, so the copy never happens.",
         ["google", "amazon"]),
    _mkq("os-m4-l5-q6", "os-m4-l5", "memory-management", 8,
         "Two processes share a physical page containing library code. In their page tables, the entries for that page:",
         ["Point to the same frame number, typically marked read-only/execute",
          "Must point to different frames",
          "Are marked invalid in one process",
          "Cannot exist — sharing is impossible with paging"], 0,
         "Sharing is just two page-table entries holding the same frame number — one physical copy, two mappings, saving RAM. Marking it non-writable protects the shared code from corruption by either process.",
         ["microsoft", "google"]),
    # ==================== M4-L6: Page Replacement ====================
    _mkq("os-m4-l6-q1", "os-m4-l6", "memory-management", 4,
         "Page replacement is needed when:",
         ["A page fault occurs and no free frame is available",
          "The TLB is full",
          "A process terminates",
          "The disk is full"], 0,
         "On a fault the OS must load the page somewhere; if every frame is occupied, some resident page must be evicted (written back first if dirty) to make room. TLB fullness, process exit, and disk capacity are unrelated triggers.",
         ["tcs", "infosys"]),
    _mkq("os-m4-l6-q2", "os-m4-l6", "memory-management", 5,
         "Reference string 7, 0, 1, 2, 0, 3, 0, 4 with 3 frames using FIFO gives how many page faults?",
         ["7", "6", "8", "9"], 0,
         "Walk it: 7(f), 0(f), 1(f), 2 evicts 7(f), 0 hit, 3 evicts 0(f), 0 evicts 1(f), 4 evicts 2(f) = 7 faults. The two 0s look like hits, but the second 0 arrives after 0 was already evicted — FIFO's blindness to reuse is exactly the point.",
         ["amazon", "wipro"]),
    _mkq("os-m4-l6-q3", "os-m4-l6", "memory-management", 6,
         "Belady's anomaly is demonstrated by reference string 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 with FIFO: 3 frames give 9 faults, 4 frames give 10. This shows:",
         ["More frames can sometimes increase page faults under FIFO",
          "More frames always reduce faults",
          "FIFO is the optimal algorithm",
          "LRU also shows the anomaly"], 0,
         "Belady's anomaly means giving FIFO more frames can counter-intuitively raise faults (9 to 10 here). It happens because FIFO evicts by age, not by future usefulness. Stack algorithms like LRU and Optimal never show this anomaly.",
         ["google", "amazon"]),
    _mkq("os-m4-l6-q4", "os-m4-l6", "memory-management", 7,
         "Reference string 7, 0, 1, 2, 0, 3, 0, 4 with 3 frames using the Optimal algorithm gives:",
         ["6 faults", "7 faults", "5 faults", "8 faults"], 0,
         "Optimal evicts the page used farthest in the future: 7(f), 0(f), 1(f), 2 evicts 7 — never used again (f), 0 hit, 3 evicts 2 — never used again (f), 0 hit, 4 evicts 3 (f) = 6 faults. Optimal needs future knowledge, so it is unrealizable, but it sets the lower bound every real algorithm is measured against.",
         ["microsoft", "google"]),
    _mkq("os-m4-l6-q5", "os-m4-l6", "memory-management", 8,
         "Same string (7, 0, 1, 2, 0, 3, 0, 4), 3 frames, using LRU gives:",
         ["6 faults", "7 faults", "5 faults", "9 faults"], 0,
         "Trace: 7(f), 0(f), 1(f), 2 evicts 7 — least recently used (f), 0 hit, 3 evicts 1 — LRU among {2,0,1} (f), 0 hit, 4 evicts 2 — LRU among {2,3,0} (f) = 6 faults. LRU matches Optimal here because this string's recency pattern happens to predict the future well.",
         ["google", "amazon"]),
    _mkq("os-m4-l6-q6", "os-m4-l6", "memory-management", 9,
         "Reference string 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 with 3 frames using LRU gives:",
         ["10 faults", "9 faults", "8 faults", "12 faults"], 0,
         "Trace: 1(f), 2(f), 3(f), 4 evicts 1(f), 1 evicts 2(f), 2 evicts 3(f), 5 evicts 4(f), 1 hit, 2 hit, 3 evicts 5(f), 4 evicts 1(f), 5 evicts 2(f) = 10 faults. Note LRU (10) does worse than FIFO (9) on this string — no algorithm dominates on every reference string.",
         ["amazon", "google"]),
    # ==================== M4-L7: Thrashing & Working Set ====================
    _mkq("os-m4-l7-q1", "os-m4-l7", "memory-management", 4,
         "Thrashing is:",
         ["The system spending more time paging than executing processes",
          "A disk crash",
          "Rapid context switching between two processes",
          "CPU overheating"], 0,
         "Thrashing is the collapse where nearly every memory access faults, so the CPU sits idle waiting on disk while the pager churns. The fix is reducing the degree of multiprogramming (suspend some processes), not faster context switches.",
         ["tcs", "infosys"]),
    _mkq("os-m4-l7-q2", "os-m4-l7", "memory-management", 4,
         "The most common cause of thrashing is:",
         ["Too high a degree of multiprogramming — processes' needs exceed available frames",
          "Too few processes running",
          "A very large page size",
          "Disabling virtual memory"], 0,
         "When too many processes share RAM, each gets fewer frames than its working set, so every process faults constantly and steals frames from others — a vicious cycle. Fewer processes (or more frames per process) breaks it.",
         ["wipro", "accenture"]),
    _mkq("os-m4-l7-q3", "os-m4-l7", "memory-management", 5,
         "The working set W(t, delta) is:",
         ["The set of pages referenced in the most recent delta time units",
          "All pages of the process",
          "The pages currently on disk",
          "The TLB contents"], 0,
         "The working set is the process's current locality — whatever it touched in the last delta window. It changes as the program moves between phases, and the OS uses it to decide how many frames each process genuinely needs.",
         ["amazon", "tcs"]),
    _mkq("os-m4-l7-q4", "os-m4-l7", "memory-management", 6,
         "Using the working-set model, the OS can detect thrashing when:",
         ["The sum of all processes' working sets exceeds the number of available frames",
          "A single page fault occurs",
          "CPU utilization is 100%",
          "The disk is full"], 0,
         "If the sum of working sets is greater than total frames, the processes physically cannot all keep their working sets resident — faults are inevitable and thrashing follows. The OS responds by suspending (swapping out) a process to shrink demand.",
         ["google", "microsoft"]),
    _mkq("os-m4-l7-q5", "os-m4-l7", "memory-management", 7,
         "Page-fault-frequency (PFF) control works by:",
         ["Giving a process more frames when its fault rate is too high, taking some away when it is too low",
          "Fixing the frame allocation forever",
          "Counting total system faults only",
          "Disabling demand paging"], 0,
         "PFF sets upper and lower bounds on the acceptable fault rate per process: above the upper bound the process is frame-starved, so grant more; below the lower bound it hoards idle frames, so reclaim some. It adapts allocation to each process's actual locality.",
         ["google", "amazon"]),
    _mkq("os-m4-l7-q6", "os-m4-l7", "memory-management", 8,
         "With global page replacement, one process's heavy faulting can:",
         ["Steal frames from well-behaved processes and drag the whole system toward thrashing",
          "Only affect itself",
          "Improve other processes' hit rates",
          "Be prevented by the TLB"], 0,
         "Global replacement lets any process evict any frame, so a looping process can evict everyone else's working sets — its thrashing becomes contagious. Local (per-process) replacement contains the damage, which is why working-set-based schemes prefer it.",
         ["microsoft", "google"]),
    # ==================== M4-L8: TLB ====================
    _mkq("os-m4-l8-q1", "os-m4-l8", "memory-management", 4,
         "The TLB (translation lookaside buffer) is:",
         ["A fast cache of recently used page-table entries",
          "A second page table on disk",
          "A CPU scheduling queue",
          "A type of RAM chip"], 0,
         "The TLB is small, associative, very fast memory inside the MMU holding recent virtual-page to frame translations. A hit avoids the slower page-table walk in RAM; it caches entries, it is not itself a page table.",
         ["tcs", "infosys"]),
    _mkq("os-m4-l8-q2", "os-m4-l8", "memory-management", 5,
         "On a TLB miss, address translation costs:",
         ["Extra memory accesses to walk the page table, then the actual data access",
          "Nothing extra",
          "A disk read always",
          "A context switch"], 0,
         "A miss means consulting the page table in RAM (one access per level) to find the frame, then accessing the data — roughly two memory accesses for a single-level table versus one on a hit. No disk is involved unless the page itself is also not resident.",
         ["wipro", "accenture"]),
    _mkq("os-m4-l8-q3", "os-m4-l8", "memory-management", 5,
         "TLB hit ratio 90%, memory access time 100 ns, TLB lookup negligible. Effective access time is:",
         ["110 ns", "100 ns", "200 ns", "90 ns"], 0,
         "EAT = hit x 1 memory access + miss x 2 memory accesses = 0.9 x 100 + 0.1 x 200 = 90 + 20 = 110 ns. A miss costs double because the page table must be read before the data.",
         ["amazon", "tcs"]),
    _mkq("os-m4-l8-q4", "os-m4-l8", "memory-management", 6,
         "TLB lookup takes 5 ns, memory access 50 ns, hit ratio 80%. EAT is:",
         ["65 ns", "55 ns", "105 ns", "60 ns"], 0,
         "Hit path = 5 + 50 = 55 ns; miss path = 5 + 50 + 50 = 105 ns. EAT = 0.8 x 55 + 0.2 x 105 = 44 + 21 = 65 ns. Including the TLB's own lookup time on both paths is the step most people forget.",
         ["google", "microsoft"]),
    _mkq("os-m4-l8-q5", "os-m4-l8", "memory-management", 7,
         "Memory access time is 100 ns (TLB lookup negligible). What minimum hit ratio keeps EAT at or below 120 ns?",
         ["80%", "90%", "70%", "60%"], 0,
         "EAT = h x 100 + (1-h) x 200 = 200 - 100h <= 120, so 100h >= 80 and h >= 0.8. Below 80% hits, the doubled cost of misses drags the average past 120 ns.",
         ["google", "amazon"]),
    _mkq("os-m4-l8-q6", "os-m4-l8", "memory-management", 8,
         "With a two-level page table, TLB lookup 10 ns, memory access 100 ns, hit ratio 95%. EAT is:",
         ["120 ns", "110 ns", "210 ns", "105 ns"], 0,
         "Hit path = 10 + 100 = 110 ns. Miss path = TLB lookup + two page-table accesses + data access = 10 + 100 + 100 + 100 = 310 ns. EAT = 0.95 x 110 + 0.05 x 310 = 104.5 + 15.5 = 120 ns. Each extra page-table level adds one more memory access to the miss penalty.",
         ["microsoft", "google"]),
]
