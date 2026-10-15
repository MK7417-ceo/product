"""Seed content: Operating Systems — Modules 5 (File Systems) and 6 (System Concepts).

Part-file of the OS curriculum seed. Provides MODULES, LESSONS, QUESTIONS lists
using the frozen dataclasses from app.domain.curriculum. All theory is original
and interview-focused; disk-scheduling figures are hand-verified.

Expected to be picked up by the curriculum content loader alongside the other
os_part_*.py seed files (same MODULES/LESSONS/QUESTIONS shape).
"""

from __future__ import annotations

from app.domain.curriculum import (
    CurriculumLesson,
    CurriculumModule,
    CurriculumQuestion,
    validate_curriculum_question,
)

DOMAIN_SLUG = "operating-systems"


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


def _mkl(lesson_id, module_id, slug, title, content, order_index,
         estimated_minutes=35):
    return CurriculumLesson(
        id=lesson_id,
        module_id=module_id,
        slug=slug,
        title=title,
        content=content,
        order_index=order_index,
        estimated_minutes=estimated_minutes,
    )


# ------------------------------------------------------------------ modules

MODULES = [
    CurriculumModule(
        id="os-m5",
        domain_slug=DOMAIN_SLUG,
        slug="file-systems",
        name="File Systems",
        description=(
            "How the OS stores and finds data on disk: file concepts and "
            "operations, directory structures, allocation methods, disk "
            "scheduling algorithms with worked examples, free-space "
            "management and RAID."
        ),
        order_index=5,
        estimated_days=6,
    ),
    CurriculumModule(
        id="os-m6",
        domain_slug=DOMAIN_SLUG,
        slug="system-concepts",
        name="System Concepts",
        description=(
            "How the OS protects itself and serves programs: system calls, "
            "kernel vs user mode, interrupts/traps/exceptions, OS "
            "structures, and booting."
        ),
        order_index=6,
        estimated_days=5,
    ),
]

# ------------------------------------------------------------------ lessons

