"""Outbound adapter: curated JavaScript coding problem bank.

40 ORIGINAL problems across 4 topics, ordered basics -> interview practice.
DOM-free on purpose: everything runs in Node or any JS console, focusing on
language mechanics (closures, promises, array methods) that interviews test.

Every problem carries a short theory primer, hand-verified examples,
realistic constraints, hints, and JavaScript starter code.

Content is written originally for SkillForge — not copied from any site.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class JSProblem:
    id: str
    title: str
    topic: str  # basics | logic | advanced | practice
    difficulty: str  # basic | easy | medium | hard
    description: str
    examples: list  # [{"input": str, "output": str, "explanation": str}]
    constraints: list
    theory: str  # 2-3 sentence concept explanation
    hints: list
    starter_code: dict  # {"javascript": ...}
    companies: list = field(default_factory=list)  # companies known to ask this pattern


def _p(pid: str, title: str, topic: str, difficulty: str, description: str,
       examples: list, constraints: list, theory: str, hints: list,
       starter_code: dict) -> JSProblem:
    return JSProblem(
        id=pid, title=title, topic=topic, difficulty=difficulty,
        description=description, examples=examples, constraints=constraints,
        theory=theory, hints=hints, starter_code=starter_code,
    )


def _ex(inp: str, out: str, why: str) -> dict:
    return {"input": inp, "output": out, "explanation": why}


_JS_BANK: list[JSProblem] = [
    # ================= BASICS (10) =================
    _p(
        "js-b01", "Sum of Array", "basics", "basic",
        "Given an array of numbers, return their sum. An empty array sums to 0.",
        [
            _ex("[1, 2, 3, 4]", "10", "Straight addition."),
            _ex("[]", "0", "Empty array edge case."),
        ],
        ["0 <= arr.length <= 10^5"],
        "Array.prototype.reduce folds an array into one value with an accumulator — "
        "the functional alternative to a for loop. Passing 0 as the initial value "
        "handles the empty array cleanly.",
        ["arr.reduce((sum, x) => sum + x, 0)",
         "The 0 initial value is what makes [] return 0."],
        {"javascript": "function arraySum(arr) {\n  // return the sum\n}"},
    ),
    _p(
        "js-b02", "FizzBuzz", "basics", "basic",
        "Given n, return an array of strings 1..n where multiples of 3 become "
        "\"Fizz\", of 5 become \"Buzz\", and of both become \"FizzBuzz\".",
        [
            _ex("n = 5", '["1","2","Fizz","4","Buzz"]', "3->Fizz, 5->Buzz."),
            _ex("n = 15 (last)", '"FizzBuzz"', "15 is a multiple of both."),
        ],
        ["1 <= n <= 10^4"],
        "Check the combined case (15) FIRST — testing 3 before 15 would print "
        "just \"Fizz\". Ordering conditions from most-specific to least is the "
        "lesson this old interview chestnut teaches.",
        ["Build the string: let s = ''; if 3 add Fizz, if 5 add Buzz, if empty use i.",
         "Push s into the result array each iteration."],
        {"javascript": "function fizzBuzz(n) {\n  // return array of strings\n}"},
    ),
    _p(
        "js-b03", "Reverse a String", "basics", "basic",
        "Given a string s, return it reversed.",
        [
            _ex('"hello"', '"olleh"', "Characters in reverse order."),
            _ex('""', '""', "Empty string stays empty."),
        ],
        ["0 <= s.length <= 10^5"],
        "Strings are immutable, so split('') -> reverse() -> join('') goes through "
        "an array. The manual loop version (build from the end) teaches the same "
        "two-pointer idea used in array reversal.",
        ["[...s].reverse().join('') handles unicode better than split('').",
         "Manual: let r=''; for (let i=s.length-1;i>=0;i--) r+=s[i];"],
        {"javascript": "function reverseString(s) {\n  // return reversed string\n}"},
    ),
    _p(
        "js-b04", "Factorial", "basics", "basic",
        "Given non-negative n, return n!. 0! = 1.",
        [
            _ex("n = 5", "120", "5*4*3*2*1."),
            _ex("n = 0", "1", "Definition."),
        ],
        ["0 <= n <= 20"],
        "A loop multiplying a running product is the iterative shape; the recursive "
        "version (n * factorial(n-1)) shows the base-case + shrink pattern. JS "
        "numbers are doubles, so results stay exact up to 20! here.",
        ["let r = 1; for (let i = 2; i <= n; i++) r *= i;",
         "Recursive: return n <= 1 ? 1 : n * factorial(n - 1);"],
        {"javascript": "function factorial(n) {\n  // return n!\n}"},
    ),
    _p(
        "js-b05", "Largest in Array", "basics", "basic",
        "Given a non-empty array of numbers, return the largest.",
        [
            _ex("[3, 1, 4, 1, 5]", "5", "5 wins."),
            _ex("[-2, -9, -1]", "-1", "-1 is the least negative."),
        ],
        ["1 <= arr.length <= 10^5"],
        "Seed max with arr[0] (not 0) so all-negative arrays work. Math.max(...arr) "
        "is the one-liner, but the spread fails on huge arrays (call-stack limits) — "
        "the loop is the safe general solution.",
        ["let m = arr[0]; for (const x of arr) if (x > m) m = x;",
         "for...of is the clean modern loop for values."],
        {"javascript": "function findMax(arr) {\n  // return largest number\n}"},
    ),
    _p(
        "js-b06", "Palindrome String", "basics", "easy",
        "Given a string s, return true if it reads the same forwards and backwards "
        "(case-sensitive), else false.",
        [
            _ex('"racecar"', "true", "Mirrors perfectly."),
            _ex('"hello"', "false", "o != h."),
        ],
        ["0 <= s.length <= 10^5"],
        "Compare s with its reverse, or walk two pointers from both ends — the "
        "pointer version exits early on mismatch (O(1) best case) instead of always "
        "building the full reversed string.",
        ["Two pointers: i=0, j=s.length-1; while i<j compare and move inward.",
         "Empty and single-char strings are palindromes."],
        {"javascript": "function isPalindrome(s) {\n  // return true/false\n}"},
    ),
    _p(
        "js-b07", "Count Vowels", "basics", "easy",
        "Given a string s, count vowels (a, e, i, o, u, case-insensitive).",
        [
            _ex('"Hello World"', "3", "e, o, o."),
            _ex('"rhythm"', "0", "Sometimes-y is not a vowel here."),
        ],
        ["0 <= s.length <= 10^5"],
        "Lowercase once, then test membership in a vowel Set — Set.has is O(1), and "
        "the pattern (normalize -> classify -> count) is the template for most "
        "character-counting problems.",
        ["const vowels = new Set('aeiou');",
         "Loop chars: if (vowels.has(ch.toLowerCase())) count++."],
        {"javascript": "function countVowels(s) {\n  // return vowel count\n}"},
    ),
    _p(
        "js-b08", "Remove Duplicates", "basics", "easy",
        "Given an array, return a new array with duplicates removed, keeping the "
        "first occurrence order.",
        [
            _ex("[1, 2, 2, 3, 1]", "[1, 2, 3]", "First occurrences kept."),
            _ex("[]", "[]", "Empty in, empty out."),
        ],
        ["0 <= arr.length <= 10^5"],
        "[...new Set(arr)] is the idiomatic one-liner: Set keeps insertion order and "
        "drops repeats. Knowing WHY it works (SameValueZero equality, ordered "
        "iteration) turns a trick into understanding.",
        ["return [...new Set(arr)];",
         "Manual version: track seen in a Set, push unseen items."],
        {"javascript": "function removeDuplicates(arr) {\n  // return deduped array\n}"},
    ),
    _p(
        "js-b09", "Celsius to Fahrenheit", "basics", "basic",
        "Given Celsius c, return Fahrenheit: F = C * 9/5 + 32. Round to 1 decimal.",
        [
            _ex("c = 0", "32", "Freezing point."),
            _ex("c = 100", "212", "Boiling point."),
            _ex("c = 37", "98.6", "Body temperature."),
        ],
        ["-273.15 <= c <= 1000"],
        "Floating-point arithmetic plus rounding: Math.round(x * 10) / 10 rounds to "
        "one decimal. toFixed(1) returns a STRING — a classic gotcha when the "
        "caller expects a number.",
        ["const f = c * 9/5 + 32; return Math.round(f * 10) / 10;",
         "Order matters: multiply before dividing to keep precision."],
        {"javascript": "function celsiusToFahrenheit(c) {\n  // return Fahrenheit rounded to 1 decimal\n}"},
    ),
    _p(
        "js-b10", "Sum of Even Numbers", "basics", "easy",
        "Given an array of integers, return the sum of the even ones.",
        [
            _ex("[1, 2, 3, 4]", "6", "2 + 4."),
            _ex("[1, 3, 5]", "0", "No evens."),
        ],
        ["0 <= arr.length <= 10^5"],
        "filter keeps the evens, reduce sums them — chaining reads like a pipeline. "
        "It is the canonical demo of combining array methods instead of one "
        "mega-loop with nested ifs.",
        ["arr.filter(x => x % 2 === 0).reduce((s, x) => s + x, 0)",
         "=== avoids the type-coercion surprises of ==."],
        {"javascript": "function sumEvens(arr) {\n  // return sum of even numbers\n}"},
    ),
    # ================= LOGIC (10) =================
    _p(
        "js-l01", "Title Case Words", "logic", "easy",
        "Given a sentence, return it with each word's first letter capitalized and "
        "the rest lowercase.",
        [
            _ex('"hello world"', '"Hello World"', "Each word capitalized."),
            _ex('"jAVAsCRIPT is FUN"', '"Javascript Is Fun"', "Rest lowercased."),
        ],
        ["0 <= s.length <= 10^4"],
        "split(' ') -> map(word => word[0].toUpperCase() + word.slice(1).toLowerCase()) "
        "-> join(' '). Handling word[0] on empty words (from double spaces) needs a "
        "guard — real-world strings are messy.",
        ["Map each word, guarding empty strings.",
         "Join back with single spaces."],
        {"javascript": "function titleCase(s) {\n  // return title-cased sentence\n}"},
    ),
    _p(
        "js-l02", "Anagram Check", "logic", "easy",
        "Given two strings, return true if one is an anagram of the other "
        "(same letters, same counts). Case-sensitive.",
        [
            _ex('"listen", "silent"', "true", "Same letters rearranged."),
            _ex('"hello", "world"', "false", "Different letters."),
        ],
        ["0 <= lengths <= 10^5"],
        "Sorting both and comparing is O(n log n) and simple; counting chars in a "
        "Map is O(n). Either way the KEY insight: anagrams are equal exactly when "
        "their sorted forms (or count maps) match.",
        ["Sort: [...a].sort().join('') === [...b].sort().join('')",
         "Quick reject: different lengths can never be anagrams."],
        {"javascript": "function isAnagram(a, b) {\n  // return true/false\n}"},
    ),
    _p(
        "js-l03", "Flatten One Level", "logic", "easy",
        "Given an array that may contain sub-arrays one level deep, return a flat "
        "array with those sub-arrays spliced in.",
        [
            _ex("[1, [2, 3], 4]", "[1, 2, 3, 4]", "One level flattened."),
            _ex("[[1], [2], [3]]", "[1, 2, 3]", "All sub-arrays."),
        ],
        ["nesting depth <= 1"],
        "Array.prototype.flat() with no args flattens exactly one level — but "
        "writing it manually (concat in a loop, or reduce) teaches what the "
        "built-in does. flat(Infinity) is the deep version.",
        ["return arr.flat();  // one level",
         "Manual: arr.reduce((acc, x) => acc.concat(x), []);"],
        {"javascript": "function flattenOne(arr) {\n  // return flattened array\n}"},
    ),
    _p(
        "js-l04", "Chunk Array", "logic", "easy",
        "Given an array and size k, split it into sub-arrays of length k "
        "(the last may be shorter).",
        [
            _ex("[1,2,3,4,5], k=2", "[[1,2],[3,4],[5]]", "Last chunk is short."),
            _ex("[1,2], k=5", "[[1,2]]", "One chunk smaller than k."),
        ],
        ["1 <= k <= 10^4"],
        "slice(i, i+k) stepping i by k never mutates the original — slice is the "
        "non-destructive twin of splice. Chunking appears in pagination and batch "
        "processing, so it is genuinely useful.",
        ["for (let i = 0; i < arr.length; i += k) out.push(arr.slice(i, i + k));",
         "slice clamps automatically when i+k overshoots."],
        {"javascript": "function chunk(arr, k) {\n  // return array of chunks\n}"},
    ),
    _p(
        "js-l05", "Most Frequent Character", "logic", "medium",
        "Given a string s, return the character that appears most often. If tied, "
        "return the one that appears first in s.",
        [
            _ex('"hello"', '"l"', "l appears twice, first among ties."),
            _ex('"aabb"', '"a"', "Tie -> first in string wins."),
        ],
        ["1 <= s.length <= 10^5"],
        "Count into a Map in one pass, then find the max — but iterate the STRING "
        "(not the Map) for the max pass so ties resolve by first appearance. Map "
        "preserves insertion order, which is the other way to get tie-breaking "
        "right.",
        ["First pass: counts.set(ch, (counts.get(ch) || 0) + 1).",
         "Second pass over s: track the char with the highest count."],
        {"javascript": "function mostFrequent(s) {\n  // return most frequent char\n}"},
    ),
    _p(
        "js-l06", "Valid Parentheses", "logic", "medium",
        "Given a string of brackets ()[]{} , return true if every opener is closed "
        "by the right closer in the right order.",
        [
            _ex('"()[]{}"', "true", "All matched."),
            _ex('"(]"', "false", "Wrong closer."),
            _ex('"([)]"', "false", "Interleaved, not nested."),
        ],
        ["0 <= s.length <= 10^4"],
        "A stack models nesting perfectly: push openers, pop on closers and check "
        "the pair. A closing bracket with an empty stack, or a non-empty stack at "
        "the end, both mean invalid.",
        ["Map closers to openers: {')':'(', ']':'[', '}':'{'}",
         "Push openers; on closer, pop and compare."],
        {"javascript": "function isValid(s) {\n  // return true/false\n}"},
    ),
    _p(
        "js-l07", "Two Sum", "logic", "medium",
        "Given an array of numbers and a target, return the indices [i, j] of two "
        "distinct elements that add to target. Exactly one solution exists.",
        [
            _ex("[2,7,11,15], target=9", "[0,1]", "2 + 7 = 9."),
            _ex("[3,3], target=6", "[0,1]", "The two 3s."),
        ],
        ["2 <= arr.length <= 10^4"],
        "For each x, the partner needed is target - x: a Map from value to index "
        "finds it in O(1), giving O(n) total. Checking the map BEFORE inserting x "
        "prevents using the same element twice.",
        ["Map seen values to indices as you go.",
         "For x at i: if seen.has(target - x) return [seen.get(target-x), i]."],
        {"javascript": "function twoSum(arr, target) {\n  // return [i, j]\n}"},
    ),
    _p(
        "js-l08", "Merge Sorted Arrays", "logic", "easy",
        "Given two sorted arrays, return one sorted array containing all elements.",
        [
            _ex("[1,3,5], [2,4,6]", "[1,2,3,4,5,6]", "Interleaved merge."),
            _ex("[], [1]", "[1]", "Empty left array."),
        ],
        ["0 <= lengths <= 10^5"],
        "Two pointers (one per array) always take the smaller head — O(n+m), the "
        "merge step of merge sort. [...a, ...b].sort() works but is O(n log n) and "
        "misses the point in interviews.",
        ["While both have items: push the smaller head, advance that pointer.",
         "Then append whichever array has leftovers."],
        {"javascript": "function mergeSorted(a, b) {\n  // return merged sorted array\n}"},
    ),
    _p(
        "js-l09", "Rotation Check", "logic", "medium",
        "Given strings a and b of equal length, return true if b is a rotation of "
        "a (e.g. 'waterbottle' rotated).",
        [
            _ex('"waterbottle", "erbottlewat"', "true", "A rotation."),
            _ex('"abc", "acb"', "false", "Not a rotation."),
        ],
        ["lengths equal, 0 <= n <= 10^4"],
        "Every rotation of a appears as a substring of a+a — so the check is one "
        "includes() call. It is the classic 'reduce a hard problem to a known "
        "operation' trick.",
        ["return (a + a).includes(b);  // after length check",
         "Different lengths can never be rotations — reject first."],
        {"javascript": "function isRotation(a, b) {\n  // return true/false\n}"},
    ),
    _p(
        "js-l10", "Group By First Letter", "logic", "medium",
        "Given an array of words, return an object mapping each first letter "
        "(lowercased) to the array of words starting with it.",
        [
            _ex('["apple","avocado","banana"]', '{a: ["apple","avocado"], b: ["banana"]}',
                "Grouped by initial."),
        ],
        ["0 <= arr.length <= 10^4"],
        "reduce into an object, creating each key's array on first sight "
        "((obj[k] ||= [])). Grouping is everywhere — SQL GROUP BY, analytics "
        "buckets — and this is its in-memory form.",
        ["Key = word[0].toLowerCase(); push word into obj[key].",
         "Guard empty words before reading word[0]."],
        {"javascript": "function groupByFirst(words) {\n  // return grouping object\n}"},
    ),
    # ================= ADVANCED (10) =================
    _p(
        "js-a01", "Counter With Closure", "advanced", "medium",
        "Write makeCounter(start) returning an object { inc(), dec(), value() } "
        "where the count is private (not accessible from outside).",
        [
            _ex("c = makeCounter(5); c.inc(); c.value()", "6",
                "Private state incremented."),
            _ex("c.dec(); c.dec(); c.value()", "4", "Decrement works too."),
        ],
        [],
        "The inner functions close over `count` — it survives after makeCounter "
        "returns because the closures reference it. Privacy via closure (not "
        "classes) is the original JavaScript encapsulation pattern.",
        ["let count = start; return { inc: () => ++count, ... };",
         "Nothing named count should be reachable on the returned object."],
        {"javascript": "function makeCounter(start) {\n  // return { inc, dec, value }\n}"},
    ),
    _p(
        "js-a02", "Debounce", "advanced", "hard",
        "Write debounce(fn, ms) returning a wrapper that only calls fn after ms "
        "have passed without another call. The wrapper must forward the latest "
        "arguments and `this`.",
        [
            _ex("rapid 3 calls, then quiet", "fn runs once, with last args",
                "Earlier calls are cancelled."),
        ],
        ["ms >= 0"],
        "clearTimeout on every call plus setTimeout captures the pattern: each new "
        "call resets the timer. It is how search-as-you-type avoids firing a "
        "request per keystroke.",
        ["Keep timerId in the closure; on call: clearTimeout(timerId).",
         "timerId = setTimeout(() => fn.apply(this, args), ms);"],
        {"javascript": "function debounce(fn, ms) {\n  // return debounced wrapper\n}"},
    ),
    _p(
        "js-a03", "Once Function", "advanced", "medium",
        "Write once(fn) returning a wrapper that calls fn only on its first "
        "invocation and returns the cached result afterwards.",
        [
            _ex("w = once(() => 42); w(); w()", "42, then 42 again (cached)",
                "fn ran a single time."),
        ],
        [],
        "A `called` flag plus a cached result in the closure. This is memoization "
        "for zero-arg functions and the pattern behind one-time initializers.",
        ["let called = false, result; return (...a) => { if (!called) {...} return result; };",
         "Cache even falsy results — check the flag, not the result."],
        {"javascript": "function once(fn) {\n  // return once-wrapper\n}"},
    ),
    _p(
        "js-a04", "Promise Delay", "advanced", "easy",
        "Write delay(ms) returning a Promise that resolves after ms milliseconds "
        "with the value ms.",
        [
            _ex("await delay(100)", "100 (after ~100ms)", "Resolves with ms."),
        ],
        ["ms >= 0"],
        "new Promise(resolve => setTimeout(() => resolve(ms), ms)) — the executor "
        "runs immediately, resolve settles it later. This tiny function is the "
        "building block for all promise timing tests.",
        ["The executor takes (resolve, reject); call resolve(ms) in the timeout.",
         "No async keyword needed — you are CREATING the promise."],
        {"javascript": "function delay(ms) {\n  // return Promise resolving with ms\n}"},
    ),
    _p(
        "js-a05", "Sequential Promise Chain", "advanced", "medium",
        "Given an array of functions [f1, f2, f3] each returning a Promise, run "
        "them IN SEQUENCE and return a Promise resolving to the array of results.",
        [
            _ex("[() => delay(30).then(()=>'a'), () => delay(10).then(()=>'b')]",
                "['a','b'] in order", "Sequence preserved despite timing."),
        ],
        ["0 <= fns.length <= 100"],
        "reduce chaining (p.then(f).then(collect)) serializes async work; "
        "Promise.all would run them concurrently instead. Sequential-vs-parallel "
        "is a core async design decision.",
        ["fns.reduce((p, f) => p.then(results => f().then(r => [...results, r])), Promise.resolve([]))",
         "Or a simple for...of loop with await."],
        {"javascript": "async function runSequential(fns) {\n  // return Promise of results array\n}"},
    ),
    _p(
        "js-a06", "Async Retry", "advanced", "hard",
        "Write retry(fn, n) that calls async fn up to n times, returning its first "
        "success; if all n fail, throw the last error.",
        [
            _ex("fn fails twice then succeeds, n=3", "success", "Third try wins."),
            _ex("fn always fails, n=2", "throws last error", "Exhausted retries."),
        ],
        ["n >= 1"],
        "A for loop with try/catch around await fn(): return on success, stash the "
        "error and continue on failure, throw after the loop. Retry-with-backoff "
        "builds on this by adding delay between attempts.",
        ["for (let i = 0; i < n; i++) { try { return await fn(); } catch (e) { last = e; } } throw last;",
         "Don't forget: the throw AFTER the loop is what surfaces total failure."],
        {"javascript": "async function retry(fn, n) {\n  // return fn's result or throw last error\n}"},
    ),
    _p(
        "js-a07", "Pipeline With Map/Filter/Reduce", "advanced", "medium",
        "Given users [{name, age}], return the names of users aged >= 18, "
        "uppercased, joined with '; '.",
        [
            _ex("[{name:'a',age:20},{name:'b',age:15}]", '"A"', "Only adults, uppercased."),
        ],
        [],
        "filter -> map -> join is a declarative pipeline: each step does one thing "
        "and the data flows through. Compare with the nested-loop version to feel "
        "why functional style dominates data transformation.",
        ["users.filter(u => u.age >= 18).map(u => u.name.toUpperCase()).join('; ')",
         "Empty result joins to '' — no special-casing needed."],
        {"javascript": "function adultNames(users) {\n  // return joined string\n}"},
    ),
    _p(
        "js-a08", "Memoize", "advanced", "hard",
        "Write memoize(fn) returning a wrapper that caches results by JSON-"
        "stringified arguments and returns cached values on repeats.",
        [
            _ex("m = memoize(add); m(1,2); m(1,2)", "3, then cached 3 (fn ran once)",
                "Second call hits the cache."),
        ],
        ["fn is pure (same args -> same result)"],
        "A Map keyed by JSON.stringify(args) in the closure. The limitation worth "
        "knowing: key order and non-serializable args (functions, circular refs) "
        "break the keying — fine for this exercise, noted for production.",
        ["const cache = new Map(); key = JSON.stringify(args);",
         "if (cache.has(key)) return cache.get(key); compute, set, return."],
        {"javascript": "function memoize(fn) {\n  // return memoized wrapper\n}"},
    ),
    _p(
        "js-a09", "Deep Clone (Plain Objects)", "advanced", "hard",
        "Write deepClone(obj) that recursively copies plain objects and arrays "
        "(no functions, Dates, or cycles in input).",
        [
            _ex("{a: 1, b: {c: [2, 3]}}", "equal but not === nested",
                "Nested structures are fresh copies."),
        ],
        ["input is plain objects/arrays/primitives only"],
        "Recurse: arrays map to deepClone of each item, objects rebuild key by "
        "key, primitives return as-is. structuredClone does this natively now — "
        "but writing it teaches the recursive shape shared by all tree walks.",
        ["if (obj === null || typeof obj !== 'object') return obj;",
         "Array.isArray check first, then rebuild."],
        {"javascript": "function deepClone(obj) {\n  // return deep copy\n}"},
    ),
    _p(
        "js-a10", "Tiny Event Emitter", "advanced", "hard",
        "Write makeEmitter() returning { on(event, fn), emit(event, ...args), "
        "off(event, fn) }. Multiple listeners per event run in registration order.",
        [
            _ex("e.on('x', a); e.on('x', b); e.emit('x')", "a then b run",
                "Registration order preserved."),
            _ex("e.off('x', a); e.emit('x')", "only b runs", "Removed listener skipped."),
        ],
        [],
        "A Map of event -> listener array in the closure; emit spreads args to each. "
        "This is the observer pattern and the core of Node's EventEmitter — "
        "understanding it demystifies half of Node's API surface.",
        ["Store: const map = new Map(); on pushes, off splices, emit loops a copy.",
         "Iterate a copy ([...list]) so listeners can safely off() mid-emit."],
        {"javascript": "function makeEmitter() {\n  // return { on, emit, off }\n}"},
    ),
    # ================= PRACTICE (10) =================
    _p(
        "js-p01", "Longest Word", "practice", "easy",
        "Given a sentence, return the longest word (letters only — strip "
        "punctuation). First longest wins ties.",
        [
            _ex('"The quick brown fox"', '"quick"', "First 5-letter word."),
            _ex('"a bb ccc"', '"ccc"', "ccc is longest."),
        ],
        [],
        "Split on whitespace, strip non-letters with replace(/[^a-z]/gi, ''), track "
        "the max with strict > so ties keep the first. Regex cleanup is the "
        "practical half of the problem.",
        ["words = s.split(/\\s+/); clean each before comparing lengths.",
         "Use > not >= to keep the FIRST longest on ties."],
        {"javascript": "function longestWord(s) {\n  // return longest word\n}"},
    ),
    _p(
        "js-p02", "Missing Number", "practice", "medium",
        "Given an array of n distinct numbers from 0..n with one missing, return "
        "the missing one.",
        [
            _ex("[3, 0, 1]", "2", "2 is absent."),
            _ex("[0]", "1", "Only 1 missing."),
        ],
        ["1 <= n <= 10^4"],
        "Sum 0..n is n*(n+1)/2; subtract the actual sum and the difference is the "
        "missing number — O(n) time, O(1) space. (XOR of all indices+values is the "
        "overflow-proof twin.)",
        ["expected = (n * (n + 1)) / 2; return expected - actualSum;",
         "n = arr.length (the full range size)."],
        {"javascript": "function missingNumber(arr) {\n  // return missing number\n}"},
    ),
    _p(
        "js-p03", "Move Zeros to End", "practice", "medium",
        "Given an array, move all zeros to the end in place, preserving the order "
        "of non-zero elements.",
        [
            _ex("[0, 1, 0, 3, 12]", "[1, 3, 12, 0, 0]", "Order of nonzeros kept."),
        ],
        ["0 <= arr.length <= 10^4"],
        "Two pointers: a write pointer collects non-zeros at the front, then fill "
        "the tail with zeros. In-place and stable — the same partition idea as "
        "quicksort's first step.",
        ["let w = 0; for (x of arr) if (x !== 0) arr[w++] = x;",
         "Then fill arr[w..] with 0."],
        {"javascript": "function moveZeros(arr) {\n  // modify in place, return arr\n}"},
    ),
    _p(
        "js-p04", "First Non-Repeating Char", "practice", "medium",
        "Given a string s, return the first character that appears exactly once, "
        "or null if none.",
        [
            _ex('"leetcode"', '"l"', "l is the first unique."),
            _ex('"aabb"', "null", "No unique char."),
        ],
        ["0 <= s.length <= 10^5"],
        "Two passes: count frequencies, then scan s in order returning the first "
        "with count 1. Scanning s (not the Map) preserves first-appearance order — "
        "the same tie-break trick as most-frequent-char.",
        ["Count with a Map, then for (const ch of s) if (map.get(ch) === 1) return ch;",
         "Return null after the loop if nothing found."],
        {"javascript": "function firstUnique(s) {\n  // return char or null\n}"},
    ),
    _p(
        "js-p05", "Binary Search", "practice", "medium",
        "Given a sorted array and target, return the target's index or -1.",
        [
            _ex("[1,3,5,7,9], 7", "3", "Found at index 3."),
            _ex("[1,3,5], 4", "-1", "Absent."),
        ],
        ["0 <= arr.length <= 10^5"],
        "Halve the search space each step: compare mid, discard the wrong half. "
        "O(log n) — but ONLY valid on sorted input, and mid = lo + (hi-lo)/2 "
        "avoids the (lo+hi) overflow of the naive formula.",
        ["while (lo <= hi): mid = lo + ((hi - lo) >> 1); compare and shrink.",
         "<= keeps the last single element in play."],
        {"javascript": "function binarySearch(arr, target) {\n  // return index or -1\n}"},
    ),
    _p(
        "js-p06", "Fibonacci With Memoization", "practice", "medium",
        "Return the nth Fibonacci number using recursion + memoization "
        "(fib(0)=0, fib(1)=1).",
        [
            _ex("n = 10", "55", "0,1,1,2,3,5,8,13,21,34,55."),
            _ex("n = 50", "12586269025", "Fast only with memoization."),
        ],
        ["0 <= n <= 70"],
        "Plain recursion is O(2^n); caching each computed fib(k) in a Map makes "
        "each value computed once — O(n). It is THE canonical memoization demo "
        "and the gateway to dynamic programming.",
        ["const memo = new Map([[0,0],[1,1]]); recurse with memo lookup first.",
         "n=70 exceeds safe integer? 190392490709135 fits in 2^53 — fine."],
        {"javascript": "function fibMemo(n) {\n  // return nth Fibonacci\n}"},
    ),
    _p(
        "js-p07", "Simple Email Check", "practice", "medium",
        "Without regex, return true if s looks like an email: exactly one '@', "
        "non-empty local part, and a domain containing a '.' not at the start/end.",
        [
            _ex('"a@b.com"', "true", "Valid shape."),
            _ex('"a@@b.com"', "false", "Two @ signs."),
            _ex('"@b.com"', "false", "Empty local part."),
        ],
        [],
        "Split on '@' and require exactly 2 parts; check the domain has a dot with "
        "chars on both sides. Real email validation needs regex/RFC — this teaches "
        "string splitting and layered validation instead.",
        ["const parts = s.split('@'); if (parts.length !== 2) return false;",
         "Check local non-empty; domain: dot index > 0 and < len-1."],
        {"javascript": "function isEmail(s) {\n  // return true/false\n}"},
    ),
    _p(
        "js-p08", "Array Intersection", "practice", "easy",
        "Given two arrays, return the unique values present in both (order of "
        "first array).",
        [
            _ex("[1,2,3], [2,3,4]", "[2, 3]", "Common values."),
            _ex("[1,1,2], [2,2,3]", "[2]", "Deduped."),
        ],
        [],
        "Put the second array in a Set, filter the first by membership, dedupe the "
        "result. Set lookups are O(1), so the whole thing is O(n+m) — the reason "
        "Sets exist for membership problems.",
        ["const b = new Set(arrB); return [...new Set(arrA.filter(x => b.has(x)))];",
         "The outer Set dedupes; filter preserves arrA's order."],
        {"javascript": "function intersect(a, b) {\n  // return common unique values\n}"},
    ),
    _p(
        "js-p09", "Palindrome Number", "practice", "easy",
        "Given a non-negative integer n, return true if its decimal form is a "
        "palindrome.",
        [
            _ex("121", "true", "Mirrors."),
            _ex("10", "false", "'01' != '10'."),
        ],
        ["0 <= n <= 10^9"],
        "String(n) compared to its reverse is the pragmatic JS answer (numbers "
        "convert cheaply). The arithmetic reverse (no strings) is the follow-up "
        "that shows the same digit-peeling from the C bank.",
        ["const s = String(n); return s === [...s].reverse().join('');",
         "Negative inputs: not in constraints, but '-' would break symmetry."],
        {"javascript": "function isPalindromeNum(n) {\n  // return true/false\n}"},
    ),
    _p(
        "js-p10", "Simple LRU Cache", "practice", "hard",
        "Implement LRUCache(capacity) with get(key) and put(key, value). get "
        "returns -1 if missing. put evicts the least-recently-used key when full. "
        "Access (get or put) marks a key most-recent.",
        [
            _ex("c=new LRU(2); put(1,1); put(2,2); get(1); put(3,3); get(2)",
                "1, then -1 (evicted)", "Key 2 was least recently used."),
        ],
        ["1 <= capacity <= 100"],
        "JS Map preserves insertion order — delete + re-set moves a key to "
        "'most recent', and map.keys().next().value is the LRU victim. It is a "
        "one-data-structure LRU; the O(1) production version pairs a hash map "
        "with a doubly linked list.",
        ["get: if missing return -1; else delete+set to refresh, return value.",
         "put: delete existing key first; if size == capacity evict LRU key."],
        {"javascript": "class LRUCache {\n  constructor(capacity) {}\n  get(key) {}\n  put(key, value) {}\n}"},
    ),
]




_COMPANIES: dict[str, list[str]] = {
    "js-a01": ['amazon', 'google', 'flipkart'],
    "js-a02": ['google', 'amazon', 'flipkart'],
    "js-a03": ['amazon', 'google', 'microsoft'],
    "js-a04": ['tcs', 'infosys', 'accenture'],
    "js-a05": ['amazon', 'flipkart', 'google'],
    "js-a06": ['google', 'amazon', 'uber'],
    "js-a07": ['tcs', 'infosys', 'flipkart'],
    "js-a08": ['google', 'amazon', 'flipkart'],
    "js-a09": ['amazon', 'google', 'microsoft'],
    "js-a10": ['google', 'amazon', 'uber'],
    "js-b01": ['tcs', 'infosys', 'wipro'],
    "js-b02": ['tcs', 'infosys', 'accenture'],
    "js-b03": ['tcs', 'wipro', 'infosys'],
    "js-b04": ['infosys', 'tcs'],
    "js-b05": ['tcs', 'accenture', 'wipro'],
    "js-b06": ['tcs', 'infosys', 'amazon'],
    "js-b07": ['tcs', 'wipro'],
    "js-b08": ['tcs', 'infosys', 'accenture'],
    "js-b09": ['tcs', 'tech-mahindra'],
    "js-b10": ['infosys', 'tcs'],
    "js-l01": ['tcs', 'infosys', 'accenture'],
    "js-l02": ['amazon', 'tcs', 'flipkart'],
    "js-l03": ['amazon', 'flipkart', 'tcs'],
    "js-l04": ['amazon', 'tcs', 'infosys'],
    "js-l05": ['amazon', 'google', 'flipkart'],
    "js-l06": ['amazon', 'google', 'microsoft'],
    "js-l07": ['amazon', 'google', 'flipkart'],
    "js-l08": ['amazon', 'tcs', 'infosys'],
    "js-l09": ['tcs', 'infosys', 'accenture'],
    "js-l10": ['flipkart', 'amazon', 'tcs'],
    "js-p01": ['tcs', 'infosys', 'accenture'],
    "js-p02": ['amazon', 'google', 'flipkart'],
    "js-p03": ['amazon', 'flipkart', 'google'],
    "js-p04": ['amazon', 'google', 'microsoft'],
    "js-p05": ['tcs', 'infosys', 'amazon'],
    "js-p06": ['amazon', 'google', 'tcs'],
    "js-p07": ['tcs', 'accenture', 'infosys'],
    "js-p08": ['tcs', 'infosys', 'accenture'],
    "js-p09": ['tcs', 'infosys'],
    "js-p10": ['amazon', 'google', 'flipkart'],
}

for _prob in _JS_BANK:
    _prob.companies = _COMPANIES.get(_prob.id, [])

def get_problems(topic: str | None = None, difficulty: str | None = None) -> list[JSProblem]:
    """Return problems, optionally filtered by topic and/or difficulty.

    Preserves bank order (basics -> practice progression).
    """
    out = _JS_BANK
    if topic is not None:
        out = [p for p in out if p.topic == topic]
    if difficulty is not None:
        out = [p for p in out if p.difficulty == difficulty]
    return list(out)


def get_problem(pid: str) -> JSProblem | None:
    """Return the problem with the given id, or None if unknown."""
    for p in _JS_BANK:
        if p.id == pid:
            return p
    return None


def list_topics() -> list[str]:
    """Return topic slugs in bank (progression) order."""
    seen: list[str] = []
    for p in _JS_BANK:
        if p.topic not in seen:
            seen.append(p.topic)
    return seen
