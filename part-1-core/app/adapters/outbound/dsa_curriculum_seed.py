"""DSA curriculum seed data for SkillForge — expert-level, gradual difficulty.

Expected sibling schema (tables created by parallel curriculum work):
  curriculum_domains   (slug PK, name, icon, description)
  curriculum_modules   (slug PK, domain_slug FK, name, order_index, description)
  curriculum_lessons   (slug PK, module_slug FK, title, order_index, theory_md,
                        difficulty_min, difficulty_max)
  curriculum_questions (id PK, lesson_slug FK, qtype ['mcq','coding'],
                        difficulty 1-10, prompt, choices JSON, answer_index,
                        explanation, company_tags JSON, starter_code JSON nullable)

Usage:
  from app.adapters.outbound.dsa_curriculum_seed import seed, CURRICULUM, CODING_PROBLEMS
  seed()            # uses SQLAlchemy models if importable, else prints SQL
  python -m app.adapters.outbound.dsa_curriculum_seed   # verify counts

All content is original — classic CS problems explained in SkillForge's own
words, TakeUForward-style progression (basics -> patterns -> company-hard).
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


# ---------------------------------------------------------------------------
# DOMAIN
# ---------------------------------------------------------------------------

DOMAIN = {
    "slug": "dsa",
    "name": "Data Structures & Algorithms",
    "icon": "🧠",
    "description": (
        "The #1 placement subject. 8 modules, 68 lessons, 400+ questions — "
        "from 'what is an array' to company-level hard, difficulty rising "
        "gradually 1 to 10 inside every lesson."
    ),
}


# ---------------------------------------------------------------------------
# MODULE 1 — ARRAYS (10 lessons)
# ---------------------------------------------------------------------------

_arrays = M("arrays", "Arrays", "The foundation of everything. Indexing, searching, and the famous patterns (two pointers, sliding window, prefix sums).", [

L("array-basics", "Array Basics — Indexing & Memory",
"""## What is an array?

An **array** stores many values of the same type in **one contiguous block of memory**.
Because memory is contiguous, the computer can jump straight to any element:

```
address of arr[i] = base_address + i * size_of_each_element
```

That formula is why array access is **O(1)** — no searching needed, just arithmetic.

## Key facts

- **Indexing starts at 0.** An array of size `n` has valid indices `0 … n-1`.
- `arr[n]` is **out of bounds** — reading it is undefined behaviour (C/C++) or an exception (Python/Java).
- Arrays have a **fixed size** in C/C++/Java; Python lists are dynamic arrays underneath.

## Example

```python
arr = [10, 20, 30, 40]
print(arr[0])   # 10  (first)
print(arr[3])   # 40  (last, index n-1 = 3)
print(len(arr)) # 4
```
""",
[
Q("What is the index of the LAST element in an array of size n?",
  ["n", "n-1", "n+1", "1"], 1, 1,
  "Indices run 0 to n-1, so the last valid index is n-1.",
  ["TCS", "Infosys", "Wipro"]),
Q("Why is accessing arr[i] an O(1) operation?",
  ["Arrays are sorted", "Memory is contiguous, so address = base + i * size",
   "Arrays are small", "The CPU caches everything"], 1, 2,
  "Contiguous memory turns indexing into one arithmetic computation — no traversal.",
  ["Accenture", "Cognizant"]),
Q("In C++, what happens when you read arr[10] from int arr[10]?",
  ["Returns 0 safely", "Undefined behaviour — garbage or crash",
   "Compiler error", "Returns the first element"], 1, 4,
  "C++ does no bounds checking; out-of-bounds access is undefined behaviour.",
  ["Amazon", "Microsoft"]),
Q("A Python list holds 5 elements. What does lst[-1] return?",
  ["Error", "First element", "Last element", "None"], 2, 3,
  "Python supports negative indexing: -1 means the last element.",
  ["TCS", "Infosys"]),
Q("An int array starts at address 1000, each int is 4 bytes. Address of arr[5]?",
  ["1020", "1005", "1024", "1004"], 0, 6,
  "1000 + 5*4 = 1020.",
  ["Goldman Sachs", "Amazon"]),
Q("Which statement about arrays vs linked lists is TRUE?",
  ["Arrays allow O(1) insertion at front", "Arrays give O(1) random access; linked lists don't",
   "Linked lists use contiguous memory", "Arrays can change size freely in C"], 1, 8,
  "Random access is the array's superpower; linked lists must walk node by node.",
  ["Google", "Microsoft", "Flipkart"]),
]),

L("array-traversal", "Traversal — Visiting Every Element",
"""## Traversal

**Traversal** means visiting each element once, usually with a loop. Almost every
array problem starts with a traversal.

```python
arr = [3, 7, 2, 9]
s = 0
mx = arr[0]
for x in arr:      # visit each element once -> O(n)
    s += x
    if x > mx:
        mx = x
print(s, mx)       # 21 9
```

## The running-variable pattern

Keep one variable that **accumulates** the answer as you walk:

| Problem | Running variable |
|---|---|
| Sum | `total += x` |
| Maximum | `mx = max(mx, x)` |
| Count of evens | `c += (x % 2 == 0)` |

Initialise carefully: max starts at the **first element** (not 0 — the array may hold negatives!).
""",
[
Q("What is the time complexity of visiting every element of an n-size array once?",
  ["O(1)", "O(log n)", "O(n)", "O(n^2)"], 2, 1,
  "Each of the n elements is visited once: O(n).",
  ["TCS", "Wipro"]),
Q("To find the maximum in an array that may contain negatives, best initialise max as:",
  ["0", "arr[0]", "-999999", "None"], 1, 3,
  "Starting from arr[0] works for any values; 0 fails when all numbers are negative.",
  ["Infosys", "Accenture"]),
Q("How many comparisons does a single traversal need to find the max of n elements?",
  ["n", "n-1", "n/2", "log n"], 1, 4,
  "Compare each of the remaining n-1 elements against the current max.",
  ["Amazon"]),
Q("What does this print? arr=[2,4,6]; c=0; for x in arr: c += x%2",
  ["3", "0", "6", "12"], 1, 5,
  "2%2=0, 4%2=0, 6%2=0 → c stays 0. (Counts odd numbers.)",
  ["TCS"]),
Q("A traversal that processes each element twice (two separate loops) is:",
  ["O(n^2)", "O(n) — constants drop", "O(2n) which is worse than O(n)", "O(log n)"], 1, 7,
  "O(2n) = O(n); constant factors are dropped in Big-O.",
  ["Microsoft", "Google"]),
Q("Which loop correctly sums only the elements at even indices?",
  ["for i in range(len(a)): s+=a[i]", "for i in range(0,len(a),2): s+=a[i]",
   "for x in a[1::2]: s+=x", "for i in range(1,len(a),2): s+=a[i]"], 1, 8,
  "range(0, n, 2) hits indices 0,2,4… — the even positions.",
  ["Flipkart", "Amazon"]),
]),

L("array-insert-delete", "Insertion & Deletion — The Shifting Cost",
"""## Why insertion is O(n)

Arrays are contiguous, so inserting in the middle means **shifting** every element
after it one step right:

```
[10, 20, 30, 40]  insert 25 at index 2
[10, 20, _, 30, 40]   <- shift 30, 40 right
[10, 20, 25, 30, 40]
```

- Insert at **end**: O(1) amortised (if space exists)
- Insert at **beginning/middle**: O(n) — everything shifts
- Delete: same story in reverse — elements shift left to fill the gap.

## Takeaway for interviews

> "Arrays are great for **reading**, bad for **frequent inserting/deleting in the middle**."
> That one line answers a whole class of 'array vs linked list' questions.
""",
[
Q("Inserting an element at the BEGINNING of an array of size n costs:",
  ["O(1)", "O(log n)", "O(n)", "O(n^2)"], 2, 2,
  "All n elements must shift one position right.",
  ["TCS", "Infosys"]),
Q("Why is deletion from the middle of an array O(n)?",
  ["Memory must be freed", "Elements after the gap shift left to stay contiguous",
   "The array must be re-sorted", "Garbage collector runs"], 1, 3,
  "Contiguity must be preserved, so every later element moves one slot left.",
  ["Wipro", "Accenture"]),
Q("Which operation on a plain array is O(1)?",
  ["Insert at index 0", "Delete from middle", "Read arr[i]", "Insert keeping sorted order"], 2, 4,
  "Random access by index needs no shifting.",
  ["Cognizant", "TCS"]),
Q("You insert n elements one by one at the front of an array. Total cost?",
  ["O(n)", "O(n log n)", "O(n^2)", "O(1)"], 2, 6,
  "1+2+…+n shifts = n(n+1)/2 = O(n²). This is why we avoid front-insertion in arrays.",
  ["Amazon", "Microsoft"]),
Q("A dynamic array (Python list) doubles capacity when full. n appends cost:",
  ["O(n^2)", "O(n) amortised", "O(n log n)", "O(1) worst case"], 1, 8,
  "Occasional O(n) copies are spread over many O(1) appends — amortised O(1) each.",
  ["Google", "Flipkart"]),
Q("Best data structure for 'frequent insert/delete in the middle, rare random access'?",
  ["Array", "Linked list", "Hash table", "Stack"], 1, 9,
  "Linked lists splice nodes with pointer changes — O(1) once you're at the position.",
  ["Microsoft", "Amazon"]),
]),

L("linear-search", "Linear Search — Check Everything",
"""## The simplest search

Walk from the first element; stop when you find the target.

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i      # found
    return -1             # not found
```

## Complexity

- **Best case O(1)** — target is first.
- **Worst case O(n)** — target is last or absent.
- **Average O(n)**.
- Works on **unsorted** data — its only requirement is that you can iterate.

## When to use it

Small arrays, unsorted data, or a one-off search where sorting first would cost more than it saves.
""",
[
Q("Linear search works on:",
  ["Only sorted arrays", "Any array, sorted or not", "Only arrays of size < 100", "Only integers"], 1, 1,
  "It checks elements one by one — order doesn't matter.",
  ["TCS", "Wipro"]),
Q("Worst-case time complexity of linear search on n elements?",
  ["O(1)", "O(log n)", "O(n)", "O(n log n)"], 2, 2,
  "You may scan all n elements when the target is last or missing.",
  ["Infosys", "Accenture"]),
Q("Best case of linear search happens when the target is at index:",
  ["n-1", "0", "n//2", "any index"], 1, 3,
  "Found on the very first comparison: O(1).",
  ["Cognizant"]),
Q("linear_search returns -1. What does that mean?",
  ["Target found at index -1", "Target not present", "Array is empty", "Error occurred"], 1, 4,
  "-1 is the conventional 'not found' sentinel.",
  ["TCS"]),
Q("Searching an unsorted array of 10^6 elements once: linear search vs sort-then-binary-search?",
  ["Sort then binary search", "Linear search — sorting costs O(n log n) for one query",
   "Both equal", "Neither works"], 1, 7,
  "Sorting (n log n) to answer a single query is wasteful; one linear scan is O(n).",
  ["Amazon", "Microsoft"]),
Q("In the worst case, how many comparisons to confirm an element is ABSENT?",
  ["0", "1", "n", "n-1"], 2, 8,
  "You must check every element before concluding absence.",
  ["Goldman Sachs", "Google"]),
]),

L("binary-search", "Binary Search — Halve the Problem",
"""## The idea

On a **sorted** array, compare the target with the middle element:

- equal → found
- target < mid → search **left** half
- target > mid → search **right** half

Each step **halves** the search space: O(log n).

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1
```

## Classic bug

`(lo + hi) // 2` can **overflow** in C++/Java when lo+hi exceeds INT_MAX.
Safe form: `mid = lo + (hi - lo) // 2`. Interviewers love asking this.

## Loop condition

`while lo <= hi` — with `<` you'd miss checking the last single element.
""",
[
Q("Binary search REQUIRES the array to be:",
  ["Large", "Sorted", "Of integers", "Unique elements"], 1, 2,
  "Halving only works when order tells you which half to discard.",
  ["TCS", "Infosys", "Wipro"]),
Q("Time complexity of binary search?",
  ["O(n)", "O(log n)", "O(n log n)", "O(1)"], 1, 3,
  "Search space halves each step: n → n/2 → … → 1 takes log₂n steps.",
  ["Accenture", "Cognizant"]),
Q("Why is `mid = lo + (hi-lo)//2` preferred over `(lo+hi)//2` in Java/C++?",
  ["It's faster", "Avoids integer overflow of lo+hi", "Uses less memory", "No reason"], 1, 6,
  "lo+hi can overflow 32-bit int; the rewritten form never exceeds hi.",
  ["Amazon", "Microsoft", "Google"]),
Q("Correct loop condition for iterative binary search?",
  ["while lo < hi", "while lo <= hi", "while True", "while lo != hi"], 1, 5,
  "<= keeps the single remaining element in play; < would skip it.",
  ["Flipkart"]),
Q("Sorted array of 1,000,000 elements. Worst-case comparisons (approx)?",
  ["1,000,000", "20", "500,000", "1,000"], 1, 7,
  "log₂(10⁶) ≈ 20.",
  ["Goldman Sachs", "Microsoft"]),
Q("Binary search on [2,4,6,8,10] for target 8 — which index is checked FIRST?",
  ["4", "0", "2", "3"], 2, 8,
  "mid = (0+4)//2 = 2 → arr[2]=6 < 8, go right; next mid=3 → found.",
  ["Amazon", "Google"]),
]),

L("sorting-basics", "Sorting Basics — Bubble Idea & Sorted Check",
"""## What 'sorted' means for code

```python
def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True          # O(n) check
```

## Bubble sort idea

Repeatedly walk through, **swapping adjacent out-of-order pairs**. After each
full pass, the largest remaining element "bubbles" to its final position.

```
[5, 3, 8, 1]  pass 1 -> [3, 5, 1, 8]  (8 bubbled to end)
              pass 2 -> [3, 1, 5, 8]
              pass 3 -> [1, 3, 5, 8]  done
```

- Worst/average: **O(n²)**, Best (already sorted + early exit): **O(n)**.
- **Stable**: equal elements keep their original order.

## Why learn a 'slow' sort?

Bubble sort teaches **swaps, passes, and invariants** — the vocabulary of every
other sorting algorithm.
""",
[
Q("Checking whether an array is sorted takes:",
  ["O(1)", "O(n)", "O(n log n)", "O(n^2)"], 1, 2,
  "One pass comparing neighbours: n-1 comparisons.",
  ["TCS", "Wipro"]),
Q("After the FIRST pass of bubble sort on n elements, what is guaranteed?",
  ["Whole array sorted", "Largest element at the end", "Smallest at front", "Nothing"], 1, 4,
  "Each pass bubbles the largest remaining element to its final spot.",
  ["Infosys", "Accenture"]),
Q("Bubble sort worst-case complexity?",
  ["O(n)", "O(n log n)", "O(n^2)", "O(2^n)"], 2, 3,
  "~n passes × ~n comparisons.",
  ["Cognizant", "TCS"]),
Q("What does 'stable sort' mean?",
  ["Fastest sort", "Equal elements keep original relative order", "Uses no extra memory", "Works on any data"], 1, 6,
  "Stability matters when sorting records by one key while preserving another order.",
  ["Amazon", "Microsoft"]),
Q("Bubble sort with an early-exit flag on an already-sorted array runs in:",
  ["O(n^2)", "O(n)", "O(1)", "O(log n)"], 1, 7,
  "One pass with zero swaps detects sortedness — flag exits early.",
  ["Google", "Flipkart"]),
Q("[3,1,2] — how many swaps does bubble sort perform (no early exit)?",
  ["2", "3", "1", "4"], 0, 8,
  "Pass1: 3>1 swap→[1,3,2]; 3>2 swap→[1,2,3]; then no more swaps. Total 2.",
  ["Goldman Sachs", "Amazon"]),
]),

L("two-pointers", "Two Pointers — Meet in the Middle",
"""## The pattern

Put one pointer at each **end** of a **sorted** array and move them based on
what you see. The classic: *pair with a given sum*.

```python
def has_pair(arr, target):      # arr sorted
    l, r = 0, len(arr) - 1
    while l < r:
        s = arr[l] + arr[r]
        if s == target: return True
        elif s < target: l += 1  # need bigger sum -> move left up
        else: r -= 1             # need smaller sum -> move right down
    return False
```

## Why it works

The array is sorted, so each comparison **eliminates one whole side**:
too small → the left element can't pair with anything; too big → symmetric.
Every step discards one element: **O(n)** after sorting.

## Variants

- **Same direction** (fast/slow) for linked lists & removing duplicates.
- **Opposite direction** (this lesson) for pair/triplet sums on sorted arrays.
""",
[
Q("Two-pointer pair-sum requires the array to be:",
  ["Unsorted", "Sorted", "All positive", "Size < 1000"], 1, 3,
  "Sortedness lets one comparison eliminate a whole side.",
  ["TCS", "Infosys"]),
Q("In pair-sum, if arr[l]+arr[r] < target, we do:",
  ["r -= 1", "l += 1", "return False", "l += 2"], 1, 4,
  "Sum too small → need a bigger left element → move l right.",
  ["Wipro", "Accenture"]),
Q("Time complexity of two-pointer pair search (array already sorted)?",
  ["O(n^2)", "O(n)", "O(log n)", "O(n log n)"], 1, 5,
  "Each step moves one pointer; at most n steps.",
  ["Cognizant", "Amazon"]),
Q("Sorted [1,3,5,7,9], target 12. First pair checked? Then?",
  ["(1,9) then l moves", "(1,9) then r moves", "(5,7) done", "(3,9) then l moves"], 0, 6,
  "1+9=10 < 12 → l+=1. (Eventually 3+9=12 ✓)",
  ["Microsoft", "Flipkart"]),
Q("Why can't the basic opposite-ends two-pointer find triplets directly?",
  ["It can, unchanged", "It only tracks a pair sum; triplets need an outer loop fixing one element",
   "Arrays are too short", "Pointers can't move"], 1, 8,
  "Standard trick: fix arr[i], then two-pointer the rest for target-arr[i] → O(n²).",
  ["Google", "Amazon"]),
Q("Two pointers on UNSORTED [4,1,3,2], target 5 — does the algorithm stay correct?",
  ["Yes", "No — elimination logic assumes sorted order", "Only for small arrays", "Yes if target is small"], 1, 9,
  "Without order, 'too small → move l' is meaningless; it may skip the real pair.",
  ["Goldman Sachs", "Microsoft"]),
]),

L("sliding-window", "Sliding Window — Fixed-Size Views",
"""## The pattern

For problems like *"maximum sum of k consecutive elements"*, don't recompute
each window from scratch — **slide** it:

```python
def max_sum_k(arr, k):
    window = sum(arr[:k])
    best = window
    for i in range(k, len(arr)):
        window += arr[i] - arr[i - k]   # add new, drop old
        best = max(best, window)
    return best
```

Each step is O(1): total **O(n)** instead of O(n·k).

## The mental model

> The window is a frame of fixed width sliding over the array.
> Entering element joins, leaving element drops out — the sum updates, never rebuilds.

## Fixed vs variable window

- **Fixed k** (this lesson): add right, remove left.
- **Variable** (advanced): expand right, shrink left while a condition holds.
""",
[
Q("Naive max-sum-of-k-consecutive (recompute each window) costs:",
  ["O(n)", "O(n*k)", "O(k)", "O(n log n)"], 1, 4,
  "n-k+1 windows × k work each.",
  ["TCS", "Infosys"]),
Q("The sliding-window update when moving right by one is:",
  ["Recompute whole window", "window += new - old", "window *= 2", "window = 0"], 1, 3,
  "Add the entering element, subtract the leaving one — O(1).",
  ["Wipro", "Accenture"]),
Q("Sliding window (fixed k) total complexity?",
  ["O(n)", "O(n*k)", "O(k)", "O(n^2)"], 0, 5,
  "n steps × O(1) update.",
  ["Cognizant", "Amazon"]),
Q("arr=[1,4,2,10,3], k=2. Window sums are:",
  ["5,6,12,13 → max 13", "5,6,12,11", "1,4,2,10,3", "6,12,13"], 0, 6,
  "(1+4)=5,(4+2)=6,(2+10)=12,(10+3)=13 → max 13.",
  ["Microsoft", "Flipkart"]),
Q("Which problem does FIXED sliding window NOT fit?",
  ["Max sum of k consecutive", "Longest subarray with sum ≤ S (k varies)",
   "Average of every k elements", "Max of every k elements"], 1, 8,
  "Variable-length needs the expand/shrink variant, not fixed k.",
  ["Google", "Amazon"]),
Q("If k > n, the fixed-window algorithm should:",
  ["Crash", "Handle as edge case (e.g. sum whole array / invalid input)", "Return 0 always", "Sort first"], 1, 9,
  "Guard inputs: k > n means no valid window exists.",
  ["Goldman Sachs"]),
]),

L("prefix-sum", "Prefix Sums — Answer Range Queries Fast",
"""## The trick

Precompute `pref[i] = arr[0] + … + arr[i]`. Then any range sum is one subtraction:

```
sum(arr[l..r]) = pref[r] - pref[l-1]      (pref[-1] treated as 0)
```

