"""Seed content: Operating Systems — Modules 1-2 (Processes & Threads, CPU Scheduling).

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

DOMAIN_SLUG = "operating-systems"

MODULES = [
    CurriculumModule(
        id="os-m1",
        domain_slug=DOMAIN_SLUG,
        slug="processes-threads",
        name="Processes & Threads",
        description=(
            "From program on disk to process in memory: the process image, "
            "the PCB, process states, threads vs processes, multithreading "
            "models, context switching, fork/exec, and inter-process communication."
        ),
        order_index=1,
        estimated_days=8,
    ),
    CurriculumModule(
        id="os-m2",
        domain_slug=DOMAIN_SLUG,
        slug="cpu-scheduling",
        name="CPU Scheduling",
        description=(
            "How the OS picks the next process: scheduling criteria and formulas, "
            "FCFS, SJF, SRTF, Round Robin, priority scheduling with aging, and "
            "multilevel (feedback) queues — with hand-computed Gantt charts."
        ),
        order_index=2,
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
# LESSONS — Module 1: Processes & Threads
# ---------------------------------------------------------------------------

LESSONS = [
    CurriculumLesson(
        id="os-m1-l1",
        module_id="os-m1",
        slug="program-vs-process",
        title="Program vs Process",
        content="""A **program** is a passive file sitting on disk — just bytes of machine
instructions and data. A **process** is that program *in execution*: the OS
loads it into memory, gives it its own address space, and starts running its
instructions. One program can spawn many processes at once — open two terminals
running `python` and you have two processes of the same program, each isolated
from the other.

The running program's memory layout is called the **process image**, and it has
distinct segments:

- **Text**: the compiled machine code (read-only).
- **Data**: initialized global and static variables.
- **BSS**: uninitialized globals (zeroed at load time).
- **Heap**: grows upward at runtime via `malloc()`/`new`; holds dynamically
  allocated memory.
- **Stack**: grows downward; holds function call frames — local variables,
  parameters, return addresses.

**Interview tip:** when asked "what happens when you run a program?", trace it:
the loader copies text/data into memory, allocates heap and stack, creates a
PCB, and sets the program counter to `main()`. The difference between program
and process is the difference between a recipe book on a shelf and a chef
actively cooking — state, resources, and momentum.
""",
        order_index=1,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="os-m1-l2",
        module_id="os-m1",
        slug="process-control-block",
        title="Process Control Block (PCB)",
        content="""Every process the OS manages needs a dossier, and that dossier is the
**Process Control Block (PCB)** — a kernel data structure created at process
birth and destroyed at death. When the CPU switches from one process to
another, the PCB is where state is saved and restored; without it,
multitasking is impossible.

A typical PCB holds:

- **Process ID (PID)** — the unique handle (what `ps` shows you).
- **Process state** — new, ready, running, waiting, or terminated.
- **Program counter** — address of the next instruction to execute.
- **CPU registers** — the working values at the moment of interruption.
- **Scheduling info** — priority, pointers into scheduling queues.
- **Memory info** — page-table base pointer, base/limit registers.
- **I/O status** — open files, allocated devices.
- **Accounting** — CPU time used, limits.

PCBs live in **kernel memory**, never in user space — a user process must not
be able to rewrite its own scheduling priority or another process's registers.
That is why even reading your own PID needs a system call.

**Worked intuition:** hit Ctrl+Z on a running program. The OS freezes it
mid-instruction, copies its registers and program counter into its PCB, marks
it stopped, and hands the CPU to your shell. Type `fg`, and the OS does the
reverse — loads the PCB back into the CPU and the program resumes exactly where
it left off, oblivious to the interruption. The PCB is the process's saved
game file.
""",
        order_index=2,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="os-m1-l3",
        module_id="os-m1",
        slug="process-states",
        title="Process States",
        content="""At any instant, a process is in exactly one state. The classic
five-state model:

- **New** — being created (PCB allocated, program loading).
- **Ready** — loaded in memory, waiting only for the CPU.
- **Running** — instructions executing on the CPU right now.
- **Waiting (blocked)** — paused until an event occurs, usually I/O completion.
- **Terminated** — finished; resources being reclaimed.

The transitions are what interviews probe:

- new → ready (admitted), ready → running (**dispatch** by the scheduler)
- running → ready (**preemption** — time quantum expired or a higher-priority
  process arrived)
- running → waiting (the process itself requests I/O)
- waiting → ready (the I/O completes) — note: *never* waiting → running directly
- running → terminated (`exit()`)

Two extra states appear when memory is tight: **suspended ready** and
**suspended blocked** — the process is swapped out to disk. A suspended blocked
process whose I/O finishes becomes suspended ready; it must be swapped back in
before it can run.

**Worked example:** you type in an editor and hit save. The editor was
*running*, issues a disk write, and moves to *waiting*. The scheduler dispatches
your music player (*ready → running*). The disk finishes → the editor moves
*waiting → ready*, and soon gets the CPU again. On a single CPU, only one
process is ever *running* — "multitasking" is the OS flickering processes
between ready and running dozens of times per second.
""",
        order_index=3,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m1-l4",
        module_id="os-m1",
        slug="threads-vs-processes",
        title="Threads vs Processes",
        content="""A **thread** is the smallest unit of CPU scheduling — a single flow of
execution. A traditional process has one thread; a multithreaded process has
several threads running (conceptually) in parallel inside the same process.

Threads of one process **share**: the code section, the data section, and open
files — the whole address space. Each thread keeps only two private things:
its own **stack** (separate call history) and its own **registers / program
counter** (separate "where was I").

This sharing is why threads are **lightweight**: creating a thread needs no new
address space, no page tables, no file-table copies; switching between threads
of the same process skips the expensive memory-management switch that process
switching requires. A web server can juggle thousands of client connections as
threads far more cheaply than as processes.

But sharing is a double-edged sword. One thread's wild pointer can corrupt
another thread's data — there is no memory protection *between* threads. And
because data is shared, threads need synchronization (locks) to avoid race
conditions.

**Interview tip:** "Why not always use threads instead of processes?" Answer
with the trade-off — threads are cheap and share data easily, but one crashing
thread kills the whole process, and shared state invites concurrency bugs.
Processes give you isolation and fault tolerance at the cost of heavier
creation and explicit IPC. Chrome famously uses *processes* per tab for
stability; a game engine uses *threads* per subsystem for speed.
""",
        order_index=4,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m1-l5",
        module_id="os-m1",
        slug="multithreading-models",
        title="Multithreading Models",
        content="""Threads come in two flavors: **user-level threads** (managed by a thread
library in user space — fast to create/switch, no kernel involvement) and
**kernel-level threads** (the OS knows about and schedules them — true
parallelism on multicores, but each operation costs a system call). The
**multithreading model** describes how the two map to each other:

- **Many-to-one**: many user threads multiplexed onto a single kernel thread.
  Thread management is blazing fast and portable — but if one thread makes a
  blocking system call, the *entire process* blocks, and threads can never run
  truly in parallel on multiple cores. (Classic example: Solaris Green Threads.)
- **One-to-one**: each user thread gets its own kernel thread. Blocking one
  thread blocks only that thread, and threads spread across cores — at the cost
  of kernel overhead per thread, which caps how many you can create.
  (Linux, Windows.)
- **Many-to-many**: many user threads multiplexed onto a smaller-or-equal
  number of kernel threads. Developers create as many user threads as they
  like; the kernel schedules a sufficient set of kernel threads. You get
  concurrency without the one-to-one overhead and without many-to-one's
  blocking problem. (The most flexible — and most complex to implement.)

**Interview tip:** if asked "which model does Linux use?", answer **one-to-one**
— every `pthread` you create maps to a kernel-schedulable task. Then add the
trade-off: user-level threading is fast because it avoids mode switches, but
only kernel threads buy you real multicore parallelism. Knowing *why* each
model exists matters more than memorizing names.
""",
        order_index=5,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m1-l6",
        module_id="os-m1",
        slug="context-switching",
        title="Context Switching",
        content="""A **context switch** happens when the CPU stops running one process (or
thread) and starts another: the OS saves the outgoing process's program counter
and registers into its PCB, loads the incoming process's saved state, and
resumes it. From the process's viewpoint, nothing happened — it just continued.

The catch: a context switch does **zero useful work**. Its costs are:

- **Direct**: the save/restore instructions themselves (typically microseconds).
- **Indirect**: the new process finds a "cold" cache and TLB — its data was
  evicted while it was away, so it suffers a burst of cache misses until its
  working set is reloaded.

Do not confuse it with a **mode switch**: when your program makes a system
call, the CPU flips from user mode to kernel mode *but keeps running the same
process* — no PCB save/restore, much cheaper.

**Worked numbers:** suppose a context switch costs 10 microseconds and the
system performs 1,000 switches per second. That is 1,000 × 10 µs = 10 ms of
every second — 1% of the CPU burned on bookkeeping. Now shrink the scheduling
time quantum too far and switches multiply: the CPU spends more time switching
than computing. This is exactly why the Round Robin quantum cannot be tiny —
scheduling policy and context-switch cost are two sides of one trade-off.

