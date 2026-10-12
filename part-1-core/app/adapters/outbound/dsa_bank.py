"""Outbound adapter: curated Daily-DSA question bank.

14 classic problems (7 easy / 5 medium / 2 hard) with stdin/stdout I/O so
they run in the sandboxed code engine. Every hidden test's expected output
was machine-verified against a reference solution (see tests).

This is the DailyDSAProvider port implementation: the user's future AI
question generator will implement the same interface (pick_for_date +
submit grading) without any API change.
"""
from __future__ import annotations

from app.domain.dsa import DSAQuestion, Example, HiddenTest


def _q(qid, title, difficulty, description, examples, starter,
       hidden, tags=(), hints=()) -> DSAQuestion:
    q = DSAQuestion(
        id=qid, title=title, difficulty=difficulty, description=description,
        examples=tuple(Example(*e) for e in examples),
        starter_code=starter,
        hidden_tests=tuple(HiddenTest(*t) for t in hidden),
        topic_tags=tuple(tags), hints=tuple(hints),
    )
    q.validate()
    return q


_PY = "python"


def _starter(body: str) -> str:
    return (
        "import sys\n\n"
        "def solve() -> None:\n"
        "    data = sys.stdin.read().strip().split()\n"
        "    if not data:\n"
        "        return\n" + body + "\n\n"
        "if __name__ == \"__main__\":\n"
        "    solve()\n"
    )