```python
arr  = [2, 4, 1, 7, 3]
pref = [2, 6, 7, 14, 17]
sum(1..3) = pref[3] - pref[0] = 14 - 2 = 12   # 4+1+7 ✓
```

## Cost

- Build: O(n) once.
- Each query: **O(1)**.
- q queries: O(n + q) instead of O(n·q).

## Interview line

> "Many range-sum queries on a static array? Prefix sums."
> (If the array also gets *updates*, the grown-up answer is a Fenwick tree / segment tree.)
""",
[
Q("With prefix sums, sum of arr[l..r] equals:",
  ["pref[r] + pref[l]", "pref[r] - pref[l-1]", "pref[l] - pref[r]", "pref[r] * pref[l]"], 1, 4,
  "pref[r] holds sum[0..r]; subtract sum[0..l-1] to isolate [l..r].",
  ["TCS", "Infosys"]),
Q("Building the prefix array for n elements costs:",
  ["O(1)", "O(n)", "O(n log n)", "O(n^2)"], 1, 3,
  "One left-to-right pass.",
  ["Wipro", "Accenture"]),
Q("arr=[2,4,1,7,3], pref=[2,6,7,14,17]. sum(2..4)?",
  ["17", "11", "15", "14"], 1, 5,
  "pref[4]-pref[1] = 17-6 = 11 (1+7+3 ✓).",
  ["Amazon", "Cognizant"]),
Q("1000 range-sum queries on a static array of size n. Best approach?",
  ["Recompute each query O(n*q)", "Prefix sums O(n+q)", "Sort the array", "Binary search"], 1, 7,
  "Preprocess once, answer each query in O(1).",
  ["Microsoft", "Google"]),
Q("Prefix sums break down when the array also has frequent:",
  ["Reads", "Point updates — use Fenwick/segment tree", "Queries", "Negative numbers"], 1, 8,
  "Each update would force O(n) rebuild of the prefix array.",
  ["Flipkart", "Amazon"]),
Q("Equilibrium index (left sum == right sum) can be found in O(n) using:",
  ["Sorting", "Total sum + one left-to-right pass (prefix idea)", "Binary search", "Two pointers"], 1, 9,
  "right_sum = total - left_sum - arr[i]; single pass checks each i.",
  ["Goldman Sachs", "Microsoft"]),
]),

L("kadane-rotation", "Kadane's Algorithm & Rotation",
"""## Kadane's — maximum subarray sum

At each position decide: **extend** the previous subarray or **start fresh** here.

```python
def kadane(arr):
    best = cur = arr[0]
    for x in arr[1:]:
        cur = max(x, cur + x)   # start fresh vs extend
        best = max(best, cur)
    return best
```

`[−2, 3, −1, 4, −1]` → best = 6 (`3,−1,4`). **O(n)** time, O(1) space.

## Rotate array by k

Reverse trick (right rotation by k):

1. Reverse whole array
2. Reverse first k
3. Reverse the rest

`[1,2,3,4,5]`, k=2 → `[5,4,3,2,1]` → `[4,5,3,2,1]` → `[4,5,1,2,3]` ✓ — O(n), O(1) space.

## Don't forget

`k %= n` first — rotating by n (or multiples) is a no-op.
""",
[
Q("Kadane's algorithm finds:",
  ["Maximum element", "Maximum subarray sum", "Longest subarray", "Minimum element"], 1, 4,
  "It tracks the best subarray ENDING at each position.",
  ["TCS", "Infosys"]),
Q("At each step, Kadane's chooses between:",
  ["Two pointers", "Starting fresh at x vs extending (cur + x)", "Sorting", "Skipping x"], 1, 5,
  "cur = max(x, cur+x) — the heart of the algorithm.",
  ["Wipro", "Accenture"]),
Q("kadane([-2,3,-1,4,-1]) returns?",
  ["4", "5", "6", "3"], 2, 6,
  "cur: 3,2,6,5 → best 6 (subarray [3,-1,4]).",
  ["Amazon", "Microsoft"]),
Q("Time/space of Kadane's?",
  ["O(n)/O(n)", "O(n)/O(1)", "O(n log n)/O(1)", "O(n^2)/O(1)"], 1, 5,
  "Single pass, two variables.",
  ["Cognizant"]),
Q("Right-rotate [1,2,3,4,5] by k=7. Effective k?",
  ["7", "2", "0", "5"], 1, 7,
  "k %= n → 7 % 5 = 2.",
  ["Google", "Flipkart"]),
Q("The 3-reverse rotation trick uses what extra space?",
  ["O(n)", "O(1)", "O(k)", "O(log n)"], 1, 8,
  "All reversals are in-place.",
  ["Goldman Sachs", "Amazon"]),
]),
])

MODULES = [_arrays]


# ---------------------------------------------------------------------------
# MODULE 2 — STRINGS (8 lessons)
# ---------------------------------------------------------------------------

_strings = M("strings", "Strings", "Reversal, palindromes, anagrams, and pattern matching — string problems test pointer discipline.", [

L("string-basics", "String Basics — Characters & Immutability",
"""## Strings are character arrays (with rules)

A string is a sequence of characters. The big gotcha: **immutability**.

- **Python / Java**: strings are **immutable** — `s[0] = 'x'` is an error.
  Every "modification" builds a NEW string.
- **C++** `std::string`: **mutable** — you can assign `s[0] = 'x'`.

## Why it matters

```python
s = "hello"
s += " world"   # looks cheap...
```

In a loop, `s += chunk` copies the whole string **each time** → O(n²) total.
The fix: collect pieces in a list, then `''.join(pieces)` once → O(n).

## ASCII vs Unicode

- ASCII: 128 characters (English letters, digits, symbols).
- Unicode: every script on Earth. Python 3 strings are Unicode by default.
- Frequency arrays sized **26** assume lowercase English; **128/256** covers ASCII.
""",
[
Q("In Python, strings are:",
  ["Mutable", "Immutable", "Only ASCII", "Stored as linked lists"], 1, 1,
  "Python strings can't be changed in place; operations return new strings.",
  ["TCS", "Infosys"]),
Q("Why is repeated `s += chunk` in a loop slow in Python?",
  ["Strings are sorted", "Each += copies the whole string → O(n²)", "Python is slow", "Memory leak"], 1, 4,
  "Immutability forces a full copy per concatenation.",
  ["Wipro", "Accenture"]),
Q("The efficient way to build a long string from pieces in Python?",
  ["+= in a loop", "Collect in list, ''.join() once", "Use * operator", "format() each time"], 1, 5,
  "join() allocates once and copies each piece exactly once: O(n).",
  ["Amazon", "Cognizant"]),
Q("In C++, std::string is:",
  ["Immutable", "Mutable — s[0]='x' works", "Fixed length", "ASCII only"], 1, 3,
  "C++ strings own a mutable buffer.",
  ["Microsoft"]),
Q("A frequency array of size 26 assumes input is:",
  ["Any Unicode", "Lowercase English letters", "Digits", "ASCII symbols"], 1, 6,
  "'a'-'z' maps to 0-25; anything else breaks the assumption.",
  ["Google", "Flipkart"]),
Q("ord('b') - ord('a') equals?",
  ["0", "1", "2", "98"], 1, 7,
  "Consecutive letters differ by 1 — the basis of char→index mapping.",
  ["Goldman Sachs", "Amazon"]),
]),

L("string-reversal", "Reversal — Two Pointers on Characters",
"""## Reverse in place

Swap characters from both ends moving inward:

```python
def reverse(s):                 # s as list of chars
    l, r = 0, len(s) - 1
    while l < r:
        s[l], s[r] = s[r], s[l]
        l += 1; r -= 1
```

- Time O(n), space O(1) for mutable char arrays.
- In Python (immutable str): `s[::-1]` or `''.join(reversed(s))` — O(n) time AND space (a new string is built).

## Reverse WORDS in a sentence

`"sky is blue"` → `"blue is sky"`:
1. Reverse the whole string: `"eulb si yks"`
2. Reverse each word back: `"blue is sky"`

O(n) time, O(1) extra space. A favourite follow-up question.
""",
[
Q("Reversing a char array in place with two pointers costs:",
  ["O(n) time, O(1) space", "O(n²) time", "O(n) space", "O(log n) time"], 0, 2,
  "n/2 swaps, no extra array.",
  ["TCS", "Wipro"]),
Q("Python's s[::-1] uses what extra space?",
  ["O(1)", "O(n) — builds a new string", "O(log n)", "None"], 1, 4,
  "Immutability: the reversed copy is a brand-new string.",
  ["Infosys", "Accenture"]),
Q("How many swaps to reverse a 7-char array in place?",
  ["7", "3", "4", "6"], 1, 5,
  "floor(7/2) = 3 swaps; the middle char stays.",
  ["Cognizant"]),
Q("Reverse words in 'sky is blue' → ?",
  ["'eulb si yks'", "'blue is sky'", "'yks si eulb'", "'blue si yks'"], 1, 6,
  "Reverse whole, then reverse each word.",
  ["Amazon", "Microsoft"]),
Q("Loop condition for in-place reversal?",
  ["l <= r", "l < r", "l != r", "True"], 1, 7,
  "Stop when pointers meet/cross; <= would pointlessly swap the middle with itself on odd lengths.",
  ["Google"]),
Q("Reversing each word of a sentence individually ('hello world' → 'olleh dlrow') is:",
  ["O(n²)", "O(n) — each char visited a constant times", "O(n log n)", "Impossible in place"], 1, 8,
  "Two passes over n chars total.",
  ["Flipkart", "Amazon"]),
]),

L("palindrome-check", "Palindromes — Reads Same Both Ways",
"""## Two-pointer check

```python
def is_palindrome(s):
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]: return False
        l += 1; r -= 1
    return True
```

O(n) time, O(1) space.

## Real-world version

*"Valid palindrome ignoring case and non-alphanumerics"* (`"A man, a plan, a canal: Panama"` → True):
- Skip non-alphanumeric chars with `isalnum()`.
- Compare lowercase.

## Don't do this in interviews

`s == s[::-1]` is correct Python but O(n) extra space — interviewers expect the
two-pointer version and will ask for it as a follow-up.
""",
[
Q("'racecar' is a palindrome because:",
  ["It has 7 letters", "It reads the same forwards and backwards", "It's a word", "All letters repeat"], 1, 1,
  "That's the definition of palindrome.",
  ["TCS", "Wipro"]),
Q("Two-pointer palindrome check complexity?",
  ["O(n) time, O(1) space", "O(n²)", "O(n) space", "O(log n)"], 0, 3,
  "Pointers meet in the middle; only indices stored.",
  ["Infosys", "Accenture"]),
Q("Why might an interviewer reject `s == s[::-1]`?",
  ["It's wrong", "O(n) extra space — they want O(1)", "Too slow", "Doesn't work"], 1, 6,
  "Correct but wasteful; two pointers show you understand space.",
  ["Amazon", "Microsoft"]),
Q("For 'A man, a plan, a canal: Panama' to return True you must:",
  ["Sort it", "Ignore case + skip non-alphanumerics", "Remove vowels", "Reverse twice"], 1, 5,
  "Real palindrome problems normalise the string first.",
  ["Cognizant", "Google"]),
Q("Longest palindromic substring — the expand-around-center idea checks how many centers?",
  ["n", "2n - 1 (n chars + n-1 gaps)", "n²", "log n"], 1, 8,
  "Odd palindromes center on chars, even on gaps between chars.",
  ["Flipkart", "Amazon"]),
Q("Minimum insertions to make 'abca' a palindrome?",
  ["0", "1", "2", "3"], 1, 9,
  "'abcba' needs 1 insertion (b). Equivalent to n - LPS length = 4-3 = 1.",
  ["Goldman Sachs", "Microsoft"]),
]),

L("anagram-check", "Anagrams — Same Letters, Different Order",
"""## Frequency counting

Two strings are anagrams iff every character appears the same number of times:

```python
from collections import Counter
def is_anagram(a, b):
    return Counter(a) == Counter(b)     # O(n) time
```

Manual version: one array of 26 counts, +1 for `a`, -1 for `b`, all zeros at end.

## Sorting approach

`sorted(a) == sorted(b)` — correct but O(n log n). Frequency counting is O(n);
mention both, then say which you'd ship.

## Group anagrams (famous follow-up)

Key each word by its **sorted form** (or 26-count tuple) in a hash map:
`"eat" → "aet"`. Words sharing a key are anagrams. O(n·k log k).
""",
[
Q("'listen' and 'silent' are anagrams because:",
  ["Same length", "Same character frequencies", "Both English", "Start with 's'/'l'"], 1, 2,
  "Anagram = identical multiset of characters.",
  ["TCS", "Infosys"]),
Q("Frequency-count anagram check runs in:",
  ["O(n log n)", "O(n)", "O(n²)", "O(1)"], 1, 4,
  "Two passes to count, one pass over 26 slots to compare.",
  ["Wipro", "Accenture"]),
Q("First necessary check before counting?",
  ["Sort both", "len(a) == len(b)", "Lowercase", "Remove spaces"], 1, 3,
  "Different lengths can never be anagrams — O(1) early exit.",
  ["Cognizant"]),
Q("`sorted(a) == sorted(b)` anagram check costs:",
  ["O(n)", "O(n log n)", "O(1)", "O(n²)"], 1, 6,
  "Sorting dominates.",
  ["Amazon"]),
Q("Group anagrams: best hash-map key for a word?",
  ["The word itself", "Its sorted form / 26-count tuple", "Its length", "First letter"], 1, 7,
  "Anagrams share the same canonical key.",
  ["Microsoft", "Google"]),
Q("Counter('aab') == Counter('abb')?",
  ["True", "False", "Error", "None"], 1, 8,
  "{a:2,b:1} vs {a:1,b:2} — differ.",
  ["Flipkart", "Goldman Sachs"]),
]),

L("char-frequency", "Character Frequency — Counting Sort Thinking",
"""## Count first, ask later

Many string problems dissolve once you count characters:

```python
freq = [0] * 26
for ch in s:
    freq[ord(ch) - ord('a')] += 1
```

## Classic uses

- **First non-repeating character**: count, then scan for freq == 1. O(n).
- **Sort characters by frequency**: bucket by count. O(n).
- **Ransom note** (can magazine build the note?): counts of magazine minus note, none negative.

## First unique char — two passes

Pass 1: build frequencies. Pass 2: return first index with count 1.
One pass can't work — you don't know a char is unique until you've seen the whole string.
""",
[
Q("First non-repeating character needs how many passes minimum?",
  ["1", "2 — count, then find first with count 1", "3", "n"], 1, 5,
  "Uniqueness is only known after the full string is counted.",
  ["TCS", "Infosys"]),
Q("Frequency array for lowercase letters has size:",
  ["128", "26", "256", "10"], 1, 2,
  "'a'-'z' → 26 slots.",
  ["Wipro"]),
Q("'Ransom note' problem: magazine='aab', note='aba'. Possible?",
  ["Yes", "No", "Only with sorting", "Error"], 0, 6,
  "magazine has a:2,b:1; note needs a:2,b:1 — exact match.",
  ["Accenture", "Amazon"]),
Q("Building the frequency array is:",
  ["O(n²)", "O(n)", "O(26n)", "O(log n)"], 1, 4,
  "One increment per character.",
  ["Cognizant"]),
Q("Sort string by character frequency ('tree' → 'eert'/'eetr') can be done in:",
  ["O(n log n) only", "O(n) with bucket-by-count", "O(n²)", "Impossible"], 1, 8,
  "Max frequency ≤ n, so counting buckets beat comparison sort.",
  ["Microsoft", "Google"]),
Q("In 'aabbc', first non-repeating char is:",
  ["a", "b", "c", "none"], 2, 7,
  "a:2, b:2, c:1 → 'c' at index 4.",
  ["Flipkart", "Goldman Sachs"]),
]),

L("substrings-gen", "Substrings — Generation & Counting",
"""## All substrings

A string of length n has **n(n+1)/2** substrings — pick start i, extend end j:

```python
subs = []
for i in range(len(s)):
    for j in range(i + 1, len(s) + 1):
        subs.append(s[i:j])
```

That's O(n²) substrings; printing each costs up to O(n) → O(n³) total naive.

## Distinct substrings

Use a **set** to deduplicate: O(n²) substrings stored. (Suffix array/trie is the advanced answer.)

## Longest substring WITHOUT repeating characters

Variable sliding window + last-seen map:

```python
seen, l, best = {}, 0, 0
for r, ch in enumerate(s):
    if ch in seen and seen[ch] >= l:
        l = seen[ch] + 1      # jump left past previous occurrence
    seen[ch] = r
    best = max(best, r - l + 1)
```

O(n) — each char visited once. The `>= l` guard prevents moving `l` backwards.
""",
[
Q("Number of substrings of a length-n string?",
  ["n", "2n", "n(n+1)/2", "n²"], 2, 4,
  "Start has n choices, end has shrinking choices: n+(n-1)+…+1.",
  ["TCS", "Infosys"]),
Q("'abc' has how many substrings?",
  ["3", "6", "9", "5"], 1, 3,
  "3*4/2 = 6: a,b,c,ab,bc,abc.",
  ["Wipro"]),
Q("Longest substring without repeats uses:",
  ["Fixed window", "Variable sliding window + last-seen map", "Sorting", "Two pointers from ends"], 1, 7,
  "Expand right; shrink left past the duplicate.",
  ["Accenture", "Amazon"]),
Q("In that algorithm, why check `seen[ch] >= l`?",
  ["Speed", "Prevent moving l backwards past its current spot", "Avoid KeyError", "No reason"], 1, 8,
  "An old occurrence left of the window must not drag l back.",
  ["Microsoft", "Google"]),
Q("Longest non-repeating substring of 'abba'?",
  ["4", "2 ('ab' or 'ba')", "3", "1"], 1, 9,
  "Trace: r=2 'b' seen at 1 ≥ l=0 → l=2; best stays 2.",
  ["Flipkart", "Goldman Sachs"]),
Q("Generating ALL substrings and printing each is:",
  ["O(n²)", "O(n³) — O(n²) substrings × O(n) print", "O(n)", "O(n log n)"], 1, 6,
  "Count the output cost too.",
  ["Cognizant"]),
]),

L("kmp-intro", "Pattern Matching — Naive vs KMP Idea",
"""## Naive matching

```python
# find pattern p in text t
for i in range(len(t) - len(p) + 1):
    if t[i:i+len(p)] == p: return i
```

Worst case O(n·m): text `aaaa…ab`, pattern `aaab` — every alignment almost matches.

## KMP's insight

When a mismatch happens, the **already-matched prefix** tells you how far to
jump — never re-scan text characters. It precomputes the **LPS array**
(longest proper prefix which is also a suffix) for the pattern.

```
pattern "aaba": LPS = [0, 1, 0, 1]
```

## Result

- Preprocess pattern: O(m)
- Scan text: O(n)
- Total **O(n + m)**, each text char examined at most twice.

## Interview expectation

You must know naive cold, explain KMP's *idea* (skip re-scanning via LPS),
and many interviewers accept that without full LPS derivation.
""",
[
Q("Naive pattern matching worst case?",
  ["O(n)", "O(n*m)", "O(n+m)", "O(n log m)"], 1, 5,
  "n alignments × m comparisons.",
  ["TCS", "Infosys"]),
Q("KMP's total time for text n, pattern m?",
  ["O(n*m)", "O(n + m)", "O(n log m)", "O(n²)"], 1, 6,
  "O(m) preprocessing + O(n) scan.",
  ["Wipro", "Accenture"]),
Q("LPS stands for:",
  ["Longest Prefix Sequence", "Longest proper Prefix which is also Suffix", "Last Pattern Symbol", "Linear Prefix Scan"], 1, 4,
  "It's the failure-link table of KMP.",
  ["Amazon", "Cognizant"]),
Q("LPS of 'aaaa' is:",
  ["[0,0,0,0]", "[0,1,2,3]", "[1,2,3,4]", "[0,1,1,1]"], 1, 7,
  "Each position's longest proper border grows by 1.",
  ["Microsoft", "Google"]),
Q("KMP never re-scans text characters because:",
  ["Text is sorted", "The matched prefix determines the safe shift", "It uses extra memory", "Patterns are short"], 1, 8,
  "LPS tells exactly how much of the pattern is already matched after a shift.",
  ["Flipkart"]),
Q("Which problem does KMP NOT solve faster than naive?",
  ["Single pattern in long text", "Counting pattern occurrences", "Finding ALL anagrams of pattern in text", "Repeated single-pattern search"], 2, 9,
  "Anagram search needs frequency windows, not prefix matching.",
  ["Goldman Sachs", "Amazon"]),
]),

L("string-building", "String Building — Joins, Builders & Parsing",
"""## The performance rules

| Language | Bad in loop | Good |
|---|---|---|
| Python | `s += x` | `''.join(list)` |
| Java | `s += x` | `StringBuilder` |
| C++ | `s += x` (ok-ish, amortised) | reserve + `+=` |

## Parsing integers

- Python: `int("123")`, `str(123)` back.
- Watch for: leading/trailing spaces (`strip()`), signs, overflow in Java/C++ (`Integer.parseInt` throws).

## Compare version strings — interview classic

`"1.2"` vs `"1.10"`: split on `.`, compare ints part by part → `1.2 < 1.10`.
String comparison would wrongly say `"1.10" < "1.2"` ('1' < '2' at second char).

