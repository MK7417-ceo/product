"""Domain: deterministic template-based question generator. PURE — no DB, no I/O, no network.

Why templates instead of an LLM:
- Answers are COMPUTED (real simulations), never hallucinated.
- Deterministic: same (domain, seed) -> byte-identical questions (seeded RNG).
- Scales: parameter spaces yield 500+ unique questions per domain.

Conventions:
- Every generator has signature: gen(rng: random.Random, difficulty: int) -> dict
- Question dict: {
    "prompt": str, "choices": [str x4], "answer_index": int,
    "explanation": str, "difficulty": int (1-10), "qtype": "mcq",
    "company_tags": [str], "generator": "dsa/time-complexity",
  }
- generate_questions(domain_slug, seed, count, difficulty_range) distributes
  `count` across the domain's generators deterministically and dedupes prompts.
- questions_generatable(domain_slug) -> conservative unique-question capacity.
"""
from __future__ import annotations

import math
import random
from itertools import combinations

from app.domain.user import DomainError

SUPPORTED_DOMAINS = ("dsa", "os", "dbms")

_COMPANY_POOL = [
    "tcs", "infosys", "wipro", "accenture", "amazon", "google", "microsoft",
]


def _tags(rng: random.Random, n: int = 2) -> list[str]:
    """Deterministic company tags."""
    pool = list(_COMPANY_POOL)
    rng.shuffle(pool)
    return sorted(pool[:n])


def _mcq(rng: random.Random, prompt: str, correct: str,
         distractors: list[str], explanation: str, difficulty: int,
         generator: str, num_tags: int = 2) -> dict:
    """Build a validated MCQ dict; shuffles choices deterministically."""
    seen = []
    for c in [correct] + distractors:
        s = str(c)
        if s not in seen:
            seen.append(s)
    if len(seen) < 4:
        raise DomainError(f"generator {generator}: need 4 distinct choices")
    rng.shuffle(seen)
    return {
        "prompt": prompt,
        "choices": seen[:4],
        "answer_index": seen.index(str(correct)),
        "explanation": explanation,
        "difficulty": int(difficulty),
        "qtype": "mcq",
        "company_tags": _tags(rng, num_tags),
        "generator": generator,
    }


def _num_distractors(correct: int, deltas=(1, 2, 3)) -> list[str]:
    """Numeric distractors around the correct integer answer."""
    out = []
    for d in deltas:
        for cand in (correct + d, correct - d):
            s = str(cand)
            if s != str(correct) and s not in out:
                out.append(s)
            if len(out) == 3:
                return out
    return out


# =====================================================================
# DSA generators
# =====================================================================

_DSA_COMPLEXITIES = [
    ("Bubble Sort", "O(n²)"),
    ("Selection Sort", "O(n²)"),
    ("Insertion Sort", "O(n²)"),
    ("Merge Sort", "O(n log n)"),
    ("Quick Sort (average case)", "O(n log n)"),
    ("Heap Sort", "O(n log n)"),
    ("Binary Search", "O(log n)"),
    ("Linear Search", "O(n)"),
    ("Hash table lookup (average)", "O(1)"),
    ("DFS/BFS traversal of a graph", "O(V + E)"),
    ("Two nested loops over n elements", "O(n²)"),
    ("A single loop over n elements", "O(n)"),
]
_COMPLEXITY_CHOICES = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)", "O(n!)"]
# growth rank for comparisons (higher = grows faster)
_COMPLEXITY_RANK = {"O(1)": 0, "O(log n)": 1, "O(n)": 2, "O(n log n)": 3,
                   "O(n²)": 4, "O(V + E)": 4, "O(2ⁿ)": 5, "O(n!)": 6}


def gen_time_complexity(rng: random.Random, difficulty: int) -> dict:
    """Identify Big-O of an algorithm, or compare two complexities."""
    if difficulty <= 4 or rng.random() < 0.6:
        name, cx = rng.choice(_DSA_COMPLEXITIES)
        others = [c for c in _COMPLEXITY_CHOICES if c != cx][:6]
        distract = rng.sample(others, 3)
        return _mcq(
            rng,
            f"What is the time complexity of {name}?",
            cx, distract,
            f"{name} runs in {cx} time in the standard analysis "
            f"(count how the work scales as input size n grows).",
            max(1, min(4, difficulty)), "dsa/time-complexity",
        )
    c1, c2 = rng.sample([c for c in _COMPLEXITY_CHOICES if c != "O(V + E)"], 2)
    faster = c1 if _COMPLEXITY_RANK[c1] < _COMPLEXITY_RANK[c2] else c2
    return _mcq(
        rng,
        f"For very large n, which grows slower (is faster): {c1} or {c2}?",
        faster, [c1 if faster == c2 else c2, "Both grow at the same rate",
                 "Cannot be determined"],
        f"Growth order: O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!). "
        f"So {faster} grows slower than {c1 if faster == c2 else c2}.",
        max(5, min(8, difficulty)), "dsa/time-complexity",
    )