LESSONS = [
    _mkl(
        "os-m5-l1", "os-m5", "file-concepts", "File Concepts",
        """A file is the OS's fundamental abstraction for persistent data: a named
collection of related information (a program, a document, a database) stored on
secondary storage. The OS hides raw disk geometry behind this clean unit, so
programs think in files while the kernel thinks in blocks.

Every file carries attributes (metadata): name, unique identifier, type,
location on disk, size, protection/permissions, and timestamps (creation, last
modified, last accessed). Attributes live in the directory entry, so the OS can
manage a file without reading its contents.

The core operations the OS exposes are: create, open, close, read, write,
append, seek (reposition the read/write pointer), delete, rename, and truncate.
Notice the asymmetry interviewers love: open() returns a handle, reads and
writes then proceed on the handle, and close() releases it.

File types matter to the OS and tools: source files, executables, object files,
and structured types (zip, pdf) recognized by extension or magic numbers.

Access methods decide how data is reached. Sequential access reads record n
before n+1 (like a tape). Direct (random) access jumps to any block without
touching the ones before it (like a disk). Indexed access uses an index block
that maps logical records to physical blocks, like a book's index. Databases
choose direct/indexed access; a log file is naturally sequential.""",
        1,
    ),
    _mkl(
        "os-m5-l2", "os-m5", "directory-structures", "Directory Structures",
        """Directories map human-readable names to file metadata. Five classic
designs, each a trade-off:

Single-level: one flat directory for every user. Simple, but names collide
across users and lookup is O(n).

Two-level: one directory per user (first level holds user names). Collisions
across users disappear, but each user's space is still flat and every path
needs the user context.

Tree-structured: directories nest arbitrarily; users get private subtrees and
pathnames like /home/user/docs. This is what modern OSes use: hierarchy makes
searching recursive and grouping natural.

Acyclic-graph: allows sharing — a file can appear in multiple directories via
hard links. New problem: deletion. When is the last reference gone? The OS
keeps a reference count and frees the file only at zero.

General graph: adds symbolic links (shortcuts storing a pathname), which CAN
create cycles. The OS must detect cycles during traversal or a search loops
forever.

Interview line: Unix chose tree + links — hierarchy for organization, links
for sharing without duplication. If asked to compare, anchor on three axes:
name collisions, sharing, and deletion complexity.""",
        2,
    ),
    _mkl(
        "os-m5-l3", "os-m5", "file-allocation-methods", "File Allocation Methods",
        """Three classic strategies decide where a file's blocks land on disk:

Contiguous allocation places blocks in consecutive sectors. Sequential and
direct access are both trivially fast with minimal seeks. The price: finding
free space needs first-fit/best-fit search (external fragmentation), and a file
cannot grow without relocation.

Linked allocation chains blocks with pointers; the directory stores only the
first block's address. No external fragmentation, files grow freely. But direct
access is O(n) — you walk the chain — and a lost pointer corrupts the tail.

Indexed allocation (inode-based, the Unix way): an index block holds pointers
to all data blocks, plus single, double, and triple indirect pointers for large
files. Direct access is O(1), there is no external fragmentation, and growth is
easy — at the cost of one index block per file.

Modern Unix combines direct and indirect: a dozen or so direct pointers cover
small files with zero indirection; indirect levels scale to huge files.

Interview trap: internal fragmentation (wasted bytes in the last partially
used block) vs external fragmentation (scattered free space). Indexed
allocation suffers internal fragmentation only; contiguous suffers both.""",
        3,
    ),
    _mkl(
        "os-m5-l4", "os-m5", "disk-scheduling", "Disk Scheduling",
        """Disk I/O cost is dominated by seek time — moving the arm between
cylinders dwarfs rotational latency and transfer time. So schedulers reorder
the request queue to minimize total head movement:

FCFS serves requests in arrival order. Fair, but the arm swings wildly (640
cylinders in the classic example below).

SSTF always serves the nearest pending request. Minimizes per-move distance
(236 in the example) but a steady stream of nearby requests can starve a
distant one.

SCAN (the elevator algorithm) sweeps in one direction, serving everything on
the way, then reverses. Fair like an elevator — no starvation, moderate total
movement.

C-SCAN sweeps one way serving requests, then jumps back to the start without
serving on the return trip. Gives more uniform wait times under heavy load.

LOOK is SCAN that reverses at the last request in each direction instead of
traveling to the disk's end — it skips the dead travel.

Worked example — requests 98, 183, 37, 122, 14, 124, 65, 67, head starts at 53:
FCFS: 45+85+146+85+108+110+59+2 = 640. SSTF order is 65, 67, 37, 14, 98, 122,
124, 183: 12+2+30+23+84+24+2+59 = 236. LOOK (moving up first, reversing at the
last request): 130 up to 183, then 146 down to 37, then 23 to 14 = 299.
Interview must-know: SSTF risks starvation, SCAN does not.""",
        4, estimated_minutes=45,
    ),
    _mkl(
        "os-m5-l5", "os-m5", "free-space-raid", "Free-Space Management & RAID",
        """The OS must track which disk blocks are free. Four approaches:

Bit vector: one bit per block. Finding n free blocks is fast, but the whole
vector must live in memory.

Linked list: free blocks chained together. Zero extra space, but finding a
contiguous run is slow.

Grouping: the first free block stores the addresses of n more free blocks —
the best of both worlds, and the standard choice.

Counting: store free runs as (address, count) pairs. Excellent when blocks are
allocated contiguously.

RAID (redundant array of independent disks) trades extra disks for speed and
reliability:

RAID 0 stripes data with no redundancy — capacity and speed add up, but one
disk dies and everything is lost.

RAID 1 mirrors every block — reads get faster, writes cost double, capacity
cost is 50%. Survives a disk failure trivially.

RAID 5 stripes blocks and distributes parity — survives one disk failure with
only 1/n capacity overhead, but writes pay a read-modify-write parity cost.
The datacenter default for years.

Interview line: RAID is not backup — it protects against disk failure, not
accidental deletion or corruption. Also know the hot spare and the rebuild
window, when the array is most vulnerable.""",
        5,
    ),
    _mkl(
        "os-m6-l1", "os-m6", "system-calls", "System Calls",
        """User programs cannot touch hardware directly — they ask the OS through
system calls, the controlled gate between user mode and kernel mode.

The classic set: process control (fork, exec, wait, exit), file management
(open, read, write, close), device management (ioctl), information maintenance
(getpid, sleep), communication (pipe, shmget), and protection (chmod).

Mechanics: the program loads the call number and arguments into registers and
executes a trap instruction (syscall on x86-64). The CPU switches to kernel
mode, jumps through the system-call table to the right handler, runs with full
privileges, then returns the result and drops back to user mode.

Why the gate exists: without it, any program could halt the machine or read
another process's memory. Every privileged action is funneled through kernel
code that validates it first.

Interview hook: a library call like printf eventually funnels into the write()
system call — the C library is a friendly wrapper, the trap is the real
boundary. Run strace on any Linux program and you can watch this live: open,
read, write, close marching past as the program runs.""",
        1,
    ),
    _mkl(
        "os-m6-l2", "os-m6", "kernel-vs-user-mode", "Kernel vs User Mode",
        """The CPU runs in at least two modes so the OS is protected from user
programs. The mode bit says which: user mode (restricted) or kernel /
supervisor mode (everything allowed).

Privileged instructions — I/O operations, halt, disabling interrupts, setting
the timer, writing to the mode bit, modifying page tables — trigger a hardware
trap if attempted in user mode. That is why a crashing user program cannot
take the whole machine down.

The dance: a user program runs in user mode, needs something privileged, makes
a system call or trap, the CPU switches to kernel mode, the kernel does the
work safely, and the return drops back to user mode.

This is what makes multi-user systems possible: your buggy program is caged
while the kernel is not. The OS itself always runs in kernel mode; everything
you launch runs in user mode.

Modern nuance: virtualization adds a hypervisor mode (ring -1) beneath the
kernel, and some architectures define more than two rings — but the interview
answer stays dual-mode: one bit, two privileges, and the trap as the only
legal crossing.""",
        2,
    ),
    _mkl(
        "os-m6-l3", "os-m6", "interrupts-traps-exceptions",
        "Interrupts, Traps & Exceptions",
        """Three events transfer control to the kernel:

Hardware interrupt: asynchronous, caused by devices — a key pressed, a disk
finishing, the timer ticking. The CPU finishes the current instruction, saves
state, and jumps to the interrupt service routine (ISR) via the interrupt
vector table, indexed by IRQ number.

Trap (software interrupt): synchronous and deliberate, caused by the executing
program itself. The system-call instruction is the canonical trap; debuggers
use breakpoint traps the same way.

Exception / fault: synchronous, caused by an error — divide by zero, page
fault, invalid opcode. The kernel either fixes it (page fault: load the page,
resume the instruction) or kills the process (segfault).

Why it matters: interrupts let the OS multiplex the CPU. The timer interrupt
is literally what makes preemptive multitasking possible — at every tick the
kernel gets control and the scheduler can steal the CPU back from a process
that never yields.

The vector table is the OS's dispatch board. Interviewers love "what happens
when you press a key?": the keyboard raises an IRQ, the CPU jumps through the
vector table to the ISR, the ISR buffers the scancode and wakes the waiting
process.""",
        3,
    ),
    _mkl(
        "os-m6-l4", "os-m6", "os-structures", "OS Structures",
        """How the OS itself is organized:

Monolithic: everything — scheduler, file system, drivers — runs in one big
kernel address space (classic Unix, Linux). Fast, because services call each
other directly, but a bug anywhere can crash the kernel.

Layered: the OS is a strict stack of layers, each using only the layer below
(the THE system). Clean and debuggable, but layer crossings cost performance
and strict layering is hard to maintain.

Microkernel: the kernel does almost nothing — just IPC, basic scheduling, and
memory primitives. Everything else (file systems, drivers) runs as user-space
servers (Mach, MINIX). Tiny trusted base, very stable; historically slower
because every service call is a message, not a function call.

Modular / hybrid: the modern answer — a monolithic core plus loadable kernel
modules (Linux modules, macOS's XNU hybrid kernel, modern Windows). You get
most of monolithic speed with microkernel-like extensibility: drivers load and
unload at runtime without rebooting.

Interview take: "why is Linux monolithic?" — performance and pragmatism;
modules add the flexibility without the IPC cost. If asked to design an OS for
a pacemaker vs a server, reach for microkernel (safety) vs monolithic/hybrid
(speed).""",
        4,
    ),
    _mkl(
        "os-m6-l5", "os-m6", "booting-system-programs", "Booting & System Programs",
        """Booting is how a dead machine becomes a running OS:

1. Power on: firmware (legacy BIOS, modern UEFI) runs POST and initializes
   hardware.
2. The firmware finds the boot device and loads the bootstrap loader (the boot
   block, e.g. GRUB).
3. The bootloader loads the kernel into memory and jumps to it.
4. The kernel initializes devices, mounts the root file system, and starts
   init — PID 1 (systemd on modern Linux).
5. init/systemd spawns services and the login prompt.

System programs vs application programs: system programs ship with the OS and
manage it — shells, compilers, file managers, status tools. They run in user
mode with no special magic; their power is just convenient access to system
calls. Application programs are everything else the user runs. The line is
about purpose, not privilege: ls is a system program, your game is an
application.

Interview classics: "what is the first process?" — init/systemd, PID 1, the
parent of all processes and adopter of orphans. "BIOS vs UEFI?" — UEFI reads
the bootloader as a file from an EFI partition; BIOS executed raw code from
the 446-byte MBR boot sector.""",
        5, estimated_minutes=30,
    ),
]