**Interview tip:** "Is a context switch expensive?" Answer: the switch itself is
cheap (microseconds), but at high frequency the aggregate cost — plus cache
pollution — is real, which is why OS designers obsess over quantum sizes.
""",
        order_index=6,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m1-l7",
        module_id="os-m1",
        slug="process-creation-termination",
        title="Process Creation & Termination",
        content="""New processes are born from old ones. On Unix, **`fork()`** clones the
calling process: parent and child are near-identical (same code, copied data —
modern systems use copy-on-write so the copy is lazy), but `fork()` returns
the child's PID to the *parent* and `0` to the *child*, letting each know who
it is. **`exec()`** then replaces the current process's entire memory image
with a new program — same PID, brand-new code. The shell runs your commands
with exactly this dance: `fork()` to clone itself, `exec()` in the child to
become `ls`, `wait()` in the parent to pause until `ls` finishes, and `exit()`
in the child to terminate.

Termination has two messy edge cases interviews love:

- **Zombie**: a child that has terminated, but whose parent has not called
  `wait()` yet. The child is dead — no memory, no CPU — but its process-table
  entry (PID + exit status) lingers until the parent collects it.
- **Orphan**: a child whose parent died first. It gets adopted by
  `init`/`systemd` (PID 1), which dutifully `wait()`s on it, so orphans never
  become zombies.

**Interview tip:** "How do you kill a zombie?" Trick question — you cannot kill
what is already dead. You either make the parent call `wait()`, or kill the
*parent*, turning the zombie's siblings into orphans adopted by init, which
reaps them. And if someone asks why the shell uses fork+exec instead of exec
alone: exec alone would *replace the shell itself* — there would be no shell
left to show you the next prompt.
""",
        order_index=7,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m1-l8",
        module_id="os-m1",
        slug="inter-process-communication",
        title="Inter-Process Communication",
        content="""Processes are isolated by design — separate address spaces — so
cooperating processes need **Inter-Process Communication (IPC)**. The two
fundamental approaches:

**Shared memory**: the OS maps the same physical pages into two processes'
address spaces. After setup, processes read/write at full memory speed — the
fastest IPC for bulk data. The price: *no* built-in synchronization. Two
processes writing the same counter can interleave into garbage (a race
condition), so you must add your own locks or semaphores.

**Message passing**: processes exchange messages via kernel-mediated `send()`
and `receive()`. The kernel copies data between address spaces — slower
(system calls + copying), but synchronization comes free: a `receive()` simply
blocks until a message arrives. It also works unchanged across a network
(sockets), where shared memory is impossible.

Common mechanisms: **pipes** (unidirectional byte streams, usually
parent-to-child — this is what `ls | grep x` uses), named pipes/FIFOs,
**message queues**, **sockets**, and **signals** (tiny notifications, not data
transfer).

**Worked trade-off:** a video pipeline moving 4K frames between a capture
process and an encoder wants *shared memory* — copying gigabytes through the
kernel would be wasteful, and the team accepts writing careful synchronization.
A chat server's worker processes, coordinating small control messages, prefer
*message passing* — the volumes are tiny and blocking-receive gives clean
synchronization for free.

**Interview tip:** "Which IPC is fastest?" → shared memory, *but* immediately
add "at the cost of manual synchronization" — interviewers ask the follow-up to
check you know the catch.
""",
        order_index=8,
        estimated_minutes=40,
    ),
]


# ---------------------------------------------------------------------------
# LESSONS — Module 2: CPU Scheduling
# ---------------------------------------------------------------------------

LESSONS += [
    CurriculumLesson(
        id="os-m2-l1",
        module_id="os-m2",
        slug="scheduling-criteria",
        title="Scheduling Criteria",
        content="""When several processes sit in the ready queue, the **CPU scheduler** picks
who runs next. To judge schedulers, the OS community uses five metrics:

- **CPU utilization** — fraction of time the CPU is busy (target: as close to
  100% as practical).
- **Throughput** — processes completed per unit time.
- **Turnaround time** = completion time − arrival time. The wall-clock time
  from submission to done — what a batch user feels.
- **Waiting time** = turnaround time − burst time = total time spent sitting in
  the ready queue. The scheduler's report card.
- **Response time** = time of *first* CPU run − arrival time. What an
  interactive user feels — the delay before the system first reacts.

The classic interview trap is mixing up waiting and turnaround time. Remember:
turnaround includes everything (waiting + execution); waiting excludes the
burst itself.

**Worked example:** a process arrives at t=2, first gets the CPU at t=5,
finishes at t=12, with a CPU burst of 4.

- Response time = 5 − 2 = **3**
- Turnaround = 12 − 2 = **10**
- Waiting = 10 − 4 = **6**

Notice the process "waited" 6 units but its turnaround is 10 — the 4 units of
actual execution count toward turnaround but not waiting.

These metrics conflict: maximizing throughput (favor short jobs) can starve
long ones and wreck their turnaround; minimizing response time (frequent
preemption) adds context-switch overhead that hurts utilization. Every
scheduling algorithm is a stance on these trade-offs — the rest of this module
is a tour of the classic stances.
""",
        order_index=1,
        estimated_minutes=30,
    ),
    CurriculumLesson(
        id="os-m2-l2",
        module_id="os-m2",
        slug="fcfs-scheduling",
        title="FCFS Scheduling",
        content="""**First-Come, First-Served (FCFS)** is the simplest scheduler: run
processes in arrival order, non-preemptively — once a process gets the CPU, it
keeps it until it finishes or blocks.

**Worked example** — three processes arrive: P1 at 0 (burst 24), P2 at 2
(burst 3), P3 at 3 (burst 3). Gantt chart:

    |---- P1 (0-24) ----| P2 (24-27) | P3 (27-30) |

Waiting times: P1 = 0 − 0 = 0; P2 = 24 − 2 = 22; P3 = 27 − 3 = 24.
Average = (0 + 22 + 24) / 3 = **15.33**.

See the problem? Two tiny 3-unit jobs waited ~24 units behind one 24-unit job.
This is the **convoy effect**: short processes (often I/O-bound and
interactive) queue up behind one long CPU-bound process, and average waiting
time balloons.

FCFS is fair in a naive sense — nobody is preempted, arrival order is
respected — and it has zero scheduling overhead. But its average waiting time
is highly sensitive to arrival order: reverse the arrivals (short jobs first)
and the same workload averages a fraction of the wait. Real systems rarely use
pure FCFS for the CPU, though the idea survives inside other schedulers (e.g.,
tie-breaking, or per-queue ordering in Round Robin).

**Interview tip:** when asked for FCFS's disadvantage, do not just say "convoy
effect" — *show* it with the numbers above. Interviewers remember candidates
who compute.
""",
        order_index=2,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m2-l3",
        module_id="os-m2",
        slug="sjf-scheduling",
        title="SJF Scheduling",
        content="""**Shortest-Job-First (SJF)** runs the ready process with the smallest next
CPU burst, non-preemptively. Its claim to fame: for a given set of processes,
**no other non-preemptive schedule gives a lower average waiting time** — it
is provably optimal.

**Worked example:** P1 arrives 0 (burst 5), P2 arrives 1 (burst 3), P3 arrives
2 (burst 2). At t=0 only P1 is ready, so P1 runs 0–5. At t=5, P2 (3) and P3 (2)
wait — P3 is shorter, so P3 runs 5–7, then P2 runs 7–10.

    | P1 (0-5) | P3 (5-7) | P2 (7-10) |

Waiting: P1 = 0, P3 = 5 − 2 = 3, P2 = 7 − 1 = 6 → average **3** (FCFS on the
same data gave 3.33).

The catch: SJF needs to know each burst *in advance*. Real systems **predict**
it with exponential averaging: tau(n+1) = alpha·t(n) + (1−alpha)·tau(n),
blending the last actual burst t(n) with the old prediction tau(n). With
alpha = 0.5, tau(n) = 10, t(n) = 6: next prediction = 0.5×6 + 0.5×10 = **8**.

SJF's dark side is **starvation**: if short processes keep arriving, a long
process may wait forever. SJF is the "optimal but impractical" baseline — its
preemptive sibling (next lesson) fixes the waiting, and aging fixes the
starvation.

**Interview tip:** "Prove SJF is optimal" is a famous question — the intuition
is an exchange argument: if a longer job runs before a shorter one, swapping
them reduces total waiting without harming anything else.
""",
        order_index=3,
        estimated_minutes=35,
    ),
    CurriculumLesson(
        id="os-m2-l4",
        module_id="os-m2",
        slug="srtf-scheduling",
        title="SRTF Scheduling",
        content="""**Shortest-Remaining-Time-First (SRTF)** is SJF made preemptive: whenever
a new process arrives, compare its burst with the *remaining* time of the
running process — if the newcomer is shorter, preempt.

**Worked example:** P1 arrives 0 (burst 6), P2 arrives 1 (burst 3), P3 arrives
2 (burst 1).