def _bubble_pass(arr: list[int]) -> list[int]:
    a = list(arr)
    for i in range(len(a) - 1):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
    return a


def _selection_pass(arr: list[int]) -> list[int]:
    a = list(arr)
    m = min(range(len(a)), key=lambda i: a[i])
    a[0], a[m] = a[m], a[0]
    return a


def _fmt_arr(arr: list[int]) -> str:
    return "[" + ", ".join(str(x) for x in arr) + "]"


def _arr_variants(rng: random.Random, correct: list[int], original: list[int]) -> list[str]:
    """Plausible wrong arrays: original, sorted, one-swap mutations."""
    cands = [_fmt_arr(original), _fmt_arr(sorted(original))]
    a = list(correct)
    if len(a) >= 2:
        b = list(a)
        b[0], b[-1] = b[-1], b[0]
        cands.append(_fmt_arr(b))
        c = list(a)
        i = rng.randrange(len(c) - 1)
        c[i], c[i + 1] = c[i + 1], c[i]
        cands.append(_fmt_arr(c))
    out = []
    for s in cands:
        if s != _fmt_arr(correct) and s not in out:
            out.append(s)
    return out[:3]


def gen_array_trace(rng: random.Random, difficulty: int) -> dict:
    """Trace a small array operation; answer computed by simulation."""
    n = 4 if difficulty <= 3 else (5 if difficulty <= 6 else 6)
    arr = rng.sample(range(1, 30), n)
    op = rng.choice(["reverse", "bubble-pass", "rotate-left", "max"])
    if op == "reverse":
        result = arr[::-1]
        prompt = f"What is the result of reversing the array {_fmt_arr(arr)}?"
        expl = f"Reversing reads the array back-to-front: {_fmt_arr(result)}."
    elif op == "bubble-pass":
        result = _bubble_pass(arr)
        prompt = (f"After ONE complete pass of bubble sort (ascending) on "
                  f"{_fmt_arr(arr)}, what is the array?")
        expl = (f"One bubble-sort pass compares adjacent pairs and swaps when "
                f"out of order, so the largest element bubbles to the end: "
                f"{_fmt_arr(result)}.")
    elif op == "rotate-left":
        k = rng.randint(1, n - 1)
        result = arr[k:] + arr[:k]
        prompt = (f"After rotating the array {_fmt_arr(arr)} left by {k} "
                  f"position(s), what is the array?")
        expl = (f"Left rotation by {k} moves the first {k} element(s) to the "
                f"end: {_fmt_arr(result)}.")
    else:
        result = [max(arr)]
        prompt = f"What is the maximum element of the array {_fmt_arr(arr)}?"
        expl = f"Scanning all elements, the largest is {result[0]}."
    correct = _fmt_arr(result)
    distract = _arr_variants(rng, result, arr)
    return _mcq(rng, prompt, correct, distract, expl,
                difficulty, "dsa/array-trace")


def _big_o_value(cx: str, n: int) -> float:
    if cx == "O(1)":
        return 1.0
    if cx == "O(log n)":
        return math.log2(n)
    if cx == "O(n)":
        return float(n)
    if cx == "O(n log n)":
        return n * math.log2(n)
    if cx == "O(n²)":
        return float(n * n)
    if cx == "O(2ⁿ)":
        return float(2 ** n)
    if cx == "O(n!)":
        return float(math.factorial(n))
    raise DomainError(f"unknown complexity {cx}")


def gen_big_o_compare(rng: random.Random, difficulty: int) -> dict:
    """Which of two complexities is larger at a given n — computed exactly."""
    pool = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)", "O(n!)"]
    c1, c2 = rng.sample(pool, 2)
    if "O(n!)" in (c1, c2):
        n = 10
    elif "O(2ⁿ)" in (c1, c2):
        n = 20
    else:
        n = rng.choice([100, 1000])
    v1, v2 = _big_o_value(c1, n), _big_o_value(c2, n)
    if abs(v1 - v2) < 1e-9:
        return gen_big_o_compare(rng, difficulty)  # re-roll ties
    bigger = c1 if v1 > v2 else c2
    def _fmt(v: float) -> str:
        if v >= 1e12:
            return f"{v:.1e}"
        if v == int(v):
            return str(int(v))
        return f"{v:.1f}"
    return _mcq(
        rng,
        f"For n = {n}, which is larger: {c1} or {c2}?",
        bigger,
        [c1 if bigger == c2 else c2, "Both are equal",
         "Cannot be determined without the constant factors"],
        f"At n = {n}: {c1} ≈ {_fmt(v1)}, {c2} ≈ {_fmt(v2)}. "
        f"So {bigger} is larger.",
        difficulty, "dsa/big-o-compare",
    )


