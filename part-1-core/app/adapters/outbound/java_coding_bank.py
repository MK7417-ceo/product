"""Outbound adapter: Java coding problem bank.

50 ORIGINAL Java coding problems across 5 topics, ordered basics -> practice
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
    topic: str  # basics | oop | collections | advanced | practice
    difficulty: str  # basic | easy | medium | hard
    description: str
    examples: list  # [{"input": str, "output": str, "explanation": str}]
    constraints: list
    theory: str  # 2-3 sentence concept explanation
    hints: list
    starter_code: dict  # {"java": ...}
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
        theory=theory, hints=hints, starter_code={"java": starter_code},
        test_cases=test_cases, companies=companies or [],
    )


_JAVA_BANK: list[CodingProblem] = [
    # ================= BASICS (10) =================
    _p(
        "ja-b01", "Sum of First N Numbers", "basics", "basic",
        "Given an integer n, return the sum of the first n natural numbers "
        "(1 + 2 + ... + n).",
        [
            _ex("n = 5", "15", "1+2+3+4+5 = 15."),
            _ex("n = 100", "5050", "The classic Gauss sum."),
        ],
        ["1 <= n <= 10^9"],
        "Use long for the result since n*(n+1)/2 can overflow int for large n. "
        "Java's fixed-width types force you to think about overflow — a discipline "
        "Python hides. The O(1) formula beats any loop.",
        ["long result = (long) n * (n + 1) / 2; — cast BEFORE multiplying.",
         "int overflows near n = 65536; long is safe to 10^9."],
        "public long sumN(int n)",
        [_tc("n = 5", "15"), _tc("n = 100", "5050")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "ja-b02", "Even or Odd", "basics", "basic",
        "Given an integer n, return the string \"even\" if n is even and "
        "\"odd\" otherwise. Zero counts as even.",
        [
            _ex("n = 4", "\"even\"", "4 is divisible by 2."),
            _ex("n = -3", "\"odd\"", "-3 leaves remainder -1, still odd."),
        ],
        ["-10^9 <= n <= 10^9"],
        "n % 2 == 0 tests evenness; in Java, -3 % 2 is -1 (sign follows the "
        "dividend), unlike Python. Use .equals() for string comparison — never "
        "== on strings.",
        ["return n % 2 == 0 ? \"even\" : \"odd\";",
         "The ternary operator keeps it one line."],
        "public String evenOrOdd(int n)",
        [_tc("n = 4", "even"), _tc("n = -3", "odd")],
        companies=["tcs", "wipro"],
    ),
    _p(
        "ja-b03", "Factorial", "basics", "basic",
        "Given a non-negative integer n, return n! (n factorial). 0! = 1. "
        "Return a long.",
        [
            _ex("n = 5", "120", "5*4*3*2*1."),
            _ex("n = 0", "1", "Base case."),
        ],
        ["0 <= n <= 20"],
        "20! fits in a long (2.4M * ... = 2432902008176640000) but 21! overflows "
        "— hence the constraint. A simple for loop multiplying a running long "
        "is the standard iterative solution.",
        ["long result = 1; for (int i = 2; i <= n; i++) result *= i;",
         "Start result at 1 so n = 0 works."],
        "public long factorial(int n)",
        [_tc("n = 5", "120"), _tc("n = 0", "1")],
        companies=["tcs"],
    ),
    _p(
        "ja-b04", "Reverse a String", "basics", "basic",
        "Given a string s, return it reversed.",
        [
            _ex("s = \"hello\"", "\"olleh\"", "Characters in reverse order."),
            _ex("s = \"a\"", "\"a\"", "Single char unchanged."),
        ],
        ["0 <= s.length() <= 10^4"],
        "new StringBuilder(s).reverse().toString() is the idiomatic one-liner — "
        "StringBuilder is mutable, String is not. Manual char-array swapping "
        "teaches the two-pointer technique.",
        ["StringBuilder has a built-in reverse().",
         "Manual: swap chars[i] and chars[n-1-i]."],
        "public String reverse(String s)",
        [_tc("s = \"hello\"", "olleh"), _tc("s = \"\"", "")],
        companies=["tcs", "infosys", "amazon"],
    ),
    _p(
        "ja-b05", "Palindrome Number", "basics", "basic",
        "Given an integer n >= 0, return true if it reads the same forwards "
        "and backwards.",
        [
            _ex("n = 121", "true", "Reversed is 121."),
            _ex("n = 123", "false", "Reversed is 321."),
        ],
        ["0 <= n <= 10^9"],
        "Reverse the number arithmetically (rev = rev*10 + n%10) and compare — "
        "no string conversion needed. Negative numbers are never palindromes "
        "because of the minus sign.",
        ["Build rev digit by digit, then return rev == n.",
         "Watch overflow: use long for rev."],
        "public boolean isPalindrome(int n)",
        [_tc("n = 121", "true"), _tc("n = 10", "false")],
        companies=["infosys", "wipro"],
    ),
    _p(
        "ja-b06", "Largest in Array", "basics", "basic",
        "Given a non-empty int array, return its largest element.",
        [
            _ex("arr = [3, 7, 2, 9]", "9", "9 is the maximum."),
            _ex("arr = [-5, -1, -8]", "-1", "Largest among negatives."),
        ],
        ["1 <= arr.length <= 10^5"],
        "Initialize max to arr[0] (not 0 — arrays can be all-negative!) then scan. "
        "This 'champion' single pass is O(n). Arrays.asList doesn't work on "
        "int[] — use loops or streams.",
        ["int max = arr[0]; then compare each element.",
         "Starting at 0 fails for all-negative arrays."],
        "public int largest(int[] arr)",
        [_tc("arr = [3, 7, 2]", "7"), _tc("arr = [-5, -1]", "-1")],
        companies=["tcs"],
    ),
    _p(
        "ja-b07", "Fibonacci Nth", "basics", "easy",
        "Return the nth Fibonacci number (0-indexed: fib(0)=0, fib(1)=1) as "
        "a long, iteratively.",
        [
            _ex("n = 6", "8", "0,1,1,2,3,5,8."),
            _ex("n = 50", "12586269025", "Needs long, not int."),
        ],
        ["0 <= n <= 92"],
        "Keep only the last two values (a, b) and roll forward — O(n) time, "
        "O(1) space. fib(93) overflows long, hence the constraint. Iterative "
        "beats naive recursion here (no exponential blowup).",
        ["long a = 0, b = 1; loop n times: { long t = a+b; a = b; b = t; }",
         "After n iterations, a holds fib(n)."],
        "public long fib(int n)",
        [_tc("n = 6", "8"), _tc("n = 0", "0")],
        companies=["infosys"],
    ),
    _p(
        "ja-b08", "Prime Check", "basics", "easy",
        "Given an integer n, return true if n is prime, else false. Numbers "
        "below 2 are not prime.",
        [
            _ex("n = 7", "true", "No divisors except 1 and 7."),
            _ex("n = 1", "false", "Not prime by definition."),
        ],
        ["0 <= n <= 10^6"],
        "Check divisors only up to sqrt(n): if n = a*b, one factor is <= sqrt(n). "
        "Math.sqrt(n) or i*i <= n both work; the i*i form avoids floating point.",
        ["if (n < 2) return false;",
         "for (int i = 2; (long) i * i <= n; i++) if (n % i == 0) return false;"],
        "public boolean isPrime(int n)",
        [_tc("n = 7", "true"), _tc("n = 15", "false")],
        companies=["tcs", "wipro"],
    ),
    _p(
        "ja-b09", "Count Vowels", "basics", "basic",
        "Given a string s, return how many vowels (a,e,i,o,u, either case) "
        "it contains.",
        [
            _ex("s = \"Hello World\"", "3", "e, o, o."),
            _ex("s = \"rhythm\"", "0", "No vowels."),
        ],
        ["0 <= s.length() <= 10^4"],
        "Convert once with s.toLowerCase(), then check \"aeiou\".indexOf(c) >= 0. "
        "Strings are immutable in Java — every 'modification' creates a new "
        "object, so transform-then-scan is the norm.",
        ["String v = \"aeiou\"; loop chars of s.toLowerCase().",
         "Count when v.indexOf(c) != -1."],
        "public int countVowels(String s)",
        [_tc("s = \"Hello\"", "2"), _tc("s = \"xyz\"", "0")],
        companies=["tcs"],
    ),
    _p(
        "ja-b10", "Swap Two Numbers", "basics", "basic",
        "Given an int array of exactly 2 elements [a, b], swap them in place "
        "and return the array as [b, a].",
        [
            _ex("arr = [3, 7]", "[7, 3]", "Swapped."),
        ],
        ["arr.length == 2"],
        "The temp-variable swap (t = a; a = b; b = t) is the clearest and "
        "safest. Arithmetic/XOR swaps are clever but risk overflow and confuse "
        "readers — clarity wins in real code.",
        ["int t = arr[0]; arr[0] = arr[1]; arr[1] = t;",
         "Return arr after swapping in place."],
        "public int[] swap(int[] arr)",
        [_tc("arr = [3, 7]", "[7, 3]")],
        companies=["infosys"],
    ),

    # ================= OOP (10) =================
    _p(
        "ja-o01", "Student Class", "oop", "basic",
        "Create a class Student with private fields name (String) and marks "
        "(int), a constructor setting both, and a method getGrade() returning "
        "'A' if marks >= 90, 'B' if >= 75, 'C' if >= 60, else 'D'.",
        [
            _ex("new Student(\"A\", 95).getGrade()", "\"A\"", "95 >= 90."),
            _ex("new Student(\"B\", 70).getGrade()", "\"C\"", "70 >= 60."),
        ],
        ["0 <= marks <= 100"],
        "Private fields + public constructor is encapsulation: the object's "
        "state can only be set through controlled entry points. getGrade() "
        "encodes the grading rule inside the class that owns the data.",
        ["private String name; private int marks; — set in constructor.",
         "Chain if/else on marks thresholds."],
        "class Student {\n    public Student(String name, int marks) {}\n    public char getGrade() { return 'D'; }\n}",
        [_tc("new Student(\"A\", 95).getGrade()", "A"), _tc("new Student(\"B\", 50).getGrade()", "D")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "ja-o02", "Constructor Overloading", "oop", "easy",
        "Create class Rectangle with private width/height. Provide two "
        "constructors: Rectangle(w, h) and Rectangle(side) for squares. Add "
        "area() returning width*height.",
        [
            _ex("new Rectangle(3, 4).area()", "12", "3*4."),
            _ex("new Rectangle(5).area()", "25", "Square: 5*5."),
        ],
        ["Dimensions > 0"],
        "Constructors can be overloaded like methods — same name, different "
        "parameters. The single-arg version delegates: this(side, side). "
        "Overloading gives callers convenient shortcuts.",
        ["Rectangle(int side) { this(side, side); } — must be first line.",
         "Store both fields in the two-arg constructor."],
        "class Rectangle {\n    public Rectangle(int w, int h) {}\n    public Rectangle(int side) {}\n    public int area() { return 0; }\n}",
        [_tc("new Rectangle(3, 4).area()", "12"), _tc("new Rectangle(5).area()", "25")],
        companies=["infosys", "wipro"],
    ),
    _p(
        "ja-o03", "Vehicle Inheritance", "oop", "easy",
        "Create class Vehicle with method fuel() returning \"petrol\". Create "
        "class Car extends Vehicle overriding fuel() to return \"petrol+electric\" "
        "(hybrid). Create class Truck extends Vehicle returning \"diesel\".",
        [
            _ex("new Car().fuel()", "\"petrol+electric\"", "Overridden."),
            _ex("new Truck().fuel()", "\"diesel\"", "Overridden."),
        ],
        ["No constraints"],
        "extends creates an is-a relationship; @Override replaces the parent's "
        "method. A Vehicle reference to a Car still calls Car's fuel() — "
        "runtime polymorphism via dynamic dispatch.",
        ["class Car extends Vehicle { @Override public String fuel() ... }",
         "Use @Override so typos become compile errors."],
        "class Vehicle {\n    public String fuel() { return \"petrol\"; }\n}\nclass Car extends Vehicle {\n}\nclass Truck extends Vehicle {\n}",
        [_tc("new Car().fuel()", "petrol+electric"), _tc("new Vehicle().fuel()", "petrol")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "ja-o04", "Method Overriding Shapes", "oop", "easy",
        "Create class Shape with method area() returning 0.0. Create "
        "class Circle extends Shape with radius field, overriding area() to "
        "return Math.PI * r * r.",
        [
            _ex("new Circle(2).area() approx", "12.566", "pi * 4."),
        ],
        ["r > 0"],
        "Overriding lets subclasses specialize behavior while sharing the "
        "type. Shape s = new Circle(2); s.area() calls Circle's version — "
        "the compiler checks the type, the JVM picks the method at runtime.",
        ["Store radius via constructor.",
         "@Override public double area() { return Math.PI * radius * radius; }"],
        "class Shape {\n    public double area() { return 0.0; }\n}\nclass Circle extends Shape {\n    public Circle(double r) {}\n    public double area() { return 0.0; }\n}",
        [_tc("Math.round(new Circle(1).area() * 100)", "314")],
        companies=["tcs"],
    ),
    _p(
        "ja-o05", "Abstract Shape", "oop", "medium",
        "Create abstract class Shape with abstract method area(). Create "
        "class Square extends Shape with side field implementing area().",
        [
            _ex("new Square(4).area()", "16.0", "4*4."),
        ],
        ["side > 0"],
        "abstract methods have no body; abstract classes can't be instantiated. "
        "Subclasses MUST implement every abstract method — the compiler "
        "enforces the contract. Use abstract classes for 'is-a' templates.",
        ["abstract class Shape { public abstract double area(); }",
         "Square extends Shape and implements area()."],
        "abstract class Shape {\n    public abstract double area();\n}\nclass Square extends Shape {\n    public Square(double side) {}\n    public double area() { return 0.0; }\n}",
        [_tc("new Square(4).area()", "16.0")],
        companies=["infosys"],
    ),
    _p(
        "ja-o06", "Drawable Interface", "oop", "medium",
        "Create interface Drawable with method draw() (no body). Create class "
        "Circle2 implements Drawable printing \"circle\" via draw(), and class "
        "Square2 implements Drawable printing \"square\".",
        [
            _ex("new Circle2().draw()", "prints \"circle\"", "Interface implemented."),
        ],
        ["No constraints"],
        "Interfaces declare pure contracts; a class can implement many "
        "interfaces but extend only one class. Prefer interfaces for 'can-do' "
        "abilities — they keep designs flexible and testable.",
        ["interface Drawable { void draw(); }",
         "class Circle2 implements Drawable { public void draw() { ... } }"],
        "interface Drawable {\n    void draw();\n}\nclass Circle2 implements Drawable {\n    public void draw() {}\n}\nclass Square2 implements Drawable {\n    public void draw() {}\n}",
        [_tc("(new Circle2() instanceof Drawable)", "true")],
        companies=["wipro", "tcs"],
    ),
    _p(
        "ja-o07", "Encapsulated Person", "oop", "basic",
        "Create class Person with private age. Provide setAge(int a) that "
        "throws IllegalArgumentException if a < 0 or a > 150, else sets it. "
        "Provide getAge().",
        [
            _ex("setAge(30); getAge()", "30", "Valid age stored."),
            _ex("setAge(-5)", "IllegalArgumentException", "Rejected."),
        ],
        ["Any int input"],
        "Private fields + validating setters = encapsulation: invalid states "
        "become unrepresentable. Throwing IllegalArgumentException on bad input "
        "fails fast instead of corrupting state silently.",
        ["if (a < 0 || a > 150) throw new IllegalArgumentException(\"bad age\");",
         "getAge just returns the field."],
        "class Person {\n    public void setAge(int a) {}\n    public int getAge() { return 0; }\n}",
        [_tc("(new Person() {{ setAge(30); }}).getAge()", "30")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "ja-o08", "Static Counter", "oop", "easy",
        "Create class Visitor with a private static int count. Increment it "
        "in the constructor. Add public static int totalVisitors() returning "
        "count.",
        [
            _ex("new Visitor(); new Visitor(); Visitor.totalVisitors()", "2",
                "Counts across instances."),
        ],
        ["No constraints"],
        "static belongs to the class, not instances — one shared count. "
        "Constructors run per instance, so incrementing there counts creations. "
        "Static methods can't touch instance fields (no this).",
        ["private static int count = 0; in constructor: count++;",
         "public static int totalVisitors() { return count; }"],
        "class Visitor {\n    public Visitor() {}\n    public static int totalVisitors() { return 0; }\n}",
        [_tc("Visitor.totalVisitors() >= 0", "true")],
        companies=["infosys"],
    ),
    _p(
        "ja-o09", "Overloaded Adder", "oop", "easy",
        "Create class Adder with three overloaded add methods: add(int,int), "
        "add(int,int,int), and add(double,double) — each returning the sum.",
        [
            _ex("add(2, 3)", "5", "Two-int version."),
            _ex("add(1, 2, 3)", "6", "Three-int version."),
            _ex("add(1.5, 2.5)", "4.0", "Double version."),
        ],
        ["No constraints"],
        "Method overloading = same name, different signatures; the compiler "
        "picks by argument types at compile time (static polymorphism). "
        "Overloading is about convenience — one name, many shapes.",
        ["Three methods named add with different parameter lists.",
         "Return types may differ but signatures must."],
        "class Adder {\n    public int add(int a, int b) { return 0; }\n    public int add(int a, int b, int c) { return 0; }\n    public double add(double a, double b) { return 0.0; }\n}",
        [_tc("new Adder().add(2, 3)", "5"), _tc("new Adder().add(1.5, 2.5)", "4.0")],
        companies=["tcs"],
    ),
    _p(
        "ja-o10", "Super Constructor", "oop", "medium",
        "Create class Animal with a constructor Animal(String name) storing "
        "name. Create class Dog extends Animal with constructor Dog(String "
        "name, String breed) calling super(name) and storing breed. Add "
        "getInfo() returning name + \":\" + breed.",
        [
            _ex("new Dog(\"R\", \"Lab\").getInfo()", "\"R:Lab\"", "Both fields set."),
        ],
        ["Non-empty strings"],
        "If the parent has no no-arg constructor, the child MUST call "
        "super(...) as its first line. super() chains construction upward so "
        "every level initializes its own fields — construction order is "
        "parent-first.",
        ["Dog(...) { super(name); this.breed = breed; } — super first!",
         "getInfo returns name + \":\" + breed (name accessible if protected/public)."],
        "class Animal {\n    protected String name;\n    public Animal(String name) {}\n}\nclass Dog extends Animal {\n    public Dog(String name, String breed) { super(name); }\n    public String getInfo() { return \"\"; }\n}",
        [_tc("new Dog(\"R\", \"Lab\").getInfo()", "R:Lab")],
        companies=["infosys", "wipro"],
    ),

    # ================= COLLECTIONS (10) =================
    _p(
        "ja-c01", "Dedupe List", "collections", "easy",
        "Given an ArrayList<Integer>, return a new ArrayList with duplicates "
        "removed, preserving first-occurrence order.",
        [
            _ex("[3, 1, 3, 2, 1]", "[3, 1, 2]", "Order kept."),
        ],
        ["0 <= size <= 10^4"],
        "new ArrayList<>(new LinkedHashSet<>(list)) dedupes in O(n) with order "
        "preserved — LinkedHashSet remembers insertion order. Plain HashSet is "
        "faster but scrambles order.",
        ["LinkedHashSet removes dupes, keeps order.",
         "Wrap back in ArrayList for the return type."],
        "import java.util.*;\npublic ArrayList<Integer> dedupe(ArrayList<Integer> list)",
        [_tc("dedupe(new ArrayList<>(Arrays.asList(1, 2, 1)))", "[1, 2]")],
        companies=["amazon", "flipkart"],
    ),
    _p(
        "ja-c02", "Word Frequency Map", "collections", "easy",
        "Given a String[] of words, return a HashMap<String, Integer> of "
        "word counts.",
        [
            _ex("[\"a\", \"b\", \"a\"]", "{a=2, b=1}", "Counts mapped."),
        ],
        ["0 <= length <= 10^4"],
        "map.getOrDefault(w, 0) + 1 counts without null checks; "
        "map.merge(w, 1, Integer::sum) is the one-liner. HashMap gives O(1) "
        "average put/get — the engine of counting problems.",
        ["for (String w : words) map.put(w, map.getOrDefault(w, 0) + 1);",
         "Return the map."],
        "import java.util.*;\npublic HashMap<String, Integer> wordFreq(String[] words)",
        [_tc("wordFreq(new String[]{\"x\",\"y\",\"x\"}).get(\"x\")", "2")],
        companies=["amazon"],
    ),
    _p(
        "ja-c03", "Find Duplicates", "collections", "easy",
        "Given an int[], return a sorted ArrayList<Integer> of values that "
        "appear more than once.",
        [
            _ex("[4, 3, 2, 7, 8, 2, 3, 1]", "[2, 3]", "2 and 3 repeat."),
            _ex("[1, 2, 3]", "[]", "No duplicates."),
        ],
        ["1 <= length <= 10^5"],
        "A HashSet tracks seen values; a second set collects repeats — one "
        "pass, O(n). Collections.sort() the result. Sets turn 'have I seen "
        "this?' into O(1).",
        ["seen.add fails (returns false) -> it's a duplicate.",
         "Collect dupes in a set, sort into a list."],
        "import java.util.*;\npublic ArrayList<Integer> findDupes(int[] arr)",
        [_tc("findDupes(new int[]{1, 2, 1, 3, 2})", "[1, 2]")],
        companies=["amazon", "flipkart"],
    ),
    _p(
        "ja-c04", "Sort Descending", "collections", "easy",
        "Given an ArrayList<Integer>, return a new list sorted in descending "
        "order.",
        [
            _ex("[3, 1, 4, 1, 5]", "[5, 4, 3, 1, 1]", "Descending."),
        ],
        ["0 <= size <= 10^4"],
        "Collections.sort(list, Collections.reverseOrder()) sorts descending "
        "in place — copy first to avoid mutating input. Comparators define "
        "ordering; reverseOrder() flips natural ordering.",
        ["Copy: new ArrayList<>(list), then sort with reverseOrder().",
         "Or sort ascending then Collections.reverse()."],
        "import java.util.*;\npublic ArrayList<Integer> sortDesc(ArrayList<Integer> list)",
        [_tc("sortDesc(new ArrayList<>(Arrays.asList(2, 1, 3)))", "[3, 2, 1]")],
        companies=["tcs"],
    ),
    _p(
        "ja-c05", "Reverse Linked List", "collections", "medium",
        "Given a LinkedList<Integer>, return a new LinkedList with elements "
        "reversed. Do not modify the input.",
        [
            _ex("[1, 2, 3]", "[3, 2, 1]", "Reversed copy."),
        ],
        ["0 <= size <= 10^4"],
        "Collections.reverse(copy) reverses in place — so copy first. "
        "LinkedList shines at head/tail ops; ArrayList at random access. "
        "Choosing the right List implementation matters.",
        ["LinkedList<Integer> r = new LinkedList<>(list);",
         "Collections.reverse(r); return r;"],
        "import java.util.*;\npublic LinkedList<Integer> reverseLL(LinkedList<Integer> list)",
        [_tc("reverseLL(new LinkedList<>(Arrays.asList(1, 2)))", "[2, 1]")],
        companies=["amazon"],
    ),
    _p(
        "ja-c06", "Two Sum Indices", "collections", "medium",
        "Given an int[] and target, return int[]{i, j} (i < j) with "
        "arr[i] + arr[j] == target. Exactly one solution exists.",
        [
            _ex("[2, 7, 11, 15], 9", "[0, 1]", "2+7=9."),
        ],
        ["2 <= length <= 10^4"],
        "HashMap value->index; for x, look up target - x — O(n). Check BEFORE "
        "inserting x so you never pair an element with itself. The complement-"
        "lookup pattern dominates array problems.",
        ["Map<Integer,Integer> seen = new HashMap<>();",
         "if (seen.containsKey(need)) return new int[]{seen.get(need), i};"],
        "import java.util.*;\npublic int[] twoSum(int[] arr, int target)",
        [_tc("Arrays.toString(twoSum(new int[]{2,7,11,15}, 9))", "[0, 1]")],
        companies=["amazon", "google"],
    ),
    _p(
        "ja-c07", "Sorted Key Map", "collections", "easy",
        "Given a HashMap<String, Integer>, return its entries as a list of "
        "\"key=value\" strings sorted by key ascending.",
        [
            _ex("{b=2, a=1}", "[\"a=1\", \"b=2\"]", "Keys sorted."),
        ],
        ["0 <= size <= 10^3"],
        "TreeMap sorts keys automatically (Red-Black tree, O(log n) ops). "
        "new TreeMap<>(hashMap) converts; then iterate entrySet(). When order "
        "matters, reach for TreeMap/TreeSet.",
        ["TreeMap<String,Integer> t = new TreeMap<>(map);",
         "Build k + \"=\" + v strings from t.entrySet()."],
        "import java.util.*;\npublic ArrayList<String> sortedEntries(HashMap<String, Integer> map)",
        [_tc("sortedEntries(new HashMap<>(Map.of(\"b\", 2, \"a\", 1)))", "[a=1, b=2]")],
        companies=["flipkart"],
    ),
    _p(
        "ja-c08", "Queue with LinkedList", "collections", "medium",
        "Implement a FIFO queue with enqueue(x)/dequeue() using LinkedList "
        "as storage. dequeue on empty throws NoSuchElementException.",
        [
            _ex("enqueue 1, 2; dequeue", "1", "First in, first out."),
        ],
        ["Values in int range"],
        "LinkedList implements Deque: addLast() enqueues, removeFirst() "
        "dequeues in O(1). Programming to the Queue interface (not the "
        "concrete class) keeps implementations swappable.",
        ["private LinkedList<Integer> q = new LinkedList<>();",
         "enqueue: q.addLast(x); dequeue: return q.removeFirst();"],
        "import java.util.*;\nclass MyQueue {\n    public void enqueue(int x) {}\n    public int dequeue() { return 0; }\n}",
        [_tc("(new MyQueue() {{ enqueue(5); enqueue(6); }}).dequeue()", "5")],
        companies=["amazon"],
    ),
    _p(
        "ja-c09", "Max in List", "collections", "basic",
        "Given an ArrayList<Integer> (non-empty), return its maximum value.",
        [
            _ex("[3, 7, 2, 9]", "9", "Maximum."),
        ],
        ["1 <= size <= 10^5"],
        "Collections.max(list) is the one-liner; a manual loop teaches the "
        "champion pattern. Note: Collections.max throws on empty lists — "
        "guard or document the precondition.",
        ["Collections.max(list) — simplest.",
         "Manual: track best, update when larger found."],
        "import java.util.*;\npublic int maxList(ArrayList<Integer> list)",
        [_tc("maxList(new ArrayList<>(Arrays.asList(3, 7, 2)))", "7")],
        companies=["tcs"],
    ),
    _p(
        "ja-c10", "Merge Sorted Lists", "collections", "medium",
        "Given two sorted ArrayList<Integer>, merge into one sorted "
        "ArrayList. Do not use Collections.sort.",
        [
            _ex("[1, 3, 5], [2, 4, 6]", "[1, 2, 3, 4, 5, 6]", "Interleaved merge."),
            _ex("[], [1]", "[1]", "Empty handled."),
        ],
        ["0 <= sizes <= 10^4"],
        "The two-pointer merge: compare heads, take the smaller, advance that "
        "pointer — O(n+m). This is merge sort's merge step and the template "
        "for all sorted-array problems.",
        ["i=j=0; while both remain: add smaller, advance.",
         "Append leftovers after one list exhausts."],
        "import java.util.*;\npublic ArrayList<Integer> mergeSorted(ArrayList<Integer> a, ArrayList<Integer> b)",
        [_tc("mergeSorted(new ArrayList<>(Arrays.asList(1,3)), new ArrayList<>(Arrays.asList(2)))", "[1, 2, 3]")],
        companies=["amazon", "google"],
    ),

    # ================= ADVANCED (10) =================
    _p(
        "ja-a01", "Safe Parse Int", "advanced", "basic",
        "Write parseInt(String s) returning the int value, or -1 if s is not "
        "a valid integer (catch NumberFormatException).",
        [
            _ex("\"42\"", "42", "Parsed."),
            _ex("\"abc\"", "-1", "Exception caught."),
        ],
        ["s non-null"],
        "try { return Integer.parseInt(s); } catch (NumberFormatException e) "
        "{ return -1; } — checked vs unchecked exceptions: NumberFormatException "
        "is unchecked (RuntimeException), so no throws clause needed.",
        ["Integer.parseInt throws NumberFormatException on bad input.",
         "Catch it specifically, not generic Exception."],
        "public int parseInt(String s)",
        [_tc("parseInt(\"42\")", "42"), _tc("parseInt(\"xx\")", "-1")],
        companies=["tcs"],
    ),
    _p(
        "ja-a02", "Age Validator", "advanced", "medium",
        "Write validateAge(int age): throw IllegalArgumentException(\"too "
        "young\") if age < 18, (\"too old\") if age > 120, else return \"ok\".",
        [
            _ex("25", "\"ok\"", "Valid."),
            _ex("10", "throws \"too young\"", "Rejected."),
        ],
        ["Any int"],
        "IllegalArgumentException signals bad arguments — unchecked, so callers "
        "aren't forced to catch. Fail-fast validation at method entry keeps "
        "invariants intact throughout the object.",
        ["if (age < 18) throw new IllegalArgumentException(\"too young\");",
         "Check upper bound, then return \"ok\"."],
        "public String validateAge(int age)",
        [_tc("validateAge(25)", "ok")],
        companies=["infosys"],
    ),
    _p(
        "ja-a03", "Generic Box", "advanced", "medium",
        "Create a generic class Box<T> with set(T value)/get() returning T. "
        "Demonstrate type safety: Box<String> holding \"hi\".",
        [
            _ex("Box<String> b; b.set(\"hi\"); b.get()", "\"hi\"", "Type-safe, no cast."),
        ],
        ["No constraints"],
        "Generics (Box<T>) move type checks to compile time — no casts, no "
        "ClassCastException at runtime. Type erasure means T is Object at "
        "runtime, but the compiler guarantees safety.",
        ["class Box<T> { private T value; ... }",
         "get() returns T directly — no cast needed."],
        "class Box<T> {\n    public void set(T value) {}\n    public T get() { return null; }\n}",
        [_tc("(new Box<String>() {{ set(\"hi\"); }}).get()", "hi")],
        companies=["amazon"],
    ),
    _p(
        "ja-a04", "Stream Filter Evens", "advanced", "medium",
        "Given a List<Integer>, use streams to return a new List of only the "
        "even numbers.",
        [
            _ex("[1, 2, 3, 4]", "[2, 4]", "Evens kept."),
        ],
        ["List non-null"],
        "list.stream().filter(x -> x % 2 == 0).collect(Collectors.toList()) — "
        "declarative: describe WHAT, not HOW. Streams are lazy until a terminal "
        "op (collect) runs; they don't mutate the source.",
        ["filter takes a Predicate lambda.",
         "collect(Collectors.toList()) is the terminal op."],
        "import java.util.*;\nimport java.util.stream.*;\npublic List<Integer> evens(List<Integer> list)",
        [_tc("evens(Arrays.asList(1, 2, 3, 4))", "[2, 4]")],
        companies=["flipkart", "amazon"],
    ),
    _p(
        "ja-a05", "Stream Sum of Squares", "advanced", "medium",
        "Given a List<Integer>, use streams to return the sum of squares as "
        "an int.",
        [
            _ex("[1, 2, 3]", "14", "1+4+9."),
        ],
        ["List non-null"],
        "mapToInt(x -> x * x).sum() — mapToInt avoids boxing overhead by "
        "working with primitive int streams. Primitive specializations "
        "(IntStream, LongStream) exist precisely for performance.",
        ["mapToInt produces an IntStream.",
         ".sum() is the terminal reduction."],
        "import java.util.*;\npublic int sumSquares(List<Integer> list)",
        [_tc("sumSquares(Arrays.asList(1, 2, 3))", "14")],
        companies=["amazon"],
    ),
    _p(
        "ja-a06", "Sort by Length Lambda", "advanced", "medium",
        "Given a List<String>, return a new list sorted by string length "
        "ascending, using a lambda comparator. Do not modify the input.",
        [
            _ex("[\"bb\", \"a\", \"ccc\"]", "[\"a\", \"bb\", \"ccc\"]", "By length."),
        ],
        ["No nulls"],
        "Comparator.comparingInt(String::length) is the method-reference form; "
        "(a, b) -> a.length() - b.length() is the lambda form. Lambdas are "
        "shorthand for single-method interfaces — the core of functional Java.",
        ["Copy list, then sort with the comparator.",
         "comparingInt avoids integer-subtraction overflow bugs."],
        "import java.util.*;\npublic List<String> sortByLen(List<String> list)",
        [_tc("sortByLen(Arrays.asList(\"bb\", \"a\"))", "[a, bb]")],
        companies=["flipkart"],
    ),
    _p(
        "ja-a07", "Count File Lines", "advanced", "easy",
        "Given a file path, return the number of lines using "
        "try-with-resources so the reader always closes.",
        [
            _ex("file with 3 lines", "3", "Lines counted."),
        ],
        ["File exists"],
        "try (BufferedReader br = new BufferedReader(new FileReader(path))) "
        "auto-closes br — no finally block needed. try-with-resources works "
        "with anything implementing AutoCloseable.",
        ["Loop while ((line = br.readLine()) != null) count++.",
         "Declare the reader inside try(...) parentheses."],
        "import java.io.*;\npublic int countLines(String path) throws IOException",
        [_tc("countLines(\"/tmp/jlines.txt\")", "3")],
        companies=["tcs", "wipro"],
    ),
    _p(
        "ja-a08", "Two Threads Count", "advanced", "medium",
        "Create and start two Threads, each printing numbers 1..3. Return "
        "the string \"done\" after both finish (use join()).",
        [
            _ex("run()", "\"done\"", "Both threads completed."),
        ],
        ["No constraints"],
        "thread.start() begins execution; thread.join() waits for it. Without "
        "join, main can return before threads finish. Extending Thread vs "
        "implementing Runnable — prefer Runnable (frees inheritance).",
        ["Create t1, t2; start both; join both; return \"done\".",
         "join() throws InterruptedException — declare throws."],
        "public String runThreads() throws InterruptedException",
        [_tc("runThreads()", "done")],
        companies=["amazon", "google"],
    ),
    _p(
        "ja-a09", "Safe Get Optional", "advanced", "medium",
        "Given a HashMap<String, String>, write getOrDefault2(map, key) "
        "returning the value or \"N/A\" if absent — using Optional (not "
        "Map.getOrDefault).",
        [
            _ex("map={a=1}, key=\"b\"", "\"N/A\"", "Absent -> default."),
            _ex("map={a=1}, key=\"a\"", "\"1\"", "Present -> value."),
        ],
        ["Map non-null"],
        "Optional.ofNullable(map.get(key)).orElse(\"N/A\") makes absence "
        "explicit in the type. Optional is for return values signaling "
        "'maybe nothing' — never for fields or parameters.",
        ["ofNullable wraps a possibly-null value.",
         "orElse supplies the fallback."],
        "import java.util.*;\npublic String getOrDefault2(HashMap<String, String> map, String key)",
        [_tc("getOrDefault2(new HashMap<>(Map.of(\"a\", \"1\")), \"b\")", "N/A")],
        companies=["google"],
    ),
    _p(
        "ja-a10", "Reverse Words", "advanced", "easy",
        "Given a sentence, return it with words in reverse order, single-"
        "spaced. Use StringBuilder for building.",
        [
            _ex("\"hello world java\"", "\"java world hello\"", "Words reversed."),
        ],
        ["Words separated by single spaces"],
        "Split on \" \", iterate backwards appending to a StringBuilder, trim "
        "the trailing space. StringBuilder avoids the O(n^2) cost of += on "
        "Strings in loops (each += copies).",
        ["String[] w = s.split(\" \"); append from end.",
         "Delete trailing space or trim at the end."],
        "public String reverseWords(String s)",
        [_tc("reverseWords(\"a b c\")", "c b a")],
        companies=["amazon", "flipkart"],
    ),

    # ================= PRACTICE (10) =================
    _p(
        "ja-p01", "FizzBuzz", "practice", "basic",
        "Given n, return a List<String> for 1..n: \"Fizz\" for multiples of 3, "
        "\"Buzz\" for multiples of 5, \"FizzBuzz\" for both, else the number.",
        [
            _ex("n = 5", "[\"1\",\"2\",\"Fizz\",\"4\",\"Buzz\"]", "Classic rules."),
            _ex("n = 15 last", "\"FizzBuzz\"", "15 is both."),
        ],
        ["1 <= n <= 10^4"],
        "Check divisibility by 15 FIRST — else the 3-check swallows it. Order "
        "of conditions matters whenever cases overlap. FizzBuzz screens for "
        "basic loop + branch competence.",
        ["if (i % 15 == 0) FizzBuzz; else if (i % 3 == 0) Fizz; ...",
         "Add String.valueOf(i) otherwise."],
        "import java.util.*;\npublic List<String> fizzBuzz(int n)",
        [_tc("fizzBuzz(3)", "[1, 2, Fizz]")],
        companies=["tcs", "infosys", "wipro"],
    ),
    _p(
        "ja-p02", "Anagram Check", "practice", "easy",
        "Given two lowercase strings, return true if they are anagrams.",
        [
            _ex("\"listen\", \"silent\"", "true", "Same letters."),
            _ex("\"hello\", \"world\"", "false", "Different letters."),
        ],
        ["0 <= lengths <= 10^4"],
        "Sort both char arrays and compare — O(n log n) and obviously correct. "
        "The O(n) counting version (26-slot frequency array) is the follow-up. "
        "Anagrams = same multiset of characters.",
        ["char[] a = s.toCharArray(); Arrays.sort(a); compare with Arrays.equals.",
         "Different lengths -> false immediately."],
        "import java.util.*;\npublic boolean isAnagram(String s, String t)",
        [_tc("isAnagram(\"listen\", \"silent\")", "true"), _tc("isAnagram(\"a\", \"b\")", "false")],
        companies=["amazon", "google"],
    ),
    _p(
        "ja-p03", "Missing Number", "practice", "easy",
        "Given an int[] containing n distinct numbers from 0..n, return the "
        "missing one.",
        [
            _ex("[3, 0, 1]", "2", "2 is missing."),
            _ex("[0, 1]", "2", "n = 2, missing 2."),
        ],
        ["1 <= n <= 10^4"],
        "Sum 0..n = n*(n+1)/2; subtract the array's sum — the difference is "
        "the missing number, O(n) time O(1) space. XOR of all indices+values "
        "also works and avoids overflow entirely.",
        ["expected = n*(n+1)/2 as long; subtract each arr[i].",
         "Return (int)(expected - actual)."],
        "public int missingNumber(int[] arr)",
        [_tc("missingNumber(new int[]{3, 0, 1})", "2")],
        companies=["amazon"],
    ),
    _p(
        "ja-p04", "Binary Search", "practice", "medium",
        "Given a sorted int[] and target, return its index or -1 if absent. "
        "Implement binary search manually (no Arrays.binarySearch).",
        [
            _ex("[1, 3, 5, 7], 5", "2", "Found at index 2."),
            _ex("[1, 3, 5], 4", "-1", "Not present."),
        ],
        ["0 <= length <= 10^5", "sorted ascending"],
        "Halve the search space each step: mid = lo + (hi-lo)/2 avoids "
        "overflow (unlike (lo+hi)/2). O(log n). Binary search is the template "
        "for all 'search in sorted structure' problems.",
        ["while (lo <= hi): compute mid, compare, shrink half.",
         "Return -1 when lo > hi."],
        "public int binarySearch(int[] arr, int target)",
        [_tc("binarySearch(new int[]{1,3,5,7}, 5)", "2"), _tc("binarySearch(new int[]{1,3}, 2)", "-1")],
        companies=["amazon", "google"],
    ),
    _p(
        "ja-p05", "Bubble Sort", "practice", "easy",
        "Given an int[], sort it ascending in place using bubble sort and "
        "return it.",
        [
            _ex("[5, 3, 8, 1]", "[1, 3, 5, 8]", "Sorted."),
        ],
        ["0 <= length <= 10^3"],
        "Repeatedly bubble the largest remaining element to the end via "
        "adjacent swaps; after pass i, the last i are fixed. O(n^2), but the "
        "early-exit flag (no swaps -> done) makes nearly-sorted input O(n).",
        ["for i in 0..n-1: swapped=false; for j in 0..n-2-i: swap if out of order.",
         "Break early if a full pass swaps nothing."],
        "public int[] bubbleSort(int[] arr)",
        [_tc("Arrays.toString(bubbleSort(new int[]{3,1,2}))", "[1, 2, 3]")],
        companies=["tcs", "infosys"],
    ),
    _p(
        "ja-p06", "Char Frequency", "practice", "easy",
        "Given a lowercase string, return a HashMap<Character, Integer> of "
        "character counts.",
        [
            _ex("\"aabbc\"", "{a=2, b=2, c=1}", "Counts."),
        ],
        ["0 <= length <= 10^4", "a-z only"],
        "Same counting pattern as word frequency, keyed by Character. "
        "Autoboxing converts char <-> Character automatically. For a-z only, "
        "an int[26] is even faster — know both.",
        ["for (char c : s.toCharArray()) map.put(c, map.getOrDefault(c, 0)+1);",
         "Return the map."],
        "import java.util.*;\npublic HashMap<Character, Integer> charFreq(String s)",
        [_tc("charFreq(\"aab\").get('a')", "2")],
        companies=["amazon"],
    ),
    _p(
        "ja-p07", "Longest Word", "practice", "easy",
        "Given a sentence (words separated by single spaces), return the "
        "longest word. Ties -> first occurrence.",
        [
            _ex("\"the quick brown fox\"", "\"quick\"", "5 letters, first of ties."),
        ],
        ["Non-empty"],
        "Split and track the champion: strictly-greater comparison keeps the "
        "FIRST longest on ties. The champion pattern (best-so-far + strict "
        "update) appears in max/min problems everywhere.",
        ["String best = \"\"; for (String w : s.split(\" \")) if (w.length() > best.length()) best = w;",
         "Strict > keeps first occurrence on ties."],
        "public String longestWord(String s)",
        [_tc("longestWord(\"a bb ccc\")", "ccc")],
        companies=["flipkart"],
    ),
    _p(
        "ja-p08", "GCD", "practice", "easy",
        "Given two positive ints a, b, return their greatest common divisor.",
        [
            _ex("12, 18", "6", "Largest shared divisor."),
            _ex("7, 5", "1", "Coprime."),
        ],
        ["1 <= a, b <= 10^6"],
        "Euclid: gcd(a,b) = gcd(b, a%b) — logarithmic time. The loop version "
        "(while b != 0: t = a%b; a = b; b = t) avoids recursion depth concerns. "
        "GCD underlies fraction reduction and modular arithmetic.",
        ["while (b != 0) { int t = a % b; a = b; b = t; } return a;",
         "gcd(a, 0) = a is the base case."],
        "public int gcd(int a, int b)",
        [_tc("gcd(12, 18)", "6"), _tc("gcd(7, 5)", "1")],
        companies=["tcs"],
    ),
    _p(
        "ja-p09", "Armstrong Number", "practice", "medium",
        "Given n >= 0, return true if it is Armstrong: sum of its digits "
        "each raised to the digit count equals n.",
        [
            _ex("153", "true", "1^3+5^3+3^3 = 153."),
            _ex("123", "false", "Sums to 36."),
        ],
        ["0 <= n <= 10^5"],
        "Count digits first, then sum Math.pow(digit, count) — needs the count "
        "before the sum, so two passes over the digits. Math.pow returns "
        "double; cast carefully or multiply manually.",
        ["int digits = String.valueOf(n).length(); then peel digits.",
         "sum += (int) Math.pow(d, digits); compare to n."],
        "public boolean isArmstrong(int n)",
        [_tc("isArmstrong(153)", "true"), _tc("isArmstrong(123)", "false")],
        companies=["infosys", "wipro"],
    ),
    _p(
        "ja-p10", "Matrix Transpose", "practice", "medium",
        "Given an m x n int[][], return its n x m transpose (rows become "
        "columns).",
        [
            _ex("[[1,2,3],[4,5,6]]", "[[1,4],[2,5],[3,6]]", "Flipped over diagonal."),
        ],
        ["1 <= m, n <= 100"],
        "Allocate result[n][m], then result[j][i] = a[i][j] — indices swap. "
        "Rectangular (non-square) transpose needs a NEW array; in-place only "
        "works for square matrices.",
        ["int[][] t = new int[n][m]; nested loops copy t[j][i] = a[i][j].",
         "Handle empty matrix (m or n = 0) gracefully."],
        "public int[][] transpose(int[][] a)",
        [_tc("Arrays.deepToString(transpose(new int[][]{{1,2},{3,4}}))", "[[1, 3], [2, 4]]")],
        companies=["amazon"],
    ),
]


def get_problems(topic: str | None = None, difficulty: str | None = None) -> list[CodingProblem]:
    """Return problems, optionally filtered by topic and/or difficulty.

    Preserves bank order (basics -> practice progression).
    """
    out = _JAVA_BANK
    if topic is not None:
        out = [p for p in out if p.topic == topic]
    if difficulty is not None:
        out = [p for p in out if p.difficulty == difficulty]
    return list(out)


def get_problem(pid: str) -> CodingProblem | None:
    """Return the problem with the given id, or None if unknown."""
    for p in _JAVA_BANK:
        if p.id == pid:
            return p
    return None


def list_topics() -> list[str]:
    """Return topic slugs in bank (progression) order."""
    seen: list[str] = []
    for p in _JAVA_BANK:
        if p.topic not in seen:
            seen.append(p.topic)
    return seen