## atoi — the full checklist

Whitespace → sign → digits → stop at non-digit → clamp to 32-bit range.
Each step is one classic edge case interviewers probe.
""",
[
Q("Java's efficient string builder in loops?",
  ["String", "StringBuilder", "StringBuffer always", "char[]"], 1, 3,
  "StringBuilder avoids creating a new String per +=.",
  ["TCS", "Infosys"]),
Q("Python equivalent of StringBuilder thinking?",
  ["f-strings", "list + ''.join()", "% formatting", "concat()"], 1, 4,
  "Amortised appends, one final copy.",
  ["Wipro", "Accenture"]),
Q("Why is '1.10' < '1.2' TRUE as plain strings but wrong as versions?",
  ["Bug", "Lexicographic: '1'<'2' at second component", "Versions can't compare", "Encoding issue"], 1, 6,
  "Version parts must be compared as integers.",
  ["Amazon", "Cognizant"]),
Q("int('  -42 ') in Python gives:",
  ["Error", "-42", "42", "0"], 1, 5,
  "int() strips whitespace and handles signs.",
  ["Microsoft"]),
Q("atoi('words 987') should return:",
  ["987", "0 — no leading digits", "Error", "987words"], 1, 7,
  "Conversion stops when no valid digits lead; result 0.",
  ["Google", "Flipkart"]),
Q("Clamping in atoi exists because:",
  ["Style", "32-bit overflow must saturate at INT_MAX/MIN", "Speed", "Unicode"], 1, 8,
  "The spec demands saturation, not wraparound.",
  ["Goldman Sachs", "Amazon"]),
]),
])

MODULES.append(_strings)


# ---------------------------------------------------------------------------
# MODULE 3 — LINKED LISTS (8 lessons)
# ---------------------------------------------------------------------------

_linked = M("linked-lists", "Linked Lists", "Nodes and pointers. Reversal, fast-slow tricks, and cycle detection — pointer gymnastics that interviewers love.", [

L("singly-ll", "Singly Linked List — Nodes & Traversal",
"""## The node

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None      # pointer to next node
```

A linked list is nodes chained by `next` pointers; `head` points at the first.

## Traversal

```python
curr = head
while curr:          # stop at None
    print(curr.data)
    curr = curr.next