def gen_ds_operation(rng: random.Random, difficulty: int) -> dict:
    """Simulate stack/queue operations; answers computed by simulation."""
    is_stack = rng.random() < 0.5
    ops: list[tuple[str, int | None]] = []
    size = 0
    length = rng.randint(4, 7)
    for _ in range(length):
        if size == 0 or (size < 4 and rng.random() < 0.65):
            v = rng.randint(1, 9)
            ops.append(("push" if is_stack else "enqueue", v))
            size += 1
        else:
            ops.append(("pop" if is_stack else "dequeue", None))
            size -= 1
    # simulate
    store: list[int] = []
    removed: list[int] = []
    for op, v in ops:
        if op in ("push", "enqueue"):
            store.append(v)  # type: ignore[arg-type]
        else:
            if is_stack:
                removed.append(store.pop())
            else:
                removed.append(store.pop(0))
    name = "stack" if is_stack else "queue"
    op_str = ", ".join(f"{o}({v})" if v is not None else f"{o}()" for o, v in ops)
    ask = rng.choice(["top", "removed", "size"])
    if ask == "top" or (ask == "removed" and not removed):
        end = "top" if is_stack else "front"
        correct = str(store[0] if store else "empty")
        prompt = (f"After these {name} operations: {op_str} — "
                  f"what is the {end} element?")
        expl = (f"Simulating in order, the {name} ends as {store}, "
                f"so the {end} is {correct}.")
    elif ask == "removed":
        which = "last removed" if is_stack else "first removed"
        correct = str(removed[-1] if is_stack else removed[0])
        prompt = (f"After these {name} operations: {op_str} — "
                  f"what was the {which} element?")
        expl = (f"{'Stack pops from the top (LIFO)' if is_stack else 'Queue dequeues from the front (FIFO)'}, "
                f"so the {which} element is {correct}.")
    else:
        correct = str(len(store))
        prompt = (f"After these {name} operations: {op_str} — "
                  f"how many elements remain?")
        expl = f"Simulating leaves {store}, which has {correct} element(s)."
    distract = _num_distractors(int(correct)) if correct.lstrip("-").isdigit() else ["empty", "0", "1"]
    return _mcq(rng, prompt, correct, distract, expl, difficulty,
                "dsa/ds-operation")


def gen_tree_height(rng: random.Random, difficulty: int) -> dict:
    """Complete-binary-tree height / level capacity — computed exactly."""
    form = rng.choice(["height", "min-height", "level-cap", "max-nodes"])
    if form in ("height", "min-height"):
        n = rng.randint(1, 500)
        ans = int(math.floor(math.log2(n)))
        if form == "height":
            prompt = (f"A complete binary tree has {n} nodes. What is its height "
                      f"(number of edges on the longest root-to-leaf path)?")
            expl = (f"For a complete binary tree, height = floor(log2(n)) = "
                    f"floor(log2({n})) = {ans}.")
        else:
            prompt = (f"What is the minimum possible height (in edges) of a "
                      f"binary tree with {n} nodes?")
            expl = (f"The most balanced (complete) tree gives minimum height = "
                    f"floor(log2({n})) = {ans}.")
        return _mcq(rng, prompt, str(ans), _num_distractors(ans), expl,
                    difficulty, "dsa/tree-height")
    if form == "level-cap":
        lvl = rng.randint(0, 6)
        ans = 2 ** lvl
        return _mcq(
            rng,
            f"In a binary tree, at most how many nodes can be at level {lvl} "
            f"(root is level 0)?",
            str(ans), _num_distractors(ans),
            f"Level l of a binary tree holds at most 2^l nodes: 2^{lvl} = {ans}.",
            difficulty, "dsa/tree-height",
        )
    h = rng.randint(1, 5)
    ans = 2 ** (h + 1) - 1
    return _mcq(
        rng,
        f"A binary tree of height {h} (in edges) has at most how many nodes?",
        str(ans), _num_distractors(ans),
        f"A perfect tree of height h has 2^(h+1) − 1 nodes: "
        f"2^{h + 1} − 1 = {ans}.",
        difficulty, "dsa/tree-height",
    )


def gen_sorting_steps(rng: random.Random, difficulty: int) -> dict:
    """Array after k passes of bubble/selection sort — computed by simulation."""
    n = 5 if difficulty <= 5 else 6
    arr = rng.sample(range(1, 40), n)
    algo = rng.choice(["bubble", "selection"])
    passes = 1 if difficulty <= 6 else 2
    a = list(arr)
    for _ in range(passes):
        a = _bubble_pass(a) if algo == "bubble" else _selection_pass(a)
    label = "bubble sort" if algo == "bubble" else "selection sort"
    noun = "pass" if passes == 1 else "passes"
    prompt = (f"After {passes} {noun} of {label} (ascending) on {_fmt_arr(arr)}, "
              f"what is the array?")
    if algo == "bubble":
        expl = (f"Each bubble-sort pass bubbles the largest remaining element "
                f"to its final position: {_fmt_arr(a)}.")
    else:
        expl = (f"Each selection-sort pass puts the smallest remaining element "
                f"at the front: {_fmt_arr(a)}.")
    return _mcq(rng, prompt, _fmt_arr(a), _arr_variants(rng, a, arr), expl,
                difficulty, "dsa/sorting-steps")


