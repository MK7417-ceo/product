"""Seed content: Computer Organization & Architecture — Modules 1-2
(Digital Logic, CPU Architecture).

Part-file for the SkillForge curriculum seed. All content is original:
every lesson theory and every question is written from scratch for
GATE + interview preparation. Every numerical answer (binary/hex
conversions, K-map minimizations, ALU flag computations, effective
addresses, opcode math, vector-table sizing, counter frequencies) was
verified by running Python before being baked into the file.

Exports a single variable, ``MODULES``: a list of 2 module dicts, each
with nested lesson dicts and, inside those, question dicts.

Module 1 ``digital-logic``   — 6 lessons (number systems, Boolean
algebra, K-maps, combinational circuits, flip-flops, counters &
shift registers).
Module 2 ``cpu-architecture`` — 7 lessons (ALU, control unit,
fetch-decode-execute, addressing modes, RISC vs CISC, instruction
formats, interrupts & exceptions).
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
    M("digital-logic", "Digital Logic",
      "Number systems, Boolean algebra, K-maps, combinational and sequential circuits.",
      [
          L("digital-logic-number-systems", "Number Systems: Binary, Octal, Hex",
            """# Number Systems: Binary, Octal, Hex

Digital hardware speaks **binary** (base 2). Humans use **octal**
(base 8) and **hex** (base 16): 3 bits per octal digit, 4 per hex digit.

## Base conversions

| From → To | Method |
|---|---|
| Decimal → Binary | Repeatedly divide by 2, read remainders bottom-up |
| Binary → Decimal | Sum of place values: each `1` contributes 2^position |
| Binary ↔ Hex/Octal | Group bits in fours (hex) or threes (octal) |

## Worked example 1: 45₁₀ → binary

45 = 32 + 8 + 4 + 1, so set bits 5, 3, 2, 0:
```
  32  16   8   4   2   1
   1   0   1   1   0   1   →  101101₂   (32+8+4+1 = 45 ✓)
```

## Worked example 2: 0x2F → decimal

`0x2F = 2 × 16 + 15 = 32 + 15 = 47` ✓

## Worked example 3: 110101₂ → hex

Group in fours from the right: `11 0101` → `0011 0101` → **0x35**.
Check: 0x35 = 53 and 110101₂ = 32+16+4+1 = 53 ✓

## Negative numbers: 2's complement

Negate: invert all bits, add 1. Signed n-bit range: **−2ⁿ⁻¹ … 2ⁿ⁻¹−1**.
−45 in 8 bits: `00101101` → `11010010` → **`11010011`** ✓

## Fractions

`1010.11₂ = 8 + 2 + 1/2 + 1/4 = 10.75`. Decimal → binary fraction:
multiply by 2 repeatedly, read integer parts top-down:
0.625 → 1, 0, 1, so `0.625₁₀ = 0.101₂` ✓
""",
            [
                Q("A debugger shows a CPU register holding the value 45. What bit pattern is actually stored in the register?",
                  ["101011", "101101", "110101", "100101"],
                  1, 2,
                  "45 = 32 + 8 + 4 + 1, so bits at positions 5, 3, 2, 0 are set: 101101.",
                  ["gate", "tcs", "infosys"]),
                Q("A memory dump shows the byte 0x2F at some address. What decimal value does that byte represent?",
                  ["0x2F = 47", "0x2F = 45", "0x2F = 52", "0x2F = 41"],
                  0, 4,
                  "0x2F = 2×16 + 15 = 32 + 15 = 47.",
                  ["gate", "tcs"]),
                Q("A logic analyzer captures the 6-bit signal 110101 on a data bus. Express this value in hexadecimal.",
                  ["0x25", "0x53", "0xD5", "0x35"],
                  3, 5,
                  "Group in fours: 0011 0101 → 3 and 5, giving 0x35.",
                  ["gate", "infosys"]),
                Q("What is the 8-bit 2's complement representation of −45?",
                  ["10110011", "11010011", "11010010", "00101101"],
                  1, 6,
                  "45 = 00101101; invert to 11010010 and add 1 → 11010011.",
                  ["gate", "microsoft"]),
                Q("An embedded controller uses a 12-bit address bus. How many distinct memory locations can it address?",
                  ["4096", "2048", "4095", "8192"],
                  0, 8,
                  "n bits give 2ⁿ patterns; 2¹² = 4096 (0 through 4095 unsigned).",
                  ["gate", "amazon"]),
                Q("A sensor ADC outputs the binary reading 1010.11. What is its decimal value?",
                  ["10.75", "10.11", "11.75", "10.5"],
                  0, 10,
                  "1010₂ = 10 and .11₂ = 1/2 + 1/4 = 0.75, so 10.75.",
                  ["gate", "google"]),
            ]),
          L("digital-logic-boolean-algebra", "Boolean Algebra & De Morgan's Laws",
            """# Boolean Algebra & De Morgan's Laws

Boolean algebra is the math of digital circuits: variables take values
**0** or **1**, and the operators are AND (·), OR (+), NOT (′ or overbar).

## Core laws

| Law | AND form | OR form |
|---|---|---|
| Commutative | A·B = B·A | A+B = B+A |
| Associative | (A·B)·C = A·(B·C) | (A+B)+C = A+(B+C) |
| Distributive | A·(B+C) = A·B + A·C | A+(B·C) = (A+B)·(A+C) |
| Identity | A·1 = A | A+0 = A |
| Complement | A·A′ = 0 | A+A′ = 1 |
| Absorption | A·(A+B) = A | **A + A·B = A** |

## De Morgan's laws (most asked in GATE)

- **(A + B)′ = A′ · B′** — "break the bar, flip the sign"
- **(A · B)′ = A′ + B′**

## Worked simplification

Simplify `F = A·B + A·B′`:

```
F = A·B + A·B′        (given)
  = A·(B + B′)        (distributive: factor out A)
  = A·1               (complement law: B + B′ = 1)
  = A                 (identity law)
```

