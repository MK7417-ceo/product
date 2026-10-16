"""Outbound adapter: curated C coding problem bank.

40 ORIGINAL problems across 4 topics, ordered basics -> advanced the way a
C learner should progress: I/O and loops, then pointers, then manual memory
management, then files, recursion and bit tricks.

Every problem carries a short theory primer, hand-verified examples,
realistic constraints, hints, and C starter code (function signatures only).

Content is written originally for SkillForge — not copied from any site.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CProblem:
    id: str
    title: str
    topic: str  # basics | pointers | memory | advanced
    difficulty: str  # basic | easy | medium | hard
    description: str
    examples: list  # [{"input": str, "output": str, "explanation": str}]
    constraints: list
    theory: str  # 2-3 sentence concept explanation
    hints: list
    starter_code: dict  # {"c": ...}
    companies: list = field(default_factory=list)  # companies known to ask this pattern


def _p(pid: str, title: str, topic: str, difficulty: str, description: str,
       examples: list, constraints: list, theory: str, hints: list,
       starter_code: dict) -> CProblem:
    return CProblem(
        id=pid, title=title, topic=topic, difficulty=difficulty,
        description=description, examples=examples, constraints=constraints,
        theory=theory, hints=hints, starter_code=starter_code,
    )


def _ex(inp: str, out: str, why: str) -> dict:
    return {"input": inp, "output": out, "explanation": why}


_C_BANK: list[CProblem] = [
    # ================= BASICS (10) =================
    _p(
        "c-b01", "Multiplication Table", "basics", "basic",
        "Given an integer n, print its multiplication table from 1 to 10, "
        "one entry per line in the format 'n x i = result'.",
        [
            _ex("n = 5", "5 x 1 = 5\n5 x 2 = 10\n...\n5 x 10 = 50",
                "Each line multiplies 5 by the row number 1 through 10."),
            _ex("n = 3", "3 x 1 = 3\n3 x 2 = 6\n...\n3 x 10 = 30",
                "Same pattern with n = 3."),
        ],
        ["1 <= n <= 20"],
        "A single for loop from 1 to 10 covers the whole table; the format string "
        "\"%d x %d = %d\\n\" prints each row. This is the canonical first loop program "
        "in C and teaches printf formatting alongside iteration.",
        ["Loop i from 1 to 10 and print n, i and n * i in one printf.",
         "Watch the exact spacing: '5 x 1 = 5'."],
        {"c": "void print_table(int n);"},
    ),
    _p(
        "c-b02", "Sum of First N Numbers", "basics", "basic",
        "Given an integer n, return the sum 1 + 2 + ... + n.",
        [
            _ex("n = 5", "15", "1+2+3+4+5 = 15."),
            _ex("n = 1", "1", "A single term sums to itself."),
            _ex("n = 100", "5050", "The classic Gauss sum."),
        ],
        ["1 <= n <= 10^6"],
        "A loop accumulating into a total variable is the straightforward way, but the "
        "closed form n*(n+1)/2 is O(1) and avoids overflow worries for large n when you "
        "use long long. Comparing both teaches the loop-vs-formula tradeoff.",
        ["Use a long long accumulator so n = 10^6 does not overflow int.",
         "Bonus: implement the n*(n+1)/2 formula and compare."],
        {"c": "long long sum_n(int n);"},
    ),
    _p(
        "c-b03", "Even or Odd", "basics", "basic",
        "Given an integer n (possibly negative), return 1 if it is even and 0 if odd.",
        [
            _ex("n = 4", "1", "4 is even."),
            _ex("n = -3", "0", "-3 is odd; the sign does not matter."),
        ],
        ["-10^9 <= n <= 10^9"],
        "The modulo operator gives the remainder after division; even numbers leave "
        "remainder 0. In C, n % 2 is 0 exactly for even n (including negatives), so a "
        "single comparison decides it.",
        ["Return (n % 2 == 0).",
         "No loop needed — this is a constant-time check."],
        {"c": "int is_even(int n);"},
    ),
    _p(
        "c-b04", "Factorial", "basics", "basic",
        "Given a non-negative integer n, return n! (n factorial). 0! is defined as 1.",
        [
            _ex("n = 5", "120", "5*4*3*2*1 = 120."),
            _ex("n = 0", "1", "By definition 0! = 1."),
        ],
        ["0 <= n <= 20"],
        "Factorial grows fast — 20! already needs 64 bits, which is why the return type "
        "is long long. The iterative loop (multiply a running product) mirrors the "
        "mathematical definition directly.",
        ["Use long long for the result; int overflows at 13!.",
         "Loop i from 2 to n, multiplying into the result."],
        {"c": "long long factorial(int n);"},
    ),
    _p(
        "c-b05", "Nth Fibonacci Number", "basics", "easy",
        "Given n, return the nth Fibonacci number where fib(0) = 0, fib(1) = 1, "
        "and fib(n) = fib(n-1) + fib(n-2).",
        [
            _ex("n = 6", "8", "Sequence: 0,1,1,2,3,5,8."),
            _ex("n = 0", "0", "Base case."),
        ],
        ["0 <= n <= 50"],
        "The naive recursion recomputes the same values exponentially many times. An "
        "iterative version keeps only the last two values (a, b) and rolls them forward "
        "in O(n) time and O(1) space — the standard interview expectation.",
        ["Keep two variables a=0, b=1 and iterate n times.",
         "Each step: next = a + b, then shift a = b, b = next."],
        {"c": "long long fibonacci(int n);"},
    ),
    _p(
        "c-b06", "Palindrome Number", "basics", "easy",
        "Given a non-negative integer n, return 1 if it reads the same forwards and "
        "backwards, else 0.",
        [
            _ex("n = 121", "1", "121 reversed is 121."),
            _ex("n = 123", "0", "123 reversed is 321."),
            _ex("n = 10", "0", "Reversed 10 is 01 = 1, not equal."),
        ],
        ["0 <= n <= 10^9"],
        "Reverse the digits arithmetically (the same peel-and-build trick as digit "
        "problems) and compare with the original. No string conversion needed, which "
        "keeps it O(digits) time and O(1) space.",
        ["Build rev with rev = rev*10 + n%10 while stripping n.",
         "Compare rev with the original value."],
        {"c": "int is_palindrome(int n);"},
    ),
    _p(
        "c-b07", "Prime Check", "basics", "easy",
        "Given an integer n, return 1 if n is prime, else 0. Numbers below 2 are not prime.",
        [
            _ex("n = 13", "1", "13 has no divisors except 1 and 13."),
            _ex("n = 15", "0", "15 = 3 * 5."),
            _ex("n = 1", "0", "1 is not prime by definition."),
        ],
        ["0 <= n <= 10^9"],
        "Checking divisors only up to sqrt(n) is enough: if n = a*b with a <= b, then "
        "a <= sqrt(n), so any composite reveals a small factor early. That turns an "
        "O(n) scan into O(sqrt(n)).",
        ["Reject n < 2 immediately.",
         "Loop i from 2 while i*i <= n; return 0 on first divisor."],
        {"c": "int is_prime(int n);"},
    ),
    _p(
        "c-b08", "Sum of Digits", "basics", "basic",
        "Given a non-negative integer n, return the sum of its decimal digits.",
        [
            _ex("n = 1234", "10", "1+2+3+4 = 10."),
            _ex("n = 9", "9", "A single digit sums to itself."),
        ],
        ["0 <= n <= 10^9"],
        "Peel digits with n % 10 and drop them with n /= 10, adding each peeled digit "
        "to a running total. It is the same digit-peeling loop as counting digits, "
        "only the accumulation changes.",
        ["total += n % 10, then n /= 10, until n is 0.",
         "n = 0 should return 0, which the loop handles naturally."],
        {"c": "int digit_sum(int n);"},
    ),
    _p(
        "c-b09", "Swap Without Temp", "basics", "easy",
        "Given two integers a and b, swap their values using arithmetic (no third "
        "variable). Return the swapped pair packed as: the function writes the new "
        "values back through the pointers pa and pb.",
        [
            _ex("a = 3, b = 7", "a = 7, b = 3", "Values exchanged."),
            _ex("a = -5, b = -5", "a = -5, b = -5", "Equal values stay equal."),
        ],
        ["-10^9 <= a, b <= 10^9"],
        "The arithmetic trick (a = a+b; b = a-b; a = a-b) swaps without extra storage, "
        "but it can overflow for large values — which is why XOR swap exists. The "
        "deeper lesson: writing through pointers is how C functions return multiple "
        "values, since return gives back only one.",
        ["Use *pa and *pb to read and write the caller's variables.",
         "Arithmetic swap: *pa = *pa + *pb; *pb = *pa - *pb; *pa = *pa - *pb;"],
        {"c": "void swap_no_temp(int *pa, int *pb);"},
    ),
    _p(
        "c-b10", "Armstrong Number", "basics", "medium",
        "Given a non-negative integer n with d digits, return 1 if n equals the sum "
        "of its digits each raised to the power d (an Armstrong/narcissistic number).",
        [
            _ex("n = 153", "1", "1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153."),
            _ex("n = 123", "0", "1^3 + 2^3 + 3^3 = 36, not 123."),
        ],
        ["0 <= n <= 10^6"],
        "This combines two earlier skills: count the digits first, then peel digits "
        "again while raising each to the d-th power. It is a good check that you can "
        "compose small loops into a bigger algorithm.",
        ["First pass: count digits d. Second pass: sum += pow(digit, d).",
         "Compute integer powers with your own loop to avoid math.h float issues."],
        {"c": "int is_armstrong(int n);"},
    ),
    # ================= POINTERS (10) =================
    _p(
        "c-p01", "Swap Via Pointers", "pointers", "basic",
        "Given pointers pa and pb to two integers, swap the values they point to "
        "using a temporary variable.",
        [
            _ex("a = 3, b = 7", "a = 7, b = 3", "Values exchanged via pointers."),
        ],
        ["-10^9 <= *pa, *pb <= 10^9"],
        "Dereferencing (*pa) reaches the caller's variable, so assignments through the "
        "pointer are visible after the function returns. This is the fundamental C "
        "idiom for 'returning' more than one value.",
        ["int tmp = *pa; *pa = *pb; *pb = tmp;",
         "Never swap the pointers themselves — swap what they point to."],
        {"c": "void swap_ptr(int *pa, int *pb);"},
    ),
    _p(
        "c-p02", "Array Sum With Pointer Arithmetic", "pointers", "easy",
        "Given an int array and its length n, return the sum of its elements using "
        "only pointer arithmetic (no arr[i] indexing).",
        [
            _ex("arr = [1,2,3,4], n = 4", "10", "1+2+3+4 = 10."),
            _ex("n = 0", "0", "An empty array sums to 0."),
        ],
        ["0 <= n <= 10^5", "-10^4 <= arr[i] <= 10^4"],
        "In C, arr[i] is exactly *(arr + i): adding i to a pointer advances it by "
        "i elements, not bytes. Walking with *(p++) is the idiomatic fast traversal "
        "and demystifies what indexing really does.",
        ["int *end = arr + n; loop while p < end, adding *p++.",
         "Use long long for the sum to avoid overflow."],
        {"c": "long long array_sum_ptr(int *arr, int n);"},
    ),
    _p(
        "c-p03", "String Length Via Pointer", "pointers", "basic",
        "Given a null-terminated string s, return its length by walking a pointer "
        "until '\\0' (do not use strlen).",
        [
            _ex('s = "hello"', "5", "Five characters before the terminator."),
            _ex('s = ""', "0", "Empty string: the first char is the terminator."),
        ],
        ["0 <= length <= 10^5"],
        "C strings are just char arrays ending with '\\0'. Counting characters until "
        "that sentinel is literally what strlen does internally — writing it yourself "
        "teaches the representation every C string function relies on.",
        ["const char *p = s; while (*p) p++; return p - s;",
         "Pointer subtraction gives the element distance, i.e. the length."],
        {"c": "int str_len_ptr(const char *s);"},
    ),
    _p(
        "c-p04", "Reverse Array In Place", "pointers", "easy",
        "Given an int array and length n, reverse the array in place using two "
        "pointers moving toward each other.",
        [
            _ex("arr = [1,2,3,4,5], n = 5", "[5,4,3,2,1]",
                "Ends swap inward until they meet."),
            _ex("arr = [1,2], n = 2", "[2,1]", "A single swap."),
        ],
        ["0 <= n <= 10^5"],
        "Two pointers (left at the start, right at the end) swap and step inward; "
        "when left >= right you are done. This pattern — converging pointers — "
        "reappears in partition, palindrome and binary-search-adjacent problems.",
        ["int *l = arr, *r = arr + n - 1; while (l < r) swap and advance.",
         "n = 0 or 1 needs no work; the loop condition handles it."],
        {"c": "void reverse_array(int *arr, int n);"},
    ),
    _p(
        "c-p05", "Copy String With Pointers", "pointers", "easy",
        "Given a source string src and a destination buffer dst (large enough), copy "
        "src into dst including the '\\0' terminator, using pointer arithmetic only. "
        "Return dst.",
        [
            _ex('src = "abc"', '"abc"', "Exact copy including terminator."),
            _ex('src = ""', '""', "Only the terminator is copied."),
        ],
        ["dst has room for strlen(src)+1 chars"],
        "The classic while ((*dst++ = *src++)); copies byte-by-byte and stops after "
        "copying the '\\0' (assignment evaluates to the copied char). It is the "
        "densest C idiom there is — and a great test of understanding assignment "
        "as an expression.",
        ["Copy in a loop until you have copied the '\\0' itself.",
         "Return the ORIGINAL dst pointer, not the advanced one."],
        {"c": "char *str_copy_ptr(char *dst, const char *src);"},
    ),
    _p(
        "c-p06", "Find Max Via Pointer Traversal", "pointers", "easy",
        "Given an int array of length n (n >= 1), return the maximum element using "
        "pointer traversal (no indexing).",
        [
            _ex("arr = [3,1,4,1,5], n = 5", "5", "5 is the largest."),
            _ex("arr = [-2,-9], n = 2", "-2", "-2 beats -9."),
        ],
        ["1 <= n <= 10^5", "-10^9 <= arr[i] <= 10^9"],
        "Seed max with the first element (*arr), then walk the rest comparing. "
        "Starting from arr[0] instead of 0/INT_MIN keeps the code correct for "
        "all-negative arrays — a classic edge-case lesson.",
        ["int max = *arr; then walk p from arr+1 to arr+n.",
         "Update max whenever *p is larger."],
        {"c": "int array_max_ptr(int *arr, int n);"},
    ),
    _p(
        "c-p07", "Double Pointer Basics", "pointers", "medium",
        "Given a pointer to a pointer pp (int **pp), set the integer it ultimately "
        "points to to the value 42. (That is: **pp = 42.)",
        [
            _ex("x = 0, p = &x, pp = &p", "x becomes 42",
                "Two levels of indirection still reach x."),
        ],
        ["pp, *pp are valid non-null pointers"],
        "Each * peels one level: *pp is the int*, **pp is the int. Double pointers "
        "appear whenever a function must change the caller's pointer itself (e.g. "
        "inserting at a list head) — so reading **pp fluently matters.",
        ["**pp = 42; is the entire body.",
         "Think: *pp gives the inner pointer, * again gives the int."],
        {"c": "void set_via_double_ptr(int **pp);"},
    ),
    _p(
        "c-p08", "Count Vowels Using Pointer", "pointers", "easy",
        "Given a null-terminated string s, count vowels (a,e,i,o,u, both cases) by "
        "walking a pointer through the string.",
        [
            _ex('s = "Hello World"', "3", "e, o, o."),
            _ex('s = "rhythm"', "0", "No vowels."),
        ],
        ["0 <= length <= 10^5"],
        "Walking with a pointer and testing each char against a vowel set combines "
        "pointer traversal with a small classification helper. It is the same shape "
        "as most 'scan and count' string problems.",
        ["Write a tiny is_vowel(char c) helper.",
         "Advance the pointer until *p == '\\0'."],
        {"c": "int count_vowels_ptr(const char *s);"},
    ),
    _p(
        "c-p09", "Rotate Array Right By K", "pointers", "medium",
        "Given an int array of length n and k, rotate the array right by k positions "
        "in place (k may exceed n).",
        [
            _ex("arr = [1,2,3,4,5], k = 2", "[4,5,1,2,3]",
                "Last two elements move to the front."),
            _ex("arr = [1,2,3], k = 3", "[1,2,3]", "Full rotation = no change."),
        ],
        ["0 <= n <= 10^5", "0 <= k <= 10^9"],
        "The three-reversal trick: reverse the whole array, then reverse the first k "
        "and the rest. Each element moves O(1) times, giving O(n) time and O(1) space — "
        "better than shifting one-by-one k times.",
        ["Reduce k with k %= n first; handle n <= 1 as a no-op.",
         "Reuse your in-place reverse on the three segments."],
        {"c": "void rotate_right(int *arr, int n, int k);"},
    ),
    _p(
        "c-p10", "String Compare With Pointers", "pointers", "medium",
        "Implement strcmp: given s1 and s2, walk both with pointers and return <0, 0, "
        "or >0 according as s1 is lexicographically less than, equal to, or greater "
        "than s2.",
        [
            _ex('s1="abc", s2="abd"', "negative", "'c' < 'd' at position 3."),
            _ex('s1="abc", s2="abc"', "0", "Identical strings."),
            _ex('s1="b", s2="abc"', "positive", "'b' > 'a' at position 1."),
        ],
        ["0 <= lengths <= 10^5"],
        "Compare char-by-char; the first difference decides, and if one string ends "
        "first the '\\0' (value 0) compares smaller than any letter. Returning "
        "(*p1 - *p2) as unsigned chars is how the real strcmp avoids sign pitfalls.",
        ["Loop while *p1 && *p1 == *p2, advancing both.",
         "Return (unsigned char)*p1 - (unsigned char)*p2."],
        {"c": "int str_cmp_ptr(const char *s1, const char *s2);"},
    ),
    # ================= MEMORY (10) =================
    _p(
        "c-m01", "Dynamic Array Allocation", "memory", "easy",
        "Allocate an int array of n elements with malloc, fill it with values "
        "1..n, and return the pointer. (The caller will free it.)",
        [
            _ex("n = 4", "[1,2,3,4]", "Heap array holding 1..4."),
            _ex("n = 1", "[1]", "Single element."),
        ],
        ["1 <= n <= 10^6"],
        "malloc(n * sizeof(int)) requests raw bytes from the heap and returns void*, "
        "which converts to int*. Unlike stack arrays, the size can be decided at "
        "runtime — the whole point of dynamic allocation.",
        ["Check the malloc result for NULL before writing.",
         "Fill with arr[i] = i + 1."],
        {"c": "int *make_range(int n);"},
    ),
    _p(
        "c-m02", "Sum of Malloc'd Array", "memory", "easy",
        "Given a heap-allocated int array and its length n, return the sum of its "
        "elements. (Do not free inside — the caller owns it.)",
        [
            _ex("arr = [5,5,5], n = 3", "15", "Straight sum."),
        ],
        ["1 <= n <= 10^6"],
        "Ownership discipline: whoever allocates frees. A function that only reads "
        "the array must not free it, or the caller gets a use-after-free. Clear "
        "ownership rules prevent most heap bugs.",
        ["Simple loop accumulating into long long.",
         "Do NOT call free here."],
        {"c": "long long heap_sum(const int *arr, int n);"},
    ),
    _p(
        "c-m03", "Struct Student Records", "memory", "medium",
        "Define struct Student { char name[50]; int roll; float marks; }. Write a "
        "function that allocates one Student on the heap, fills it from the "
        "arguments, and returns the pointer.",
        [
            _ex('name="Asha", roll=7, marks=91.5', "Student{7, Asha, 91.5}",
                "Heap struct with copied fields."),
        ],
        ["name shorter than 50 chars"],
        "Structs group related data; malloc(sizeof(struct Student)) reserves one on "
        "the heap. Use strncpy for the name to avoid overflow, and access fields "
        "through -> on the pointer.",
        ["malloc(sizeof(struct Student)), check NULL.",
         "strncpy(s->name, name, 49); s->name[49] = '\\0'; then assign roll/marks."],
        {"c": "struct Student { char name[50]; int roll; float marks; };\nstruct Student *make_student(const char *name, int roll, float marks);"},
    ),
    _p(
        "c-m04", "Growing Array With Realloc", "memory", "medium",
        "Given a heap array, its current length n, and new length m > n, grow it "
        "with realloc preserving old values, zero-fill the new slots, and return "
        "the (possibly moved) pointer.",
        [
            _ex("arr=[1,2], n=2, m=4", "[1,2,0,0]", "Old values kept, new are 0."),
        ],
        ["1 <= n < m <= 10^6"],
        "realloc may move the block, so you must use its return value — the old "
        "pointer is invalid afterward. Assign to a temp first: if realloc fails it "
        "returns NULL but the original block is still valid.",
        ["int *tmp = realloc(arr, m * sizeof(int)); check tmp != NULL.",
         "Zero indices n..m-1, then return tmp."],
        {"c": "int *grow_array(int *arr, int n, int m);"},
    ),
    _p(
        "c-m05", "2D Matrix With Malloc", "memory", "medium",
        "Allocate a rows x cols int matrix as an array of row pointers (int**), "
        "initialize every cell to 0, and return it.",
        [
            _ex("rows=2, cols=3", "[[0,0,0],[0,0,0]]", "Zeroed 2x3 matrix."),
        ],
        ["1 <= rows, cols <= 500"],
        "A true 2D dynamic array needs rows+1 allocations: one for the pointer array, "
        "one per row. Freeing must mirror this in reverse. (A single flat block is "
        "faster in practice, but the pointer-array form teaches the layout.)",
        ["Allocate int** of rows pointers, then each row of cols ints.",
         "On any NULL, free what you allocated so far (or keep it simple: assume success in tests)."],
        {"c": "int **make_matrix(int rows, int cols);"},
    ),
    _p(
        "c-m06", "Linked List Node Creation", "memory", "medium",
        "Define struct Node { int data; struct Node *next; }. Write a function that "
        "creates a node with the given data, next set to NULL, and returns it.",
        [
            _ex("data = 10", "Node{10, NULL}", "Fresh heap node."),
        ],
        ["-10^9 <= data <= 10^9"],
        "Every linked structure starts here: one malloc'd node with its link "
        "initialized. Forgetting next = NULL is the #1 beginner list bug — the "
        "dangling pointer then poisons every traversal.",
        ["malloc(sizeof(struct Node)); check NULL.",
         "Set data and next = NULL before returning."],
        {"c": "struct Node { int data; struct Node *next; };\nstruct Node *new_node(int data);"},
    ),
    _p(
        "c-m07", "Safe Free Pattern", "memory", "easy",
        "Given int **pp (pointer to a heap pointer), free the memory and set *pp to "
        "NULL so a later accidental free is harmless.",
        [
            _ex("pp -> [1,2,3]", "freed, *pp == NULL", "No dangling pointer left."),
        ],
        ["*pp was malloc'd or NULL"],
        "Freeing does not change the pointer — it still points at released memory "
        "(dangling). Setting it to NULL right after is the standard guard: free(NULL) "
        "is a safe no-op, so double-free becomes impossible.",
        ["free(*pp); *pp = NULL;",
         "Guard: only free if *pp != NULL (free(NULL) is safe anyway)."],
        {"c": "void safe_free(int **pp);"},
    ),
    _p(
        "c-m08", "Struct With Dynamic String", "memory", "medium",
        "Define struct Person { char *name; int age; }. Allocate a Person on the "
        "heap AND a heap copy of the name string, fill both, return the Person*.",
        [
            _ex('name="Ravi", age=30', 'Person{"Ravi", 30}',
                "Both struct and string live on the heap."),
        ],
        ["name shorter than 1000 chars"],
        "Two allocations, two frees: the struct and its owned string have independent "
        "lifetimes. strdup (or malloc+strcpy) copies the caller's string so the "
        "Person stays valid after the caller's buffer disappears.",
        ["malloc Person, then p->name = malloc(strlen(name)+1); strcpy it.",
         "The +1 is for the terminator — forgetting it is a classic heap overflow."],
        {"c": "struct Person { char *name; int age; };\nstruct Person *make_person(const char *name, int age);"},
    ),
    _p(
        "c-m09", "Copy Array With Malloc", "memory", "easy",
        "Given an int array src of length n, allocate a new heap array, copy all "
        "elements into it, and return the new pointer.",
        [
            _ex("src=[4,5,6], n=3", "[4,5,6] (new allocation)",
                "Equal contents, different memory."),
        ],
        ["1 <= n <= 10^6"],
        "A deep copy duplicates the data so the two arrays live independent lives. "
        "memcpy(dst, src, n * sizeof(int)) does it in one call — the byte count "
        "argument is where size mistakes hide, so double-check it.",
        ["malloc(n * sizeof(int)), check NULL, then memcpy.",
         "Return the new pointer; src is untouched."],
        {"c": "int *copy_array(const int *src, int n);"},
    ),
    _p(
        "c-m10", "Fix the Leak", "memory", "hard",
        "You are given a function that builds a heap array of n ints (values 0..n-1) "
        "but the harness cannot free it. Change the design: write build_range that "
        "returns the array AND document the contract — instead, implement a paired "
        "destroy_range(int *arr) that frees it, proving the leak is fixed by "
        "construction.",
        [
            _ex("n = 3", "build -> [0,1,2]; destroy frees it",
                "Allocate/free are symmetric."),
        ],
        ["1 <= n <= 10^6"],
        "The real fix for leaks is API design: every allocating function gets a "
        "documented destroy partner, and ownership is explicit. Tools like "
        "valgrind verify, but the habit — 'who frees this?' asked at write time — "
        "prevents leaks before they exist.",
        ["build_range: malloc + fill 0..n-1, return pointer.",
         "destroy_range: free(arr); (NULL-safe)."],
        {"c": "int *build_range(int n);\nvoid destroy_range(int *arr);"},
    ),
    # ================= ADVANCED (10) =================
    _p(
        "c-a01", "Copy File", "advanced", "medium",
        "Copy the entire contents of text file src_path to dst_path using FILE* "
        "streams. Return 0 on success, -1 if either file cannot be opened.",
        [
            _ex('src="a.txt"("hi")', 'dst gets "hi", return 0', "Byte-identical copy."),
            _ex('src="missing.txt"', "return -1", "Open failure reported."),
        ],
        ["files are text, any size"],
        "fopen/fgetc/fputc/fclose is the portable file-copy loop; checking both "
        "fopen results and closing both streams even on the happy path is the "
        "discipline. Return codes (not crashes) report errors in C.",
        ["Open src \"r\", dst \"w\"; if either NULL return -1.",
         "Loop c = fgetc(fin); while c != EOF: fputc(c, fout). Close both."],
        {"c": "int copy_file(const char *src_path, const char *dst_path);"},
    ),
    _p(
        "c-a02", "Count Lines in File", "advanced", "easy",
        "Given a path, count '\\n' characters in the file and return the count. "
        "Return -1 if the file cannot be opened.",
        [
            _ex('file = "a\\nb\\n"', "2", "Two newline characters."),
            _ex('missing file', "-1", "Open failure."),
        ],
        ["text file"],
        "Counting newlines approximates line count (a file not ending in newline has "
        "one more line than newlines — note the edge case). Streaming char-by-char "
        "uses O(1) memory regardless of file size.",
        ["fopen \"r\", NULL check -> return -1.",
         "Count fgetc(c) == '\\n', then fclose."],
        {"c": "int count_lines(const char *path);"},
    ),
    _p(
        "c-a03", "Recursive Power", "advanced", "easy",
        "Compute base^exp recursively (exp >= 0). Use the definition "
        "pow(b, e) = b * pow(b, e-1), pow(b, 0) = 1.",
        [
            _ex("base=2, exp=10", "1024", "2^10."),
            _ex("base=5, exp=0", "1", "Anything^0 = 1."),
        ],
        ["0 <= exp <= 30", "-10 <= base <= 10"],
        "Recursion needs a base case (exp == 0) and a step that shrinks toward it. "
        "This linear version is O(exp) calls; the fast version (exponentiation by "
        "squaring) halves exp each call for O(log exp) — a good follow-up.",
        ["if (exp == 0) return 1; return base * power(base, exp - 1);",
         "Return type long long for headroom."],
        {"c": "long long power_rec(int base, int exp);"},
    ),
    _p(
        "c-a04", "Tower of Hanoi Move Count", "advanced", "medium",
        "Return the minimum number of moves to solve Tower of Hanoi with n disks. "
        "(You do not need to print the moves.)",
        [
            _ex("n = 3", "7", "Classic 3-disk solution takes 7 moves."),
            _ex("n = 1", "1", "One disk, one move."),
        ],
        ["1 <= n <= 30"],
        "The recurrence T(n) = 2*T(n-1) + 1 solves to 2^n - 1: move n-1 disks aside, "
        "move the largest, move the n-1 back. Recognizing the recurrence is the "
        "skill; the closed form makes it O(1).",
        ["Return (1LL << n) - 1 for n <= 30.",
         "Or recurse: hanoi(n) = 2*hanoi(n-1) + 1."],
        {"c": "long long hanoi_moves(int n);"},
    ),
    _p(
        "c-a05", "Count Set Bits", "advanced", "easy",
        "Given an unsigned int n, return how many 1-bits it contains "
        "(its population count).",
        [
            _ex("n = 13 (1101)", "3", "Three ones."),
            _ex("n = 0", "0", "No bits set."),
        ],
        ["0 <= n <= 2^32 - 1"],
        "n & (n-1) clears the lowest set bit, so looping until n is 0 iterates "
        "exactly popcount times — O(k) for k set bits instead of O(32). This "
        "bit trick is an interview staple.",
        ["while (n) { count++; n &= n - 1; }",
         "Use unsigned int so shifts and & behave predictably."],
        {"c": "int popcount(unsigned int n);"},
    ),
    _p(
        "c-a06", "Reverse Bits", "advanced", "medium",
        "Given a 32-bit unsigned int, return the value with its bits reversed "
        "(bit 0 <-> bit 31, etc.).",
        [
            _ex("n = 1 (…0001)", "2147483648 (1000…)", "Bit 0 moves to bit 31."),
            _ex("n = 0", "0", "All zeros stay zero."),
        ],
        ["0 <= n < 2^32"],
        "Build the answer by shifting it left and OR-ing in the lowest bit of n, "
        "then shifting n right — 32 iterations. It is the bit-level mirror of "
        "reversing decimal digits.",
        ["Loop 32 times: rev = (rev << 1) | (n & 1); n >>= 1;",
         "Use unsigned int / uint32_t throughout."],
        {"c": "unsigned int reverse_bits(unsigned int n);"},
    ),
    _p(
        "c-a07", "Single Number With XOR", "advanced", "medium",
        "Given an array where every element appears exactly twice except one, "
        "return the single one using O(1) extra space.",
        [
            _ex("arr=[4,1,2,1,2], n=5", "4", "4 is the loner."),
            _ex("arr=[7], n=1", "7", "Single element."),
        ],
        ["1 <= n <= 10^5"],
        "XOR cancels pairs (a^a=0) and 0^x=x, so XOR-ing everything leaves the "
        "loner. Order does not matter (xor is commutative) — the whole array "
        "folds down in one pass with one variable.",
        ["int x = 0; for each: x ^= arr[i]; return x;",
         "No hash map needed — that would be O(n) space."],
        {"c": "int single_number(int *arr, int n);"},
    ),
    _p(
        "c-a08", "Binary String to Decimal", "advanced", "easy",
        "Given a string of '0'/'1' characters, return its decimal value.",
        [
            _ex('s = "1011"', "11", "8+2+1 = 11."),
            _ex('s = "0"', "0", "Zero."),
        ],
        ["1 <= length <= 31"],
        "Horner's method: result = result*2 + (c - '0') scans left to right in one "
        "pass. It avoids pow() and floating point entirely — the same pattern "
        "parses decimal and hex strings too.",
        ["Walk the chars: val = val * 2 + (*p - '0').",
         "31 bits fit in a signed int; still, long long is safe."],
        {"c": "long long bin_to_dec(const char *s);"},
    ),
    _p(
        "c-a09", "Write and Read Struct", "advanced", "medium",
        "Given a struct Student {int roll; float marks;} and a path, write n "
        "students to a binary file with fwrite, then read them back into a "
        "malloc'd array and return it. Return NULL on any failure.",
        [
            _ex("students=[{1,90.0},{2,80.0}]", "round-trips identically",
                "Binary write + read preserves the structs."),
        ],
        ["1 <= n <= 1000"],
        "fwrite(&s, sizeof(struct Student), 1, f) dumps raw memory — fast but "
        "non-portable (padding, endianness). For a learning exercise it teaches "
        "binary I/O; production code would serialize field-by-field.",
        ["Write loop with fwrite, close, reopen \"rb\", malloc + fread loop.",
         "Check every fopen/fread/fwrite return."],
        {"c": "struct Student { int roll; float marks; };\nstruct Student *roundtrip_students(const struct Student *arr, int n, const char *path);"},
    ),
    _p(
        "c-a10", "Sum Command-Line Args", "advanced", "easy",
        "Implement the body of main-style logic: given argc and argv (argv[0] is "
        "the program name), parse argv[1..] as integers with atoi and return "
        "their sum.",
        [
            _ex('argv = ["prog","3","4","5"]', "12", "3+4+5."),
            _ex('argv = ["prog"]', "0", "No numbers given."),
        ],
        ["0 <= argc <= 100"],
        "main(int argc, char *argv[]) is how programs receive input from the shell. "
        "argv[0] is the program name by convention, so user args start at index 1 — "
        "the classic off-by-one to watch for.",
        ["Loop i from 1 to argc-1: sum += atoi(argv[i]);",
         "atoi is fine here; strtol is the robust production choice."],
        {"c": "int sum_argv(int argc, char *argv[]);"},
    ),
]




_COMPANIES: dict[str, list[str]] = {
    "c-a01": ['tcs', 'infosys', 'wipro'],
    "c-a02": ['tcs', 'accenture'],
    "c-a03": ['infosys', 'tcs', 'wipro'],
    "c-a04": ['amazon', 'microsoft', 'tcs'],
    "c-a05": ['google', 'amazon', 'microsoft'],
    "c-a06": ['google', 'amazon', 'flipkart'],
    "c-a07": ['amazon', 'google', 'flipkart'],
    "c-a08": ['tcs', 'infosys'],
    "c-a09": ['tcs', 'wipro'],
    "c-a10": ['tcs', 'infosys', 'accenture'],
    "c-b01": ['tcs', 'infosys', 'wipro'],
    "c-b02": ['tcs', 'infosys', 'accenture'],
    "c-b03": ['tcs', 'wipro', 'tech-mahindra'],
    "c-b04": ['infosys', 'tcs', 'cognizant'],
    "c-b05": ['tcs', 'infosys', 'wipro'],
    "c-b06": ['tcs', 'infosys', 'accenture'],
    "c-b07": ['infosys', 'wipro', 'tcs'],
    "c-b08": ['tcs', 'tech-mahindra', 'cognizant'],
    "c-b09": ['infosys', 'tcs', 'hcl'],
    "c-b10": ['tcs', 'wipro', 'accenture'],
    "c-m01": ['tcs', 'infosys', 'amazon'],
    "c-m02": ['tcs', 'wipro'],
    "c-m03": ['infosys', 'tcs', 'accenture'],
    "c-m04": ['amazon', 'microsoft', 'tcs'],
    "c-m05": ['amazon', 'tcs', 'infosys'],
    "c-m06": ['tcs', 'infosys', 'wipro'],
    "c-m07": ['microsoft', 'amazon', 'tcs'],
    "c-m08": ['amazon', 'tcs'],
    "c-m09": ['tcs', 'infosys'],
    "c-m10": ['amazon', 'microsoft', 'google'],
    "c-p01": ['tcs', 'infosys', 'wipro'],
    "c-p02": ['infosys', 'tcs', 'accenture'],
    "c-p03": ['tcs', 'wipro', 'tech-mahindra'],
    "c-p04": ['tcs', 'infosys', 'amazon'],
    "c-p05": ['infosys', 'wipro', 'tcs'],
    "c-p06": ['tcs', 'accenture', 'cognizant'],
    "c-p07": ['amazon', 'microsoft', 'tcs'],
    "c-p08": ['tcs', 'infosys', 'wipro'],
    "c-p09": ['amazon', 'tcs', 'infosys'],
    "c-p10": ['microsoft', 'tcs', 'wipro'],
}

for _prob in _C_BANK:
    _prob.companies = _COMPANIES.get(_prob.id, [])

def get_problems(topic: str | None = None, difficulty: str | None = None) -> list[CProblem]:
    """Return problems, optionally filtered by topic and/or difficulty.

    Preserves bank order (basics -> advanced progression).
    """
    out = _C_BANK
    if topic is not None:
        out = [p for p in out if p.topic == topic]
    if difficulty is not None:
        out = [p for p in out if p.difficulty == difficulty]
    return list(out)


def get_problem(pid: str) -> CProblem | None:
    """Return the problem with the given id, or None if unknown."""
    for p in _C_BANK:
        if p.id == pid:
            return p
    return None


def list_topics() -> list[str]:
    """Return topic slugs in bank (progression) order."""
    seen: list[str] = []
    for p in _C_BANK:
        if p.topic not in seen:
            seen.append(p.topic)
    return seen