# =====================================================================
# OS generators
# =====================================================================

def _fcfs_total_waiting(procs: list[tuple[str, int, int]]) -> int:
    """procs: (pid, arrival, burst). Returns total waiting time (FCFS)."""
    order = sorted(procs, key=lambda p: (p[1], p[0]))
    t = 0
    total = 0
    for pid, arr, burst in order:
        start = max(t, arr)
        total += start - arr
        t = start + burst
    return total


def _sjf_total_waiting(procs: list[tuple[str, int, int]]) -> int:
    """Non-preemptive SJF. Returns total waiting time."""
    remaining = {pid: (arr, burst) for pid, arr, burst in procs}
    t = 0
    total = 0
    done = set()
    while len(done) < len(procs):
        avail = [(pid, arr, b) for pid, (arr, b) in remaining.items()
                 if pid not in done and arr <= t]
        if not avail:
            t = min(arr for pid, (arr, b) in remaining.items() if pid not in done)
            continue
        pid, arr, burst = min(avail, key=lambda p: (p[2], p[1], p[0]))
        total += t - arr
        t += burst
        done.add(pid)
    return total


def _rr_total_waiting(procs: list[tuple[str, int, int]], quantum: int) -> int:
    """Round Robin. Returns total waiting time."""
    arr_of = {pid: arr for pid, arr, _ in procs}
    burst_of = {pid: b for pid, _, b in procs}
    remaining = dict(burst_of)
    order = sorted(procs, key=lambda p: (p[1], p[0]))
    idx, t, queue, in_q, completion = 0, 0, [], set(), {}
    n = len(procs)
    while len(completion) < n:
        while idx < n and order[idx][1] <= t:
            pid = order[idx][0]
            if pid not in in_q:
                queue.append(pid)
                in_q.add(pid)
            idx += 1
        if not queue:
            t = order[idx][1]
            continue
        pid = queue.pop(0)
        run = min(quantum, remaining[pid])
        t += run
        remaining[pid] -= run
        while idx < n and order[idx][1] <= t:
            p2 = order[idx][0]
            if p2 not in in_q:
                queue.append(p2)
                in_q.add(p2)
            idx += 1
        if remaining[pid] == 0:
            completion[pid] = t
        else:
            queue.append(pid)
    return sum(completion[pid] - arr_of[pid] - burst_of[pid] for pid in completion)


def gen_scheduling(rng: random.Random, difficulty: int) -> dict:
    """CPU scheduling: total waiting time COMPUTED by simulation."""
    n = 3 if difficulty <= 5 else 4
    pids = [f"P{i + 1}" for i in range(n)]
    procs = []
    for pid in pids:
        arr = rng.randint(0, 3)
        burst = rng.randint(2, 8)
        procs.append((pid, arr, burst))
    if difficulty <= 4:
        algo, total, extra = "FCFS", _fcfs_total_waiting(procs), ""
        expl_algo = "FCFS runs processes in arrival order"
    elif difficulty <= 7:
        algo, total, extra = "SJF (non-preemptive)", _sjf_total_waiting(procs), ""
        expl_algo = ("SJF always picks the arrived process with the shortest "
                     "burst next")
    else:
        q = rng.choice([2, 3])
        algo, total = "Round Robin", _rr_total_waiting(procs, q)
        extra = f" with time quantum = {q}"
        expl_algo = (f"Round Robin cycles through ready processes giving each "
                     f"{q} units")
    desc = ", ".join(f"{pid}(arrival={a}, burst={b})" for pid, a, b in procs)
    prompt = (f"Processes: {desc}. Using {algo}{extra}, "
              f"what is the TOTAL waiting time of all processes?")
    return _mcq(
        rng, prompt, str(total), _num_distractors(total),
        f"{expl_algo}. Waiting time = start − arrival for each process; "
        f"total = {total}.",
        difficulty, "os/scheduling",
    )


def _fifo_faults(refs: list[int], frames: int) -> int:
    mem: list[int] = []
    faults = 0
    for r in refs:
        if r not in mem:
            faults += 1
            if len(mem) < frames:
                mem.append(r)
            else:
                mem.pop(0)
                mem.append(r)
    return faults