So `A·B + A·B′ = A`. The dual also holds: `(A+B)·(A+B′) = A`.

## Absorption in action

`X + X′·Y = X + Y`. Proof sketch: `X + X′·Y = (X + X′)·(X + Y)`
by the OR-distributive law `= 1·(X+Y) = X + Y`. This pattern appears
constantly when minimizing logic by hand.
""",
            [
                Q("A circuit designer must implement (A + B)′ using NAND-style logic. By De Morgan's law, this equals:",
                  ["A′ · B′", "A′ + B′", "A · B", "A′ + B"],
                  0, 2,
                  "De Morgan's: break the bar and flip OR to AND, giving A′·B′.",
                  ["gate", "tcs", "infosys"]),
                Q("The absorption law states that A + A·B equals:",
                  ["A", "1", "A·B", "B"],
                  0, 3,
                  "Absorption: A + A·B = A(1 + B) = A·1 = A.",
                  ["gate", "tcs"]),
                Q("While optimizing a decoder circuit you encounter the logic expression A·B + A·B′. It simplifies to:",
                  ["B", "A + B", "A", "0"],
                  2, 5,
                  "Factor: A·(B + B′) = A·1 = A.",
                  ["gate", "infosys", "wipro"]),
                Q("Apply De Morgan's law to (A·B′ + C)′.",
                  ["(A′ + B)·C′", "(A + B′)·C", "A·B + C′", "A′ + B′ + C′"],
                  0, 7,
                  "Break the bar: (A·B′)′·C′ = (A′ + B)·C′.",
                  ["gate", "microsoft"]),
                Q("An interviewer writes X + X′·Y on the board and asks you to simplify it using Boolean laws:",
                  ["X", "X′ + Y", "X·Y", "X + Y"],
                  3, 8,
                  "By the distributive law, X + X′·Y = (X + X′)(X + Y) = X + Y.",
                  ["gate", "amazon"]),
                Q("A GATE-style minimization problem: (A + B)·(A + B′)·(A′ + B) simplifies to:",
                  ["A + B", "B", "A·B", "A"],
                  2, 10,
                  "(A+B)(A+B′) = A, then A·(A′+B) = A·A′ + A·B = A·B.",
                  ["gate", "google"]),
            ]),
          L("digital-logic-kmaps", "K-Maps: Minimizing Logic",
            """# K-Maps: Minimizing Logic

A **Karnaugh map** is a truth table rearranged so that adjacent cells
differ in exactly one variable (Gray-code ordering). Circling groups of
1s lets you read off a minimized sum-of-products expression.

## Grouping rules

1. Groups must contain **1, 2, 4, 8, …** (powers of two) cells.
2. Make groups **as large as possible** — bigger group = fewer literals.
3. Every `1` must be covered; cells may be reused across groups.
4. **Wrap-around** counts as adjacency: the left edge touches the right
   edge, the top edge touches the bottom edge.
5. **Don't cares (X)** may be treated as 1 or 0, whichever gives
   bigger groups — never leave a don't care uncovered on purpose, and
   never include one you don't need.

## Worked example (4 variables)

Minimize `F(A,B,C,D) = Σm(0, 1, 2, 3, 8, 9, 10, 11)`.

Write each minterm in binary (A B C D):

```
 0: 0000    1: 0001    2: 0010    3: 0011
 8: 1000    9: 1001   10: 1010   11: 1011
```

Variable **B** (second bit) is **0 in all eight minterms**, while
A, C, D all vary — so the eight 1s form one legal group of 8, and
every variable except B drops out.

**Minimal expression: F = B′.** Verified by truth table: F = 1 exactly
when B = 0, for all 16 input combinations.

## Quick patterns to memorize

- `Σm(0,1,2,3)` (4-var) → **A′B′** (top row of the map)
- `Σm(1,3,5,7)` (3-var) → **C** (all odd minterms: C = 1)
- Four corners of a 4-var map group together (wrap-around both ways)
""",
            [
                Q("In K-map minimization, which group size is legal?",
                  ["3", "5", "8", "6"],
                  2, 2,
                  "Groups must contain a power of two cells: 1, 2, 4, 8, 16…",
                  ["gate", "tcs"]),
                Q("For a 3-variable map, F = Σm(1, 3, 5, 7) minimizes to:",
                  ["C", "B", "A", "C′"],
                  0, 4,
                  "All odd minterms have C = 1, so the function is simply C.",
                  ["gate", "infosys"]),
                Q("In a 4-variable K-map, minterms 0 (0000) and 8 (1000) are adjacent because:",
                  ["they are in the same row", "the map wraps around top-to-bottom", "they differ only in variable A", "minterms are always adjacent"],
                  2, 6,
                  "0000 and 1000 differ in exactly one variable (A), and the map's top and bottom edges wrap around.",
                  ["gate", "wipro"]),
                Q("For a 4-variable map, F = Σm(0, 1, 2, 3) minimizes to:",
                  ["A′B′", "A′", "B′", "AB"],
                  0, 7,
                  "Minterms 0000–0011 form one group of 4 where A = 0 and B = 0 throughout.",
                  ["gate", "tcs"]),
                Q("How should don't-care conditions be used in a K-map?",
                  ["include them only when they enlarge a group", "they are treated as 0 always", "they are treated as 1 always", "they must all be covered"],
                  0, 8,
                  "Don't cares are flexible: use one as a 1 only if it helps form a larger group of real 1s.",
                  ["gate", "amazon"]),
                Q("Minimize F(A,B,C,D) = Σm(0, 1, 2, 3, 8, 9, 10, 11).",
                  ["B′", "A′", "B", "A′B′"],
                  0, 10,
                  "All eight minterms have B = 0 while A, C, D vary, so they form one group of 8: F = B′.",
                  ["gate", "google", "microsoft"]),
            ]),
          L("digital-logic-combinational", "Combinational Circuits: MUX, Decoder, Encoder",
            """# Combinational Circuits: MUX, Decoder, Encoder

