"""Seed content: Computer Organization & Architecture — Part 3 (Modules 3-4).

Pipelining (5-stage pipeline, hazards, forwarding, branch prediction,
superscalar, performance math) and Memory Hierarchy (locality, cache mapping,
write policies, AMAT, virtual memory, TLB, page replacement).

ORIGINAL educational content written for SkillForge. All numbers, bit
splits, AMAT/EAT values, and page-fault counts were verified by running
Python during authoring — never hand-computed unchecked. Questions are
GATE-style numericals plus interview staples; no textbook problem is
copied verbatim.

Exports a single variable ``MODULES``: a list of 2 module dicts
(pipelining, memory-hierarchy) with 13 lessons total, each lesson with
exactly 6 MCQs (78 questions total).
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
    M("pipelining", "Pipelining",
      "5-stage pipeline, hazards, forwarding, branch prediction, superscalar execution.",
      [
          dict(L("pipeline-five-stage", "The 5-Stage Pipeline",
"""## What a pipeline is

A CPU runs each instruction as small steps — five in a classic RISC:

| Stage | Name | Job |
|---|---|---|
| IF | Fetch | Read the instruction addressed by the PC |
| ID | Decode | Decode opcode, read source registers |
| EX | Execute | ALU: arithmetic, address, branch condition |
| MEM | Memory | Data memory access (loads/stores only) |
| WB | Write-back | Write result to the destination register |

## Overlap, not faster single instructions

A **sequential** CPU finishes all 5 steps of one
instruction before starting the next: 5 cycles
per instruction. A **pipelined** CPU starts a new
instruction every cycle — an assembly line where
instruction 1 is in EX while 2 is in ID and 3
is in IF. Latency stays 5 cycles, but throughput
becomes one instruction per cycle.

## Timing picture (text)

```
cycle:  1   2   3   4   5   6   7
i1:     IF  ID  EX  MEM WB
i2:         IF  ID  EX  MEM WB
i3:             IF  ID  EX  MEM WB
i4:                 IF  ID  EX  MEM WB
```

## Ideal CPI = 1

With no hazards the pipeline retires one
instruction per cycle, so the ideal **CPI = 1**
— even though every instruction still spends
5 cycles inside. For n instructions the total
is **k + n − 1 cycles** instead of k × n: the
k−1 fill and drain cycles are pure overhead.""",
              [
                  Q("While tracing a program on a classic 5-stage RISC core, you watch the IF stage fire. What does it do?",
                    ["Uses the PC to fetch the instruction from instruction memory",
                     "Decodes the opcode and reads source registers",
                     "Performs the ALU computation for the instruction",
                     "Writes the result back to the register file"],
                    0, 1,
                    "IF (Instruction Fetch) reads the instruction addressed by the program counter from instruction memory.",
                    ["gate", "tcs", "infosys"]),
                  Q("In an ideal 5-stage pipeline with no hazards, what is the CPI?",
                    ["5, because every instruction visits 5 stages",
                     "1, because one instruction completes every cycle in steady state",
                     "0.2, because 5 instructions finish per cycle",
                     "It depends on the clock frequency"],
                    1, 3,
                    "Latency per instruction is 5 cycles but throughput is one completion per cycle, so ideal CPI = 1.",
                    ["gate", "amazon"]),
                  Q("In which stage does an ADD instruction compute its sum?",
                    ["IF",
                     "ID",
                     "EX",
                     "WB"],
                    2, 4,
                    "The ALU lives in the EX stage; arithmetic, address computation, and branch-condition evaluation all happen there.",
                    ["gate", "google"]),
                  Q("A 5-stage pipeline executes 4 instructions with no hazards. How many cycles does it take?",
                    ["5 cycles",
                     "20 cycles",
                     "9 cycles",
                     "8 cycles"],
                    3, 6,
                    "Total = k + n − 1 = 5 + 4 − 1 = 8 cycles, versus 5 × 4 = 20 sequential.",
                    ["gate", "amazon", "tcs"]),
                  Q("Why does the classic 5-stage design write registers in the first half of the WB cycle and read them in the second half of the ID cycle?",
                    ["So that an instruction reading a register in ID sees the value written by an instruction in WB in the same cycle",
                     "To reduce the number of pipeline registers",
                     "Because the ALU is only free in the first half-cycle",
                     "To keep the clock frequency higher"],
                    0, 8,
                    "This half-cycle trick resolves the same-cycle read-after-write on the register file without extra forwarding.",
                    ["google", "gate", "amazon"]),
                  Q("An interviewer asks: 'If deeper pipelines are faster, why not use 50 stages?' What is the best answer?",
                    ["Deeper pipelines always win; 50 stages is ideal",
                     "Each stage's latch overhead and clock skew eat the gains, and branch misprediction penalties grow with depth",
                     "Caches cannot keep up with 50 stages",
                     "The ISA limits pipelines to 5 stages"],
                    1, 9,
                    "Deeper pipelines shorten the clock period but each stage adds latch overhead, and a mispredicted branch flushes more stages, so penalties grow with depth.",
                    ["google", "amazon", "gate"]),
              ]), has_visual=True),
          dict(L("pipeline-hazards", "Pipeline Hazards",
"""## What a hazard is

A **hazard** stalls the pipeline, breaking the ideal CPI = 1.
Three families: data, control, structural.

## 1. Data hazards — waiting on a value

**RAW (Read After Write)** — the true dependence:
```
add r1, r2, r3    # writes r1
sub r4, r1, r5    # reads r1 -> waits for add
```
**WAR (Write After Read):** `sub r2, r4, r5` must not overwrite r2
before `add r1, r2, r3` reads it.
**WAW (Write After Write):** two writes to r1 — the later one must win.
WAR and WAW are *name* dependences: they only bite in out-of-order
pipelines, where register renaming removes them. RAW is a *true*
dependence — the value genuinely flows forward — and no renaming
can remove it.

## 2. Control hazards — waiting on a decision

After a branch, the next PC is unknown until the branch resolves, so
already-fetched instructions may be wrong and must be flushed.

## 3. Structural hazards — waiting on hardware

Two instructions need the same unit in one cycle — e.g. one memory
port shared by IF (instruction fetch) and MEM (load/store). Fixed by
duplicating the resource (split I/D caches, multi-port register file).

## Fixes at a glance