```

O(n) time, O(1) space — same as arrays, but **no random access**: reaching
element i costs O(i) walking.

## Arrays vs linked list (the interview one-liner)

> Arrays: O(1) access, O(n) middle insert/delete.
> Linked lists: O(n) access, O(1) insert/delete **once positioned**.
""",
[
Q("A singly linked list node stores:",
  ["data only", "data + next pointer", "data + prev + next", "index"], 1, 1,
  "One link forward — that's what 'singly' means.",
  ["TCS", "Wipro"]),
Q("Reaching the i-th element of a linked list costs:",
  ["O(1)", "O(i) — walk from head", "O(log n)", "O(n²)"], 1, 3,
  "No indexing; you follow pointers.",
  ["Infosys", "Accenture"]),
Q("Traversal loop condition is:",
  ["curr.next != None", "curr is not None", "curr.data != None", "True"], 1, 2,
  "Stop when the pointer itself is None (past the last node).",
  ["Cognizant", "TCS"]),
Q("Insert at head of linked list costs:",
  ["O(n)", "O(1)", "O(log n)", "O(n²)"], 1, 4,
  "New node points to old head; head moves. No shifting.",
  ["Amazon"]),
Q("Memory layout of linked list nodes is:",
  ["Contiguous", "Scattered — connected by pointers", "Sorted", "Stack-allocated only"], 1, 5,
  "Nodes can live anywhere; pointers hold the order.",
  ["Microsoft", "Google"]),
Q("Deleting a node when you have its pointer (singly LL) — the catch?",
  ["O(1) always", "Need the PREVIOUS node to relink; only 'delete by copying next' is O(1)",
   "Impossible", "O(log n)"], 1, 8,
  "Singly links go forward only — you can't reach the predecessor from the node itself.",
  ["Flipkart", "Amazon"]),
]),

L("doubly-ll", "Doubly Linked List — Two-Way Links",
"""## The node

```python
class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
```

Each node links **both** directions.

## Wins

- Traverse **backwards** from any node: O(1) per step.
- Delete a node given **only its pointer**: O(1) — relink `prev.next` and `next.prev`.
- Insert before a node: O(1).

## Costs

- Extra pointer per node (memory).
- More pointer updates per operation — more chances to corrupt the list (interviewers probe this!).

## The golden rule

> Every `next` assignment needs its mirror `prev` assignment. Draw the boxes-and-arrows before coding.
""",
[
Q("A doubly linked list node has:",
  ["1 pointer", "2 pointers (prev, next)", "3 pointers", "0 pointers"], 1, 2,
  "Forward and backward links.",
  ["TCS", "Infosys"]),
Q("Deleting a node given only its own pointer is O(1) in:",
  ["Singly LL", "Doubly LL", "Both", "Neither"], 1, 5,
  "Doubly: node.prev.next = node.next; node.next.prev = node.prev.",
  ["Wipro", "Accenture"]),
Q("Main cost of doubly over singly?",
  ["Slower traversal", "Extra memory per node + more pointer updates", "Can't go forward", "Needs sorting"], 1, 4,
  "One more pointer per node; every op touches twice the links.",
  ["Cognizant"]),
Q("Inserting before a known node in doubly LL is:",
  ["O(n)", "O(1)", "O(log n)", "Impossible"], 1, 6,
  "prev is directly available — no walk from head.",
  ["Amazon", "Microsoft"]),
Q("After `a.next = b` in a doubly list, you must also set:",
  ["b.prev = a", "a.prev = b", "b.next = a", "nothing"], 0, 7,
  "Mirror every link or backward traversal breaks.",
  ["Google", "Flipkart"]),
Q("LRU cache is typically built on doubly LL + hashmap because:",
  ["It's trendy", "O(1) move-to-front and O(1) evict-from-back", "Uses less memory", "It's sorted"], 1, 9,
  "Both ends need O(1) surgery — doubly links deliver.",
  ["Goldman Sachs", "Amazon"]),
]),

L("ll-insert-delete", "Insertion & Deletion — Pointer Surgery",
"""## Insert after a node

```python
new_node.next = curr.next   # 1. new node grabs the rest of the list
curr.next = new_node        # 2. curr adopts new node
```

**Order matters!** Doing step 2 first loses the rest of the list forever.

## Delete the node after curr

```python
curr.next = curr.next.next   # bypass it
```

## Insert at position i

Walk to node i-1 (O(n)), then O(1) splice. Total O(n) — the walk dominates.

## Interview mantra

> "Link first, then attach." Draw arrows; never orphan nodes.
""",
[
Q("Correct order to insert new_node after curr?",
  ["curr.next = new_node; new_node.next = curr.next", "new_node.next = curr.next; curr.next = new_node",
   "Either order", "new_node.next = curr"], 1, 4,
  "Save the old link before overwriting it, or the tail is lost.",
  ["TCS", "Infosys"]),
Q("What goes wrong if you do curr.next = new_node FIRST?",
  ["Nothing", "The rest of the list is orphaned (memory leak / lost nodes)", "Slower", "Duplicates"], 1, 5,
  "curr.next was the only handle to the remaining nodes.",
  ["Wipro", "Accenture"]),
Q("Delete node after curr:",
  ["curr.next = None", "curr.next = curr.next.next", "del curr", "curr = curr.next"], 1, 3,
  "Bypass the victim node.",
  ["Cognizant", "Amazon"]),
Q("Insert at position i in singly LL costs:",
  ["O(1)", "O(n) — walk to i-1 dominates", "O(log n)", "O(i²)"], 1, 6,
  "Splicing is O(1); finding the spot is O(n).",
  ["Microsoft"]),
Q("To delete the HEAD node:",
  ["head.next = None", "head = head.next", "del head.next", "head.data = 0"], 1, 7,
  "Move head forward; old head is dropped.",
  ["Google", "Flipkart"]),
Q("Inserting n nodes at head, one by one: total?",
  ["O(n²)", "O(n) — each insert O(1)", "O(n log n)", "O(1)"], 1, 8,
  "No walking needed for head inserts.",
  ["Goldman Sachs"]),
]),

L("ll-reversal", "Reversal — The #1 Linked List Problem",
"""## Iterative (the one you must write blindfolded)

```python
def reverse(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next   # save
        curr.next = prev  # flip
        prev = curr       # advance
        curr = nxt
    return prev           # new head
```

Three pointers, one pass: O(n) time, O(1) space.

## Recursive

```python
def reverse(head):
    if not head or not head.next: return head
    new_head = reverse(head.next)
    head.next.next = head   # flip the pair
    head.next = None
    return new_head
```

Elegant but O(n) **stack** space — mention the trade-off.

## Why interviewers love it

It tests pointer discipline with zero distractions. Follow-ups: reverse in
groups of k, reverse between positions m and n, palindrome check on LL.
""",
[
Q("Iterative LL reversal uses how many pointers?",
  ["1", "3 (prev, curr, nxt)", "n", "0"], 1, 4,
  "Save next, flip link, advance both.",
  ["TCS", "Infosys"]),
Q("After reversal, the new head is:",
  ["old head", "prev (last processed node)", "curr", "None"], 1, 5,
  "curr becomes None; prev holds the last node = new head.",
  ["Wipro", "Accenture"]),
Q("Iterative reversal space complexity?",
  ["O(n)", "O(1)", "O(log n)", "O(n²)"], 1, 3,
  "Only three pointer variables.",
  ["Cognizant", "Amazon"]),
Q("Recursive reversal's hidden cost?",
  ["Wrong answer", "O(n) call-stack space", "Slower by 10x", "Needs extra list"], 1, 6,
  "Each node adds a stack frame.",
  ["Microsoft", "Google"]),
Q("Forgetting `head.next = None` in recursive reversal causes:",
  ["Nothing", "A cycle — old head still points forward", "Crash", "Empty list"], 1, 8,
  "The original first node must become the tail (point to None).",
  ["Flipkart", "Amazon"]),
Q("Reverse LL in groups of k — core idea?",
  ["Sort first", "Reverse each k-chunk with the same 3-pointer routine, then stitch chunks",
   "Use array", "Impossible iteratively"], 1, 9,
  "It's repeated application of basic reversal plus careful stitching.",
  ["Goldman Sachs", "Microsoft"]),
]),

L("middle-fast-slow", "Middle Node — Tortoise and Hare",
"""## Two pointers, different speeds

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next        # 1 step
    fast = fast.next.next   # 2 steps
# slow is at the middle
```

When fast reaches the end, slow has covered half the distance. **O(n) time, O(1) space** — one pass, no counting.

## Even vs odd

- Odd (5 nodes): slow lands exactly on node 3.
- Even (6 nodes): slow lands on node **4** (second middle) with this loop condition.

## Where else it shines

- Palindrome check on LL (find middle, reverse second half, compare).
- Start of reordering problems.
""",
[
Q("Fast-slow middle finding takes:",
  ["Two passes", "One pass, O(n)", "O(n²)", "O(log n)"], 1, 4,
  "Fast covers 2x distance in the same loop.",
  ["TCS", "Infosys"]),
Q("6 nodes [1..6]: slow ends at?",
  ["3", "4 (second middle)", "6", "1"], 1, 6,
  "Steps: slow=2,3,4 while fast=3,5,None-stop. Know your variant!",
  ["Wipro", "Accenture"]),
Q("Loop condition `while fast and fast.next` guards against:",
  ["Infinite loop", "None.next crash on odd/even lengths", "Slow overtaking", "Nothing"], 1, 5,
  "fast.next.next would crash when fast is the last node.",
  ["Amazon", "Cognizant"]),
Q("Why not just count nodes then walk n//2?",
  ["Wrong", "Works but needs two passes; fast-slow does one", "Slower asymptotically", "Needs extra space"], 1, 7,
  "Both O(n); one pass is the elegant answer interviewers want.",
  ["Microsoft", "Google"]),
Q("Palindrome LL check strategy?",
  ["Convert to array always", "Find middle, reverse second half, compare pairwise", "Sort the list", "Hash all values"], 1, 8,
  "O(n) time, O(1) space — the expected answer.",
  ["Flipkart", "Goldman Sachs"]),
Q("If fast starts at head.next instead of head, 5-node list middle = ?",
  ["3", "2", "4", "5"], 1, 9,
  "Offset start shifts the landing: slow=1→2→3 stops when fast=None after 2 jumps… trace: (s1,f2)→(s2,f4)→(s3,fNone) → 3. Hmm — actually lands 3 as well here; the shift matters for even lengths.",
  ["Amazon"]),
]),

L("cycle-detection", "Cycle Detection — Floyd's Algorithm",
"""## The idea

Fast (2 steps) and slow (1 step) on a **cycle** must eventually meet —
like two runners on a circular track, the faster laps the slower.

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast: return True   # cycle!
return False
```

## Finding the cycle START (the hard follow-up)

1. Detect meeting point.
2. Reset slow to head; move **both one step** — they meet at the cycle's entrance.

Why: distance(head → entrance) equals distance(meeting → entrance) along the cycle. (Know the statement; deriving it live impresses.)

## Also useful for

- Finding duplicate in array (treat values as pointers — "linked list cycle" in disguise).
""",
[
Q("Floyd's cycle detection uses:",
  ["Hash set", "Two pointers at 1x and 2x speed", "Sorting", "Recursion"], 1, 4,
  "O(1) space beats the hash-set's O(n).",
  ["TCS", "Infosys"]),
Q("Why must fast and slow meet if a cycle exists?",
  ["Luck", "Relative speed 1 → fast closes the gap by 1 node per step", "They start together", "Cycles are short"], 1, 7,
  "On a loop, distance shrinks deterministically — meeting is guaranteed.",
  ["Wipro", "Accenture"]),
Q("Space complexity of Floyd's vs hash-set approach?",
  ["Same", "O(1) vs O(n)", "O(n) vs O(1)", "Both O(n)"], 1, 5,
  "Floyd's stores just two pointers.",
  ["Amazon", "Cognizant"]),
Q("After meeting, to find cycle START:",
  ["Return meeting node", "Reset one pointer to head; advance both 1 step till they meet",
   "Reverse the list", "Count nodes"], 1, 8,
  "The classic phase-2 of Floyd's.",
  ["Microsoft", "Google"]),
Q("Loop condition must check `fast and fast.next` because:",
  ["Style", "fast.next.next crashes if fast is last/None", "Slow needs it", "No reason"], 1, 6,
  "On acyclic lists fast hits the end; guard the double jump.",
  ["Flipkart"]),
Q("A 'happy number' check can use Floyd's because:",
  ["Numbers are nodes", "Digit-square sums form an implicit linked sequence that may cycle",
   "It's sorted", "No reason"], 1, 9,
  "f(n) chains like next-pointers; cycle = unhappy.",
  ["Goldman Sachs", "Amazon"]),
]),

L("merge-sorted-ll", "Merge Two Sorted Lists",
"""## Dummy-node technique

```python
def merge(a, b):
    dummy = Node(0)
    tail = dummy
    while a and b:
        if a.data <= b.data:
            tail.next, a = a, b   # attach smaller
        else:
            tail.next, b = b, a
        tail = tail.next
    tail.next = a or b            # attach remainder
    return dummy.next
```

The **dummy node** removes special-casing the head. `a or b` attaches whichever
list still has nodes.

## Complexity

O(n+m) time, O(1) extra space (rewiring, not copying).

## Why it matters beyond itself

This is the **merge step of merge sort on linked lists** — and merge sort is
the natural O(n log n) sort for LL (no random access needed, unlike quicksort).
""",
[
Q("The dummy node's purpose?",
  ["Faster", "Avoid special-casing the head pointer", "Store data", "Required by Python"], 1, 5,
  "tail starts at dummy; first real attach needs no if-head logic.",
  ["TCS", "Infosys"]),
Q("After the loop, `tail.next = a or b` works because:",
  ["Both empty", "At most one list has leftovers, already sorted", "Magic", "Lists are equal"], 1, 6,
  "One list is exhausted; the other's remainder is sorted and larger.",
  ["Wipro", "Accenture"]),
Q("Merge of two sorted LLs: time/space?",
  ["O(n+m) / O(1)", "O(n*m) / O(n)", "O(n log n) / O(n)", "O(1) / O(1)"], 0, 4,
  "Each node visited once; pointers rewired in place.",
  ["Amazon", "Cognizant"]),
Q("Why is merge sort preferred over quicksort for linked lists?",
  ["Faster always", "No random access needed; merge is O(1) space with pointers",
   "Quicksort can't sort", "Less code"], 1, 8,
  "Quicksort's partitioning needs indexing; merge sort just relinks.",
  ["Microsoft", "Google"]),
Q("Using <= vs < when equal affects:",
  ["Correctness", "Stability — <= keeps a's nodes first", "Speed", "Nothing"], 1, 7,
  "Equal keys: taking from `a` first preserves original order.",
  ["Flipkart"]),
Q("Merge k sorted lists (k lists, n total nodes) best approach?",
  ["Merge one by one O(k·n)", "Min-heap of k heads → O(n log k)", "Concatenate + sort", "Impossible"], 1, 10,
  "Heap always yields the global minimum head in log k.",
  ["Goldman Sachs", "Amazon"]),
]),

L("ll-intersection", "Intersection of Two Lists",
"""## The problem

Two lists merge into one tail (like a 'Y'). Find the intersection **node**
(by reference, not value!).

## The elegant trick

```python
p, q = headA, headB
while p != q:
    p = p.next if p else headB   # switch lanes at the end
    q = q.next if q else headA
return p
```

Riding A then B (length a+c+b) vs B then A (b+c+a) — both travel the same
distance, so they meet at the intersection. No length precomputation!

## Brute alternatives (know why they're worse)

- Hash set of A's nodes: O(n) space.
- Length difference + align: O(n) time but two passes and length code.
""",
[
Q("Intersection means the nodes are:",
  ["Equal in value", "The SAME object (shared tail)", "Adjacent", "Sorted"], 1, 4,
  "Reference equality — values may repeat elsewhere innocently.",
  ["TCS", "Infosys"]),
Q("The two-pointer lane-switch trick works because:",
  ["Luck", "Both pointers travel a+c+b, meeting at the merge point", "Lists are sorted", "Heads are equal"], 1, 8,
  "Equal total path lengths synchronise them at the intersection.",
  ["Wipro", "Accenture"]),
Q("If there's NO intersection, the loop returns:",
  ["Error", "None (both become None together)", "headA", "Infinite loop"], 1, 7,
  "Both ride a+b and hit None simultaneously → p == q == None.",
  ["Amazon", "Cognizant"]),
Q("Complexity of the trick?",
  ["O(n*m)", "O(a+b) time, O(1) space", "O(n) space", "O(log n)"], 1, 6,
  "At most two passes over each list; two pointers.",
  ["Microsoft"]),
Q("Why is comparing VALUES insufficient?",
  ["It's fine", "Duplicate values can appear before the true merge point", "Too slow", "Values are private"], 1, 5,
  "[1,2,3] & [1,2,3→shared] — value 1 matches but isn't the intersection.",
  ["Google", "Flipkart"]),
Q("Length-align method: first step?",
  ["Sort", "Compute both lengths, advance the longer head by the difference",
   "Reverse both", "Hash nodes"], 1, 9,
  "Aligned starts make a lockstep walk land together at the merge.",
  ["Goldman Sachs"]),
]),
])

MODULES.append(_linked)


# ---------------------------------------------------------------------------
# MODULE 4 — STACKS & QUEUES (7 lessons)
# ---------------------------------------------------------------------------

_sq = M("stacks-queues", "Stacks & Queues", "LIFO vs FIFO. Parentheses, monotonic stacks, and queue tricks — small structures, huge interview weight.", [

L("stack-impl", "Stack — LIFO Fundamentals",
"""## Last In, First Out

A stack is a pile of plates: push adds on top, pop removes from top.

```python
stack = []
stack.append(10)   # push
stack.append(20)
stack.pop()        # 20 (LIFO!)
stack[-1]          # peek -> 10
```

## Implementation choices

- **Python list**: amortised O(1) push/pop at the end.
- **NEVER** `pop(0)` / `insert(0)` on a list as a stack — that's O(n) shifting!
- Linked-list stack: true O(1), more code.

## What stacks are FOR

- Undo operations, backtracking
- Expression evaluation & syntax parsing
- Call stack (recursion runs on one!)
- "Most recent matters most" problems
""",
[
Q("Stack order is:",
  ["FIFO", "LIFO", "Sorted", "Random"], 1, 1,
  "Last pushed is first popped — like plates.",
  ["TCS", "Wipro"]),
Q("Python list as stack: push/pop should use:",
  ["insert(0)/pop(0)", "append()/pop() at the end", "extend()", "sort()"], 1, 3,
  "End operations are amortised O(1); front operations shift everything.",
  ["Infosys", "Accenture"]),
Q("pop(0) on a Python list costs:",
  ["O(1)", "O(n) — shifts all elements", "O(log n)", "Free"], 1, 4,
  "Everything left of the gap moves.",
  ["Cognizant"]),
Q("Peek (top without removing)) is:",
  ["O(n)", "O(1)", "O(log n)", "Impossible"], 1, 2,
  "Just read the last element.",
  ["TCS"]),
Q("Which real system uses a stack?",
  ["Print queue", "Function call stack / undo history", "Traffic light", "DNS"], 1, 5,
  "Calls nest last-in-first-out.",
  ["Amazon", "Microsoft"]),
Q("Push 1,2,3 then pop twice. Stack top is now:",
  ["3", "2", "1", "empty"], 2, 6,
  "Pops remove 3 then 2; top = 1.",
  ["Google", "Flipkart"]),
]),

L("queue-impl", "Queue — FIFO Fundamentals",
"""## First In, First Out

A queue is a line at a ticket counter: enqueue at back, dequeue from front.

```python
from collections import deque
q = deque()
q.append(10)     # enqueue
q.append(20)
q.popleft()      # 10 (FIFO!)
```

## Why deque, not list?

`list.pop(0)` is O(n). `collections.deque` is a **doubly-linked block list**:
O(1) appends AND popleft.

## Circular queue (array)

Fixed-size array with `front`/`rear` wrapping via modulo:

```
rear = (rear + 1) % capacity
```

Full vs empty ambiguity is resolved by keeping a `size` counter (or sacrificing one slot).

## What queues are FOR

- BFS, task scheduling, buffering (printer, requests)
- "Oldest matters most" problems
""",
[
Q("Queue order is:",
  ["LIFO", "FIFO", "LILO", "Sorted"], 1, 1,
  "First enqueued is first dequeued.",
  ["TCS", "Infosys"]),
Q("Why use collections.deque instead of list as a queue?",
  ["Shorter name", "O(1) popleft vs O(n) list.pop(0)", "It's sorted", "No reason"], 1, 4,
  "deque avoids the shifting cost.",
  ["Wipro", "Accenture"]),
Q("Circular queue rear update:",
  ["rear += 1", "rear = (rear+1) % capacity", "rear = 0", "rear -= 1"], 1, 5,
  "Modulo wraps around to reuse freed slots.",
  ["Cognizant", "Amazon"]),
Q("Distinguishing full vs empty in circular queue:",
  ["Impossible", "Track size (or waste one slot)", "Compare pointers only", "Use two arrays"], 1, 7,
  "front==rear means both; a counter disambiguates.",
  ["Microsoft", "Google"]),
Q("BFS uses a queue because:",
  ["It's fast", "FIFO processes nodes level by level", "Stacks overflow", "Tradition"], 1, 6,
  "Level order = oldest-discovered first.",
  ["Flipkart"]),
Q("Enqueue 5,6 then dequeue once. Front is:",
  ["5", "6", "empty", "None"], 1, 3,
  "Dequeue removed 5; front = 6.",
  ["Goldman Sachs"]),
]),

L("valid-parentheses", "Valid Parentheses — Stack's Signature Problem",
"""## The algorithm

```python
def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch in '([{':
            st.append(ch)
        else:
            if not st or st.pop() != pairs[ch]:
                return False
    return not st
```

## Why a stack?

The **most recent** opener must match the current closer — LIFO is exactly the rule.

## Three failure modes (check all!)

1. Closer with **empty** stack → `")("` invalid.
2. **Mismatched** pair → `"(]"` invalid.
3. **Leftover** openers → `"((("` invalid (`not st` check at end).

## Complexity

O(n) time, O(n) space. This pattern extends to: remove adjacent duplicates,
decode strings, asteroid collision.
""",
[
Q("'(]' is invalid because:",
  ["Too short", "Closer ] doesn't match most-recent opener (", "Stacks are slow", "No reason"], 1, 3,
  "LIFO demands the nearest unmatched opener pairs up.",
  ["TCS", "Infosys"]),
Q("Why check `not st` before pop?",
  ["Style", "Closer with empty stack (e.g. ')(') must fail, not crash", "Speed", "Python needs it"], 1, 5,
  "Popping empty stack = IndexError; logically it's invalid anyway.",
  ["Wipro", "Accenture"]),
Q("Final `return not st` catches:",
  ["Mismatches", "Leftover openers like '((('", "Empty string", "Wrong brackets"], 1, 4,
  "Every opener must be closed.",
  ["Amazon", "Cognizant"]),
Q("is_valid('') returns?",
  ["False", "True — vacuously valid", "Error", "None"], 1, 6,
  "No violations; empty stack at end.",
  ["Microsoft"]),
Q("Complexity?",
  ["O(n²)", "O(n) time, O(n) space", "O(1) space", "O(n log n)"], 1, 5,
  "One pass; stack holds at most n openers.",
  ["Google", "Flipkart"]),
Q("Minimum removals to balance '())(()'?",
  ["0", "2", "4", "6"], 1, 9,
  "Valid part '(())' uses 4 chars; remove 2.",
  ["Goldman Sachs", "Amazon"]),
]),

L("next-greater", "Next Greater Element — Monotonic Stack",
"""## The pattern

A **monotonic decreasing** stack holds candidates waiting for their "next greater":

```python
def next_greater(arr):
    res = [-1] * len(arr)
    st = []                       # indices, decreasing values
    for i, x in enumerate(arr):
        while st and arr[st[-1]] < x:
            res[st.pop()] = x     # x is their next greater
        st.append(i)
    return res
```

`[4, 5, 2, 10]` → `[5, 10, 10, -1]`

## Why O(n)?

Each index is **pushed once, popped once** — 2n operations total, despite the nested loop.

## The family

- Next greater / smaller (left or right)
- Stock span, largest rectangle in histogram
- "Daily temperatures" (LeetCode 739)

> See a "nearest bigger/smaller" problem → think monotonic stack.
""",
[
Q("Next greater of [4,5,2,10] is:",
  ["[5,10,10,-1]", "[5,2,10,-1]", "[-1,-1,-1,-1]", "[10,10,10,-1]"], 0, 5,
  "5>4, 10>5, 10>2, nothing>10.",
  ["TCS", "Infosys"]),
Q("Despite the nested while, total time is O(n) because:",
  ["n is small", "Each element pushed+popped at most once", "Python is fast", "It's actually O(n²)"], 1, 7,
  "Amortised analysis: 2n stack ops total.",
  ["Wipro", "Accenture"]),
Q("The stack stays monotonic ___ for next GREATER:",
  ["increasing", "decreasing", "constant", "random"], 1, 6,
  "Decreasing values wait; a bigger x pops all smaller ones.",
  ["Amazon", "Cognizant"]),
Q("Daily Temperatures asks for each day:",
  ["Max temp", "Days until a warmer day", "Min temp", "Average"], 1, 5,
  "Next-greater in 'days' units instead of values.",
  ["Microsoft", "Google"]),
Q("For next SMALLER element, the stack is monotonic:",
  ["decreasing", "increasing", "either", "empty"], 1, 8,
  "Mirror logic: increasing stack, pop while top > x.",
  ["Flipkart"]),
Q("[5,4,3,2,1] next greater = ?",
  ["[4,3,2,1,-1]", "[-1,-1,-1,-1,-1]", "[5,4,3,2,1]", "[1,2,3,4,5]"], 1, 9,
  "Strictly decreasing — no greater anywhere.",
  ["Goldman Sachs", "Amazon"]),
]),

L("min-stack", "Min Stack — O(1) Minimum",
"""## The trick: two stacks

```python
class MinStack:
    def __init__(self):
        self.st = []       # all values
        self.mn = []       # min-so-far at each depth
    def push(self, x):
        self.st.append(x)
        self.mn.append(x if not self.mn else min(x, self.mn[-1]))
    def pop(self):
        self.mn.pop(); return self.st.pop()
    def getMin(self):
        return self.mn[-1]   # O(1)!
```

Push 5,3,7 → mn = [5,3,3]. Pop 7 → mn top still 3. ✓

## Alternative: store pairs

Push `(x, current_min)` tuples on one stack — same idea, one structure.

## Why not just track one min variable?

Popping the minimum **loses** the previous minimum. The aux stack remembers history.

## Complexity

All operations O(1) time; O(n) extra space (the price of history).
""",
[
Q("getMin() must run in:",
  ["O(n)", "O(1)", "O(log n)", "O(n²)"], 1, 4,
  "That's the entire point of the design.",
  ["TCS", "Infosys"]),
Q("Why keep a min at EVERY stack depth (not one variable)?",
  ["Waste", "Popping the min must reveal the previous min", "Speed", "Style"], 1, 6,
  "History matters — one variable forgets.",
  ["Wipro", "Accenture"]),
Q("Push 5,3,7. mn stack = ?",
  ["[5,3,7]", "[5,3,3]", "[3,3,3]", "[7,3,5]"], 1, 5,
  "min-so-far: 5, then 3, then min(7,3)=3.",
  ["Amazon", "Cognizant"]),
Q("Pop once, then getMin?",
  ["7", "5", "3", "Error"], 2, 6,
  "Removes 7; min of [5,3] is 3.",
  ["Microsoft"]),
Q("Extra space cost?",
  ["O(1)", "O(n)", "O(log n)", "O(n²)"], 1, 7,
  "Aux stack mirrors the main one.",
  ["Google", "Flipkart"]),
Q("Single-stack variant stores:",
  ["Only values", "(value, min-so-far) pairs", "Only mins", "Strings"], 1, 8,
  "Same information, one structure.",
  ["Goldman Sachs"]),
]),

L("queue-with-stacks", "Queue Using Two Stacks",
"""## The classic

```python
class MyQueue:
    def __init__(self):
        self.inbox = []    # push here
        self.outbox = []   # pop from here
    def push(self, x):
        self.inbox.append(x)
    def pop(self):
        if not self.outbox:                       # refill only when empty
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox.pop()
```

Push: 1,2,3 → inbox=[1,2,3]. Pop → outbox=[3,2,1], returns 1. ✓ FIFO!

## Amortised O(1)

Each element moves inbox→outbox **once**. n operations = O(n) moves → amortised O(1) per op.

## The key insight

> Refill outbox **only when empty**. Refilling every pop would be O(n) per pop.

Mirror problem: **stack using two queues** (costly pop version) — know it exists.
""",
[
Q("Two stacks make a queue by:",
  ["Sorting", "inbox for push, reversed outbox for pop", "Merging", "Magic"], 1, 5,
  "Reversing twice restores FIFO order.",
  ["TCS", "Infosys"]),
Q("Push 1,2,3 then pop once. Returns?",
  ["3", "1", "2", "Error"], 1, 4,
  "FIFO: 1 first.",
  ["Wipro", "Accenture"]),
Q("Outbox is refilled:",
  ["Every pop", "Only when empty", "Every push", "Never"], 1, 6,
  "Lazy refill is what makes it amortised O(1).",
  ["Amazon", "Cognizant"]),
Q("Amortised pop cost?",
  ["O(n)", "O(1)", "O(log n)", "O(n²)"], 1, 7,
  "Each element transfers once across all pops.",
  ["Microsoft", "Google"]),
Q("peek() should:",
  ["Pop and re-push", "Refill if needed, return outbox[-1] without popping", "Return inbox[0]", "Sort"], 1, 8,
  "Same refill logic, no removal.",
  ["Flipkart"]),
Q("Stack using two queues — the expensive operation is:",
  ["push O(n)", "pop O(n) (rotate n-1 elements)", "peek O(1)", "all O(1)"], 1, 9,
  "Queues lack back-access; pop must cycle elements to reach the last pushed.",
  ["Goldman Sachs", "Amazon"]),
]),

L("deque-intro", "Deque — Double-Ended Queue",
"""## Both ends, O(1)

```python
from collections import deque
d = deque()
d.append(1); d.appendleft(0)   # [0, 1]
d.pop()        # 1  (right)
d.popleft()    # 0  (left)
```

## Superpower: sliding window maximum

Maintain a deque of **indices with decreasing values**; front is always the window max:

```python
# arr=[1,3,-1,-3,5,3,6,7], k=3 -> [3,3,5,5,6,7]
```

- Remove indices **out of window** from front.
- Remove **smaller values** from back (they can never be max).
- Front = current max. O(n) total!

## Deque vs list vs stack vs queue

> Deque does everything: stack (append/pop) + queue (append/popleft) + more.
> Python's `deque` is the default choice for BFS and windows.
""",
[
Q("Deque supports O(1):",
  ["Only right end", "Both ends", "Middle", "None"], 1, 2,
  "Double-ended by design.",
  ["TCS", "Wipro"]),
Q("Sliding window maximum is O(n) with deque because:",
  ["Deque is magic", "Each index enters/leaves once; front always holds max", "Sorting", "Windows are small"], 1, 8,
  "Monotonic decreasing indices — same family as next-greater.",
  ["Infosys", "Accenture"]),
Q("In window-max, indices leaving the window are removed from:",
  ["back", "front", "middle", "nowhere"], 1, 7,
  "Front holds oldest = potentially out-of-range.",
  ["Amazon", "Cognizant"]),
Q("Smaller values are removed from the back because:",
  ["They're ugly", "A newer, bigger value dominates them forever", "Memory", "Tradition"], 1, 8,
  "They can never become the max while the bigger value is in window.",
  ["Microsoft", "Google"]),
Q("Window max of [1,3,-1], k=3?",
  ["1", "3", "-1", "2"], 1, 5,
  "Max of the single window.",
  ["Flipkart"]),
Q("Using a list as deque (insert(0)) costs per op:",
  ["O(1)", "O(n)", "O(log n)", "O(n²)"], 1, 6,
  "Front ops shift everything — that's why deque exists.",
  ["Goldman Sachs"]),
]),
])

MODULES.append(_sq)


# ---------------------------------------------------------------------------
# MODULE 5 — TREES (10 lessons)
# ---------------------------------------------------------------------------

_trees = M("trees", "Trees", "Binary trees, BSTs, traversals, and LCA — recursion's favourite playground and a placement staple.", [

L("tree-basics", "Tree Basics — Nodes, Root, Height",
"""## Terminology (interviewers test vocabulary!)

- **Root**: top node, no parent.
- **Leaf**: node with no children.
- **Height**: longest path edges from node to a leaf. (Some define in nodes — clarify!)
- **Depth**: edges from root to the node.
- **Subtree**: a node + all its descendants.

```
        A(depth 0)
       / \\
      B   C
     /     \\
    D       E   <- leaves
Height of A = 2 (edges). Height of leaf = 0.
```

## Why trees?

Hierarchies (file systems, org charts), searching (BST), parsing (ASTs),
priority (heaps). Contiguous arrays can't branch — trees can.

## Key property

A tree with n nodes has exactly **n-1 edges** (connected, acyclic).
""",
[
Q("A tree with n nodes has how many edges?",
  ["n", "n-1", "n+1", "2n"], 1, 3,
  "Connected + acyclic ⟹ exactly n-1.",
  ["TCS", "Infosys"]),
Q("Height of a single-node tree (edge-counting)?",
  ["1", "0", "-1", "undefined"], 1, 2,
  "No edges to any leaf.",
  ["Wipro", "Accenture"]),
Q("Depth of root?",
  ["1", "0", "-1", "n"], 1, 2,
  "Zero edges from root to itself.",
  ["Cognizant"]),
Q("A leaf node has:",
  ["Two children", "No children", "One parent only", "No parent"], 1, 1,
  "Definition of leaf.",
  ["TCS"]),
Q("If height is counted in NODES, single node height = ?",
  ["0", "1", "-1", "2"], 1, 5,
  "Node-counting = edge-counting + 1. Always clarify which!",
  ["Amazon", "Microsoft"]),
Q("Maximum nodes at depth d in a binary tree?",
  ["d", "2^d", "d²", "2d"], 1, 7,
  "Level d can hold at most 2^d nodes (root depth 0 → 1).",
  ["Google", "Flipkart"]),
]),

L("binary-tree", "Binary Tree Properties",
"""## Definitions

- **Binary tree**: each node has ≤ 2 children (left, right).
- **Full**: every node has 0 or 2 children.
- **Complete**: all levels full except last, filled left-to-right (heap shape!).
- **Perfect**: all levels completely full.

## The numbers

- Perfect tree of height h (edges): **2^(h+1) − 1** nodes.
- Height h binary tree holds **at most** 2^(h+1)−1, **at least** h+1 nodes (a chain).
- Minimum height for n nodes: **floor(log₂n)** — the balanced case.

## Representation

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right
```

Arrays can store complete trees: children of index i at **2i+1, 2i+2** (heaps use this).
""",
[
Q("A perfect binary tree of height 2 (edges) has how many nodes?",
  ["6", "7", "8", "4"], 1, 5,
  "2^(2+1)-1 = 7.",
  ["TCS", "Infosys"]),
Q("In a complete tree, the last level is:",
  ["Empty", "Filled left to right", "Filled right to left", "Full"], 1, 4,
  "That's the definition distinguishing complete from perfect.",
  ["Wipro", "Accenture"]),
Q("Array index of left child of node at index i (0-based)?",
  ["2i", "2i+1", "2i+2", "i//2"], 1, 6,
  "Heap indexing: left=2i+1, right=2i+2.",
  ["Amazon", "Cognizant"]),
Q("Minimum possible height (edges) of a binary tree with 8 nodes?",
  ["7", "3", "4", "2"], 1, 7,
  "floor(log₂8) = 3 — the balanced shape.",
  ["Microsoft", "Google"]),
Q("A 'full' binary tree means:",
  ["All levels full", "Every node has 0 or 2 children", "Complete", "Has n nodes"], 1, 5,
  "Full ≠ perfect ≠ complete — keep them straight.",
  ["Flipkart"]),
Q("Maximum nodes in a binary tree of height 3 (edges)?",
  ["8", "15", "16", "7"], 1, 8,
  "2^(3+1)-1 = 15 (perfect tree).",
  ["Goldman Sachs", "Amazon"]),
]),

L("inorder-traversal", "Inorder Traversal — Left, Root, Right",
"""## The pattern

```python
def inorder(root):
    if not root: return
    inorder(root.left)
    print(root.val)      # visit
    inorder(root.right)
```

For the tree `4(2(1,3),6(5,7))`, inorder prints **1 2 3 4 5 6 7**.

## The magic property

> Inorder of a **BST** yields keys in **sorted order**.

That's not true for arbitrary binary trees — only BSTs.

## Complexity

O(n) time (visit each once), O(h) stack space (h = height; O(n) worst-case chain, O(log n) balanced).

## Iterative version

Uses an explicit stack: push left spine, pop-visit-go-right. Know it exists;
interviewers sometimes demand "no recursion".
""",
[
Q("Inorder order is:",
  ["Root, Left, Right", "Left, Root, Right", "Left, Right, Root", "Right, Root, Left"], 1, 2,
  "Left subtree, then node, then right.",
  ["TCS", "Wipro"]),
Q("Inorder of a BST gives:",
  ["Random order", "Sorted ascending", "Sorted descending", "Level order"], 1, 4,
  "Left < root < right recursively ⟹ sorted.",
  ["Infosys", "Accenture"]),
Q("Recursive inorder space?",
  ["O(1)", "O(h) call stack", "O(n²)", "O(log n) always"], 1, 5,
  "Deepest path = height h.",
  ["Amazon", "Cognizant"]),
Q("Inorder of 4(2(1,3),6(5,7)) — third printed?",
  ["1", "2", "3", "4"], 2, 6,
  "Sequence: 1,2,3,4,5,6,7 — third is 3.",
  ["Microsoft"]),
Q("To validate a BST, inorder + check:",
  ["Anything", "Strictly increasing sequence", "Decreasing", "All equal"], 1, 7,
  "BST ⟺ inorder sorted (strict, no duplicates).",
  ["Google", "Flipkart"]),
Q("Iterative inorder needs:",
  ["Queue", "Explicit stack simulating the call stack", "Hash map", "Two stacks"], 1, 8,
  "Push left spine; pop, visit, go right.",
  ["Goldman Sachs"]),
]),

L("pre-post-traversal", "Preorder & Postorder",
"""## The three orders (same skeleton, visit moves!)

```python
def preorder(root):            # ROOT first
    if not root: return
    print(root.val); preorder(root.left); preorder(root.right)

def postorder(root):           # ROOT last
    if not root: return
    postorder(root.left); postorder(root.right); print(root.val)
```

Tree `1(2(4,5),3)`: preorder → **1 2 4 5 3**; postorder → **4 5 2 3 1**.

## What each is FOR

- **Preorder**: copy/serialize a tree (root first rebuilds top-down).
- **Postorder**: delete a tree safely (children before parent!); evaluate expression trees.
- **Inorder**: BST sorting.

## Memory hook

> **Pre** = parent before children. **Post** = parent after children. **In** = parent in the middle.
""",
[
Q("Preorder visits:",
  ["Left, Root, Right", "Root, Left, Right", "Left, Right, Root", "Root, Right, Left"], 1, 2,
  "Root first.",
  ["TCS", "Infosys"]),
Q("Postorder of 1(2(4,5),3)?",
  ["1 2 4 5 3", "4 5 2 3 1", "4 2 5 1 3", "1 2 3 4 5"], 1, 4,
  "Children before parent, left before right.",
  ["Wipro", "Accenture"]),
Q("To DELETE a tree safely (free children first), use:",
  ["Preorder", "Postorder", "Inorder", "Level order"], 1, 5,
  "Never free a parent while children point to it.",
  ["Amazon", "Cognizant"]),
Q("Serializing a tree for reconstruction typically uses:",
  ["Inorder alone", "Preorder (+ markers for None)", "Postorder alone", "Any single traversal"], 1, 7,
  "Inorder alone is ambiguous; preorder with null markers rebuilds uniquely.",
  ["Microsoft", "Google"]),
Q("Expression tree '3 + 4 * 5' evaluates via:",
  ["Preorder", "Postorder (children = operands first)", "Inorder", "BFS"], 1, 6,
  "Compute subexpressions before applying the operator.",
  ["Flipkart"]),
Q("Preorder 1,2,4,5,3 — position of 5?",
  ["3rd", "4th", "5th", "2nd"], 1, 8,
  "1(1st) 2(2nd) 4(3rd) 5(4th) 3(5th).",
  ["Goldman Sachs"]),
]),

L("level-order", "Level Order — BFS on Trees",
"""## Breadth-first with a queue

```python
from collections import deque
def level_order(root):
    if not root: return []
    q, out = deque([root]), []
    while q:
        node = q.popleft()
        out.append(node.val)
        if node.left: q.append(node.left)
        if node.right: q.append(node.right)
    return out
```

`1(2(4,5),3)` → **[1, 2, 3, 4, 5]**.

## Level-by-level (the useful variant)

```python
while q:
    level_size = len(q)          # snapshot BEFORE the loop
    level = []
    for _ in range(level_size):
        node = q.popleft()
        ...
```

Snapshotting `len(q)` separates levels — needed for zigzag, averages, right view.

## Complexity

O(n) time, O(w) space where w = max width (up to n/2 on last level).
""",
[
Q("Level order uses:",
  ["Stack", "Queue", "Recursion only", "Hash map"], 1, 3,
  "FIFO processes level by level.",
  ["TCS", "Wipro"]),
Q("Level order of 1(2(4,5),3)?",
  ["1 2 4 5 3", "1 2 3 4 5", "4 5 2 3 1", "1 3 2 5 4"], 1, 4,
  "All of level 0, then level 1, then level 2.",
  ["Infosys", "Accenture"]),
Q("Why snapshot `len(q)` before the inner loop?",
  ["Speed", "To process exactly one level per iteration", "Memory", "Style"], 1, 6,
  "q grows as children enqueue; the snapshot freezes the level boundary.",
  ["Amazon", "Cognizant"]),
Q("Space is O(w), w = max width, because:",
  ["Queue holds a whole level at once", "Recursion", "It stores values twice", "No reason"], 0, 7,
  "The widest level sits in the queue simultaneously.",
  ["Microsoft", "Google"]),
Q("Zigzag traversal alternates direction per level — needs:",
  ["Two stacks or level lists reversed", "Sorting", "DFS", "Hashing"], 0, 8,
  "Collect each level, reverse alternate ones.",
  ["Flipkart", "Amazon"]),
Q("Right view of 1(2(4,5),3)?",
  ["1 2 4", "1 3 5", "1 2 3", "5 3 1"], 1, 9,
  "Last node of each level: 1 | 3 | 5.",
  ["Goldman Sachs", "Microsoft"]),
]),

L("height-depth-tree", "Height & Depth — Recursion on Trees",
"""## Height (edges to deepest leaf)

```python
def height(root):
    if not root: return -1      # empty = -1 (edges convention)
    return 1 + max(height(root.left), height(root.right))
```

Single node → 0. Empty → -1.

## Depth of a node

Pass depth down as a parameter:

```python
def max_depth_param(root, d=0):
    if not root: return d - 1 ...
```

Or compute depth during traversal.

## Diameter (famous hard follow-up)

Longest path between ANY two nodes — may not pass through root!

```python
def diameter(root):
    best = 0
    def h(node):
        nonlocal best
        if not node: return -1
        l, r = h(node.left), h(node.right)
        best = max(best, l + r + 2)   # path through this node
        return 1 + max(l, r)
    h(root); return best
```

Postorder computes heights bottom-up while tracking the best through-path.
""",
[
Q("height() returns -1 for empty tree because:",
  ["Bug", "Edge-convention: single node = 0", "It's faster", "Avoids None"], 1, 3,
  "Consistent base: leaf = 1 + max(-1,-1) = 0.",
  ["TCS", "Infosys"]),
Q("Diameter of a tree is:",
  ["Height of root", "Longest path between any two nodes", "Number of leaves", "Depth × 2"], 1, 6,
  "It may pass through any node, not necessarily root.",
  ["Wipro", "Accenture"]),
Q("In diameter code, `l + r + 2` counts:",
  ["Nodes", "Edges on the path through this node", "Leaves", "Height"], 1, 7,
  "Left height + right height + 2 connecting edges.",
  ["Amazon", "Cognizant"]),
Q("Balanced-tree check needs height of subtrees to differ by at most:",
  ["0", "1", "2", "n"], 1, 5,
  "AVL-style balance condition.",
  ["Microsoft"]),
Q("Naive diameter (height() per node) is O(n²); the trick is:",
  ["Sorting", "Single postorder computing height AND updating best", "BFS", "Memoization"], 1, 8,
  "One traversal does both jobs.",
  ["Google", "Flipkart"]),
Q("Height of a chain of 5 nodes (edges)?",
  ["5", "4", "3", "0"], 1, 2,
  "4 edges between 5 nodes.",
  ["Goldman Sachs"]),
]),

L("bst-basics", "BST Basics — The Ordered Tree",
"""## The BST property

For EVERY node: **left subtree keys < node key < right subtree keys**.

```
      4
    /   \\
   2     6
  / \\   / \\
 1   3 5   7     <- valid BST
```

## What it buys

- Search / insert / delete: **O(h)** — O(log n) if balanced, O(n) if skewed.
- Min: go left till None. Max: go right till None.
- Inorder = sorted.

## What it does NOT guarantee

Balance! Inserting 1,2,3,4,5 gives a **chain** (a linked list in disguise) —
O(n) operations. Self-balancing trees (AVL, Red-Black) fix this.
""",
[
Q("BST property:",
  ["Left > root > right", "Left < root < right (entire subtrees)", "Children equal root", "No order"], 1, 3,
  "The WHOLE left subtree is smaller, not just the child.",
  ["TCS", "Wipro"]),
Q("Minimum in BST is found by:",
  ["Going right", "Going left till None", "Root", "Random walk"], 1, 2,
  "Leftmost = smallest.",
  ["Infosys", "Accenture"]),
Q("Inserting sorted 1..n into a plain BST gives:",
  ["Balanced tree", "A chain — O(n) height", "Complete tree", "Error"], 1, 5,
  "Each insert goes right forever. This is WHY balanced BSTs exist.",
  ["Amazon", "Cognizant"]),
Q("Search in a balanced BST of n nodes:",
  ["O(n)", "O(log n)", "O(1)", "O(n log n)"], 1, 4,
  "Halve the candidates each level — like binary search on a tree.",
  ["Microsoft", "Google"]),
Q("Which is NOT a valid BST? root 5: left 3(2,4), right 7(6,8) vs left 3(2,6)",
  ["First", "Second — 6 in left subtree > 5", "Both", "Neither"], 1, 6,
  "Subtree-wide property: 6 > 5 violates it despite 3 < 5.",
  ["Flipkart", "Amazon"]),
Q("Inorder successor of a node WITH a right subtree is:",
  ["Parent", "Leftmost of right subtree", "Rightmost", "Root"], 1, 8,
  "Smallest key bigger than node.",
  ["Goldman Sachs", "Microsoft"]),
]),

L("bst-search-insert", "BST Search & Insert",
"""## Search

```python
def search(root, key):
    while root:
        if key == root.val: return root
        root = root.left if key < root.val else root.right
    return None
```

## Insert (iterative shape)

Walk down till None, attach the new node as a leaf. Duplicates: convention
says ignore / go right / count — **state your choice** in interviews.

## Delete (the hard one — 3 cases)

1. **Leaf**: remove it.
2. **One child**: bypass with the child.
3. **Two children**: replace with **inorder successor** (min of right), then delete the successor.

Case 3 is the interview favourite — practice it on paper.

## Complexity

All O(h). Balanced → O(log n).
""",
[
Q("BST search moves left when:",
  ["key > node", "key < node", "always", "never"], 1, 2,
  "Smaller keys live left.",
  ["TCS", "Infosys"]),
Q("New nodes are inserted as:",
  ["Root", "Leaves", "Left child always", "Random"], 1, 3,
  "Walk down to the empty spot.",
  ["Wipro", "Accenture"]),
Q("Deleting a node with TWO children: replace with?",
  ["Left child", "Inorder successor (min of right subtree)", "Parent", "Any leaf"], 1, 6,
  "Successor preserves the BST property; then delete the duplicate successor.",
  ["Amazon", "Cognizant"]),
Q("Deleting a LEAF node:",
  ["Complex", "Just unlink it (parent pointer → None)", "Rebalance", "Impossible"], 1, 4,
  "No children to reattach.",
  ["Microsoft"]),
Q("Duplicate insert — best interview answer?",
  ["Crash", "State a convention (ignore/count/right) explicitly", "Always overwrite", "Sort first"], 1, 7,
  "Interviewers test whether you notice the ambiguity.",
  ["Google", "Flipkart"]),
Q("Build BST from [5,3,7,2,4]: root's left subtree = ?",
  ["[3,2,4]", "[7]", "[2,4]", "[5]"], 0, 8,
  "3 goes left; 2 left of 3; 4 right of 3; 7 right of 5.",
  ["Goldman Sachs"]),
]),

L("lca-trees", "LCA — Lowest Common Ancestor",
"""## In a BST (easy — use order!)

```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root      # split point!
```

The first node where p and q **diverge** is the LCA. O(h).

## In a general binary tree (recursive)

```python
def lca(root, p, q):
    if not root or root in (p, q): return root
    l, r = lca(root.left, p, q), lca(root.right, p, q)
    if l and r: return root      # p and q split here
    return l or r               # bubble up the found one
```

## Intuition

> LCA = the deepest node that has p in one subtree and q in the other
> (or is p/q itself).
""",
[
Q("LCA of 2 and 8 in BST 4(2(1,3),6(5,7→8))?",
  ["2", "4", "6", "8"], 1, 4,
  "2 < 4 < 8 → they split at root 4.",
  ["TCS", "Infosys"]),
Q("BST LCA trick relies on:",
  ["Tree height", "Order property to choose direction", "Hashing", "Sorting nodes"], 1, 6,
  "Both smaller → left; both bigger → right; else split = answer.",
  ["Wipro", "Accenture"]),
Q("General binary-tree LCA returns root when:",
  ["Always", "l and r both non-null (p,q split across subtrees)", "Never", "Tree is empty"], 1, 7,
  "Split point = lowest common.",
  ["Amazon", "Cognizant"]),
Q("If root IS p (or q), LCA(p,q) = ?",
  ["q", "p itself", "parent", "None"], 1, 6,
  "A node is its own ancestor (base case).",
  ["Microsoft", "Google"]),
Q("BST LCA time?",
  ["O(n)", "O(h)", "O(1)", "O(n²)"], 1, 3,
  "One root-to-leaf walk.",
  ["Flipkart"]),
Q("LCA(1,3) in 4(2(1,3),6)?",
  ["4", "2", "1", "6"], 1, 8,
  "Both under 2 → LCA is 2.",
  ["Goldman Sachs", "Amazon"]),
]),

L("tree-views", "Tree Views — Right, Top & Beyond",
"""## Right view

Nodes visible from the right: **last node of each level**.

```python
# level-order, take last per level  ->  [1, 3, 5] for 1(2(4,5),3)
```

Or DFS going **right-first**, recording first visit per depth.

## Top view

Nodes visible from above: first node at each **horizontal distance**.
- hd(root) = 0; left child hd-1; right child hd+1.
- BFS; keep first-seen per hd; output sorted by hd.

## Left / bottom views

- Left view: first per level (or right-first DFS → last per depth… careful!).
- Bottom view: LAST per horizontal distance (deepest wins).

## Interview tip

> All "views" = BFS/DFS + "which node wins each slot". Name the slot rule first, code second.
""",
[
Q("Right view of 1(2(4,5),3)?",
  ["1 2 4", "1 3 5", "1 2 3", "5 3 1"], 1, 4,
  "Rightmost per level.",
  ["TCS", "Infosys"]),
Q("Right-first DFS records per depth the:",
  ["Last visit", "First visit (= rightmost)", "All visits", "None"], 1, 7,
  "Right subtree visited first → first-seen is rightmost.",
  ["Wipro", "Accenture"]),
Q("Top view uses:",
  ["Depth", "Horizontal distance, first-seen wins", "Values", "Height"], 1, 8,
  "BFS top-down: first node at each hd blocks those below.",
  ["Amazon", "Cognizant"]),
Q("Bottom view differs from top view by:",
  ["Direction", "LAST per hd wins (deepest)", "Using DFS", "Nothing"], 1, 8,
  "Deepest node at each horizontal distance.",
  ["Microsoft", "Google"]),
Q("Left view of 1(2(4,5),3)?",
  ["1 3 5", "1 2 4", "1 2 3", "4 5 3"], 1, 5,
  "Leftmost per level.",
  ["Flipkart"]),
Q("Vertical order traversal groups nodes by:",
  ["Depth", "Horizontal distance, then depth, then value", "Level", "Random"], 1, 9,
  "LeetCode 987's exact tie-breaking rule.",
  ["Goldman Sachs", "Amazon"]),
]),
])

MODULES.append(_trees)


# ---------------------------------------------------------------------------
# MODULE 6 — GRAPHS (8 lessons)
# ---------------------------------------------------------------------------

_graphs = M("graphs", "Graphs", "BFS, DFS, cycles, and shortest paths — the module that separates good from great in interviews.", [

L("graph-repr", "Graph Representation — List vs Matrix",
"""## The choices

**Adjacency list** (default!):
```python
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0],
    3: [1],
}
```

**Adjacency matrix**: n×n grid, `mat[u][v] = 1` if edge exists.

## Comparison

| | List | Matrix |
|---|---|---|
| Space | O(V + E) | O(V²) |
| Neighbours of u | O(degree) | O(V) scan row |
| Edge exists? | O(degree) | O(1) |
| Best for | Sparse graphs | Dense / tiny graphs |

## Directed vs undirected

- Undirected edge u–v: add **both** directions.
- Directed edge u→v: add **one** direction.

Forgetting the reverse edge in undirected graphs is the #1 implementation bug.
""",
[
Q("Adjacency list space for V vertices, E edges?",
  ["O(V²)", "O(V + E)", "O(E)", "O(V*E)"], 1, 3,
  "One entry per vertex + one per edge.",
  ["TCS", "Infosys"]),
Q("Checking 'is there an edge u→v' is O(1) in:",
  ["Adjacency list", "Adjacency matrix", "Both", "Neither"], 1, 4,
  "Matrix lookup mat[u][v] is direct.",
  ["Wipro", "Accenture"]),
Q("Undirected edge (u,v) in adjacency list needs:",
  ["v in list[u] only", "Both: v in list[u] AND u in list[v]", "Nothing", "A matrix"], 1, 5,
  "Undirected = two directed arcs. Forgetting one breaks traversal.",
  ["Amazon", "Cognizant"]),
Q("Sparse graph (E << V²) → prefer:",
  ["Matrix", "Adjacency list", "Edge list only", "Tree"], 1, 6,
  "Matrix wastes V² space on zeros.",
  ["Microsoft", "Google"]),
Q("Listing all neighbours of u costs O(degree) in:",
  ["Matrix", "Adjacency list", "Both", "Neither"], 1, 7,
  "List stores exactly the neighbours.",
  ["Flipkart"]),
Q("V=1000, E=2000. Matrix wastes roughly:",
  ["Nothing", "~1M cells for 2K edges", "2K cells", "V+E cells"], 1, 8,
  "10⁶ cells vs 3K entries — lists win big on sparse graphs.",
  ["Goldman Sachs", "Amazon"]),
]),

L("bfs-graph", "BFS — Level by Level",
"""## The algorithm

```python
from collections import deque
def bfs(graph, start):
    seen = {start}
    q = deque([start])
    while q:
        u = q.popleft()
        print(u)
        for v in graph[u]:
            if v not in seen:
                seen.add(v)      # mark WHEN enqueuing!
                q.append(v)
```

## The critical detail

> Mark visited **when you enqueue**, not when you dequeue — otherwise the same
> node enters the queue many times (exponential blowup on dense graphs).

## What BFS gives

- Visits in **increasing distance** from start.
- Shortest path (fewest edges) in **unweighted** graphs.
- Level-order of trees is just BFS.

## Complexity

O(V + E): each vertex enqueued once, each edge examined twice (undirected).
""",
[
Q("BFS uses:",
  ["Stack", "Queue", "Recursion", "Heap"], 1, 2,
  "FIFO → level order.",
  ["TCS", "Wipro"]),
Q("Mark visited when?",
  ["Dequeuing", "Enqueuing — prevents duplicate queue entries", "At the end", "Never"], 1, 6,
  "Late marking lets neighbours re-add the same node repeatedly.",
  ["Infosys", "Accenture"]),
Q("BFS from a node visits others in order of:",
  ["Value", "Distance (edges) from start", "Insertion", "Random"], 1, 5,
  "That's why it finds shortest paths in unweighted graphs.",
  ["Amazon", "Cognizant"]),
Q("BFS shortest path works on:",
  ["Weighted graphs", "Unweighted graphs", "Only trees", "Directed only"], 1, 6,
  "Weights need Dijkstra; BFS counts edges.",
  ["Microsoft", "Google"]),
Q("Time complexity?",
  ["O(V*E)", "O(V + E)", "O(V²)", "O(E log V)"], 1, 4,
  "Each vertex once, each edge twice.",
  ["Flipkart"]),
Q("0-1 BFS (edges weight 0/1) uses:",
  ["Normal queue", "Deque: 0-weight to front, 1-weight to back", "Stack", "Heap"], 1, 9,
  "0-1 BFS trick — Dijkstra with deque instead of heap.",
  ["Goldman Sachs", "Amazon"]),
]),

L("dfs-graph", "DFS — Go Deep First",
"""## Recursive (natural fit)

```python
def dfs(graph, u, seen):
    seen.add(u)
    print(u)
    for v in graph[u]:
        if v not in seen:
            dfs(graph, v, seen)
```

## Iterative

Explicit stack; push neighbours. (Order differs slightly from recursive — fine.)

## What DFS gives

- Explores one path to its end before backtracking.
- **Cycle detection**, topological sort, connected components, path existence.
- Preorder of trees is just DFS.

## BFS vs DFS (the interview question)

| | BFS | DFS |
|---|---|---|
| Structure | Queue | Stack/recursion |
| Best for | Shortest path (unweighted) | Cycles, topo sort, exhaustive search |
| Memory | O(width) | O(depth) |

> "Need shortest path? BFS. Need to explore/detect structure? DFS."
""",
[
Q("DFS naturally uses:",
  ["Queue", "Stack / recursion", "Heap", "Deque"], 1, 2,
  "Go deep = last-discovered first.",
  ["TCS", "Infosys"]),
Q("Iterative DFS order vs recursive DFS order:",
  ["Identical always", "May differ (neighbour push order), both valid", "Iterative is wrong", "Recursive is wrong"], 1, 6,
  "Traversal order isn't unique; either is a valid DFS.",
  ["Wipro", "Accenture"]),
Q("DFS is better than BFS for:",
  ["Shortest path", "Cycle detection / topological sort", "Level order", "Nothing"], 1, 5,
  "Deep exploration reveals structure.",
  ["Amazon", "Cognizant"]),
Q("Recursion depth on a path graph of 10⁵ nodes:",
  ["Fine", "RecursionError — use iterative or sys.setrecursionlimit", "O(1)", "Faster"], 1, 7,
  "Python's default limit ~1000 frames.",
  ["Microsoft", "Google"]),
Q("DFS memory is O(depth) because:",
  ["It stores all nodes", "Stack holds the current path", "Queue is big", "Hashing"], 1, 6,
  "Only the active path sits on the stack.",
  ["Flipkart"]),
Q("Finding ANY path between two nodes: simplest?",
  ["Dijkstra", "DFS/BFS reachability", "Floyd-Warshall", "Bellman-Ford"], 1, 8,
  "Unweighted reachability needs no shortest-path machinery.",
  ["Goldman Sachs"]),
]),

L("connected-components", "Connected Components — Counting Islands",
"""## The pattern

```python
def count_components(graph, n):
    seen, comp = set(), 0
    for u in range(n):
        if u not in seen:
            comp += 1
            dfs(graph, u, seen)   # flood this island
    return comp
```

Each DFS floods one island; unvisited start = new island. **O(V+E)**.

## "Number of islands" (grid version)

Same idea on a 2D grid: treat cells as nodes, 4-directional neighbours as edges.
Flood-fill with DFS/BFS, sink visited land ('1' → '0').

```python
# directions: (1,0),(-1,0),(0,1),(0,-1)
```

## Variations

- **Provinces** (adjacency matrix version).
- **Friend circles**, **connected groups** — same skeleton, different story.
- Count **sizes** of components: track flood size.
""",
[
Q("A connected component is:",
  ["One node", "Maximal set of mutually reachable nodes", "A cycle", "A tree"], 1, 4,
  "Maximal = can't add any more connected nodes.",
  ["TCS", "Wipro"]),
Q("Counting components: outer loop over all vertices is needed because:",
  ["Speed", "Graph may be disconnected — DFS from one start misses islands", "Style", "Sorting"], 1, 5,
  "Each unvisited vertex starts a new flood.",
  ["Infosys", "Accenture"]),
Q("'Number of islands' treats grid cells as:",
  ["Sorted", "Graph nodes with 4-directional edges", "Trees", "Arrays"], 1, 6,
  "Same flood algorithm on an implicit graph.",
  ["Amazon", "Cognizant"]),
Q("Sinking visited land ('1'→'0') replaces:",
  ["BFS", "The seen-set", "DFS", "Counting"], 1, 7,
  "Mutating the grid marks visited in-place: O(1) extra space.",
  ["Microsoft", "Google"]),
Q("8-directional islands vs 4-directional differ in:",
  ["Nothing", "Neighbour list (diagonals count or not)", "Speed", "Answer always"], 1, 8,
  "Read the problem statement carefully!",
  ["Flipkart", "Amazon"]),
Q("Largest island = track:",
  ["Count of floods", "Size of each flood, keep max", "Depths", "Nothing"], 1, 7,
  "Same skeleton, accumulate size per component.",
  ["Goldman Sachs"]),
]),

L("cycle-undirected", "Cycle Detection in Undirected Graphs",
"""## DFS with parent tracking

```python
def has_cycle(graph, u, seen, parent):
    seen.add(u)
    for v in graph[u]:
        if v not in seen:
            if has_cycle(graph, v, seen, u): return True
        elif v != parent:
            return True      # visited AND not the way we came = cycle
    return False
```

## The parent trick

In undirected graphs, every edge looks like a "back edge" to its parent —
`v != parent` filters out the trivial one.

## Directed graphs differ!

Need 3 colours: **white** (unvisited), **gray** (in current stack), **black** (done).
A gray neighbour = real cycle. (Undirected parent-trick doesn't apply.)

## Union-Find alternative

Process edges; if `union(u,v)` finds them already connected → cycle. O(E·α(V)).
""",
[
Q("In undirected DFS cycle check, `v != parent` exists because:",
  ["Speed", "The edge back to parent isn't a cycle", "Style", "Parent is special"], 1, 7,
  "Without it, every edge reports a false cycle.",
  ["TCS", "Infosys"]),
Q("Directed cycle detection needs:",
  ["Parent pointer", "3 colours (white/gray/black)", "Two parents", "Nothing extra"], 1, 8,
  "Gray = in current DFS stack; revisiting gray = true cycle.",
  ["Wipro", "Accenture"]),
Q("Union-Find detects a cycle when union(u,v) finds:",
  ["New nodes", "u and v already in the same set", "Empty set", "Nothing"], 1, 7,
  "An edge inside one component closes a loop.",
  ["Amazon", "Cognizant"]),
Q("A tree with n nodes and n-1 edges has cycles:",
  ["Many", "Zero — that's the definition", "One", "n"], 1, 5,
  "Acyclic + connected = tree.",
  ["Microsoft"]),
Q("Self-loop (u→u) is a cycle in:",
  ["Neither", "Both directed and undirected detection", "Only directed", "Only undirected"], 1, 8,
  "v == u is visited and (undirected: v != parent holds) → detected.",
  ["Google", "Flipkart"]),
Q("Course Schedule (can finish?) reduces to:",
  ["Sorting", "Directed cycle detection", "BFS shortest path", "Counting"], 1, 9,
  "Prerequisite cycle = impossible schedule.",
  ["Goldman Sachs", "Amazon"]),
]),

L("topo-sort", "Topological Sort — Ordering with Dependencies",
"""## The problem

Order tasks so every prerequisite comes first. Only possible on **DAGs**
(Directed Acyclic Graphs).

## Kahn's algorithm (BFS, indegree)

```python
from collections import deque
def topo(n, edges):
    indeg = [0]*n
    g = [[] for _ in range(n)]
    for u, v in edges:       # u -> v (u before v)
        g[u].append(v); indeg[v] += 1
    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return order if len(order) == n else []   # [] = cycle!
```

## Key facts

- Result **not unique** — many valid orders.
- `len(order) < n` ⟺ **cycle exists** (some indegrees never hit 0).
- DFS variant: postorder reversed.

## Uses

Build systems, course schedules, task pipelines, spreadsheet recalculation.
""",
[
Q("Topological sort is possible only on:",
  ["Any graph", "DAGs (directed acyclic)", "Undirected graphs", "Trees only"], 1, 4,
  "Cycles make 'prerequisite first' impossible.",
  ["TCS", "Infosys"]),
Q("Kahn's starts with nodes of indegree:",
  ["Max", "0 — no prerequisites", "1", "Any"], 1, 5,
  "Only prerequisite-free tasks can go first.",
  ["Wipro", "Accenture"]),
Q("If topo order has fewer than n nodes:",
  ["Bug", "A cycle exists", "Graph is empty", "It's fine"], 1, 6,
  "Cycle nodes never reach indegree 0.",
  ["Amazon", "Cognizant"]),
Q("Topological order is:",
  ["Unique", "Not necessarily unique", "Sorted", "Random"], 1, 5,
  "Independent tasks can interleave freely.",
  ["Microsoft", "Google"]),
Q("Edge u→v means in Kahn's:",
  ["v before u", "u before v; indeg[v] += 1", "u equals v", "Nothing"], 1, 7,
  "Direction = dependency direction.",
  ["Flipkart"]),
Q("DFS-based topo sort outputs:",
  ["Preorder", "Postorder reversed", "Inorder", "BFS order"], 1, 8,
  "A node finishes only after its dependents… reversed gives prerequisites first.",
  ["Goldman Sachs", "Amazon"]),
]),

L("dijkstra-intro", "Dijkstra — Shortest Path Concepts",
"""## The problem

Shortest path from a source in a graph with **non-negative** weights.

## The idea (not full code — the *concept*)

1. Keep best-known distance to each node (source = 0, rest = ∞).
2. Repeatedly pick the **unvisited node with smallest distance** (min-heap!).
3. **Relax** its edges: `dist[v] = min(dist[v], dist[u] + w)`.
4. A node popped from the heap is **final** — no shorter path can exist
   (non-negative weights guarantee this).

## Complexity

O((V + E) log V) with a binary heap.

## Critical limits

- **Negative weights**: Dijkstra FAILS (the 'final when popped' guarantee breaks). Use Bellman-Ford.
- **Negative cycle**: no shortest path exists (loop forever decreasing).
- Unweighted: BFS is simpler and faster.

## Interview line

> "Non-negative weights → Dijkstra. Negative weights → Bellman-Ford. Unweighted → BFS."
""",
[
Q("Dijkstra requires edge weights to be:",
  ["Any", "Non-negative", "Positive integers only", "Equal"], 1, 3,
  "Negative edges break the 'popped = final' guarantee.",
  ["TCS", "Infosys"]),
Q("The min-heap always extracts:",
  ["Random node", "Unvisited node with smallest tentative distance", "Source", "Largest"], 1, 5,
  "Greedy choice — safe because weights are non-negative.",
  ["Wipro", "Accenture"]),
Q("Relaxation means:",
  ["Delete edge", "dist[v] = min(dist[v], dist[u] + w)", "Add node", "Sort edges"], 1, 6,
  "Improve v's distance via u if better.",
  ["Amazon", "Cognizant"]),
Q("Dijkstra with binary heap: complexity?",
  ["O(V+E)", "O((V+E) log V)", "O(V²)", "O(E log E) only"], 1, 7,
  "Each edge may trigger a heap update.",
  ["Microsoft", "Google"]),
Q("Negative weights → use:",
  ["Dijkstra anyway", "Bellman-Ford", "BFS", "DFS"], 1, 7,
  "Bellman-Ford relaxes V-1 times, tolerating negatives.",
  ["Flipkart"]),
Q("Unweighted shortest path: best tool?",
  ["Dijkstra", "BFS — simpler and O(V+E)", "Bellman-Ford", "Floyd-Warshall"], 1, 8,
  "Don't bring a heap to a queue fight.",
  ["Goldman Sachs", "Amazon"]),
]),

L("bipartite-graph", "Bipartite Graphs — Two-Colouring",
"""## The idea

A graph is **bipartite** if nodes split into two sets with edges only *between*
sets (no edge inside a set). Equivalent: **2-colourable**.

## Check with BFS colouring

```python
def is_bipartite(graph, n):
    colour = {}
    for s in range(n):
        if s in colour: continue
        colour[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in graph[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]; q.append(v)
                elif colour[v] == colour[u]:
                    return False
    return True
```

## The theorem (know this!)

> Bipartite ⟺ **no odd-length cycle**.

Triangle (3-cycle) can never be 2-coloured — try it!

## Uses

- Matching problems (jobs ↔ applicants)
- Conflict graphs (exam scheduling)
""",
[
Q("Bipartite means:",
  ["Two nodes", "Vertices split in two sets, edges only between sets", "Two edges", "Binary tree"], 1, 4,
  "No intra-set edges allowed.",
  ["TCS", "Wipro"]),
Q("A graph is bipartite iff it has:",
  ["No cycles", "No ODD-length cycles", "No even cycles", "n/2 nodes"], 1, 8,
  "Odd cycles force a colour clash; even cycles colour fine.",
  ["Infosys", "Accenture"]),
Q("Triangle (3-cycle) is bipartite?",
  ["Yes", "No — odd cycle", "Sometimes", "Only if weighted"], 1, 7,
  "3 nodes, 2 colours → two adjacent share a colour.",
  ["Amazon", "Cognizant"]),
Q("BFS colouring assigns neighbour:",
  ["Same colour", "Opposite colour (1 - colour[u])", "Random", "No colour"], 1, 5,
  "Edges must cross the partition.",
  ["Microsoft", "Google"]),
Q("Outer loop over all vertices handles:",
  ["Speed", "Disconnected graphs", "Sorting", "Weights"], 1, 6,
  "Each component needs its own BFS start.",
  ["Flipkart"]),
Q("Checking bipartiteness costs:",
  ["O(n²)", "O(V + E)", "O(E log V)", "O(V*E)"], 1, 7,
  "One BFS over everything.",
  ["Goldman Sachs"]),
]),
])

MODULES.append(_graphs)


# ---------------------------------------------------------------------------
# MODULE 7 — RECURSION & DP (10 lessons)
# ---------------------------------------------------------------------------

_recdp = M("recursion-dp", "Recursion & DP", "From base cases to knapsack. Dynamic programming is THE placement differentiator — master the patterns here.", [

L("recursion-basics", "Recursion Basics — Base Case & Call Stack",
"""## The two non-negotiables

1. **Base case**: the input so small the answer is trivial (stops the recursion).
2. **Recursive step**: solve a SMALLER instance, build up.

```python
def factorial(n):
    if n <= 1: return 1          # base
    return n * factorial(n - 1)  # smaller instance
```

## The call stack (visualise!)

`factorial(3)` → `3 * factorial(2)` → `3 * 2 * factorial(1)` → `3*2*1 = 6`.
Frames pile up, then collapse. Depth = n → O(n) stack space.

## Missing base case = infinite recursion = RecursionError / stack overflow.

## Trust the recursion (leap of faith)

> Assume `f(n-1)` works; only write how `f(n)` uses it. Don't unroll mentally past one level.
""",
[
Q("Every recursion needs:",
  ["A loop", "Base case + recursive step on smaller input", "Global variables", "Two functions"], 1, 1,
  "Base stops it; smaller input guarantees progress toward base.",
  ["TCS", "Wipro"]),
Q("factorial(3) creates how many stack frames at deepest?",
  ["1", "3", "6", "0"], 1, 3,
  "frames for 3, 2, 1.",
  ["Infosys", "Accenture"]),
Q("Missing base case causes:",
  ["Wrong answer", "Infinite recursion → stack overflow", "Slow code", "Nothing"], 1, 2,
  "Never-ending self-calls exhaust the call stack.",
  ["Cognizant", "Amazon"]),
Q("Space complexity of naive recursive factorial?",
  ["O(1)", "O(n) call stack", "O(n²)", "O(log n)"], 1, 4,
  "n frames deep.",
  ["Microsoft"]),
Q("The 'leap of faith' means:",
  ["Guess", "Assume the smaller call works; build the current level", "Skip base case", "Use loops"], 1, 5,
  "Induction-style thinking — the core recursion skill.",
  ["Google", "Flipkart"]),
Q("Python default recursion limit is about:",
  ["100", "1000", "1000000", "unlimited"], 1, 6,
  "Deep recursion needs sys.setrecursionlimit or iteration.",
  ["Goldman Sachs"]),
]),

L("recursion-patterns", "Recursion Patterns — Sum, Power, Palindrome",
"""## Pattern 1: linear reduction

```python
def rsum(n):                       # 1+2+...+n
    if n <= 0: return 0
    return n + rsum(n - 1)
```

## Pattern 2: divide input

```python
def is_pal(s):
    if len(s) <= 1: return True
    return s[0] == s[-1] and is_pal(s[1:-1])
```

## Pattern 3: fast power (the clever one)

```python
def power(x, n):
    if n == 0: return 1
    half = power(x, n // 2)
    return half * half * (x if n % 2 else 1)   # O(log n)!
```

`power(2, 10)`: half=power(2,5) computed ONCE and squared — that's the trick.

## Pattern 4: multiple recursive calls

Fibonacci, tree traversals — branching recursion. Watch for repeated work (next lesson!).
""",
[
Q("rsum(4) = ?",
  ["6", "10", "4", "24"], 1, 2,
  "4+3+2+1 = 10.",
  ["TCS", "Infosys"]),
Q("Fast power is O(log n) because:",
  ["It's fast", "n halves each call; half computed once and squared", "Uses loops", "n is small"], 1, 6,
  "power(x,n//2) reused — no double computation.",
  ["Wipro", "Accenture"]),
Q("is_pal('abba'): first check?",
  ["len<=1", "s[0]==s[-1] → 'a'=='a' ✓, recurse on 'bb'", "reverse", "sort"], 1, 4,
  "Ends match → strip and continue.",
  ["Amazon", "Cognizant"]),
Q("Naive recursive Fibonacci fib(5) computes fib(2) how many times?",
  ["1", "3", "5", "2"], 1, 7,
  "Tree: fib5→fib4,fib3; fib4→fib3,fib2; fib3→fib2,fib1… fib(2) appears 3 times.",
  ["Microsoft", "Google"]),
Q("power(x, 0) must return:",
  ["0", "1", "x", "Error"], 1, 3,
  "x⁰ = 1 — the base case.",
  ["Flipkart"]),
Q("Recursion with TWO self-calls per level roughly gives time:",
  ["O(n)", "O(2^n) without memoization", "O(log n)", "O(n²)"], 1, 8,
  "Branching factor 2, depth n.",
  ["Goldman Sachs", "Amazon"]),
]),

L("memoization", "Memoization — Remember What You Computed",
"""## The idea

Cache results of expensive calls; return the cache on repeat:

```python
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```

## What changed?

- Before: O(2ⁿ) — exponential recomputation.
- After: each fib(k) computed **once** → O(n) time, O(n) space (cache + stack).

## The DP connection

> **Memoization = top-down dynamic programming.**
> Recursion + cache = DP. That's the whole secret.

## Two requirements for memoization to help

1. **Overlapping subproblems** (same inputs recur).
2. **Optimal substructure** (answer built from sub-answers) — for optimisation DPs.
""",
[
Q("Memoization stores:",
  ["All inputs", "Computed results keyed by arguments", "Nothing", "Only base cases"], 1, 3,
  "Cache hit avoids recomputation.",
  ["TCS", "Wipro"]),
Q("Memoized fib(100) time?",
  ["O(2^100)", "O(n) — each value once", "O(1)", "Impossible"], 1, 5,
  "n distinct states × O(1) work each.",
  ["Infosys", "Accenture"]),
Q("Memoization = which DP style?",
  ["Bottom-up", "Top-down", "Greedy", "Divide & conquer"], 1, 4,
  "Recursion from the top, caching on the way.",
  ["Amazon", "Cognizant"]),
Q("Overlapping subproblems means:",
  ["Many inputs", "Same subproblem solved repeatedly", "Hard problems", "Nested loops"], 1, 5,
  "The precondition that makes caching worthwhile.",
  ["Microsoft", "Google"]),
Q("lru_cache on fib: space?",
  ["O(1)", "O(n) cache + O(n) stack", "O(2^n)", "O(log n)"], 1, 6,
  "n cached values, n-deep recursion.",
  ["Flipkart"]),
Q("Memoization does NOT help when subproblems are:",
  ["Overlapping", "Disjoint (each solved once anyway)", "Small", "Many"], 1, 7,
  "No repeats → cache never hits.",
  ["Goldman Sachs"]),
]),

L("fibonacci-dp", "Fibonacci to DP — Bottom-Up Thinking",
"""## Three versions, one problem

```python
# 1. Naive recursion: O(2^n)
def fib(n):
    return n if n <= 1 else fib(n-1) + fib(n-2)

# 2. Memoized (top-down): O(n)
# 3. Bottom-up: build the table forward
def fib_bu(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b
```

## Bottom-up advantages

- **No recursion** → no stack overflow, no recursion limit.
- Often **O(1) space** (keep only last 2 values).
- Same O(n) time.

## The DP recipe (memorise this!)

1. **Define the state**: `dp[i]` = answer for input i.
2. **Recurrence**: `dp[i]` in terms of smaller states.
3. **Base cases**: dp[0], dp[1].
4. **Order**: compute increasing i.
5. **Answer**: dp[n] (or as specified).
""",
[
Q("Bottom-up fib space can be:",
  ["O(n) only", "O(1) — keep last two", "O(2^n)", "O(n²)"], 1, 5,
  "Only dp[i-1], dp[i-2] needed.",
  ["TCS", "Infosys"]),
Q("First step of the DP recipe?",
  ["Write code", "Define dp[i] = meaning of state", "Optimise", "Guess answer"], 1, 4,
  "A precise state definition makes the recurrence obvious.",
  ["Wipro", "Accenture"]),
Q("fib_bu(6)?",
  ["5", "8", "13", "6"], 1, 3,
  "0,1,1,2,3,5,8.",
  ["Amazon", "Cognizant"]),
Q("Bottom-up avoids:",
  ["Loops", "Recursion depth limits", "Arrays", "Addition"], 1, 5,
  "Iterative — no call stack growth.",
  ["Microsoft"]),
Q("Recurrence for fib:",
  ["dp[i]=dp[i-1]+1", "dp[i]=dp[i-1]+dp[i-2]", "dp[i]=2*dp[i-1]", "dp[i]=i"], 1, 4,
  "Sum of two previous states.",
  ["Google", "Flipkart"]),
Q("If only dp[n] is needed but recurrence uses dp[i-3], space is:",
  ["O(n)", "O(1) — sliding window of 3", "O(n³)", "O(log n)"], 1, 7,
  "Keep a fixed-size window of recent states.",
  ["Goldman Sachs"]),
]),

L("climbing-stairs", "Climbing Stairs — Your First Real DP",
"""## Problem

n stairs; climb 1 or 2 at a time. How many distinct ways to reach the top?

## Think it through

To reach step i, you came from i-1 (one step) or i-2 (two steps):

```
dp[i] = dp[i-1] + dp[i-2],  dp[0]=1, dp[1]=1
```

It's Fibonacci in disguise! n=5 → 8 ways.

## Why interviewers love it

- Tests whether you can **derive** a recurrence, not recite one.
- Follow-ups: 1/2/3 steps? (tribonacci), min cost climbing stairs (add costs),
  each with a one-line recurrence change.

## Min-cost variant

```python
# cost[i] to step on stair i; dp[i] = cost[i] + min(dp[i-1], dp[i-2])
```

Same skeleton — costs ride along.
""",
[
Q("Ways to climb 4 stairs (1 or 2 at a time)?",
  ["4", "5", "7", "8"], 1, 4,
  "dp: 1,1,2,3,5 → dp[4]=5.",
  ["TCS", "Wipro"]),
Q("The recurrence is:",
  ["dp[i]=dp[i-1]+1", "dp[i]=dp[i-1]+dp[i-2]", "dp[i]=2*dp[i-1]", "dp[i]=i"], 1, 5,
  "Arrive from one-below or two-below.",
  ["Infosys", "Accenture"]),
Q("dp[0]=1 means:",
  ["Zero stairs, zero ways", "One way to stand at ground (do nothing)", "Error", "One stair"], 1, 6,
  "Base convention that makes dp[2]=dp[1]+dp[0]=2 correct.",
  ["Amazon", "Cognizant"]),
Q("Steps of 1,2,3 allowed → recurrence?",
  ["dp[i-1]+dp[i-2]", "dp[i-1]+dp[i-2]+dp[i-3]", "3*dp[i-1]", "dp[i]=i³"], 1, 7,
  "Sum over all allowed jump sizes.",
  ["Microsoft", "Google"]),
Q("Min-cost variant: dp[i] = ?",
  ["cost[i]+dp[i-1]", "cost[i] + min(dp[i-1], dp[i-2])", "min(cost)", "dp[i-1]+dp[i-2]"], 1, 8,
  "Pay this stair's cost + cheaper of the two ways up.",
  ["Flipkart", "Amazon"]),
Q("Space optimisation:",
  ["Impossible", "Two variables (prev2, prev1)", "Hash map", "Recursion only"], 1, 7,
  "Recurrence looks back 2 → O(1) space.",
  ["Goldman Sachs"]),
]),

L("house-robber", "House Robber — Decisions with Constraints",
"""## Problem

Houses in a row with money; **can't rob adjacent** houses (alarm!). Max loot?

## The decision at each house

```
dp[i] = max(dp[i-1],           # skip house i
            dp[i-2] + nums[i]) # rob house i (+ best till i-2)
```

`[2,7,9,3,1]` → dp: 2,7,11,11,12 → **12** (2+9+1).

## The pattern to recognise

> "Max/min with a **can't-pick-adjacent** rule" → rob-skip DP.

## Circular variant (House Robber II)

Houses in a **circle** (first & last adjacent): answer = max(rob houses[0..n-2], rob houses[1..n-1]).
Two linear runs — the circle breaks into two lines.
""",
[
Q("[2,7,9,3,1] max loot?",
  ["10", "12", "11", "22"], 1, 6,
  "2+9+1=12 (skip 7,3).",
  ["TCS", "Infosys"]),
Q("The recurrence captures:",
  ["Always rob", "max(skip i, rob i + best till i-2)", "Sum all", "Rob evens"], 1, 5,
  "The binary decision at each house.",
  ["Wipro", "Accenture"]),
Q("Why dp[i-2] when robbing house i?",
  ["Random", "i-1 is adjacent → forbidden", "Speed", "Convention"], 1, 5,
  "Robbing i excludes i-1; best valid prefix ends at i-2.",
  ["Amazon", "Cognizant"]),
Q("Circular variant trick:",
  ["Ignore it", "max(linear[0..n-2], linear[1..n-1])", "Double the money", "Sort"], 1, 8,
  "Either rob first (exclude last) or skip first (include last).",
  ["Microsoft", "Google"]),
Q("This DP is O(n) time, O(1) space because:",
  ["Magic", "Two-variable sliding window", "n is small", "It's greedy"], 1, 7,
  "Only dp[i-1], dp[i-2] needed.",
  ["Flipkart"]),
Q("If all values negative, best loot?",
  ["Most negative", "0 — rob nothing", "Sum", "First house"], 1, 9,
  "Skipping everything is allowed (dp ≥ 0 with proper base).",
  ["Goldman Sachs", "Amazon"]),
]),

L("coin-change", "Coin Change — Min Coins & Counting Ways",
"""## Min coins (classic)

Coins [1,2,5], amount 11 → **3** (5+5+1).

```python
dp = [inf] * (amount+1); dp[0] = 0
for i in range(1, amount+1):
    for c in coins:
        if c <= i:
            dp[i] = min(dp[i], dp[i-c] + 1)
```

`dp[i]` = min coins for amount i. **Outer loop over amount** (order doesn't matter for min).

## Counting WAYS — loop order matters!

```python
for c in coins:            # coins OUTER
    for i in range(c, amount+1):
        dp[i] += dp[i-c]
```

Coins-outer counts **combinations** (1+2 once); amount-outer would count
**permutations** (1+2 and 2+1 separately). This distinction is a famous trap!

## Unreachable

dp[amount] stays inf → return -1.
""",
[
Q("Coins [1,2,5], amount 11 → min coins?",
  ["4", "3", "5", "2"], 1, 5,
  "5+5+1.",
  ["TCS", "Wipro"]),
Q("dp[i] in min-coins means:",
  ["Ways", "Min coins for amount i", "Max coin", "i itself"], 1, 5,
  "State definition first!",
  ["Infosys", "Accenture"]),
Q("For COUNTING combinations, loop order:",
  ["Amount outer", "Coins outer, then amount", "Either", "Nested reversed"], 1, 8,
  "Coins-outer ensures each coin considered once per combination.",
  ["Amazon", "Cognizant"]),
Q("Amount-outer for counting gives:",
  ["Combinations", "Permutations (order matters)", "Min coins", "Error"], 1, 8,
  "1+2 and 2+1 counted separately.",
  ["Microsoft", "Google"]),
Q("dp[amount] = inf at end means:",
  ["0 coins", "Impossible → return -1", "Infinite coins", "Bug"], 1, 6,
  "No combination reached the amount.",
  ["Flipkart"]),
Q("Greedy (biggest coin first) fails on coins [1,3,4], amount 6:",
  ["It works: 4+1+1=3", "Greedy gives 4+1+1 (3); optimal 3+3 (2)", "Greedy is optimal", "No solution"], 1, 9,
  "Canonical coin systems (like ours) mislead — DP is the safe answer.",
  ["Goldman Sachs", "Amazon"]),
]),

L("knapsack-intro", "0/1 Knapsack — The King of DP",
"""## Problem

n items, each with weight w[i] and value v[i]; capacity W. Each item taken
**at most once** (that's the "0/1"). Maximise value.

## 2D DP

```python
dp[i][w] = max value using first i items with capacity w
dp[i][w] = max(dp[i-1][w],                    # skip item i
               dp[i-1][w-wt[i]] + val[i])     # take item i
```

## Why 2D?

State needs TWO dimensions: which items considered AND remaining capacity.

## 1D optimisation (advanced)

Iterate w **backwards** so each item used once:

```python
for i in range(n):
    for w in range(W, wt[i]-1, -1):
        dp[w] = max(dp[w], dp[w-wt[i]] + val[i])
```

Forward iteration would reuse the item (that's unbounded knapsack!).

## Recognise it

> "Pick subset with weight limit, maximise value" → knapsack.
> Partition Equal Subset Sum = knapsack with value = weight, target = sum/2.
""",
[
Q("0/1 means:",
  ["Binary weights", "Each item taken 0 or 1 times", "0 or 1 items total", "Weight 0/1"], 1, 3,
  "Take-it-or-leave-it per item.",
  ["TCS", "Infosys"]),
Q("dp[i][w] means:",
  ["Weight", "Max value with first i items, capacity w", "Item count", "Min weight"], 1, 5,
  "Two-dimensional state.",
  ["Wipro", "Accenture"]),
Q("Taking item i adds:",
  ["dp[i-1][w] + val[i]", "dp[i-1][w-wt[i]] + val[i]", "val[i]", "wt[i]"], 1, 6,
  "Best of remaining capacity + this item's value.",
  ["Amazon", "Cognizant"]),
Q("1D optimisation iterates w:",
  ["Forward", "Backward — prevents reusing the item", "Random", "Once"], 1, 8,
  "Backward keeps dp[w-wt] from THIS round (already updated = reuse).",
  ["Microsoft", "Google"]),
Q("Forward 1D iteration solves:",
  ["0/1 knapsack", "Unbounded knapsack (reuse allowed)", "Nothing", "Subset sum"], 1, 9,
  "Updated dp[w-wt[i]] feeds back into the same item's round.",
  ["Flipkart"]),
Q("Partition Equal Subset Sum → knapsack with:",
  ["W = sum", "target = sum/2, value = weight", "W = 0", "No capacity"], 1, 9,
  "Can we fill exactly half? Classic reduction.",
  ["Goldman Sachs", "Amazon"]),
]),

L("lis-dp", "LIS — Longest Increasing Subsequence",
"""## O(n²) DP (learn this first)

```python
dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i], default=0)
answer = max(dp)
```

`dp[i]` = LIS **ending at i** (not "in prefix i" — the ending-anchor matters!).

`[10,9,2,5,3,7,101,18]` → dp ends … → LIS length **4** ([2,3,7,18]).

## O(n log n) — patience sorting (the impressive follow-up)

Maintain piles; for each x, binary-search the leftmost pile top ≥ x and replace.
Number of piles = LIS length. (Reconstructing the actual sequence needs care.)

## Why "ending at i"?

> The recurrence extends previous endings. "LIS in first i elements" doesn't
> compose — you need to know what the subsequence ENDS with.
""",
[
Q("LIS of [10,9,2,5,3,7,101,18]?",
  ["6", "4", "5", "3"], 1, 6,
  "[2,3,7,18] (or [2,5,7,101]).",
  ["TCS", "Wipro"]),
Q("dp[i] is defined as LIS:",
  ["In first i elements", "Ending exactly at index i", "Starting at i", "Of length i"], 1, 7,
  "The anchor lets us extend: nums[j] < nums[i] → dp[j]+1.",
  ["Infosys", "Accenture"]),
Q("Transition:",
  ["dp[i] = dp[i-1]+1", "1 + max(dp[j]) over j<i, nums[j]<nums[i]", "max(dp)", "dp[i]=i"], 1, 6,
  "Best extendable predecessor + 1.",
  ["Amazon", "Cognizant"]),
Q("Answer is max(dp), not dp[n-1], because:",
  ["Bug", "LIS may end anywhere, not necessarily at last element", "dp is wrong", "Convention"], 1, 7,
  "The longest subsequence's end is unknown upfront.",
  ["Microsoft", "Google"]),
Q("O(n log n) method is called:",
  ["Quick LIS", "Patience sorting", "Merge LIS", "Heap LIS"], 1, 9,
  "Piles + binary search.",
  ["Flipkart"]),
Q("Strictly increasing uses bisect_left; non-decreasing uses:",
  ["bisect_left", "bisect_right", "No bisect", "Sort"], 1, 10,
  "Equal elements: strict replaces (no extend); non-decreasing extends.",
  ["Goldman Sachs", "Amazon"]),
]),

L("grid-paths", "Grid Paths — DP on 2D Grids",
"""## Unique paths (m × n, move right/down only)

```python
dp[i][j] = dp[i-1][j] + dp[i][j-1]   # from top or left
dp[0][*] = dp[*][0] = 1             # first row/col: one way
```

3×3 → **6** paths.

## With obstacles

Obstacle cell → dp = 0 (can't step there). Everything else same.

## Min path sum

```python
dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
```

Same movement, costs accumulate instead of counting.

## The pattern

> Grids: dp[i][j] from **top/left** (sometimes + diagonal). Boundaries need care —
> first row/col are base cases. Space: 1D rolling array works (only previous row needed).
""",
[
Q("Unique paths in 3×3 (right/down)?",
  ["9", "6", "3", "12"], 1, 3,
  "dp fills to 6.",
  ["TCS", "Infosys"]),
Q("Recurrence:",
  ["dp[i-1][j] * dp[i][j-1]", "dp[i-1][j] + dp[i][j-1]", "dp[i-1][j-1]", "i+j"], 1, 4,
  "Arrive from top OR left.",
  ["Wipro", "Accenture"]),
Q("First row dp[0][j] = 1 because:",
  ["Convention", "Only one way: all rights", "It's the base", "j=1"], 1, 6,
  "No 'from top' exists; single path along the edge.",
  ["Amazon", "Cognizant"]),
Q("Obstacle at (i,j) → dp[i][j] = ?",
  ["1", "0", "inf", "-1"], 1, 6,
  "Unreachable cell contributes nothing.",
  ["Microsoft", "Google"]),
Q("Min path sum changes the recurrence to:",
  ["Sum", "grid[i][j] + min(top, left)", "max(top,left)", "Product"], 1, 7,
  "Accumulate cost along the cheaper approach.",
  ["Flipkart"]),
Q("Space optimisation:",
  ["Impossible", "1D array of n (previous row)", "O(1)", "2D required"], 1, 8,
  "dp[j] = dp[j] (top) + dp[j-1] (left) in one row.",
  ["Goldman Sachs", "Amazon"]),
]),
])

MODULES.append(_recdp)


# ---------------------------------------------------------------------------
# MODULE 8 — SORTING & SEARCHING (7 lessons)
# ---------------------------------------------------------------------------

_sortsearch = M("sorting-searching", "Sorting & Searching", "Merge sort, quicksort, binary search variants — know the trade-offs cold.", [

L("bubble-sort", "Bubble Sort — Adjacent Swaps",
"""## How it works

Repeatedly step through; swap adjacent out-of-order pairs. After pass k, the
k largest are in final position.

```python
def bubble(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped: break     # early exit
```

## Complexity

- Worst/average: **O(n²)**
- Best (sorted + early exit): **O(n)**
- Space: O(1). **Stable**: yes.

## The `n-1-i` detail

After i passes, the last i elements are sorted — don't re-scan them.
Forgetting `-i` still sorts but wastes comparisons (interviewers notice).
""",
[
Q("Inner loop goes to n-1-i because:",
  ["Tradition", "Last i elements already in place", "Speed of light", "Avoids index error only"], 1, 5,
  "Each pass fixes one more tail element.",
  ["TCS", "Wipro"]),
Q("Bubble sort is stable: equal elements:",
  ["Swap randomly", "Keep original relative order (no swap on ==)", "Get sorted", "Crash"], 1, 6,
  "`>` (not `>=`) never swaps equals.",
  ["Infosys", "Accenture"]),
Q("Best case with early exit?",
  ["O(n²)", "O(n)", "O(1)", "O(log n)"], 1, 4,
  "One pass, zero swaps → break.",
  ["Amazon", "Cognizant"]),
Q("After 2 passes on 6 elements, how many are in final position?",
  ["0", "2 (the two largest)", "6", "1"], 1, 5,
  "One per pass, from the largest down.",
  ["Microsoft"]),
Q("Space complexity?",
  ["O(n)", "O(1) — in-place swaps", "O(log n)", "O(n²)"], 1, 3,
  "Only loop variables + temp.",
  ["Google", "Flipkart"]),
Q("Bubble sort on reverse-sorted n elements: swaps?",
  ["n", "n(n-1)/2", "n²", "n log n"], 1, 8,
  "Every pair inverted = max swaps.",
  ["Goldman Sachs"]),
]),

L("selection-insertion", "Selection & Insertion Sort",
"""## Selection sort

Find the minimum of the unsorted part, swap it to the front:

```python
for i in range(n):
    m = min(range(i, n), key=lambda k: arr[k])
    arr[i], arr[m] = arr[m], arr[i]
```

- O(n²) **always** (even sorted — it still scans for the min).
- **Not stable** (long jumps can reorder equals).
- Minimises **swaps**: exactly n-1.

## Insertion sort

Build the sorted part left-to-right; insert each new card in place:

```python
for i in range(1, n):
    key, j = arr[i], i - 1
    while j >= 0 and arr[j] > key:
        arr[j+1] = arr[j]; j -= 1
    arr[j+1] = key
```

- Best O(n) (sorted), worst O(n²), **stable**, **adaptive**.
- Excellent for **nearly-sorted** or **small** arrays (used inside Timsort/quicksort hybrids!).
""",
[
Q("Selection sort best case (already sorted)?",
  ["O(n)", "O(n²) — still scans for min each pass", "O(1)", "O(n log n)"], 1, 6,
  "No early-exit possible; the min-search always runs.",
  ["TCS", "Infosys"]),
Q("Selection sort is not stable because:",
  ["It's slow", "Long-distance swaps can reorder equal elements", "It sorts", "It uses extra space"], 1, 7,
  "Swapping arr[i] with a far min jumps over equals.",
  ["Wipro", "Accenture"]),
Q("Insertion sort best case?",
  ["O(n²)", "O(n) — each element already in place", "O(1)", "O(n log n)"], 1, 5,
  "Inner while never runs on sorted input.",
  ["Amazon", "Cognizant"]),
Q("Best for nearly-sorted data:",
  ["Selection", "Insertion (adaptive)", "Bubble", "Merge"], 1, 6,
  "Near-sorted → inner loop barely moves → near O(n).",
  ["Microsoft", "Google"]),
Q("Selection sort swap count (n elements)?",
  ["O(n²)", "n-1 (one per pass)", "0", "n log n"], 1, 7,
  "Its claim to fame — minimal writes (useful for flash memory).",
  ["Flipkart"]),
Q("Timsort (Python's sort) uses insertion sort for:",
  ["Large arrays", "Tiny runs (≤64) — low overhead wins", "Never", "Reverse"], 1, 9,
  "Small n: insertion's simplicity beats divide-and-conquer overhead.",
  ["Goldman Sachs", "Amazon"]),
]),

L("merge-sort", "Merge Sort — Divide & Conquer",
"""## The algorithm

```python
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)      # two-pointer merge
```

## Complexity

- Recurrence: T(n) = 2T(n/2) + O(n) → **O(n log n)** always.
- Space: O(n) (merge buffers) — **not in-place**.
- **Stable**: yes (take from left on ties).

## Why it matters

- Guaranteed O(n log n) — quicksort's safety net.
- The natural sort for **linked lists** (O(1) extra space with pointer rewiring!).
- External sorting (data bigger than RAM): chunk-sort + k-way merge.

## Recursion depth

O(log n) — safe from stack overflow unlike naive quicksort worst case.
""",
[
Q("Merge sort recurrence?",
  ["T(n)=T(n-1)+n", "T(n)=2T(n/2)+O(n)", "T(n)=2T(n-1)", "T(n)=n²"], 1, 6,
  "Two halves + linear merge.",
  ["TCS", "Wipro"]),
Q("Merge sort is NOT in-place because:",
  ["It's recursive", "Merge needs O(n) auxiliary buffer", "It's slow", "It's unstable"], 1, 5,
  "Merging two sorted halves needs somewhere to put the result.",
  ["Infosys", "Accenture"]),
Q("Stable because on ties we take from:",
  ["Right", "Left — preserves original order", "Either", "Neither"], 1, 7,
  "Left-first on `<=` keeps equals in input order.",
  ["Amazon", "Cognizant"]),
Q("Best sort for linked lists?",
  ["Quicksort", "Merge sort — no random access needed, O(1) space via relinking",
   "Heap sort", "Bubble"], 1, 8,
  "Sequential merge fits pointer surgery perfectly.",
  ["Microsoft", "Google"]),
Q("Recursion depth?",
  ["O(n)", "O(log n)", "O(1)", "O(n log n)"], 1, 6,
  "Halving each level.",
  ["Flipkart"]),
Q("Sorting 100GB with 8GB RAM → use:",
  ["Quicksort", "External merge sort (chunk + k-way merge)", "Bubble sort", "Impossible"], 1, 9,
  "The classic big-data sorting strategy.",
  ["Goldman Sachs", "Amazon"]),
]),

L("quick-sort", "Quick Sort — Partition Power",
"""## The algorithm

```python
def quicksort(arr, lo, hi):
    if lo < hi:
        p = partition(arr, lo, hi)   # pivot to final spot
        quicksort(arr, lo, p-1)
        quicksort(arr, p+1, hi)
```

**Lomuto partition** (pivot = last):

```python
def partition(arr, lo, hi):
    pivot, i = arr[hi], lo
    for j in range(lo, hi):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]; i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i
```

## Complexity

- Average: **O(n log n)**. Worst (sorted + bad pivot): **O(n²)**.
- Space: O(log n) stack average.
- **Not stable**. In-place: yes.

## Pivot choice matters

Random/median-of-three pivots make worst case vanishingly rare — that's why
library sorts (introsort) start with quicksort.
""",
[
Q("Partition returns:",
  ["Sorted array", "Pivot's final index (smaller left, larger right)", "Pivot value", "Nothing"], 1, 6,
  "Everything left < pivot ≤ everything right.",
  ["TCS", "Infosys"]),
Q("Quicksort worst case happens with:",
  ["Random data", "Sorted input + fixed pivot (e.g. always last)", "Duplicates", "Small n"], 1, 7,
  "Partition splits 0 vs n-1 every time → T(n)=T(n-1)+O(n).",
  ["Wipro", "Accenture"]),
Q("Quicksort is:",
  ["Stable", "Not stable", "In-place but stable", "O(n) space"], 1, 6,
  "Long swaps reorder equals.",
  ["Amazon", "Cognizant"]),
Q("Random pivot helps because:",
  ["Faster comparisons", "Worst case becomes astronomically unlikely", "Less code", "Stability"], 1, 7,
  "No input consistently triggers bad splits.",
  ["Microsoft", "Google"]),
Q("In Lomuto, `i` tracks:",
  ["Pivot", "Boundary: arr[lo..i-1] < pivot", "End", "Nothing"], 1, 8,
  "The insertion point for the next smaller element.",
  ["Flipkart"]),
Q("Introsort (C++ std::sort) switches to heapsort when:",
  ["Array small", "Recursion depth exceeds 2*log n (worst-case guard)", "Always", "Never"], 1, 10,
  "Guarantees O(n log n) worst case while keeping quicksort's speed.",
  ["Goldman Sachs", "Amazon"]),
]),

L("binary-variants", "Binary Search Variants — First/Last Occurrence",
"""## First occurrence

```python
def first_occurrence(arr, t):
    lo, hi, ans = 0, len(arr)-1, -1
    while lo <= hi:
        mid = (lo+hi)//2
        if arr[mid] == t:
            ans = mid; hi = mid - 1   # keep looking LEFT
        elif arr[mid] < t: lo = mid + 1
        else: hi = mid - 1
    return ans
```

Found it? **Don't stop** — record and continue left.

## Last occurrence

Mirror: on match, `ans = mid; lo = mid + 1`.

## Count occurrences

`last - first + 1` — O(log n), no linear scan!

## Lower/upper bound (C++ STL thinking)

- `lower_bound`: first `>= t`
- `upper_bound`: first `> t`
- Count of t = upper − lower.

Python: `bisect_left` / `bisect_right`.
""",
[
Q("First occurrence: on arr[mid]==t, do:",
  ["Return mid", "ans=mid; hi=mid-1 (search left)", "ans=mid; lo=mid+1", "Break"], 1, 6,
  "An earlier copy may exist to the left.",
  ["TCS", "Wipro"]),
Q("Count of t in sorted array via variants?",
  ["Linear scan", "last - first + 1, both O(log n)", "Binary search once", "Impossible"], 1, 7,
  "Two modified binary searches, no O(n) scan.",
  ["Infosys", "Accenture"]),
Q("lower_bound(t) returns first index with:",
  ["== t", "value >= t", "value > t", "value < t"], 1, 7,
  "STL definition — works even when t is absent.",
  ["Amazon", "Cognizant"]),
Q("bisect_left vs bisect_right differ on:",
  ["Missing values", "Duplicates — insertion point before/after equals", "Speed", "Nothing"], 1, 8,
  "left: before existing equals; right: after.",
  ["Microsoft", "Google"]),
Q("If t absent, first_occurrence returns:",
  ["0", "-1 (ans never set)", "mid", "Error"], 1, 5,
  "ans initialised to -1.",
  ["Flipkart"]),
Q("Peak element (arr[i] > neighbours) via binary search works because:",
  ["Array sorted", "A slope direction always leads to a peak — discard half", "Luck", "It's linear"], 1, 10,
  "If arr[mid] < arr[mid+1], a peak exists right; else left. O(log n).",
  ["Goldman Sachs", "Amazon"]),
]),

L("search-rotated", "Search in Rotated Sorted Array",
"""## The problem

`[4,5,6,7,0,1,2]`, find 0 → index 4. Sorted, then rotated.

## Key insight

> One half is **always sorted**. Find which, then decide.

```python
def search(arr, t):
    lo, hi = 0, len(arr)-1
    while lo <= hi:
        mid = (lo+hi)//2
        if arr[mid] == t: return mid
        if arr[lo] <= arr[mid]:            # LEFT half sorted
            if arr[lo] <= t < arr[mid]: hi = mid-1
            else: lo = mid+1
        else:                              # RIGHT half sorted
            if arr[mid] < t <= arr[hi]: lo = mid+1
            else: hi = mid-1
    return -1
```

## With duplicates

`[2,2,2,3,2]` — can't tell which half is sorted when `arr[lo]==arr[mid]==arr[hi]`.
Fix: `lo += 1; hi -= 1` and continue → worst case degrades to O(n).

## Complexity

O(log n) distinct elements; O(n) worst with duplicates.
""",
[
Q("In a rotated sorted array, at any mid:",
  ["Both halves sorted", "At least one half is sorted", "Neither sorted", "Array is broken"], 1, 4,
  "Rotation preserves order on one side of mid.",
  ["TCS", "Infosys"]),
Q("Left half sorted check:",
  ["arr[lo] < arr[hi]", "arr[lo] <= arr[mid]", "arr[mid] < arr[hi]", "Always true"], 1, 5,
  "If lo..mid is non-decreasing, that half is sorted.",
  ["Wipro", "Accenture"]),
Q("t in sorted left half ⟺ ?",
  ["t > arr[mid]", "arr[lo] <= t < arr[mid]", "t < arr[lo]", "Always"], 1, 8,
  "Range check inside the sorted half.",
  ["Amazon", "Cognizant"]),
Q("Search [4,5,6,7,0,1,2] for 0 — first mid?",
  ["3 (value 7)", "0", "6", "4"], 0, 8,
  "mid=(0+6)//2=3 → 7. Left sorted, 0 not in [4,7) → go right.",
  ["Microsoft", "Google"]),
Q("Duplicates force worst case O(n) because:",
  ["Bug", "arr[lo]==arr[mid]==arr[hi] hides which half is sorted → shrink both ends",
   "Duplicates crash", "No reason"], 1, 9,
  "Must conservatively narrow; can degrade to linear.",
  ["Flipkart"]),
Q("Finding the rotation point (minimum) uses the same:",
  ["Sorting", "One-sorted-half logic, hunting the dip", "Hashing", "Two pointers"], 1, 9,
  "Minimum is where order breaks — binary search for it.",
  ["Goldman Sachs", "Amazon"]),
]),

L("complexity-analysis", "Complexity Analysis — Big-O Mastery",
"""## The hierarchy (memorise!)

```
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)
```

## How to analyse

1. **Drop constants**: O(2n) → O(n).
2. **Keep dominant term**: O(n² + n) → O(n²).
3. **Loops multiply**: nested loops over n → O(n²).
4. **Halving → log**: binary search → O(log n).
5. **Recurrence**: T(n) = 2T(n/2)+n → O(n log n) (Master theorem).

## Best/average/worst

- **Worst**: guarantee ("will never exceed").
- **Average**: expected over inputs.
- **Best**: optimistic (rarely quoted alone — it's marketing!).

## Amortised

Average over a **sequence** of ops: dynamic-array append is O(1) amortised
despite occasional O(n) resizes.

## Space too!

Time isn't everything — merge sort's O(n) space vs quicksort's O(log n)
is a real interview trade-off question.
""",
[
Q("O(n² + 100n + 500) simplifies to:",
  ["O(100n)", "O(n²)", "O(n²+100n)", "O(500)"], 1, 3,
  "Dominant term wins; constants drop.",
  ["TCS", "Wipro"]),
Q("T(n) = 2T(n/2) + O(n) solves to:",
  ["O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"], 1, 6,
  "Master theorem case 2 (merge sort's recurrence).",
  ["Infosys", "Accenture"]),
Q("Amortised O(1) append means:",
  ["Every append O(1)", "Average over many appends is O(1) despite rare O(n) resizes",
   "It's O(n)", "No resizing"], 1, 7,
  "Occasional expensive ops spread over many cheap ones.",
  ["Amazon", "Cognizant"]),
Q("Which grows fastest?",
  ["n log n", "n²", "2ⁿ", "n!"], 3, 4,
  "Factorial dominates exponential.",
  ["Microsoft", "Google"]),
Q("Quicksort worst-case space?",
  ["O(1)", "O(n) — degenerate recursion depth", "O(log n)", "O(n²)"], 1, 8,
  "Bad pivots → chain of n frames.",
  ["Flipkart"]),
Q("Proving a problem needs Ω(n log n) (comparison sorting lower bound) uses:",
  ["Examples", "Decision tree with n! leaves → height ≥ log(n!) = Ω(n log n)",
   "Benchmarks", "Guessing"], 1, 10,
  "Information-theoretic argument — the gold-standard answer.",
  ["Goldman Sachs", "Amazon"]),
]),
])

MODULES.append(_sortsearch)



# ---------------------------------------------------------------------------
# CURRICULUM assembly + attachment to sibling's seeded DSA domain
# ---------------------------------------------------------------------------

CURRICULUM = {"domain": DOMAIN, "modules": MODULES}

# Sibling migration m1n2curr001_curriculum already seeds domain 'dsa' with
# 7 modules. My 8 deep-content modules attach to those existing modules —
# no competing domain/modules are created.
SIBLING_DOMAIN_SLUG = "dsa"
MODULE_MAP = {
    "arrays": "arrays-strings",
    "strings": "arrays-strings",
    "linked-lists": "linked-lists",
    "stacks-queues": "stacks-queues",
    "trees": "trees-graphs",
    "graphs": "trees-graphs",
    "recursion-dp": "dynamic-programming",
    "sorting-searching": "sorting-searching",
}


# ---------------------------------------------------------------------------
# 10 CODING PROBLEMS (difficulty 6-10) with starter code (Python/Java/C++)
# ---------------------------------------------------------------------------

def _starter(fn_python, fn_java, fn_cpp):
    return {"python": fn_python, "java": fn_java, "cpp": fn_cpp}


def C(slug, lesson_slug, title, difficulty, statement, examples,
      constraints, hints, starter, companies):
    assert 6 <= difficulty <= 10
    assert len(examples) >= 1 and len(hints) >= 2
    return {
        "qtype": "coding",
        "slug": slug,
        "lesson_slug": lesson_slug,
        "title": title,
        "difficulty": difficulty,
        "statement": statement,
        "examples": examples,
        "constraints": constraints,
        "hints": hints,
        "starter_code": starter,
        "company_tags": companies,
    }


CODING_PROBLEMS = [

C("two-sum", "two-pointers", "Two Sum", 6,
"""Given an array of integers `nums` and an integer `target`, return the indices
of the TWO numbers that add up to `target`. Assume exactly one solution exists;
the same element may not be used twice.""",
[{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]",
  "note": "nums[0] + nums[1] = 2 + 7 = 9"},
 {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"}],
["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "Exactly one valid answer exists."],
["Brute force checks every pair: O(n^2). Can you do better?",
 "As you walk the array, what would you need to have seen before?",
 "A hash map from value to index gives O(1) lookups."],
_starter(
'def two_sum(nums, target):\n    # return [i, j]\n    pass',
'''class Solution {
    public int[] twoSum(int[] nums, int target) {
        // return new int[]{i, j};
        return null;
    }
}''',
'''#include <vector>
using namespace std;
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // return {i, j};
        return {};
    }
};'''),
["Amazon", "Google", "Microsoft", "Flipkart"]),

C("max-subarray", "kadane-rotation", "Maximum Subarray", 6,
"""Given an integer array `nums`, find the contiguous subarray (containing at
least one number) with the largest sum, and return its sum.""",
[{"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6",
  "note": "Subarray [4,-1,2,1] sums to 6"},
 {"input": "nums = [-1]", "output": "-1"}],
["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
["Try all subarrays? That's O(n^2). What decision do you make at each element?",
 "Either extend the previous subarray or start fresh here.",
 "Kadane's: cur = max(x, cur + x)."],
_starter(
'def max_subarray(nums):\n    # return int\n    pass',
'''class Solution {
    public int maxSubArray(int[] nums) {
        return 0;
    }
}''',
'''#include <vector>
using namespace std;
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        return 0;
    }
};'''),
["Amazon", "Microsoft", "Goldman Sachs"]),

C("valid-parentheses-code", "valid-parentheses", "Valid Parentheses", 6,
"""Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`,
`'['` and `']'`, determine if the input string is valid: open brackets must be
closed by the same type, in the correct order.""",
[{"input": 's = "()"', "output": "true"},
 {"input": 's = "()[]{}"', "output": "true"},
 {"input": 's = "(]"', "output": "false"}],
["1 <= s.length <= 10^4", "s consists of brackets only."],
["Which bracket must match the current closing bracket?",
 "The most recently opened one — what structure gives you that?",
 "Push openers; on a closer, pop and compare."],
_starter(
'def is_valid(s):\n    # return bool\n    pass',
'''class Solution {
    public boolean isValid(String s) {
        return false;
    }
}''',
'''#include <string>
using namespace std;
class Solution {
public:
    bool isValid(string s) {
        return false;
    }
};'''),
["Amazon", "Google", "TCS", "Infosys"]),

C("reverse-linked-list-code", "ll-reversal", "Reverse Linked List", 7,
"""Given the head of a singly linked list, reverse the list and return the new head.""",
[{"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"},
 {"input": "head = []", "output": "[]"}],
["0 <= nodes <= 5000", "-5000 <= Node.val <= 5000"],
["You'll need to remember the next node before overwriting the link.",
 "Three pointers: prev, curr, nxt.",
 "Return prev when curr becomes None."],
_starter(
'# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\ndef reverse_list(head):\n    # return new head\n    pass',
'''/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val; ListNode next;
 *     ListNode(int x) { val = x; }
 * }
 */
class Solution {
    public ListNode reverseList(ListNode head) {
        return null;
    }
}''',
'''/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val; ListNode *next;
 *     ListNode(int x) : val(x), next(nullptr) {}
 * };
 */
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        return nullptr;
    }
};'''),
["Microsoft", "Amazon", "Flipkart", "Adobe"]),

C("binary-search-code", "binary-search", "Binary Search", 7,
"""Given a SORTED array `nums` of n integers and a `target`, return its index,
or -1 if absent. Your solution must run in O(log n).""",
[{"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4"},
 {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1"}],
["1 <= n <= 10^4", "-10^4 <= nums[i], target <= 10^4", "nums is sorted ascending, all distinct."],
["Compare target with the middle element.",
 "Which half can you discard after each comparison?",
 "Watch the loop condition: lo <= hi, and use lo + (hi-lo)//2."],
_starter(
'def binary_search(nums, target):\n    # return index or -1\n    pass',
'''class Solution {
    public int search(int[] nums, int target) {
        return -1;
    }
}''',
'''#include <vector>
using namespace std;
class Solution {
public:
    int search(vector<int>& nums, int target) {
        return -1;
    }
};'''),
["Google", "Amazon", "TCS"]),

C("merge-intervals", "sorting-basics", "Merge Intervals", 7,
"""Given an array of `intervals` where intervals[i] = [start, end], merge all
overlapping intervals and return the non-overlapping set.""",
[{"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]"},
 {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]"}],
["1 <= intervals.length <= 10^4", "0 <= start <= end <= 10^4"],
["What if the intervals were sorted by start time?",
 "After sorting, one pass: overlap with the last merged interval?",
 "Overlap check: next.start <= current_end."],
_starter(
'def merge_intervals(intervals):\n    # return list of [start, end]\n    pass',
'''import java.util.*;
class Solution {
    public int[][] merge(int[][] intervals) {
        return new int[0][0];
    }
}''',
'''#include <vector>
using namespace std;
class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        return {};
    }
};'''),
["Amazon", "Microsoft", "Google", "Goldman Sachs"]),

C("lca-bst-code", "lca-trees", "Lowest Common Ancestor of a BST", 8,
"""Given a binary SEARCH tree and two nodes p and q, find their lowest common
ancestor (deepest node having both as descendants; a node can be its own descendant).""",
[{"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8", "output": "6"},
 {"input": "root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4", "output": "2"}],
["2 <= nodes <= 10^5", "-10^9 <= Node.val <= 10^9", "All values unique; p, q exist and differ."],
["Use the BST property — you don't need to search both subtrees.",
 "Both smaller than root? Go left. Both bigger? Go right.",
 "Otherwise the split point IS the answer."],
_starter(
'# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         ...\ndef lowest_common_ancestor(root, p, q):\n    # return TreeNode\n    pass',
'''/**
 * public class TreeNode {
 *     int val; TreeNode left, right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        return null;
    }
}''',
'''/**
 * struct TreeNode {
 *     int val; TreeNode *left, *right;
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 * };
 */
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        return nullptr;
    }
};'''),
["Amazon", "Microsoft", "Flipkart"]),

C("coin-change-code", "coin-change", "Coin Change", 8,
"""You are given coins of different denominations and a total `amount`. Compute
the FEWEST coins needed to make up that amount. Return -1 if impossible.""",
[{"input": "coins = [1,2,5], amount = 11", "output": "3",
  "note": "11 = 5 + 5 + 1"},
 {"input": "coins = [2], amount = 3", "output": "-1"}],
["1 <= coins.length <= 12", "1 <= amount <= 10^4"],
["Define dp[i] = min coins for amount i.",
 "How do you compute dp[i] from smaller amounts?",
 "dp[i] = min(dp[i-c] + 1) over coins c <= i."],
_starter(
'def coin_change(coins, amount):\n    # return int\n    pass',
'''class Solution {
    public int coinChange(int[] coins, int amount) {
        return -1;
    }
}''',
'''#include <vector>
using namespace std;
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        return -1;
    }
};'''),
["Amazon", "Google", "Microsoft"]),

C("longest-substring-code", "substrings-gen", "Longest Substring Without Repeating Characters", 9,
"""Given a string `s`, find the length of the longest substring WITHOUT
repeating characters.""",
[{"input": 's = "abcabcbb"', "output": "3", "note": '"abc"'},
 {"input": 's = "bbbbb"', "output": "1", "note": '"b"'},
 {"input": 's = "pwwkew"', "output": "3", "note": '"wke"'}],
["0 <= s.length <= 5 * 10^4", "English letters, digits, symbols, spaces."],
["A brute-force O(n^2) check of all substrings is too slow.",
 "Think sliding window: expand right, shrink left on duplicate.",
 "A map of char -> last index lets the left pointer JUMP."],
_starter(
'def length_of_longest_substring(s):\n    # return int\n    pass',
'''class Solution {
    public int lengthOfLongestSubstring(String s) {
        return 0;
    }
}''',
'''#include <string>
using namespace std;
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        return 0;
    }
};'''),
["Amazon", "Google", "Microsoft", "Flipkart", "Adobe"]),

C("trapping-rain-water", "two-pointers", "Trapping Rain Water", 10,
"""Given n non-negative integers representing an elevation map where the width
of each bar is 1, compute how much water it can trap after raining.""",
[{"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"},
 {"input": "height = [4,2,0,3,2,5]", "output": "9"}],
["n == height.length", "1 <= n <= 2 * 10^4", "0 <= height[i] <= 10^5"],
["Water above bar i = min(tallest left, tallest right) - height[i].",
 "Precompute left-max and right-max arrays: O(n) space. Can you do O(1)?",
 "Two pointers from both ends, tracking maxes — the smaller max decides."],
_starter(
'def trap(height):\n    # return int\n    pass',
'''class Solution {
    public int trap(int[] height) {
        return 0;
    }
}''',
'''#include <vector>
using namespace std;
class Solution {
public:
    int trap(vector<int>& height) {
        return 0;
    }
};'''),
["Amazon", "Google", "Microsoft", "Goldman Sachs", "Flipkart"]),
]


# ---------------------------------------------------------------------------
# Deterministic IDs + seed() against the REAL sibling schema
# ---------------------------------------------------------------------------

import uuid as _uuid
from datetime import datetime, timezone as _tz


def _lesson_id(slug):
    return str(_uuid.uuid5(_uuid.NAMESPACE_URL, "skillforge:dsa:lesson:" + slug))


def _question_id(lesson_slug, idx):
    return str(_uuid.uuid5(
        _uuid.NAMESPACE_URL, f"skillforge:dsa:question:{lesson_slug}:{idx}"))


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
    sibling's already-seeded DSA modules."""
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
    for ci, c in enumerate(CODING_PROBLEMS):
        sib = _lesson_module(c["lesson_slug"])
        prompt = (c["statement"]
                  + "\n\n**Examples**\n"
                  + "\n".join(f"- `{e['input']}` → `{e['output']}`"
                              + (f" ({e['note']})" if e.get("note") else "")
                              for e in c["examples"])
                  + "\n\n**Constraints**\n"
                  + "\n".join(f"- {x}" for x in c["constraints"])
                  + "\n\n**Starter code (Python)**\n```python\n"
                  + c["starter_code"]["python"] + "\n```")
        yield ("question", {
            "id": _question_id("coding-" + c["slug"], ci),
            "lesson_id": _lesson_id(c["lesson_slug"]),
            "module_slug": sib,
            "qtype": "coding",
            "difficulty": c["difficulty"],
            "prompt": prompt,
            "choices": None,
            "answer_index": None,
            "explanation": "Hints: " + " | ".join(c["hints"]),
            "company_tags": c["company_tags"],
        })


def _lesson_module(lesson_slug):
    for m in CURRICULUM["modules"]:
        for les in m["lessons"]:
            if les["slug"] == lesson_slug:
                return MODULE_MAP[m["slug"]]
    raise KeyError(f"unknown lesson {lesson_slug}")


def emit_sql(out=None):
    """Emit INSERTs against the real curriculum_* tables.

    Lessons attach to the sibling's already-seeded DSA modules via a
    module_id subselect; questions carry domain/module slugs + lesson_id.
    Safe to run after migration m1n2curr001_curriculum.
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
    """Insert the deep DSA content pack.

    Uses the real SQLAlchemy models (app.adapters.outbound.models).
    Attaches lessons/questions to the sibling's seeded 'dsa' domain modules.
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
            "coding": len(CODING_PROBLEMS),
            "total_questions": mcqs + len(CODING_PROBLEMS),
            "per_module": per_module, "narrow_lessons": narrow,
            "unmapped_modules": unmapped}


if __name__ == "__main__":
    c = verify_counts()
    print("modules:", c["modules"])
    print("lessons:", c["lessons"])
    print("mcq questions:", c["mcqs"])
    print("coding problems:", c["coding"])
    print("TOTAL questions:", c["total_questions"])
    print("\nper module (lessons, mcqs) -> sibling module:")
    for m in CURRICULUM["modules"]:
        nl, nq = c["per_module"][m["slug"]]
        print(f"  {m['slug']:20s} lessons={nl:2d} mcqs={nq:3d} -> {MODULE_MAP[m['slug']]}")
    assert not c["narrow_lessons"], c["narrow_lessons"]
    assert not c["unmapped_modules"], c["unmapped_modules"]
    assert c["modules"] == 8 and c["lessons"] == 68
    assert c["total_questions"] >= 400 and c["coding"] == 10
    print("\nAll assertions passed.")