**Combinational** circuits have no memory: the output depends only on
the *current* inputs.

## Multiplexer (MUX): data selector

A **2ⁿ:1 MUX** routes one of 2ⁿ data inputs to the output using **n
select lines**. A 4:1 MUX has 4 data inputs (D₀–D₃) and 2 select lines:

| S₁ | S₀ | Y |
|----|----|---|
| 0 | 0 | D₀ |
| 0 | 1 | D₁ |
| 1 | 0 | D₂ |
| 1 | 1 | D₃ |

Bigger MUXes are built from smaller ones: a 16:1 MUX needs
8 + 4 + 2 + 1 = **15** two-to-one MUXes (each stage halves the inputs).

## Decoder: n inputs → 2ⁿ outputs

A decoder activates exactly one of its 2ⁿ outputs. A **3-to-8 decoder**
(3 inputs, 8 outputs Y₀–Y₇) drives Y₅ high when the input is 101.
Decoders implement any Boolean function by OR-ing the needed minterm
outputs.

## Encoder: the reverse

An **8-to-3 encoder** compresses 8 input lines into a 3-bit code.
A **priority encoder** resolves the clash when several inputs are
active at once by picking the highest-priority one.

## Adders

- **Half adder**: adds 2 bits. `Sum = A ⊕ B`, `Carry = A · B`.
- **Full adder**: adds 3 bits (A, B, Cᵢₙ).
  `Sum = A ⊕ B ⊕ Cᵢₙ`, `Cₒᵤₜ = AB + BCᵢₙ + ACᵢₙ`.
- A **ripple-carry adder** chains full adders; the carry ripples from
  LSB to MSB, which limits its speed.
""",
            [
                Q("You must select one of 4 sensor inputs using a multiplexer. How many select lines does the 4:1 MUX need?",
                  ["1", "4", "3", "2"],
                  3, 1,
                  "A 2ⁿ:1 MUX needs n select lines; 4:1 means n = 2.",
                  ["gate", "tcs", "infosys"]),
                Q("A 3-to-8 decoder has how many output lines?",
                  ["3", "6", "8", "5"],
                  2, 3,
                  "An n-to-2ⁿ decoder has 2ⁿ outputs; 2³ = 8.",
                  ["gate", "tcs"]),
                Q("In a half adder, the carry output is produced by which gate?",
                  ["XOR", "OR", "AND", "NAND"],
                  2, 5,
                  "Half-adder carry = A·B, which is a single AND gate; sum uses XOR.",
                  ["gate", "wipro"]),
                Q("A design needs a 16:1 MUX but the lab only stocks 2:1 MUX chips. How many 2:1 multiplexers are needed?",
                  ["8", "16", "15", "7"],
                  2, 6,
                  "Stage counts: 8 + 4 + 2 + 1 = 15 two-to-one MUXes.",
                  ["gate", "microsoft"]),
                Q("How many inputs does a full adder have?",
                  ["2", "4", "3", "5"],
                  2, 8,
                  "A full adder adds A, B, and carry-in — 3 inputs, 2 outputs.",
                  ["gate", "infosys"]),
                Q("A 32-register file uses one 32:1 MUX to route a register value to the ALU. How many select lines does it need?",
                  ["4", "6", "32", "5"],
                  3, 9,
                  "2ⁿ:1 needs n select lines; 2⁵ = 32, so 5 select lines.",
                  ["gate", "google", "amazon"]),
            ]),
          L("digital-logic-sequential", "Flip-Flops: SR, JK, D, T",
            """# Flip-Flops: SR, JK, D, T

**Sequential** circuits have memory: the output depends on current
inputs *and* past history, stored in **flip-flops**. Q is the present
state; Q⁺ is the next state after the clock edge.

## The four flip-flops

| Type | Characteristic equation | Behavior |
|---|---|---|
| **SR** | Q⁺ = S + R′Q | Set (S=1), Reset (R=1); S=R=1 is **forbidden** |
| **JK** | Q⁺ = JQ′ + K′Q | J=K=0 hold, J≠K set/reset, **J=K=1 toggles** |
| **D** | Q⁺ = D | Output follows D at the clock edge (delay element) |
| **T** | Q⁺ = T ⊕ Q | T=1 toggles, T=0 holds |

## Worked example: JK flip-flop

Given Q = 1, J = 0, K = 1. Apply Q⁺ = JQ′ + K′Q:

```
Q⁺ = (0)(0) + (0)(1) = 0 + 0 = 0
```

J=0, K=1 is the **reset** combination, so Q⁺ = 0 regardless of Q.

## Race-around condition (JK flip-flop)

If J = K = 1 and the clock pulse stays high longer than the flip-flop's
propagation delay, the output toggles **multiple times** during one
pulse instead of once — the final state becomes unpredictable. This is
the **race-around condition**. The fix is **edge triggering** (react
only to the clock edge) or a **master–slave** configuration.

## Why D flip-flops dominate