# ---------------------------------------------------------------- questions

QUESTIONS = [
    # ---- os-m5-l1 File Concepts (difficulties 2-7)
    _mkq("os-m5-l1-q1", "os-m5-l1", "file-systems", 2,
         "Which of the following is NOT a file attribute maintained by the OS?",
         ["The file's name", "The file's size in bytes",
          "The file's protection settings",
          "The text written inside the file"],
         3,
         "Name, size, and protection are metadata the OS stores in the directory "
         "entry so it can manage the file without reading it. The text inside is "
         "the file's data (content), not an attribute.",
         ["tcs", "infosys"]),
    _mkq("os-m5-l1-q2", "os-m5-l1", "file-systems", 3,
         "Which file operation repositions the read/write pointer without reading or writing any data?",
         ["read", "append", "seek", "truncate"],
         2,
         "seek (reposition) moves the file pointer to a new offset so the next "
         "read or write happens there. read consumes data, append writes at the "
         "end, and truncate empties the file.",
         ["wipro", "accenture"]),
    _mkq("os-m5-l1-q3", "os-m5-l1", "file-systems", 4,
         "Which statement about access methods is TRUE?",
         ["Direct access lets a program jump to any block without reading the blocks before it",
          "Sequential access is the fastest way to reach a random record",
          "Direct access requires reading every previous block first",
          "Sequential access needs an index block to work"],
         0,
         "Direct (random) access addresses blocks independently, so jumping to "
         "block N costs one seek, not N reads. Sequential access must pass "
         "through earlier records, and index blocks belong to indexed access, "
         "not sequential.",
         ["amazon", "microsoft"]),
    _mkq("os-m5-l1-q4", "os-m5-l1", "file-systems", 5,
         "A database engine stores fixed-size records and constantly jumps to record #N. Which access method fits best, and why?",
         ["Indexed access, because an index block maps logical records directly to physical blocks",
          "Sequential access, because fixed-size records are read fastest in order",
          "Linked allocation, because pointer chains give O(1) jumps",
          "Append-only access, because databases never re-read data"],
         0,
         "Jumping to record #N is a random-access pattern, and indexed access "
         "resolves the record-to-block mapping in O(1). Sequential access would "
         "force reading N-1 records first, and linked allocation makes random "
         "jumps O(n).",
         ["amazon", "google"]),
    _mkq("os-m5-l1-q5", "os-m5-l1", "file-systems", 6,
         "What is the difference between truncate() and delete()?",
         ["truncate() empties the file's contents but keeps its name and attributes; delete() removes the file entirely",
          "delete() empties the contents but keeps the attributes; truncate() removes the file",
          "They are identical operations with different names",
          "truncate() works only on directories, delete() only on files"],
         0,
         "truncate resets the file length to zero while the directory entry, "
         "name, and permissions survive. delete removes the directory entry "
         "(and frees the blocks once no handles remain). Interviewers use this "
         "to check you know metadata vs content.",
         ["google", "microsoft"]),
    _mkq("os-m5-l1-q6", "os-m5-l1", "file-systems", 7,
         "An OS supports both sequential and direct access on the same file. A program reads records in order, then occasionally re-reads an earlier record. Which mechanism makes the re-read efficient, and what breaks if the file lives on a tape drive?",
         ["The seek operation repositions the pointer for the re-read; on tape, direct positioning is impractical because tape is inherently sequential",
          "The append operation; tape drives cannot append data",
          "The inode; tape drives have no inodes",
          "Memory mapping; tape cannot be memory-mapped at all"],
         0,
         "seek gives O(1) repositioning on disk, so the occasional re-read is "
         "cheap. Tape is physically sequential — 'seeking' means fast-"
         "forwarding past everything in between, which destroys the "
         "performance the program assumed. The access method must match the "
         "medium.",
         ["microsoft", "amazon"]),

    # ---- os-m5-l2 Directory Structures (difficulties 2-7)
    _mkq("os-m5-l2-q1", "os-m5-l2", "file-systems", 2,
         "In a tree-structured directory, what does the path /home/user/docs represent?",
         ["A single file with a very long name",
          "Nesting of directories from the root down to docs",
          "A network address of a remote machine",
          "A physical disk sector address"],
         1,
         "A tree path is read left to right from the root: home contains user, "
         "which contains docs. That nesting is exactly what makes tree "
         "directories searchable recursively.",
         ["tcs", "wipro"]),
    _mkq("os-m5-l2-q2", "os-m5-l2", "file-systems", 3,
         "What is the main advantage of a two-level directory over a single-level directory?",
         ["Faster disk seek times",
          "Each user gets their own directory, so file names cannot collide across users",
          "It supports symbolic links",
          "Path names are no longer needed"],
         1,
         "The first level holds user names and the second holds each user's "
         "files, so two users can both have 'notes.txt'. It does not speed up "
         "the disk or add linking — those come with later designs.",
         ["infosys", "accenture"]),
    _mkq("os-m5-l2-q3", "os-m5-l2", "file-systems", 4,
         "What new problem do hard links (acyclic-graph directories) introduce that plain trees do not have?",
         ["File names can no longer be unique",
          "Path names become impossible to construct",
          "Deletion: the OS must track when the last link is removed before freeing the file",
          "Files can no longer be shared between users"],
         2,
         "With one file reachable from several directories, deleting one link "
         "must not free the blocks. The OS keeps a reference count and frees "
         "the file only when it reaches zero — bookkeeping trees never need.",
         ["amazon", "microsoft"]),
    _mkq("os-m5-l2-q4", "os-m5-l2", "file-systems", 5,
         "Why must the OS detect cycles when traversing a general graph directory structure?",
         ["Cycles corrupt the disk hardware",
          "Symbolic links can form cycles, so a naive search would loop forever",
          "Cycles make every file unreadable",
          "Hard links always create cycles by definition"],
         1,
         "A symlink can point to an ancestor directory (directly or through a "
         "chain), forming a cycle. Traversal without visited-set detection "
         "never terminates. Hard links cannot create cycles — that is the "
         "acyclic-graph guarantee.",
         ["google", "amazon"]),
    _mkq("os-m5-l2-q5", "os-m5-l2", "file-systems", 6,
         "A shared file has 3 hard links. One user deletes their link. What should happen, and how does the OS know?",
         ["The file is deleted immediately for everyone",
          "The file stays; a link count drops from 3 to 2, and the blocks are freed only when it reaches 0",
          "All remaining links break and must be repaired",
          "The file is copied privately to each remaining user"],
         1,
         "The directory entry removed is just one name pointing at the inode. "
         "The inode's link count decrements, and only the transition to zero "
         "frees the data blocks. This is why 'delete' on a hard-linked file "
         "does not necessarily delete data.",
         ["google", "microsoft"]),
    _mkq("os-m5-l2-q6", "os-m5-l2", "file-systems", 7,
         "Two teams must see the same project files in their own directories without duplicating data. Which structure fits, and what is its cost?",
         ["Single-level directory; no cost at all",
          "Two-level directory; the cost is slower search",
          "Acyclic-graph with hard links; the cost is reference-count bookkeeping, and directory hard links are forbidden to avoid cycles",
          "General graph with symlinks; there is no cost"],
         2,
         "Hard links give both teams real directory entries for the same inode "
         "with no duplication. The OS pays with link-count maintenance on every "
         "create/delete, and it bans hard links to directories precisely to "
         "keep the graph acyclic. Symlinks would also work but add indirection "
         "and cycle risk.",
         ["amazon", "tcs"]),
    # ---- os-m5-l3 File Allocation Methods (difficulties 2-7)
    _mkq("os-m5-l3-q1", "os-m5-l3", "file-systems", 2,
         "Which allocation method stores a file's blocks in consecutive disk sectors?",
         ["Linked allocation", "Contiguous allocation", "Indexed allocation",
          "Hashed allocation"],
         1,
         "Contiguous allocation lays blocks back-to-back on disk, which makes "
         "both sequential and direct access fast. Linked chains blocks with "
         "pointers and indexed uses an index block; neither is consecutive.",
         ["tcs", "infosys"]),
    _mkq("os-m5-l3-q2", "os-m5-l3", "file-systems", 3,
         "What is the main drawback of linked allocation for database-style random access?",
         ["It wastes half the disk to external fragmentation",
          "Files cannot grow once created",
          "Reaching block N requires walking N-1 pointers",
          "It needs one index block per data block"],
         2,
         "Linked allocation only stores the first block's address, so random "
         "access degrades to a linear walk of the chain. Its strengths are the "
         "opposite: no external fragmentation and free growth.",
         ["wipro", "accenture"]),
    _mkq("os-m5-l3-q3", "os-m5-l3", "file-systems", 4,
         "In Unix inode-based (indexed) allocation, what problem do indirect pointers solve?",
         ["They speed up sequential reads of small files",
          "They let files grow beyond what the direct pointers can address",
          "They eliminate internal fragmentation",
          "They replace the directory entry"],
         1,
         "A fixed set of direct pointers covers only small files. Single, "
         "double, and triple indirect blocks add levels of indirection, each "
         "multiplying the addressable size so huge files stay representable.",
         ["amazon", "microsoft"]),
    _mkq("os-m5-l3-q4", "os-m5-l3", "file-systems", 5,
         "Which allocation method suffers from external fragmentation, and why?",
         ["Linked, because pointers scatter blocks across the disk",
          "Indexed, because index blocks fragment the free space",
          "Contiguous, because it needs a run of consecutive free blocks, found via first-fit/best-fit search",
          "None of them; fragmentation only affects RAM"],
         2,
         "Contiguous allocation demands consecutive free sectors. Over time "
         "free space splinters into small runs (external fragmentation) and "
         "large files cannot be placed even when total free space suffices. "
         "Linked and indexed allocation place blocks anywhere, so they avoid "
         "it.",
         ["google", "amazon"]),
    _mkq("os-m5-l3-q5", "os-m5-l3", "file-systems", 6,
         "A 1-byte file on a 4KB-block indexed file system wastes nearly 4KB in its last block. Which fragmentation is this, and can disk compaction fix it?",
         ["External fragmentation; yes, compaction fixes it",
          "Internal fragmentation; no, compaction cannot fix it",
          "Internal fragmentation; yes, compaction fixes it",
          "External fragmentation; no, compaction cannot fix it"],
         1,
         "Wasted space inside an allocated block is internal fragmentation — "
         "the block belongs to the file, so rearranging blocks (compaction) "
         "changes nothing. Compaction only fixes external fragmentation, the "
         "scattering of free space.",
         ["microsoft", "google"]),
    _mkq("os-m5-l3-q6", "os-m5-l3", "file-systems", 7,
         "Small files are the common case, but occasional huge files exist. How does the combined inode scheme (direct + single/double/triple indirect pointers) serve both, and what does the huge file pay?",
         ["Small files use indirect pointers for safety; huge files use direct pointers for speed",
          "Small files are served by direct pointers with zero indirection and tiny overhead; huge files pay extra disk reads per indirect level on every access",
          "Both use the same single-indirect path, so there is no difference",
          "Small files are stored in the directory entry; huge files cannot be stored at all"],
         1,
         "A dozen direct pointers cover typical small files with a single disk "
         "read per block and just one inode of overhead. Huge files spill into "
         "indirect levels, where each access may first read an indirect block "
         "(or two, or three) — the classic space/speed trade-off made adaptive.",
         ["amazon", "microsoft"]),

    # ---- os-m5-l4 Disk Scheduling (difficulties 2-7)
    _mkq("os-m5-l4-q1", "os-m5-l4", "file-systems", 2,
         "Which component of disk access time do scheduling algorithms mainly try to reduce?",
         ["Transfer time", "Rotational latency", "Seek time",
          "Controller processing time"],
         2,
         "Moving the arm between cylinders (seek time) dominates the other "
         "components by orders of magnitude, so every classic algorithm — "
         "FCFS, SSTF, SCAN — is really a strategy for minimizing total head "
         "movement.",
         ["tcs", "infosys"]),
    _mkq("os-m5-l4-q2", "os-m5-l4", "file-systems", 3,
         "Request queue: 98, 183, 37, 122, 14, 124, 65, 67; head starts at 53. What is the total head movement under FCFS?",
         ["236 cylinders", "640 cylinders", "299 cylinders", "208 cylinders"],
         1,
         "FCFS serves in arrival order: 45 + 85 + 146 + 85 + 108 + 110 + 59 + "
         "2 = 640. The wild swings (183 down to 37, 122 down to 14) show why "
         "FCFS is fair but slow.",
         ["wipro", "accenture", "tcs"]),
    _mkq("os-m5-l4-q3", "os-m5-l4", "file-systems", 4,
         "Same queue (98, 183, 37, 122, 14, 124, 65, 67; head at 53). What is the total head movement under SSTF?",
         ["640 cylinders", "299 cylinders", "236 cylinders", "183 cylinders"],
         2,
         "SSTF always picks the nearest: 65 (12), 67 (2), 37 (30), 14 (23), 98 "
         "(84), 122 (24), 124 (2), 183 (59) = 236. Note 37 beats 98 from 67 "
         "(30 < 31) — nearest-first, not direction-first.",
         ["amazon", "microsoft"]),
    _mkq("os-m5-l4-q4", "os-m5-l4", "file-systems", 5,
         "Why can SSTF starve requests while SCAN cannot?",
         ["SSTF serves requests alphabetically, so late letters wait forever",
          "SSTF always picks the nearest request, so a steady stream of nearby requests can delay a distant one indefinitely; SCAN's sweep guarantees every request is eventually reached",
          "SCAN is always faster than SSTF on every workload",
          "SSTF cannot handle more than 8 requests in its queue"],
         1,
         "Starvation is SSTF's classic flaw: 'nearest' is a local decision "
         "with no fairness bound. SCAN's elevator sweep is a global pass — the "
         "arm must reach every cylinder in its path, so no request waits "
         "forever.",
         ["google", "amazon"]),
    _mkq("os-m5-l4-q5", "os-m5-l4", "file-systems", 6,
         "Same queue (98, 183, 37, 122, 14, 124, 65, 67; head at 53, moving toward larger cylinders). Under LOOK — which reverses at the last request in each direction instead of the disk end — what is the total head movement?",
         ["236 cylinders", "640 cylinders", "299 cylinders", "331 cylinders"],
         2,
         "Moving up: 65, 67, 98, 122, 124, 183 costs 130. LOOK reverses at 183 "
         "(the last request) instead of traveling to the disk end: 183 down to "
         "37 costs 146, then 37 to 14 costs 23. Total 130 + 146 + 23 = 299 — "
         "the saved dead travel is LOOK's whole advantage over SCAN.",
         ["microsoft", "google"]),
    _mkq("os-m5-l4-q6", "os-m5-l4", "file-systems", 7,
         "For a heavily loaded database server, why might C-SCAN give more uniform wait times than SCAN?",
         ["C-SCAN moves the arm twice as fast",
          "C-SCAN serves only while sweeping in one direction, so every cylinder waits at most one full sweep; SCAN serves on both passes, favoring middle cylinders",
          "C-SCAN uses SSTF within each sweep",
          "SCAN cannot handle heavy loads at all"],
         1,
         "Under SCAN, a request just missed by the arm waits almost two full "
         "sweeps, and middle cylinders get served on both the outward and "
         "return passes. C-SCAN's one-way service plus empty return equalizes "
         "the worst-case wait for all positions — uniformity at the cost of "
         "the empty return trip.",
         ["amazon", "microsoft"]),

    # ---- os-m5-l5 Free-Space Management & RAID (difficulties 2-7)
    _mkq("os-m5-l5-q1", "os-m5-l5", "file-systems", 2,
         "In the bit-vector method of free-space management, what does each bit represent?",
         ["One file on the disk", "One disk block — 1 means free, 0 means allocated (or vice versa)",
          "One user of the system", "One directory entry"],
         1,
         "The vector has one bit per disk block, so checking or finding free "
         "blocks is fast. The downside is size: the whole vector is usually "
         "kept in memory.",
         ["tcs", "infosys"]),
    _mkq("os-m5-l5-q2", "os-m5-l5", "file-systems", 3,
         "Which RAID level mirrors data across disks?",
         ["RAID 0", "RAID 1", "RAID 5", "RAID 10 is the only mirroring level"],
         1,
         "RAID 1 keeps a complete duplicate of every block on a second disk. "
         "RAID 0 stripes with no redundancy, RAID 5 uses distributed parity "
         "instead of full mirrors.",
         ["wipro", "accenture"]),
    _mkq("os-m5-l5-q3", "os-m5-l5", "file-systems", 4,
         "How many simultaneous disk failures can RAID 5 survive, and why?",
         ["Two, because parity is stored twice",
          "One, because distributed parity can reconstruct any single missing disk's data",
          "Zero — RAID 5 has no redundancy",
          "As many as there are disks"],
         1,
         "RAID 5 keeps one parity block per stripe (rotated across disks). "
         "XOR-ing the surviving blocks with the parity rebuilds exactly one "
         "missing disk. A second failure in the same stripe means data loss.",
         ["amazon", "microsoft"]),
    _mkq("os-m5-l5-q4", "os-m5-l5", "file-systems", 5,
         "A video-editing scratch disk needs maximum speed and capacity; all footage is backed up elsewhere nightly. Which RAID level fits, and why?",
         ["RAID 1, because mirroring doubles read speed",
          "RAID 0, because striping gives full capacity plus speed, and no redundancy is needed since backups exist",
          "RAID 5, because parity protects the scratch data",
          "No RAID — a single disk is always fastest"],
         1,
         "RAID 0's striping sums the throughput and capacity of all disks with "
         "zero redundancy overhead. Redundancy (RAID 1/5) costs capacity or "
         "write speed to protect data that is already protected by backups — "
         "paying twice for safety.",
         ["google", "amazon"]),
    _mkq("os-m5-l5-q5", "os-m5-l5", "file-systems", 6,
         "Why is RAID 5 write performance worse than RAID 0?",
         ["RAID 5 disks spin slower by design",
          "Every RAID 5 write needs a read-modify-write cycle to recompute parity",
          "RAID 5 cannot stripe data, only parity",
          "RAID 0 uses a write cache that RAID 5 lacks"],
         1,
         "Updating one data block forces the controller to read the old data "
         "and old parity, compute the new parity, and write both back — four "
         "I/Os per logical write. RAID 0 just stripes the write with no extra "
         "work. This 'write penalty' is RAID 5's famous cost.",
         ["microsoft", "google"]),
    _mkq("os-m5-l5-q6", "os-m5-l5", "file-systems", 7,
         "'RAID is not a backup.' A company runs RAID 1 and skips backups entirely. Name two failure modes RAID 1 does NOT protect against.",
         ["Slow disks and full disks",
          "Accidental deletion or corruption (mirrored instantly to both copies) and site disaster such as fire or flood",
          "Power loss and CPU failure",
          "RAID 1 protects against every failure mode"],
         1,
         "Mirroring duplicates everything — including your mistakes: delete a "
         "file and both copies vanish together, corrupt data and both copies "
         "are corrupt. And both disks usually sit in the same room, so fire, "
         "flood, or theft takes the 'backup' with the original. RAID covers "
         "disk failure; backups cover everything else.",
         ["amazon", "microsoft"]),
    # ---- os-m6-l1 System Calls (difficulties 2-7)
    _mkq("os-m6-l1-q1", "os-m6-l1", "system-concepts", 2,
         "Which of the following is a system call?",
         ["strlen() from the C library", "read(), which asks the kernel to fetch file data",
          "A CPU register name", "An HTML tag"],
         1,
         "read() crosses into the kernel via a trap to perform privileged I/O. "
         "strlen() is pure user-space computation in the C library — no kernel "
         "involvement at all.",
         ["tcs", "infosys"]),
    _mkq("os-m6-l1-q2", "os-m6-l1", "system-concepts", 3,
         "What triggers the switch from user mode to kernel mode when a program makes a system call?",
         ["A page fault", "The trap (syscall) instruction",
          "A timer interrupt", "A power failure"],
         1,
         "The program deliberately executes a trap instruction with the call "
         "number in a register. The CPU then switches to kernel mode and "
         "dispatches through the system-call table. Interrupts and faults are "
         "different entry paths into the kernel.",
         ["wipro", "accenture"]),
    _mkq("os-m6-l1-q3", "os-m6-l1", "system-concepts", 4,
         "Why must open() be a system call rather than an ordinary library function?",
         ["Library functions cannot take string arguments",
          "Only the kernel can safely check permissions and manage the shared open-file table",
          "System calls run faster than library functions",
          "open() needs to allocate RAM directly"],
         1,
         "Opening a file touches shared kernel state — permission checks "
         "against the file's metadata and an entry in the system-wide "
         "open-file table. Letting user code do that directly would let any "
         "program bypass permissions.",
         ["amazon", "microsoft"]),
    _mkq("os-m6-l1-q4", "os-m6-l1", "system-concepts", 5,
         'A program calls printf("hi"). Which system call actually moves those bytes toward the screen?',
         ["fork()", "write()", "exec()", "malloc()"],
         1,
         "printf formats the text in user space (C library), then funnels the "
         "bytes through the write() system call — the real kernel boundary. "
         "fork/exec manage processes, and malloc never touches the kernel per "
         "call.",
         ["google", "amazon"]),
    _mkq("os-m6-l1-q5", "os-m6-l1", "system-concepts", 6,
         'What does strace show you, and why is it the first tool to reach for when a program fails with "cannot open file"?',
         ["The program's source code, so you can recompile it",
          "Every system call with its arguments and return values; the failing open() reveals the exact path tried and the errno",
          "The CPU temperature during execution",
          "Only the network packets the program sent"],
         1,
         "strace traces the kernel boundary. A failed open() line shows "
         "precisely which path was attempted and why it failed (ENOENT, "
         "EACCES, ...), turning a vague error message into a diagnosis in one "
         "look.",
         ["microsoft", "google"]),
    _mkq("os-m6-l1-q6", "os-m6-l1", "system-concepts", 7,
         "If user programs could execute privileged I/O instructions directly, what breaks? Connect this to why the trap gate exists.",
         ["Nothing — programs would simply run faster",
          "Any buggy or malicious program could corrupt other processes' data or halt the machine; the trap forces all privileged work through kernel validation",
          "The CPU would overheat",
          "System calls would become unnecessary because libraries are faster"],
         1,
         "Privileged instructions are the keys to shared hardware. The trap "
         "gate exists so every use passes through kernel code that validates "
         "permissions first. Remove the gate and one bad pointer in any "
         "program can scribble over another process's disk blocks or stop the "
         "machine.",
         ["amazon", "microsoft"]),

    # ---- os-m6-l2 Kernel vs User Mode (difficulties 2-7)
    _mkq("os-m6-l2-q1", "os-m6-l2", "system-concepts", 2,
         "Which mode is allowed to execute privileged instructions like halt or direct I/O?",
         ["User mode", "Kernel (supervisor) mode", "Safe mode", "Debug mode"],
         1,
         "Only kernel mode may run privileged instructions. User mode attempts "
         "trap as hardware violations — that single rule is what keeps a "
         "crashing app from taking down the machine.",
         ["tcs", "wipro"]),
    _mkq("os-m6-l2-q2", "os-m6-l2", "system-concepts", 3,
         "What is the mode bit used for?",
         ["To select which user is logged in",
          "To tell the CPU whether the currently running code may execute privileged instructions",
          "To enable the floating-point unit",
          "To switch between 32-bit and 64-bit programs"],
         1,
         "The mode bit is hardware state: 0 (kernel) means full privilege, 1 "
         "(user) means restricted. The CPU checks it on every privileged "
         "instruction — it is the actual enforcement mechanism.",
         ["infosys", "accenture"]),
    _mkq("os-m6-l2-q3", "os-m6-l2", "system-concepts", 4,
         "A user program tries to execute 'disable interrupts'. What happens?",
         ["It succeeds; interrupts are per-process",
          "The hardware traps — the attempt fails as a privilege violation",
          "The program is moved to kernel mode permanently",
          "Nothing; the instruction is ignored silently"],
         1,
         "Disabling interrupts is privileged because it would let a process "
         "block the timer tick and monopolize the CPU. The CPU traps the "
         "attempt, and the kernel typically terminates the offender.",
         ["amazon", "microsoft"]),
    _mkq("os-m6-l2-q4", "os-m6-l2", "system-concepts", 5,
         "During a system call, when does the mode switch to kernel and back?",
         ["It never switches; system calls run in user mode",
          "The trap instruction switches user to kernel; the return-from-syscall switches kernel back to user",
          "It switches to kernel at boot and stays there",
          "The mode flips on every clock tick regardless"],
         1,
         "The trap is the user-to-kernel door and the syscall return is the "
         "way back. Between them the handler runs fully privileged; after the "
         "return the program resumes exactly where it trapped, in user mode.",
         ["google", "microsoft"]),
    _mkq("os-m6-l2-q5", "os-m6-l2", "system-concepts", 6,
         "Why do device drivers traditionally run in kernel mode, and what is the risk?",
         ["They need privileged I/O instructions to talk to hardware; a driver bug can crash the entire kernel",
          "They run faster in user mode; the risk is slowness",
          "Kernel mode gives them more RAM; the risk is memory waste",
          "There is no reason; it is purely historical"],
         0,
         "Talking to device registers requires privileged I/O, so drivers "
         "live in the kernel. The price: a null pointer in a driver is a "
         "kernel panic, not a segfault — which is why microkernels push "
         "drivers to user space.",
         ["amazon", "google"]),
    _mkq("os-m6-l2-q6", "os-m6-l2", "system-concepts", 7,
         'Virtualization adds a hypervisor "ring -1" beneath the kernel. Why does this not break the dual-mode protection model?',
         ["It does break it; virtualized kernels have no protection",
          "The guest kernel still cannot touch real hardware — its privileged attempts trap to the hypervisor, which emulates them, so the protection principle recurses one level down",
          "Rings below zero disable the mode bit entirely",
          "The hypervisor runs all guest code in user mode permanently"],
         1,
         "The model is fractal: each layer believes it is privileged while the "
         "layer below actually enforces. The guest kernel's 'privileged' "
         "instructions trap to the hypervisor exactly as user instructions "
         "trap to the kernel.",
         ["microsoft", "amazon"]),

    # ---- os-m6-l3 Interrupts, Traps & Exceptions (difficulties 2-7)
    _mkq("os-m6-l3-q1", "os-m6-l3", "system-concepts", 2,
         "A keypress is delivered to the OS via...",
         ["A system call made by the keyboard", "A hardware interrupt",
          "A page fault", "A trap instruction in the text editor"],
         1,
         "The keyboard controller raises an IRQ — asynchronous hardware "
         "signaling. The CPU finishes its current instruction, then jumps to "
         "the keyboard's interrupt service routine.",
         ["tcs", "infosys"]),
    _mkq("os-m6-l3-q2", "os-m6-l3", "system-concepts", 3,
         "What is the interrupt vector table?",
         ["A list of all running processes",
          "An array mapping each interrupt number to the address of its handler (ISR)",
          "The hard disk's bad-sector list",
          "A table of file permissions"],
         1,
         "When interrupt N fires, the CPU indexes the table at N and jumps to "
         "the stored handler address. It is the OS's dispatch board — without "
         "it the CPU would not know which code serves which device.",
         ["wipro", "accenture"]),
    _mkq("os-m6-l3-q3", "os-m6-l3", "system-concepts", 4,
         "What is the key difference between a trap and a hardware interrupt?",
         ["Traps are faster than interrupts",
          "A trap is synchronous and deliberate — caused by the running program itself (e.g. a syscall); a hardware interrupt is asynchronous, caused by a device or timer independent of the current instruction",
          "Interrupts run in user mode, traps in kernel mode",
          "There is no difference; the terms are synonyms"],
         1,
         "Synchronous vs asynchronous is the dividing line. A trap is the "
         "program asking for the kernel; an interrupt is the outside world "
         "demanding attention. Both end up in kernel handlers, but their "
         "causes — and timing guarantees — differ.",
         ["amazon", "microsoft"]),
    _mkq("os-m6-l3-q4", "os-m6-l3", "system-concepts", 5,
         "A page fault and a divide-by-zero are both exceptions, but the OS treats them very differently. How?",
         ["Both always kill the process immediately",
          "A page fault is fixable — the kernel loads the missing page and resumes the instruction; a divide-by-zero is fatal and the process is terminated",
          "A divide-by-zero is fixable but a page fault is fatal",
          "Neither can be handled; both panic the kernel"],
         1,
         "Exceptions split into recoverable faults and fatal ones. The page "
         "fault is the happy case the virtual-memory system depends on: fix "
         "the cause, retry the instruction, the program never notices. "
         "Arithmetic faults have no fix, so the process dies.",
         ["google", "amazon"]),
    _mkq("os-m6-l3-q5", "os-m6-l3", "system-concepts", 6,
         "How does the timer interrupt enable preemptive multitasking?",
         ["It speeds up the CPU clock",
          "Each tick hands control to the kernel, letting the scheduler preempt the running process even if it never yields",
          "It pauses all I/O devices periodically",
          "It forces every process to call yield()"],
         1,
         "Without the timer, a process that never makes a system call could "
         "hold the CPU forever (cooperative multitasking's flaw). The periodic "
         "tick guarantees the kernel regains control and can switch processes "
         "— preemption by hardware.",
         ["microsoft", "google"]),
    _mkq("os-m6-l3-q6", "os-m6-l3", "system-concepts", 7,
         '"What happens when you press a key?" Trace the path from hardware to the waiting program.',
         ["The key press directly writes into the program's memory",
          "The keyboard raises an IRQ; the CPU jumps via the vector table to the ISR; the ISR buffers the scancode and wakes the blocked reader process, which the scheduler eventually runs",
          "The program polls the keyboard in a loop until it notices",
          "The shell makes a system call on behalf of the keyboard"],
         1,
         "Full chain: hardware IRQ → vector-table dispatch → ISR runs "
         "(buffers input, marks the waiting process runnable) → scheduler "
         "picks it up. This single path exercises interrupts, the vector "
         "table, ISRs, blocking/wakeup, and scheduling — which is why "
         "interviewers love the question.",
         ["amazon", "microsoft"]),
    # ---- os-m6-l4 OS Structures (difficulties 2-7)
    _mkq("os-m6-l4-q1", "os-m6-l4", "system-concepts", 2,
         "Linux is traditionally described as which kind of kernel structure?",
         ["Microkernel", "Monolithic", "Layered", "Exokernel"],
         1,
         "Linux runs the scheduler, file systems, and drivers in one big "
         "kernel address space — the monolithic design. Loadable modules add "
         "flexibility, but the core remains monolithic.",
         ["tcs", "infosys"]),
    _mkq("os-m6-l4-q2", "os-m6-l4", "system-concepts", 3,
         "What is the main advantage of a microkernel's tiny trusted base?",
         ["It uses less disk space for the source code",
          "Less privileged code means fewer catastrophic bugs, and crashed services are isolated in user space instead of panicking the kernel",
          "It boots faster on every machine",
          "It needs no device drivers at all"],
         1,
         "In a microkernel only IPC, scheduling, and memory primitives run "
         "privileged. A file-server crash restarts the server; in a "
         "monolithic kernel the same bug panics everything. Small trusted "
         "base = small blast radius.",
         ["wipro", "accenture"]),
    _mkq("os-m6-l4-q3", "os-m6-l4", "system-concepts", 4,
         "Why was classic microkernel IPC considered a performance problem?",
         ["Messages travel over the network",
          "Every service call crosses protection boundaries via message passing instead of a cheap direct function call",
          "Microkernels cannot use the CPU cache",
          "IPC requires a disk write per message"],
         1,
         "A monolithic file read is a function call; on a pure microkernel it "
         "is a message to a user-space server — context switches and copies "
         "each way. That overhead is the historic knock on Mach-style designs.",
         ["amazon", "microsoft"]),
    _mkq("os-m6-l4-q4", "os-m6-l4", "system-concepts", 5,
         "How do loadable kernel modules give Linux microkernel-like flexibility without the IPC cost?",
         ["They run in user space like microkernel servers",
          "Drivers and file systems load into kernel space and run as direct function calls, and can be loaded or unloaded at runtime",
          "They replace system calls with network RPCs",
          "They move the scheduler into user space"],
         1,
         "Modules are the hybrid trick: extensibility (load/unload drivers "
         "without rebooting, like adding a microkernel server) with "
         "monolithic speed (a direct call once loaded, no message passing).",
         ["google", "amazon"]),
    _mkq("os-m6-l4-q5", "os-m6-l4", "system-concepts", 6,
         "In a layered OS (like the THE system), what is the debugging advantage and the performance cost?",
         ["No advantage; layers only slow things down",
          "Each layer is testable in isolation since it uses only lower layers; the cost is overhead from strictly crossing every layer boundary",
          "Layers eliminate all bugs; the cost is higher memory use",
          "The advantage is speed; the cost is complexity"],
         1,
         "Layering gives you unit-testable slices of an OS — debug layer 3 "
         "using only the verified layer 2. But a request that could jump "
         "straight to hardware must politely descend every layer, and that "
         "discipline costs cycles.",
         ["microsoft", "google"]),
    _mkq("os-m6-l4-q6", "os-m6-l4", "system-concepts", 7,
         "macOS's XNU kernel is called a hybrid. What does it hybridize, and why?",
         ["It mixes Linux and Windows source code",
          "It combines Mach microkernel IPC with BSD monolithic services in one kernel — Mach messaging where useful, BSD direct calls for speed",
          "It runs two kernels side by side for redundancy",
          "It switches between monolithic and microkernel at boot time"],
         1,
         "XNU keeps Mach's IPC and object model for things like inter-process "
         "communication, but runs the BSD subsystem (file systems, "
         "networking, process model) monolithically in the same address space. "
         "Pragmatism over purity: pay IPC cost only where its abstraction "
         "earns it.",
         ["amazon", "microsoft"]),

    # ---- os-m6-l5 Booting & System Programs (difficulties 2-7)
    _mkq("os-m6-l5-q1", "os-m6-l5", "system-concepts", 2,
         "What runs first when you power on a PC?",
         ["The operating system kernel", "Firmware — BIOS or UEFI",
          "The login screen", "The bootloader GRUB"],
         1,
         "Firmware is burned into the motherboard and is the only code the CPU "
         "can reach at power-on. It runs POST, initializes hardware, and only "
         "then loads the bootloader, which loads the kernel.",
         ["tcs", "infosys"]),
    _mkq("os-m6-l5-q2", "os-m6-l5", "system-concepts", 3,
         "What is the bootstrap loader's job?",
         ["To check the RAM for errors",
          "To load the kernel into memory and start it",
          "To log the user in",
          "To install device drivers permanently"],
         1,
         "The firmware is too small to understand file systems fully, so it "
         "loads a slightly smarter program — the bootloader (e.g. GRUB) — "
         "whose whole purpose is finding, loading, and jumping to the kernel.",
         ["wipro", "accenture"]),
    _mkq("os-m6-l5-q3", "os-m6-l5", "system-concepts", 4,
         "What is PID 1 on modern Linux, and why does it matter?",
         ["The shell; it interprets user commands",
          "systemd (init); it is the parent of all processes, adopts orphans, and starts system services",
          "The kernel itself",
          "The login manager only"],
         1,
         "PID 1 is the first user-space process the kernel starts and the "
         "ancestor of everything. Orphaned processes get reparented to it so "
         "someone always reaps them, and it brings up services at boot.",
         ["amazon", "microsoft"]),
    _mkq("os-m6-l5-q4", "os-m6-l5", "system-concepts", 5,
         "Is the shell special to the kernel? What separates a system program from an application program?",
         ["Yes; the shell runs in kernel mode",
          "No — the shell is an ordinary user-mode program; system programs differ from applications by purpose (managing/using the OS), not privilege",
          "Yes; only the shell may make system calls",
          "No difference exists at all"],
         1,
         "Anyone can write a shell — it is just a program that reads input and "
         "calls fork/exec. 'System program' (shell, compiler, ls) vs "
         "'application' (your game) is about role: both are unprivileged user "
         "code talking to the kernel through the same system calls.",
         ["google", "amazon"]),
    _mkq("os-m6-l5-q5", "os-m6-l5", "system-concepts", 6,
         "Why does the kernel mount the root filesystem before starting init?",
         ["It is just tradition; the order does not matter",
          "init and every later program live as files — without a mounted root, the kernel cannot load the first user-space program",
          "Mounting requires init to be running first",
          "The root filesystem contains the kernel itself"],
         1,
         "The kernel ends its own boot by executing a file (/sbin/init). Files "
         "require a mounted filesystem, so mounting root is the bridge from "
         "'kernel running' to 'user space exists'. No mount, no init, no "
         "users.",
         ["microsoft", "google"]),
    _mkq("os-m6-l5-q6", "os-m6-l5", "system-concepts", 7,
         "UEFI vs legacy BIOS boot: what fundamentally changed about the bootloader stage?",
         ["UEFI removed the bootloader entirely",
          "UEFI reads the bootloader as an ordinary file from an EFI system partition, instead of executing raw code from the MBR's 446-byte boot sector",
          "BIOS was faster because it skipped firmware",
          "UEFI boots directly into the kernel with no loader"],
         1,
         "The MBR gave bootloaders 446 bytes of raw sector code — famously "
         "cramped, hence multi-stage loaders like GRUB. UEFI is a mini-OS "
         "that understands FAT partitions, so the bootloader is just a file "
         "it executes. Same job, civilized interface.",
         ["amazon", "microsoft"]),
]
