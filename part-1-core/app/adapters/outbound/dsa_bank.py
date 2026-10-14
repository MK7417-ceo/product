"""Outbound adapter: curated DSA problem bank (TakeUForward-style progression).

30 ORIGINAL problems across 8 topics, ordered basics -> trees the way a
beginner should learn them. Every problem carries a short theory primer,
hand-verified examples, realistic constraints, hints, and starter code
(function signatures only) in Python, C++, Java and C.

Content is written originally for SkillForge — not copied from any site.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DSAProblem:
    id: str
    title: str
    topic: str  # basics | arrays | strings | linked-list | recursion | sorting | stack-queue | trees
    difficulty: str  # basic | easy | medium | hard
    description: str
    examples: list  # [{"input": str, "output": str, "explanation": str}]
    constraints: list
    theory: str  # 2-3 sentence concept explanation
    hints: list
    starter_code: dict  # {"python": ..., "cpp": ..., "java": ..., "c": ...}


def _p(pid: str, title: str, topic: str, difficulty: str, description: str,
       examples: list, constraints: list, theory: str, hints: list,
       starter_code: dict) -> DSAProblem:
    return DSAProblem(
        id=pid, title=title, topic=topic, difficulty=difficulty,
        description=description, examples=examples, constraints=constraints,
        theory=theory, hints=hints, starter_code=starter_code,
    )


def _ex(inp: str, out: str, why: str) -> dict:
    return {"input": inp, "output": out, "explanation": why}


_DSA_BANK: list[DSAProblem] = [
    # ================= BASICS (5) =================
    _p(
        "dsa-b01", "Print a Star Pyramid", "basics", "basic",
        "Given an integer n, print a right-angled triangle of stars with n rows, "
        "where row i (1-indexed) contains exactly i star characters.",
        [
            _ex("n = 3", "*\n**\n***",
                "Row 1 has 1 star, row 2 has 2 stars, row 3 has 3 stars."),
            _ex("n = 1", "*", "A single row with a single star."),
        ],
        ["1 <= n <= 50"],
        "Patterns teach nested loops: the outer loop picks the row, the inner loop "
        "prints that row's characters. Once you can control 'how many per row', you "
        "can draw any shape by changing the inner loop's rule.",
        ["Use two loops: outer for rows 1..n, inner for stars 1..i.",
         "Print a newline after each inner loop finishes."],
        {
            "python": "def print_pyramid(n: int) -> None:",
            "cpp": "void printPyramid(int n);",
            "java": "public void printPyramid(int n)",
            "c": "void print_pyramid(int n);",
        },
    ),
    _p(
        "dsa-b02", "Count Digits", "basics", "basic",
        "Given an integer n, return how many digits it has. The number 0 has 1 digit.",
        [
            _ex("n = 12345", "5", "12345 has five digits."),
            _ex("n = 0", "1", "Zero is treated as a single digit."),
            _ex("n = 7", "1", "Single-digit numbers return 1."),
        ],
        ["0 <= n <= 10^9"],
        "Repeatedly dividing by 10 strips one digit at a time, so the number of "
        "divisions until zero equals the digit count. This 'peel one digit' trick "
        "is the foundation of most number problems.",
        ["Handle n = 0 as a special case before the loop.",
         "Loop while n > 0: increment a counter, then do n //= 10."],
        {
            "python": "def count_digits(n: int) -> int:",
            "cpp": "int countDigits(int n);",
            "java": "public int countDigits(int n)",
            "c": "int count_digits(int n);",
        },
    ),
    _p(
        "dsa-b03", "Reverse a Number", "basics", "basic",
        "Given an integer n, return the number formed by reversing its digits. "
        "Leading zeros of the reversed form disappear (120 becomes 21).",
        [
            _ex("n = 1234", "4321", "Digits read backwards."),
            _ex("n = 120", "21", "The trailing zero vanishes after reversal."),
        ],
        ["0 <= n <= 10^9"],
        "Build the answer digit by digit: take the last digit with n % 10, append it "
        "with rev = rev * 10 + digit, then drop it with n //= 10. It is the same "
        "'peel one digit' idea as counting, but constructive instead of just counting.",
        ["Extract the last digit with n % 10.",
         "Grow the answer with rev = rev * 10 + digit."],
        {
            "python": "def reverse_number(n: int) -> int:",
            "cpp": "int reverseNumber(int n);",
            "java": "public int reverseNumber(int n)",
            "c": "int reverse_number(int n);",
        },
    ),
    _p(
        "dsa-b04", "Greatest Common Divisor", "basics", "basic",
        "Given two positive integers a and b, return their greatest common divisor "
        "(the largest number that divides both).",
        [
            _ex("a = 12, b = 18", "6",
                "Common divisors of 12 and 18 are 1, 2, 3, 6; the greatest is 6."),
            _ex("a = 7, b = 5", "1", "7 and 5 share no divisor except 1."),
        ],
        ["1 <= a, b <= 10^6"],
        "Euclid's algorithm: gcd(a, b) = gcd(b, a % b), because any common divisor of "
        "a and b also divides the remainder. Repeating this shrinks the numbers until "
        "one becomes zero, running in logarithmic time.",
        ["Try the Euclidean algorithm: gcd(a, b) = gcd(b, a % b).",
         "Base case: gcd(a, 0) = a."],
        {
            "python": "def gcd(a: int, b: int) -> int:",
            "cpp": "int gcd(int a, int b);",
            "java": "public int gcd(int a, int b)",
            "c": "int gcd(int a, int b);",
        },
    ),
    _p(
        "dsa-b05", "Armstrong Number", "basics", "basic",
        "A number is Armstrong if the sum of its digits, each raised to the power of "
        "the digit count, equals the number itself. Return true if n is Armstrong.",
        [
            _ex("n = 153", "true", "1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153."),
            _ex("n = 123", "false", "1^3 + 2^3 + 3^3 = 36, which is not 123."),
        ],
        ["0 <= n <= 10^5"],
        "Combine digit extraction (n % 10) with a power sum: count the digits first, "
        "then raise each digit to that power and add them up. It bundles two basic "
        "number tricks into a single check.",
        ["First count the digits, then sum digit**count.",
         "153 is the classic example: 1^3+5^3+3^3 = 153."],
        {
            "python": "def is_armstrong(n: int) -> bool:",
            "cpp": "bool isArmstrong(int n);",
            "java": "public boolean isArmstrong(int n)",
            "c": "bool is_armstrong(int n);",
        },
    ),

    # ================= ARRAYS (6) =================
    _p(
        "dsa-a01", "Largest Element in Array", "arrays", "easy",
        "Given an array of integers, return the largest element.",
        [
            _ex("arr = [3, 7, 2, 9, 4]", "9", "9 is the maximum value."),
            _ex("arr = [5]", "5", "A single element is trivially the largest."),
        ],
        ["1 <= n <= 10^5", "-10^9 <= arr[i] <= 10^9"],
        "Track the best answer seen so far in one pass: start with the first element "
        "and update whenever you find something bigger. This single-pass 'champion' "
        "pattern beats sorting's O(n log n).",
        ["Initialize max_val with arr[0], not 0 (beware negatives!).",
         "One loop is enough — no sorting needed."],
        {
            "python": "def largest(arr: list[int]) -> int:",
            "cpp": "int largest(vector<int>& arr);",
            "java": "public int largest(int[] arr)",
            "c": "int largest(int* arr, int n);",
        },
    ),
    _p(
        "dsa-a02", "Second Largest Element", "arrays", "easy",
        "Given an array, return the second largest distinct element. "
        "If no such element exists, return -1.",
        [
            _ex("arr = [3, 7, 2, 9, 4]", "7", "Largest is 9, next distinct is 7."),
            _ex("arr = [10, 10, 5]", "5", "Distinct values are 10 and 5."),
            _ex("arr = [5, 5, 5]", "-1", "Only one distinct value exists."),
        ],
        ["1 <= n <= 10^5", "-10^9 <= arr[i] <= 10^9"],
        "Extend the champion pattern with two trackers: largest and second largest. "
        "Skip values equal to the largest so duplicates cannot fake a 'second' place.",
        ["Keep two variables: largest and second.",
         "Ignore duplicates of the largest value."],
        {
            "python": "def second_largest(arr: list[int]) -> int:",
            "cpp": "int secondLargest(vector<int>& arr);",
            "java": "public int secondLargest(int[] arr)",
            "c": "int second_largest(int* arr, int n);",
        },
    ),
    _p(
        "dsa-a03", "Check if Array is Sorted", "arrays", "easy",
        "Given an array, return true if it is sorted in non-decreasing order "
        "(each element <= the next).",
        [
            _ex("arr = [1, 2, 3, 4]", "true", "Every pair is in order."),
            _ex("arr = [1, 3, 2]", "false", "3 > 2 breaks the order."),
            _ex("arr = [2, 2, 3]", "true", "Equal neighbours are allowed."),
        ],
        ["1 <= n <= 10^5", "-10^9 <= arr[i] <= 10^9"],
        "Sorted means every adjacent pair is in order, so checking all n-1 pairs in "
        "one pass is both necessary and sufficient. Many algorithms assume sorted "
        "input, making this a useful guard check.",
        ["Compare each element with the next one.",
         "Return false at the first inversion you find."],
        {
            "python": "def is_sorted(arr: list[int]) -> bool:",
            "cpp": "bool isSorted(vector<int>& arr);",
            "java": "public boolean isSorted(int[] arr)",
            "c": "bool is_sorted(int* arr, int n);",
        },
    ),
    _p(
        "dsa-a04", "Remove Duplicates from Sorted Array", "arrays", "medium",
        "Given a sorted array, remove duplicates in-place so the first k positions "
        "hold the unique values in order. Return k (the count of unique elements).",
        [
            _ex("arr = [1, 1, 2, 2, 3]", "3",
                "First 3 positions become [1, 2, 3]."),
            _ex("arr = [1, 2, 3]", "3", "No duplicates; nothing changes."),
        ],
        ["1 <= n <= 10^5", "-10^9 <= arr[i] <= 10^9", "arr is sorted ascending"],
        "Two pointers: a slow writer index and a fast reader. Because the array is "
        "sorted, duplicates sit together, so the writer only advances when the reader "
        "finds a new value. O(1) extra space.",
        ["Use a write pointer starting at 1.",
         "Copy arr[read] only when it differs from arr[write-1]."],
        {
            "python": "def remove_duplicates(arr: list[int]) -> int:",
            "cpp": "int removeDuplicates(vector<int>& arr);",
            "java": "public int removeDuplicates(int[] arr)",
            "c": "int remove_duplicates(int* arr, int n);",
        },
    ),
    _p(
        "dsa-a05", "Rotate Array by K", "arrays", "medium",
        "Given an array and an integer k, rotate the array to the right by k steps "
        "(elements falling off the end reappear at the front).",
        [
            _ex("arr = [1, 2, 3, 4, 5], k = 2", "[4, 5, 1, 2, 3]",
                "The last 2 elements move to the front."),
            _ex("arr = [1, 2, 3], k = 4", "[3, 1, 2]",
                "k = 4 is the same as k = 1 for length 3."),
        ],
        ["1 <= n <= 10^5", "0 <= k <= 10^9", "-10^9 <= arr[i] <= 10^9"],
        "Rotating by k equals rotating by k % n. The reversal trick does it in O(1) "
        "space: reverse the whole array, then reverse the first k elements and the "
        "rest separately.",
        ["Reduce k with k % n first.",
         "Try: reverse all, reverse first k, reverse the rest."],
        {
            "python": "def rotate(arr: list[int], k: int) -> None:",
            "cpp": "void rotate(vector<int>& arr, int k);",
            "java": "public void rotate(int[] arr, int k)",
            "c": "void rotate(int* arr, int n, int k);",
        },
    ),
    _p(
        "dsa-a06", "Move Zeros to End", "arrays", "easy",
        "Given an array, move all zeros to the end while keeping the relative order "
        "of the non-zero elements. Do it in-place.",
        [
            _ex("arr = [0, 1, 0, 3, 12]", "[1, 3, 12, 0, 0]",
                "Non-zeros keep their order; zeros collect at the end."),
            _ex("arr = [0, 0, 1]", "[1, 0, 0]", "Single non-zero moves to front."),
        ],
        ["1 <= n <= 10^5", "-10^9 <= arr[i] <= 10^9"],
        "Another two-pointer partition: the writer collects non-zeros at the front in "
        "order, then the tail is filled with zeros. Stable and in-place.",
        ["Copy every non-zero to the next write position.",
         "Fill the remaining positions with zeros."],
        {
            "python": "def move_zeros(arr: list[int]) -> None:",
            "cpp": "void moveZeros(vector<int>& arr);",
            "java": "public void moveZeros(int[] arr)",
            "c": "void move_zeros(int* arr, int n);",
        },
    ),

    # ================= STRINGS (4) =================
    _p(
        "dsa-s01", "Reverse a String", "strings", "easy",
        "Given a string, return a new string with its characters in reverse order.",
        [
            _ex('s = "hello"', '"olleh"', "Characters read backwards."),
            _ex('s = "abc"', '"cba"', "First and last swap positions."),
        ],
        ["1 <= len(s) <= 10^5"],
        "Two pointers from both ends swapping inward is the classic in-place reversal: "
        "each swap fixes two positions and they meet in the middle.",
        ["Swap s[left] and s[right], then move both inward.",
         "Stop when left >= right."],
        {
            "python": "def reverse_string(s: str) -> str:",
            "cpp": "string reverseString(string s);",
            "java": "public String reverseString(String s)",
            "c": "void reverse_string(char* s);",
        },
    ),
    _p(
        "dsa-s02", "Palindrome Check", "strings", "easy",
        "Given a string, return true if it reads the same forwards and backwards.",
        [
            _ex('s = "madam"', "true", "Reversed it is still 'madam'."),
            _ex('s = "hello"', "false", "'hello' reversed is 'olleh'."),
            _ex('s = "a"', "true", "A single character is trivially a palindrome."),
        ],
        ["1 <= len(s) <= 10^5"],
        "A palindrome equals its own reverse, but comparing s[i] with s[n-1-i] directly "
        "avoids building the reversed copy, using O(1) extra space.",
        ["Compare characters from both ends moving inward.",
         "A mismatch at any position means not a palindrome."],
        {
            "python": "def is_palindrome(s: str) -> bool:",
            "cpp": "bool isPalindrome(string s);",
            "java": "public boolean isPalindrome(String s)",
            "c": "bool is_palindrome(char* s);",
        },
    ),
    _p(
        "dsa-s03", "Valid Anagram", "strings", "easy",
        "Given two strings s and t, return true if t is an anagram of s "
        "(same characters with the same counts).",
        [
            _ex('s = "listen", t = "silent"', "true",
                "Both use l,i,s,t,e,n exactly once."),
            _ex('s = "hello", t = "world"', "false",
                "Character counts differ."),
        ],
        ["1 <= len(s), len(t) <= 10^5", "lowercase English letters only"],
        "Anagrams have identical character-frequency maps. Counting with a fixed "
        "array of 26 (for lowercase letters) beats sorting's O(n log n).",
        ["Different lengths can never be anagrams — check first.",
         "Count characters of s, subtract characters of t; all zeros means anagram."],
        {
            "python": "def is_anagram(s: str, t: str) -> bool:",
            "cpp": "bool isAnagram(string s, string t);",
            "java": "public boolean isAnagram(String s, String t)",
            "c": "bool is_anagram(char* s, char* t);",
        },
    ),
    _p(
        "dsa-s04", "Longest Common Prefix", "strings", "easy",
        "Given an array of strings, return the longest prefix shared by all of them. "
        'Return "" if there is no common prefix.',
        [
            _ex('strs = ["flower", "flow", "flight"]', '"fl"',
                '"fl" starts all three; "flo" fails on "flight".'),
            _ex('strs = ["dog", "racecar", "car"]', '""',
                "No shared starting character."),
            _ex('strs = ["alone"]', '"alone"', "One string: the whole string is the prefix."),
        ],
        ["1 <= n <= 200", "0 <= len(strs[i]) <= 200", "lowercase English letters"],
        "Take the first string as the candidate prefix and shrink it while any other "
        "string doesn't start with it. The prefix can only shrink, so one pass over "
        "the array suffices.",
        ["Start with the whole first string as the prefix.",
         "While strs[i] doesn't start with the prefix, chop its last character."],
        {
            "python": "def longest_common_prefix(strs: list[str]) -> str:",
            "cpp": "string longestCommonPrefix(vector<string>& strs);",
            "java": "public String longestCommonPrefix(String[] strs)",
            "c": "char* longest_common_prefix(char** strs, int n);",
        },
    ),

    # ================= LINKED LIST (3) =================
    _p(
        "dsa-l01", "Traverse a Linked List", "linked-list", "basic",
        "Given the head of a singly linked list, return its values as an array, "
        "in order from head to tail.",
        [
            _ex("head = 1 -> 2 -> 3", "[1, 2, 3]", "Values in traversal order."),
            _ex("head = 7", "[7]", "A single node yields one value."),
        ],
        ["0 <= nodes <= 10^4", "-10^9 <= node.val <= 10^9"],
        "A linked list is walked with a moving pointer: start at head, record the "
        "value, follow .next until None. This traversal is the foundation every other "
        "list operation builds on.",
        ["Use a current pointer starting at head.",
         "Loop while current is not None, appending current.val."],
        {
            "python": "# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\ndef traverse(head) -> list[int]:",
            "cpp": "// struct ListNode { int val; ListNode* next; };\nvector<int> traverse(ListNode* head);",
            "java": "// class ListNode { int val; ListNode next; }\npublic List<Integer> traverse(ListNode head)",
            "c": "// struct ListNode { int val; struct ListNode* next; };\nint* traverse(struct ListNode* head, int* out_n);",
        },
    ),
    _p(
        "dsa-l02", "Reverse a Linked List", "linked-list", "medium",
        "Given the head of a singly linked list, reverse it in-place and return "
        "the new head.",
        [
            _ex("head = 1 -> 2 -> 3", "3 -> 2 -> 1", "All links flipped."),
            _ex("head = 1 -> 2", "2 -> 1", "Two nodes swap direction."),
        ],
        ["0 <= nodes <= 10^4", "-10^9 <= node.val <= 10^9"],
        "Walk the list flipping each .next pointer backwards as you go — keep prev, "
        "curr, and next so no link is lost mid-flip. The last node becomes the new head.",
        ["Track prev, curr, and save nxt = curr.next before rewiring.",
         "Set curr.next = prev, then advance prev and curr."],
        {
            "python": "# class ListNode: ... (val, next)\ndef reverse_list(head):",
            "cpp": "// struct ListNode { int val; ListNode* next; };\nListNode* reverseList(ListNode* head);",
            "java": "// class ListNode { int val; ListNode next; }\npublic ListNode reverseList(ListNode head)",
            "c": "// struct ListNode { int val; struct ListNode* next; };\nstruct ListNode* reverse_list(struct ListNode* head);",
        },
    ),
    _p(
        "dsa-l03", "Middle of Linked List", "linked-list", "easy",
        "Given the head of a singly linked list, return the middle node. "
        "For even length, return the second middle node.",
        [
            _ex("head = 1 -> 2 -> 3 -> 4 -> 5", "3", "Middle of five nodes."),
            _ex("head = 1 -> 2 -> 3 -> 4", "3", "Second middle of four nodes."),
        ],
        ["1 <= nodes <= 10^4", "-10^9 <= node.val <= 10^9"],
        "The tortoise-and-hare trick: move one pointer one step and another two steps; "
        "when the fast one reaches the end, the slow one sits exactly in the middle. "
        "One pass, no length counting needed.",
        ["Use slow and fast pointers starting at head.",
         "Move slow by 1, fast by 2; when fast ends, slow is the middle."],
        {
            "python": "# class ListNode: ... (val, next)\ndef middle_node(head):",
            "cpp": "// struct ListNode { int val; ListNode* next; };\nListNode* middleNode(ListNode* head);",
            "java": "// class ListNode { int val; ListNode next; }\npublic ListNode middleNode(ListNode head)",
            "c": "// struct ListNode { int val; struct ListNode* next; };\nstruct ListNode* middle_node(struct ListNode* head);",
        },
    ),

    # ================= RECURSION (3) =================
    _p(
        "dsa-r01", "Factorial", "recursion", "basic",
        "Given a non-negative integer n, return n! (the product of 1..n). "
        "By definition, 0! = 1. Use recursion.",
        [
            _ex("n = 5", "120", "5*4*3*2*1 = 120."),
            _ex("n = 0", "1", "Base case by definition."),
        ],
        ["0 <= n <= 12"],
        "Recursion needs a base case and a shrinking step: factorial(n) = n * "
        "factorial(n-1) with factorial(0) = 1. Each call handles one multiplication "
        "and trusts recursion for the rest.",
        ["Base case: n <= 1 returns 1.",
         "Recursive step: return n * factorial(n - 1)."],
        {
            "python": "def factorial(n: int) -> int:",
            "cpp": "int factorial(int n);",
            "java": "public int factorial(int n)",
            "c": "int factorial(int n);",
        },
    ),
    _p(
        "dsa-r02", "Fibonacci Number", "recursion", "easy",
        "Return the nth Fibonacci number, where fib(0) = 0, fib(1) = 1, and "
        "fib(n) = fib(n-1) + fib(n-2). Use recursion.",
        [
            _ex("n = 6", "8", "Sequence: 0,1,1,2,3,5,8."),
            _ex("n = 2", "1", "fib(2) = fib(1) + fib(0) = 1."),
        ],
        ["0 <= n <= 20"],
        "fib(n) = fib(n-1) + fib(n-2) mirrors the definition directly — but naive "
        "recursion recomputes the same values exponentially many times, which is why "
        "memoization or iteration matters later.",
        ["Base cases: fib(0) = 0, fib(1) = 1.",
         "Return fib(n-1) + fib(n-2)."],
        {
            "python": "def fib(n: int) -> int:",
            "cpp": "int fib(int n);",
            "java": "public int fib(int n)",
            "c": "int fib(int n);",
        },
    ),
    _p(
        "dsa-r03", "Sum of First N Numbers", "recursion", "basic",
        "Given n, return 1 + 2 + ... + n using recursion.",
        [
            _ex("n = 5", "15", "1+2+3+4+5 = 15."),
            _ex("n = 1", "1", "Base case."),
        ],
        ["1 <= n <= 10^4"],
        "sum(n) = n + sum(n-1) with sum(1) = 1 — the simplest recursive shape after "
        "factorial, showing how a problem reduces to a smaller copy of itself.",
        ["Base case: n == 1 returns 1.",
         "Return n + sum_of_n(n - 1)."],
        {
            "python": "def sum_n(n: int) -> int:",
            "cpp": "int sumN(int n);",
            "java": "public int sumN(int n)",
            "c": "int sum_n(int n);",
        },
    ),

    # ================= SORTING (3) =================
    _p(
        "dsa-so01", "Bubble Sort", "sorting", "easy",
        "Given an array, sort it in ascending order using bubble sort. "
        "Modify the array in-place.",
        [
            _ex("arr = [5, 3, 8, 4, 2]", "[2, 3, 4, 5, 8]", "Fully sorted."),
            _ex("arr = [1, 2, 3]", "[1, 2, 3]", "Already sorted; unchanged."),
        ],
        ["1 <= n <= 10^4", "-10^9 <= arr[i] <= 10^9"],
        "Repeatedly bubble the largest unsorted element to the end by swapping adjacent "
        "out-of-order pairs. After each pass one more position is final — and an "
        "early-exit flag makes already-sorted input O(n).",
        ["Inner loop swaps arr[j] and arr[j+1] when out of order.",
         "After pass i, the last i elements are already sorted."],
        {
            "python": "def bubble_sort(arr: list[int]) -> None:",
            "cpp": "void bubbleSort(vector<int>& arr);",
            "java": "public void bubbleSort(int[] arr)",
            "c": "void bubble_sort(int* arr, int n);",
        },
    ),
    _p(
        "dsa-so02", "Insertion Sort", "sorting", "easy",
        "Given an array, sort it in ascending order using insertion sort. "
        "Modify the array in-place.",
        [
            _ex("arr = [5, 3, 8, 4, 2]", "[2, 3, 4, 5, 8]", "Fully sorted."),
            _ex("arr = [2, 1]", "[1, 2]", "Two elements swap once."),
        ],
        ["1 <= n <= 10^4", "-10^9 <= arr[i] <= 10^9"],
        "Grow a sorted prefix one element at a time: take the next unsorted card and "
        "slide it left into place, like sorting playing cards in your hand. Excellent "
        "for nearly-sorted data.",
        ["For each i, store key = arr[i] and shift larger elements right.",
         "Insert the key into the gap you opened."],
        {
            "python": "def insertion_sort(arr: list[int]) -> None:",
            "cpp": "void insertionSort(vector<int>& arr);",
            "java": "public void insertionSort(int[] arr)",
            "c": "void insertion_sort(int* arr, int n);",
        },
    ),
    _p(
        "dsa-so03", "Merge Sort", "sorting", "medium",
        "Given an array, sort it in ascending order using merge sort. "
        "Implement the merge step carefully.",
        [
            _ex("arr = [6, 3, 8, 5, 2]", "[2, 3, 5, 6, 8]", "Fully sorted."),
            _ex("arr = [4, 1]", "[1, 4]", "Split, sort, merge."),
        ],
        ["1 <= n <= 10^5", "-10^9 <= arr[i] <= 10^9"],
        "Divide and conquer: split the array in half, sort each half recursively, then "
        "merge two sorted halves in linear time. The merge step is the heart; the "
        "recursion guarantees O(n log n).",
        ["Split at mid, sort both halves, then merge.",
         "Merge with three pointers: i, j for the halves, k for output."],
        {
            "python": "def merge_sort(arr: list[int]) -> None:",
            "cpp": "void mergeSort(vector<int>& arr);",
            "java": "public void mergeSort(int[] arr)",
            "c": "void merge_sort(int* arr, int n);",
        },
    ),

    # ================= STACK / QUEUE (3) =================
    _p(
        "dsa-q01", "Implement Stack using Array", "stack-queue", "easy",
        "Implement a stack (LIFO) with push(x), pop(), top(), and isEmpty() "
        "operations using an array/list as the underlying storage.",
        [
            _ex("push(1), push(2), top()", "2", "Last pushed is on top."),
            _ex("push(1), push(2), pop(), top()", "1",
                "pop() removed 2; 1 is now on top."),
        ],
        ["0 <= operations <= 10^4", "-10^9 <= x <= 10^9"],
        "A stack is LIFO — last in, first out. An array with append/pop at one end "
        "gives amortized O(1) operations and is the simplest correct implementation.",
        ["Use a list; push = append, pop() removes the last.",
         "top() returns the last element without removing it."],
        {
            "python": "class Stack:\n    def push(self, x: int) -> None: ...\n    def pop(self) -> int: ...\n    def top(self) -> int: ...\n    def is_empty(self) -> bool: ...",
            "cpp": "class Stack {\n public:\n  void push(int x);\n  int pop();\n  int top();\n  bool isEmpty();\n};",
            "java": "class Stack {\n    public void push(int x) {}\n    public int pop() { return 0; }\n    public int top() { return 0; }\n    public boolean isEmpty() { return false; }\n}",
            "c": "void push(int x);\nint pop(void);\nint top(void);\nbool is_empty(void);",
        },
    ),
    _p(
        "dsa-q02", "Valid Parentheses", "stack-queue", "easy",
        "Given a string containing only ()[]{} characters, return true if every "
        "opening bracket is closed by the correct type in the correct order.",
        [
            _ex('s = "()[]{}"', "true", "Each pair matches in order."),
            _ex('s = "([)]"', "false", "Interleaved brackets never match."),
            _ex('s = "{[]}"', "true", "Properly nested."),
        ],
        ["1 <= len(s) <= 10^4"],
        "A stack tracks nesting: push openings, and on a closing bracket the top must "
        "be its match. Any mismatch or leftover means invalid. This is the canonical "
        "stack application.",
        ["Push every opening bracket.",
         "On a closing bracket, the stack top must match — else false."],
        {
            "python": "def is_valid(s: str) -> bool:",
            "cpp": "bool isValid(string s);",
            "java": "public boolean isValid(String s)",
            "c": "bool is_valid(char* s);",
        },
    ),
    _p(
        "dsa-q03", "Queue using Two Stacks", "stack-queue", "medium",
        "Implement a FIFO queue using two LIFO stacks, supporting enqueue(x) "
        "and dequeue().",
        [
            _ex("enqueue(1), enqueue(2), dequeue()", "1",
                "First in is first out."),
            _ex("enqueue(1), enqueue(2), dequeue(), dequeue()", "2",
                "Order preserved across operations."),
        ],
        ["0 <= operations <= 10^4", "-10^9 <= x <= 10^9"],
        "Two stacks reverse order twice: push everything into stack A, then pour into "
        "stack B to flip the order, making the oldest element pop first. Amortized O(1) "
        "per operation.",
        ["Keep an input stack and an output stack.",
         "Move elements to the output stack only when it is empty."],
        {
            "python": "class Queue:\n    def enqueue(self, x: int) -> None: ...\n    def dequeue(self) -> int: ...",
            "cpp": "class Queue {\n public:\n  void enqueue(int x);\n  int dequeue();\n};",
            "java": "class Queue {\n    public void enqueue(int x) {}\n    public int dequeue() { return 0; }\n}",
            "c": "void enqueue(int x);\nint dequeue(void);",
        },
    ),

    # ================= TREES (3) =================
    _p(
        "dsa-t01", "Binary Tree Traversals", "trees", "basic",
        "Given the root of a binary tree, return its inorder, preorder, and "
        "postorder traversals as three arrays.",
        [
            _ex("root = [1, 2, 3]  (1 with left 2, right 3)",
                "inorder=[2, 1, 3], preorder=[1, 2, 3], postorder=[2, 3, 1]",
                "The three orders differ only in when the root is visited."),
        ],
        ["0 <= nodes <= 10^4", "-10^9 <= node.val <= 10^9"],
        "The three traversals differ only in when the root is visited relative to its "
        "subtrees — inorder (left, root, right) famously yields sorted order for a BST. "
        "Master one recursive template and the others are one-line changes.",
        ["Write a recursive helper visiting left and right subtrees.",
         "Inorder: left, root, right; preorder: root first; postorder: root last."],
        {
            "python": "# class TreeNode: ... (val, left, right)\ndef traversals(root) -> dict:",
            "cpp": "// struct TreeNode { int val; TreeNode *left, *right; };\n// return inorder, preorder, postorder via output vectors",
            "java": "// class TreeNode { int val; TreeNode left, right; }\n// fill inorder, preorder, postorder lists",
            "c": "// struct TreeNode { int val; struct TreeNode *left, *right; };\n// fill output arrays in inorder / preorder / postorder",
        },
    ),
    _p(
        "dsa-t02", "Maximum Depth of Binary Tree", "trees", "easy",
        "Given the root of a binary tree, return the number of nodes on the longest "
        "path from the root down to any leaf.",
        [
            _ex("root = [3, 9, 20, null, null, 15, 7]", "3",
                "Longest path: 3 -> 20 -> 15 (3 nodes)."),
            _ex("root = []", "0", "An empty tree has depth 0."),
        ],
        ["0 <= nodes <= 10^4", "-10^9 <= node.val <= 10^9"],
        "Depth is 1 plus the deeper of the two subtrees: depth(node) = 1 + "
        "max(depth(left), depth(right)), with an empty tree at depth 0. Post-order "
        "recursion in its purest form.",
        ["Base case: None has depth 0.",
         "Return 1 + max of left and right depths."],
        {
            "python": "# class TreeNode: ... (val, left, right)\ndef max_depth(root) -> int:",
            "cpp": "// struct TreeNode { int val; TreeNode *left, *right; };\nint maxDepth(TreeNode* root);",
            "java": "// class TreeNode { int val; TreeNode left, right; }\npublic int maxDepth(TreeNode root)",
            "c": "// struct TreeNode { int val; struct TreeNode *left, *right; };\nint max_depth(struct TreeNode* root);",
        },
    ),
    _p(
        "dsa-t03", "Inorder Traversal", "trees", "easy",
        "Given the root of a binary tree, return the inorder traversal of its "
        "values (left subtree, node, right subtree).",
        [
            _ex("root = [1, null, 2, 3]  (1 with right 2; 2 with left 3)",
                "[1, 3, 2]", "Visit 1, then left-subtree of 2 which is [3], then 2."),
            _ex("root = [1, 2, 3]", "[2, 1, 3]", "Left, root, right."),
        ],
        ["0 <= nodes <= 10^4", "-10^9 <= node.val <= 10^9"],
        "Inorder visits left subtree, node, then right subtree — for a binary search "
        "tree this produces values in ascending order, which is why it is the "
        "most-used traversal.",
        ["Recurse left, record the value, recurse right.",
         "An iterative version uses an explicit stack."],
        {
            "python": "# class TreeNode: ... (val, left, right)\ndef inorder(root) -> list[int]:",
            "cpp": "// struct TreeNode { int val; TreeNode *left, *right; };\nvector<int> inorder(TreeNode* root);",
            "java": "// class TreeNode { int val; TreeNode left, right; }\npublic List<Integer> inorder(TreeNode root)",
            "c": "// struct TreeNode { int val; struct TreeNode *left, *right; };\nint* inorder(struct TreeNode* root, int* out_n);",
        },
    ),
]


def get_problems(topic: str | None = None, difficulty: str | None = None) -> list[DSAProblem]:
    """Return problems, optionally filtered by topic and/or difficulty.

    Preserves bank order (TakeUForward-style progression).
    """
    out = _DSA_BANK
    if topic is not None:
        out = [p for p in out if p.topic == topic]
    if difficulty is not None:
        out = [p for p in out if p.difficulty == difficulty]
    return list(out)


def get_problem(pid: str) -> DSAProblem | None:
    """Return the problem with the given id, or None if unknown."""
    for p in _DSA_BANK:
        if p.id == pid:
            return p
    return None


def list_topics() -> list[str]:
    """Return topic slugs in bank (progression) order."""
    seen: list[str] = []
    for p in _DSA_BANK:
        if p.topic not in seen:
            seen.append(p.topic)
    return seen