Registers, counters, and shift registers are built from **D
flip-flops** because Q⁺ = D is the simplest possible next-state
behavior: whatever is on D at the clock edge gets stored.
""",
            [
                Q("The characteristic equation of a D flip-flop is:",
                  ["Q⁺ = D", "Q⁺ = Q", "Q⁺ = D ⊕ Q", "Q⁺ = D′"],
                  0, 2,
                  "A D flip-flop simply copies D to Q at the clock edge: Q⁺ = D.",
                  ["gate", "tcs"]),
                Q("In a frequency-divider circuit, a JK flip-flop has J = 1 and K = 1 tied high. On each clock edge it will:",
                  ["toggle its state", "set to 1", "reset to 0", "hold its state"],
                  0, 4,
                  "J=K=1 is the toggle condition of the JK flip-flop.",
                  ["gate", "infosys"]),
                Q("A T flip-flop with T = 1 and current state Q = 0 goes to:",
                  ["invalid", "oscillates", "0", "1"],
                  3, 5,
                  "Q⁺ = T ⊕ Q = 1 ⊕ 0 = 1; with T=1 the flip-flop toggles.",
                  ["gate", "wipro"]),
                Q("The race-around condition in a JK flip-flop occurs when:",
                  ["S=R=1", "the clock frequency is too low", "the clock is edge-triggered", "J=K=1 and the clock pulse is wider than the propagation delay"],
                  3, 6,
                  "A wide clock pulse with J=K=1 lets the output toggle repeatedly within one pulse.",
                  ["gate", "microsoft"]),
                Q("During board testing, both S and R inputs of an SR flip-flop are accidentally driven high (S = 1, R = 1). This combination is:",
                  ["the hold state", "the toggle state", "forbidden / invalid", "the reset state"],
                  2, 8,
                  "S=R=1 drives both outputs of the underlying latch to 0, an invalid state.",
                  ["gate", "amazon"]),
                Q("A JK flip-flop has Q = 1, J = 0, K = 1. What is Q⁺?",
                  ["0", "1", "toggles", "holds at 1"],
                  0, 10,
                  "Q⁺ = JQ′ + K′Q = 0·0 + 0·1 = 0. J=0, K=1 resets the flip-flop.",
                  ["gate", "google"]),
            ]),
          L("digital-logic-counters", "Counters & Shift Registers",
            """# Counters & Shift Registers

Both are built by chaining flip-flops (usually D or JK).

## Counters

- **Ripple (asynchronous) counter**: each flip-flop is clocked by the
  previous one's output. Simple, but the delay **accumulates**: total
  settling time = n × t_pd, so the max clock frequency is
  **f_max = 1 / (n × t_pd)**.
- **Synchronous counter**: all flip-flops share one clock; faster and
  glitch-free, but needs extra gating logic.

A counter with **n flip-flops** has at most **2ⁿ states**. A
**MOD-n counter** cycles through exactly n states (0 … n−1) and needs
⌈log₂n⌉ flip-flops. A MOD-10 (decade) counter needs 4 flip-flops
(2³ = 8 < 10 ≤ 16 = 2⁴).

### Worked example: max frequency

A 4-bit ripple counter with t_pd = 50 ns per flip-flop: total delay =
4 × 50 ns = 200 ns, so f_max = 1 / 200 ns = **5 MHz**.

## Shift registers

Bits shift one position per clock. Named by how data enters/exits:

| Type | Serial in? | Serial out? | Use |
|---|---|---|---|
| **SISO** | yes | yes | delay line |
| **SIPO** | yes | parallel | serial-to-parallel conversion (UART RX) |
| **PISO** | parallel | yes | parallel-to-serial conversion (UART TX) |
| **PIPO** | parallel | parallel | temporary storage register |

An n-bit **SISO** register needs **n clock pulses** to shift in n bits.
A **ring counter** circulates a single 1 (n states from n flip-flops);
a **Johnson (twisted-ring) counter** feeds back the inverted output and
gives **2n states** from n flip-flops.
""",
            [
                Q("How many flip-flops does a 4-bit ripple counter contain?",
                  ["8", "2", "16", "4"],
                  3, 2,
                  "Each bit of the counter is one flip-flop: 4 bits → 4 flip-flops.",
                  ["gate", "tcs"]),
                Q("A MOD-16 counter cycles through how many distinct states?",
                  ["15", "8", "16", "10"],
                  2, 4,
                  "MOD-n means exactly n states: 0 through 15, i.e. 16 states.",
                  ["gate", "infosys"]),
                Q("What is the minimum number of flip-flops for a MOD-10 counter?",
                  ["3", "10", "5", "4"],
                  3, 5,
                  "Need 2ⁿ ≥ 10; 2³ = 8 is too few, 2⁴ = 16 works, so 4 flip-flops.",
                  ["gate", "wipro"]),
                Q("How many clock pulses are needed to serially load 4 bits into a 4-bit SISO shift register?",
                  ["1", "8", "2", "4"],
                  3, 7,
                  "One bit shifts in per clock, so 4 bits need 4 clocks.",
                  ["gate", "tcs"]),
                Q("A 4-bit ripple counter uses flip-flops with 50 ns propagation delay each. Its maximum clock frequency is:",
                  ["20 MHz", "12.5 MHz", "5 MHz", "50 MHz"],
                  2, 8,
                  "Total delay = 4×50 ns = 200 ns; f_max = 1/200ns = 5 MHz.",
                  ["gate", "amazon", "microsoft"]),
                Q("In a hardware interview you are asked: a 4-bit Johnson (twisted-ring) counter has how many distinct states?",
                  ["16", "4", "8", "10"],
                  2, 10,
                  "A Johnson counter with n flip-flops gives 2n states: 2×4 = 8.",
                  ["gate", "google"]),
            ]),
      ]),
    M("cpu-architecture", "CPU Architecture",
      "ALU, control unit, instruction cycle, addressing modes, RISC vs CISC, instruction formats.",
      [
          L("cpu-alu", "The ALU: Arithmetic & Logic Unit",
            """# The ALU: Arithmetic & Logic Unit

The **ALU** is the CPU's calculator: it performs arithmetic
(ADD, SUB, INC, DEC) and logic (AND, OR, XOR, NOT) operations on its
two inputs A and B, selected by control lines.

## Core operations