def _lru_faults(refs: list[int], frames: int) -> int:
    mem: list[int] = []  # most-recently-used at the end
    faults = 0
    for r in refs:
        if r in mem:
            mem.remove(r)
            mem.append(r)
        else:
            faults += 1
            if len(mem) < frames:
                mem.append(r)
            else:
                mem.pop(0)
                mem.append(r)
    return faults


def gen_page_faults(rng: random.Random, difficulty: int) -> dict:
    """Page faults for FIFO/LRU — computed by simulation."""
    length = rng.randint(6, 10)
    refs = [rng.randint(1, 5) for _ in range(length)]
    frames = 3 if difficulty <= 5 else rng.choice([3, 4])
    algo = rng.choice(["FIFO", "LRU"])
    faults = _fifo_faults(refs, frames) if algo == "FIFO" else _lru_faults(refs, frames)
    ref_str = ", ".join(str(r) for r in refs)
    return _mcq(
        rng,
        f"Reference string: [{ref_str}], {frames} frames, {algo} replacement. "
        f"How many page faults occur?",
        str(faults), _num_distractors(faults),
        f"Simulating {algo} step by step: a fault occurs on every reference "
        f"not currently in memory. Total faults = {faults}.",
        difficulty, "os/page-faults",
    )


_DEADLOCK_TEMPLATES = [
    ("The OS is allowed to forcibly take a resource away from a process and "
     "give it to another.", "No preemption",
     "If resources can be preempted, the 'no preemption' condition never holds, "
     "so deadlock is impossible."),
    ("Every process requests ALL the resources it will ever need up front, "
     "before starting execution.", "Hold and wait",
     "A process that never holds resources while waiting breaks 'hold and wait'."),
    ("All shared devices are spoolable (e.g., printers via a spooler), so any "
     "number of processes can share them.", "Mutual exclusion",
     "Spoolable resources don't need exclusive access, so 'mutual exclusion' "
     "never holds."),
    ("Resources are numbered, and a process may only request resources in "
     "strictly increasing order of their numbers.", "Circular wait",
     "Ordered allocation makes a circular wait chain impossible."),
    ("A system uses timeouts: any process waiting longer than T releases all "
     "its resources and retries later.", "No preemption",
     "Forced release on timeout is a form of preemption, so 'no preemption' "
     "cannot hold."),
    ("Processes are never allowed to request a new resource while holding "
     "another; they must release everything first.", "Hold and wait",
     "Releasing everything before requesting more breaks 'hold and wait'."),
]
_DEADLOCK_CONDITIONS = ["Mutual exclusion", "Hold and wait", "No preemption",
                        "Circular wait"]


def gen_deadlock(rng: random.Random, difficulty: int) -> dict:
    """Which Coffman condition is absent in the described system."""
    scenario, missing, why = rng.choice(_DEADLOCK_TEMPLATES)
    distract = [c for c in _DEADLOCK_CONDITIONS if c != missing]
    return _mcq(
        rng,
        f"{scenario} Which of the four necessary conditions for deadlock is "
        f"ABSENT here (so deadlock cannot occur)?",
        missing, distract,
        f"Deadlock needs all four: mutual exclusion, hold and wait, no "
        f"preemption, circular wait. {why}",
        difficulty, "os/deadlock",
    )


_PROCESS_TRANSITIONS = [
    ("RUNNING", "READY", "Its time slice expired (it was preempted)",
     ["It requested I/O", "Its I/O operation completed", "It terminated"],
     "When the time slice expires, a running process is preempted back to READY."),
    ("RUNNING", "WAITING", "It requested an I/O operation",
     ["Its time slice expired", "The scheduler dispatched it", "It terminated"],
     "A process that needs I/O blocks: RUNNING → WAITING until I/O completes."),
    ("WAITING", "READY", "Its I/O operation completed",
     ["Its time slice expired", "It was dispatched by the scheduler", "It requested I/O"],
     "I/O completion wakes the process: WAITING → READY."),
    ("READY", "RUNNING", "The CPU scheduler dispatched it",
     ["Its time slice expired", "It requested I/O", "Its I/O completed"],
     "Dispatch assigns the CPU: READY → RUNNING."),
    ("RUNNING", "TERMINATED", "It finished execution (or was killed)",
     ["Its time slice expired", "It requested I/O", "Its I/O completed"],
     "A process that finishes leaves the system: RUNNING → TERMINATED."),
]


def gen_process_state(rng: random.Random, difficulty: int) -> dict:
    """Process state transitions — fixed OS facts, varied presentation."""
    frm, to, correct, distract, why = rng.choice(_PROCESS_TRANSITIONS)
    return _mcq(
        rng,
        f"A process moves from {frm} to {to}. What most likely happened?",
        correct, distract, why, difficulty, "os/process-state",
    )


# =====================================================================
# DBMS generators
# =====================================================================