| Hazard | Fix |
|---|---|
| RAW | Forwarding; stalls when forwarding cannot help |
| WAR / WAW | Register renaming (out-of-order cores) |
| Control | Branch prediction, speculation + flush |
| Structural | Duplicate the resource |""",
              [
                  Q("A compiler engineer sees `add r1, r2, r3` followed by `sub r4, r1, r5` — the second needs r1 before the first writes it. What is this hazard called?",
                    ["A branch target is not yet known",
                     "An instruction writes a register that a later instruction writes again",
                     "An instruction reads a register before an earlier instruction has written its new value",
                     "Two instructions need the ALU in the same cycle"],
                    2, 2,
                    "RAW = Read After Write: the consumer reads a register whose producer has not yet produced the value.",
                    ["gate", "tcs", "infosys"]),
                  Q("In the sequence `add r1, r2, r3` followed by `sub r4, r1, r5`, what hazard exists?",
                    ["WAR hazard on r1",
                     "Structural hazard on the ALU",
                     "No hazard at all",
                     "RAW hazard on r1"],
                    3, 3,
                    "The sub reads r1 which the add writes — a Read-After-Write true dependence on r1.",
                    ["gate", "amazon"]),
                  Q("Which of these is a control hazard?",
                    ["A conditional branch whose outcome is unknown while later instructions are already fetched",
                     "Two writes to the same register",
                     "Two instructions needing the register file at once",
                     "A load followed by an instruction using the loaded value"],
                    0, 5,
                    "Control hazards come from branches/jumps: the next PC is unknown until the branch resolves.",
                    ["gate", "google"]),
                  Q("A processor has ONE memory port shared for instructions and data. An IF fetch and a MEM data access collide. What is this?",
                    ["A control hazard",
                     "A structural hazard",
                     "A WAW hazard",
                     "A RAW data hazard"],
                    1, 6,
                    "Two instructions contending for the same hardware unit in one cycle is a structural (resource) hazard.",
                    ["gate", "amazon"]),
                  Q("WAR and WAW hazards do NOT occur in a classic in-order 5-stage pipeline. Why?",
                    ["Because there are only 5 stages",
                     "Because the compiler removes all WAR/WAW pairs",
                     "Because instructions read operands and write results in fixed program order, so name dependences cannot invert",
                     "Because forwarding handles them"],
                    2, 8,
                    "WAR/WAW are ordering hazards on register names; in-order issue and in-order writeback preserve program order, so they cannot happen. They appear only with out-of-order execution, where renaming fixes them.",
                    ["google", "gate"]),
                  Q("Which hazard can forwarding alone NOT eliminate?",
                    ["WAW between two ALU instructions",
                     "EX-to-EX RAW between two ALU instructions",
                     "MEM-to-EX RAW from an ALU instruction to a later one",
                     "Load-use RAW (a load followed immediately by its consumer)"],
                    3, 9,
                    "A load's data is only available after its MEM stage, but the consumer needs it in EX the very next cycle — even perfect forwarding leaves a 1-cycle bubble.",
                    ["google", "amazon", "gate"]),
              ])),
          dict(L("pipeline-forwarding", "Forwarding & Stalls",
"""## Forwarding: the fast path

Instead of waiting for WB, **forwarding** routes a result directly
from a later stage back to the ALU inputs. Two classic paths:

- **EX → EX**: producer in MEM, consumer in EX — the ALU result feeds
  straight back into the ALU (back-to-back ALU instructions).
- **MEM → EX**: producer in WB, consumer in EX — forwarded from the
  MEM/WB pipeline register.

## Stalls: when forwarding is not enough

A **stall** freezes IF/ID for a cycle and injects a **bubble** into EX.
The unavoidable case is the **load-use hazard**:
```
lw  r1, 0(r2)     # data ready only after MEM
add r3, r1, r4    # needs r1 in EX, one cycle too early
```
Data leaves memory at the end of MEM; the consumer's EX starts a cycle
earlier, so one bubble is mandatory.

## Worked example