- t=0–1: P1 runs (remaining 5).
- t=1: P2 arrives (3 < 5) → preempt. P2 runs 1–2 (remaining 2).
- t=2: P3 arrives (1 < 2) → preempt. P3 runs 2–3, finishes.
- t=3: P2 (remaining 2) vs P1 (remaining 5) → P2 runs 3–5, finishes.
- t=5: P1 runs 5–11, finishes.

    | P1 (0-1) | P2 (1-2) | P3 (2-3) | P2 (3-5) | P1 (5-11) |

Waiting (= turnaround − burst): P1 = 11 − 6 = 5, P2 = (5−1) − 3 = 1,
P3 = (3−2) − 1 = 0 → average **2**, beating non-preemptive schedules.

SRTF gives the minimum possible average waiting time among all schedulers, but
inherits SJF's starvation (a steady stream of short arrivals freezes long jobs
out) and adds preemption overhead — every arrival triggers a comparison and
possibly a context switch.

**Interview tip:** expect "SJF vs SRTF on this workload — compute both." The
method is mechanical: for SRTF, re-evaluate at *every arrival instant*. Draw
the timeline first, then read waiting times off it. Most arithmetic errors come
from forgetting that a preempted process's waiting includes *all* of its
non-running intervals.
""",
        order_index=4,
        estimated_minutes=40,
    ),
    CurriculumLesson(
        id="os-m2-l5",
        module_id="os-m2",
        slug="round-robin",
        title="Round Robin",
        content="""**Round Robin (RR)** gives each ready process a small **time quantum**
(typically 10–100 ms), then preempts it to the back of the queue. It is the
fair-share workhorse — every process is guaranteed CPU within (n−1) quanta, so
response time is excellent.

**Worked example** — quantum = 2; P1 (burst 5), P2 (burst 3), P3 (burst 2),
all arrive at 0:

    | P1 (0-2) | P2 (2-4) | P3 (4-6) done | P1 (6-8) | P2 (8-9) done | P1 (9-10) done |

Completions: P3 at 6, P2 at 9, P1 at 10. Turnaround = 6, 9, 10 (avg 8.33);
waiting = turnaround − burst = 4, 6, 5 (avg **5**).

The quantum is everything:

- **Too large** → each process finishes inside one quantum; RR degenerates
  into FCFS.
- **Too small** → the CPU drowns in context switches; throughput collapses
  (recall the context-switch math: switches × cost).
- Rule of thumb: the quantum should be large relative to context-switch time
  but small relative to interactive response needs — hence 10–100 ms.

RR does not minimize average waiting or turnaround (SJF/SRTF beat it), but it
optimizes what interactive systems care about: no process waits long for its
*first* slice. That is why timesharing systems pair RR-like fairness with
priority feedback (next lessons).

**Interview tip:** "What happens as quantum → 0?" and "as quantum → ∞?" are
the two canonical questions — answer "context-switch meltdown" and "becomes
FCFS", each with the one-line why.
""",
        order_index=5,
        estimated_minutes=40,
    ),
    CurriculumLesson(
        id="os-m2-l6",
        module_id="os-m2",
        slug="priority-scheduling",
        title="Priority Scheduling",
        content="""**Priority scheduling** assigns each process a priority number and always
runs the highest-priority ready process (convention varies — here, larger
number = higher priority; some systems invert it, so state your assumption).
It can be preemptive or non-preemptive, and it is how real systems express
"this matters more" — kernel tasks outrank user apps, interactive jobs outrank
batch.

**Worked example** (non-preemptive, higher number wins): P1 (prio 2, burst 5),
P2 (prio 5, burst 2), P3 (prio 4, burst 3), all arrive at 0.
Order: P2 → P3 → P1.

    | P2 (0-2) | P3 (2-5) | P1 (5-10) |

Waiting: P2 = 0, P3 = 2, P1 = 5 → average **2.33**.

The infamous flaw is **starvation** (indefinite blocking): a low-priority
process can wait forever if higher-priority work keeps arriving. The classic
cure is **aging** — gradually raising the priority of processes the longer
they wait, so every process eventually becomes the highest priority.

A nastier cousin is **priority inversion**: a low-priority process holds a lock
that a high-priority process needs, while medium-priority processes hog the CPU
— the high-priority process effectively waits on the low one. The fix is
**priority inheritance**: the lock-holder temporarily inherits the blocked
process's priority.

**Interview tip:** "How does Linux implement priorities?" → nice values (−20
highest … 19 lowest) feeding the Completely Fair Scheduler. Mentioning aging
unprompted signals you know the starvation story, not just the definition.
""",
        order_index=6,
        estimated_minutes=40,
    ),
    CurriculumLesson(
        id="os-m2-l7",
        module_id="os-m2",
        slug="multilevel-queue-feedback",
        title="Multilevel Queue & Feedback",
        content="""Real systems do not use one queue with one rule — they layer them.

**Multilevel Queue (MLQ)** partitions the ready queue into fixed classes —
e.g., system processes, interactive jobs, batch jobs. Each queue gets its own
algorithm (RR for interactive, FCFS for batch), and the queues themselves are
scheduled — usually strict priority (a batch job runs only when no interactive
job waits) or time-sliced between queues. Key property: a process **never
moves** between queues, so a low queue can starve under fixed-priority
inter-queue scheduling.

**Multilevel Feedback Queue (MLFQ)** adds the missing ingredient:
**movement**. Rules of thumb (Unix-style):

1. New processes enter the top queue with a small quantum.
2. A process that exhausts its quantum is **demoted** to a lower queue (larger
   quantum) — it revealed itself as CPU-bound.
3. A process that yields early for I/O **stays high** — it revealed itself as
   interactive.
4. **Aging**: a process waiting too long in a low queue is promoted back up,
   preventing starvation.

The magic: MLFQ **approximates SJF/SRTF without knowing burst lengths**.
Short/interactive jobs finish in the top queues with tiny quanta; long
CPU-bound jobs sink to the bottom where big quanta suit them. The scheduler
learns each job's nature from its behavior — feedback, hence the name.