def _eval_where(row: dict, col: str, op: str, val) -> bool:
    lhs = row[col]
    if op == ">":
        return lhs > val
    if op == "<":
        return lhs < val
    if op == ">=":
        return lhs >= val
    if op == "<=":
        return lhs <= val
    if op == "=":
        return lhs == val
    if op == "!=":
        return lhs != val
    raise DomainError(f"bad op {op}")


def _gen_emp_table(rng: random.Random) -> list[dict]:
    names = ["Asha", "Ravi", "Meera", "Arjun", "Divya", "Karan"]
    depts = ["Eng", "HR", "Sales"]
    rng.shuffle(names)
    rows = []
    for i in range(rng.randint(4, 5)):
        rows.append({
            "id": i + 1,
            "name": names[i],
            "dept": rng.choice(depts),
            "salary": rng.choice([30000, 40000, 50000, 60000, 70000, 80000]),
        })
    return rows


def _fmt_table(rows: list[dict]) -> str:
    lines = ["id | name  | dept  | salary", "---+-------+-------+-------"]
    for r in rows:
        lines.append(f"{r['id']:2d} | {r['name']:<5s} | {r['dept']:<5s} | {r['salary']}")
    return "\n".join(lines)


def gen_sql_output(rng: random.Random, difficulty: int) -> dict:
    """Small table + SQL query; result COMPUTED by a tiny evaluator."""
    rows = _gen_emp_table(rng)
    form = rng.choice(["count", "sum", "avg", "max", "min"])
    col, op, val = "salary", rng.choice([">", "<", ">=", "<="]), rng.choice([40000, 50000, 60000])
    if difficulty >= 6 and rng.random() < 0.4:
        dept = rng.choice(["Eng", "HR", "Sales"])
        extra = f" AND dept = '{dept}'"
        filt = lambda r: _eval_where(r, col, op, val) and r["dept"] == dept
    else:
        extra, dept = "", None
        filt = lambda r: _eval_where(r, col, op, val)
    matched = [r for r in rows if filt(r)]
    if not matched:
        # degenerate filter: fall back to a COUNT(*) = 0 question
        form = "count"
    if form == "count":
        ans, q = len(matched), f"SELECT COUNT(*) FROM emp WHERE salary {op} {val}{extra}"
        expl = f"{len(matched)} of {len(rows)} rows satisfy the condition."
    elif form == "sum":
        ans, q = sum(r["salary"] for r in matched), f"SELECT SUM(salary) FROM emp WHERE salary {op} {val}{extra}"
        expl = f"Salaries of matching rows sum to {ans}."
    elif form == "avg":
        total = sum(r["salary"] for r in matched)
        ans = round(total / len(matched), 1) if matched else 0
        if ans == int(ans):
            ans = int(ans)
        q = f"SELECT AVG(salary) FROM emp WHERE salary {op} {val}{extra}"
        expl = f"Average of matching salaries = {total}/{len(matched)} = {ans}."
    elif form == "max":
        ans, q = (max(r["salary"] for r in matched) if matched else "NULL"), f"SELECT MAX(salary) FROM emp WHERE salary {op} {val}{extra}"
        expl = f"The largest matching salary is {ans}."
    else:
        ans, q = (min(r["salary"] for r in matched) if matched else "NULL"), f"SELECT MIN(salary) FROM emp WHERE salary {op} {val}{extra}"
        expl = f"The smallest matching salary is {ans}."
    prompt = f"Table emp:\n{_fmt_table(rows)}\n\nWhat does this query return?\n{q};"
    if isinstance(ans, int):
        distract = _num_distractors(ans)
    else:
        distract = [str(ans + 10000), str(ans - 10000), str(ans + 20000)]
    return _mcq(rng, prompt, str(ans), distract,
                f"Evaluating row by row: {expl}", difficulty, "dbms/sql-output")


def _fd_closure(attrs: tuple, fds: list, start) -> set:
    closure = set(start)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if set(lhs) <= closure and not set(rhs) <= closure:
                closure |= set(rhs)
                changed = True
    return closure


def _is_superkey(attrs: tuple, fds: list, lhs) -> bool:
    return _fd_closure(attrs, fds, lhs) == set(attrs)


def _candidate_keys(attrs: tuple, fds: list) -> list:
    keys = []
    for r in range(1, len(attrs) + 1):
        for combo in combinations(attrs, r):
            if _is_superkey(attrs, fds, combo):
                if not any(set(k) < set(combo) for k in keys):
                    keys.append(combo)
    return keys


