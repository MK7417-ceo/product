"""Outbound adapter: curated Go coding problem bank.

30 ORIGINAL problems across 3 topics, ordered basics -> functions -> the
concurrency that makes Go special (goroutines and channels).

Every problem carries a short theory primer, hand-verified examples,
realistic constraints, hints, and Go starter code.

Content is written originally for SkillForge — not copied from any site.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GoProblem:
    id: str
    title: str
    topic: str  # basics | functions | concurrency
    difficulty: str  # basic | easy | medium | hard
    description: str
    examples: list  # [{"input": str, "output": str, "explanation": str}]
    constraints: list
    theory: str  # 2-3 sentence concept explanation
    hints: list
    starter_code: dict  # {"go": ...}
    companies: list = field(default_factory=list)  # companies known to ask this pattern


def _p(pid: str, title: str, topic: str, difficulty: str, description: str,
       examples: list, constraints: list, theory: str, hints: list,
       starter_code: dict) -> GoProblem:
    return GoProblem(
        id=pid, title=title, topic=topic, difficulty=difficulty,
        description=description, examples=examples, constraints=constraints,
        theory=theory, hints=hints, starter_code=starter_code,
    )


def _ex(inp: str, out: str, why: str) -> dict:
    return {"input": inp, "output": out, "explanation": why}


_GO_BANK: list[GoProblem] = [
    # ================= BASICS (10) =================
    _p(
        "go-b01", "Variables and Sum", "basics", "basic",
        "Declare two integers a and b using short variable declaration (:=), "
        "then return their sum.",
        [
            _ex("a = 3, b = 4", "7", "3 + 4."),
        ],
        [],
        ":= declares AND initializes with type inference — the idiomatic Go way "
        "inside functions. Unused variables are a compile ERROR in Go, so every "
        "declared name must be used.",
        ["a := 3; b := 4; return a + b",
         ":= only works inside functions; package level needs var."],
        {"go": "func add(a, b int) int {\n\t// return a + b\n}"},
    ),
    _p(
        "go-b02", "Sum 1 to N", "basics", "basic",
        "Given n, return the sum 1 + 2 + ... + n.",
        [
            _ex("n = 5", "15", "1+2+3+4+5."),
            _ex("n = 1", "1", "Single term."),
        ],
        ["1 <= n <= 10^6"],
        "Go has only ONE loop keyword: for. It covers while-style (for cond), "
        "infinite (for {}), and classic three-part loops — learning the three "
        "forms is learning Go iteration completely.",
        ["sum := 0; for i := 1; i <= n; i++ { sum += i }",
         "Or the formula n*(n+1)/2."],
        {"go": "func sumN(n int) int {\n\t// return 1+2+...+n\n}"},
    ),
    _p(
        "go-b03", "Even or Odd", "basics", "basic",
        "Given n, return \"even\" if n is even, else \"odd\".",
        [
            _ex("n = 4", '"even"', "4 is even."),
            _ex("n = -3", '"odd"', "Sign irrelevant."),
        ],
        [],
        "Go's if can include a short statement: if r := n % 2; r == 0. Modulo "
        "on negatives follows the dividend's sign in Go, but == 0 is still the "
        "correct even test.",
        ['if n%2 == 0 { return "even" }; return "odd"',
         "Go strings use double quotes; single quotes are runes."],
        {"go": "func evenOrOdd(n int) string {\n\t// return \"even\" or \"odd\"\n}"},
    ),
    _p(
        "go-b04", "Factorial", "basics", "basic",
        "Given non-negative n, return n!. 0! = 1.",
        [
            _ex("n = 5", "120", "5*4*3*2*1."),
            _ex("n = 0", "1", "Definition."),
        ],
        ["0 <= n <= 20"],
        "Use int64 for the result (20! overflows int32). Go has no ternary "
        "operator and no while keyword — the for loop and if/else cover it, "
        "which keeps the language small by design.",
        ["result := int64(1); for i := int64(2); i <= int64(n); i++ { result *= i }",
         "Convert n once to int64 to keep types clean."],
        {"go": "func factorial(n int) int64 {\n\t// return n!\n}"},
    ),
    _p(
        "go-b05", "Slice Sum", "basics", "easy",
        "Given a slice of ints, return their sum. A nil/empty slice sums to 0.",
        [
            _ex("[]int{1, 2, 3}", "6", "Straight sum."),
            _ex("[]int{}", "0", "Empty slice."),
        ],
        [],
        "Slices are Go's dynamic arrays: a header (pointer, length, capacity) over "
        "a backing array. range gives index AND value — use _ to ignore the index "
        "or the compiler complains about the unused variable.",
        ["sum := 0; for _, v := range nums { sum += v }",
         "_ discards the index you don't need."],
        {"go": "func sliceSum(nums []int) int {\n\t// return sum\n}"},
    ),
    _p(
        "go-b06", "Word Count Map", "basics", "easy",
        "Given a slice of words, return a map from each word to its count.",
        [
            _ex('["a","b","a"]', '{"a": 2, "b": 1}', "a appears twice."),
            _ex("[]", "{}", "Empty map."),
        ],
        [],
        "Maps must be initialized with make before writing — assigning to a nil "
        "map panics. Reading a missing key returns the zero value, so "
        "counts[w]++ works even on first sight.",
        ["counts := make(map[string]int); for _, w := range words { counts[w]++ }",
         "Return the map itself (maps are reference types)."],
        {"go": "func wordCount(words []string) map[string]int {\n\t// return word -> count map\n}"},
    ),
    _p(
        "go-b07", "Reverse String (Runes)", "basics", "medium",
        "Given a string s (may contain unicode), return it reversed.",
        [
            _ex('"hello"', '"olleh"', "ASCII reversal."),
            _ex('"héllo"', '"olléh"', "é survives as one rune."),
        ],
        [],
        "Go strings are byte sequences; ranging over a string yields RUNES "
        "(unicode code points), not bytes. Converting to []rune first makes "
        "reversal unicode-correct — reversing bytes would corrupt multi-byte "
        "characters.",
        ["r := []rune(s); reverse the rune slice; return string(r)",
         "Two-pointer swap on the []rune."],
        {"go": "func reverseString(s string) string {\n\t// return reversed, unicode-safe\n}"},
    ),
    _p(
        "go-b08", "Max in Slice", "basics", "easy",
        "Given a non-empty slice of ints, return the largest.",
        [
            _ex("[]int{3, 1, 4}", "4", "4 wins."),
            _ex("[]int{-5, -2}", "-2", "Least negative."),
        ],
        [],
        "Seed max with nums[0] so all-negative slices work. Go has no built-in "
        "max for slices (there is builtin max for scalars since 1.21) — the loop "
        "is the standard approach.",
        ["m := nums[0]; for _, v := range nums[1:] { if v > m { m = v } }",
         "nums[1:] slices from index 1 — no copy, just a new header."],
        {"go": "func findMax(nums []int) int {\n\t// return largest (nums non-empty)\n}"},
    ),
    _p(
        "go-b09", "FizzBuzz Slice", "basics", "easy",
        "Given n, return a []string of 1..n with multiples of 3 as \"Fizz\", of 5 "
        "as \"Buzz\", of both as \"FizzBuzz\".",
        [
            _ex("n = 5", '["1","2","Fizz","4","Buzz"]', "Classic."),
        ],
        ["1 <= n <= 10^4"],
        "strconv.Itoa converts int to string (no implicit int->string conversion "
        "in Go — string(65) gives \"A\", the classic gotcha). make([]string, 0, n) "
        "pre-allocates capacity for efficiency.",
        ["Build with append; check i%15 first, then 3, then 5.",
         "strconv.Itoa(i) for the plain numbers."],
        {"go": "func fizzBuzz(n int) []string {\n\t// return fizzbuzz slice\n}"},
    ),
    _p(
        "go-b10", "Prime Check", "basics", "easy",
        "Given n, return true if n is prime, false otherwise (n < 2 is not prime).",
        [
            _ex("n = 13", "true", "Prime."),
            _ex("n = 15", "false", "3 * 5."),
        ],
        ["0 <= n <= 10^9"],
        "Trial division up to sqrt(n): for i := 2; i*i <= n; i++. Go's for with a "
        "condition is the while-loop replacement — the language deliberately has "
        "just the one loop construct.",
        ["if n < 2 { return false }; loop i while i*i <= n.",
         "i*i <= n avoids floating-point sqrt entirely."],
        {"go": "func isPrime(n int) bool {\n\t// return true if prime\n}"},
    ),
    # ================= FUNCTIONS (10) =================
    _p(
        "go-f01", "Divide With Remainder", "functions", "easy",
        "Write divmod(a, b int) returning (quotient, remainder) as MULTIPLE "
        "return values. Assume b != 0.",
        [
            _ex("a = 7, b = 3", "(2, 1)", "7 = 2*3 + 1."),
        ],
        [],
        "Go functions can return several values — the idiomatic way to return a "
        "result plus metadata (or an error). Callers receive them as a tuple: "
        "q, r := divmod(7, 3).",
        ["func divmod(a, b int) (int, int) { return a / b, a % b }",
         "Integer division truncates toward zero in Go."],
        {"go": "func divmod(a, b int) (int, int) {\n\t// return quotient, remainder\n}"},
    ),
    _p(
        "go-f02", "Named Returns", "functions", "easy",
        "Write split(sum int) using NAMED return values (x, y int) that split sum "
        "into x = sum*4/9 and y = sum - x. Use a bare return.",
        [
            _ex("sum = 18", "(8, 10)", "x=8, y=10."),
        ],
        [],
        "Named results (x, y int) are pre-declared variables; bare `return` "
        "returns their current values. It documents the outputs in the signature "
        "— beloved for short functions, frowned upon in long ones.",
        ["func split(sum int) (x, y int) { x = sum * 4 / 9; y = sum - x; return }",
         "The bare return hands back x and y as they stand."],
        {"go": "func split(sum int) (x, y int) {\n\t// use bare return\n}"},
    ),
    _p(
        "go-f03", "Variadic Sum", "functions", "easy",
        "Write sumAll(nums ...int) int summing any number of arguments.",
        [
            _ex("sumAll(1, 2, 3)", "6", "Three args."),
            _ex("sumAll()", "0", "Zero args."),
            _ex('sumAll(s...) where s=[]int{1,2}', "3", "Slice spread with ...."),
        ],
        [],
        "...int collects trailing args into a []int inside the function. Callers "
        "can spread a slice with s... — the symmetry makes variadic functions "
        "compose naturally.",
        ["func sumAll(nums ...int) int { total := 0; for _, n := range nums { total += n }; return total }",
         "nums is a real []int inside — range over it normally."],
        {"go": "func sumAll(nums ...int) int {\n\t// return sum of all args\n}"},
    ),
    _p(
        "go-f04", "Defer Order", "functions", "medium",
        "Write deferredOrder() that defers three fmt-free appends of 1, 2, 3 to a "
        "slice and returns the final slice. Predict: what order do deferred calls run?",
        [
            _ex("deferredOrder()", "[3, 2, 1]", "Defers run LIFO."),
        ],
        [],
        "Deferred calls run LAST-IN-FIRST-OUT when the function returns — like a "
        "stack. This makes defer perfect for cleanup (close, unlock) because the "
        "most recently acquired resource releases first.",
        ["var out []int; defer func() { out = append(out, 1) }(); ... then return out",
         "Careful: named return or closure capture needed since defers run at return."],
        {"go": "func deferredOrder() (out []int) {\n\t// defer appends of 1, 2, 3; return out\n}"},
    ),
    _p(
        "go-f05", "Rectangle Method", "functions", "easy",
        "Define type Rect struct{ W, H float64 } with a VALUE-receiver method "
        "Area() float64 returning W*H.",
        [
            _ex("Rect{3, 4}.Area()", "12", "3 * 4."),
        ],
        [],
        "Methods attach to types: func (r Rect) Area() float64. A value receiver "
        "gets a COPY — fine for read-only methods like Area. (Pointer receivers "
        "are for mutation.)",
        ["type Rect struct { W, H float64 }",
         "func (r Rect) Area() float64 { return r.W * r.H }"],
        {"go": "type Rect struct {\n\tW, H float64\n}\n\nfunc (r Rect) Area() float64 {\n\t// return W*H\n}"},
    ),
    _p(
        "go-f06", "Counter With Pointer Receiver", "functions", "medium",
        "Define type Counter struct{ n int } with pointer-receiver methods Inc() "
        "(n++) and Value() int. Demonstrate that Inc mutates the original.",
        [
            _ex("c := Counter{}; c.Inc(); c.Inc(); c.Value()", "2", "Mutations stick."),
        ],
        [],
        "Pointer receivers (func (c *Counter)) operate on the ORIGINAL struct; "
        "value receivers get a copy and mutations vanish. Rule of thumb: if ANY "
        "method needs a pointer receiver, use it for all methods of the type.",
        ["func (c *Counter) Inc() { c.n++ }",
         "func (c *Counter) Value() int { return c.n }"],
        {"go": "type Counter struct {\n\tn int\n}\n\nfunc (c *Counter) Inc() {\n\t// increment n\n}\n\nfunc (c *Counter) Value() int {\n\t// return n\n\treturn 0\n}"},
    ),
    _p(
        "go-f07", "Shape Interface", "functions", "medium",
        "Define interface Shape with Area() float64. Implement it for Rect{W,H} "
        "and Circle{R}. Write totalArea(shapes []Shape) float64 summing areas.",
        [
            _ex("[Rect{2,3}, Circle{1}]", "≈ 9.14", "6 + π."),
        ],
        [],
        "Interfaces are satisfied IMPLICITLY — no 'implements' keyword. Any type "
        "with Area() float64 IS a Shape. This duck-typing keeps dependencies "
        "loose and is the heart of Go's composition style.",
        ["type Shape interface { Area() float64 }",
         "Circle Area: math.Pi * c.R * c.R. totalArea ranges and sums s.Area()."],
        {"go": "type Shape interface {\n\tArea() float64\n}\n\n// implement Rect and Circle, then:\nfunc totalArea(shapes []Shape) float64 {\n\t// return sum of areas\n\treturn 0\n}"},
    ),
    _p(
        "go-f08", "Error Return Pattern", "functions", "easy",
        "Write safeDiv(a, b float64) (float64, error) returning an error "
        "\"division by zero\" when b == 0, else the quotient and nil.",
        [
            _ex("safeDiv(6, 3)", "(2, nil)", "Normal division."),
            _ex("safeDiv(1, 0)", "(0, err)", "Error, not a panic."),
        ],
        [],
        "Go has no exceptions: errors are VALUES returned alongside results, "
        "conventionally as the last return. errors.New creates one; callers "
        "check err != nil. Explicit error paths are a Go cultural cornerstone.",
        ['if b == 0 { return 0, errors.New("division by zero") }',
         "Import \"errors\". Return (a/b, nil) otherwise."],
        {"go": "func safeDiv(a, b float64) (float64, error) {\n\t// return quotient or error\n}"},
    ),
    _p(
        "go-f09", "Append Gotcha", "functions", "medium",
        "Given s := []int{1,2,3}, write extendTwo(s []int) []int that appends 4 "
        "and 5 and RETURNS the new slice. Explain in a comment when the caller's "
        "slice would/wouldn't see the change.",
        [
            _ex("extendTwo([]int{1,2,3})", "[1,2,3,4,5]", "Returned slice has 5."),
        ],
        [],
        "append may REALLOCATE: the returned slice header is the truth, the "
        "caller's old header may point at the old array. Always use the return "
        "value (s = append(s, x)) — ignoring it is the #1 slice bug.",
        ["return append(s, 4, 5)",
         "Comment: caller must use the return value; append can move the array."],
        {"go": "func extendTwo(s []int) []int {\n\t// append 4, 5 and return; note the gotcha in a comment\n}"},
    ),
    _p(
        "go-f10", "Merge Maps", "functions", "easy",
        "Write mergeMaps(a, b map[string]int) map[string]int returning a NEW map "
        "with all entries; b's values win on key conflicts. Do not mutate inputs.",
        [
            _ex('{"x":1}, {"x":2,"y":3}', '{"x":2,"y":3}', "b wins x."),
        ],
        [],
        "Allocate the result with make, copy a's entries, then b's. Mutating an "
        "input map would surprise the caller (maps are reference types) — "
        "returning a fresh map is the polite, predictable API.",
        ["out := make(map[string]int); copy a, then b.",
         "len(a)+len(b) as size hint is a nice touch."],
        {"go": "func mergeMaps(a, b map[string]int) map[string]int {\n\t// return new merged map\n}"},
    ),
    # ================= CONCURRENCY (10) =================
    _p(
        "go-c01", "First Goroutine", "concurrency", "easy",
        "Write runAsync(done chan bool) that launches a goroutine sending true "
        "on done, then the CALLER waits on <-done before returning.",
        [
            _ex("runAsync(ch)", "returns after goroutine signals", "Synchronized."),
        ],
        [],
        "go f() launches f concurrently; channels coordinate. Receiving (<-done) "
        "blocks until the send happens — the simplest possible goroutine "
        "rendezvous, and the pattern every concurrent Go program builds on.",
        ["go func() { done <- true }(); then <-done in the caller.",
         "Unbuffered chan bool: send blocks until someone receives."],
        {"go": "func runAsync(done chan bool) {\n\t// launch goroutine that sends true; wait for it\n}"},
    ),
    _p(
        "go-c02", "Channel Ping-Pong", "concurrency", "easy",
        "Write pingPong() string: create a channel, send \"ping\" from a goroutine, "
        "receive it in main flow, reply \"pong\" back through the same channel "
        "from main flow, and have the goroutine return the reply. Return \"pong\".",
        [
            _ex("pingPong()", '"pong"', "Round trip complete."),
        ],
        [],
        "Channels are bidirectional by default: the same channel carries ping one "
        "way and pong back. Each send pairs with a receive — thinking in these "
        "'handoff pairs' prevents deadlocks.",
        ["ch := make(chan string); go func() { msg := <-ch; ch <- msg + \"ong\" }()",
         "Main: ch <- \"ping\"; return <-ch  (== \"pong\")."],
        {"go": "func pingPong() string {\n\t// round-trip ping/pong over one channel\n\treturn \"\"\n}"},
    ),
    _p(
        "go-c03", "Buffered Channel", "concurrency", "medium",
        "Write bufferedSend() int: make a channel with buffer 2, send 1 and 2 "
        "WITHOUT a goroutine (no blocking), then receive and return their sum.",
        [
            _ex("bufferedSend()", "3", "1 + 2."),
        ],
        [],
        "make(chan int, 2) buffers 2 sends — they complete without a receiver "
        "waiting. Buffering decouples producers from consumers; unbuffered "
        "channels are pure synchronization (rendezvous).",
        ["ch := make(chan int, 2); ch <- 1; ch <- 2; return <-ch + <-ch",
         "A third send WOULD block — buffer size matters."],
        {"go": "func bufferedSend() int {\n\t// use buffer-2 channel, no goroutine\n\treturn 0\n}"},
    ),
    _p(
        "go-c04", "Parallel Sum", "concurrency", "medium",
        "Write parallelSum(nums []int) int: split nums in half, sum each half in "
        "its own goroutine sending to a channel, combine both results.",
        [
            _ex("[]int{1,2,3,4}", "10", "5 + 5 via two goroutines."),
            _ex("[]int{7}", "7", "Odd length: halves of 0 and 1."),
        ],
        [],
        "Fan-out/fan-in: launch workers, collect from channels. Splitting at "
        "len/2 handles odd lengths (one half may be empty — sum is 0). For big "
        "slices this is a real speedup; for tiny ones, goroutine overhead wins — "
        "know the tradeoff.",
        ["ch := make(chan int, 2); go sumHalf(...); go sumHalf(...); return <-ch + <-ch",
         "Buffered chan (2) so goroutines never block on send."],
        {"go": "func parallelSum(nums []int) int {\n\t// sum halves concurrently\n\treturn 0\n}"},
    ),
    _p(
        "go-c05", "Range Over Channel", "concurrency", "medium",
        "Write squares(n int) []int: a goroutine sends 1²..n² then CLOSES the "
        "channel; the caller ranges over it collecting results.",
        [
            _ex("squares(3)", "[1, 4, 9]", "Squares in order."),
            _ex("squares(0)", "[]", "No sends, immediate close."),
        ],
        ["n >= 0"],
        "Closing signals 'no more values' — range over a channel ends at close. "
        "Only the SENDER should close; closing twice or sending on closed panics. "
        "This is the canonical producer/consumer shape.",
        ["go func() { defer close(ch); for i := 1; i <= n; i++ { ch <- i*i } }()",
         "for v := range ch { out = append(out, v) }"],
        {"go": "func squares(n int) []int {\n\t// collect squares via ranged channel\n}"},
    ),
    _p(
        "go-c06", "Select Two Channels", "concurrency", "medium",
        "Write firstOf(a, b <-chan string) string: return whichever channel "
        "delivers first using select.",
        [
            _ex("a gets \"x\" first", '"x"', "Fastest wins."),
        ],
        [],
        "select waits on MULTIPLE channels and runs the first ready case — Go's "
        "answer to 'wait for any of these events'. If both are ready, it picks "
        "pseudorandomly (fairness by design).",
        ["select { case v := <-a: return v; case v := <-b: return v }",
         "No default: blocks until one is ready."],
        {"go": "func firstOf(a, b <-chan string) string {\n\t// return first available value\n\treturn \"\"\n}"},
    ),
    _p(
        "go-c07", "Worker Pool", "concurrency", "hard",
        "Write workerPool(jobs []int, workers int) []int: distribute jobs over "
        "'workers' goroutines; each worker doubles its job and sends results. "
        "Return all results (any order).",
        [
            _ex("jobs=[1,2,3,4], workers=2", "[2,4,6,8] any order", "All doubled."),
        ],
        ["workers >= 1"],
        "Jobs channel feeds workers; each worker ranges until jobs closes, "
        "sending to results. Close results after all workers finish (track with "
        "a WaitGroup or count). This pattern saturates CPU cores on real work.",
        ["Launch workers ranging over jobs; close(jobs) after sending all.",
         "Collect exactly len(jobs) results."],
        {"go": "func workerPool(jobs []int, workers int) []int {\n\t// fan-out workers, collect doubled results\n}"},
    ),
    _p(
        "go-c08", "WaitGroup Basics", "concurrency", "medium",
        "Write waitAll(n int) int: launch n goroutines each adding 1 to a shared "
        "counter protected by a mutex; wait with WaitGroup; return the counter.",
        [
            _ex("waitAll(100)", "100", "All goroutines accounted for."),
        ],
        ["n >= 0"],
        "sync.WaitGroup: Add(1) before each goroutine, Done() inside (defer it!), "
        "Wait() blocks until the counter hits zero. Forgetting Done deadlocks; "
        "the mutex protects the shared counter from data races.",
        ["var wg sync.WaitGroup; var mu sync.Mutex; count := 0",
         "wg.Add(1); go func() { defer wg.Done(); mu.Lock(); count++; mu.Unlock() }(); wg.Wait()"],
        {"go": "func waitAll(n int) int {\n\t// n goroutines each add 1; return total\n\treturn 0\n}"},
    ),
    _p(
        "go-c09", "Channel Direction", "concurrency", "medium",
        "Write produce(ch chan<- int, n int) sending 1..n then closing, and "
        "consume(ch <-chan int) int summing until close. Note the DIRECTIONAL "
        "types in the signatures.",
        [
            _ex("produce then consume, n=4", "10", "1+2+3+4."),
        ],
        ["n >= 0"],
        "chan<- int (send-only) and <-chan int (receive-only) in signatures "
        "document intent AND get compiler enforcement — passing the wrong "
        "direction is a compile error. Self-documenting concurrency contracts.",
        ["produce: for i:=1..n { ch <- i }; close(ch)",
         "consume: sum := 0; for v := range ch { sum += v }; return sum"],
        {"go": "func produce(ch chan<- int, n int) {\n\t// send 1..n, then close\n}\n\nfunc consume(ch <-chan int) int {\n\t// sum until channel closes\n\treturn 0\n}"},
    ),
    _p(
        "go-c10", "Timeout With Select", "concurrency", "hard",
        "Write withTimeout(ch <-chan string, ms int) (string, bool): return the "
        "channel's value (true) if it arrives within ms milliseconds, else "
        "(\"\", false).",
        [
            _ex("value arrives in time", '(v, true)', "Got it."),
            _ex("nothing arrives", '("", false)', "Timed out."),
        ],
        ["ms >= 0"],
        "select with time.After: case v := <-ch (success) vs case <-time.After(...) "
        "(timeout). Timeouts bound every network call in production Go — this "
        "exact shape appears in real services constantly.",
        ["select { case v := <-ch: return v, true; case <-time.After(time.Duration(ms) * time.Millisecond): return \"\", false }",
         "Import \"time\"."],
        {"go": "func withTimeout(ch <-chan string, ms int) (string, bool) {\n\t// value or timeout\n\treturn \"\", false\n}"},
    ),
]




_COMPANIES: dict[str, list[str]] = {
    "go-b01": ['tcs', 'infosys', 'google'],
    "go-b02": ['tcs', 'infosys'],
    "go-b03": ['tcs', 'wipro'],
    "go-b04": ['infosys', 'tcs'],
    "go-b05": ['google', 'tcs', 'uber'],
    "go-b06": ['google', 'uber', 'tcs'],
    "go-b07": ['google', 'uber', 'cloudflare'],
    "go-b08": ['tcs', 'infosys'],
    "go-b09": ['tcs', 'infosys', 'accenture'],
    "go-b10": ['tcs', 'google'],
    "go-c01": ['google', 'uber', 'cloudflare'],
    "go-c02": ['google', 'uber'],
    "go-c03": ['google', 'cloudflare', 'dropbox'],
    "go-c04": ['google', 'uber', 'cloudflare'],
    "go-c05": ['google', 'uber', 'dropbox'],
    "go-c06": ['google', 'cloudflare', 'uber'],
    "go-c07": ['google', 'uber', 'dropbox'],
    "go-c08": ['google', 'cloudflare', 'uber'],
    "go-c09": ['google', 'uber'],
    "go-c10": ['google', 'uber', 'cloudflare'],
    "go-f01": ['google', 'tcs', 'uber'],
    "go-f02": ['google', 'uber'],
    "go-f03": ['google', 'tcs'],
    "go-f04": ['google', 'uber', 'cloudflare'],
    "go-f05": ['google', 'tcs'],
    "go-f06": ['google', 'uber', 'dropbox'],
    "go-f07": ['google', 'uber', 'cloudflare'],
    "go-f08": ['google', 'uber', 'dropbox'],
    "go-f09": ['google', 'cloudflare', 'uber'],
    "go-f10": ['google', 'tcs', 'uber'],
}

for _prob in _GO_BANK:
    _prob.companies = _COMPANIES.get(_prob.id, [])

def get_problems(topic: str | None = None, difficulty: str | None = None) -> list[GoProblem]:
    """Return problems, optionally filtered by topic and/or difficulty.

    Preserves bank order (basics -> concurrency progression).
    """
    out = _GO_BANK
    if topic is not None:
        out = [p for p in out if p.topic == topic]
    if difficulty is not None:
        out = [p for p in out if p.difficulty == difficulty]
    return list(out)


def get_problem(pid: str) -> GoProblem | None:
    """Return the problem with the given id, or None if unknown."""
    for p in _GO_BANK:
        if p.id == pid:
            return p
    return None


def list_topics() -> list[str]:
    """Return topic slugs in bank (progression) order."""
    seen: list[str] = []
    for p in _GO_BANK:
        if p.topic not in seen:
            seen.append(p.topic)
    return seen
