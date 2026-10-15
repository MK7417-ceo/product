"""SkillForge COA curriculum — Part 5/6: I/O Systems & Advanced Topics.

GATE + interview focused content for the Computer Organization &
Architecture deep track. All theory and questions are original material
written for this curriculum (not copied from any textbook or bank).

Modules:
  - io-systems : I/O methods, DMA, buses & arbitration, RAID, storage
  - advanced   : SMP/NUMA, Flynn's taxonomy, Amdahl's law,
                 Gustafson's law, GPU architecture

Export: MODULES (a list of 2 module dicts, 10 lessons, 60 MCQs).
"""

from __future__ import annotations


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
    assert max(diffs) - min(diffs) >= 4, f"lesson {slug}: difficulty span too narrow"
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


MODULES = [
    M(
        "io-systems",
        "I/O Systems",
        "I/O methods, DMA, buses, RAID, storage devices.",
        [
            L(
                "io-methods",
                "I/O Methods: Programmed, Interrupt, DMA",
                """# I/O Methods: Programmed, Interrupt, DMA

Three ways a CPU moves data with devices — differing in CPU involvement.

## 1. Programmed I/O (polling)
The CPU does everything: it repeatedly reads the device status register
until ready, then moves each word itself. Simple hardware, but the CPU
busy-waits — burning cycles doing nothing useful. Only sane for very
fast devices or tiny transfers.

## 2. Interrupt-driven I/O
The CPU starts the operation, does other work, and the device raises an
interrupt when done; the CPU jumps to an interrupt service routine (ISR)
that moves the data. The CPU is free between transfers, but every word
(or chunk) costs an interrupt + context switch — a fast disk streaming
megabytes drowns the CPU in interrupts.

## 3. DMA (Direct Memory Access)
A DMA controller moves the whole block between device and memory
directly. The CPU only programs source/destination/count, then gets one
interrupt when the block finishes. (Next lesson covers DMA in depth.)

## Comparison
| Aspect            | Programmed I/O     | Interrupt-driven     | DMA                  |
|-------------------|--------------------|----------------------|----------------------|
| CPU per word      | moves each word    | moves each word      | moves nothing        |
| CPU while waiting | busy-wait (wasted) | free, does real work | free, does real work |
| Interrupts/block  | 0                  | one per word/chunk   | one per block        |
| Hardware cost     | minimal            | interrupt logic      | DMA controller       |
| Best for          | fast/tiny xfers    | medium-rate devices  | bulk high-speed xfers|

**Rule of thumb:** programmed I/O = CPU-bound, interrupt I/O = per-word
overhead, DMA = per-block overhead. Faster device + bigger transfer →
move down the table.""",
                [
                    Q(
                        "In programmed I/O, how does the CPU know when an I/O device is ready?",
                        [
                            "It repeatedly polls the device status register until ready",
                            "The device raises an interrupt when ready",
                            "The DMA controller signals completion",
                            "The OS scheduler notifies the process",
                        ],
                        0,
                        1,
                        "Programmed I/O is polling-based: the CPU busy-waits on the status register. Interrupts belong to interrupt-driven I/O, and DMA uses a controller.",
                        ["gate", "tcs", "infosys"],
                    ),
                    Q(
                        "Which I/O method leaves the CPU free to do other work while waiting for the device?",
                        [
                            "Programmed I/O only",
                            "Interrupt-driven I/O",
                            "Neither — the CPU always waits",
                            "Only DMA with burst mode",
                        ],
                        1,
                        2,
                        "In interrupt-driven I/O the CPU starts the operation and works on other tasks until the device interrupts. Programmed I/O busy-waits instead.",
                        ["gate", "wipro", "tcs"],
                    ),
                    Q(
                        "A fast disk streams a 10 MB file. Why is interrupt-driven I/O a poor choice here compared to DMA?",
                        [
                            "Interrupts cannot be used with disks at all",
                            "Each word/chunk triggers an interrupt, so interrupt overhead dominates the transfer",
                            "DMA is always slower than interrupts",
                            "The CPU cannot run an ISR during disk transfers",
                        ],
                        1,
                        4,
                        "Interrupt-driven I/O pays a context-switch cost per word or small chunk; for bulk transfers that overhead dwarfs useful work. DMA reduces this to one interrupt per block.",
                        ["gate", "amazon", "google"],
                    ),
                    Q(
                        "Rank these by CPU involvement per transfer, from most to least:",
                        [
                            "DMA > interrupt-driven > programmed",
                            "Programmed > interrupt-driven > DMA",
                            "Interrupt-driven > DMA > programmed",
                            "All three involve the CPU equally",
                        ],
                        1,
                        5,
                        "Programmed I/O moves every word on the CPU and busy-waits; interrupt-driven still moves words on the CPU but frees it between; DMA moves nothing on the CPU.",
                        ["gate", "microsoft"],
                    ),
                    Q(
                        "An ISR for a keyboard takes 50 us to run, and keys arrive at most 10 per second. What is the approximate CPU overhead of interrupt-driven keyboard input?",
                        [
                            "50 us x 10 = 500 us per second, about 0.05% — negligible",
                            "50 us x 10 = 500 ms per second — 50% overhead",
                            "Cannot be computed without the clock speed",
                            "10 x 50 us = 5 ms per key — too slow for typing",
                        ],
                        0,
                        7,
                        "10 interrupts/s x 50 us = 500 us/s = 0.05% of CPU time — negligible. Interrupt-driven I/O is ideal for slow, infrequent devices like keyboards.",
                        ["gate", "google"],
                    ),
                    Q(
                        "A designer proposes programmed I/O for a gigabit network card receiving full-rate traffic. What is the fundamental flaw?",
                        [
                            "Network cards do not have status registers",
                            "Polling cannot keep up: the CPU would spend all its time busy-waiting and moving words, starving real work",
                            "Programmed I/O requires a DMA controller",
                            "Interrupts are disabled during polling loops",
                        ],
                        1,
                        9,
                        "At gigabit rates the CPU would be trapped in the poll-and-copy loop with zero time for useful work — exactly the regime where interrupt-driven or DMA I/O is required.",
                        ["gate", "amazon", "nvidia"],
                    ),
                ],
            ),
            L(
                "io-dma",
                "DMA: Direct Memory Access",
                """# DMA: Direct Memory Access

The DMA controller is a dedicated engine that moves blocks between an
I/O device and main memory while the CPU does other work.

## Steps of a DMA transfer
1. **Program:** CPU writes source address, destination address, and
   word count into the controller's registers; the device is started.
2. **Request:** the device asserts DMA request (DREQ) when ready.
3. **Grant:** the controller requests the bus (HOLD); the CPU replies
   with hold-acknowledge (HLDA) and releases the buses.
4. **Transfer:** the controller puts addresses on the bus and moves
   data directly between device and memory, word per cycle.
5. **Complete:** count hits zero → controller releases the bus and
   raises one interrupt; the CPU's ISR does final bookkeeping.

## Transfer modes
* **Cycle stealing:** bus grabbed one cycle at a time, only when the
  CPU isn't using it. CPU slightly slowed, never blocked. Most common.
* **Burst (block) mode:** controller holds the bus for the whole block.
  Fastest, but the CPU stalls throughout. For devices that can't wait.
* **Transparent mode:** transfers only in cycles the CPU provably
  doesn't need — zero CPU impact, slowest DMA.

## Why it matters
A 1 MB disk read at 4 bytes/word is ~250,000 words: per-word interrupts
would drown the CPU; DMA reduces it to one interrupt plus setup.
Cycle-stealing vs burst is the classic tradeoff: granularity of CPU
blocking vs transfer throughput. Note the coherence catch: DMA writes
memory directly, bypassing CPU caches — modern systems use
cache-coherent DMA / IOMMU invalidation to avoid stale cached copies.

**GATE facts:** the word-count register decrements per transfer while
the address increments; the CPU is interrupted only at end of block.""",
                [
                    Q(
                        "What is the main job of a DMA controller?",
                        [
                            "To run the operating system's scheduler",
                            "To move blocks of data between device and memory without CPU per-word involvement",
                            "To convert virtual addresses to physical addresses",
                            "To encrypt data before it reaches the disk",
                        ],
                        1,
                        1,
                        "The DMA controller is a dedicated engine that transfers whole blocks directly between device and memory; the CPU only sets it up and gets one interrupt at the end.",
                        ["gate", "tcs", "infosys"],
                    ),
                    Q(
                        "Which registers must the CPU program into the DMA controller before a transfer starts?",
                        [
                            "Program counter and stack pointer",
                            "Source address, destination address, and word count",
                            "Cache tags and TLB entries",
                            "Interrupt vector and priority level",
                        ],
                        1,
                        3,
                        "A DMA transfer is fully described by where data comes from, where it goes, and how many words to move — the controller handles the rest.",
                        ["gate", "wipro"],
                    ),
                    Q(
                        "In cycle-stealing DMA mode, what happens to the CPU during the transfer?",
                        [
                            "The CPU is fully halted until the block completes",
                            "The CPU loses occasional single bus cycles but otherwise keeps running",
                            "The CPU runs at double speed to compensate",
                            "The CPU is switched to a different process",
                        ],
                        1,
                        4,
                        "Cycle stealing grabs the bus one cycle at a time, so the CPU is only slightly slowed, never fully blocked — unlike burst mode, which stalls the CPU for the whole block.",
                        ["gate", "amazon"],
                    ),
                    Q(
                        "During a DMA transfer, the word-count register reaches zero. What happens next?",
                        [
                            "The controller immediately starts the next block on its own",
                            "The controller releases the bus and raises an interrupt to notify the CPU",
                            "The CPU polls the controller to discover completion",
                            "The device keeps sending data until the CPU stops it",
                        ],
                        1,
                        5,
                        "Zero count = block complete: the controller gives up the bus and interrupts once. That single end-of-block interrupt is the whole point of DMA.",
                        ["gate", "microsoft", "google"],
                    ),
                    Q(
                        "A 1 MB disk read uses 4-byte words. Roughly how many interrupts does DMA save compared to per-word interrupt-driven I/O?",
                        [
                            "About 10",
                            "About 1,000",
                            "About 250,000 — one interrupt instead of one per word",
                            "None; both use exactly one interrupt",
                        ],
                        2,
                        7,
                        "1 MB / 4 bytes = 262,144 words ≈ 250K interrupts under per-word I/O, versus exactly 1 with DMA. This is why DMA exists for bulk transfers.",
                        ["gate", "nvidia"],
                    ),
                    Q(
                        "A CPU caches memory location X. A DMA controller then writes new data directly to X in RAM. What hazard does this create, and how do modern systems handle it?",
                        [
                            "No hazard — caches update automatically",
                            "Stale cache: the CPU may read the old cached copy; handled with cache-coherent DMA or IOMMU invalidation",
                            "The DMA transfer is automatically cancelled",
                            "The hazard is avoided by disabling interrupts",
                        ],
                        1,
                        9,
                        "DMA bypasses the CPU cache, so cached copies go stale. Modern systems use cache-coherent interconnects or IOMMU-based invalidation/flushing to keep memory consistent.",
                        ["gate", "google", "amazon"],
                    ),
                ],
            ),
            L(
                "io-buses",
                "Buses & Arbitration",
                """# Buses & Arbitration

A **bus** is a shared set of wires linking CPU, memory, and I/O:
* **Data bus** — carries data (bidirectional); width = bits/transfer.
* **Address bus** — carries the address; 32 bits → 2^32 = 4 GiB.
* **Control bus** — read/write, clock, interrupt, request/grant.

## Bandwidth math (worked)
Bandwidth = (bus width in bytes) × (transfers per second).

**Example:** 64-bit bus at 100 MHz, one transfer per clock:
* 64 bits = 8 bytes per transfer
* 100 MHz = 100 × 10^6 transfers/second
* Bandwidth = 8 × 100 × 10^6 = **800 MB/s** (verified)

Double the width or the clock → double the bandwidth. (DDR buses do 2
transfers per clock — watch for that multiplier in GATE questions.)

## Synchronous vs asynchronous
* **Synchronous:** common clock times everything. Simple, but every
  device must meet the slowest device's timing.
* **Asynchronous:** no common clock; devices handshake with
  request/acknowledge signals. Slower per transfer, but mixed-speed
  devices coexist.

## Bus arbitration — who gets the bus?
* **Daisy chaining:** grant ripples through devices in fixed order.
  Cheap, but priority is fixed by position and a broken device kills
  the chain.
* **Centralized:** an arbiter collects requests, grants by priority or
  round-robin. Flexible and fairer, more hardware.
* **Distributed:** devices negotiate among themselves using priority
  codes (used in some modern buses).

## PCIe lanes
PCIe replaced the shared parallel bus with serial **lanes** (~1 GB/s
per direction per lane in PCIe 3.0). A x16 slot ≈ 16 GB/s each way.
Bandwidth scales by adding lanes; point-to-point links remove most
arbitration fights.""",
                [
                    Q(
                        "Which bus carries the memory address of the data being accessed?",
                        [
                            "Data bus",
                            "Address bus",
                            "Control bus",
                            "PCIe lane",
                        ],
                        1,
                        1,
                        "The address bus carries the location (CPU to memory/device); the data bus carries the contents; the control bus carries command signals.",
                        ["gate", "tcs", "infosys"],
                    ),
                    Q(
                        "A 32-bit address bus can directly address how much memory?",
                        [
                            "32 MB",
                            "4 GB",
                            "32 GB",
                            "2^32 bits = 512 MB",
                        ],
                        1,
                        3,
                        "2^32 addresses x 1 byte each = 4 GiB. Address width sets the addressable space; data width sets transfer size.",
                        ["gate", "wipro"],
                    ),
                    Q(
                        "A 64-bit bus runs at 100 MHz with one transfer per clock. What is its peak bandwidth?",
                        [
                            "640 MB/s",
                            "800 MB/s",
                            "100 MB/s",
                            "6.4 GB/s",
                        ],
                        1,
                        4,
                        "64 bits = 8 bytes per transfer; 8 x 100M transfers/s = 800 MB/s. (Verified: 8 * 100e6 = 800e6 bytes/s.)",
                        ["gate", "amazon"],
                    ),
                    Q(
                        "Why would a designer choose an asynchronous bus over a synchronous one?",
                        [
                            "It is always faster per transfer",
                            "Devices of different speeds can share the bus using handshake signals instead of a common clock",
                            "It needs no control lines at all",
                            "It eliminates the need for arbitration",
                        ],
                        1,
                        6,
                        "Asynchronous buses use request/acknowledge handshakes, so slow and fast devices coexist — at the cost of per-transfer speed versus a clocked synchronous bus.",
                        ["gate", "google"],
                    ),
                    Q(
                        "In daisy-chain arbitration, what is the main drawback compared to centralized arbitration?",
                        [
                            "It requires more wires than centralized arbitration",
                            "Priority is fixed by physical position and one faulty device can break the whole chain",
                            "It cannot handle more than two devices",
                            "It is slower because of the central arbiter bottleneck",
                        ],
                        1,
                        7,
                        "Daisy chaining is cheap but rigid: grant signals ripple in fixed order, so priority depends on position and a broken link kills arbitration for everyone downstream.",
                        ["gate", "microsoft"],
                    ),
                    Q(
                        "A PCIe 3.0 x16 slot offers roughly 16 GB/s per direction. A device needs 40 GB/s full-duplex. Which is true?",
                        [
                            "A single x16 slot suffices since 16 GB/s > 40 GB/s total",
                            "It needs about 40 lanes (e.g. more than x16 provides); bandwidth scales by adding lanes, so x16 alone is insufficient",
                            "PCIe bandwidth cannot be increased by adding lanes",
                            "It should use a shared parallel bus instead",
                        ],
                        1,
                        9,
                        "PCIe scales linearly with lane count (~1 GB/s per lane per direction in gen 3); 40 GB/s needs ~40 lanes, more than one x16 slot. Lanes are the unit of scaling, unlike a fixed shared bus.",
                        ["gate", "nvidia", "amazon"],
                    ),
                ],
            ),
            L(
                "io-raid",
                "RAID Levels",
                """# RAID Levels

**RAID** combines disks for speed, capacity, redundancy. Building blocks:
* **Striping:** data split across disks → parallel throughput, but one
  dead disk kills the array.
* **Mirroring:** every byte duplicated → parallel reads, 50% capacity
  overhead.
* **Parity:** XOR checksum blocks reconstruct a dead disk's contents —
  cheaper than mirroring.

## Worked capacity — 4 disks × 2 TB (8 TB raw), verified
| Level   | How it works               | Usable | Survives     |
|---------|----------------------------|--------|--------------|
| RAID 0  | striping, no redundancy    | 8 TB   | 0 failures   |
| RAID 1  | mirroring (pairs)          | 2 TB   | 1 per pair   |
| RAID 5  | striped + distrib. parity  | 6 TB   | any 1 disk   |
| RAID 6  | striped + double parity    | 4 TB   | any 2 disks  |
| RAID 10 | mirror pairs, then striped | 4 TB   | 1 per mirror |

Formulas (n disks of size S): RAID 0 = nS; RAID 1 = S;
RAID 5 = (n−1)S; RAID 6 = (n−2)S; RAID 10 = (n/2)S.

## Which to pick? (interview framing)
* **RAID 0:** scratch/temp data — speed matters, loss is OK.
* **RAID 1:** tiny arrays, OS boot disks — simple, fast reads.
* **RAID 5:** general file servers — balanced; but rebuilds are slow
  and a second failure mid-rebuild is fatal.
* **RAID 6:** large disks with hour-long rebuilds — extra parity buys
  safety during the rebuild window.
* **RAID 10:** databases — best random I/O + redundancy at 2× cost.

**GATE facts:** RAID 5 needs ≥3 disks, RAID 6 ≥4. RAID 2/3/4
(bit/byte striping, dedicated parity disk) are obsolete — the parity
disk becomes the bottleneck.""",
                [
                    Q(
                        "What does striping in RAID 0 provide?",
                        [
                            "Data redundancy against disk failure",
                            "Higher throughput by spreading data across disks, with no fault tolerance",
                            "Automatic backup to a parity disk",
                            "Encryption of stored data",
                        ],
                        1,
                        1,
                        "RAID 0 stripes data for parallel speed but keeps no redundancy — one disk failure destroys the array.",
                        ["gate", "tcs", "infosys"],
                    ),
                    Q(
                        "Four 2 TB disks in RAID 0 give how much usable space, and how many disk failures can it survive?",
                        [
                            "8 TB usable, 0 failures",
                            "6 TB usable, 1 failure",
                            "4 TB usable, 2 failures",
                            "2 TB usable, 1 failure",
                        ],
                        0,
                        3,
                        "RAID 0: usable = n*S = 8 TB, with zero redundancy. (Verified: 4 x 2 TB = 8 TB.)",
                        ["gate", "wipro", "amazon"],
                    ),
                    Q(
                        "Four 2 TB disks in RAID 5 give how much usable space?",
                        [
                            "8 TB",
                            "6 TB",
                            "4 TB",
                            "2 TB",
                        ],
                        1,
                        4,
                        "RAID 5: usable = (n-1)*S = 3 x 2 TB = 6 TB — one disk's worth holds distributed parity. (Verified.)",
                        ["gate", "google"],
                    ),
                    Q(
                        "Four 2 TB disks: which configurations both yield 4 TB usable?",
                        [
                            "RAID 1 and RAID 5",
                            "RAID 6 and RAID 10",
                            "RAID 0 and RAID 6",
                            "RAID 5 and RAID 10",
                        ],
                        1,
                        6,
                        "RAID 6 = (n-2)*S = 4 TB; RAID 10 = (n/2)*S = 4 TB. RAID 1 gives 2 TB, RAID 5 gives 6 TB, RAID 0 gives 8 TB. (Verified.)",
                        ["gate", "microsoft"],
                    ),
                    Q(
                        "A database needs the best random read/write performance with redundancy, and disk cost is secondary. Which RAID level fits?",
                        [
                            "RAID 0",
                            "RAID 5",
                            "RAID 10",
                            "RAID 6",
                        ],
                        2,
                        7,
                        "RAID 10 (mirrored pairs, striped) gives excellent random I/O plus redundancy at 2x disk cost — the standard choice for databases.",
                        ["gate", "amazon"],
                    ),
                    Q(
                        "Why is RAID 6 preferred over RAID 5 for arrays built from very large disks?",
                        [
                            "RAID 6 is faster at sequential writes",
                            "RAID 6 uses fewer disks",
                            "Rebuilding a huge disk takes hours, and RAID 6's double parity survives a second failure during that long rebuild window",
                            "RAID 5 cannot be built with large disks",
                        ],
                        2,
                        9,
                        "Large disks mean long rebuilds, during which the array is vulnerable; RAID 6 tolerates any 2 failures, covering a second disk dying mid-rebuild.",
                        ["gate", "google", "nvidia"],
                    ),
                ],
            ),
            L(
                "io-storage",
                "Storage: HDD vs SSD",
                """# Storage: HDD vs SSD

## HDD — mechanical
Data on spinning magnetic **platters**; heads on an actuator arm seek
the right track. Access time = seek + rotational latency + transfer.
* **RPM:** 5400 (laptops), 7200 (desktops), 15000 (old enterprise).
* **Seek time:** arm to the track (~4–10 ms average).
* **Rotational latency:** waiting for the sector to spin under the head
  — average is half a revolution.

### Worked: 7200 RPM (verified)
* Revs/second = 7200/60 = 120
* Time/revolution = 1/120 s = 8.333 ms
* **Average rotational latency = half = 4.17 ms**

Reference: 5400 RPM → 5.56 ms; 15000 RPM → 2.0 ms. GATE loves
the formula: avg latency = 60 / RPM / 2.

## SSD — electronic
Data in **NAND flash**; no platters, heads, or moving parts.
* Random access in tens of microseconds (~100× faster than HDD —
  no seek, no rotation).
* **Wear leveling:** the controller spreads program/erase cycles evenly
  since flash cells wear out after limited cycles.
* No defragmentation needed — random reads cost the same as sequential.

## NVMe
NVMe is a protocol for SSDs on the **PCIe bus**, replacing the
SATA/AHCI path designed for spinning disks. Tens of thousands of
parallel queues cut latency and unlock PCIe bandwidth: SATA SSD ~550
MB/s vs NVMe ~3500+ MB/s — same NAND, different interface.

**Interview one-liner:** "HDDs are limited by mechanics — seek plus
half a rotation; SSDs by electronics — microseconds, with wear
leveling for flash endurance; NVMe removes the legacy SATA bottleneck
by speaking PCIe natively.""",
                [
                    Q(
                        "Which component of HDD access time is eliminated entirely in an SSD?",
                        [
                            "Transfer time",
                            "Seek time and rotational latency — SSDs have no moving parts",
                            "Controller overhead",
                            "ECC computation",
                        ],
                        1,
                        2,
                        "SSDs store data in NAND flash with no platters or heads, so there is nothing to seek and nothing to rotate — random access drops to microseconds.",
                        ["gate", "tcs", "infosys"],
                    ),
                    Q(
                        "What is the average rotational latency of a 7200 RPM hard disk?",
                        [
                            "8.33 ms",
                            "4.17 ms",
                            "2.08 ms",
                            "13.9 ms",
                        ],
                        1,
                        4,
                        "One revolution = 60/7200 s = 8.333 ms; average latency is half a revolution = 4.17 ms. (Verified: 60/7200/2*1000 = 4.1667 ms.)",
                        ["gate", "wipro"],
                    ),
                    Q(
                        "A disk has 5 ms average seek time and spins at 7200 RPM. Ignoring transfer time, what is the average access time?",
                        [
                            "5 ms",
                            "9.17 ms",
                            "13.33 ms",
                            "4.17 ms",
                        ],
                        1,
                        5,
                        "Access = seek + avg rotational latency = 5 ms + 4.17 ms = 9.17 ms. (Rotational latency verified above.)",
                        ["gate", "amazon"],
                    ),
                    Q(
                        "What is wear leveling in an SSD?",
                        [
                            "Spreading read/write heads evenly across platters",
                            "Distributing program/erase cycles evenly across flash cells to extend drive life",
                            "Cooling the controller to prevent thermal wear",
                            "Balancing load across RAID disks",
                        ],
                        1,
                        6,
                        "NAND cells wear out after limited erase cycles, so the SSD controller spreads writes across all cells — there are no heads or platters in an SSD.",
                        ["gate", "google"],
                    ),
                    Q(
                        "Why does NVMe outperform SATA for the same NAND flash chips?",
                        [
                            "NVMe uses denser flash cells",
                            "NVMe speaks natively over PCIe with massive parallel queues instead of the legacy AHCI path designed for spinning disks",
                            "NVMe disks spin faster",
                            "SATA cannot address more than 1 TB",
                        ],
                        1,
                        8,
                        "The bottleneck was the interface, not the flash: NVMe exploits PCIe bandwidth and tens of thousands of queues, while AHCI/SATA was built around single-queue spinning disks.",
                        ["gate", "nvidia", "microsoft"],
                    ),
                    Q(
                        "An HDD datasheet claims 15000 RPM and 3 ms average seek. A workload does 4 KB random reads with negligible transfer time. Estimate average IOPS.",
                        [
                            "About 100 IOPS",
                            "About 200 IOPS",
                            "About 333 IOPS",
                            "About 500 IOPS",
                        ],
                        1,
                        9,
                        "Avg rotational latency = 60/15000/2 = 2 ms; access = 3 + 2 = 5 ms per read, so ~1/0.005 = 200 IOPS. (Verified: 60/15000/2*1000 = 2.0 ms.)",
                        ["gate", "amazon"],
                    ),
                ],
            ),
        ],
    ),
    M(
        "advanced",
        "Advanced Topics",
        "Multiprocessors, Flynn's taxonomy, Amdahl's and Gustafson's laws, GPU architecture.",
        [
            L(
                "adv-multiprocessors",
                "Multiprocessors: SMP & NUMA",
                """# Multiprocessors: SMP & NUMA

Key design question: how does each CPU reach memory?

## SMP / UMA — Symmetric Multiprocessing
All CPUs share **one physical memory** over a common bus/interconnect.
**UMA** = every CPU reaches every byte with the *same latency*.
Symmetric: any CPU runs any thread, touches any address. The shared
bus becomes the bottleneck — SMP scales to roughly tens of cores.

## NUMA — Non-Uniform Memory Access
Memory is **distributed**: each CPU/node has *local* memory plus slower
access to *remote* memory. Latency depends on where data lives — hence
"non-uniform". Scales to hundreds of cores, but software must be
**NUMA-aware**: pin threads near their data or remote-access penalties
eat the speedup.

| Aspect      | SMP / UMA             | NUMA                    |
|-------------|-----------------------|-------------------------|
| Memory      | single shared pool    | distributed, per-node   |
| Latency     | uniform for all CPUs  | local fast, remote slow |
| Scaling     | ~tens of cores        | hundreds of cores       |
| Programming | easy, symmetric       | needs locality awareness|

## The cache coherence problem
Each CPU has private caches. If CPU-0 caches X and CPU-1 writes X,
CPU-0's copy is **stale**. Hardware keeps caches coherent — the classic
protocol is **MESI** (Modified, Exclusive, Shared, Invalid): each line
carries a state, and caches snoop the bus (or use directories) to
invalidate/update each other.

## Multicore vs multiprocessor
* **Multicore:** many cores on one chip (your laptop/phone).
* **Multiprocessor:** many CPU chips/sockets on one board (servers).
* A modern server is both: multiple sockets × many cores, usually NUMA
  across sockets.""",
                [
                    Q(
                        "What does UMA guarantee in an SMP system?",
                        [
                            "Each CPU has its own private memory",
                            "Every CPU accesses all memory with the same latency",
                            "Memory latency is zero for local accesses",
                            "Only one CPU may access memory at a time",
                        ],
                        1,
                        2,
                        "UMA = Uniform Memory Access: one shared pool, identical latency from every CPU. Private per-CPU memory is the NUMA/distributed model.",
                        ["gate", "tcs", "infosys"],
                    ),
                    Q(
                        "Why does a bus-based SMP system stop scaling at a few tens of cores?",
                        [
                            "CPUs overheat beyond 32 cores",
                            "The shared bus/interconnect saturates — memory requests from many CPUs contend for the same path",
                            "The OS cannot schedule more than 32 threads",
                            "Cache coherence is impossible past 16 cores",
                        ],
                        1,
                        4,
                        "One shared bus means every CPU's memory traffic fights for the same wires; contention, not heat or the scheduler, is the fundamental SMP scaling wall.",
                        ["gate", "amazon"],
                    ),
                    Q(
                        "In a NUMA machine, a thread repeatedly accesses memory on a remote node. What is the performance-conscious fix?",
                        [
                            "Increase the CPU clock speed",
                            "Migrate the thread or its data so accesses become node-local",
                            "Disable the remote node's memory",
                            "Switch the system to programmed I/O",
                        ],
                        1,
                        5,
                        "NUMA penalties come from remote latency; the fix is locality — pin threads near their data or migrate pages to the accessing node.",
                        ["gate", "google"],
                    ),
                    Q(
                        "CPU-0 holds variable X in its cache. CPU-1 writes a new value of X to memory. What problem arises?",
                        [
                            "A bus arbitration deadlock",
                            "CPU-0's cached copy is stale — the cache coherence problem",
                            "The write is automatically mirrored to CPU-0's cache",
                            "X becomes permanently locked",
                        ],
                        1,
                        6,
                        "Private caches can disagree about the same address; coherence protocols like MESI exist precisely to invalidate or update stale copies.",
                        ["gate", "microsoft", "nvidia"],
                    ),
                    Q(
                        "What does the 'M' (Modified) state mean in the MESI protocol?",
                        [
                            "The cache line matches memory and may be shared",
                            "This cache holds the only valid, dirty copy — memory is stale and the line must be written back",
                            "The line is invalid and must be refetched",
                            "The line is locked for DMA",
                        ],
                        1,
                        8,
                        "Modified = this cache owns the sole up-to-date copy and it differs from memory, so the cache must supply/write back the data. Exclusive/Shared/Invalid cover the other cases.",
                        ["gate", "google"],
                    ),
                    Q(
                        "A server has 4 sockets x 32 cores. An architect calls it 'both multiprocessor and multicore NUMA'. Why is that accurate?",
                        [
                            "It is marketing — the terms are synonyms",
                            "Each socket is a multicore chip (cores share on-chip resources), and the 4 sockets form a multiprocessor with NUMA memory across sockets",
                            "NUMA requires exactly 4 sockets",
                            "Multicore only applies to GPUs",
                        ],
                        1,
                        9,
                        "Multicore = many cores per chip; multiprocessor = many chips per system; NUMA describes the non-uniform memory across those sockets. Modern servers are all three at once.",
                        ["gate", "amazon", "nvidia"],
                    ),
                ],
            ),
            L(
                "adv-flynn",
                "Flynn's Taxonomy",
                """# Flynn's Taxonomy

Flynn (1966) classified architectures by **instruction streams** ×
**data streams**. Four boxes:

## SISD — Single Instruction, Single Data
One instruction, one data item: the classic **uniprocessor**.
**Example:** old single-core CPU running sequential code.

## SIMD — Single Instruction, Multiple Data
One instruction on **many data items** at once (vector/data-parallel).
**Example:** GPU adding two arrays element-wise; AVX processing 8
floats per instruction. Ideal for images, simulation, ML inference.

## MISD — Multiple Instruction, Single Data
Many instructions, one data stream — rarely built. **Example:**
fault-tolerant systems where redundant processors run different
implementations on the same input and vote (avionics, space probes).

## MIMD — Multiple Instruction, Multiple Data
Each processor runs its own instructions on its own data — the dominant
parallel architecture today. **Example:** multicore CPU threads; server
clusters; supercomputers. Split into shared-memory (SMP/NUMA) and
distributed-memory (message passing, MPI).

|                | Single Data          | Multiple Data           |
|----------------|----------------------|-------------------------|
| Single Instr   | SISD: classic CPU    | SIMD: GPU/vector        |
| Multiple Instr | MISD: fault-tolerant | MIMD: multicore/cluster |

**Interview tip:** "classify a GPU" → SIMD (data-parallel), more
precisely **SIMT** (single instruction, multiple threads). Mention both.""",
                [
                    Q(
                        "A classic single-core CPU running one sequential program is an example of:",
                        [
                            "SIMD",
                            "SISD",
                            "MIMD",
                            "MISD",
                        ],
                        1,
                        1,
                        "One instruction stream on one data stream = SISD, the classic uniprocessor box in Flynn's taxonomy.",
                        ["gate", "tcs", "infosys"],
                    ),
                    Q(
                        "A GPU adding two large arrays element-wise with a single instruction is an example of:",
                        [
                            "SISD",
                            "MISD",
                            "SIMD",
                            "MIMD",
                        ],
                        2,
                        3,
                        "One instruction applied across many data elements in parallel is the definition of SIMD (data-parallel).",
                        ["gate", "nvidia", "wipro"],
                    ),
                    Q(
                        "Which Flynn category is considered rare in practice, used mainly for fault-tolerant redundant execution?",
                        [
                            "SISD",
                            "SIMD",
                            "MISD",
                            "MIMD",
                        ],
                        2,
                        4,
                        "MISD — multiple instruction streams on a single data stream — is the odd one out, seen in redundant fault-tolerant systems like avionics.",
                        ["gate", "google"],
                    ),
                    Q(
                        "A cluster of servers where each node runs its own program on its own data falls under:",
                        [
                            "SISD",
                            "SIMD",
                            "MISD",
                            "MIMD",
                        ],
                        3,
                        5,
                        "Independent instruction streams on independent data streams = MIMD — the dominant parallel architecture from multicore chips to supercomputers.",
                        ["gate", "amazon", "microsoft"],
                    ),
                    Q(
                        "An interviewer asks you to classify a modern NVIDIA GPU. The strongest answer is:",
                        [
                            "Pure SISD, since each thread runs independently",
                            "SIMD-like data-parallel execution, more precisely SIMT: warps of threads execute the same instruction in lockstep",
                            "MISD, because of redundant shader cores",
                            "It falls outside Flynn's taxonomy entirely",
                        ],
                        1,
                        7,
                        "GPUs are data-parallel (SIMD family); the precise term is SIMT — single instruction, multiple threads — with warps executing in lockstep.",
                        ["gate", "nvidia", "google"],
                    ),
                    Q(
                        "Why does Flynn's taxonomy classify by instruction AND data streams rather than just core count?",
                        [
                            "Core counts were unknown in 1966",
                            "Two machines with the same core count can behave utterly differently — a 64-core vector processor (SIMD) vs 64 independent cores (MIMD) need different programming models",
                            "Instruction streams are easier to count than cores",
                            "It was designed only for GPUs",
                        ],
                        1,
                        9,
                        "Core count alone hides the execution model: SIMD cores march in lockstep on shared instructions while MIMD cores run freely — taxonomy captures how you must program the machine.",
                        ["gate", "google", "amazon"],
                    ),
                ],
            ),
            L(
                "adv-amdahl",
                "Amdahl's Law",
                """# Amdahl's Law

Hard ceiling on speedup when the **problem size is fixed**: the serial
fraction dominates. If fraction **P** is parallelizable over **N**
processors:

Speedup(N) = 1 / ((1 − P) + P / N)

## Worked (verified)
**P = 0.8, N = 4:** 1 / (0.2 + 0.8/4) = 1 / 0.4 = **2.5×**
**P = 0.9, N = 8:** 1 / (0.1 + 0.9/8) = 1 / 0.2125 ≈ **4.71×**

## Diminishing returns — P = 0.9 (verified)
| N  | Speedup | Note                 |
|----|---------|----------------------|
| 1  | 1.00×   | —                    |
| 2  | 1.82×   |                      |
| 4  | 3.08×   |                      |
| 8  | 4.71×   |                      |
| 16 | 6.40×   | doubling buys little |
| ∞  | 10.00×  | hard ceiling 1/(1−P) |

## Key insights (GATE + interview)
* Max speedup = **1 / (1 − P)** — the P/N term vanishes as N → ∞.
* Halving the *serial* fraction beats doubling cores: P = 0.95 →
  ceiling jumps to 20×.
* Assumes **fixed problem size** (strong scaling). Growing problems →
  Gustafson's law (next lesson).
* Real world is worse: ignores communication overhead, load imbalance,
  memory contention.""",
                [
                    Q(
                        "Amdahl's law assumes which kind of scaling?",
                        [
                            "Weak scaling — the problem grows with processor count",
                            "Strong scaling — the problem size is fixed",
                            "No scaling — processors are never added",
                            "Memory scaling only",
                        ],
                        1,
                        2,
                        "Amdahl fixes the problem size and asks how much faster N processors go — that is strong scaling. Gustafson covers the growing-problem (weak scaling) case.",
                        ["gate", "tcs", "infosys"],
                    ),
                    Q(
                        "80% of a program is parallelizable. What is the maximum speedup on 4 cores?",
                        [
                            "4x",
                            "3.2x",
                            "2.5x",
                            "1.25x",
                        ],
                        2,
                        4,
                        "Speedup = 1/(0.2 + 0.8/4) = 1/0.4 = 2.5x. (Verified.) The serial 20% caps the gain well below 4x.",
                        ["gate", "amazon", "wipro"],
                    ),
                    Q(
                        "90% of a program is parallelizable. What is the speedup on 8 cores?",
                        [
                            "8x",
                            "7.2x",
                            "4.71x",
                            "10x",
                        ],
                        2,
                        5,
                        "Speedup = 1/(0.1 + 0.9/8) = 1/0.2125 ≈ 4.71x. (Verified: 4.7059.)",
                        ["gate", "google"],
                    ),
                    Q(
                        "With 90% parallelizable code, what is the absolute speedup ceiling with infinite cores?",
                        [
                            "Infinite",
                            "100x",
                            "10x",
                            "9x",
                        ],
                        2,
                        6,
                        "Ceiling = 1/(1-P) = 1/0.1 = 10x. No core count beats the serial fraction. (Verified.)",
                        ["gate", "microsoft"],
                    ),
                    Q(
                        "For P = 0.9, doubling cores from 8 to 16 raises speedup from 4.71x to 6.40x. What does this illustrate?",
                        [
                            "Linear scaling",
                            "Diminishing returns — each doubling buys less, approaching the 10x ceiling",
                            "Amdahl's law is wrong for large N",
                            "Gustafson's law taking over",
                        ],
                        1,
                        8,
                        "The gains shrink per doubling (4.71 -> 6.40, then toward 10x max) — the signature diminishing-returns curve of Amdahl's law. (Values verified.)",
                        ["gate", "nvidia"],
                    ),
                    Q(
                        "Team A doubles cores (8 -> 16) on P = 0.9 code; Team B halves the serial fraction (P = 0.9 -> 0.95) on 8 cores. Whose speedup improves more, and why?",
                        [
                            "Team A: more cores always wins",
                            "Team B: raising the ceiling from 10x to 20x beats adding cores against a fixed ceiling — their speedup goes 4.71x to about 5.93x vs A's 6.40x, but B's headroom is far larger",
                            "Both improve equally",
                            "Neither improves at all",
                        ],
                        1,
                        10,
                        "A: 1/(0.1+0.9/16) = 6.40x. B: 1/(0.05+0.95/8) = 1/0.16875 ≈ 5.93x — slightly less now, but B doubled the absolute ceiling (10x -> 20x). Attacking the serial fraction is the deeper win. (Verified: 1/0.16875 = 5.9259.)",
                        ["gate", "google", "amazon"],
                    ),
                ],
            ),
            L(
                "adv-gustafson",
                "Gustafson's Law & Scalability",
                """# Gustafson's Law & Scalability

Amdahl fixes the problem size. Gustafson observed that bigger machines
solve **bigger problems** — scale the work with the processor count.

## Formula (scaled speedup)
Scaled speedup(N) = N − (1 − P)(N − 1), equivalently (1 − P) + P·N:
the serial part stays one unit while the parallel part grows with N.

## Worked (verified)
**P = 0.9, N = 8:** 8 − 0.1 × 7 = 8 − 0.7 = **7.3×**
Amdahl (fixed size) gave only **4.71×** for the same P, N.

## Amdahl vs Gustafson
|                | Amdahl (fixed)     | Gustafson (scaled) |
|----------------|--------------------|--------------------|
| Problem size   | fixed              | grows with N       |
| Asks           | "how much faster?" | "how much bigger?" |
| Speedup bound  | 1/(1−P) ceiling    | ~linear in N       |
| Scaling type   | **strong**         | **weak**           |

## Strong vs weak scaling
* **Strong:** fixed problem, more processors → time reduction. Amdahl.
  Hard — the serial fraction bites.
* **Weak:** work per processor fixed, total grows with N → constant
  time. Gustafson. Easier to look good — most supercomputer benchmarks.

**Interview framing:** "Amdahl says diminishing returns on a fixed
problem; Gustafson says we scale problems up, so speedups look linear.
Always report *which* scaling you measured — or the number is
meaningless.""",
                [
                    Q(
                        "What key assumption separates Gustafson's law from Amdahl's law?",
                        [
                            "Gustafson assumes zero serial code",
                            "Gustafson assumes the problem size grows with the number of processors",
                            "Gustafson assumes processors are slower",
                            "Gustafson ignores parallel code entirely",
                        ],
                        1,
                        2,
                        "Amdahl fixes the problem size; Gustafson scales the workload up with N so every processor stays busy — the realistic case for bigger machines.",
                        ["gate", "tcs", "infosys"],
                    ),
                    Q(
                        "With P = 0.9 parallelizable code on 8 processors, what is Gustafson's scaled speedup?",
                        [
                            "4.71x",
                            "7.3x",
                            "8x",
                            "10x",
                        ],
                        1,
                        4,
                        "S = N - (1-P)(N-1) = 8 - 0.1*7 = 7.3x — far above Amdahl's 4.71x for the same P and N. (Verified.)",
                        ["gate", "wipro", "amazon"],
                    ),
                    Q(
                        "A benchmark keeps the problem size fixed while adding processors and reports the time reduction. Which scaling and which law apply?",
                        [
                            "Weak scaling, Gustafson's law",
                            "Strong scaling, Amdahl's law",
                            "Strong scaling, Gustafson's law",
                            "Weak scaling, Amdahl's law",
                        ],
                        1,
                        5,
                        "Fixed problem + more processors = strong scaling, governed by Amdahl. Growing problem per processor = weak scaling, governed by Gustafson.",
                        ["gate", "google"],
                    ),
                    Q(
                        "Why do supercomputer benchmarks usually report weak scaling rather than strong scaling?",
                        [
                            "Weak scaling numbers are always smaller",
                            "Growing the problem with N keeps efficiency high and looks better — strong scaling would expose Amdahl's serial-fraction wall",
                            "Strong scaling is impossible to measure",
                            "Benchmarks are forbidden from using Amdahl's law",
                        ],
                        1,
                        7,
                        "Weak scaling hides the serial bottleneck by feeding each new processor more work; strong scaling on a fixed problem would show diminishing returns quickly.",
                        ["gate", "microsoft", "nvidia"],
                    ),
                    Q(
                        "Using S = (1-P) + P*N: for P = 0.95 and N = 64, what is the scaled speedup, and what dominates it?",
                        [
                            "60.85x, dominated by the P*N parallel term",
                            "20x, dominated by the serial term",
                            "64x exactly",
                            "12.8x, dominated by overhead",
                        ],
                        0,
                        8,
                        "S = 0.05 + 0.95*64 = 0.05 + 60.8 = 60.85x. The parallel term P*N dwarfs the serial remainder — the essence of Gustafson's optimism. (Verified: 0.05+60.8 = 60.85.)",
                        ["gate", "google"],
                    ),
                    Q(
                        "A paper claims 'near-linear speedup to 1024 cores' but the problem size grew 1024x too. A reviewer objects. What is the valid criticism?",
                        [
                            "Linear speedup is mathematically impossible",
                            "The claim measures weak (Gustafson) scaling, not strong scaling — it says nothing about how much faster a fixed problem runs",
                            "Amdahl's law forbids scaling past 100 cores",
                            "The experiment used too many cores",
                        ],
                        1,
                        10,
                        "Growing the problem with core count is weak scaling; near-linear results are expected there (S ≈ P*N). The claim cannot be read as 'a fixed job runs 1024x faster' — that needs a strong-scaling experiment.",
                        ["gate", "amazon", "google"],
                    ),
                ],
            ),
            L(
                "adv-gpu",
                "GPU Architecture Basics",
                """# GPU Architecture Basics

## Latency vs throughput
CPUs optimize for **latency**: few powerful cores, big caches, branch
prediction — finish *one* thread fast. GPUs optimize for **throughput**:
thousands of simple cores — finish *many* threads fast, hiding memory
latency by always having another thread ready.

|           | CPU                     | GPU                       |
|-----------|-------------------------|---------------------------|
| Cores     | few (8–64), complex     | thousands, simple         |
| Caches    | large, sophisticated    | small, minimal            |
| Best at   | serial logic, branching | data-parallel crunching   |

## SIMT — Single Instruction, Multiple Threads
Threads group into **warps** (32 on NVIDIA; AMD **wavefronts** of 64).
All threads in a warp execute the *same instruction* in lockstep, each
on its own data — like SIMD, programmed as independent threads.
* **Divergence hurts:** if a warp splits on if/else, *both* paths run
  serially with threads masked off.
* **Coalesced access wins:** adjacent addresses per warp merge into one
  memory transaction.

## When GPUs win vs lose
* **Win:** dense linear algebra, image/video, physics sim, ML —
  regular, data-parallel, high arithmetic intensity.
* **Lose:** pointer-chasing, heavy branching, tiny serial tasks, or
  when PCIe transfer time dwarfs compute time.

## CUDA / ROCm
* **CUDA** (NVIDIA): dominant GPGPU platform — kernels over grids of
  thread blocks, in C/C++/Python.
* **ROCm** (AMD): the open counterpart.
* Model: host (CPU) offloads kernels to the device (GPU); memory is
  explicitly moved or unified.

**One-liner:** "A GPU is a throughput engine: thousands of SIMT cores
in warps of 32. Wins on regular data-parallel work, loses on divergent
branches — and never forget the PCIe transfer cost.""",
                [
                    Q(
                        "What is the fundamental design tradeoff of a GPU versus a CPU?",
                        [
                            "GPU optimizes single-thread latency; CPU optimizes throughput",
                            "GPU optimizes throughput with thousands of simple cores; CPU optimizes latency with a few complex cores",
                            "GPUs have larger caches than CPUs",
                            "There is no difference — the terms are interchangeable",
                        ],
                        1,
                        2,
                        "CPUs spend transistors on caches and branch prediction to finish one thread fast (latency); GPUs spend them on thousands of simple cores to finish many threads fast (throughput).",
                        ["gate", "nvidia", "tcs"],
                    ),
                    Q(
                        "In NVIDIA terminology, what is a warp?",
                        [
                            "A high-speed interconnect between GPU and CPU",
                            "A group of 32 threads that execute the same instruction in lockstep",
                            "A type of GPU cache",
                            "A CUDA compiler optimization pass",
                        ],
                        1,
                        3,
                        "A warp (32 threads; AMD's wavefront is 64) is the SIMT execution unit — all threads in it share one instruction stream, each on its own data.",
                        ["gate", "nvidia", "infosys"],
                    ),
                    Q(
                        "Threads in a warp take different branches of an if/else. What happens to performance?",
                        [
                            "Nothing — branches are free on GPUs",
                            "Both paths execute serially with threads masked off, wasting throughput",
                            "The warp automatically splits into two warps at no cost",
                            "The GPU switches to CPU mode",
                        ],
                        1,
                        5,
                        "SIMT lockstep means divergence serializes: the warp runs the if-path with else-threads masked, then vice versa — branch-heavy code is the classic GPU pitfall.",
                        ["gate", "nvidia", "google"],
                    ),
                    Q(
                        "Which workload is the best fit for a GPU?",
                        [
                            "Pointer-chasing through a linked list",
                            "Dense matrix multiplication over large regular arrays",
                            "A deeply nested recursive search with unpredictable branches",
                            "A single-threaded script with heavy I/O",
                        ],
                        1,
                        6,
                        "Dense, regular, data-parallel arithmetic (matmul, image processing, ML) matches SIMT perfectly; irregular branching and pointer-chasing do not.",
                        ["gate", "amazon", "nvidia"],
                    ),
                    Q(
                        "A kernel runs in 2 ms on the GPU but moving its data over PCIe takes 50 ms each way. What should the engineer conclude?",
                        [
                            "The GPU is still faster because kernels are fast",
                            "The transfer cost (100 ms round trip) dwarfs the 2 ms compute — keep it on the CPU or batch much more work per transfer",
                            "Use a faster GPU",
                            "PCIe transfer time does not count in speedup",
                        ],
                        1,
                        8,
                        "End-to-end time is what matters: 100 ms of transfer vs 2 ms of compute means the GPU loses badly. GPUs only win when compute dominates transfer.",
                        ["gate", "google", "amazon"],
                    ),
                    Q(
                        "Why does coalesced memory access matter for GPU performance?",
                        [
                            "It reduces the number of warps needed",
                            "When a warp's threads access adjacent addresses, hardware merges them into fewer memory transactions, using full bus bandwidth",
                            "It eliminates branch divergence",
                            "It lets the CPU access GPU memory directly",
                        ],
                        1,
                        9,
                        "GPUs fetch memory in wide transactions; scattered accesses waste most of each transaction, while adjacent (coalesced) accesses let one transaction serve the whole warp.",
                        ["gate", "nvidia", "microsoft"],
                    ),
                ],
            ),
        ],
    ),
]


# Spread correct-answer positions evenly across 0-3. Each question's
# choices are rotated (the correct answer moves with its text, so the
# stored answer_index stays correct).
for _m in MODULES:
    for _li, _les in enumerate(_m["lessons"]):
        for _qi, _q in enumerate(_les["questions"]):
            _t = (_qi + _li) % 4
            _s = (_t - _q["answer_index"]) % 4
            if _s:
                _c = _q["choices"]
                _q["choices"] = _c[-_s:] + _c[:-_s]
                _q["answer_index"] = _t
del _m, _li, _les, _qi, _q, _t, _s, _c