| Operation | Result | Note |
|---|---|---|
| ADD | A + B | sets carry/overflow flags |
| SUB | A − B | done as A + (2's complement of B) |
| AND | A · B | bitwise; masks bits |
| OR | A + B | bitwise; sets bits |
| XOR | A ⊕ B | bitwise; toggles bits |
| NOT | A′ | inverts every bit |

XOR-ing with all 1s flips every bit — a cheap bitwise NOT.

## Status flags

- **Z (zero)**: result was all zeros. **C (carry)**: carry out of the MSB (unsigned overflow).
- **V (overflow)**: signed overflow = carry-into-MSB ⊕ carry-out-of-MSB.
- **S/N (sign)**: MSB of the result (1 = negative in 2's complement).

## Worked example: 4-bit addition with flags

Add `A = 0111` (+7) and `B = 0001` (+1) → `1000` (8 unsigned, −8 signed):

- **Z = 0** (result ≠ 0), **C = 0** (no carry out of bit 3),
- carry into bit 3 was 1, carry out 0 → **V = 1 ⊕ 0 = 1**,
- **S = 1** (MSB is 1).

Two positive numbers produced a "negative" result: classic **signed
overflow**, exactly what V = 1 reports. Branches like "branch if
overflow" read these flags.
""",
            [
                Q("Which ALU flag is set when the result of an operation is zero?",
                  ["carry flag", "zero flag", "overflow flag", "sign flag"],
                  1, 2,
                  "The zero (Z) flag is set to 1 exactly when every result bit is 0.",
                  ["gate", "tcs", "infosys"]),
                Q("A 4-bit ALU computes 0011 + 0010. What is the carry flag?",
                  ["0", "depends on sign flag", "undefined", "1"],
                  0, 4,
                  "0011 + 0010 = 0101 (5); no carry out of the MSB, so C = 0.",
                  ["gate", "tcs"]),
                Q("A firmware routine XORs an 8-bit sensor reading with 0xFF before transmission. The result is:",
                  ["the value unchanged", "zero", "the bitwise NOT of the value", "the 2's complement"],
                  2, 5,
                  "XOR with 1 flips each bit, so XOR with all-1s inverts the whole value.",
                  ["gate", "wipro", "infosys"]),
                Q("A 4-bit ALU adds 0111 (+7) and 0001 (+1), giving 1000. Which statement is true?",
                  ["carry = 0, overflow = 1", "zero = 1, sign = 0", "carry = 1, overflow = 1", "carry = 1, overflow = 0"],
                  0, 6,
                  "No carry out (C=0), but carry into the MSB differs from carry out, so signed overflow V=1.",
                  ["gate", "microsoft"]),
                Q("A 4-bit ALU subtracts 0011 (3) from 0100 (4). What is the result and the zero flag?",
                  ["0001, zero = 0", "0001, zero = 1", "0111, zero = 0", "1111, zero = 0"],
                  0, 8,
                  "4 − 3 = 1 = 0001, which is nonzero, so Z = 0.",
                  ["gate", "amazon"]),
                Q("A 4-bit ALU adds 0101 (+5) and 0101 (+5). Which flags are set?",
                  ["Z=1, V=0", "C=1, S=0", "C=1, V=0", "C=0, V=1, S=1"],
                  3, 10,
                  "0101+0101 = 1010: no carry out (C=0), but +5++5=+10 overflows signed range (V=1) and MSB=1 (S=1).",
                  ["gate", "google"]),
            ]),
          L("cpu-control-unit", "Control Unit: Hardwired vs Microprogrammed",
            """# Control Unit: Hardwired vs Microprogrammed

The **control unit** is the CPU's conductor: it decodes each
instruction and generates the timed control signals that move data
between registers, ALU, and memory.

## The two designs

| Aspect | Hardwired | Microprogrammed |
|---|---|---|
| Built from | Combinational logic / finite-state machine (PLA) | **Control memory** holding microinstructions |
| Speed | **Faster** (no memory fetch for control) | Slower (each step reads control memory) |
| Flexibility | Hard to change — rewiring needed | **Easy to change** — rewrite the microprogram |
| Design effort | Complex, error-prone for rich ISAs | Systematic, easier to verify |
| Best for | Simple, fixed ISAs (RISC) | Complex ISAs (classic CISC) |

## Microprogramming (Wilkes, 1951)

Maurice Wilkes proposed storing control signals as **microinstructions**
in a fast **control memory**. Executing one machine instruction means
running a short **microprogram** — a sequence of micro-operations like
"MAR ← PC" or "ALU ← ADD". Changing the CPU's behavior becomes a
firmware update instead of a hardware redesign.

## Worked scenario

A vendor must add a new string-search instruction to a shipped CPU:

- **Microprogrammed**: engineers write a new micro-routine into control
  memory (or a patch RAM) — no silicon change.
- **Hardwired**: the control PLA must be redesigned and the chip
  re-fabricated — vastly more expensive.

This is why complex, evolving ISAs historically chose
microprogramming, while clean-sheet RISC designs — with few, simple,
fixed-length instructions — could afford fast hardwired control.
""",
            [
                Q("Which type of control unit is generally faster?",
                  ["both are equal", "depends on the ALU", "microprogrammed", "hardwired"],
                  3, 1,
                  "Hardwired control generates signals directly from logic with no control-memory fetch, so it is faster.",
                  ["gate", "tcs"]),
                Q("The concept of microprogramming was introduced by:",
                  ["Alan Turing", "Gordon Moore", "John von Neumann", "Maurice Wilkes"],
                  3, 3,
                  "Maurice Wilkes proposed microprogramming in 1951.",
                  ["gate", "infosys"]),
                Q("In a microprogrammed control unit, control signals are stored as:",
                  ["flip-flop states", "microinstructions in control memory", "cache lines", "register values"],
                  1, 5,
                  "Control memory holds microinstructions; each machine instruction runs a microprogram of micro-operations.",
                  ["gate", "wipro"]),
                Q("Which control unit is easier to modify when the instruction set changes?",
                  ["both equally", "neither can be modified", "hardwired", "microprogrammed"],
                  3, 6,
                  "Microprogrammed control is firmware-like: rewrite the microprogram instead of rewiring hardware.",
                  ["gate", "tcs"]),
                Q("A hardwired control unit is typically implemented using:",
                  ["control memory and a sequencer", "combinational logic / PLA as a finite-state machine", "a stack and micro-operations", "associative memory"],
                  1, 8,
                  "Hardwired control is pure logic — a finite-state machine built from gates or a PLA.",
                  ["gate", "amazon"]),
                Q("In a processor-design interview you are asked: why do classic RISC processors favor hardwired control?",
                  ["RISC needs microcode for pipelining", "simple fixed-length instructions make hardwired control feasible and fast", "hardwired control uses less power always", "RISC instructions are too complex for microcode"],
                  1, 9,
                  "RISC ISAs are small and regular, so the control logic stays manageable and runs at full speed.",
                  ["gate", "google", "microsoft"]),
            ]),
          L("cpu-instruction-cycle", "Fetch–Decode–Execute",
            """# Fetch–Decode–Execute: The Instruction Cycle

Every instruction a CPU runs passes through the same cycle:

**Fetch → Decode → Execute** (plus memory-access and write-back
stages in modern pipelines).

## The phases with register transfers

Assume PC = 300 and memory holds the program.

### 1. Fetch — get the instruction into the CPU

`MAR ← PC`, `MDR ← M[MAR]`, `IR ← MDR`, `PC ← PC + 1` (now 301).

### 2. Decode — figure out what it says

The control unit interprets the **IR**: opcode (what to do) and
operand fields (what to do it to). No data moves yet.

### 3. Execute — do it

For `LOAD R1, [400]` (direct): `MAR ← 400`, `MDR ← M[MAR]`, `R1 ← MDR`.

## Worked trace: two instructions

Memory: `M[300] = LOAD R1, [400]`, `M[301] = ADD R1, R2`,
`M[400] = 25`, and R2 already holds 5.

- **Instruction 1** (PC=300): fetch as above → IR = LOAD R1,[400] →
  execute: MAR←400, MDR←M[400]=25, **R1←25**. PC is now 301.
- **Instruction 2** (PC=301): fetch → IR = ADD R1,R2 → decode →
  execute: **R1 ← R1 + R2 = 25 + 5 = 30**. PC is now 302.

Note PC increments during *fetch*, so by execute time it already
points past the current instruction — this is why branch offsets are
computed relative to the *next* instruction's address.
""",
            [
                Q("What is the first register transfer of the fetch phase?",
                  ["MAR ← PC", "IR ← MDR", "PC ← PC + 1", "MDR ← M[MAR]"],
                  0, 2,
                  "The address must go out first: MAR ← PC, then the memory read happens.",
                  ["gate", "tcs", "infosys"]),
                Q("After the fetch phase completes, the program counter points to:",
                  ["the operand address", "zero", "the current instruction", "the next instruction"],
                  3, 4,
                  "PC ← PC + 1 happens during fetch, so PC already aims at the following instruction.",
                  ["gate", "tcs"]),
                Q("During the decode phase, the control unit interprets the contents of:",
                  ["the program counter", "the MAR", "the MDR", "the IR"],
                  3, 5,
                  "The Instruction Register holds the fetched instruction that decode must interpret.",
                  ["gate", "wipro"]),
                Q("Which register holds the memory address currently being accessed?",
                  ["MDR", "IR", "MAR", "accumulator"],
                  2, 7,
                  "MAR (Memory Address Register) drives the address bus; MDR carries the data.",
                  ["gate", "infosys"]),
                Q("A LOAD instruction with direct addressing needs how many memory reads in total?",
                  ["1", "3", "2", "4"],
                  2, 8,
                  "One read fetches the instruction itself, a second read fetches the operand — 2 total.",
                  ["gate", "amazon"]),
                Q("PC = 300, M[300] = LOAD R2, [450], M[450] = 77. After this instruction executes, R2 holds:",
                  ["450", "300", "77", "301"],
                  2, 10,
                  "Fetch loads the instruction, then the CPU reads M[450] = 77 into R2.",
                  ["gate", "google", "microsoft"]),
            ]),
          L("cpu-addressing-modes", "Addressing Modes",
            """# Addressing Modes

An **addressing mode** is the rule an instruction uses to find its
operand. The **effective address (EA)** is the final memory address
(or value) the rule produces.

## The modes (operand field = 100, R holds 50, M[100] = 250)

| Mode | Example | Effective address / operand |
|---|---|---|
| **Immediate** | `ADD #100` | operand **is** 100 (no memory access) |
| **Direct** (absolute) | `LOAD R1, [100]` | EA = **100** |
| **Indirect** | `LOAD R1, @100` | EA = M[100] = **250** (extra memory read) |
| **Register** | `ADD R1, R2` | operands are registers (fastest) |
| **Register indirect** | `LOAD R1, (R2)` | EA = contents of R2 |
| **Indexed** | `LOAD R1, 100(R3)` | EA = 100 + R3 = 100 + 50 = **150** |
| **PC-relative** | `JUMP +100` (PC=500) | EA = PC + offset = 500 + 100 = **600** |

## Worked examples

**Indexed (arrays):** base 100, index R3 = 50 →
`EA = 100 + 50 = 150`, operand = M[150]. Keep the base fixed, walk the index.

**PC-relative (branches):** PC = 500, offset +100 →
`EA = 500 + 100 = 600`. Code stays **position-independent**: targets move with the program.

## Trade-offs

- Immediate: fastest, but the constant's size is limited by the
  instruction format.
- Indirect: flexible (pointers!), but costs an extra memory access.
- Register: fastest of all — no memory access — but registers are few.
""",
            [
                Q("In immediate addressing mode, the operand is located:",
                  ["inside the instruction itself", "in a register", "in the stack", "in memory at the given address"],
                  0, 2,
                  "Immediate mode embeds the constant value directly in the instruction — no memory access.",
                  ["gate", "tcs"]),
                Q("An instruction has operand field 100 and uses direct addressing. The effective address is:",
                  ["PC + 100", "contents of R100", "M[100]", "100"],
                  3, 3,
                  "Direct addressing uses the operand field itself as the address: EA = 100.",
                  ["gate", "infosys"]),
                Q("With indirect addressing, operand field = 100 and M[100] = 250. The effective address is:",
                  ["350", "M[250]", "100", "250"],
                  3, 5,
                  "Indirect adds one memory hop: EA = M[100] = 250.",
                  ["gate", "wipro", "tcs"]),
                Q("Indexed addressing with base 100 and index register holding 50 gives effective address:",
                  ["50", "100", "150", "5000"],
                  2, 6,
                  "EA = base + index = 100 + 50 = 150.",
                  ["gate", "amazon"]),
                Q("In register-indirect addressing, the effective address is:",
                  ["the next instruction's address", "always zero", "the register number", "the contents of the specified register"],
                  3, 8,
                  "The register holds a pointer: EA = contents of that register.",
                  ["gate", "microsoft"]),
                Q("A branch uses PC-relative addressing with PC = 500 and offset +100. The target address is:",
                  ["400", "100", "600", "500"],
                  2, 10,
                  "EA = PC + offset = 500 + 100 = 600.",
                  ["gate", "google"]),
            ]),
          L("cpu-risc-cisc", "RISC vs CISC",
            """# RISC vs CISC

Two philosophies for designing an instruction set.

## Head-to-head

| Aspect | RISC | CISC |
|---|---|---|
| Instruction length | **Fixed** (e.g. 32-bit) | **Variable** (1–15 bytes on x86) |
| Philosophy | Few simple instructions, each ~1 cycle | Many complex instructions, one does a lot |
| Memory access | **Load–store**: only LOAD/STORE touch memory | Most instructions can access memory |
| Addressing modes | Few (2–4) | Many (10+) |
| Registers | **Large** general-purpose file | Fewer, some specialized |
| Control unit | **Hardwired** (simple enough) | Microprogrammed (historically) |
| Examples | **ARM, RISC-V**, MIPS, PowerPC | **x86 / x86-64** (Intel, AMD) |
| Pipelining | Easy — uniform stages | Hard — instructions differ wildly |

## Why RISC pipelines so well

A pipeline overlaps fetch/decode/execute of several instructions.
That works best when every instruction looks alike: fixed length
(fetch is trivial), simple format (decode is one step), and
load–store discipline (memory stage timing is predictable). CISC's
variable lengths and memory operands make each stage's duration
unpredictable, complicating the pipeline.

## The honest footnote

Modern x86 **decodes** CISC instructions into RISC-like **micro-ops**
internally — "RISC vs CISC" today describes the programmer-visible ISA, not the silicon.

## GATE favorite facts

- RISC targets **CPI ≈ 1** (cycles per instruction near one).
- CISC optimizes for **code density** (fewer bytes per program) —
  valuable when memory was expensive.
- Load–store means arithmetic instructions take **register operands
  only**.
""",
            [
                Q("A startup is choosing an ISA for a low-power IoT chip. Which of these is a RISC instruction set architecture?",
                  ["ARM", "VAX", "PDP-11", "x86"],
                  0, 1,
                  "ARM is the classic RISC ISA; x86 is the canonical CISC example.",
                  ["gate", "tcs", "infosys"]),
                Q("x86 is an example of which ISA philosophy?",
                  ["RISC", "CISC", "VLIW", "EPIC"],
                  1, 3,
                  "x86 has variable-length, complex, memory-operand instructions — textbook CISC.",
                  ["gate", "tcs"]),
                Q("The load–store architecture, where only LOAD/STORE access memory, belongs to:",
                  ["stack machines", "microprogrammed CPUs", "CISC", "RISC"],
                  3, 5,
                  "Load–store discipline is a defining RISC trait; ALU ops use registers only.",
                  ["gate", "wipro"]),
                Q("Why is RISC considered more pipeline-friendly than CISC?",
                  ["it has more addressing modes", "fixed-length simple instructions make each pipeline stage predictable", "it uses microprogrammed control", "its clock speed is always higher"],
                  1, 6,
                  "Uniform instruction length and format let fetch/decode/execute overlap cleanly.",
                  ["gate", "amazon", "microsoft"]),
                Q("Which ISA style typically provides more addressing modes?",
                  ["both provide the same", "neither uses addressing modes", "RISC", "CISC"],
                  3, 8,
                  "CISC exposes many addressing modes (10+ on classic designs); RISC keeps just a few.",
                  ["gate", "infosys"]),
                Q("Which statement about RISC is TRUE?",
                  ["every RISC instruction executes in exactly one clock cycle", "RISC aims for CPI near 1 with simple fixed-length instructions", "RISC programs are always shorter than CISC programs", "RISC forbids pipelining"],
                  1, 9,
                  "RISC targets CPI ≈ 1 on average — not a guarantee per instruction — via simple uniform instructions.",
                  ["gate", "google"]),
            ]),
          L("cpu-instruction-formats", "Instruction Formats: 0/1/2/3-Address",
            """# Instruction Formats: 0/1/2/3-Address Machines

An instruction format decides **where operands live** and how many
address fields each instruction carries.

## The four classic formats

| Addresses | Operands live in | Example: compute A + B | Needs |
|---|---|---|---|
| **3-address** | registers/memory | `ADD R1, R2, R3` → R1 = R2 + R3 | long instructions |
| **2-address** | registers/memory | `ADD R1, R2` → R1 = R1 + R2 (destructive) | moderate length |
| **1-address** | **accumulator** + memory | `LOAD A` / `ADD B` → AC = AC + M[B] | short, but many instructions |
| **0-address** | **stack** | `PUSH A; PUSH B; ADD` → push(A+B) | no address fields at all |

## Worked example: 0-address (stack machine)

`PUSH 5` → [5]; `PUSH 3` → [5, 3]; `ADD` → pop 3, pop 5, push 8 → [8].
Top of stack is **8** — operands are implied, no address fields needed.

## Worked example: 3-address vs 2-address

- 3-address: `ADD R1, R2, R3` means **R1 ← R2 + R3** (R2, R3 preserved).
- 2-address: `ADD R1, R2` means **R1 ← R1 + R2** (R1 is overwritten —
  one source is destroyed).

## Opcode math (GATE loves this)

An **n-bit opcode** field can encode **2ⁿ distinct operations**.
A 6-bit opcode → 2⁶ = **64** operations.

Instruction-length budgeting: a 32-bit instruction with an 8-bit
opcode and two 12-bit address fields uses 8 + 12 + 12 = **32 bits** —
it fits exactly, with no room left over.
""",
            [
                Q("Zero-address instructions are designed for which machine organization?",
                  ["accumulator", "register file", "stack", "cache"],
                  2, 2,
                  "With no address fields, operands are implied — the top of the stack.",
                  ["gate", "tcs"]),
                Q("One-address instructions typically use which implied operand holder?",
                  ["the stack", "the accumulator", "the program counter", "the flag register"],
                  1, 4,
                  "1-address machines keep one operand in the accumulator: ADD X means AC = AC + M[X].",
                  ["gate", "infosys"]),
                Q("A 6-bit opcode field can encode how many distinct operations?",
                  ["12", "36", "32", "64"],
                  3, 5,
                  "n opcode bits → 2ⁿ operations; 2⁶ = 64.",
                  ["gate", "wipro", "tcs"]),
                Q("The 2-address instruction ADD R1, R2 performs:",
                  ["R2 ← R1 + R2", "R1 ← R1 + R2", "R1 ← R2 + R3", "push(R1 + R2)"],
                  1, 7,
                  "In 2-address format one register is both source and destination: R1 = R1 + R2.",
                  ["gate", "amazon"]),
                Q("A 32-bit instruction has an 8-bit opcode and two 12-bit address fields. Which is true?",
                  ["it overflows by 8 bits", "it fits exactly with 0 bits wasted", "it wastes 4 bits", "it needs 40 bits"],
                  1, 8,
                  "8 + 12 + 12 = 32 — the fields fill the instruction word exactly.",
                  ["gate", "microsoft"]),
                Q("Tracing a stack-machine program: PUSH 5, PUSH 3, ADD. After execution, what is on the top of the stack?",
                  ["5", "3", "8", "15"],
                  2, 10,
                  "ADD pops 3 and 5, pushes their sum: 5 + 3 = 8.",
                  ["gate", "google"]),
            ]),
          L("cpu-interrupts", "Interrupts & Exceptions",
            """# Interrupts & Exceptions

An **interrupt** is a signal that pauses the current program so the
CPU can handle an urgent event, then resumes where it left off.

## Handling sequence

1. CPU finishes the current instruction; hardware **saves the PC** and flags.
2. CPU jumps to the **ISR** via the **interrupt vector table** (entry *n* = address of handler *n*).
3. ISR runs, executes return-from-interrupt; the saved PC is restored and the program resumes.

## Maskable vs non-maskable

| Type | Can the CPU ignore it? | Examples |
|---|---|---|
| **Maskable** | Yes — the interrupt-enable flag can block it | keyboard, timer, I/O completion |
| **Non-maskable (NMI)** | **No** — always serviced | power failure, memory parity error |

NMIs exist for events so critical that ignoring them risks hardware
damage or data loss.

## Worked example: vector-table sizing

256 vectors × 4-byte entries: `256 × 4 = 1024 bytes = 1 KB`.

## Polling vs interrupt-driven I/O

- **Polling**: the CPU repeatedly asks each device "are you ready?"
  Simple, but burns CPU cycles checking idle devices.
- **Interrupt-driven**: the device signals the CPU only when it needs
  attention. Efficient, but needs vector tables, ISRs, and context
  saving.

Interrupts also implement **exceptions** (synchronous, from the
program itself): divide-by-zero, illegal opcode, page fault. The
mechanism is identical — only the trigger differs (internal vs
external).
""",
            [
                Q("ISR stands for:",
                  ["Interrupt Service Routine", "Internal System Reset", "Indexed Segment Register", "Instruction Service Register"],
                  0, 2,
                  "The ISR is the handler routine the CPU jumps to when an interrupt fires.",
                  ["gate", "tcs", "infosys"]),
                Q("A power-failure detector must interrupt the CPU no matter what the CPU is doing. Which of these is a non-maskable interrupt?",
                  ["keyboard press", "power failure", "timer tick", "disk I/O completion"],
                  1, 3,
                  "Power failure is an NMI — the CPU must service it; it cannot be masked off.",
                  ["gate", "wipro"]),
                Q("The interrupt vector table holds:",
                  ["pending interrupt flags", "device status words", "the saved program counters", "addresses of interrupt service routines"],
                  3, 5,
                  "Entry n of the vector table is the start address of the handler for interrupt n.",
                  ["gate", "tcs"]),
                Q("A CPU has 256 interrupt vectors with 4-byte entries. The vector table size is:",
                  ["256 bytes", "1024 bytes", "4096 bytes", "64 bytes"],
                  1, 6,
                  "256 × 4 = 1024 bytes = 1 KB.",
                  ["gate", "amazon", "microsoft"]),
                Q("Compared with interrupt-driven I/O, polling mainly wastes:",
                  ["memory bandwidth", "CPU cycles checking idle devices", "disk space", "register file entries"],
                  1, 8,
                  "Polling loops asking 'ready yet?' burn CPU time even when nothing needs doing.",
                  ["gate", "infosys"]),
                Q("After an ISR finishes, how does the CPU resume the interrupted program?",
                  ["it restarts the program from the beginning", "it restores the saved PC and continues", "it jumps to the next interrupt vector", "it halts until reset"],
                  1, 9,
                  "The hardware-saved PC is restored by the return-from-interrupt, resuming exactly where it paused.",
                  ["gate", "google"]),
            ]),
      ]),
]