def _highest_nf(attrs: tuple, fds: list) -> str:
    """Compute highest normal form: 1NF / 2NF / 3NF / BCNF."""
    keys = _candidate_keys(attrs, fds)
    prime = {a for k in keys for a in k}
    for lhs, rhs in fds:  # 2NF: no partial dependency
        for a in rhs:
            if a in lhs:
                continue
            if a not in prime and any(set(lhs) < set(k) for k in keys):
                return "1NF"
    for lhs, rhs in fds:  # 3NF
        for a in rhs:
            if a in lhs:
                continue
            if not _is_superkey(attrs, fds, lhs) and a not in prime:
                return "2NF"
    for lhs, rhs in fds:  # BCNF
        for a in rhs:
            if a in lhs:
                continue
            if not _is_superkey(attrs, fds, lhs):
                return "3NF"
    return "BCNF"


# (attrs, fds, note) — answers computed by _highest_nf; hand-verified in tests
_NF_TEMPLATES = [
    (("A", "B", "C"), [(("A",), ("B",)), ((("B",), ("C",)))],
     "A→B and B→C; key is A"),
    (("A", "B", "C"), [((("A", "B"), ("C",)))],
     "only AB→C; key is AB"),
    (("A", "B", "C"), [(("A",), ("B",))],
     "only A→B; key is AC"),
    (("A", "B", "C"), [(("A",), ("B",)), ((("A",), ("C",)))],
     "A→B and A→C; key is A"),
    (("A", "B", "C"), [(("B",), ("C",)), ((("A",), ("B",)))],
     "B→C and A→B; key is A"),
    (("A", "B", "C", "D"), [((("A", "B"), ("C",))), ((("C",), ("D",)))],
     "AB→C and C→D; key is AB"),
]


def gen_normal_form(rng: random.Random, difficulty: int) -> dict:
    """Highest normal form of a relation — COMPUTED from FDs."""
    attrs, fds, note = rng.choice(_NF_TEMPLATES)
    nf = _highest_nf(attrs, fds)
    fd_str = ", ".join(
        f"{''.join(l)}→{''.join(r)}" for l, r in fds)
    r_str = f"R({', '.join(attrs)})"
    order = ["1NF", "2NF", "3NF", "BCNF"]
    if difficulty <= 5 or rng.random() < 0.5:
        prompt = (f"Given {r_str} with functional dependencies {{{fd_str}}}, "
                  f"what is the HIGHEST normal form it satisfies?")
        expl = (f"Checking 2NF (no partial dependency), then 3NF, then BCNF "
                f"({note}): the highest satisfied is {nf}.")
        distract = [x for x in order if x != nf]
        return _mcq(rng, prompt, nf, distract, expl, difficulty,
                    "dbms/normal-form")
    violated = {"1NF": "2NF", "2NF": "3NF", "3NF": "BCNF"}.get(nf)
    if violated is None:  # BCNF satisfied — ask highest instead
        prompt = (f"Given {r_str} with functional dependencies {{{fd_str}}}, "
                  f"what is the HIGHEST normal form it satisfies?")
        expl = f"Every determinant is a superkey ({note}): {nf}."
        distract = [x for x in order if x != nf]
        return _mcq(rng, prompt, nf, distract, expl, difficulty,
                    "dbms/normal-form")
    prompt = (f"Given {r_str} with functional dependencies {{{fd_str}}}, "
              f"which normal form is VIOLATED?")
    expl = (f"The relation satisfies {nf} but fails {violated} "
            f"({note}).")
    distract = [x for x in ["2NF", "3NF", "BCNF"] if x != violated]
    return _mcq(rng, prompt, violated, distract, expl, difficulty,
                "dbms/normal-form")


_ACID_TEMPLATES = [
    ("A transfer debits account A and credits account B. The system crashes "
     "after the debit but before the credit; on recovery the debit is undone.",
     "Atomicity",
     "All-or-nothing: the partial debit was rolled back, so the transaction "
     "is atomic."),
    ("A rule says account balances can never go below zero. After every "
     "committed transfer, all balances are still ≥ 0.",
     "Consistency",
     "Committed transactions move the DB from one valid state to another — "
     "consistency."),
    ("Two transfers run at the same time, but the final balances are exactly "
     "as if the transfers had run one after another.",
     "Isolation",
     "Concurrent transactions behave as if serial — isolation."),
    ("A transfer commits. The power fails a second later, but after reboot "
     "the transfer is still recorded.",
     "Durability",
     "Committed data survives crashes — durability."),
    ("A transaction reads a value, another transaction changes it and commits, "
     "then the first transaction reads a DIFFERENT value for the same item.",
     "Isolation",
     "This non-repeatable read shows isolation was violated."),
    ("Half of a transaction's writes are applied and the system accepts this "
     "as the final state.",
     "Atomicity",
     "Accepting a partial transaction violates all-or-nothing — atomicity."),
]


def gen_acid(rng: random.Random, difficulty: int) -> dict:
    """ACID property identification — fixed answer per scenario template."""
    scenario, prop, why = rng.choice(_ACID_TEMPLATES)
    others = ["Atomicity", "Consistency", "Isolation", "Durability"]
    distract = [p for p in others if p != prop]
    return _mcq(
        rng,
        f"{scenario} Which ACID property is this about?",
        prop, distract, why, difficulty, "dbms/acid",
    )