**Interview tip:** "Why is MLFQ considered the best general-purpose
scheduler?" → it simultaneously delivers good response time (interactive jobs
stay high), good throughput (batch jobs get big quanta low down), and no
starvation (aging) — adaptively, with zero advance knowledge of workloads.
""",
        order_index=7,
        estimated_minutes=40,
    ),
]


# ---------------------------------------------------------------------------
# QUESTIONS — Module 1: Processes & Threads (6 per lesson, easy -> hard)
# ---------------------------------------------------------------------------

QUESTIONS = [
    # --- os-m1-l1: Program vs Process ---
    _mkq("os-m1-l1-q1", "os-m1-l1", "processes-threads", 1,
        "Which statement best describes the relationship between a program and a process?",
        ("A process is a program in execution",
         "A program is a process stored on disk",
         "They are two names for the same thing",
         "A program is a running instance of a process"),
        0,
        "A program is passive — just machine code and data sitting on disk. It becomes a process only when the OS loads it into memory, gives it an address space and a PCB, and starts executing it. One program can therefore have many processes (open the same app twice).",
        ("tcs", "infosys")),
    _mkq("os-m1-l1-q2", "os-m1-l1", "processes-threads", 1,
        "Which segment of a process image stores the local variables of active function calls?",
        ("Stack", "Heap", "Text", "Data"),
        0,
        "Each function call pushes a frame — parameters, local variables, return address — onto the stack, and the frame is popped when the function returns. The heap holds dynamic allocations (malloc/new), text holds code, and data holds globals.",
        ("tcs", "wipro")),
    _mkq("os-m1-l1-q3", "os-m1-l1", "processes-threads", 2,
        "Initialized global variables of a C program live in which segment?",
        ("Data segment", "Stack segment", "Heap segment", "Text segment"),
        0,
        "The data segment holds initialized globals and statics — the loader copies their initial values from the executable. Uninitialized globals go to BSS, locals go on the stack, and dynamic memory goes on the heap.",
        ("infosys", "accenture")),
    _mkq("os-m1-l1-q4", "os-m1-l1", "processes-threads", 2,
        "A process repeatedly calls malloc() without ever calling free(). Which segment keeps growing?",
        ("Heap", "Stack", "Text", "BSS"),
        0,
        "malloc() allocates from the heap, which grows upward as more dynamic memory is requested. This is the classic memory-leak pattern: the heap keeps growing because nothing is freed. The stack grows with call depth, not with allocation calls.",
        ("wipro", "tcs")),
    _mkq("os-m1-l1-q5", "os-m1-l1", "processes-threads", 3,
        "Two processes run the same program at the same time. Which statement is TRUE?",
        ("Each process has its own separate address space and stack",
         "They must share a single stack",
         "Only one of them can ever be in the running state",
         "They share the same PID"),
        0,
        "Each process gets a private process image — its own data, heap, and stack — even for the same program (the read-only text/code segment may be shared to save memory). They have distinct PIDs, and the scheduler time-shares the CPU between them.",
        ("accenture", "infosys")),
    _mkq("os-m1-l1-q6", "os-m1-l1", "processes-threads", 3,
        "Which of the following exists only AFTER a program becomes a process?",
        ("Its own stack and program counter",
         "Its machine code instructions",
         "Its initialized global variables",
         "Its executable file on disk"),
        0,
        "Machine code, globals, and the disk file all belong to the passive program. A stack (call frames for the live execution) and a program counter (where execution currently is) exist only once the program is loaded and running — i.e., once it is a process.",
        ("tcs", "accenture")),

    # --- os-m1-l2: Process Control Block ---
    _mkq("os-m1-l2-q1", "os-m1-l2", "processes-threads", 1,
        "PCB stands for:",
        ("Process Control Block", "Program Counter Buffer", "Process Communication Bus", "Program Control Byte"),
        0,
        "The Process Control Block is the OS's per-process dossier: PID, state, program counter, registers, scheduling and memory info. The kernel saves and restores it on every context switch, which is what makes multitasking possible.",
        ("tcs", "infosys")),
    _mkq("os-m1-l2-q2", "os-m1-l2", "processes-threads", 2,
        "Which of the following is stored in a process's PCB?",
        ("Program counter and CPU registers",
         "The program's source code",
         "The compiler used to build it",
         "The user's login password"),
        0,
        "The PCB records everything needed to pause and later resume the process: where it was executing (program counter), its working values (registers), plus scheduling, memory, and I/O bookkeeping. Source code and build tools are not runtime state.",
        ("wipro", "infosys")),
    _mkq("os-m1-l2-q3", "os-m1-l2", "processes-threads", 2,
        "Why is the PCB kept in kernel memory rather than user memory?",
        ("So user processes cannot tamper with scheduling and state information",
         "Because kernel memory is larger than user memory",
         "Because PCBs are too small to fit in user memory",
         "To make context switches deliberately slower"),
        0,
        "The PCB holds security-sensitive state — priorities, register contents, open files. If a user process could rewrite its own PCB, it could escalate its priority or forge another process's state. Kernel memory is protected from user-mode access.",
        ("accenture", "tcs")),
    _mkq("os-m1-l2-q4", "os-m1-l2", "processes-threads", 3,
        "After a context switch back to a process, which PCB field tells the CPU which instruction to execute next?",
        ("Program counter", "Process ID", "Open-file table", "CPU time used"),
        0,
        "The program counter holds the address of the next instruction. On a switch-out it is saved into the PCB; on a switch-in it is reloaded, so the process resumes exactly where it was interrupted. The PID only identifies the process.",
        ("infosys", "wipro")),
    _mkq("os-m1-l2-q5", "os-m1-l2", "processes-threads", 3,
        "A process opens three files. What changes in its PCB?",
        ("Its open-file table gains three entries",
         "Its program counter advances by three",
         "Its PID changes to a new value",
         "Its text segment is reloaded from disk"),
        0,
        "The PCB's I/O status section includes the open-file table, which tracks every file descriptor the process holds. Opening files adds entries there; it does not change the PID, the program counter, or the code segment.",
        ("tcs", "accenture")),
    _mkq("os-m1-l2-q6", "os-m1-l2", "processes-threads", 4,
        "Two processes run the same program. How does the OS distinguish them?",
        ("Each has its own PCB with a unique PID",
         "They always run on different CPUs",
         "Their code segments are different",
         "They cannot run at the same time"),
        0,
        "Identity in the OS comes from the PCB, keyed by the unique PID — not from the code being executed. Two processes can share the same read-only text segment yet remain fully distinct because each owns a separate PCB, address space, and stack.",
        ("accenture", "infosys")),

    # --- os-m1-l3: Process States ---
    _mkq("os-m1-l3-q1", "os-m1-l3", "processes-threads", 2,
        "On a single-CPU system, how many processes can be in the running state at the same instant?",
        ("At most one", "As many as are ready", "An unlimited number", "Exactly two"),
        0,
        "The running state means 'instructions executing on the CPU right now'. With one CPU there is only one execution stream, so at most one process runs at a time — multitasking is the rapid ready/running flicker orchestrated by the scheduler.",
        ("tcs", "wipro")),
    _mkq("os-m1-l3-q2", "os-m1-l3", "processes-threads", 2,
        "A process that issued a disk read and is waiting for it to complete is in which state?",
        ("Waiting (blocked)", "Running", "Ready", "Terminated"),
        0,
        "A process paused until an event occurs — here, I/O completion — is waiting (blocked). It is not ready, because even with a free CPU it could not proceed; it must first be woken by the I/O-complete event.",
        ("infosys", "tcs")),
    _mkq("os-m1-l3-q3", "os-m1-l3", "processes-threads", 3,
        "Which state transition is NOT possible?",
        ("Waiting -> Running", "Running -> Ready", "Waiting -> Ready", "Running -> Waiting"),
        0,
        "A process whose I/O completes moves from waiting to ready — it must be dispatched by the scheduler before it can run again. There is no direct waiting-to-running shortcut; every running process is selected from the ready queue.",
        ("accenture", "wipro")),
    _mkq("os-m1-l3-q4", "os-m1-l3", "processes-threads", 3,
        "A process's time quantum expires while it still has work to do. It moves from running to:",
        ("Ready", "Waiting", "Terminated", "New"),
        0,
        "Quantum expiry is preemption: the process is still runnable, it simply lost the CPU, so it rejoins the ready queue. It goes to waiting only if it blocks on an event itself, and to terminated only via exit().",
        ("tcs", "infosys")),
    _mkq("os-m1-l3-q5", "os-m1-l3", "processes-threads", 4,
        "What does 'suspended blocked' mean?",
        ("The process waits for an event AND is swapped out of main memory",
         "The process is executing while stored on disk",
         "The process has terminated but still holds memory",
         "The process is ready and resident in memory"),
        0,
        "'Blocked' means it waits for an event; 'suspended' means it has been swapped out to disk to free RAM. A suspended blocked process whose I/O finishes becomes suspended ready and must be swapped back in before it can run.",
        ("wipro", "accenture")),
    _mkq("os-m1-l3-q6", "os-m1-l3", "processes-threads", 4,
        "A blocked process's I/O completes. Which transition fires?",
        ("Waiting -> Ready", "Waiting -> Running", "Waiting -> Terminated", "Ready -> Running"),
        0,
        "I/O completion only unblocks the process — it becomes ready to run, not running. The scheduler still decides when it actually gets the CPU, which is the ready-to-running (dispatch) transition.",
        ("infosys", "tcs")),

    # --- os-m1-l4: Threads vs Processes ---
    _mkq("os-m1-l4-q1", "os-m1-l4", "processes-threads", 2,
        "Threads belonging to the same process share which of the following?",
        ("Code, data, and open files", "Stack", "Program counter", "Register set"),
        0,
        "Threads share the process's entire address space — code, data/heap, and open files. What makes each thread a separate flow of execution is its private stack, program counter, and registers.",
        ("tcs", "infosys")),
    _mkq("os-m1-l4-q2", "os-m1-l4", "processes-threads", 3,
        "Which of these is private to each thread?",
        ("Stack and registers", "Heap", "Open files", "Global variables"),
        0,
        "A thread needs its own call history (stack) and its own execution position (program counter + registers) to be an independent flow of control. Heap, files, and globals live in the shared address space.",
        ("accenture", "wipro")),
    _mkq("os-m1-l4-q3", "os-m1-l4", "processes-threads", 3,
        "Why is a thread called a 'lightweight process'?",
        ("Creating/switching threads avoids new address spaces and page tables",
         "Threads execute fewer CPU instructions",
         "Threads can never block on I/O",
         "Threads share the kernel's PID"),
        0,
        "The heavy work in process creation/switching is the address space: page tables, memory mappings, file tables. Threads skip all of that because they live inside an existing address space, so both creation and switching are far cheaper.",
        ("infosys", "tcs")),
    _mkq("os-m1-l4-q4", "os-m1-l4", "processes-threads", 4,
        "One thread writes to a global variable. What do its sibling threads observe?",
        ("The updated value — data is shared",
         "The old value — each thread has its own copy",
         "A segmentation fault",
         "Nothing; threads cannot access globals"),
        0,
        "Globals live in the shared data segment, so a write by one thread is immediately visible to the others. This easy sharing is a feature — and the reason threads need locks: unsynchronized concurrent writes cause race conditions.",
        ("wipro", "accenture")),
    _mkq("os-m1-l4-q5", "os-m1-l4", "processes-threads", 4,
        "A single-threaded process has how many stacks?",
        ("One", "One per function it calls", "One per CPU core", "Zero"),
        0,
        "Each thread owns exactly one stack for its call frames. A single-threaded process therefore has one stack; a process with N threads has N stacks, all inside the one shared address space.",
        ("tcs", "infosys")),
    _mkq("os-m1-l4-q6", "os-m1-l4", "processes-threads", 5,
        "Which statement about threads is FALSE?",
        ("A thread can belong to two processes at once",
         "Threads of a process share its address space",
         "Each thread has its own program counter",
         "A crashing thread can kill its whole process"),
        0,
        "A thread is defined inside one process's address space — it cannot straddle two. The other statements are true: address space is shared, each thread has a private program counter, and because memory is shared, one thread's fatal error (e.g., segfault) terminates the entire process.",
        ("accenture", "infosys")),

    # --- os-m1-l5: Multithreading Models ---
    _mkq("os-m1-l5-q1", "os-m1-l5", "processes-threads", 3,
        "In the one-to-one multithreading model, each user-level thread maps to:",
        ("Its own kernel thread", "One shared kernel thread", "A separate user process", "A CPU core directly"),
        0,
        "One-to-one means exactly what it says: every user thread gets a dedicated kernel thread that the OS schedules independently. Blocking one thread blocks only that thread, and threads can spread across cores — at the cost of kernel overhead per thread.",
        ("tcs", "wipro")),
    _mkq("os-m1-l5-q2", "os-m1-l5", "processes-threads", 3,
        "Which model multiplexes many user threads onto a smaller number of kernel threads?",
        ("Many-to-many", "One-to-one", "Many-to-one", "One-to-many"),
        0,
        "Many-to-many multiplexes an arbitrary number of user threads onto a smaller pool of kernel threads — the flexibility of many-to-one without its total-blocking problem, and without one-to-one's per-thread kernel overhead.",
        ("infosys", "accenture")),
    _mkq("os-m1-l5-q3", "os-m1-l5", "processes-threads", 4,
        "What is the main drawback of the many-to-one model?",
        ("One blocking system call blocks the entire process",
         "Too many kernel threads get created",
         "Threads cannot share memory",
         "It requires multicore hardware"),
        0,
        "With many-to-one the kernel sees only a single thread — the whole process. When any user thread makes a blocking system call, the kernel blocks that one kernel thread, freezing every user thread multiplexed onto it.",
        ("wipro", "tcs")),
    _mkq("os-m1-l5-q4", "os-m1-l5", "processes-threads", 4,
        "Why are user-level threads cheaper to create than kernel-level threads?",
        ("No system call or kernel involvement is needed",
         "They use less stack memory",
         "They skip the compilation step",
         "They run at a higher priority"),
        0,
        "User-level thread operations are pure library calls in user space — no trap into the kernel, no mode switch. Kernel thread creation requires a system call and kernel-side bookkeeping, which is an order of magnitude more expensive.",
        ("accenture", "infosys")),
    _mkq("os-m1-l5-q5", "os-m1-l5", "processes-threads", 5,
        "Which classic system used the many-to-one model (Green Threads)?",
        ("Solaris", "Linux", "Windows NT", "MS-DOS"),
        0,
        "Solaris Green Threads are the textbook many-to-one example: the threads library multiplexed user threads onto one kernel thread entirely in user space. Linux and Windows use the one-to-one model, mapping each user thread to a kernel thread.",
        ("tcs", "accenture")),
    _mkq("os-m1-l5-q6", "os-m1-l5", "processes-threads", 5,
        "On a multicore CPU, which models allow threads of one process to run truly in parallel?",
        ("One-to-one and many-to-many",
         "Many-to-one only",
         "All three models",
         "None — threads never run in parallel"),
        0,
        "True parallelism needs multiple kernel threads the OS can place on different cores. Many-to-one exposes only one kernel thread, so its user threads merely interleave on a single core. One-to-one and many-to-many both expose multiple kernel threads to the scheduler.",
        ("infosys", "wipro")),

    # --- os-m1-l6: Context Switching ---
    _mkq("os-m1-l6-q1", "os-m1-l6", "processes-threads", 2,
        "During a context switch, the OS saves:",
        ("The outgoing process's registers and program counter into its PCB",
         "The entire hard disk to RAM",
         "All user passwords to a file",
         "The compiler's symbol table"),
        0,
        "A context switch preserves exactly the CPU state needed to resume later: the program counter (where to continue) and the registers (working values), stored in the outgoing process's PCB. The incoming process's saved state is then loaded.",
        ("tcs", "infosys")),
    _mkq("os-m1-l6-q2", "os-m1-l6", "processes-threads", 3,
        "How does a mode switch (user to kernel for a system call) differ from a context switch?",
        ("The same process keeps running — no PCB save/restore happens",
         "It is always slower than a context switch",
         "It changes the process's PID",
         "It flushes the entire disk cache"),
        0,
        "A mode switch only changes privilege level so the kernel can service the call; the running process does not change, so no PCB state is saved or restored. A context switch swaps the entire running process and is therefore more expensive.",
        ("accenture", "wipro")),
    _mkq("os-m1-l6-q3", "os-m1-l6", "processes-threads", 3,
        "Why is a context switch called 'pure overhead'?",
        ("The CPU does bookkeeping instead of user computation",
         "It consumes permanent disk space",
         "It requires recompiling the program",
         "It deletes the process's memory"),
        0,
        "During a switch the CPU executes OS save/restore code — necessary, but it advances no user program by a single instruction. It is pure overhead in the same sense as time spent sharpening an axe: required, yet not cutting.",
        ("infosys", "tcs")),
    _mkq("os-m1-l6-q4", "os-m1-l6", "processes-threads", 4,
        "Besides the save/restore cost, what indirect cost follows a context switch?",
        ("Cache/TLB misses while the new process reloads its working set",
         "A higher electricity bill and nothing else",
         "Permanent loss of RAM capacity",
         "Doubled disk capacity requirements"),
        0,
        "While a process was away, other processes evicted its data from caches and the TLB. When it resumes, it suffers a burst of cache misses until its working set is reloaded — an indirect cost that can exceed the direct save/restore cost.",
        ("wipro", "accenture")),
    _mkq("os-m1-l6-q5", "os-m1-l6", "processes-threads", 4,
        "Which is faster — a mode switch or a full context switch?",
        ("Mode switch", "Context switch", "They take identical time", "Neither ever occurs"),
        0,
        "A mode switch just flips the privilege bit and jumps to a kernel handler for the same process. A context switch additionally saves one PCB, selects the next process, loads another PCB, and often flushes address-space state — strictly more work.",
        ("tcs", "accenture")),
    _mkq("os-m1-l6-q6", "os-m1-l6", "processes-threads", 5,
        "A system does 1000 context switches per second, each costing 10 microseconds. What fraction of CPU time is lost?",
        ("1%", "10%", "0.1%", "100%"),
        0,
        "1000 switches x 10 microseconds = 10,000 microseconds = 10 milliseconds per second, i.e. 1% of CPU time. This is why shrinking the scheduling quantum too far is dangerous: switches multiply and the overhead stops being negligible.",
        ("accenture", "infosys")),

    # --- os-m1-l7: Process Creation & Termination ---
    _mkq("os-m1-l7-q1", "os-m1-l7", "processes-threads", 2,
        "fork() returns 0 in:",
        ("The child process", "The parent process", "Both processes", "The init process"),
        0,
        "fork() returns twice: the child's PID to the parent (so it can track/wait for the child) and 0 to the child (so it knows it is the child). Code typically branches on 'if (pid == 0)' to run child-specific logic.",
        ("tcs", "wipro")),
    _mkq("os-m1-l7-q2", "os-m1-l7", "processes-threads", 2,
        "What does the exec() system call do?",
        ("Replaces the process's memory image with a new program",
         "Creates an exact copy of the process",
         "Terminates the process immediately",
         "Pauses the process indefinitely"),
        0,
        "exec() loads a new program's code and data over the calling process's address space — same PID, brand-new program. That is why shells fork() first (to clone) and then exec() in the child: the shell itself must survive.",
        ("infosys", "accenture")),
    _mkq("os-m1-l7-q3", "os-m1-l7", "processes-threads", 3,
        "A zombie process is:",
        ("Terminated, but its parent hasn't called wait() yet",
         "A process stuck in an infinite loop",
         "A process with no parent at all",
         "A process running on a remote machine"),
        0,
        "A zombie is already dead — it holds no memory and gets no CPU. Only its process-table entry (PID + exit status) lingers so the parent can collect the exit code via wait(). An infinite loop is a live runaway process, not a zombie.",
        ("wipro", "tcs")),
    _mkq("os-m1-l7-q4", "os-m1-l7", "processes-threads", 3,
        "Orphan processes are adopted by:",
        ("init/systemd (PID 1)", "The shell that started them", "The CPU scheduler", "No one — they become zombies"),
        0,
        "When a parent dies first, the kernel reparents its children to init (PID 1), which routinely wait()s on them and reaps their exit statuses. Because adoption is automatic, orphans never linger as zombies.",
        ("accenture", "infosys")),
    _mkq("os-m1-l7-q5", "os-m1-l7", "processes-threads", 4,
        "Why does a shell use fork() + exec() to run a command instead of just exec()?",
        ("exec() alone would replace the shell itself",
         "fork() makes commands run faster",
         "exec() cannot execute binary files",
         "fork() is mandatory for every system call"),
        0,
        "exec() overwrites the calling process's image. If the shell called exec('ls') directly, the shell would become ls and vanish — no prompt would ever return. fork() clones the shell first, so the child can exec the command while the parent shell waits.",
        ("tcs", "infosys")),
    _mkq("os-m1-l7-q6", "os-m1-l7", "processes-threads", 5,
        "What resource does a zombie process still hold?",
        ("Its process-table entry (PID and exit status)",
         "All of its former RAM",
         "Its open network sockets",
         "Reserved CPU time slices"),
        0,
        "A zombie has released everything except its slot in the process table, which preserves the PID and exit status for the parent's wait(). That is also why you cannot 'kill' a zombie — it is already dead; you fix the parent instead.",
        ("infosys", "wipro")),

    # --- os-m1-l8: Inter-Process Communication ---
    _mkq("os-m1-l8-q1", "os-m1-l8", "processes-threads", 3,
        "Which IPC mechanism is generally fastest for transferring large amounts of data?",
        ("Shared memory", "Message queues", "Pipes", "Signals"),
        0,
        "After the initial setup, shared memory lets processes read/write at full memory speed with no kernel involvement per transfer. Message queues, pipes, and signals all route data through the kernel, adding system-call and copying costs.",
        ("tcs", "accenture")),
    _mkq("os-m1-l8-q2", "os-m1-l8", "processes-threads", 3,
        "A pipe is best described as:",
        ("A unidirectional byte stream, typically between related processes",
         "A bidirectional shared database",
         "A network socket",
         "A disk file that never closes"),
        0,
        "A pipe is a kernel-buffered, one-way byte channel — what makes 'ls | grep x' work. It is usually created by a parent before fork() so parent and child share the file descriptors. Named pipes (FIFOs) extend the idea to unrelated processes.",
        ("infosys", "wipro")),
    _mkq("os-m1-l8-q3", "os-m1-l8", "processes-threads", 4,
        "What is the main hazard of shared memory that message passing avoids?",
        ("Race conditions from unsynchronized concurrent access",
         "Slower transfer speed",
         "Inability to work on a single machine",
         "Mandatory data encryption"),
        0,
        "Shared memory gives raw speed but zero synchronization: two processes updating the same counter can interleave into garbage. Message passing's blocking send/receive gives you coordination for free, at the cost of kernel-mediated copying.",
        ("accenture", "tcs")),
    _mkq("os-m1-l8-q4", "os-m1-l8", "processes-threads", 4,
        "Which IPC approach works naturally between processes on different machines?",
        ("Message passing via sockets", "Shared memory", "Ordinary pipes", "Signals"),
        0,
        "Message passing abstracts communication as send/receive, which works identically whether the peer is local or across a network (sockets). Shared memory, pipes, and signals all depend on a single machine's kernel or address space.",
        ("wipro", "infosys")),
    _mkq("os-m1-l8-q5", "os-m1-l8", "processes-threads", 4,
        "Message passing is slower than shared memory mainly because:",
        ("Every transfer involves the kernel (system calls and copying)",
         "Messages are limited to a single byte",
         "It requires a dedicated GPU",
         "It only works when the network is down"),
        0,
        "Each send/receive traps into the kernel, which validates and copies the message between address spaces. Shared memory pays a one-time setup cost and then transfers at RAM speed with no per-message kernel work.",
        ("tcs", "accenture")),
    _mkq("os-m1-l8-q6", "os-m1-l8", "processes-threads", 5,
        "A producer and consumer share a bounded buffer in shared memory. Which problem must the programmer explicitly solve?",
        ("Synchronization — mutual exclusion and full/empty coordination",
         "Compiling the buffer",
         "Assigning process IDs",
         "Encrypting the CPU registers"),
        0,
        "Shared memory provides the buffer but no rules: the producer must not overwrite a full buffer, the consumer must not read an empty one, and concurrent updates need mutual exclusion. The classic solution pairs a mutex with full/empty semaphores — all written by the programmer.",
        ("infosys", "wipro")),
]


# ---------------------------------------------------------------------------
# QUESTIONS — Module 2: CPU Scheduling (6 per lesson, easy -> hard)
# ---------------------------------------------------------------------------

QUESTIONS += [
    # --- os-m2-l1: Scheduling Criteria ---
    _mkq("os-m2-l1-q1", "os-m2-l1", "cpu-scheduling", 2,
        "Turnaround time is defined as:",
        ("Completion time - arrival time",
         "Burst time - waiting time",
         "Arrival time - completion time",
         "Quantum x number of processes"),
        0,
        "Turnaround is the full wall-clock span from when a process arrives to when it completes. It includes both waiting and execution — which is exactly why waiting time is defined as turnaround minus burst.",
        ("tcs", "infosys")),
    _mkq("os-m2-l1-q2", "os-m2-l1", "cpu-scheduling", 2,
        "Waiting time equals:",
        ("Turnaround time - burst time",
         "Burst time - turnaround time",
         "Arrival time + completion time",
         "Quantum - burst time"),
        0,
        "Waiting time counts only the time spent sitting in the ready queue, so you subtract the burst (actual execution) from the turnaround (total span). It is the scheduler's report card: everything else being equal, lower is better.",
        ("wipro", "tcs")),
    _mkq("os-m2-l1-q3", "os-m2-l1", "cpu-scheduling", 3,
        "Which metric matters most for interactive (timesharing) systems?",
        ("Response time", "Throughput", "CPU utilization", "Compilation speed"),
        0,
        "Interactive users feel the delay before the system first reacts to a keystroke or click — that is response time (first run minus arrival). Throughput and utilization matter more for batch systems; response time is the interactivity metric.",
        ("accenture", "infosys")),
    _mkq("os-m2-l1-q4", "os-m2-l1", "cpu-scheduling", 3,
        "If CPU utilization is 40%, the CPU is idle for what fraction of the time?",
        ("60%", "40%", "140%", "4%"),
        0,
        "Utilization + idle = 100% of observed time. A 40% busy CPU is idle 60% of the time — usually a sign the workload is I/O-bound and the scheduler should overlap I/O waits with other processes' bursts.",
        ("tcs", "wipro")),
    _mkq("os-m2-l1-q5", "os-m2-l1", "cpu-scheduling", 3,
        "Throughput measures:",
        ("Processes completed per unit time",
         "Bytes transferred per second",
         "Context switches per quantum",
         "Users currently logged in"),
        0,
        "Throughput is the completion rate — how many jobs finish per second/minute/hour. It depends on both the workload's burst lengths and the scheduler: favoring short jobs raises throughput but can starve long ones.",
        ("infosys", "accenture")),
    _mkq("os-m2-l1-q6", "os-m2-l1", "cpu-scheduling", 4,
        "A process arrives at t=2, first runs at t=5, finishes at t=12, with burst 4. Its response time is:",
        ("3", "6", "10", "4"),
        0,
        "Response time = first CPU run - arrival = 5 - 2 = 3. (The tempting 6 is the waiting time: turnaround (12-2=10) minus burst 4. The 10 is the turnaround itself. Keeping the three definitions apart is the classic interview trap.)",
        ("accenture", "tcs")),

    # --- os-m2-l2: FCFS Scheduling ---
    _mkq("os-m2-l2-q1", "os-m2-l2", "cpu-scheduling", 2,
        "FCFS scheduling is:",
        ("Non-preemptive", "Preemptive", "Priority-based", "Quantum-based"),
        0,
        "In FCFS a process keeps the CPU until it finishes or blocks on its own — the scheduler never takes it away. That non-preemptive simplicity is both its appeal (zero scheduling overhead) and its flaw (the convoy effect).",
        ("tcs", "infosys")),
    _mkq("os-m2-l2-q2", "os-m2-l2", "cpu-scheduling", 2,
        "P1 arrives at 0 (burst 5), P2 arrives at 1 (burst 2). Under FCFS, which runs first?",
        ("P1", "P2", "The shorter one, P2", "Both simultaneously"),
        0,
        "FCFS serves strictly in arrival order and ignores burst lengths — P1 arrived first, so P1 runs to completion before P2 starts, even though P2 is shorter. 'Shortest first' is SJF's rule, not FCFS's.",
        ("wipro", "tcs")),
    _mkq("os-m2-l2-q3", "os-m2-l2", "cpu-scheduling", 3,
        "The convoy effect refers to:",
        ("Short processes waiting behind one long process",
         "Processes migrating between CPU cores in groups",
         "The CPU overheating under load",
         "Quantum expiration storms"),
        0,
        "When one long CPU-bound job reaches the front of an FCFS queue, every short (often interactive) job behind it waits out the full burst. The short jobs 'convoy' behind the long one, and average waiting time balloons.",
        ("accenture", "infosys")),
    _mkq("os-m2-l2-q4", "os-m2-l2", "cpu-scheduling", 3,
        "P1 arrives 0 (burst 5), P2 arrives 1 (burst 3), P3 arrives 2 (burst 2). FCFS Gantt: P1 0-5, P2 5-8, P3 8-10. Average waiting time?",
        ("3.33", "5.0", "6.67", "2.0"),
        0,
        "Waiting = start - arrival: P1 = 0, P2 = 5-1 = 4, P3 = 8-2 = 6. Average = (0+4+6)/3 = 10/3 = 3.33. Note P1 waits 0 because it arrived to an empty system and ran immediately.",
        ("tcs", "wipro")),
    _mkq("os-m2-l2-q5", "os-m2-l2", "cpu-scheduling", 4,
        "Same workload (P1(0,5), P2(1,3), P3(2,2)) under FCFS. Average turnaround time?",
        ("6.67", "3.33", "10.0", "5.0"),
        0,
        "Turnaround = completion - arrival: P1 = 5-0 = 5, P2 = 8-1 = 7, P3 = 10-2 = 8. Average = (5+7+8)/3 = 20/3 = 6.67. Cross-check: avg waiting 3.33 + avg burst (5+3+2)/3 = 3.33 gives the same 6.67.",
        ("infosys", "accenture")),
    _mkq("os-m2-l2-q6", "os-m2-l2", "cpu-scheduling", 5,
        "P1 (burst 10) arrives at 0; P2 and P3 (burst 1 each) arrive at 1 and 2. Average turnaround under FCFS?",
        ("10", "4", "7.33", "12"),
        0,
        "Gantt: P1 0-10, P2 10-11, P3 11-12. Turnarounds: P1 = 10, P2 = 11-1 = 10, P3 = 12-2 = 10; average = 10. The two 1-unit jobs each suffer a turnaround of 10 — the convoy effect expressed in pure numbers.",
        ("accenture", "tcs")),

    # --- os-m2-l3: SJF Scheduling ---
    _mkq("os-m2-l3-q1", "os-m2-l3", "cpu-scheduling", 3,
        "SJF always selects the ready process with:",
        ("The smallest next CPU burst", "The earliest arrival time", "The highest priority number", "The largest burst"),
        0,
        "SJF's rule is purely burst-based: among ready processes, run the one with the shortest next CPU burst. Arrival order only matters at time 0 (whoever is there runs); priority numbers belong to priority scheduling.",
        ("tcs", "infosys")),
    _mkq("os-m2-l3-q2", "os-m2-l3", "cpu-scheduling", 3,
        "SJF is provably optimal for minimizing:",
        ("Average waiting time", "Number of context switches", "Throughput", "Response time"),
        0,
        "For a given set of processes, no non-preemptive schedule beats SJF's average waiting time (exchange argument: swapping a longer-before-shorter pair can only help). It does not optimize context switches or response time — SRTF and RR target those.",
        ("wipro", "accenture")),
    _mkq("os-m2-l3-q3", "os-m2-l3", "cpu-scheduling", 4,
        "Burst prediction: next = a*t(n) + (1-a)*old, with a=0.5, old prediction=10, last actual burst=6. The next prediction is:",
        ("8", "6", "10", "13"),
        0,
        "0.5 x 6 + 0.5 x 10 = 3 + 5 = 8. Exponential averaging blends recent behavior (weight a) with history (weight 1-a): a=0.5 weights them equally. Larger a reacts faster to changes; smaller a is more stable.",
        ("infosys", "tcs")),
    _mkq("os-m2-l3-q4", "os-m2-l3", "cpu-scheduling", 4,
        "P1(0,5), P2(1,3), P3(2,2) under non-preemptive SJF. Gantt: P1 0-5, P3 5-7, P2 7-10. Average waiting time?",
        ("3", "3.33", "4", "2.67"),
        0,
        "At t=0 only P1 is ready, so P1 runs 0-5. At t=5, P2 (burst 3) and P3 (burst 2) wait — P3 is shorter, so P3 runs 5-7, then P2 runs 7-10. Waiting: P1 = 0, P3 = 5-2 = 3, P2 = 7-1 = 6; average = 9/3 = 3, beating FCFS's 3.33.",
        ("accenture", "wipro")),
    _mkq("os-m2-l3-q5", "os-m2-l3", "cpu-scheduling", 4,
        "Same SJF schedule (P1 0-5, P3 5-7, P2 7-10). Average turnaround time?",
        ("6.33", "6.67", "5.0", "7.0"),
        0,
        "Turnaround = completion - arrival: P1 = 5, P3 = 7-2 = 5, P2 = 10-1 = 9; average = 19/3 = 6.33. Again better than FCFS (6.67) — SJF's optimality showing in both metrics here.",
        ("tcs", "infosys")),
    _mkq("os-m2-l3-q6", "os-m2-l3", "cpu-scheduling", 5,
        "Which statement about SJF is FALSE?",
        ("It can be implemented without knowing burst lengths",
         "It minimizes average waiting time",
         "It is non-preemptive",
         "Long processes may starve"),
        0,
        "SJF's fundamental impracticality is that the next CPU burst is unknowable in advance — real systems must predict it via exponential averaging. The other three are true: optimal average waiting, non-preemptive, and starvation risk for long jobs.",
        ("wipro", "accenture")),

    # --- os-m2-l4: SRTF Scheduling ---
    _mkq("os-m2-l4-q1", "os-m2-l4", "cpu-scheduling", 3,
        "SRTF differs from SJF in that it:",
        ("Preempts the running process when a shorter job arrives",
         "Uses larger time quanta",
         "Ignores process arrival times",
         "Never preempts once started"),
        0,
        "SRTF re-runs the 'shortest' comparison at every arrival: if the newcomer's burst is smaller than the running process's remaining time, it preempts. SJF makes the decision once, at dispatch time, and never revisits it.",
        ("tcs", "wipro")),
    _mkq("os-m2-l4-q2", "os-m2-l4", "cpu-scheduling", 3,
        "SRTF is best described as:",
        ("Preemptive SJF", "Preemptive FCFS", "Non-preemptive priority scheduling", "A variant of Round Robin"),
        0,
        "SRTF = Shortest Remaining Time First = SJF with preemption on arrival. The 'remaining time' framing is what lets it interrupt a running long job the moment a shorter one appears.",
        ("infosys", "accenture")),
    _mkq("os-m2-l4-q3", "os-m2-l4", "cpu-scheduling", 4,
        "P1(0,6), P2(1,3), P3(2,1) under SRTF. Gantt: P1 0-1, P2 1-2, P3 2-3, P2 3-5, P1 5-11. Average waiting time?",
        ("2", "3", "3.33", "1.33"),
        0,
        "Waiting = turnaround - burst. Turnarounds: P1 = 11-0 = 11, P2 = 5-1 = 4, P3 = 3-2 = 1. Waiting: P1 = 11-6 = 5, P2 = 4-3 = 1, P3 = 1-1 = 0; average = 6/3 = 2. Note P1's waiting spans both its preempted intervals.",
        ("accenture", "tcs")),
    _mkq("os-m2-l4-q4", "os-m2-l4", "cpu-scheduling", 5,
        "Same SRTF schedule (completions: P3 at 3, P2 at 5, P1 at 11). Average turnaround time?",
        ("5.33", "6.33", "4.0", "7.0"),
        0,
        "Turnaround = completion - arrival: P1 = 11, P2 = 5-1 = 4, P3 = 3-2 = 1; average = 16/3 = 5.33. Cross-check: avg waiting 2 + avg burst (6+3+1)/3 = 3.33 gives 5.33.",
        ("tcs", "infosys")),
    _mkq("os-m2-l4-q5", "os-m2-l4", "cpu-scheduling", 5,
        "Under SRTF, which process faces the greatest starvation risk?",
        ("A long-burst process when short processes keep arriving",
         "The shortest process in the system",
         "The first process to arrive",
         "The process with the highest priority"),
        0,
        "SRTF always favors the smallest remaining time, so a continuous stream of short arrivals keeps preempting (or jumping ahead of) a long job indefinitely. SRTF inherits SJF's starvation problem — preemption just makes the bias stronger.",
        ("wipro", "accenture")),
    _mkq("os-m2-l4-q6", "os-m2-l4", "cpu-scheduling", 6,
        "For the same workload, SRTF's average waiting time compared to SJF's is:",
        ("Less than or equal", "Always strictly greater", "Always exactly equal", "Completely unrelated"),
        0,
        "SRTF can only improve on SJF's decisions: every preemption lets a shorter job start earlier, and if no preemption ever triggers, SRTF behaves exactly like SJF. Hence its average waiting is <= SJF's — the minimum achievable. The price is extra context switches and the same starvation risk.",
        ("infosys", "tcs")),

    # --- os-m2-l5: Round Robin ---
    _mkq("os-m2-l5-q1", "os-m2-l5", "cpu-scheduling", 3,
        "In Round Robin with quantum q, a process needing 3q of CPU time is preempted how many times?",
        ("2", "3", "1", "0"),
        0,
        "It runs one quantum, is preempted (1), runs a second quantum, is preempted (2), then runs its final quantum to completion — no preemption needed at the end. So 3 quanta of work means 2 preemptions.",
        ("tcs", "infosys")),
    _mkq("os-m2-l5-q2", "os-m2-l5", "cpu-scheduling", 3,
        "If the Round Robin time quantum is made very large, RR behaves like:",
        ("FCFS", "SJF", "Priority scheduling", "Multilevel feedback queue"),
        0,
        "With a huge quantum every process finishes inside its first slice, so no preemption ever happens and processes simply run in arrival order — exactly FCFS. Quantum size is a dial between FCFS-like and fine-grained fair sharing.",
        ("wipro", "accenture")),
    _mkq("os-m2-l5-q3", "os-m2-l5", "cpu-scheduling", 4,
        "If the RR quantum is made extremely small, the main problem is:",
        ("Excessive context-switch overhead", "Starvation of long processes", "Deadlock", "Memory leaks"),
        0,
        "Tiny quanta mean the CPU switches processes constantly; with each switch costing save/restore plus cache pollution, throughput collapses — the CPU spends more time switching than computing. RR never starves (everyone cycles), and quantum size is unrelated to deadlock.",
        ("accenture", "tcs")),
    _mkq("os-m2-l5-q4", "os-m2-l5", "cpu-scheduling", 4,
        "P1(0,5), P2(0,3), P3(0,2), quantum=2. Gantt: P1 0-2, P2 2-4, P3 4-6, P1 6-8, P2 8-9, P1 9-10. Average waiting time?",
        ("5", "8.33", "3.33", "6"),
        0,
        "Completions: P3 at 6, P2 at 9, P1 at 10. Waiting = turnaround - burst: P1 = 10-5 = 5, P2 = 9-3 = 6, P3 = 6-2 = 4; average = 15/3 = 5. (8.33 is the average turnaround — the classic mix-up.)",
        ("tcs", "wipro")),
    _mkq("os-m2-l5-q5", "os-m2-l5", "cpu-scheduling", 5,
        "Same RR schedule (completions: P3 at 6, P2 at 9, P1 at 10). Average turnaround time?",
        ("8.33", "5", "10", "6.67"),
        0,
        "All arrived at 0, so turnaround = completion time: 10, 9, 6; average = 25/3 = 8.33. Cross-check: avg waiting 5 + avg burst (5+3+2)/3 = 3.33 gives 8.33.",
        ("infosys", "accenture")),
    _mkq("os-m2-l5-q6", "os-m2-l5", "cpu-scheduling", 6,
        "With n processes in the ready queue and quantum q, a newly arrived process waits at most about ___ before its first run.",
        ("(n-1)*q", "n*q*q", "q/n", "n+q"),
        0,
        "In the worst case the newcomer lands at the tail behind n-1 processes, each holding the CPU for up to one full quantum q. So its first slice comes within (n-1)*q — this bounded wait is exactly why RR gives good response time, and why shrinking q improves responsiveness until context-switch overhead bites.",
        ("accenture", "infosys")),

    # --- os-m2-l6: Priority Scheduling ---
    _mkq("os-m2-l6-q1", "os-m2-l6", "cpu-scheduling", 3,
        "In priority scheduling, the CPU is given to:",
        ("The highest-priority ready process", "The process that arrived first", "The shortest process", "A randomly chosen process"),
        0,
        "Priority scheduling's entire rule is 'highest priority among ready processes runs'. Arrival order is FCFS's rule, burst length is SJF's, and randomness is nobody's rule.",
        ("tcs", "wipro")),
    _mkq("os-m2-l6-q2", "os-m2-l6", "cpu-scheduling", 3,
        "Starvation in priority scheduling means:",
        ("A low-priority process waits indefinitely",
         "The CPU runs out of power",
         "All processes finish too quickly",
         "The ready queue overflows"),
        0,
        "If higher-priority work keeps arriving, a low-priority process may never be selected — it waits indefinitely (also called indefinite blocking). It is a scheduling pathology, not a hardware failure.",
        ("infosys", "accenture")),
    _mkq("os-m2-l6-q3", "os-m2-l6", "cpu-scheduling", 4,
        "Aging cures starvation by:",
        ("Gradually raising the priority of long-waiting processes",
         "Terminating old processes",
         "Lowering every process's priority equally",
         "Increasing the time quantum"),
        0,
        "Aging increases a waiting process's priority over time, so even the lowest-priority job eventually outranks newcomers and gets the CPU. It guarantees progress without abandoning the priority scheme.",
        ("accenture", "tcs")),
    _mkq("os-m2-l6-q4", "os-m2-l6", "cpu-scheduling", 4,
        "Non-preemptive priority (higher number = higher priority): P1(prio 2, burst 5), P2(prio 5, burst 2), P3(prio 4, burst 3), all arrive at 0. Which runs first?",
        ("P2", "P1", "P3", "P1 and P3 together"),
        0,
        "Higher number wins: P2 (5) > P3 (4) > P1 (2). Execution order is P2, then P3, then P1 — Gantt: P2 0-2, P3 2-5, P1 5-10. Burst lengths do not matter for the ordering decision.",
        ("tcs", "infosys")),
    _mkq("os-m2-l6-q5", "os-m2-l6", "cpu-scheduling", 5,
        "Same priority schedule (P2 0-2, P3 2-5, P1 5-10). Average waiting time?",
        ("2.33", "3.33", "5", "1.67"),
        0,
        "Waiting = start - arrival (all arrived at 0): P2 = 0, P3 = 2, P1 = 5; average = 7/3 = 2.33. The low-priority P1 absorbs most of the wait — the starvation pattern in miniature.",
        ("wipro", "accenture")),
    _mkq("os-m2-l6-q6", "os-m2-l6", "cpu-scheduling", 6,
        "Preemptive priority scheduling: a low-priority process holds a lock needed by a high-priority process, while medium-priority processes keep the CPU busy. This is:",
        ("Priority inversion", "Aging", "The convoy effect", "Thrashing"),
        0,
        "The high-priority process is effectively blocked behind the low-priority lock-holder, which itself cannot run because medium-priority processes preempt it — so priorities are 'inverted'. The standard fix is priority inheritance: the lock-holder temporarily inherits the highest priority of anyone waiting on its lock.",
        ("infosys", "tcs")),

    # --- os-m2-l7: Multilevel Queue & Feedback ---
    _mkq("os-m2-l7-q1", "os-m2-l7", "cpu-scheduling", 4,
        "In a Multilevel Queue (MLQ) scheduler, a process:",
        ("Stays permanently in its assigned queue",
         "Moves freely between queues",
         "Changes its own priority number",
         "Bypasses the scheduler entirely"),
        0,
        "MLQ's defining limitation is no migration: a process is classified once (system/interactive/batch) and stays in that queue forever. That rigidity is exactly what the feedback queue (MLFQ) was invented to fix.",
        ("tcs", "accenture")),
    _mkq("os-m2-l7-q2", "os-m2-l7", "cpu-scheduling", 4,
        "MLFQ differs from MLQ in that MLFQ:",
        ("Lets processes move between queues based on observed behavior",
         "Uses only a single queue",
         "Is strictly non-preemptive",
         "Ignores process priorities"),
        0,
        "The 'feedback' in MLFQ is the scheduler observing each job — exhausting a quantum demotes it, yielding early keeps it high — and moving it between queues accordingly. MLQ has fixed queues with no movement.",
        ("infosys", "wipro")),
    _mkq("os-m2-l7-q3", "os-m2-l7", "cpu-scheduling", 5,
        "In MLFQ, a CPU-bound process that always exhausts its quantum is:",
        ("Demoted to lower queues with larger quanta",
         "Promoted to the top queue",
         "Terminated for misbehavior",
         "Given a smaller quantum forever"),
        0,
        "Exhausting the quantum signals 'CPU-bound, not interactive', so MLFQ demotes the job to lower queues where larger quanta suit long bursts. Interactive jobs that yield early keep their high placement — the scheduler learns the job's nature from its behavior.",
        ("wipro", "tcs")),
    _mkq("os-m2-l7-q4", "os-m2-l7", "cpu-scheduling", 5,
        "MLFQ is best described as an adaptive approximation of:",
        ("SJF/SRTF, without needing burst lengths in advance",
         "FCFS with aging",
         "Pure Round Robin",
         "Random scheduling"),
        0,
        "MLFQ achieves SJF-like behavior — short/interactive jobs finish quickly in top queues — purely from observed behavior (quantum exhaustion vs early yield), with zero advance knowledge of burst lengths. That is its core trick.",
        ("accenture", "infosys")),
    _mkq("os-m2-l7-q5", "os-m2-l7", "cpu-scheduling", 6,
        "What is the purpose of aging (promotion) in MLFQ?",
        ("Prevent starvation of processes stuck in low queues",
         "Speed up context switches",
         "Reduce the number of queues",
         "Increase batch-job throughput"),
        0,
        "Without promotion, a CPU-bound job demoted to the bottom could wait forever under a stream of interactive arrivals. Aging periodically promotes long-waiting jobs back up, guaranteeing every process eventually runs.",
        ("tcs", "wipro")),
    _mkq("os-m2-l7-q6", "os-m2-l7", "cpu-scheduling", 7,
        "An interactive process in MLFQ repeatedly yields the CPU for I/O before its quantum expires. What happens to it?",
        ("It keeps high queue placement, preserving quick response",
         "It is demoted exactly like a CPU-bound job",
         "It is moved to the batch queue permanently",
         "Its priority is frozen at the top forever"),
        0,
        "MLFQ's feedback rule rewards yielding early: a process that does not use its full quantum looks interactive, so it stays in (or returns to) a high-priority queue with small quanta. Only quantum-exhausting CPU-bound jobs get demoted — this is how MLFQ separates interactive from batch work purely by observed behavior.",
        ("infosys", "accenture")),
]
