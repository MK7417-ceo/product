"""Outbound adapter: Python coding problem bank.

50 ORIGINAL Python coding problems across 5 topics, ordered basics -> advanced
the way a learner should progress. Every problem carries a short theory primer,
hand-verified examples, realistic constraints, hints, starter code, and
machine-checkable test cases (input/expected pairs) for auto-grading.

Content is written originally for SkillForge — not copied from any site.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CodingProblem:
    id: str
    title: str
    topic: str  # basics | data-structures | functions | oop | advanced
    difficulty: str  # basic | easy | medium | hard
    description: str
    examples: list  # [{"input": str, "output": str, "explanation": str}]
    constraints: list
    theory: str  # 2-3 sentence concept explanation
    hints: list
    starter_code: dict  # {"python": ...}
    test_cases: list = field(default_factory=list)  # [{"input": str, "expected": str}]
    companies: list = field(default_factory=list)  # e.g. ["tcs", "amazon"]


def _ex(inp: str, out: str, why: str) -> dict:
    return {"input": inp, "output": out, "explanation": why}


def _tc(inp: str, out: str) -> dict:
    return {"input": inp, "expected": out}


def _p(pid: str, title: str, topic: str, difficulty: str, description: str,
       examples: list, constraints: list, theory: str, hints: list,
       starter_code: str, test_cases: list,
       companies: list | None = None) -> CodingProblem:
    return CodingProblem(
        id=pid, title=title, topic=topic, difficulty=difficulty,
        description=description, examples=examples, constraints=constraints,
        theory=theory, hints=hints, starter_code={"python": starter_code},
        test_cases=test_cases, companies=companies or [],
    )


_PYTHON_BANK: list[CodingProblem] = [
    # ================= BASICS (10) =================
    _p(
        "py-b01", "Sum of First N Numbers", "basics", "basic",
        "Given an integer n, return the sum of the first n natural numbers "
        "(1 + 2 + ... + n).",
        [
            _ex("n = 5", "15", "1+2+3+4+5 = 15."),
            _ex("n = 1", "1", "Just the number 1."),
            _ex("n = 100", "5050", "The classic Gauss sum."),
        ],
        ["1 <= n <= 10^9"],
        "A loop adds each number one by one, but the formula n*(n+1)//2 computes it "
        "in O(1). Recognizing when a loop has a closed form is a key optimization "
        "instinct — always ask 'is there a pattern?' before writing the loop.",
        ["Try range(1, n+1) with the built-in sum().",
         "The O(1) formula is n * (n + 1) // 2 — use integer division."],
        "def sum_n(n: int) -> int:",
        [_tc("n = 5", "15"), _tc("n = 100", "5050")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "py-b02", "Even or Odd", "basics", "basic",
        "Given an integer n, return the string 'even' if n is even and 'odd' otherwise. "
        "Zero counts as even.",
        [
            _ex("n = 4", "'even'", "4 is divisible by 2."),
            _ex("n = 7", "'odd'", "7 leaves remainder 1."),
            _ex("n = 0", "'even'", "Zero is even by definition."),
        ],
        ["-10^9 <= n <= 10^9"],
        "The modulo operator % gives the remainder after division; n % 2 == 0 means "
        "no remainder, hence even. Modulo is the workhorse of parity, divisibility, "
        "and cyclic problems — learn it once, use it everywhere.",
        ["Use n % 2 == 0 to test evenness.",
         "Negative numbers work fine: -3 % 2 == 1 in Python."],
        "def even_or_odd(n: int) -> str:",
        [_tc("n = 4", "even"), _tc("n = -3", "odd")],
        companies=["tcs", "wipro"],
    ),
    _p(
        "py-b03", "Factorial", "basics", "basic",
        "Given a non-negative integer n, return n! (n factorial). "
        "0! is defined as 1.",
        [
            _ex("n = 5", "120", "5*4*3*2*1 = 120."),
            _ex("n = 0", "1", "By definition 0! = 1."),
        ],
        ["0 <= n <= 20"],
        "Factorial multiplies every integer from 1 to n — a natural loop, or a "
        "recursion: n! = n * (n-1)!. Python integers have arbitrary precision, so "
        "overflow is not a concern here (unlike C/Java).",
        ["Loop i from 1 to n, multiplying a running result.",
         "Remember the base case: 0! = 1."],
        "def factorial(n: int) -> int:",
        [_tc("n = 5", "120"), _tc("n = 0", "1")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "py-b04", "Fibonacci Series", "basics", "basic",
        "Given n, return the first n Fibonacci numbers as a list, starting "
        "with [0, 1]. The sequence continues 0, 1, 1, 2, 3, 5, 8, ...",
        [
            _ex("n = 6", "[0, 1, 1, 2, 3, 5]", "Each term is the sum of the previous two."),
            _ex("n = 1", "[0]", "Just the first term."),
            _ex("n = 2", "[0, 1]", "The two seed values."),
        ],
        ["1 <= n <= 30"],
        "Each Fibonacci number is the sum of the two before it, so you only need to "
        "remember the last two values — no array of everything required. This "
        "'keep just what you need' sliding window is the seed of dynamic programming.",
        ["Start with [0, 1] and append a+b each step.",
         "Handle n = 1 and n = 2 as edge cases before the loop."],
        "def fibonacci(n: int) -> list[int]:",
        [_tc("n = 6", "[0, 1, 1, 2, 3, 5]"), _tc("n = 1", "[0]")],
        companies=["tcs", "infosys", "wipro"],
    ),
    _p(
        "py-b05", "Palindrome String", "basics", "basic",
        "Given a string s, return True if it reads the same forwards and "
        "backwards, else False. Comparison is case-sensitive; empty string is "
        "a palindrome.",
        [
            _ex("s = 'racecar'", "True", "Reversed it is identical."),
            _ex("s = 'hello'", "False", "'olleh' differs."),
            _ex("s = ''", "True", "Empty string is trivially a palindrome."),
        ],
        ["0 <= len(s) <= 10^4"],
        "A palindrome equals its own reversal, so s == s[::-1] is the whole check in "
        "Python. Slicing with a negative step is the idiomatic trick — but also know "
        "the two-pointer version for interviews in other languages.",
        ["Try s == s[::-1] — slicing with step -1 reverses.",
         "Two-pointer alternative: compare s[i] with s[n-1-i]."],
        "def is_palindrome(s: str) -> bool:",
        [_tc("s = 'racecar'", "True"), _tc("s = 'hello'", "False")],
        companies=["tcs", "infosys", "amazon"],
    ),
    _p(
        "py-b06", "Count Vowels", "basics", "basic",
        "Given a string s, return how many vowels (a, e, i, o, u — both cases) "
        "it contains.",
        [
            _ex("s = 'hello world'", "3", "e, o, o are vowels."),
            _ex("s = 'PYTHON'", "1", "Only O is a vowel."),
            _ex("s = 'rhythm'", "0", "No vowels at all."),
        ],
        ["0 <= len(s) <= 10^4"],
        "Membership testing with `in` against a vowel set is O(1) per character. "
        "Using a set (not a list) for lookups is a habit that pays off in every "
        "frequency-style problem.",
        ["Put vowels in a set: {'a','e','i','o','u','A','E','I','O','U'}.",
         "Sum 1 for each character c where c in vowels."],
        "def count_vowels(s: str) -> int:",
        [_tc("s = 'hello world'", "3"), _tc("s = 'rhythm'", "0")],
        companies=["tcs", "wipro"],
    ),
    _p(
        "py-b07", "Largest of Three", "basics", "basic",
        "Given three integers a, b, c, return the largest. If there is a tie, "
        "return the tied value.",
        [
            _ex("a = 3, b = 7, c = 5", "7", "7 is the biggest."),
            _ex("a = 9, b = 9, c = 2", "9", "Tie returns 9."),
        ],
        ["-10^9 <= a, b, c <= 10^9"],
        "Python's built-in max() takes any number of arguments — max(a, b, c). "
        "Knowing the standard library beats re-implementing: interviewers notice "
        "when you reach for the right builtin.",
        ["Just return max(a, b, c).",
         "Manual version: keep a champion, compare each challenger."],
        "def largest_of_three(a: int, b: int, c: int) -> int:",
        [_tc("a = 3, b = 7, c = 5", "7"), _tc("a = -1, b = -5, c = -3", "-1")],
        companies=["tcs"],
    ),
    _p(
        "py-b08", "Multiplication Table", "basics", "basic",
        "Given integers n and upto, return the multiplication table of n from "
        "1 to upto as a list of strings like '3 x 4 = 12'.",
        [
            _ex("n = 3, upto = 3", "['3 x 1 = 3', '3 x 2 = 6', '3 x 3 = 9']",
                "Each row multiplies n by i."),
        ],
        ["1 <= n, upto <= 20"],
        "f-strings (f'{n} x {i} = {n*i}') make formatted output readable. String "
        "building inside loops with f-strings is the modern Python way — avoid "
        "clunky concatenation.",
        ["Loop i from 1 to upto inclusive.",
         "Use an f-string: f\"{n} x {i} = {n*i}\"."],
        "def mult_table(n: int, upto: int) -> list[str]:",
        [_tc("n = 2, upto = 2", "['2 x 1 = 2', '2 x 2 = 4']")],
        companies=["tcs", "wipro"],
    ),
    _p(
        "py-b09", "Sum of Digits", "basics", "basic",
        "Given a non-negative integer n, return the sum of its decimal digits.",
        [
            _ex("n = 1234", "10", "1+2+3+4 = 10."),
            _ex("n = 9", "9", "Single digit sums to itself."),
            _ex("n = 1000", "1", "Zeros contribute nothing."),
        ],
        ["0 <= n <= 10^9"],
        "Peel digits with n % 10 and drop them with n //= 10, accumulating the sum. "
        "This digit-peeling loop is one of the five patterns behind half of all "
        "number problems — master it cold.",
        ["While n > 0: add n % 10 to total, then n //= 10.",
         "Alternative: sum(int(d) for d in str(n))."],
        "def sum_of_digits(n: int) -> int:",
        [_tc("n = 1234", "10"), _tc("n = 1000", "1")],
        companies=["infosys", "tcs"],
    ),
    _p(
        "py-b10", "Prime Check", "basics", "easy",
        "Given an integer n, return True if n is a prime number, else False. "
        "Numbers less than 2 are not prime.",
        [
            _ex("n = 7", "True", "7 has no divisors except 1 and 7."),
            _ex("n = 10", "False", "10 = 2 x 5."),
            _ex("n = 1", "False", "1 is not prime by definition."),
        ],
        ["0 <= n <= 10^6"],
        "If n has a divisor, one of the pair is <= sqrt(n), so checking divisors up "
        "to int(sqrt(n)) is enough — O(sqrt(n)) instead of O(n). This square-root "
        "bound appears in many number-theory optimizations.",
        ["Return False for n < 2 immediately.",
         "Loop i from 2 to int(n**0.5): if n % i == 0 return False."],
        "def is_prime(n: int) -> bool:",
        [_tc("n = 7", "True"), _tc("n = 10", "False")],
        companies=["tcs", "infosys", "wipro"],
    ),

    # ================= DATA STRUCTURES (10) =================
    _p(
        "py-d01", "Reverse a List", "data-structures", "basic",
        "Given a list of integers, return a new list with the elements in "
        "reverse order. Do not modify the input list.",
        [
            _ex("nums = [1, 2, 3, 4]", "[4, 3, 2, 1]", "Order flipped."),
            _ex("nums = []", "[]", "Empty stays empty."),
        ],
        ["0 <= len(nums) <= 10^4"],
        "nums[::-1] returns a reversed copy in one expression. Knowing slicing "
        "deeply (start:stop:step) replaces many manual loops — but also practice "
        "the manual two-pointer swap for interviews.",
        ["Return nums[::-1] for a copy.",
         "Manual: swap nums[i] and nums[n-1-i] for i < n//2."],
        "def reverse_list(nums: list[int]) -> list[int]:",
        [_tc("nums = [1, 2, 3]", "[3, 2, 1]"), _tc("nums = []", "[]")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "py-d02", "Remove Duplicates", "data-structures", "easy",
        "Given a list of integers, return a new list with duplicates removed, "
        "keeping the first occurrence order.",
        [
            _ex("nums = [3, 1, 3, 2, 1]", "[3, 1, 2]", "First occurrences kept in order."),
            _ex("nums = [1, 1, 1]", "[1]", "All collapse to one."),
        ],
        ["0 <= len(nums) <= 10^4"],
        "dict.fromkeys(nums) removes duplicates in O(n) while preserving order, "
        "because dicts remember insertion order since Python 3.7. set() alone is "
        "faster but scrambles order — know the trade-off.",
        ["list(dict.fromkeys(nums)) preserves order.",
         "Manual: track seen in a set, append only unseen items."],
        "def dedupe(nums: list[int]) -> list[int]:",
        [_tc("nums = [3, 1, 3, 2]", "[3, 1, 2]"), _tc("nums = []", "[]")],
        companies=["amazon", "flipkart"],
    ),
    _p(
        "py-d03", "Word Frequency", "data-structures", "easy",
        "Given a list of words, return a dictionary mapping each word to its "
        "count.",
        [
            _ex("words = ['a', 'b', 'a', 'c', 'b', 'a']", "{'a': 3, 'b': 2, 'c': 1}",
                "Counts of each distinct word."),
        ],
        ["0 <= len(words) <= 10^4"],
        "A dict counts in one pass: freq[w] = freq.get(w, 0) + 1. This counting "
        "pattern is the backbone of anagrams, majority-element, and sliding-window "
        "problems. collections.Counter does it in one line.",
        ["Use freq.get(w, 0) + 1 to avoid KeyError.",
         "Or: from collections import Counter; return dict(Counter(words))."],
        "def word_freq(words: list[str]) -> dict[str, int]:",
        [_tc("words = ['x', 'y', 'x']", "{'x': 2, 'y': 1}")],
        companies=["amazon", "flipkart"],
    ),
    _p(
        "py-d04", "Second Largest", "data-structures", "easy",
        "Given a list of integers with at least 2 distinct values, return the "
        "second largest distinct value.",
        [
            _ex("nums = [3, 7, 2, 9, 4]", "7", "9 is largest, 7 is next."),
            _ex("nums = [5, 5, 3, 5]", "3", "Duplicates of max don't count."),
        ],
        ["2 <= len(nums) <= 10^5"],
        "Track the top two distinct values in one pass — O(n) time, O(1) space. "
        "Sorting is O(n log n) and simpler, but the one-pass champion tracking "
        "shows stronger fundamentals.",
        ["Keep largest and second; update carefully on ties.",
         "Simple: sorted(set(nums))[-2]."],
        "def second_largest(nums: list[int]) -> int:",
        [_tc("nums = [3, 7, 2, 9]", "7"), _tc("nums = [1, 2]", "1")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "py-d05", "Squares of Evens", "data-structures", "easy",
        "Given a list of integers, return a list of the squares of the even "
        "numbers, preserving their original order.",
        [
            _ex("nums = [1, 2, 3, 4, 5]", "[4, 16]", "2^2=4, 4^2=16."),
            _ex("nums = [1, 3, 5]", "[]", "No evens at all."),
        ],
        ["0 <= len(nums) <= 10^4"],
        "A list comprehension [x*x for x in nums if x % 2 == 0] fuses filter and "
        "map into one readable line. Comprehensions are faster than "
        "append-in-a-loop and are idiomatic Python — use them fluently.",
        ["[x*x for x in nums if x % 2 == 0].",
         "Condition goes at the end: [expr for x in it if cond]."],
        "def squares_of_evens(nums: list[int]) -> list[int]:",
        [_tc("nums = [1, 2, 3, 4]", "[4, 16]"), _tc("nums = [1, 3]", "[]")],
        companies=["tcs"],
    ),
    _p(
        "py-d06", "Merge Dictionaries", "data-structures", "easy",
        "Given two dicts, return a new dict with all keys from both. If a key "
        "exists in both, the value from the second dict wins.",
        [
            _ex("d1 = {'a': 1, 'b': 2}, d2 = {'b': 3, 'c': 4}", "{'a': 1, 'b': 3, 'c': 4}",
                "'b' takes d2's value."),
        ],
        ["0 <= len(d1), len(d2) <= 10^3"],
        "The unpacking {**d1, **d2} (or d1 | d2 in Python 3.9+) merges with "
        "right-side priority. Never mutate inputs when a fresh dict is expected — "
        "return a new object.",
        ["{**d1, **d2} or d1 | d2 (3.9+).",
         "Manual: copy d1, then update with d2."],
        "def merge_dicts(d1: dict, d2: dict) -> dict:",
        [_tc("d1 = {'a': 1}, d2 = {'b': 2}", "{'a': 1, 'b': 2}")],
        companies=["flipkart"],
    ),
    _p(
        "py-d07", "Common Elements", "data-structures", "basic",
        "Given two lists of integers, return a sorted list of the distinct "
        "values present in both.",
        [
            _ex("a = [1, 2, 3, 4], b = [3, 4, 5]", "[3, 4]", "Shared values, sorted."),
            _ex("a = [1, 2], b = [3, 4]", "[]", "Nothing in common."),
        ],
        ["0 <= len(a), len(b) <= 10^4"],
        "Converting to sets makes intersection O(min(n,m)): sorted(set(a) & set(b)). "
        "Set operations (&, |, -) are implemented in C and dramatically faster than "
        "nested loops for membership problems.",
        ["sorted(set(a) & set(b)) — & is intersection.",
         "set(a) | set(b) would be union; set(a) - set(b) difference."],
        "def common_elements(a: list[int], b: list[int]) -> list[int]:",
        [_tc("a = [1, 2, 3], b = [2, 3, 4]", "[2, 3]")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "py-d08", "Sort Tuples by Second", "data-structures", "easy",
        "Given a list of (name, score) tuples, return them sorted by score "
        "ascending. Ties keep original order (stable).",
        [
            _ex("t = [('b', 2), ('a', 3), ('c', 1)]", "[('c', 1), ('b', 2), ('a', 3)]",
                "Ordered by the score field."),
        ],
        ["0 <= len(t) <= 10^4"],
        "sorted(t, key=lambda x: x[1]) sorts by the second element; Python's sort "
        "is stable so ties keep input order. The key-function pattern (lambda or "
        "operator.itemgetter) is how all custom sorting is done.",
        ["key=lambda pair: pair[1] extracts the sort key.",
         "For descending: sorted(t, key=..., reverse=True)."],
        "def sort_by_score(t: list[tuple]) -> list[tuple]:",
        [_tc("t = [('b', 2), ('a', 1)]", "[('a', 1), ('b', 2)]")],
        companies=["amazon"],
    ),
    _p(
        "py-d09", "Flatten Nested List", "data-structures", "medium",
        "Given a nested list where elements are ints or lists (arbitrarily "
        "deep), return a flat list of all ints in order.",
        [
            _ex("nested = [1, [2, [3, 4], 5], 6]", "[1, 2, 3, 4, 5, 6]",
                "All nesting removed, order kept."),
            _ex("nested = []", "[]", "Empty stays empty."),
        ],
        ["0 <= total ints <= 10^4", "depth <= 100"],
        "Recursion handles arbitrary depth naturally: if the item is a list, "
        "recurse; else append. isinstance(x, list) distinguishes the two cases. "
        "This 'recurse on containers, act on leaves' shape solves tree problems too.",
        ["Base: int -> append. Recursive: list -> flatten each item.",
         "Use isinstance(item, list) to decide."],
        "def flatten(nested: list) -> list[int]:",
        [_tc("nested = [1, [2, 3]]", "[1, 2, 3]"), _tc("nested = [[[]]]", "[]")],
        companies=["amazon", "google"],
    ),
    _p(
        "py-d10", "Group Anagrams", "data-structures", "medium",
        "Given a list of lowercase words, group anagrams together. Return a "
        "list of groups (each group a list). Order of groups does not matter.",
        [
            _ex("words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']",
                "[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]",
                "Anagrams share the same sorted letters."),
        ],
        ["0 <= len(words) <= 10^4"],
        "Anagrams have identical sorted letters, so ''.join(sorted(w)) is a perfect "
        "grouping key in a dict. Canonical-key grouping (sort the letters, count "
        "the letters, etc.) is the standard anagram technique.",
        ["Key = ''.join(sorted(word)).",
         "Append each word to groups[key]."],
        "def group_anagrams(words: list[str]) -> list[list[str]]:",
        [_tc("words = ['ab', 'ba', 'cd']", "[['ab', 'ba'], ['cd']]")],
        companies=["amazon", "google"],
    ),

    # ================= FUNCTIONS (10) =================
    _p(
        "py-f01", "Recursive Factorial", "functions", "basic",
        "Implement factorial(n) using recursion (no loops). 0! = 1.",
        [
            _ex("n = 5", "120", "5 * 4 * 3 * 2 * 1."),
            _ex("n = 0", "1", "Base case."),
        ],
        ["0 <= n <= 20"],
        "Recursion needs a base case (n <= 1 returns 1) and a step that shrinks "
        "the problem (n * factorial(n-1)). Every recursive function is these two "
        "parts — get them right and the rest follows.",
        ["Base case first: if n <= 1: return 1.",
         "Recursive step: return n * factorial(n - 1)."],
        "def factorial(n: int) -> int:",
        [_tc("n = 5", "120"), _tc("n = 0", "1")],
        companies=["tcs"],
    ),
    _p(
        "py-f02", "Nth Fibonacci (Recursive)", "functions", "easy",
        "Return the nth Fibonacci number (0-indexed: fib(0)=0, fib(1)=1) using "
        "recursion.",
        [
            _ex("n = 6", "8", "Sequence: 0,1,1,2,3,5,8."),
            _ex("n = 0", "0", "Base case."),
        ],
        ["0 <= n <= 20"],
        "fib(n) = fib(n-1) + fib(n-2) is the textbook recursion, but it recomputes "
        "subproblems exponentially — O(2^n). It teaches recursion's shape; the "
        "fix (memoization) comes in py-f09.",
        ["Base cases: fib(0)=0, fib(1)=1.",
         "Return fib(n-1) + fib(n-2)."],
        "def fib(n: int) -> int:",
        [_tc("n = 6", "8"), _tc("n = 10", "55")],
        companies=["infosys"],
    ),
    _p(
        "py-f03", "Sort Strings by Length", "functions", "easy",
        "Given a list of strings, return them sorted by length ascending using "
        "a lambda as the sort key.",
        [
            _ex("words = ['apple', 'pie', 'a', 'banana']", "['a', 'pie', 'apple', 'banana']",
                "Lengths 1, 3, 5, 6."),
        ],
        ["0 <= len(words) <= 10^4"],
        "A lambda is a one-line anonymous function: lambda w: len(w). Passing it "
        "as key= customizes sorting without a def. Lambdas shine as throwaway "
        "key/transform functions.",
        ["sorted(words, key=lambda w: len(w)).",
         "key extracts the comparison value from each item."],
        "def sort_by_length(words: list[str]) -> list[str]:",
        [_tc("words = ['bb', 'a', 'ccc']", "['a', 'bb', 'ccc']")],
        companies=["amazon"],
    ),
    _p(
        "py-f04", "Map-Filter Pipeline", "functions", "easy",
        "Given a list of ints, return the sum of squares of the positive "
        "numbers, using map() and filter().",
        [
            _ex("nums = [1, -2, 3, -4]", "10", "1^2 + 3^2 = 10."),
            _ex("nums = [-1, -2]", "0", "No positives."),
        ],
        ["0 <= len(nums) <= 10^4"],
        "filter(lambda x: x > 0, nums) keeps positives; map(lambda x: x*x, ...) "
        "squares them; sum() totals. Chaining small transforms is the functional "
        "style — each step does one thing.",
        ["filter keeps items where the lambda is True.",
         "sum(map(lambda x: x*x, filter(lambda x: x > 0, nums)))."],
        "def sum_sq_positives(nums: list[int]) -> int:",
        [_tc("nums = [1, -2, 3]", "10"), _tc("nums = []", "0")],
        companies=["flipkart"],
    ),
    _p(
        "py-f05", "Infinite Counter Generator", "functions", "medium",
        "Write a generator function counter(start=0) that yields start, "
        "start+1, start+2, ... forever. The caller decides when to stop.",
        [
            _ex("take 3 from counter(5)", "[5, 6, 7]", "Yields lazily, one at a time."),
        ],
        ["start >= 0"],
        "yield pauses the function and emits a value; next() resumes it. "
        "Generators produce infinite sequences with O(1) memory because values "
        "are computed on demand — the heart of lazy evaluation.",
        ["while True: yield n; n += 1.",
         "Test with itertools.islice(counter(5), 3)."],
        "def counter(start: int = 0):",
        [_tc("list(__import__('itertools').islice(counter(10), 3))", "[10, 11, 12]")],
        companies=["google", "amazon"],
    ),
    _p(
        "py-f06", "Timing Decorator", "functions", "medium",
        "Write a decorator @timed that prints how long the wrapped function "
        "took (in seconds) and returns its result unchanged.",
        [
            _ex("@timed on slow() returning 42", "prints time, returns 42",
                "Decorator wraps without changing behavior."),
        ],
        ["Function takes < 5 seconds"],
        "A decorator is a function returning a wrapper: it calls the original, "
        "measures with time.perf_counter(), and returns the result. "
        "functools.wraps preserves the original's name — always use it.",
        ["wrapper(*args, **kwargs): start, result = fn(...), print elapsed.",
         "Use @functools.wraps(fn) on the wrapper."],
        "import time, functools\ndef timed(fn):",
        [_tc("timed(lambda: 42)()", "42")],
        companies=["google"],
    ),
    _p(
        "py-f07", "Flexible Sum", "functions", "easy",
        "Write sum_all(*args, **kwargs) returning the sum of all positional "
        "args plus all keyword-argument values.",
        [
            _ex("sum_all(1, 2, a=3, b=4)", "10", "1+2+3+4."),
            _ex("sum_all()", "0", "Nothing to sum."),
        ],
        ["All values are ints"],
        "*args collects extra positionals into a tuple; **kwargs collects extra "
        "keywords into a dict. Together they make functions accept anything — "
        "the basis of wrappers and flexible APIs.",
        ["sum(args) + sum(kwargs.values()).",
         "kwargs.values() gives just the values."],
        "def sum_all(*args, **kwargs) -> int:",
        [_tc("sum_all(1, 2, a=3)", "6"), _tc("sum_all()", "0")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "py-f08", "Recursive List Sum", "functions", "easy",
        "Return the sum of a list of ints using recursion (no loops, no sum()).",
        [
            _ex("nums = [1, 2, 3, 4]", "10", "1+2+3+4."),
            _ex("nums = []", "0", "Base case: empty sums to 0."),
        ],
        ["0 <= len(nums) <= 1000"],
        "Recursion on lists: empty list is the base case (0); otherwise "
        "nums[0] + rec_sum(nums[1:]). It mirrors the mathematical definition of "
        "summation and trains structural recursion.",
        ["if not nums: return 0.",
         "return nums[0] + rec_sum(nums[1:])."],
        "def rec_sum(nums: list[int]) -> int:",
        [_tc("nums = [1, 2, 3]", "6"), _tc("nums = []", "0")],
        companies=["tcs"],
    ),
    _p(
        "py-f09", "Memoized Fibonacci", "functions", "medium",
        "Return the nth Fibonacci number using memoization so it runs in O(n). "
        "Do not use loops.",
        [
            _ex("n = 30", "832040", "Fast even for n=30."),
            _ex("n = 0", "0", "Base case."),
        ],
        ["0 <= n <= 100"],
        "Plain recursion recomputes fib(k) many times; a memo dict stores each "
        "result once, cutting O(2^n) to O(n). Memoization is the core trick of "
        "top-down dynamic programming.",
        ["memo = {0: 0, 1: 1}; check memo before recursing.",
         "functools.lru_cache does this automatically."],
        "def fib_memo(n: int) -> int:",
        [_tc("n = 30", "832040"), _tc("n = 1", "1")],
        companies=["amazon", "google"],
    ),
    _p(
        "py-f10", "Counter Closure", "functions", "medium",
        "Write make_counter() returning a function that returns 1, 2, 3, ... "
        "on successive calls (each call increments an enclosed variable).",
        [
            _ex("c = make_counter(); c(); c()", "1 then 2", "State persists between calls."),
        ],
        ["No constraints"],
        "A closure captures the enclosing scope's variable; nonlocal lets the "
        "inner function rebind it. Closures are how Python does stateful function "
        "factories — and the mechanism behind decorators.",
        ["count = 0; def inner(): nonlocal count; count += 1; return count.",
         "Return inner from make_counter."],
        "def make_counter():",
        [_tc("(lambda c: [c(), c()])(make_counter())", "[1, 2]")],
        companies=["google"],
    ),

    # ================= OOP (10) =================
    _p(
        "py-o01", "Book Class", "oop", "basic",
        "Create a class Book with attributes title and author set via "
        "__init__, and a method describe() returning 'title by author'.",
        [
            _ex("Book('Dune', 'Herbert').describe()", "'Dune by Herbert'",
                "Formatted from attributes."),
        ],
        ["Non-empty strings"],
        "__init__ runs when the object is created; self refers to the instance. "
        "Classes bundle data (attributes) with behavior (methods) — the foundation "
        "of OOP.",
        ["def __init__(self, title, author): self.title = title ...",
         "describe returns f\"{self.title} by {self.author}\"."],
        "class Book:\n    def __init__(self, title: str, author: str): ...\n    def describe(self) -> str: ...",
        [_tc("Book('Dune', 'Herbert').describe()", "Dune by Herbert")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "py-o02", "Bank Account", "oop", "easy",
        "Create class BankAccount with balance (default 0), deposit(amount) "
        "adding to balance, withdraw(amount) subtracting only if sufficient "
        "funds (else raise ValueError), and get_balance().",
        [
            _ex("deposit(100), withdraw(30)", "balance 70", "Normal flow."),
            _ex("withdraw(50) on balance 20", "ValueError", "Insufficient funds."),
        ],
        ["amount > 0"],
        "Methods mutate self.balance; validation (amount <= balance) guards "
        "invariants. Raising ValueError on bad operations is the Pythonic way to "
        "signal misuse instead of returning magic numbers.",
        ["withdraw: if amount > self.balance: raise ValueError(...).",
         "deposit/withdraw adjust self.balance."],
        "class BankAccount:\n    def __init__(self, balance: int = 0): ...\n    def deposit(self, amount: int) -> None: ...\n    def withdraw(self, amount: int) -> None: ...\n    def get_balance(self) -> int: ...",
        [_tc("(lambda a: (a.deposit(100), a.withdraw(30), a.get_balance()))(BankAccount())[-1]", "70")],
        companies=["infosys", "wipro"],
    ),
    _p(
        "py-o03", "Animal Inheritance", "oop", "easy",
        "Create class Animal with method speak() returning 'generic sound'. "
        "Create Dog(Animal) overriding speak() to return 'woof'. Create "
        "Cat(Animal) returning 'meow'.",
        [
            _ex("Dog().speak()", "'woof'", "Overridden method."),
            _ex("Animal().speak()", "'generic sound'", "Base version."),
        ],
        ["No constraints"],
        "Inheritance: Dog(Animal) gets everything Animal has, then overrides "
        "speak(). Method resolution finds the most-derived version — this "
        "'same call, different behavior' is polymorphism's basis.",
        ["class Dog(Animal): then def speak(self): return 'woof'.",
         "No __init__ needed if only methods differ."],
        "class Animal:\n    def speak(self) -> str: ...\nclass Dog(Animal): ...\nclass Cat(Animal): ...",
        [_tc("Dog().speak()", "woof"), _tc("Cat().speak()", "meow")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "py-o04", "Shape Override", "oop", "easy",
        "Create base class Shape with method area() returning 0. Subclass "
        "Rectangle(w, h) overriding area() to return w*h. Subclass "
        "Circle(r) overriding area() to return 3.14159*r*r.",
        [
            _ex("Rectangle(3, 4).area()", "12", "3*4."),
            _ex("Circle(1).area()", "3.14159", "pi * 1^2."),
        ],
        ["w, h, r > 0"],
        "Overriding replaces the base implementation per subclass. Code that "
        "calls shape.area() works for any shape — polymorphism lets new shapes "
        "be added without touching existing code.",
        ["Store w, h in __init__; area returns self.w * self.h.",
         "Circle stores r; area returns 3.14159 * r * r."],
        "class Shape:\n    def area(self) -> float: ...\nclass Rectangle(Shape): ...\nclass Circle(Shape): ...",
        [_tc("Rectangle(3, 4).area()", "12"), _tc("round(Circle(2).area(), 2)", "12.57")],
        companies=["tcs"],
    ),
    _p(
        "py-o05", "Playlist Magic Methods", "oop", "easy",
        "Create class Playlist(songs: list) supporting len(playlist) "
        "(via __len__) and playlist[i] indexing (via __getitem__).",
        [
            _ex("len(Playlist(['a','b']))", "2", "__len__ called."),
            _ex("Playlist(['a','b'])[1]", "'b'", "__getitem__ called."),
        ],
        ["No constraints"],
        "Dunder (magic) methods let objects speak Python's protocols: __len__ "
        "powers len(), __getitem__ powers []. Implementing protocols instead of "
        "custom methods makes classes feel native.",
        ["def __len__(self): return len(self.songs).",
         "def __getitem__(self, i): return self.songs[i]."],
        "class Playlist:\n    def __init__(self, songs: list[str]): ...\n    def __len__(self) -> int: ...\n    def __getitem__(self, i: int) -> str: ...",
        [_tc("len(Playlist(['a','b','c']))", "3"), _tc("Playlist(['x','y'])[0]", "x")],
        companies=["flipkart"],
    ),
    _p(
        "py-o06", "Instance Counter", "oop", "medium",
        "Create class Widget with a class variable count tracking how many "
        "instances were created. Add a classmethod total() returning count.",
        [
            _ex("Widget(); Widget(); Widget.total()", "2", "Two instances made."),
        ],
        ["No constraints"],
        "Class variables are shared across all instances; __init__ increments "
        "Widget.count. A @classmethod receives cls (the class) instead of self — "
        "the right tool for class-level state.",
        ["count = 0 at class level; in __init__: Widget.count += 1.",
         "@classmethod def total(cls): return cls.count."],
        "class Widget:\n    count: int = 0\n    def __init__(self): ...\n    @classmethod\n    def total(cls) -> int: ...",
        [_tc("(lambda b=Widget.total(): (Widget(), Widget(), Widget.total()-b)[-1])()", "2")],
        companies=["infosys"],
    ),
    _p(
        "py-o07", "Temperature Property", "oop", "medium",
        "Create class Temperature storing celsius. Add a property fahrenheit "
        "that gets/sets the Fahrenheit value (F = C*9/5+32), keeping celsius "
        "in sync.",
        [
            _ex("t = Temperature(0); t.fahrenheit", "32.0", "0C = 32F."),
            _ex("t.fahrenheit = 212; t.celsius", "100.0", "212F = 100C."),
        ],
        ["Any float"],
        "@property makes a method behave like an attribute; @fahrenheit.setter "
        "makes assignment run code. Properties give attribute-like syntax with "
        "method-like control — validation and computed values stay clean.",
        ["@property def fahrenheit(self): return self.celsius*9/5+32.",
         "@fahrenheit.setter: self.celsius = (f-32)*5/9."],
        "class Temperature:\n    def __init__(self, celsius: float): ...\n    @property\n    def fahrenheit(self) -> float: ...\n    @fahrenheit.setter\n    def fahrenheit(self, f: float) -> None: ...",
        [_tc("Temperature(0).fahrenheit", "32.0")],
        companies=["amazon"],
    ),
    _p(
        "py-o08", "MRO Explorer", "oop", "medium",
        "Given classes A, B(A), C(A), D(B, C): write function mro_names(cls) "
        "returning the __name__ of each class in cls.__mro__ as a list.",
        [
            _ex("mro_names(D)", "['D', 'B', 'C', 'A', 'object']",
                "C3 linearization order."),
        ],
        ["No constraints"],
        "Python resolves methods via C3 linearization: depth-first, left-to-right, "
        "monotonic. cls.__mro__ exposes it directly. Understanding MRO explains "
        "which method actually runs in diamond hierarchies.",
        ["return [c.__name__ for c in cls.__mro__].",
         "D(B, C): B before C, then shared A once."],
        "class A: pass\nclass B(A): pass\nclass C(A): pass\nclass D(B, C): pass\ndef mro_names(cls) -> list[str]:",
        [_tc("mro_names(D)", "['D', 'B', 'C', 'A', 'object']")],
        companies=["google"],
    ),
    _p(
        "py-o09", "Abstract Shape", "oop", "medium",
        "Using abc.ABC, create abstract class Shape with abstract method "
        "area(). Create Square(side) implementing area(). Instantiating Shape "
        "directly must raise TypeError.",
        [
            _ex("Square(4).area()", "16", "Concrete implementation."),
            _ex("Shape()", "TypeError", "Cannot instantiate abstract class."),
        ],
        ["side > 0"],
        "ABC + @abstractmethod declares a contract: subclasses must implement "
        "area(), and the base cannot be instantiated. Abstract classes enforce "
        "designs at definition time, not at bug time.",
        ["class Shape(ABC): @abstractmethod def area(self).",
         "Square(Shape) implements area returning side*side."],
        "from abc import ABC, abstractmethod\nclass Shape(ABC):\n    @abstractmethod\n    def area(self) -> float: ...\nclass Square(Shape): ...",
        [_tc("Square(4).area()", "16")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "py-o10", "Vector Addition", "oop", "hard",
        "Create class Vector2D(x, y) supporting v1 + v2 via __add__ (component-"
        "wise), == via __eq__, and readable repr via __repr__.",
        [
            _ex("Vector2D(1,2) + Vector2D(3,4)", "Vector2D(4, 6)", "Component-wise add."),
            _ex("Vector2D(1,2) == Vector2D(1,2)", "True", "Equal components."),
        ],
        ["Any numbers"],
        "Operator overloading maps + to __add__, == to __eq__. __add__ should "
        "return a NEW Vector2D (immutable style). Custom types that behave like "
        "built-ins are the mark of a well-designed class.",
        ["__add__: return Vector2D(self.x + o.x, self.y + o.y).",
         "__eq__: compare x and y; __repr__: f'Vector2D({x}, {y})'."],
        "class Vector2D:\n    def __init__(self, x: float, y: float): ...\n    def __add__(self, o): ...\n    def __eq__(self, o) -> bool: ...\n    def __repr__(self) -> str: ...",
        [_tc("repr(Vector2D(1, 2) + Vector2D(3, 4))", "Vector2D(4, 6)"), _tc("Vector2D(1,2) == Vector2D(1,2)", "True")],
        companies=["google", "amazon"],
    ),

    # ================= ADVANCED (10) =================
    _p(
        "py-a01", "Safe Division", "advanced", "basic",
        "Write safe_divide(a, b) returning a/b, but returning the string "
        "'error' if b is zero (catch ZeroDivisionError).",
        [
            _ex("safe_divide(10, 2)", "5.0", "Normal division."),
            _ex("safe_divide(10, 0)", "'error'", "Caught the exception."),
        ],
        ["Any numbers"],
        "try/except converts a crash into a controlled outcome. Catch the "
        "specific exception (ZeroDivisionError), not bare except — precision in "
        "error handling prevents hiding real bugs.",
        ["try: return a / b / except ZeroDivisionError: return 'error'.",
         "Never use bare except: — always name the exception."],
        "def safe_divide(a: float, b: float):",
        [_tc("safe_divide(10, 2)", "5.0"), _tc("safe_divide(5, 0)", "error")],
        companies=["tcs"],
    ),
    _p(
        "py-a02", "Age Validator", "advanced", "easy",
        "Write validate_age(age): raise ValueError('too young') if age < 18, "
        "raise ValueError('invalid') if age > 150, else return 'ok'.",
        [
            _ex("validate_age(25)", "'ok'", "In range."),
            _ex("validate_age(10)", "ValueError('too young')", "Raised with message."),
        ],
        ["Any int"],
        "Custom validation raises ValueError with a clear message; callers catch "
        "it and read the message. Raising early ('fail fast') keeps invalid data "
        "from spreading through the program.",
        ["if age < 18: raise ValueError('too young').",
         "Check upper bound next, then return 'ok'."],
        "def validate_age(age: int) -> str:",
        [_tc("validate_age(25)", "ok"), _tc("validate_age(200)", "invalid")],
        companies=["infosys"],
    ),
    _p(
        "py-a03", "Word Count File", "advanced", "easy",
        "Given a file path, return the number of whitespace-separated words "
        "in the file. Use a with-block so the file always closes.",
        [
            _ex("file contains 'hello world\\nfoo'", "3", "Three words total."),
        ],
        ["File exists and is readable"],
        "with open(path) as f: guarantees closing even on errors — no leaked "
        "file handles. f.read().split() splits on any whitespace, handling "
        "spaces, tabs, and newlines uniformly.",
        ["with open(path) as f: text = f.read().",
         "return len(text.split())."],
        "def word_count(path: str) -> int:",
        [_tc("word_count('/tmp/wc_test.txt')", "3")],
        companies=["tcs", "wipro"],
    ),
    _p(
        "py-a04", "CSV to Dicts", "advanced", "medium",
        "Given a CSV file path with a header row, return a list of dicts "
        "(one per row, keys from the header). Use the csv module.",
        [
            _ex("file: 'name,age\\nA,20\\nB,30'", "[{'name':'A','age':'20'},{'name':'B','age':'30'}]",
                "Header becomes keys."),
        ],
        ["Valid CSV with header"],
        "csv.DictReader maps each row to a dict using the header — no manual "
        "index juggling. The csv module also handles quoted commas correctly, "
        "which naive split(',') gets wrong.",
        ["with open(path, newline='') as f: reader = csv.DictReader(f).",
         "return list(reader)."],
        "import csv\ndef csv_to_dicts(path: str) -> list[dict]:",
        [_tc("csv_to_dicts('/tmp/csv_test.csv')", "[{'name': 'A', 'age': '20'}]")],
        companies=["flipkart"],
    ),
    _p(
        "py-a05", "Validate Email", "advanced", "medium",
        "Given a string, return True if it looks like an email "
        "(local@domain.tld): local part allows letters/digits/._-, domain "
        "allows letters/digits/-, TLD is 2+ letters. Use re.",
        [
            _ex("s = 'a.b_1@x-y.com'", "True", "Matches the pattern."),
            _ex("s = 'bad@com'", "False", "TLD too short."),
            _ex("s = 'no-at-sign'", "False", "Missing @."),
        ],
        ["0 <= len(s) <= 100"],
        "A regex like r'^[\\w.-]+@[\\w-]+\\.[a-zA-Z]{2,}$' encodes the rule "
        "declaratively. re.fullmatch anchors both ends. Regexes are precise but "
        "write-only — keep them simple and commented.",
        ["Pattern: ^[\\w.-]+@[\\w-]+\\.[a-zA-Z]{2,}$.",
         "Use re.fullmatch(pattern, s) is not None."],
        "import re\ndef is_email(s: str) -> bool:",
        [_tc("is_email('a@b.co')", "True"), _tc("is_email('bad@com')", "False")],
        companies=["amazon"],
    ),
    _p(
        "py-a06", "Extract Numbers", "advanced", "easy",
        "Given a string, return a list of all integers appearing in it "
        "(consecutive digits form one number), as ints.",
        [
            _ex("s = 'a12b3c456'", "[12, 3, 456]", "Digit runs extracted."),
            _ex("s = 'no digits'", "[]", "Empty result."),
        ],
        ["0 <= len(s) <= 10^4"],
        "re.findall(r'\\d+', s) returns every digit-run as a string; map(int, ...) "
        "converts. \\d+ ('one or more digits') is the workhorse pattern for "
        "pulling numbers out of messy text.",
        ["re.findall(r'\\d+', s) gets the strings.",
         "[int(x) for x in ...] converts each."],
        "import re\ndef extract_numbers(s: str) -> list[int]:",
        [_tc("extract_numbers('a12b3')", "[12, 3]"), _tc("extract_numbers('abc')", "[]")],
        companies=["flipkart", "amazon"],
    ),
    _p(
        "py-a07", "Team Combinations", "advanced", "medium",
        "Given a list of names and team size k, return all k-sized teams as "
        "lists, in the order itertools.combinations produces.",
        [
            _ex("names = ['a','b','c'], k = 2", "[['a','b'], ['a','c'], ['b','c']]",
                "All 3 choose 2."),
        ],
        ["0 <= k <= len(names) <= 10"],
        "itertools.combinations(names, k) yields each k-subset once, in input "
        "order — no duplicates, no manual backtracking. itertools is the "
        "standard library's combinatorics engine: learn it instead of "
        "re-implementing.",
        ["from itertools import combinations.",
         "[list(t) for t in combinations(names, k)]."],
        "from itertools import combinations\ndef teams(names: list[str], k: int) -> list[list[str]]:",
        [_tc("teams(['a','b','c'], 2)", "[['a', 'b'], ['a', 'c'], ['b', 'c']]")],
        companies=["google"],
    ),
    _p(
        "py-a08", "Timer Context Manager", "advanced", "medium",
        "Create a class Timer usable as `with Timer() as t:` that records "
        "elapsed seconds in t.elapsed after the block. Implement __enter__ "
        "and __exit__.",
        [
            _ex("with Timer() as t: pass; t.elapsed >= 0", "True", "Elapsed recorded."),
        ],
        ["No constraints"],
        "__enter__ runs at block start (record time.perf_counter()), __exit__ "
        "runs at block end (compute elapsed). Context managers guarantee cleanup "
        "— the same protocol behind files, locks, and transactions.",
        ["__enter__: self.start = perf_counter(); return self.",
         "__exit__: self.elapsed = perf_counter() - self.start."],
        "import time\nclass Timer:\n    def __enter__(self): ...\n    def __exit__(self, *args) -> None: ...",
        [_tc("(lambda t: (t.__enter__(), t.__exit__(None, None, None), t.elapsed >= 0)[-1])(Timer())", "True")],
        companies=["amazon"],
    ),
    _p(
        "py-a09", "Filter JSON Users", "advanced", "easy",
        "Given a JSON string of a list of {'name': str, 'age': int} objects, "
        "return the names of users with age >= 18.",
        [
            _ex("'[{\"name\":\"A\",\"age\":20},{\"name\":\"B\",\"age\":15}]'", "['A']",
                "Only A is adult."),
        ],
        ["Valid JSON"],
        "json.loads parses the string into Python objects; a list comprehension "
        "filters. JSON is the lingua franca of APIs — parse → filter → use is "
        "the daily workflow.",
        ["users = json.loads(s).",
         "[u['name'] for u in users if u['age'] >= 18]."],
        "import json\ndef adult_names(s: str) -> list[str]:",
        [_tc("adult_names('[{\"name\": \"A\", \"age\": 20}]')", "['A']")],
        companies=["flipkart"],
    ),
    _p(
        "py-a10", "Two Sum Indices", "advanced", "medium",
        "Given a list of ints and a target, return [i, j] (i < j) such that "
        "nums[i] + nums[j] == target. Exactly one solution exists.",
        [
            _ex("nums = [2, 7, 11, 15], target = 9", "[0, 1]", "2 + 7 = 9."),
            _ex("nums = [3, 2, 4], target = 6", "[1, 2]", "2 + 4 = 6."),
        ],
        ["2 <= len(nums) <= 10^4"],
        "A hash map stores each value's index; for x, check if target - x was "
        "seen — O(n) instead of O(n^2). 'Complement lookup in a dict' is the "
        "single most reused trick in array problems.",
        ["seen = {}; for i, x: if target - x in seen: return [seen[target-x], i].",
         "Store seen[x] = i AFTER the check (avoids using x twice)."],
        "def two_sum(nums: list[int], target: int) -> list[int]:",
        [_tc("two_sum([2, 7, 11, 15], 9)", "[0, 1]"), _tc("two_sum([3, 3], 6)", "[0, 1]")],
        companies=["amazon", "google"],
    ),
]


def get_problems(topic: str | None = None, difficulty: str | None = None) -> list[CodingProblem]:
    """Return problems, optionally filtered by topic and/or difficulty.

    Preserves bank order (basics -> advanced progression).
    """
    out = _PYTHON_BANK
    if topic is not None:
        out = [p for p in out if p.topic == topic]
    if difficulty is not None:
        out = [p for p in out if p.difficulty == difficulty]
    return list(out)


def get_problem(pid: str) -> CodingProblem | None:
    """Return the problem with the given id, or None if unknown."""
    for p in _PYTHON_BANK:
        if p.id == pid:
            return p
    return None


def list_topics() -> list[str]:
    """Return topic slugs in bank (progression) order."""
    seen: list[str] = []
    for p in _PYTHON_BANK:
        if p.topic not in seen:
            seen.append(p.topic)
    return seen