BANK: list[DSAQuestion] = [
    _q(
        "dsa-e01", "Two Sum", "easy",
        "Given n, an array of n integers and a target, return the 0-based "
        "indices i and j (i < j) such that arr[i] + arr[j] == target. "
        "Exactly one solution exists.\n\n"
        "Input: line 1: n | line 2: n integers | line 3: target\n"
        "Output: i and j separated by a space",
        [("4\n2 7 11 15\n9", "0 1", "2 + 7 = 9")],
        _starter(
            "    it = iter(data)\n"
            "    n = int(next(it))\n"
            "    arr = [int(next(it)) for _ in range(n)]\n"
            "    target = int(next(it))\n"
            "    seen = {}\n"
            "    for i, x in enumerate(arr):\n"
            "        need = target - x\n"
            "        if need in seen:\n"
            "            print(f\"{seen[need]} {i}\")\n"
            "            return\n"
            "        seen[x] = i\n"
        ),
        [("3\n3 2 4\n6", "1 2"),
         ("2\n3 3\n6", "0 1"),
         ("5\n1 2 3 4 5\n9", "3 4"),
         ("4\n-1 -2 -3 -4\n-7", "2 3")],
        tags=("array", "hashmap"),
        hints=("A hash map of value -> index gives O(n).",),
    ),
    _q(
        "dsa-e02", "Valid Parentheses", "easy",
        "Given a string with brackets ()[]{}, decide if it is valid: every "
        "opening bracket is closed by the same type in the correct order.\n\n"
        "Input: one line (may be empty)\nOutput: true or false",
        [("()[]{}", "true", ""), ("(]", "false", "")],
        # NOTE: custom starter — empty string is valid input, so the shared
        # _starter (which early-returns on empty stdin) cannot be used.
        "import sys\n\n"
        "def solve() -> None:\n"
        "    s = sys.stdin.read().strip()\n"
        "    pairs = {')': '(', ']': '[', '}': '{'}\n"
        "    stack = []\n"
        "    for ch in s:\n"
        "        if ch in '([{':\n"
        "            stack.append(ch)\n"
        "        elif not stack or stack.pop() != pairs[ch]:\n"
        "            print('false')\n"
        "            return\n"
        "    print('true' if not stack else 'false')\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    solve()\n",
        [("([{}])", "true"),
         ("(((", "false"),
         ("", "true"),
         (")(", "false"),
         ("{[()]}", "true")],
        tags=("string", "stack"),
        hints=("Push opens, pop on close and compare.",),
    ),
    _q(
        "dsa-e03", "Binary Search", "easy",
        "Given n and a SORTED array of n integers and a target, return the "
        "0-based index of target, or -1 if absent. O(log n) expected.\n\n"
        "Input: line 1: n | line 2: n integers (sorted) | line 3: target\n"
        "Output: index or -1",
        [("5\n1 2 3 4 5\n3", "2", "")],
        _starter(
            "    it = iter(data)\n"
            "    n = int(next(it))\n"
            "    arr = [int(next(it)) for _ in range(n)]\n"
            "    target = int(next(it))\n"
            "    lo, hi = 0, n - 1\n"
            "    ans = -1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] == target:\n"
            "            ans = mid\n"
            "            break\n"
            "        elif arr[mid] < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    print(ans)\n"
        ),
        [("5\n1 2 3 4 5\n6", "-1"),
         ("1\n7\n7", "0"),
         ("4\n2 4 6 8\n5", "-1"),
         ("6\n-5 -2 0 3 9 12\n-2", "1")],
        tags=("array", "binary-search"),
        hints=("Halve the search space each step.",),
    ),
    _q(
        "dsa-e04", "Climbing Stairs", "easy",
        "You climb n stairs, taking 1 or 2 steps at a time. Count the "
        "distinct ways to reach the top.\n\nInput: n\nOutput: number of ways",
        [("3", "3", "1+1+1, 1+2, 2+1")],
        _starter(
            "    n = int(data[0])\n"
            "    a, b = 1, 1\n"
            "    for _ in range(n):\n"
            "        a, b = b, a + b\n"
            "    print(a)\n"
        ),
        [("2", "2"), ("5", "8"), ("10", "89"), ("1", "1")],
        tags=("dp",),
        hints=("ways(n) = ways(n-1) + ways(n-2).",),
    ),
    _q(
        "dsa-e05", "Best Time to Buy and Sell Stock", "easy",
        "Given n daily prices, find the max profit from one buy and one "
        "later sell. If no profit is possible, print 0.\n\n"
        "Input: line 1: n | line 2: n prices\nOutput: max profit",
        [("6\n7 1 5 3 6 4", "5", "buy at 1, sell at 6")],
        _starter(
            "    it = iter(data)\n"
            "    n = int(next(it))\n"
            "    prices = [int(next(it)) for _ in range(n)]\n"
            "    best, low = 0, float('inf')\n"
            "    for p in prices:\n"
            "        low = min(low, p)\n"
            "        best = max(best, p - low)\n"
            "    print(best)\n"
        ),
        [("5\n7 6 4 3 1", "0"),
         ("1\n5", "0"),
         ("4\n2 4 1 3", "2"),
         ("5\n3 3 3 3 3", "0")],
        tags=("array", "greedy"),
        hints=("Track the lowest price seen so far.",),
    ),
    _q(
        "dsa-e06", "Contains Duplicate", "easy",
        "Given n integers, print true if any value appears twice, else "
        "false.\n\nInput: line 1: n | line 2: n integers\nOutput: true or false",
        [("4\n1 2 3 1", "true", "")],
        _starter(
            "    it = iter(data)\n"
            "    n = int(next(it))\n"
            "    arr = [next(it) for _ in range(n)]\n"
            "    print('true' if len(set(arr)) < n else 'false')\n"
        ),
        [("4\n1 2 3 4", "false"),
         ("1\n1", "false"),
         ("6\n5 5 5 5 5 5", "true")],
        tags=("array", "hashset"),
        hints=("A set collapses duplicates.",),
    ),
    _q(
        "dsa-e07", "Fibonacci Number", "easy",
        "Print the n-th Fibonacci number with fib(0)=0, fib(1)=1.\n\n"
        "Input: n (0 <= n <= 30)\nOutput: fib(n)",
        [("10", "55", "")],
        _starter(
            "    n = int(data[0])\n"
            "    a, b = 0, 1\n"
            "    for _ in range(n):\n"
            "        a, b = b, a + b\n"
            "    print(a)\n"
        ),
        [("0", "0"), ("1", "1"), ("20", "6765"), ("30", "832040")],
        tags=("dp", "math"),
        hints=("Iterate, keeping only the last two values.",),
    ),
    _q(
        "dsa-m01", "Maximum Subarray", "medium",
        "Given n integers, find the contiguous subarray with the largest "
        "sum and print that sum.\n\n"
        "Input: line 1: n | line 2: n integers\nOutput: max subarray sum",
        [("9\n-2 1 -3 4 -1 2 1 -5 4", "6", "[4,-1,2,1]")],
        _starter(
            "    it = iter(data)\n"
            "    n = int(next(it))\n"
            "    arr = [int(next(it)) for _ in range(n)]\n"
            "    best = cur = arr[0]\n"
            "    for x in arr[1:]:\n"
            "        cur = max(x, cur + x)\n"
            "        best = max(best, cur)\n"
            "    print(best)\n"
        ),
        [("1\n-5", "-5"),
         ("5\n5 4 3 2 1", "15"),
         ("4\n-1 -2 -3 -4", "-1"),
         ("6\n-2 -3 4 -1 -2 1", "4")],
        tags=("array", "dp"),
        hints=("Kadane: extend or restart at each element.",),
    ),
    _q(
        "dsa-m02", "Merge Two Sorted Arrays", "medium",
        "Given n, m and two SORTED arrays A (n) and B (m), print the merged "
        "sorted array.\n\nInput: line 1: n m | line 2: A | line 3: B "
        "(a line may be empty when its size is 0)\nOutput: merged integers on one line",
        [("3 3\n1 3 5\n2 4 6", "1 2 3 4 5 6", "")],
        _starter(
            "    it = iter(data)\n"
            "    n = int(next(it)); m = int(next(it))\n"
            "    A = [int(next(it)) for _ in range(n)]\n"
            "    B = [int(next(it)) for _ in range(m)]\n"
            "    i = j = 0\n"
            "    out = []\n"
            "    while i < n and j < m:\n"
            "        if A[i] <= B[j]:\n"
            "            out.append(A[i]); i += 1\n"
            "        else:\n"
            "            out.append(B[j]); j += 1\n"
            "    out += A[i:] + B[j:]\n"
            "    print(' '.join(map(str, out)))\n"
        ),
        [("0 3\n\n1 2 3", "1 2 3"),
         ("2 0\n5 9\n", "5 9"),
         ("4 4\n1 1 2 2\n1 2 3 4", "1 1 1 2 2 2 3 4")],
        tags=("array", "two-pointers"),
        hints=("Walk both arrays with two pointers.",),
    ),
    _q(
        "dsa-m03", "Longest Substring Without Repeating", "medium",
        "Given a string, print the length of the longest substring without "
        "repeating characters.\n\nInput: one line (may be empty)\nOutput: length",
        [("abcabcbb", "3", "'abc'"), ("pwwkew", "3", "'wke'")],
        # NOTE: custom starter — empty string is valid input.
        "import sys\n\n"
        "def solve() -> None:\n"
        "    s = sys.stdin.read().strip()\n"
        "    last = {}\n"
        "    start = best = 0\n"
        "    for i, ch in enumerate(s):\n"
        "        if ch in last and last[ch] >= start:\n"
        "            start = last[ch] + 1\n"
        "        last[ch] = i\n"
        "        best = max(best, i - start + 1)\n"
        "    print(best)\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    solve()\n",
        [("bbbbb", "1"), ("", "0"), ("abcdef", "6"), ("abba", "2")],
        tags=("string", "sliding-window"),
        hints=("Sliding window with last-seen positions.",),
    ),
    _q(
        "dsa-m04", "Coin Change", "medium",
        "Given an amount, n coin denominations, find the fewest coins making "
        "the amount, or -1 if impossible. Unlimited coins of each type.\n\n"
        "Input: line 1: amount | line 2: n | line 3: n denominations\n"
        "Output: min coins or -1",
        [("11\n3\n1 2 5", "3", "5+5+1")],
        _starter(
            "    it = iter(data)\n"
            "    amount = int(next(it))\n"
            "    n = int(next(it))\n"
            "    coins = [int(next(it)) for _ in range(n)]\n"
            "    INF = amount + 1\n"
            "    dp = [INF] * (amount + 1)\n"
            "    dp[0] = 0\n"
            "    for a in range(1, amount + 1):\n"
            "        for c in coins:\n"
            "            if c <= a:\n"
            "                dp[a] = min(dp[a], dp[a - c] + 1)\n"
            "    print(dp[amount] if dp[amount] != INF else -1)\n"
        ),
        [("3\n1\n2", "-1"),
         ("0\n2\n1 2", "0"),
         ("7\n2\n2 5", "2"),
         ("100\n3\n1 7 10", "10")],
        tags=("dp",),
        hints=("dp[a] = 1 + min(dp[a-c]) over coins.",),
    ),
    _q(
        "dsa-m05", "Two Sum II — Sorted", "medium",
        "Like Two Sum, but the array is SORTED. Return 0-based indices.\n\n"
        "Input: line 1: n | line 2: n sorted integers | line 3: target\n"
        "Output: i and j separated by a space",
        [("4\n2 7 11 15\n9", "0 1", "")],
        _starter(
            "    it = iter(data)\n"
            "    n = int(next(it))\n"
            "    arr = [int(next(it)) for _ in range(n)]\n"
            "    target = int(next(it))\n"
            "    i, j = 0, n - 1\n"
            "    while i < j:\n"
            "        s = arr[i] + arr[j]\n"
            "        if s == target:\n"
            "            print(f'{i} {j}')\n"
            "            return\n"
            "        elif s < target:\n"
            "            i += 1\n"
            "        else:\n"
            "            j -= 1\n"
        ),
        [("3\n2 3 4\n6", "0 2"),
         ("2\n-1 0\n-1", "0 1"),
         ("5\n1 2 3 4 6\n10", "3 4")],
        tags=("array", "two-pointers"),
        hints=("Two pointers from both ends.",),
    ),
    _q(
        "dsa-h01", "Trapping Rain Water", "hard",
        "Given n bar heights, compute how much rain water is trapped after "
        "raining.\n\nInput: line 1: n | line 2: n heights\nOutput: trapped units",
        [("12\n0 1 0 2 1 0 1 3 2 1 2 1", "6", "")],
        _starter(
            "    it = iter(data)\n"
            "    n = int(next(it))\n"
            "    h = [int(next(it)) for _ in range(n)]\n"
            "    l, r = 0, n - 1\n"
            "    lmax = rmax = ans = 0\n"
            "    while l < r:\n"
            "        if h[l] < h[r]:\n"
            "            lmax = max(lmax, h[l])\n"
            "            ans += lmax - h[l]\n"
            "            l += 1\n"
            "        else:\n"
            "            rmax = max(rmax, h[r])\n"
            "            ans += rmax - h[r]\n"
            "            r -= 1\n"
            "    print(ans)\n"
        ),
        [("6\n4 2 0 3 2 5", "9"),
         ("3\n1 2 3", "0"),
         ("1\n5", "0"),
         ("5\n5 4 3 2 1", "0")],
        tags=("array", "two-pointers"),
        hints=("Two pointers tracking max walls on both sides.",),
    ),
    _q(
        "dsa-h02", "Container With Most Water", "hard",
        "Given n vertical line heights, find two lines that form the "
        "container holding the most water with the x-axis.\n\n"
        "Input: line 1: n | line 2: n heights\nOutput: max area",
        [("9\n1 8 6 2 5 4 8 3 7", "49", "")],
        _starter(
            "    it = iter(data)\n"
            "    n = int(next(it))\n"
            "    h = [int(next(it)) for _ in range(n)]\n"
            "    i, j = 0, n - 1\n"
            "    best = 0\n"
            "    while i < j:\n"
            "        best = max(best, min(h[i], h[j]) * (j - i))\n"
            "        if h[i] < h[j]:\n"
            "            i += 1\n"
            "        else:\n"
            "            j -= 1\n"
            "    print(best)\n"
        ),
        [("2\n1 1", "1"),
         ("5\n4 3 2 1 4", "16"),
         ("3\n1 2 1", "2"),
         ("6\n1 2 4 3 2 1", "6")],
        tags=("array", "two-pointers", "greedy"),
        hints=("Move the shorter side inward.",),
    ),
]