With full forwarding:
```
lw  r1, 0(r2)
add r3, r1, r4     # load-use -> 1 stall
sub r5, r3, r6     # EX->EX forwarded -> 0 stalls
```
Total: **1 stall**. Without any forwarding each RAW pair costs 2 stalls
(the consumer waits for the producer's WB) — 4 stalls here. Stalls are
detected in ID by the **hazard detection unit**, which compares register
fields and freezes the PC and IF/ID registers when needed.""",
              [
                  Q("To avoid stalling on a RAW hazard, a designer routes the ALU output directly back to a later stage's input. What is this technique called?",
                    ["Routing a result directly from a later pipeline stage back to the ALU inputs instead of waiting for the register-file write",
                     "Predicting branch outcomes to avoid stalls",
                     "Duplicating the ALU to handle two instructions at once",
                     "Skipping the WB stage for store instructions"],
                    0, 2,
                    "Forwarding bypasses the register file: a freshly computed value is fed from MEM or WB stage outputs straight into the ALU.",
                    ["gate", "tcs", "infosys"]),
                  Q("Two back-to-back ALU instructions (`add` then `sub` using the sum) are handled by which forwarding path?",
                    ["ID to EX",
                     "EX to EX",
                     "MEM to EX",
                     "WB to ID"],
                    1, 4,
                    "When the producer is in MEM and the consumer in EX, the ALU result feeds directly back into the ALU: EX→EX.",
                    ["gate", "amazon"]),
                  Q("When is the MEM→EX forwarding path used?",
                    ["When two loads execute back to back",
                     "When the instruction cache misses",
                     "When the producer is in the WB stage while the consumer is in EX",
                     "When a branch is mispredicted"],
                    2, 5,
                    "MEM→EX forwards from the MEM/WB pipeline register — the producer is one stage further along (in WB) than in the EX→EX case.",
                    ["gate", "google"]),
                  Q("Why does a load-use hazard still need a stall even with full forwarding?",
                    ["The hazard detection unit cannot see load instructions",
                     "Loads do not write registers",
                     "Forwarding only works for stores, not loads",
                     "The load's data is available only after its MEM stage, but the consumer needs it at the start of EX one cycle earlier"],
                    3, 7,
                    "Data leaves memory at the end of MEM; the next instruction's EX begins a cycle before that value could be forwarded, so one bubble is unavoidable.",
                    ["google", "amazon", "gate"]),
                  Q("With full forwarding, how many stall cycles does this sequence need?\n`lw r1,0(r2)` / `add r3,r1,r4` / `sub r5,r3,r6`",
                    ["1",
                     "2",
                     "3",
                     "0"],
                    0, 8,
                    "lw→add is a load-use hazard (1 stall); add→sub is EX→EX forwarded (0 stalls). Total = 1.",
                    ["gate", "amazon"]),
                  Q("Without ANY forwarding, how many stalls does `add r1,r2,r3` / `sub r4,r1,r5` / `add r6,r4,r7` need?",
                    ["2",
                     "4",
                     "6",
                     "0"],
                    1, 9,
                    "Each RAW pair without forwarding costs 2 stalls (consumer waits for the producer's WB): 2 pairs × 2 = 4 stalls.",
                    ["gate", "google"]),
              ])),
          dict(L("pipeline-branch-prediction", "Branch Prediction",
"""## The problem

Branches resolve in EX but fetch chooses the PC two cycles earlier —
a wrong guess flushes instructions (**misprediction penalty**).

## Static prediction: no history, no hardware

- **Always taken / not-taken**: hardwired guess (loops favor taken).
- **BTFN**: backward branches are loop edges (taken), forward are ifs.

## Dynamic prediction: learn from history

**1-bit**: remembers last outcome; one anomaly flips it → two misses.
**2-bit saturating counter** (00–11, taken when ≥ 2) needs two
consecutive anomalies to flip a strong prediction.

## Worked example (verified)

Weakly taken (10); outcomes T,T,T,N,T,N,N,N:

| State | Predict | Actual | Next |
|---|---|---|---|
| 10 | T | T | 11 |
| 11 | T | T | 11 |
| 11 | T | T | 11 |
| 11 | T | N ✗ | 10 |
| 10 | T | T | 11 |
| 11 | T | N ✗ | 10 |
| 10 | T | N ✗ | 01 |
| 01 | N | N | 00 |

**3 mispredictions** of 8.

## BTB and penalty math

The **Branch Target Buffer** caches target addresses so predicted-taken
branches fetch correctly at once. Cost = branch freq × miss rate ×
penalty = 0.2 × 0.1 × 3 = **0.06** extra CPI.""",
              [
                  Q("A simple branch predictor uses the rule 'backward taken, forward not-taken' (BTFN). What is the reasoning behind this rule?",
                    ["Flushing the pipeline on every branch",
                     "A dynamic predictor using 2-bit counters",
                     "A static heuristic: backward branches (loops) predicted taken, forward branches predicted not-taken",
                     "A cache that stores branch target addresses"],
                    2, 2,
                    "BTFN is a zero-hardware static rule exploiting that backward branches are usually loop back-edges.",
                    ["gate", "tcs"]),
                  Q("What is the main weakness of a 1-bit branch predictor?",
                    ["It cannot predict backward branches",
                     "It only works for unconditional jumps",
                     "It needs too much hardware",
                     "A single anomalous outcome flips the prediction, causing two mispredictions around loops"],
                    3, 4,
                    "One bit means one counterexample flips the guess: the loop-exit mispredicts, and then the next loop entry mispredicts too.",
                    ["gate", "amazon", "google"]),
                  Q("A 2-bit saturating counter has states 00, 01, 10, 11. When does it predict 'taken'?",
                    ["In states 10 and 11",
                     "In states 01, 10, and 11",
                     "Only in state 00",
                     "Only in state 11"],
                    0, 5,
                    "Predict taken when the counter is at least 2 (weakly/strongly taken); two consecutive anomalies are needed to flip a strong state.",
                    ["gate", "google"]),
                  Q("2-bit counter starts at weakly taken (10). Outcomes: T,T,T,N,T,N,N,N. How many mispredictions?",
                    ["2",
                     "3",
                     "4",
                     "1"],
                    1, 6,
                    "Simulation: predictions T,T,T,T,T,T,T,N vs actual T,T,T,N,T,N,N,N — misses on outcomes 4, 6, 7 = 3 mispredictions.",
                    ["gate", "amazon"]),
                  Q("What does a Branch Target Buffer (BTB) store?",
                    ["Cache lines evicted by branches",
                     "The last 2-bit counter values for each register",
                     "Recently used branch target addresses, keyed by branch instruction address",
                     "The return addresses of function calls"],
                    2, 8,
                    "The BTB caches where predicted-taken branches go, so fetch can redirect to the target address immediately.",
                    ["google", "gate"]),
                  Q("A 5-stage pipeline resolves branches in EX (3-cycle mispredict penalty). 20% of instructions are branches, mispredict rate 10%. What is the CPI contribution of mispredictions, and total CPI (base 1.0)?",
                    ["0.02, total 1.02",
                     "0.3, total 1.3",
                     "0.6, total 1.6",
                     "0.06, total 1.06"],
                    3, 10,
                    "Cost = 0.20 × 0.10 × 3 = 0.06 extra cycles per instruction, so CPI = 1.06.",
                    ["gate", "google", "amazon"]),
              ])),
          dict(L("pipeline-superscalar", "Superscalar & Out-of-Order",
"""## Beyond IPC = 1

A scalar pipeline tops out at IPC = 1. A **superscalar** core fetches,
decodes, and executes several instructions per cycle — its **width**
(2, 4, 8) is the theoretical max IPC.

## What width demands

Multiple decoders, enough functional units, a wide multi-ported register
file — and real **instruction-level parallelism (ILP)**: independent
instructions must actually sit side by side in the program.

## Superscalar vs VLIW

| | Superscalar | VLIW |
|---|---|---|
| Finds parallelism | Hardware, at run time | Compiler, at compile time |
| Instruction format | Normal; hardware groups ops | Compiler packs one long word |
| Binary compat | Easier across widths | Breaks when width changes |

## Out-of-order: Tomasulo's algorithm

Instructions execute when operands are ready, ignoring program order:
- **Reservation stations** hold waiting instructions.
- **Register renaming** kills WAR/WAW name hazards.
- The **common data bus (CDB)** broadcasts results to waiters.
Program order is restored at in-order **commit**, keeping exceptions
precise.

## IPC > 1, but rarely = width

Real IPC trails width: data dependences, branch mispredicts, cache
misses, structural limits. IPC ≈ 2–3 on a 4-wide core is typical —
and only multiple issue lets IPC exceed 1 at all.""",
              [
                  Q("A chip datasheet advertises a '4-wide superscalar' core. What makes a processor superscalar?",
                    ["It fetches, decodes, and executes multiple instructions per cycle",
                     "It has a very deep pipeline of 20+ stages",
                     "It uses microcode for every instruction",
                     "It runs at a very high clock speed"],
                    0, 2,
                    "Superscalar = multiple issue per cycle; width 4 means up to 4 instructions begin execution each cycle.",
                    ["gate", "tcs", "infosys"]),
                  Q("A program runs on a 4-wide superscalar core. What does an IPC of 2.5 mean?",
                    ["2.5 cycles per instruction",
                     "On average 2.5 instructions complete per cycle — possible only because of multiple issue",
                     "The clock is 2.5 GHz",
                     "25% of instructions are branches"],
                    1, 3,
                    "IPC > 1 is the signature of superscalar execution: more than one instruction retiring per cycle on average.",
                    ["gate", "amazon"]),
                  Q("A compiler team debates VLIW vs superscalar for a DSP chip. How does VLIW differ from superscalar?",
                    ["They are identical; VLIW is just the marketing name",
                     "VLIW runs at a higher voltage",
                     "VLIW relies on the compiler to pack independent operations; superscalar finds parallelism in hardware at run time",
                     "VLIW cannot do floating point"],
                    2, 5,
                    "VLIW moves scheduling to compile time (long instruction words), superscalar does dynamic scheduling in hardware.",
                    ["google", "gate"]),
                  Q("In an interview about out-of-order CPUs, you are asked: what problem does Tomasulo's algorithm solve?",
                    ["Branch prediction for indirect jumps",
                     "Virtual memory page faults",
                     "Cache coherence between cores",
                     "Letting instructions execute out of order as soon as operands are ready, via reservation stations and renaming"],
                    3, 7,
                    "Tomasulo enables out-of-order execution: reservation stations hold waiting ops, renaming removes WAR/WAW, the CDB broadcasts results.",
                    ["google", "amazon", "gate"]),
                  Q("A 4-wide superscalar core is being benchmarked. What is its theoretical maximum IPC?",
                    ["4",
                     "8",
                     "1",
                     "2"],
                    0, 8,
                    "Maximum IPC equals the issue width: 4 instructions per cycle if all are independent and resources allow.",
                    ["gate", "tcs"]),
                  Q("A 4-wide core sustains IPC ≈ 2.2 on real code. Which is NOT a reason it falls short of 4?",
                    ["Cache misses stalling the back end",
                     "The register file having too many ports",
                     "True data dependences between instructions",
                     "Branch mispredictions flushing the front end"],
                    1, 9,
                    "Too many register-file ports would help, not hurt. Dependences, mispredicts, and misses are the real IPC limiters.",
                    ["google", "amazon"]),
              ])),
          dict(L("pipeline-performance", "Pipeline Performance Math",
"""## The core formulas

For a k-stage pipeline and n instructions:

- Sequential cycles = k × n
- Pipelined cycles = k + n − 1
- **Speedup** = sequential / pipelined
- **Efficiency** = speedup / k

## Worked example (verified)

k = 5, n = 100:
- Sequential: 5 × 100 = **500 cycles**
- Pipelined: 5 + 100 − 1 = **104 cycles**
- Speedup = 500/104 ≈ **4.81**
- Efficiency = 4.81/5 ≈ **0.96**
As n grows, speedup approaches k — depth is the ceiling.

## CPI with stalls (worked)

20% loads, 25% of loads followed by a dependent (1 stall each):
stalls/instr = 0.20 × 0.25 × 1 = 0.05 → **CPI = 1.05**.
General form: CPI = 1 + Σ (frequency × penalty) over every hazard.

## Deeper pipeline (worked)

k = 10, n = 1000: sequential 10,000; pipelined 10+1000−1 = 1009;
speedup = 10000/1009 ≈ **9.91** — close to 10 but never above it,
because the k−1 fill/drain cycles are pure overhead.

## Interview framing

"Why not exactly k?" — fill/drain plus hazard stalls. "How to raise
throughput?" — cut stalls (forwarding, prediction) or widen issue
(superscalar); depth alone has diminishing returns.""",
              [
                  Q("In a computer-architecture exam you must write the standard formula for pipeline speedup. It is:",
                    ["1 / (1 + stall rate)",
                     "Pipelined cycles / sequential cycles",
                     "Sequential cycles / pipelined cycles",
                     "Number of stages × clock frequency"],
                    2, 3,
                    "Speedup = time without the enhancement / time with it = sequential cycles ÷ pipelined cycles.",
                    ["gate", "tcs"]),
                  Q("A 5-stage pipeline runs 100 instructions with no hazards. How many cycles?",
                    ["100",
                     "505",
                     "500",
                     "104"],
                    3, 4,
                    "Pipelined cycles = k + n − 1 = 5 + 100 − 1 = 104.",
                    ["gate", "amazon", "infosys"]),
                  Q("For the 5-stage, 100-instruction case above, what is the speedup over sequential execution?",
                    ["4.81",
                     "4.0",
                     "1.04",
                     "5.0"],
                    0, 6,
                    "Sequential = 500 cycles; 500/104 ≈ 4.81, slightly below the ideal 5× due to fill/drain.",
                    ["gate", "google"]),
                  Q("What is pipeline efficiency for that case?",
                    ["1.0",
                     "0.96",
                     "0.2",
                     "4.81"],
                    1, 7,
                    "Efficiency = speedup / k = 4.81/5 ≈ 0.96 — the pipeline achieves 96% of its ideal gain.",
                    ["gate", "amazon"]),
                  Q("20% of instructions are loads; 25% of loads cause a 1-cycle load-use stall. What is the CPI?",
                    ["2.0",
                     "1.25",
                     "1.05",
                     "1.20"],
                    2, 8,
                    "Stalls/instr = 0.20 × 0.25 × 1 = 0.05, so CPI = 1 + 0.05 = 1.05.",
                    ["gate", "google"]),
                  Q("A 10-stage pipeline runs 1000 instructions, no hazards. Speedup ≈ 9.91. Why can it never reach exactly 10?",
                    ["Because forwarding paths are limited",
                     "Because the clock slows down with depth",
                     "Because CPI cannot drop below 1",
                     "The k−1 fill and drain cycles are overhead no steady-state throughput can recover"],
                    3, 10,
                    "Speedup = kn/(k+n−1) < k always; the fill/drain overhead keeps it strictly below the stage count.",
                    ["google", "gate", "amazon"]),
              ])),
      ]),
    M("memory-hierarchy", "Memory Hierarchy",
      "Cache mapping, write policies, AMAT, virtual memory, TLB, page replacement.",
      [
          dict(L("memory-pyramid", "The Memory Pyramid & Locality",
"""## The pyramid

Small and fast at the top, big and slow at the bottom:

| Level | Typical size | Access time |
|---|---|---|
| Registers | ~1 KB | < 1 cycle |
| L1 cache | 32–64 KB | ~1 ns |
| L2 cache | 256 KB–1 MB | ~3–5 ns |
| L3 cache | 8–64 MB (shared) | ~10–20 ns |
| RAM | 8–64 GB | ~60–100 ns |
| SSD | 256 GB–4 TB | ~50–150 µs |
| HDD / network | TBs | ~ms |

Each level is ~10–100× larger and slower than the one above.

## Why it works: locality

- **Temporal locality**: touch it now, touch it again soon (a loop
  counter). Caches keep recently used blocks for this.
- **Spatial locality**: touch it now, touch its neighbors soon
  (array traversal). Caches move multi-word **blocks** (32–128 B).

## Hits and misses

The CPU checks L1 → L2 → L3 → RAM. A **hit** serves data at that
level's speed; a **miss** drops to the next level. Locality keeps most
accesses high in the pyramid, so average speed ≈ cache speed at
near-disk cost per bit.

## Miss types

- **Compulsory (cold)**: first touch of a block — unavoidable.
- **Capacity**: working set bigger than the cache; useful blocks evict
  each other — fixed by a bigger cache or smaller working set.
- **Conflict**: too many blocks map to the same set (next lesson).""",
              [
                  Q("Which level of the memory hierarchy is the fastest and smallest?",
                    ["CPU registers",
                     "SSD",
                     "L3 cache",
                     "Main memory (RAM)"],
                    0, 1,
                    "Registers sit at the very top of the pyramid: a few dozen words, accessible in under a cycle.",
                    ["gate", "tcs", "infosys"]),
                  Q("A loop repeatedly touches the same few variables. Which locality principle explains why caching helps here?",
                    ["Accessing nearby addresses in sequence",
                     "Re-accessing the same data within a short time window",
                     "Storing data permanently on disk",
                     "Fetching instructions before they are needed"],
                    1, 3,
                    "Temporal locality = reuse over time (a loop counter); it is why caches retain recently used blocks.",
                    ["gate", "amazon"]),
                  Q("Marching through an array element by element exploits which locality, and what cache feature serves it?",
                    ["Spatial locality; fully associative mapping",
                     "Temporal locality; larger cache size",
                     "Spatial locality; multi-word cache blocks fetched together",
                     "Temporal locality; write-back policy"],
                    2, 4,
                    "Sequential array access touches neighboring addresses — spatial locality — so fetching whole blocks amortizes the miss.",
                    ["gate", "google"]),
                  Q("What is a typical L1 data cache size on a modern core?",
                    ["8 MB",
                     "16 GB",
                     "1 KB",
                     "32–64 KB"],
                    3, 6,
                    "L1 is tens of kilobytes (≈32–64 KB); megabytes belong to L3, gigabytes to RAM.",
                    ["amazon", "tcs", "gate"]),
                  Q("Why does the memory pyramid give near-cache speed at near-disk cost?",
                    ["Because locality makes most accesses hit in the small fast levels, so the average is dominated by cache speed",
                     "Because disks are now faster than RAM",
                     "Because the OS compresses everything",
                     "Because RAM is as fast as L1"],
                    0, 7,
                    "Locality concentrates accesses at the top of the pyramid; the average access time is a locality-weighted average, not the slowest level.",
                    ["google", "gate"]),
                  Q("A program's working set exceeds the cache size, so useful blocks keep evicting each other. Enlarging the cache fixes it. Which miss type is this?",
                    ["Compulsory miss",
                     "Capacity miss",
                     "Conflict miss",
                     "Coherence miss"],
                    1, 9,
                    "Capacity misses come from a working set larger than the cache; bigger caches (or smaller working sets) are the cure. Compulsory misses happen on first touch regardless of size.",
                    ["gate", "amazon", "google"]),
              ]), has_visual=True),
          dict(L("cache-mapping", "Cache Mapping",
"""## The address split

```
| ---- tag ---- | --- index --- | - offset - |
```
- **offset** = byte inside the block → log2(block size) bits
- **index** = which set → log2(number of sets) bits
- **tag** = the rest → stored and compared for a hit

## Direct mapped: worked (verified)

32-bit address, 64 KB cache, 32 B blocks:
- offset = log2(32) = **5 bits**
- blocks = 64 KB/32 B = 2048 → index = log2(2048) = **11 bits**
- tag = 32 − 11 − 5 = **16 bits**
Each block has exactly one home; hot blocks colliding on it thrash
(conflict misses).

## Set-associative: worked (verified)

4-way, 128 KB cache, 64 B blocks:
- offset = log2(64) = **6 bits**
- sets = 128 KB/(4×64 B) = 512 → index = log2(512) = **9 bits**
- tag = 32 − 9 − 6 = **17 bits**
Fewer conflicts than direct mapped; cheaper than fully associative.

## Fully associative

Any block in any line — no index field (tag = 32 − offset). Zero
conflict misses, but comparing against every line is costly, so it is
used for small structures (e.g. TLBs).

## The method (memorize)

1. offset = log2(block size)
2. sets = cache size / (ways × block size); index = log2(sets)
3. tag = address bits − index − offset""",
              [
                  Q("A cache uses 32-byte blocks. How many offset bits does the address need?",
                    ["32",
                     "4",
                     "5",
                     "6"],
                    2, 3,
                    "offset bits = log2(block size) = log2(32) = 5.",
                    ["gate", "tcs"]),
                  Q("32-bit address, 64 KB direct-mapped cache, 32 B blocks. How many index bits?",
                    ["5",
                     "16",
                     "10",
                     "11"],
                    3, 4,
                    "Blocks = 65536/32 = 2048; index = log2(2048) = 11.",
                    ["gate", "amazon", "infosys"]),
                  Q("For the cache above (32-bit addr, 64 KB direct-mapped, 32 B blocks), how many tag bits?",
                    ["16",
                     "21",
                     "11",
                     "5"],
                    0, 6,
                    "tag = 32 − index − offset = 32 − 11 − 5 = 16.",
                    ["gate", "google"]),
                  Q("4-way set-associative, 128 KB cache, 64 B blocks, 32-bit addresses. How many sets, and how many index bits?",
                    ["1024 sets, 10 index bits",
                     "512 sets, 9 index bits",
                     "256 sets, 8 index bits",
                     "2048 sets, 11 index bits"],
                    1, 7,
                    "sets = 131072/(4×64) = 512; index = log2(512) = 9.",
                    ["gate", "amazon"]),
                  Q("For that 4-way cache, how many tag bits per line?",
                    ["23",
                     "9",
                     "17",
                     "15"],
                    2, 9,
                    "tag = 32 − 9 (index) − 6 (offset) = 17.",
                    ["gate", "google"]),
                  Q("2-way set-associative, 32 KB cache, 16 B blocks, 32-bit addresses. Tag bits?",
                    ["16",
                     "10",
                     "4",
                     "18"],
                    3, 10,
                    "offset = log2(16) = 4; sets = 32768/(2×16) = 1024 → index 10; tag = 32 − 10 − 4 = 18.",
                    ["gate", "amazon"]),
              ])),
          dict(L("cache-write-policies", "Write-Through vs Write-Back",
"""## Write-through

Every write updates **cache and memory** immediately. Memory is always
consistent — good for I/O and multiprocessors — but every write pays
full memory latency. The fix: a **write buffer**, a small FIFO holding
pending writes so the CPU rarely stalls while it drains.

## Write-back

Writes update **only the cache**; a **dirty bit** per block records the
difference, and the block is written to memory only on eviction.
Far less memory traffic (many writes → one write-back), but memory is
stale until eviction — coherence protocols must manage sharing.

| | Write-through | Write-back |
|---|---|---|
| Memory traffic | high (every write) | low (on eviction) |
| Extra hardware | write buffer | dirty bit per block |
| Memory fresh? | always | only after eviction |

## On a write miss: allocate or not?

- **Write-allocate**: fetch the block, then write. Pairs with write-back.
- **No-write-allocate**: write straight to memory, skip the cache.
  Pairs with write-through; avoids polluting the cache with data that
  will never be read (streaming outputs).

## Interview guidance

Default to write-back + write-allocate (least traffic); choose
write-through + no-write-allocate where immediate memory consistency
or simplicity matters. Name the hardware: write buffer vs dirty bit.""",
              [
                  Q("A designer requires that main memory always holds the latest written data. Which cache policy does this describe?",
                    ["Every write updates both the cache and main memory immediately",
                     "Writes bypass the cache entirely on a miss",
                     "Writes are buffered and never reach memory",
                     "Writes update only the cache, with a dirty bit marking modified blocks"],
                    0, 2,
                    "Write-through pushes every write to main memory at once, keeping memory always consistent.",
                    ["gate", "tcs", "infosys"]),
                  Q("A cache line has its dirty bit set in a write-back cache. What does that bit signify?",
                    ["Counting how many times a block was read",
                     "Marking blocks that have been modified in cache but not yet written to memory",
                     "Marking corrupted blocks for replacement",
                     "Indicating which set a block belongs to"],
                    1, 3,
                    "The dirty bit records that the cached copy differs from memory, so it must be written back on eviction.",
                    ["gate", "amazon"]),
                  Q("What problem does a write buffer solve in a write-through cache?",
                    ["Branch mispredictions",
                     "Conflict misses",
                     "CPU stalls on every write's full memory latency, by queueing writes to drain in the background",
                     "Dirty blocks accumulating"],
                    2, 5,
                    "The write buffer is a small FIFO between cache and memory that lets the CPU continue while writes drain asynchronously.",
                    ["gate", "google"]),
                  Q("On a write miss, a cache first fetches the block from memory and then performs the write into it. This policy is called…",
                    ["write-back",
                     "write-combining",
                     "no-write-allocate",
                     "write-allocate"],
                    3, 6,
                    "Write-allocate (fetch-on-write) loads the block on a write miss; it pairs naturally with write-back.",
                    ["gate", "amazon"]),
                  Q("A workload performs millions of repeated writes to a small array. Which policy minimizes memory traffic?",
                    ["Write-back, because repeated writes to one block cost a single eventual write to memory",
                     "Write-through, because memory stays consistent",
                     "No-write-allocate, because the array is small",
                     "Write-through with a large write buffer"],
                    0, 8,
                    "Write-back coalesces many cache writes into one memory write per evicted dirty block — ideal for write-heavy reuse.",
                    ["google", "amazon", "gate"]),
                  Q("Why pair no-write-allocate with write-through for streaming output buffers?",
                    ["It makes writes faster than write-back",
                     "Streaming writes are never re-read, so allocating cache lines for them would evict useful data for no benefit",
                     "It eliminates the need for a dirty bit",
                     "It reduces compulsory misses"],
                    1, 9,
                    "Write-only streaming data has no temporal locality; caching it only pollutes the cache, so bypassing is the win.",
                    ["google", "gate"]),
              ])),
          dict(L("cache-performance", "AMAT & Cache Math",
"""## AMAT: the one formula

**AMAT = hit time + miss rate × miss penalty**
(miss rate as a fraction; penalty is the *extra* beyond hit time.)

## Worked example (verified)

Hit 1 cycle, miss rate 5%, penalty 100 cycles:
AMAT = 1 + 0.05 × 100 = **6 cycles**.
Misses dominate: halving the miss rate to 2.5% gives
AMAT = 1 + 2.5 = **3.5 cycles**.

## Two levels (verified)

AMAT = L1_hit + L1_miss × (L2_hit + L2_miss × mem_penalty).
With 1 / 5% / 10 / 20% / 200:
AMAT = 1 + 0.05 × (10 + 0.20 × 200) = 1 + 0.05 × 50 = **3.5 cycles**.
(L2 miss rate is *local*: misses ÷ L2 accesses.)

## Levers and trade-offs

| Lever | Effect | Cost |
|---|---|---|
| Bigger cache | fewer capacity/conflict misses | slower hit, more area |
| More associativity | fewer conflict misses | slower hit, more power |
| Larger blocks | fewer compulsory misses | pollution, longer penalty |

## GATE traps

Convert % to fractions; distinguish *local* vs *global* miss rates in
multi-level hierarchies; remember hit time is paid by every access.""",
              [
                  Q("What is the AMAT formula?",
                    ["hit time − miss rate × miss penalty",
                     "hit time × miss rate × miss penalty",
                     "hit time + miss rate × miss penalty",
                     "miss rate / (hit time + miss penalty)"],
                    2, 2,
                    "AMAT = hit time + miss rate × miss penalty: every access pays the hit time, misses additionally pay the penalty.",
                    ["gate", "tcs"]),
                  Q("L1 hit time 1 cycle, miss rate 5%, miss penalty 100 cycles. AMAT?",
                    ["101 cycles",
                     "5 cycles",
                     "500 cycles",
                     "6 cycles"],
                    3, 4,
                    "AMAT = 1 + 0.05 × 100 = 6 cycles.",
                    ["gate", "amazon", "infosys"]),
                  Q("In the example above, the miss rate is halved to 2.5%. New AMAT?",
                    ["3.5 cycles",
                     "2.5 cycles",
                     "4.5 cycles",
                     "6 cycles"],
                    0, 5,
                    "AMAT = 1 + 0.025 × 100 = 3.5 cycles — halving a dominant miss term nearly halves AMAT.",
                    ["gate", "google"]),
                  Q("Two-level hierarchy: L1 hit 1, L1 miss 5%, L2 hit 10, L2 local miss 20%, memory penalty 200. AMAT?",
                    ["51 cycles",
                     "3.5 cycles",
                     "6 cycles",
                     "11 cycles"],
                    1, 7,
                    "AMAT = 1 + 0.05×(10 + 0.20×200) = 1 + 0.05×50 = 3.5 cycles.",
                    ["gate", "amazon"]),
                  Q("Why might doubling the L1 cache size sometimes NOT improve AMAT?",
                    ["Associativity drops automatically",
                     "Miss rate always drops, so it always helps",
                     "A bigger cache can increase hit time, and the slower hits apply to every access",
                     "Hit time is independent of cache size"],
                    2, 8,
                    "Every access pays hit time; if a larger, slower L1 raises hit time more than the miss-rate reduction saves, AMAT worsens.",
                    ["google", "gate"]),
                  Q("Hit time 1 cycle, miss penalty 200 cycles. What is the maximum miss rate that keeps AMAT ≤ 4 cycles?",
                    ["4%",
                     "0.5%",
                     "2%",
                     "1.5%"],
                    3, 10,
                    "1 + mr×200 ≤ 4 → mr ≤ 3/200 = 0.015 = 1.5%.",
                    ["gate", "google", "amazon"]),
              ])),
          dict(L("virtual-memory", "Virtual Memory & Paging",
"""## The idea

Each process gets its own **virtual address space**, translated to
physical addresses at run time: isolation, the illusion of more RAM
than exists, simpler linking.

## Pages and frames

Virtual memory comes in **pages**, physical RAM in **frames** (often
4 KB). The **page table** maps page number → frame number (+ permission
bits); the offset inside the page passes through untouched.

## Why one level fails: the math (verified)

32-bit addresses, 4 KB pages: pages = 2³²/2¹² = 2²⁰ = **1,048,576**;
at 4 B per entry the flat table is 2²⁰ × 4 B = **4 MB per process** —
far too much for small programs.

## Multi-level page tables

Split the page number — e.g. **10 bits directory + 10 bits table +
12 bits offset**. Each second-level table is 2¹⁰ × 4 B = **4 KB**
(one page) and is allocated **only for regions actually used**, so
sparse address spaces need a handful of tables, not one 4 MB monster.

## Internal fragmentation

Fixed-size pages leave the last page partly empty — **internal
fragmentation** (≈ half a page per segment on average). Bigger pages
need fewer TLB entries but waste more; OSes mix 4 KB and huge (2 MB)
pages for the best of both.""",
              [
                  Q("An OS interviewer asks you to distinguish pages from frames. What is the difference?",
                    ["A page is a fixed-size block of virtual memory; a frame is the corresponding block of physical memory",
                     "A frame is virtual, a page is physical",
                     "Pages are 4 KB, frames are always 1 MB",
                     "They are synonyms"],
                    0, 2,
                    "Pages live in the virtual address space, frames in physical RAM; the page table maps page numbers to frame numbers.",
                    ["gate", "tcs", "infosys"]),
                  Q("With 32-bit virtual addresses and 4 KB pages, how many pages are in the address space?",
                    ["2^10",
                     "2^20",
                     "2^12",
                     "2^32"],
                    1, 4,
                    "Pages = 2^32 / 2^12 = 2^20 = 1,048,576.",
                    ["gate", "amazon"]),
                  Q("With 4-byte page-table entries, how big is the single-level page table for the above?",
                    ["4 KB",
                     "4 MB",
                     "1 MB",
                     "16 MB"],
                    1, 5,
                    "2^20 entries × 4 B = 4,194,304 B = 4 MB per process.",
                    ["gate", "google"]),
                  Q("Why do real systems use multi-level page tables instead of one flat table?",
                    ["They eliminate page faults",
                     "They remove the need for a TLB",
                     "They translate addresses faster",
                     "Second-level tables are allocated only for virtual regions actually in use, so sparse address spaces need far less memory"],
                    3, 7,
                    "A flat 4 MB table is wasteful for sparse spaces; two levels allocate 4 KB second-level tables on demand.",
                    ["gate", "amazon", "google"]),
                  Q("In a 10/10/12 two-level split (32-bit address, 4 KB pages), how big is one second-level page table?",
                    ["4 KB",
                     "1 KB",
                     "10 KB",
                     "4 MB"],
                    0, 8,
                    "2^10 entries × 4 B = 4096 B = 4 KB — conveniently exactly one page.",
                    ["gate", "amazon"]),
                  Q("A process needs 10 KB with 4 KB pages. How many pages are allocated, and what is the internal fragmentation?",
                    ["2 pages, 6 KB wasted",
                     "3 pages, 2 KB wasted",
                     "3 pages, 0 KB wasted",
                     "10 pages, 30 KB wasted"],
                    1, 9,
                    "ceil(10/4) = 3 pages = 12 KB allocated; 12 − 10 = 2 KB wasted inside the last page.",
                    ["gate", "tcs"]),
              ])),
          dict(L("memory-tlb", "TLB",
"""## Why the TLB exists

Without it, every access pays a page-table walk first — 1–2 extra
memory reads per access. The **TLB** caches recent virtual→physical
translations and is checked before the page table.

## Hit vs miss

- **Hit**: translation in the TLB → one TLB lookup (c) + one memory
  access (m).
- **Miss**: walk the page table (one extra memory access), then the
  data → one TLB lookup + two memory accesses.

## Effective Access Time

**EAT = h × (c + m) + (1 − h) × (c + 2m)**

**Worked (verified):** h = 95%, c = 10 ns, m = 100 ns:
EAT = 0.95 × 110 + 0.05 × 210 = 104.5 + 10.5 = **115 ns** —
about half the 220 ns an uncached translation would cost.

## Design notes

- TLBs are small (64–2048 entries) and usually **fully associative**.
- On a **context switch** the OS flushes the TLB (or tags entries with
  an **ASID**), since one process's translations are meaningless to
  the next.
- A miss with the page in RAM is cheap; a miss with the page on disk
  is a **page fault** — milliseconds, millions of times slower.""",
              [
                  Q("Address translation is slow, so the CPU keeps a TLB. First principles: what does a TLB cache?",
                    ["Disk blocks of the swap file",
                     "Recently used data cache lines",
                     "Recent virtual-page-number to physical-frame-number translations",
                     "Branch target addresses"],
                    2, 2,
                    "The TLB (Translation Lookaside Buffer) caches page-table entries so most translations avoid a page-table walk.",
                    ["gate", "tcs", "infosys"]),
                  Q("On a TLB hit (single-level page table), how many memory accesses does a data access need?",
                    ["2",
                     "3",
                     "0",
                     "1"],
                    3, 4,
                    "TLB hit gives the frame directly: one TLB lookup + one memory access for the data.",
                    ["gate", "amazon"]),
                  Q("TLB hit ratio 95%, TLB time 10 ns, memory time 100 ns. What is the effective access time?",
                    ["115 ns",
                     "210 ns",
                     "220 ns",
                     "110 ns"],
                    0, 6,
                    "EAT = 0.95×110 + 0.05×210 = 104.5 + 10.5 = 115 ns.",
                    ["gate", "google", "amazon"]),
                  Q("On a TLB miss with the page resident in RAM (single-level table), how many memory accesses total?",
                    ["2",
                     "3",
                     "0",
                     "1"],
                    0, 7,
                    "One access to read the page-table entry, then one for the actual data = 2 memory accesses.",
                    ["gate", "tcs"]),
                  Q("TLB hit ratio 99%, TLB time 20 ns, memory time 100 ns. EAT?",
                    ["119 ns",
                     "120 ns",
                     "121 ns",
                     "140 ns"],
                    2, 9,
                    "EAT = 0.99×(20+100) + 0.01×(20+200) = 118.8 + 2.2 = 121 ns.",
                    ["gate", "amazon", "google"]),
                  Q("After a context switch, stale translations could corrupt the newly scheduled process. Why must the OS flush (or ASID-tag) the TLB?",
                    ["The TLB is too small for two processes",
                     "Page tables are rebuilt on every switch",
                     "To save power",
                     "Virtual addresses are per-process, so stale translations would map the new process to the old process's physical frames"],
                    3, 10,
                    "The same virtual page number means different physical frames in different processes; unflushed entries would corrupt the new process's memory view.",
                    ["google", "gate"]),
              ])),
          dict(L("page-replacement", "Page Replacement Algorithms",
"""## The setting

On a page fault with no free frame, the OS evicts a victim. Goal:
minimize future faults.

## The three algorithms

- **FIFO**: evict the longest-resident page. Simple queue, but ignores
  usage — a hot page can be evicted for being old.
- **LRU**: evict the least recently used page. Exploits temporal
  locality; usually approximated (clock algorithm).
- **Optimal (MIN)**: evict the page used farthest in the future.
  Needs the future — a yardstick, not an implementation.

## Worked: 7,0,1,2,0,3,0,4 with 3 frames (verified by simulation)

- FIFO → **7 faults**
- LRU → **6 faults**
- Optimal → **6 faults**

## Belady's anomaly

More frames can *increase* FIFO faults. Reference string
1,2,3,4,1,2,5,1,2,3,4,5 (verified by simulation):
- 3 frames → **9 faults**; 4 frames → **10 faults**.
LRU and Optimal never do this: their **stack property** (pages in n
frames ⊆ pages in n+1 frames) makes more frames monotonically better.

| | FIFO | LRU | Optimal |
|---|---|---|---|
| Victim | oldest loaded | least recently used | farthest next use |
| Needs future? | no | no | yes |
| Belady's anomaly? | yes | no | no |""",
              [
                  Q("A memory manager uses FIFO page replacement and a fault occurs. Which page gets evicted?",
                    ["The page that has been in memory the longest",
                     "The page whose next use is farthest away",
                     "A randomly chosen page",
                     "The least recently used page"],
                    0, 3,
                    "FIFO evicts the oldest-loaded page, maintaining frames as a simple queue.",
                    ["gate", "tcs", "infosys"]),
                  Q("Reference string 7,0,1,2,0,3,0,4 with 3 frames. How many page faults under FIFO?",
                    ["5",
                     "7",
                     "6",
                     "8"],
                    1, 4,
                    "Simulating FIFO: faults on 7,0,1,2,3,0,4 = 7 faults (verified by simulation).",
                    ["gate", "amazon"]),
                  Q("Same string and frames. Page faults under LRU?",
                    ["8",
                     "7",
                     "6",
                     "5"],
                    2, 6,
                    "LRU simulation gives 6 faults — one fewer than FIFO, since it keeps the reused page 0.",
                    ["gate", "google"]),
                  Q("Same string and frames. Page faults under Optimal, and why is Optimal not used in practice?",
                    ["6, because it requires knowing future references",
                     "7, because it is slower than FIFO",
                     "5, because it needs extra hardware",
                     "6, because it causes Belady's anomaly"],
                    0, 7,
                    "Optimal gives 6 faults here, but evicting the farthest-future page needs knowledge of the future — it is a theoretical yardstick only.",
                    ["gate", "amazon"]),
                  Q("Belady's anomaly on 1,2,3,4,1,2,5,1,2,3,4,5: FIFO gives 9 faults with 3 frames and 10 with 4. What does this show, and which algorithm exhibits it?",
                    ["More frames can hurt; FIFO",
                     "Fewer frames always help; Optimal",
                     "Frame count is irrelevant; LRU",
                     "More frames always help; LRU"],
                    0, 9,
                    "FIFO can fault more with more frames (9→10 here) — Belady's anomaly, verified by simulation.",
                    ["gate", "google", "amazon"]),
                  Q("Why do LRU and Optimal never suffer Belady's anomaly?",
                    ["They use more frames than FIFO",
                     "They have the stack property: pages resident with n frames are always a subset of those with n+1 frames",
                     "They never cause page faults",
                     "They are implemented in hardware"],
                    1, 10,
                    "The stack property guarantees monotonic improvement with more frames, so the anomaly is impossible.",
                    ["google", "gate"]),
              ])),
      ]),
]