def gen_join_result(rng: random.Random, difficulty: int) -> dict:
    """JOIN row counts — COMPUTED from key distributions."""
    m, n = rng.randint(3, 6), rng.randint(3, 6)
    keys = [1, 2, 3]
    dist_a = {k: 0 for k in keys}
    dist_b = {k: 0 for k in keys}
    for _ in range(m):
        dist_a[rng.choice(keys)] += 1
    for _ in range(n):
        dist_b[rng.choice(keys)] += 1
    inner = sum(dist_a[k] * dist_b[k] for k in keys)
    form = rng.choice(["inner", "left", "cross"])
    if form == "inner":
        ans = inner
        prompt = (f"Table A has {m} rows, table B has {n} rows. Key counts in A: "
                  f"{dist_a}; in B: {dist_b}. How many rows does "
                  f"`A INNER JOIN B ON A.k = B.k` return?")
        expl = (f"Each matching key pair multiplies: "
                f"{' + '.join(f'{dist_a[k]}×{dist_b[k]}' for k in keys)} = {ans}.")
    elif form == "left":
        ans = m
        prompt = (f"Table A has {m} rows, table B has {n} rows. How many rows does "
                  f"`A LEFT JOIN B ON A.k = B.k` return at minimum "
                  f"(assume every A row matches at least one B row)?")
        expl = (f"LEFT JOIN keeps every row of A at least once: {m} rows minimum "
                f"(more if an A row matches several B rows).")
    else:
        ans = m * n
        prompt = (f"Table A has {m} rows and table B has {n} rows. How many rows "
                  f"does `SELECT * FROM A CROSS JOIN B` return?")
        expl = f"Cross join = Cartesian product: {m} × {n} = {ans}."
    return _mcq(rng, prompt, str(ans), _num_distractors(ans), expl,
                difficulty, "dbms/join-result")


# =====================================================================
# Registry, capacity, public entry points
# =====================================================================

# generator function -> conservative unique-question capacity estimate
_DSA_GENERATORS = [
    (gen_time_complexity, 120),
    (gen_array_trace, 220),
    (gen_big_o_compare, 90),
    (gen_ds_operation, 180),
    (gen_tree_height, 160),
    (gen_sorting_steps, 140),
]
_OS_GENERATORS = [
    (gen_scheduling, 150),
    (gen_page_faults, 130),
    (gen_deadlock, 40),
    (gen_process_state, 30),
]
_DBMS_GENERATORS = [
    (gen_sql_output, 160),
    (gen_normal_form, 60),
    (gen_acid, 40),
    (gen_join_result, 90),
]

_REGISTRY: dict[str, list] = {
    "dsa": _DSA_GENERATORS,
    "os": _OS_GENERATORS,
    "dbms": _DBMS_GENERATORS,
}


def questions_generatable(domain_slug: str) -> int:
    """Conservative estimate of unique questions generatable for a domain."""
    domain = (domain_slug or "").strip().lower()
    if domain not in _REGISTRY:
        raise DomainError(
            f"question generation not supported for '{domain_slug}'; "
            f"supported: {SUPPORTED_DOMAINS}"
        )
    return sum(cap for _, cap in _REGISTRY[domain])


def generate_questions(domain_slug: str, seed: int = 0, count: int = 50,
                       difficulty_range: tuple[int, int] = (1, 10)) -> list[dict]:
    """Deterministically generate `count` questions for a domain.

    Same (domain_slug, seed, count, difficulty_range) -> identical output.
    Prompts are deduped within a call.
    """
    domain = (domain_slug or "").strip().lower()
    if domain not in _REGISTRY:
        raise DomainError(
            f"question generation not supported for '{domain_slug}'; "
            f"supported: {SUPPORTED_DOMAINS}"
        )
    lo, hi = difficulty_range
    if not (1 <= lo <= hi <= 10):
        raise DomainError("difficulty_range must be within 1-10 with lo <= hi")
    if not (1 <= count <= 2000):
        raise DomainError("count must be 1-2000")
    rng = random.Random(seed)
    gens = [g for g, _ in _REGISTRY[domain]]
    rng.shuffle(gens)
    out: list[dict] = []
    seen_prompts: set[str] = set()
    attempts = 0
    gi = 0
    while len(out) < count and attempts < count * 4 + 20:
        attempts += 1
        gen = gens[gi % len(gens)]
        gi += 1
        difficulty = rng.randint(lo, hi)
        try:
            q = gen(rng, difficulty)
        except DomainError:
            continue
        if q["prompt"] in seen_prompts:
            continue
        seen_prompts.add(q["prompt"])
        out.append(q)
    return out
