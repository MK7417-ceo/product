"""Seed content: OOP — Modules 1-2 (OOP Basics, Inheritance).

Interview-focused curriculum content for SkillForge Part 1 (Core).
All content is original; code examples are runnable as written.
"""

from __future__ import annotations

MODULES = [
    {
        "slug": "oop-basics",
        "name": "OOP Basics",
        "description": (
            "Learn Object-Oriented Programming from zero: classes, objects, "
            "constructors, encapsulation and abstraction — the vocabulary and "
            "mechanics every placement interview expects you to know cold."
        ),
        "lessons": [
            {
                "slug": "oop-what-is-oop",
                "title": "What is OOP? The 4 Pillars",
                "theory_md": """## What is OOP? The 4 Pillars

**OOP (Object-Oriented Programming)** is a way of writing code by modelling
real-world things as **objects** — bundles of data (attributes) and behaviour
(methods). A `Car` object carries its own `speed` and knows how to `brake()`.

### Procedural vs OOP

Procedural code (C-style) keeps data and functions separate:

```python
# Procedural: data and functions live apart
speeds = {"car1": 60}
def brake(speeds, car):
    speeds[car] = max(0, speeds[car] - 10)
```

OOP keeps them together inside the object, which scales better when a program
has hundreds of interacting parts.

### The 4 Pillars — a first taste

| Pillar | One-line idea | Tiny taste |
|---|---|---|
| **Encapsulation** | Bundle data + methods; hide internals | `self.__balance` can't be touched directly |
| **Abstraction** | Show *what*, hide *how* | `car.drive()` — you don't see the engine |
| **Inheritance** | Reuse code via IS-A hierarchies | `class Dog(Animal)` reuses `Animal.eat()` |
| **Polymorphism** | Same call, different behaviour | `shape.area()` works for Circle *and* Square |

```python
# All four pillars in 12 lines
class Animal:                       # abstraction: eat() hides details
    def __init__(self, name):
        self.__name = name          # encapsulation: private by convention
    def speak(self):
        return "..."

class Dog(Animal):                  # inheritance: Dog IS-A Animal
    def speak(self):                # polymorphism: same call, new behaviour
        return "Woof!"

print(Dog("Rex").speak())           # Woof!
```

The same idea in Java:

```java
class Dog extends Animal {          // inheritance
    @Override
    public String speak() {         // polymorphism
        return "Woof!";
    }
}
```

### Interview traps

- "OOP vs procedural?" — interviewers want *data+behaviour bundling*, not just "it uses classes".
- Mixing up encapsulation and abstraction is the #1 beginner trap (fixed in lesson 5).
- OOP is a *paradigm*, not a language feature — you can write OOP in Python, Java, C++.

**Takeaway:** OOP organises code into objects; its four pillars are encapsulation, abstraction, inheritance, and polymorphism.""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": True,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer opens with: 'In one sentence — what makes a program object-oriented?' Which answer earns the nod?",
                        "choices": [
                            "Organising code into objects that bundle data and the behaviour that operates on it",
                            "Compiling programs faster than procedural languages",
                            "Writing code as a single long sequence of instructions",
                            "Keeping all data in global variables shared by functions",
                        ],
                        "answer_index": 0,
                        "difficulty": 1,
                        "explanation": "OOP's defining idea is bundling state (attributes) and behaviour (methods) into objects that model real-world entities. This keeps related code together, unlike procedural code where data and functions live apart. Interviewers look for exactly this one-line definition.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Rapid-fire at Wipro: 'Polymorphism, compilation, encapsulation, inheritance — which one is NOT a pillar of OOP?'",
                        "choices": [
                            "Polymorphism",
                            "Compilation",
                            "Encapsulation",
                            "Inheritance",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "The four pillars are encapsulation, abstraction, inheritance, and polymorphism. Compilation is a language-implementation detail and has nothing to do with the OOP paradigm. This is a classic rapid-fire screening question.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your interviewer writes `class Dog(Animal)` on the whiteboard and asks: 'Which pillar am I demonstrating here — and what's the giveaway?'",
                        "choices": [
                            "Encapsulation, because Dog hides Animal's data",
                            "Abstraction, because Dog simplifies Animal",
                            "Inheritance, because Dog IS-A Animal and reuses its code",
                            "Polymorphism, because Dog changes Animal's type",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Dog extending Animal is inheritance: Dog IS-A Animal, so it inherits fields and methods and can reuse or override them. Encapsulation is about hiding internals, and polymorphism is about same-call-different-behaviour — related but different concepts.",
                        "company_tags": ["cognizant", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You're reviewing a teammate's PR on an Infosys banking project: the `BankAccount` class exposes `deposit()` and `withdraw()` but keeps `balance` private. The reviewer asks which pillar this design leans on. What do you say?",
                        "choices": [
                            "Abstraction, because the account is a simplified model",
                            "Inheritance, because the account reuses bank code",
                            "Polymorphism, because deposit behaves differently per account",
                            "Encapsulation, because internal state is bundled and guarded by methods",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "This is encapsulation: data (balance) and the methods that manage it are bundled together, and the internal state is protected from direct outside manipulation. Abstraction is close — deposit hides complexity — but the *guarding of state* is the encapsulation signature.",
                        "company_tags": ["infosys", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer demos this live: `shape.area()` returns 78.5 for a Circle and 25.0 for a Square — same call, different result. 'Which pillar did I just show you?' she asks.",
                        "choices": [
                            "Abstraction — shapes are simplified models",
                            "Polymorphism — one interface, many behaviours",
                            "Encapsulation — the area formula is hidden",
                            "Inheritance — Circle inherits from Shape",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "This is textbook polymorphism: the same method call dispatches to different implementations depending on the object's actual type. Inheritance may enable it (both extend Shape), but the *same call, different behaviour* phenomenon is polymorphism.",
                        "company_tags": ["amazon", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Razorpay interviewer poses a design problem: 'We add a new payment method every quarter — cards today, UPI tomorrow. How does OOP stop this from turning into spaghetti?' Which answer do you give?",
                        "choices": [
                            "Avoid classes entirely and use global functions for speed",
                            "Use procedural code, since payment logic rarely changes",
                            "Model each payment method as a class sharing a common Payment interface, so new methods plug in via polymorphism without touching existing code",
                            "Put all payment logic in one giant class to keep it simple",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "This is the Open/Closed Principle in action: model each payment type as a class behind a common interface so the system is open for extension (new payment types) but closed for modification. Polymorphism lets new classes plug in without rewriting tested code — exactly why OOP wins for evolving systems.",
                        "company_tags": ["razorpay", "phonepe"],
                    },
                ],
            },
            {
                "slug": "oop-classes-objects",
                "title": "Classes vs Objects",
                "theory_md": """## Classes vs Objects

A **class** is a blueprint; an **object** is a house built from it. One class
can produce many objects, each with its own data but sharing the same design.

### The anatomy

- **Attributes** (fields): the data an object holds — `name`, `speed`.
- **Methods**: the behaviours — `brake()`, `accelerate()`.
- **Instantiation**: creating an object from a class — `Car()`.

```python
class Car:                              # the blueprint
    def __init__(self, brand, speed=0):  # attributes set per object
        self.brand = brand
        self.speed = speed
    def accelerate(self, by=10):        # a method
        self.speed += by

c1 = Car("Tata")        # object 1
c2 = Car("Honda", 40)   # object 2 — same class, different data
c1.accelerate()
print(c1.speed, c2.speed)   # 10 40  — independent state
```

The same in Java — note the explicit types and `new`:

```java
class Car {
    String brand;
    int speed;
    Car(String brand, int speed) {
        this.brand = brand;
        this.speed = speed;
    }
    void accelerate(int by) { speed += by; }
}

Car c1 = new Car("Tata", 0);   // 'new' allocates the object
c1.accelerate(10);
```

### Class vs object — the interview table

| Class | Object |
|---|---|
| Blueprint / template | Real instance of the class |
| Declared once | Created many times (`new` / `Class()`) |
| Defines structure | Holds actual values |
| No memory at runtime (just the definition) | Occupies memory |

### Interview traps

- "Can you call a method without creating an object?" — Yes, if it's `static` (lesson 6).
- `c1.speed` vs `Car.speed`: the first is per-object state; the second (if it exists) is class-level.
- In Python, everything is an object — even classes themselves (`type(Car)` is `type`).

**Takeaway:** A class is the blueprint, an object is the instance; attributes hold per-object data, methods define per-object behaviour.""",
                "difficulty_min": 1,
                "difficulty_max": 5,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your Wipro interviewer asks: 'Explain classes versus objects the way you'd explain it to a fresher on day one.' Which one-liner do you use?",
                        "choices": [
                            "A class is an object that has been compiled",
                            "A class is a blueprint; an object is an instance created from it",
                            "An object is a blueprint; a class is an instance of it",
                            "Classes and objects are two names for the exact same thing",
                        ],
                        "answer_index": 1,
                        "difficulty": 1,
                        "explanation": "The class defines the structure (attributes and methods) once; each object is a separate instance holding its own data. This blueprint-vs-house analogy is the expected one-line interview answer.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Infosys interviewer writes `c1 = Car(\"Tata\")` and `c2 = Car(\"Honda\")`, then asks: 'Do these two share memory for their attributes?' What's the right call?",
                        "choices": [
                            "Only c1 is a real object; c2 is a reference to c1",
                            "They share the same memory for all attributes",
                            "They are two independent objects of class Car with their own attribute values",
                            "c2 overwrites c1 because they share a class",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "Each instantiation creates a fresh object with its own attribute storage. Changing c1.speed never affects c2.speed — independent state per object is the whole point of instantiation.",
                        "company_tags": ["infosys", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Zoho interviewer points at `def accelerate(self, by=10)` and asks: 'What exactly is `self` doing there — and what breaks if you drop it?'",
                        "choices": [
                            "It is optional syntax sugar with no runtime meaning",
                            "It is a keyword that creates a new class",
                            "It refers to the class itself, shared across all objects",
                            "It refers to the specific object the method was called on, giving access to its attributes",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "self is the reference to the calling instance, so self.speed reads and writes that particular object's data. It is passed implicitly: c1.accelerate(10) becomes Car.accelerate(c1, 10) under the hood.",
                        "company_tags": ["zoho", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your interviewer asks: 'Java forces `new Car(...)`, but Python just calls `Car(...)`. Is Python skipping a step, or just hiding it?'",
                        "choices": [
                            "There is no difference; both keywords do nothing",
                            "Java objects must be explicitly allocated on the heap; Python's call syntax hides the same allocation",
                            "Python does not allocate memory for objects",
                            "Java's new makes the object static",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "In Java, new explicitly allocates the object and invokes the constructor. Python's Car(...) looks like a plain call but internally allocates the instance and runs __init__ — the allocation is just hidden behind call syntax.",
                        "company_tags": ["accenture", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Flipkart interviewer slides this snippet across the table:\n```python\nclass Counter:\n    count = 0\n    def __init__(self):\n        Counter.count += 1\na = Counter(); b = Counter()\nprint(a.count, b.count, Counter.count)\n```\n'Tell me the output,' he says, 'and then the follow-up every interviewer asks: WHY?'",
                        "choices": [
                            "1 1 2",
                            "1 2 2",
                            "2 2 2",
                            "0 0 0",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "count is a class attribute shared by all instances. Each __init__ increments the single shared Counter.count, so after two objects it is 2 — and every access (a.count, b.count, Counter.count) reads that same shared value: 2 2 2.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your interviewer leans in: 'If a class is just a blueprint, where does it actually live at runtime?' What's the most accurate answer?",
                        "choices": [
                            "The class definition is loaded once (in Python, the class itself is an object of type 'type'; in Java, a Class object in the method area)",
                            "A copy of the class is stored inside every object",
                            "Classes live on the stack next to local variables",
                            "Nowhere — classes disappear after compilation",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "The class definition is loaded exactly once at runtime — in Python the class is itself an object (an instance of type), in Java it is represented by a java.lang.Class object. Objects hold their own data plus a reference to this shared definition, which is why methods are not duplicated per object.",
                        "company_tags": ["microsoft", "meta"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'You create 1,000 Employee objects from one class. How many copies of the `calculate_salary()` method exist in memory — and what does each object actually store?'",
                        "choices": [
                            "1,000 copies — every object carries its own full copy of every method",
                            "One copy lives on the class; each object stores only its own attribute values plus a link back to the class",
                            "Zero — methods are inlined into the calling code at instantiation time",
                            "Methods are copied per object, while attributes are shared across all objects",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Methods are stored once on the class object; each instance holds only its own data plus a reference to the class (in Python, `obj.__class__`). That's why a thousand objects don't cost a thousand copies of the method code — and it's the real reason the blueprint analogy matters for memory. Interviewers ask this to check you understand the object model, not just the slogan.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Zoho interviewer writes this on the board:\n```python\nclass Team:\n    def __init__(self, name):\n        self.name = name\nt1 = Team(\"Alpha\")\nt2 = t1\nt2.name = \"Beta\"\nprint(t1.name)\n```\n'Tell me the output,' she says, 'and what it proves about variables versus objects.'",
                        "choices": [
                            "\"Alpha\" — t2 is an independent copy of t1",
                            "\"Beta\" — `t2 = t1` copies the reference, so both names point to the same object",
                            "\"Alpha\" — assignment always creates a brand-new object",
                            "AttributeError — t2 was never instantiated with Team(...)",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "`t2 = t1` creates no object at all — it copies the reference, so both variables name the same Team instance, and the rename through t2 is visible through t1. Variables hold references, not objects. This aliasing trap is how interviewers separate people who memorised 'class = blueprint' from people who actually get the object model.",
                        "company_tags": ["zoho", "wipro"],
                    },
                ],
            },
            {
                "slug": "oop-constructors",
                "title": "Constructors & Destructors",
                "theory_md": """## Constructors & Destructors

A **constructor** runs automatically when an object is created. Its job: put
the newborn object into a valid initial state — no half-built objects.

### Python: `__init__`

```python
class Student:
    def __init__(self, name, marks=0):   # runs on Student(...)
        self.name = name
        self.marks = marks

s = Student("Asha")        # __init__ runs automatically
print(s.marks)             # 0 — default arg fills in
```

### Java: constructors by overloading

Java has no default arguments, so you write **multiple constructors**
(overloading) and chain them with `this(...)`:

```java
class Student {
    String name;
    int marks;
    Student(String name) {          // constructor 1
        this(name, 0);              // chains to constructor 2
    }
    Student(String name, int marks) {  // constructor 2
        this.name = name;
        this.marks = marks;
    }
}
```

### Destructors

| Language | Destructor | Notes |
|---|---|---|
| C++ | `~Student()` | Runs deterministically at scope end / `delete` |
| Python | `__del__` | Runs when garbage-collected — timing NOT guaranteed |
| Java | `finalize()` (deprecated) | Never rely on it; use try-with-resources instead |

```python
class TempFile:
    def __del__(self):
        print("cleaning up...")   # may run late, or never before exit
```

### Constructor chaining order

When a subclass object is created, the **parent constructor runs first**, then
the child (full details in the `super()` lesson).

### Interview traps

- Python has exactly ONE `__init__` — "overloading" it by defining it twice just replaces the first.
- A constructor has no return type — not even `void` in Java/C++.
- Relying on `__del__`/`finalize` for critical cleanup is a classic bug; use context managers / try-with-resources.

**Takeaway:** Constructors initialise objects at birth (`__init__` in Python, overloaded constructors in Java); destructors clean up, but only C++ guarantees when.""",
                "difficulty_min": 2,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer challenges you: 'Why do we even need constructors? I can just set attributes right after creating the object.' How do you answer?",
                        "choices": [
                            "To make all attributes public",
                            "To destroy objects when they are no longer needed",
                            "To initialise an object into a valid state automatically at creation time",
                            "To copy one class definition into another",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "A constructor runs the moment an object is created, setting up its attributes so the object starts life in a valid state. Destruction is the destructor's job, and neither has anything to do with copying classes or changing visibility.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Zoho interviewer shows you a Python class with `__init__` defined twice with different parameters. 'I create an object now,' she says. 'Walk me through what happens.'",
                        "choices": [
                            "Both run in sequence when an object is created",
                            "Python raises a compile-time error",
                            "Python overloads them and picks the right one per call",
                            "The second definition replaces the first; only it exists",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "Python does not support method overloading — redefining __init__ simply rebinds the name, so the first version is lost. The Pythonic alternative is one __init__ with default arguments. This trips up everyone coming from Java.",
                        "company_tags": ["wipro", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Cognizant interviewer points at `this(name, 0)` sitting inside a Java constructor and asks: 'What is this line actually doing?'",
                        "choices": [
                            "It creates a second, unrelated object",
                            "It calls another constructor of the same class — constructor chaining",
                            "It calls the parent class constructor",
                            "It sets a static field named this",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "this(...) invokes a sibling constructor of the same class, letting one constructor delegate to another to avoid duplicated initialisation logic. Calling the parent constructor uses super(...), not this(...).",
                        "company_tags": ["accenture", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer asks: 'I found file-closing logic inside a teammate's `__del__` method during code review. What do you flag — and what's the safe alternative?'",
                        "choices": [
                            "It makes the program run twice as fast, wasting CPU",
                            "__del__ does not exist in Python",
                            "The garbage collector's timing is not guaranteed, so cleanup may happen late or never",
                            "__del__ cannot access the object's attributes",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "__del__ runs only when the object is garbage-collected, which in CPython depends on reference counting and in other interpreters is entirely unpredictable. Critical cleanup belongs in context managers (with blocks), which guarantee timing.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your interviewer plays spot-the-lie: 'One of these four statements about constructors is false. Which one — and why is it a classic trap?'",
                        "choices": [
                            "In Java, a constructor may declare any return type including void",
                            "Python's __init__ is the constructor-equivalent, invoked by calling the class",
                            "A subclass object's creation triggers its parent constructor first",
                            "A constructor runs automatically when an object is created",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "Constructors have no return type at all — not even void. Writing `void Student(...)` in Java silently turns it into an ordinary method that never runs at construction. The other three statements are all true.",
                        "company_tags": ["microsoft", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Uber interviewer asks: 'A C++ object is created on the stack inside a function. When exactly does its destructor run — and why should a Java developer care about the difference?'",
                        "choices": [
                            "Immediately after the constructor finishes",
                            "Deterministically, when execution leaves the scope — unlike Java/Python cleanup",
                            "Only if the programmer calls delete explicitly",
                            "When the garbage collector eventually reclaims it",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "C++ stack objects are destroyed deterministically at scope exit — this RAII guarantee is why C++ can manage resources (locks, files, memory) via destructors. Java and Python have no such guarantee, which is exactly why their finalizers are unreliable.",
                        "company_tags": ["meta", "uber"],
                    },
                ],
            },
            {
                "slug": "oop-encapsulation",
                "title": "Encapsulation & Access Modifiers",
                "theory_md": """## Encapsulation & Access Modifiers

**Encapsulation** = bundling data with the methods that use it **and**
restricting direct access to the internals, so the object can never be left
in an invalid state.

### Java / C++: real access modifiers

```java
class BankAccount {
    private double balance;          // only this class can touch it
    protected String branchCode;     // this class + subclasses (+ package)
    public String owner;             // anyone

    public void deposit(double amt) {
        if (amt > 0) balance += amt; // validation lives in ONE place
    }
    public double getBalance() { return balance; }  // getter
}
```

### Python: conventions, not walls

Python has no `private` keyword — privacy is by **naming convention**:

```python
class BankAccount:
    def __init__(self):
        self.balance = 0        # public — touch freely
        self._branch = "DEL01"  # protected by CONVENTION — "don't touch"
        self.__pin = 1234       # private-ish: name-mangled to _BankAccount__pin

a = BankAccount()
print(a._BankAccount__pin)  # 1234 — mangling is obfuscation, not security!
```

### Getters, setters, and properties

```python
class Temp:
    def __init__(self):
        self._celsius = 0
    @property                       # temp.celsius looks like an attribute...
    def celsius(self):
        return self._celsius
    @celsius.setter                  # ...but runs validation code
    def celsius(self, v):
        if v < -273.15: raise ValueError("below absolute zero!")
        self._celsius = v
```

### Interview traps

- Python's `__x` is **name mangling**, not true privacy — it renames to `_Class__x` to avoid subclass collisions, and can still be accessed.
- Getters/setters exist so validation and future changes stay in one place — never scatter `if amt > 0` across your codebase.
- "Encapsulation vs abstraction?" — saved for the next lesson; know both answers.

**Takeaway:** Encapsulation guards an object's state behind methods; Java enforces it with keywords, Python with conventions plus properties.""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'Everyone recites the encapsulation definition. Tell me what it's actually protecting in a real codebase.'",
                        "choices": [
                            "The program from running out of memory",
                            "Private methods from ever being tested",
                            "The source code from being read by other developers",
                            "An object's internal state from invalid direct modification, by funnelling access through methods",
                        ],
                        "answer_index": 3,
                        "difficulty": 2,
                        "explanation": "Encapsulation keeps an object's data bundled with its methods and restricts raw access, so invariants (like balance never going negative) are enforced in one place. It is about valid state, not about hiding source code or memory.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Rapid-fire at Wipro: 'Which Java modifier locks a member down to its own class — nothing else can touch it?'",
                        "choices": [
                            "protected",
                            "private",
                            "default (package-private)",
                            "public",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "private restricts access to the declaring class alone. protected additionally opens it to subclasses, default opens it to the whole package, and public opens it to everyone. This ordering is a favourite rapid-fire question.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Zoho interviewer writes `self.__pin` inside a class and asks: 'Is this attribute now truly private? Prove your answer.'",
                        "choices": [
                            "Converts it into a static class attribute",
                            "Makes it truly inaccessible from outside the class",
                            "Name-mangles it to `_BankAccount__pin` to avoid accidental clashes, mainly in subclasses",
                            "Deletes it when the object is pickled",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "Double-underscore prefixing triggers name mangling, renaming the attribute to _BankAccount__pin. Its real purpose is preventing accidental name collisions in subclasses — it is deliberately still reachable, so it is not security.",
                        "company_tags": ["zoho", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You're reviewing a Razorpay PR where `account.balance` is a public field that any caller sets directly. The author says 'it works fine.' What do you flag?",
                        "choices": [
                            "All validation and business rules live in one place, so the balance can never become invalid",
                            "Direct assignment is a syntax error in Java",
                            "It reduces the number of lines of code",
                            "Methods run faster than attribute assignment",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "A method centralises the rules — e.g. rejecting negative amounts — so every state change is validated identically. With public fields, each caller must remember the rules, and one forgotten check corrupts the object. It usually adds lines, not fewer.",
                        "company_tags": ["amazon", "razorpay"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Swiggy interviewer asks: 'Why would a Python developer reach for `@property` instead of just leaving the attribute public?'",
                        "choices": [
                            "Properties use less memory than attributes",
                            "Attribute-style access (`obj.celsius`) can run getter/setter logic like validation, while keeping the simple syntax",
                            "Properties are inherited but attributes are not",
                            "Properties prevent the attribute from ever being read",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "@property lets you start with a simple public attribute and later add validation or computed logic behind the same `obj.x` syntax — callers never change their code. That painless upgrade path is why Python code often skips Java-style getX/setX boilerplate.",
                        "company_tags": ["google", "swiggy"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer asks: 'A parent class and its child both define `__token`. Does the child's silently destroy the parent's? Walk me through the mechanics.'",
                        "choices": [
                            "The parent's __token is deleted",
                            "The subclass attribute silently overwrites the parent's",
                            "Name mangling gives them different real names (`_Parent__token` vs `_Child__token`), so both coexist safely",
                            "Python raises an AttributeError at class definition time",
                        ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "This is the actual design purpose of name mangling: each class's __token is rewritten with its own class name, so parent and child attributes never collide. Far from being 'private', the mechanism exists to make inheritance hierarchies safe from accidental overrides.",
                        "company_tags": ["microsoft", "meta"],
                    },
                ],
            },
            {
                "slug": "oop-abstraction-basics",
                "title": "Abstraction: Hiding Complexity",
                "theory_md": """## Abstraction: Hiding Complexity

**Abstraction** means exposing *what* something does while hiding *how* it
does it. You press a car's accelerator without understanding fuel injection —
the pedal is the abstraction.

### Encapsulation vs Abstraction — the classic interview question

| | Encapsulation | Abstraction |
|---|---|---|
| Focus | **How** data is protected | **What** is exposed |
| Mechanism | Access modifiers, private fields | Interfaces, abstract classes, simple APIs |
| Solves | Invalid object state | Overwhelming complexity |
| Example | `private balance` + `deposit()` | `car.drive()` hides the engine |

> One-liner for interviews: *encapsulation hides the data, abstraction hides
> the implementation.*

### Abstraction in code

```python
from abc import ABC, abstractmethod

class Payment(ABC):                 # the ABSTRACTION: "pay" is all you see
    @abstractmethod
    def pay(self, amount): ...

class UpiPayment(Payment):          # the hidden HOW
    def pay(self, amount):
        print(f"UPI handshake... paid {amount}")

def checkout(p: Payment, amount):   # caller only knows the abstraction
    p.pay(amount)

checkout(UpiPayment(), 500)
```

```java
abstract class Payment {
    abstract void pay(double amount);   // what — no body
}
class CardPayment extends Payment {
    void pay(double amount) {           // how — hidden inside
        System.out.println("Charging card...");
    }
}
```

### Real-world abstractions you use daily

- `print()` — you don't manage output buffers.
- A TV remote — buttons abstract away infrared protocols.
- Database drivers — `cursor.execute()` hides network + SQL parsing.

### Interview traps

- Saying "abstraction = private keyword" — that's encapsulation. Abstraction is about the *simplified view*.
- Abstract classes (lesson 11) are just one *mechanism* for abstraction; good API design is another.

**Takeaway:** Abstraction shows the what and hides the how; encapsulation hides the data — know the difference cold.""",
                "difficulty_min": 2,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'Give me abstraction in one line — and make it something a non-programmer would understand.'",
                        "choices": [
                            "Deleting unnecessary code from a program",
                            "Exposing what an operation does while hiding how it is implemented",
                            "Making every field of a class public",
                            "Copying code from a parent class",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Abstraction gives users a simplified view — the what — while the messy implementation details stay hidden. The car pedal and the print() function are everyday examples of this principle.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "The classic Wipro trap: 'Aren't encapsulation and abstraction basically the same thing?' How do you shut that down in two sentences?",
                        "choices": [
                            "Encapsulation is compile-time, abstraction is runtime",
                            "Encapsulation is for Java, abstraction is for Python",
                            "Encapsulation hides data to protect state; abstraction hides implementation to reduce complexity",
                            "They are two names for the exact same concept",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Encapsulation guards *data* (private fields + methods), while abstraction simplifies the *view* (interfaces, clean APIs). Interviewers ask this constantly because beginners merge the two — the one-liner 'encapsulation hides data, abstraction hides implementation' scores full marks.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your interviewer shows you the lesson's `checkout()` function and asks: 'What does this function actually depend on — the abstraction or the implementation?'",
                        "choices": [
                            "Only the Payment abstraction — it works with any Payment subclass",
                            "The database schema used by payments",
                            "Nothing; it is a standalone function",
                            "The concrete UpiPayment implementation details",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "checkout() takes a Payment and calls pay() — it never mentions UpiPayment. That is abstraction paying off: you can add CardPayment or WalletPayment later without touching checkout at all.",
                        "company_tags": ["cognizant", "phonepe"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer gives you four code sketches and asks: 'Exactly one of these is abstraction rather than encapsulation. Which one?'",
                        "choices": [
                            "Validating amounts inside `deposit()`",
                            "A `sort()` method whose caller doesn't know whether it uses quicksort or mergesort",
                            "Name-mangling `__pin` in Python",
                            "Declaring `balance` as private in a BankAccount class",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "sort() shows the what (sorted data) while hiding the how (the algorithm) — pure abstraction. The other options are all about guarding internal state, which is encapsulation.",
                        "company_tags": ["amazon", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Flipkart interviewer asks: 'What's the real cost of having TOO LITTLE abstraction in a large codebase?'",
                        "choices": [
                            "It prevents the use of inheritance",
                            "It makes compilation slower",
                            "Callers become coupled to implementation details, so any internal change ripples across the codebase",
                            "It increases memory usage",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "Without abstraction, every caller depends on how things work internally. Change the internals and you must hunt down and fix every caller — the exact maintenance nightmare abstraction exists to prevent.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer pushes back: 'Show me abstraction WITHOUT using abstract classes or interfaces — or admit it's impossible.' What's your answer?",
                        "choices": [
                            "Only private fields count as abstraction",
                            "Abstraction without abstract classes is just encapsulation",
                            "It is impossible — abstraction requires abstract classes",
                            "Any well-designed API is abstraction: e.g. a `send_email(to, body)` function hides SMTP handshakes, retries, and encoding from its caller",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "Abstract classes are one mechanism, not the concept itself. Any clean API that hides complexity — send_email, print, database drivers — is abstraction. This answer shows you understand the principle rather than just the keyword.",
                        "company_tags": ["microsoft", "meta"],
                    },
                ],
            },
            {
                "slug": "oop-static-members",
                "title": "static, this/self and Class Members",
                "theory_md": """## static, this/self and Class Members

Not everything belongs to one object. Some data and behaviour belong to the
**class itself** — that's what `static` is for.

### Instance vs class (static) members

```python
class Employee:
    company = "Acme"          # class attribute — ONE copy shared by all
    def __init__(self, name):
        self.name = name      # instance attribute — per object

    @staticmethod
    def policy():             # static method — no self, no instance needed
        return "9-5, hybrid"

    @classmethod
    def headcount(cls):       # class method — gets the CLASS, not instance
        return cls.company

print(Employee.policy())      # works WITHOUT creating an object
```

```java
class Employee {
    static String company = "Acme";   // one copy shared by all objects
    String name;                      // per-object
    static String policy() {          // callable as Employee.policy()
        return "9-5, hybrid";
    }
}
```

### `this` (Java) vs `self` (Python)

| | Java `this` | Python `self` |
|---|---|---|
| What | Reference to current object | Reference to current object |
| Keyword? | Reserved keyword | Just a convention (but never rename it) |
| In static methods? | **Not available** | **Not available** |

### When to use static

- Utility functions with no state: `Math.sqrt()`, `Employee.policy()`.
- Counters shared across instances: `Employee.total_created += 1`.
- Constants: `static final double PI = 3.14159;`.

### Interview traps

- A `static` method **cannot** use `this`/`self` or touch instance fields — there is no object.
- In Python, `@staticmethod` vs `@classmethod`: static gets *nothing*, classmethod gets the *class* (great for alternate constructors).
- Static fields are shared mutable state — a classic source of threading bugs.

**Takeaway:** static members belong to the class, not any object; static methods can't touch instance state because there's no `this`/`self`.""",
                "difficulty_min": 3,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'When would you ever call a method without creating an object — and what kind of method makes that possible?'",
                        "choices": [
                            "Instance methods cannot be called at all",
                            "Static methods run faster",
                            "A static method belongs to the class and can run without any object; an instance method needs an object",
                            "Static methods cannot have parameters",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Static methods are class-level: Employee.policy() works with no object created. Instance methods operate on a specific object's state via self/this, so calling one requires an instance.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Accenture interviewer asks: 'Why does a static method explode if it tries to touch `this.name`? What's the fundamental reason?'",
                        "choices": [
                            "There is no object instance in context, so this/self doesn't exist there",
                            "The compiler deletes instance fields in static contexts",
                            "Static methods can only access other static methods' variables",
                            "Static methods are private by default",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "this/self refers to the calling object — but a static method is called on the class with no object. With no instance in context, there is nothing for this/self to point to, so instance fields are unreachable.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Zoho interviewer asks: 'Python gives you both `@staticmethod` and `@classmethod`. Give me a real situation where you'd pick one over the other.'",
                        "choices": [
                            "They are identical; classmethod is the old name",
                            "@staticmethod receives no implicit argument; @classmethod receives the class (cls) as its first argument",
                            "@classmethod cannot be called without an instance",
                            "@staticmethod can access instance attributes",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "A staticmethod gets nothing implicit — it's a plain function living in the class namespace. A classmethod gets cls, the class itself, which makes it ideal for alternate constructors like Employee.from_csv(row) that must work with subclasses too.",
                        "company_tags": ["zoho", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer slides this snippet over:\n```python\nclass A:\n    x = []\n    def __init__(self):\n        self.x.append(1)\na, b = A(), A()\nprint(len(a.x), len(b.x), len(A.x))\n```\n'Predict the output,' she says, 'then name the one-word concept behind it.'",
                        "choices": [
                            "1 1 0",
                            "1 2 2",
                            "2 2 2",
                            "0 0 2",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "x is a class attribute — one list shared by all instances. Each __init__ appends to that same list via self.x (lookup falls back to the class), so after two objects the shared list has 2 items, visible through a, b, and A alike: 2 2 2. This mutable-class-attribute gotcha is an interview favourite.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Flipkart interviewer asks: 'Give me a case where a static variable is genuinely the right tool — not just a lazy global in disguise.'",
                        "choices": [
                            "For temporary values inside a single method call",
                            "Static variables should never be used",
                            "For data that differs per object, like a user's name",
                            "For data shared by all instances, like a company name or an instance counter",
                        ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "Static (class-level) storage is right when there is logically one value for the whole class: constants, configuration, or counters tracking all instances. Per-object data must stay an instance attribute, or every object would overwrite everyone else's values.",
                        "company_tags": ["flipkart", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer describes a production incident: a Java service has a `static int count` incremented in the constructor, with 100 threads creating objects. 'What breaks under load?' she asks.",
                        "choices": [
                            "No risk — static fields are thread-safe by default",
                            "Race condition: increments can be lost because `count++` is not atomic",
                            "The program will not compile",
                            "Each thread gets its own copy of count",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Static fields are shared mutable state, and count++ is a read-modify-write sequence, not one atomic step. Two threads can read the same value and both write back the same increment, losing counts. Fixes include AtomicInteger or synchronization — interviewers love this follow-up.",
                        "company_tags": ["meta", "uber"],
                    },
                ],
            },
        ],
    },
    {
        "slug": "oop-inheritance",
        "name": "Inheritance",
        "description": (
            "Master IS-A reuse hierarchies: inheritance types across Java, "
            "Python and C++, method overriding, super(), abstract classes vs "
            "interfaces, and the diamond problem with Python's MRO."
        ),
        "lessons": [
            {
                "slug": "oop-inheritance-intro",
                "title": "Inheritance: The IS-A Relationship",
                "theory_md": """## Inheritance: The IS-A Relationship

**Inheritance** lets a new class (child/derived/subclass) reuse the fields and
methods of an existing class (parent/base/superclass). The test: **IS-A**.
A `Dog` IS-A `Animal` — so inheritance fits. A `Car` HAS-A `Engine` — that's
composition, not inheritance.

### Basic syntax

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def eat(self):
        return f"{self.name} is eating"

class Dog(Animal):          # Dog inherits from Animal
    def bark(self):
        return "Woof!"

d = Dog("Rex")
print(d.eat())              # reused from Animal — no rewrite needed
print(d.bark())
```

```java
class Dog extends Animal {  // 'extends' = inherits
    String bark() { return "Woof!"; }
}
```

### What the child gets

- All **public/protected** fields and methods of the parent.
- It can **add** new members and **override** inherited methods.
- In Python/Java the child constructor should initialise the parent part (see the `super()` lesson).

### IS-A vs HAS-A — say it in interviews

| Relationship | Meaning | Example | Mechanism |
|---|---|---|---|
| IS-A | "is a kind of" | Dog is an Animal | Inheritance |
| HAS-A | "has a / uses a" | Car has an Engine | Composition (field) |

> Favour composition over inheritance when reuse doesn't pass the IS-A test —
> interviewers award bonus points for this line.

### Interview traps

- Inheriting just to reuse code (without IS-A) creates fragile hierarchies — the classic misuse.
- The child IS-A parent, so a `Dog` can be used wherever an `Animal` is expected (Liskov substitution, the basis of polymorphism).

**Takeaway:** Inheritance reuses code through IS-A hierarchies; if it's really HAS-A, use composition instead.""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer opens with: 'When a class inherits from another, what does the child actually walk away with?'",
                        "choices": [
                            "Reuse the parent's fields and methods, and add or override its own",
                            "Access private fields of any class in the program",
                            "Change the parent class's code automatically",
                            "Delete the parent class's methods",
                        ],
                        "answer_index": 0,
                        "difficulty": 1,
                        "explanation": "Inheritance is code reuse: the child gets the parent's accessible members for free, can add new ones, and can override inherited behaviour. It never modifies the parent class itself.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Accenture interviewer lists four designs — Car/Engine, Dog/Animal, Student/Classroom, Book/Library — and asks: 'Exactly one of these deserves inheritance. Which one, and what's your test?'",
                        "choices": [
                            "Car inherits from Engine (a car is an engine)",
                            "Dog inherits from Animal (a dog is an animal)",
                            "Student inherits from Classroom (a student is a classroom)",
                            "Book inherits from Library (a book is a library)",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Inheritance must pass the IS-A test: a Dog IS-A Animal. The others are HAS-A relationships (a car HAS an engine, a library HAS books) and should use composition instead — getting this wrong is the most common design mistake beginners make.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Zoho interviewer writes `class Dog(Animal)` where Dog defines no `eat()`, then calls `d.eat()`. 'Narrate what Python does, step by step,' she says.",
                        "choices": [
                            "The program crashes at class definition time",
                            "It raises an AttributeError because eat is not in Dog",
                            "Python looks up eat() in Animal — inherited methods are found via the parent",
                            "It calls eat() on a new Animal instance",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Method lookup walks up the inheritance chain: if Dog doesn't define eat, Python (and Java) find Animal's version. That's the reuse payoff — Dog gets eat() without a single line of extra code.",
                        "company_tags": ["cognizant", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You're reviewing a Flipkart PR and spot `class Car(Engine)`. The author says 'it reuses the engine code nicely.' What do you flag in the review?",
                        "choices": [
                            "Copy the Engine code into Car — duplication is safest",
                            "Make Engine a subclass of Car",
                            "class Car(Engine) — inheritance is always simpler",
                            "Car holds an Engine field (composition) — because a car HAS-A engine, and composition avoids a fragile IS-A lie",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "A car is not a kind of engine, so inheritance fails the IS-A test and would expose engine internals as car behaviour. Composition (a field) models HAS-A honestly and keeps both classes independently changeable — 'favour composition over inheritance' is the expected expert answer.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Google interviewer asks: 'Why do experienced developers get nervous when an inheritance hierarchy goes six levels deep?'",
                        "choices": [
                            "They use too much memory per object",
                            "The fragile base class problem: a change in a distant parent can silently break many subclasses",
                            "They cannot be compiled",
                            "Subclasses lose access to parent methods",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Deep hierarchies couple every level to the ones above. A seemingly safe change in a grandparent class can alter behaviour in dozens of subclasses that depend on the old semantics — the fragile base class problem, and why shallow hierarchies plus composition are preferred.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Netflix interviewer asks: 'Why is it safe to hand a `Dog` object to a function that was written to expect an `Animal`?'",
                        "choices": [
                            "It can't — this always raises a type error",
                            "Because Python automatically converts Dog to Animal",
                            "Because of substitutability: a subclass object IS-A parent object, so it honours the parent's contract",
                            "Because Dog and Animal share the same memory layout by coincidence",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "This is the Liskov Substitution Principle: anywhere a parent is expected, a child must work, since the child carries all the parent's behaviour. It's the foundation that makes polymorphism safe — a function written against Animal automatically works for Dog, Cat, and future subclasses.",
                        "company_tags": ["meta", "netflix"],
                    },
                ],
            },
            {
                "slug": "oop-inheritance-types",
                "title": "Types of Inheritance",
                "theory_md": """## Types of Inheritance

Inheritance comes in five flavours. Java famously bans one of them — know
which, and why.

### The five types

```python
class A: pass

class B(A): pass            # 1. SINGLE: B -> A

class C(B): pass            # 2. MULTILEVEL: C -> B -> A

class D(A): pass            # 3. HIERARCHICAL: B and D both -> A
class E(A): pass

class F(B, D): pass         # 4. MULTIPLE: F -> B, D (Python: yes! Java: no)

# 5. HYBRID: any mix of the above, e.g. multilevel + multiple
```

The same ideas in Java (`extends` for classes, `implements` for interfaces):

```java
class B extends A {}            // single
class C extends B {}            // multilevel
interface Flyable { void fly(); }
interface Swimmable { void swim(); }
class Duck extends Bird implements Flyable, Swimmable {  // multiple interfaces: OK
    public void fly() { System.out.println("Flap!"); }
    public void swim() { System.out.println("Paddle!"); }
}
// class F extends B, D {}  -- ILLEGAL: multiple class inheritance banned
```

### Language support table — memorise this

| Type | Java (classes) | Python | C++ |
|---|---|---|---|
| Single | ✅ `extends` | ✅ | ✅ |
| Multilevel | ✅ | ✅ | ✅ |
| Hierarchical | ✅ | ✅ | ✅ |
| Multiple (classes) | ❌ banned | ✅ | ✅ |
| Multiple (interfaces) | ✅ | n/a | n/a |

Java bans multiple inheritance **of classes** to dodge the diamond problem
(next module's last lesson) — but allows multiple **interfaces**.

### Quick visual

```
Single:        B → A
Multilevel:    C → B → A
Hierarchical:  B → A ← D        (one parent, many children)
Multiple:      F → B , F → D    (one child, many parents)
```

### Interview traps

- "Does Java support multiple inheritance?" — Answer: *not for classes, yes for interfaces* — the half-answer "no" loses marks.
- Hierarchical (one parent, many children) vs multiple (many parents, one child) — interviewers love swapping these.
- C++ allows multiple inheritance but forces you to resolve ambiguity with scope resolution (`B::x`).

**Takeaway:** Five types — single, multilevel, hierarchical, multiple, hybrid; Java bans multiple class inheritance, Python and C++ allow it.""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer sketches `C → B → A` on the board and asks: 'Name this inheritance type — and how is it different from hierarchical?'",
                        "choices": [
                            "Single",
                            "Multilevel",
                            "Hierarchical",
                            "Multiple",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "The chain C → B → A has more than one level, which is multilevel inheritance. Single would be just B → A, hierarchical is one parent with several children, and multiple is one child with several parents.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Cognizant interviewer says: 'B and D both extend A. Is that multiple or hierarchical — and what's your memory trick for keeping them straight?'",
                        "choices": [
                            "Hybrid",
                            "Multiple — because two classes are involved",
                            "Hierarchical — one parent, multiple children",
                            "Multilevel — because there are multiple levels",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "One parent (A) with multiple children (B, D) is hierarchical inheritance. Multiple inheritance is the reverse — one child with multiple parents. The names describe the shape, so picture the tree.",
                        "company_tags": ["wipro", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An interviewer tries to trap you: 'Java doesn't support multiple inheritance — true or false?' What's the full-marks answer?",
                        "choices": [
                            "Java supports neither multiple classes nor multiple interfaces",
                            "Java allows multiple class inheritance only for abstract classes",
                            "Java supports multiple inheritance of classes using extends with commas",
                            "Java bans multiple inheritance of classes but allows a class to implement multiple interfaces",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Java's rule is precise: one superclass via extends (avoiding the diamond problem), but many interfaces via implements. Saying just 'Java doesn't support multiple inheritance' is the classic half-answer that loses marks.",
                        "company_tags": ["accenture", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer asks: 'Why did Java's designers DELIBERATELY ban multiple inheritance of classes? What were they afraid of?'",
                        "choices": [
                            "To make programs run faster",
                            "To avoid the diamond problem — ambiguity when two parents provide the same member",
                            "Because single inheritance uses less memory",
                            "Because interfaces didn't exist yet",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "With two parents offering the same method or field, the child faces unresolvable ambiguity — the diamond problem. Java sidestepped it entirely for classes (interfaces carry no state, so they're safe). C++ kept multiple inheritance and makes the programmer resolve ambiguity manually.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Google interviewer asks: 'In C++, both parent classes define `show()`, and the child inherits from both. How do you tell the compiler which one you mean?'",
                        "choices": [
                            "The compiler picks one at random",
                            "It cannot be resolved — the program is invalid",
                            "With scope resolution, e.g. `obj.Base1::show()`",
                            "By deleting one of the parent classes",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "C++ puts the decision on the programmer: qualify the call with the parent's name (Base1::show()). An unqualified obj.show() is a compile error due to ambiguity — unlike Python, which silently follows MRO order.",
                        "company_tags": ["google", "uber"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Netflix interviewer sketches `Vehicle → Car → ElectricCar`, plus `Vehicle → Bike` on the side, and asks: 'How many inheritance types am I looking at in this one diagram?'",
                        "choices": [
                            "Multilevel (Vehicle→Car→ElectricCar) AND hierarchical (Car and Bike share Vehicle)",
                            "Multiple, because ElectricCar indirectly has two parents",
                            "Only multilevel",
                            "Only hierarchical",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "The chain Vehicle→Car→ElectricCar is multilevel, while Car and Bike both descending from Vehicle is hierarchical — one design can exhibit several types at once (that's hybrid territory). ElectricCar has one direct parent, so this is not multiple inheritance.",
                        "company_tags": ["meta", "netflix"],
                    },
                ],
            },
            {
                "slug": "oop-method-overriding",
                "title": "Method Overriding",
                "theory_md": """## Method Overriding

**Overriding** = a subclass redefines a parent method with its *own*
implementation. Same name, same signature — new behaviour. This is runtime
polymorphism in action.

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):            # OVERRIDES Animal.speak
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

for pet in [Dog(), Cat()]:
    print(pet.speak())          # Woof! Meow! — same call, different behaviour
```

```java
class Animal {
    String speak() { return "..."; }
}
class Dog extends Animal {
    @Override                    // compiler VERIFIES the signature matches
    String speak() { return "Woof!"; }
}
```

### Overriding rules (Java — interview favourite)

1. Same name + same parameters as the parent method.
2. Cannot *reduce* visibility (`public` → `private` is illegal).
3. Cannot override `final`, `static`, or `private` methods.
4. May throw *fewer/narrower* checked exceptions, never broader ones.
5. **Covariant returns**: may return a *subtype* of the parent's return type.

### Overriding vs overloading — don't mix these

| | Overriding | Overloading |
|---|---|---|
| Where | Parent ↔ child | Same class |
| Signature | Must match | Must differ (params) |
| Binding | Runtime (dynamic) | Compile-time (static) |
| Purpose | New behaviour | Convenience |

### Interview traps

- Forgetting `@Override` in Java: a typo'd signature silently becomes a *new* method (overload) instead of an override — the annotation turns this into a compile error.
- Python has no `@Override` enforcement — overriding is just redefinition, so typos fail silently.
- Overriding a `static` method in Java *hides* it; it doesn't override (no polymorphism).

**Takeaway:** Overriding redefines a parent method in the child (runtime polymorphism); always use @Override in Java so typos can't silently break it.""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'My subclass redefines a parent method with the same signature. What's the technical name for that — and when is the decision made, compile time or runtime?'",
                        "choices": [
                            "Making a method static so it runs faster",
                            "Defining two methods with the same name but different parameters in one class",
                            "A subclass redefining a parent method with the same signature but new behaviour",
                            "Deleting a parent method from the subclass",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Overriding keeps the name and signature but swaps in the child's implementation — the engine of runtime polymorphism. Same name with different parameters in one class is overloading, a completely different mechanism.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Wipro interviewer asks: 'The `@Override` annotation is optional, right? So what does it actually buy you in practice?'",
                        "choices": [
                            "It allows overriding private methods",
                            "It is required for the program to compile",
                            "It makes the method run faster",
                            "It makes the compiler verify the method truly overrides a parent method, catching signature typos at compile time",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Without @Override, a typo like speak(String s) instead of speak() silently creates a new overload while the parent method stays un-overridden — a brutal bug to find. The annotation converts that mistake into an immediate compile error.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Rapid-fire at Cognizant: 'Name one kind of Java method that can NEVER be overridden — and why the language forbids it.'",
                        "choices": [
                            "A protected instance method",
                            "A final method",
                            "An abstract method",
                            "A public instance method",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "final explicitly forbids overriding — that's its purpose. Public and protected instance methods are overridable, and abstract methods MUST be overridden (implemented) by concrete subclasses.",
                        "company_tags": ["cognizant", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer writes `public Animal reproduce()` in a parent class, then shows four possible child versions. 'Which one compiles?' she asks.",
                        "choices": [
                            "public static Animal reproduce()",
                            "private Animal reproduce()",
                            "public Dog reproduce()  // Dog extends Animal",
                            "public String reproduce()",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "This is covariant return types: the child may narrow the return to a subtype (Dog IS-A Animal). Reducing visibility to private is illegal, changing to String breaks the signature, and adding static turns it into hiding, not overriding.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Flipkart interviewer writes this on the board:\n```java\nclass A { void show() { print(\"A\"); } }\nclass B extends A { void show() { print(\"B\"); } }\nA obj = new B();\nobj.show();\n```\n'What prints?' he asks. 'And why would I care about this in a real codebase?'",
                        "choices": [
                            "B — the object's actual type decides at runtime (dynamic dispatch)",
                            "Both A and B",
                            "Compile error — show() is ambiguous",
                            "A — the reference type decides",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "Java uses dynamic dispatch for instance methods: the call resolves against the object's runtime type (B), not the reference type (A). This is runtime polymorphism — the single most important OOP runtime concept for interviews.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer asks: 'Python has no `@Override` equivalent. Is that a gap in the language — or a deliberate trade-off? Defend your answer.'",
                        "choices": [
                            "Python methods cannot be overridden at all",
                            "Python resolves methods dynamically by name lookup at call time, so redefinition in a subclass IS the override — but typos fail silently, which is the trade-off",
                            "Python checks overrides at import time automatically",
                            "Python classes cannot inherit, so the question is moot",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "Python's method calls are late-bound attribute lookups: defining speak in Dog simply shadows Animal.speak in the MRO. No declaration or annotation is needed — the flip side being that a misspelled 'override' silently becomes a new method with zero warnings, exactly the bug Java's @Override prevents.",
                        "company_tags": ["meta", "netflix"],
                    },
                ],
            },
            {
                "slug": "oop-super-keyword",
                "title": "super() and Constructor Chaining",
                "theory_md": """## super() and Constructor Chaining

`super()` is your hotline to the parent class — for calling its constructor,
reusing its methods, and controlling the **constructor chaining order**.

### The golden rule: parent constructor runs FIRST

```python
class Animal:
    def __init__(self, name):
        self.name = name
        print("Animal init")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)   # parent part built FIRST...
        self.breed = breed       # ...then the child part
        print("Dog init")

d = Dog("Rex", "Lab")
# Animal init
# Dog init
```

```java
class Dog extends Animal {
    Dog(String name, String breed) {
        super(name);        // MUST be the first statement
        this.breed = breed;
    }
}
```

### super() beyond constructors

```python
class Dog(Animal):
    def speak(self):
        base = super().speak()       # reuse parent logic, then extend it
        return base + " Woof!"
```

| Use | Python | Java |
|---|---|---|
| Parent constructor | `super().__init__(args)` | `super(args);` (first line) |
| Parent method | `super().method()` | `super.method()` |
| Parent field | `super().field` | `super.field` |

### Interview traps

- Forgetting `super().__init__()` in Python: the parent's attributes never get set → `AttributeError` later, far from the real bug.
- In Java, `super(...)` must be the **first statement** — the parent must exist before the child builds on it.
- `super()` with no args in Python 3 is enough; the old `super(Dog, self)` form is legacy.

**Takeaway:** super() reaches the parent; constructors chain parent-first, and in Java the super() call must be line one.""",
                "difficulty_min": 2,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer points at `super().__init__(name)` in a subclass and asks: 'What breaks if I delete that one line?'",
                        "choices": [
                            "Deletes the parent class",
                            "Converts the child object into a parent object",
                            "Creates a second parent object",
                            "Calls the parent class's constructor to initialise the inherited part of the object",
                        ],
                        "answer_index": 3,
                        "difficulty": 2,
                        "explanation": "super() gives access to the parent, and calling its __init__ sets up the inherited attributes (like name). Without it, the parent part of the object stays uninitialised — a classic source of AttributeErrors.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Accenture interviewer asks: 'When a subclass object is born, whose constructor runs first — and why does that order actually matter?'",
                        "choices": [
                            "Child first, then parent",
                            "Parent first, then child",
                            "Both run simultaneously",
                            "Only the child's constructor runs",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "The parent must be fully built before the child extends it — you can't decorate a house before its foundation exists. That's why Java forces super(...) to be the first statement and Python convention calls super().__init__() first.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Cognizant interviewer asks: 'Where exactly must the `super(...)` call sit inside a Java constructor — and what happens if you move it?'",
                        "choices": [
                            "Outside the constructor",
                            "Anywhere in the constructor body",
                            "As the very first statement",
                            "As the last statement",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "Java mandates super(...) (or this(...)) as the first statement, guaranteeing the parent portion of the object exists before the child touches anything. Anything before it is a compile error.",
                        "company_tags": ["cognizant", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Zoho interviewer asks: 'My override wants the parent's behaviour PLUS something extra. How do I get both without copy-pasting the parent's code?'",
                        "choices": [
                            "Call `super().speak()` (Python) / `super.speak()` (Java) to invoke the parent's implementation",
                            "Copy the parent's code into the subclass",
                            "It is impossible once overridden",
                            "Call `speak()` directly — it reaches the parent automatically",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "super() lets the override extend rather than replace: call the parent's version, then add the child's extra behaviour. Copying the code would duplicate logic and rot over time; calling speak() bare would recurse into the override itself.",
                        "company_tags": ["zoho", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Flipkart interviewer shows you a subclass `__init__` that never calls `super().__init__()` and asks: 'Bug, or perfectly fine? Convince me.'",
                        "choices": [
                            "Python calls the parent __init__ automatically",
                            "The parent's __init__ is skipped entirely — inherited attributes are never set",
                            "The program fails to compile",
                            "The parent class is deleted",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Unlike Java (which inserts an implicit super()), Python does nothing automatically — the parent __init__ simply never runs. The object is born missing its inherited attributes, and the resulting AttributeError surfaces far from the real cause.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer asks: 'In `class Dog(Animal, Pet)`, what does a bare `super()` with no arguments actually resolve to?'",
                        "choices": [
                            "The Dog class itself",
                            "Always exactly the first parent, Animal",
                            "The next class in Dog's MRO after Dog — which is usually Animal but follows the full linearisation",
                            "Both parents simultaneously",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "Zero-arg super() is MRO-aware: it means 'the next class after the current one in the Method Resolution Order'. With single inheritance that's just the parent, but with multiple inheritance it follows the C3 linearisation — which is why cooperative multiple inheritance via super() chains correctly instead of skipping classes.",
                        "company_tags": ["microsoft", "meta"],
                    },
                ],
            },
            {
                "slug": "oop-abstract-vs-interface",
                "title": "Abstract Classes vs Interfaces",
                "theory_md": """## Abstract Classes vs Interfaces

Both define a *contract* subclasses must honour — but they differ in what
else they carry. This comparison table is pure interview gold.

### The comparison table

| | Abstract class | Interface |
|---|---|---|
| Purpose | "IS-A" base with shared code | "CAN-DO" capability contract |
| State (fields) | Can hold fields | No instance state (Java: constants only) |
| Method bodies | Can have concrete methods | Java ≤7: none; Java 8+: `default`/`static` allowed |
| Constructors | Yes | No |
| Multiple | One parent only (Java) | Many interfaces allowed |
| Python equivalent | `abc.ABC` + `@abstractmethod` | No keyword — duck typing / `Protocol` |

### Code taste

```python
from abc import ABC, abstractmethod

class Shape(ABC):                       # abstract class
    def __init__(self, color):
        self.color = color              # HAS state + concrete code
    @abstractmethod
    def area(self): ...                 # ...plus a contract

class Circle(Shape):
    def __init__(self, r):
        super().__init__("red")
        self.r = r
    def area(self):
        return 3.14 * self.r ** 2

# Shape()  -> TypeError: can't instantiate abstract class
```

```java
interface Flyable {                     // pure contract
    void fly();                         // implicitly public abstract
    default void land() {               // Java 8+: default methods allowed
        System.out.println("Landing...");
    }
}
class Bird extends Animal implements Flyable {
    public void fly() { System.out.println("Flapping"); }
}
```

### When to use which

- **Abstract class**: subclasses share an IS-A bond AND common code/state (`Shape` with `color`).
- **Interface**: unrelated classes share a capability (`Bird` and `Drone` both `Flyable`).

### Interview traps

- "Can you instantiate an abstract class?" — No, in any language. That's the point.
- Java 8 `default` methods let interfaces evolve without breaking implementers — know this; it's a common follow-up.
- Python has no `interface` keyword: ABCs, duck typing, or `typing.Protocol` fill the role.

**Takeaway:** Abstract class = shared IS-A base with code; interface = CAN-DO contract — and Java lets you implement many interfaces but extend one class.""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'Can I instantiate an abstract class directly? What exactly happens if I try — in Python AND in Java?'",
                        "choices": [
                            "It creates an object with default values",
                            "It fails — abstract classes cannot be instantiated, only subclassed",
                            "It automatically picks a subclass to instantiate",
                            "It works fine in Python but not in Java",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "An abstract class is intentionally incomplete (it has abstract methods with no body), so no language lets you instantiate it directly — Python raises TypeError, Java fails compilation. You must subclass it and implement the abstract members.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Accenture interviewer asks: 'Abstract class versus interface — give me the one-line difference in INTENT, not syntax.'",
                        "choices": [
                            "Abstract classes cannot have methods",
                            "There is no difference; the names are interchangeable",
                            "Abstract class models an IS-A relationship with shared code; an interface models a CAN-DO capability across unrelated classes",
                            "Interfaces are faster than abstract classes",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "Shape as an abstract class says Circle IS-A Shape and shares colour/state; Flyable as an interface says Bird CAN fly and Drone CAN fly despite being unrelated. IS-A versus CAN-DO is the one-line distinction interviewers want.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Cognizant interviewer writes `class Duck extends Bird implements Flyable, Swimmable` and asks: 'Legal or illegal? Defend your answer.'",
                        "choices": [
                            "Legal: one superclass via extends, multiple interfaces via implements",
                            "Legal only if the interfaces have no methods",
                            "The class must be declared abstract",
                            "This is illegal — a class can only have one parent of any kind",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "Java's rule: single inheritance of classes (extends, one only) plus multiple inheritance of interfaces (implements, many). Interfaces carry no instance state, so the diamond problem doesn't apply to them.",
                        "company_tags": ["cognizant", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer asks: 'Java survived 18 years without default methods in interfaces. Why did Java 8 bother adding them?'",
                        "choices": [
                            "To make interfaces run faster",
                            "So interfaces can evolve (add methods) without breaking every existing implementing class",
                            "To allow interfaces to have constructors",
                            "To replace abstract classes entirely",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Adding a method to an interface used to break all implementers at compile time. Default methods provide a body, so old classes keep working while new ones can override — this is how the JDK itself added stream methods to Collection safely.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Swiggy interviewer asks: 'Python has no `interface` keyword. So how would you define a notifier contract that Email, SMS, and Push all honour?'",
                        "choices": [
                            "Make every notifier inherit from object only",
                            "There is no way — Python lacks interfaces entirely",
                            "Use abc.ABC with @abstractmethod, or simply rely on duck typing / typing.Protocol",
                            "Copy the Java interface syntax into Python",
                        ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "Python has no interface keyword, but ABCs with abstractmethods enforce the contract explicitly, while duck typing ('if it has send(), it works') and typing.Protocol give lighter-weight options. The choice depends on how strict the team wants the contract to be.",
                        "company_tags": ["google", "swiggy"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Netflix interviewer hands you a design scenario: 'Twenty existing classes, five unrelated ones need a new `serialize()` capability, and nobody is allowed to change superclasses. Abstract class or interface — and why?'",
                        "choices": [
                            "Copy-paste serialize() into the 5 classes",
                            "Make serialize() static in a utility class and forbid polymorphism",
                            "An abstract class Serializable that all 20 extend — restructuring their hierarchy",
                            "An interface Serializable with a default method, implemented by just the 5 classes",
                        ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "An interface is the surgical tool: the 5 unrelated classes gain the capability without disturbing their existing single superclass, and a default method can even share the common logic. An abstract class would force a hierarchy rewrite since Java allows only one superclass.",
                        "company_tags": ["meta", "netflix"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Flipkart interviewer asks: 'We're designing a payment service with Card, UPI, and Wallet flows that keep growing. When would you pick an interface over an abstract class here — and what goes where?'",
                        "choices": [
                            "Use an abstract class for everything — interfaces are legacy and cannot hold shared code",
                            "An interface defines the `pay()` contract across the unrelated gateway classes; an abstract class earns its place only if the gateways share real state or helper code",
                            "Always prefer abstract classes — interfaces cannot be used with polymorphism",
                            "Skip both — one concrete class with an if/else per payment method is simpler",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Card, UPI, and Wallet are unrelated classes sharing a CAN-DO capability, so an interface is the natural contract — each gateway implements `pay()` its own way. Reach for an abstract class only when the siblings genuinely share an IS-A bond plus common state or helper code, like a base transaction id and logging. Choosing by IS-A vs CAN-DO keeps the design open for the next payment method without rewiring the hierarchy.",
                        "company_tags": ["flipkart", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Microsoft interviewer asks: 'We have an abstract class `Report` holding shared formatting code. Now a `Dashboard` class — which already extends `Widget` — also needs to be exportable. How do you add that capability without breaking single inheritance?'",
                        "choices": [
                            "Make Dashboard extend both Widget and Report — Java and C# allow two superclasses",
                            "Define an `Exportable` interface for the export contract; Dashboard implements it while keeping Widget as its single superclass",
                            "Copy Report's formatting code into Dashboard — duplication is safest",
                            "Convert Report from an abstract class into an interface and give up the shared code",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Single inheritance blocks a second superclass, but a class may implement many interfaces — that's exactly the CAN-DO escape hatch this rule exists for. The shared formatting code stays in the abstract class for its true IS-A children, while the interface grants the export capability across unrelated hierarchies. Interviewers ask this to see whether you reach for interfaces surgically instead of rewriting hierarchies.",
                        "company_tags": ["microsoft", "zoho"],
                    },
                ],
            },
            {
                "slug": "oop-diamond-mro",
                "title": "The Diamond Problem & MRO",
                "theory_md": """## The Diamond Problem & MRO

What happens when a class inherits from **two parents that share a
grandparent**? The hierarchy looks like a diamond — and method lookup gets
ambiguous.

### The diamond

```
        A           <- defines greet()
       / \\
      B   C        <- both override greet()
       \\ /
        D           <- which greet() does D get?
```

```python
class A:
    def greet(self): return "A"
class B(A):
    def greet(self): return "B"
class C(A):
    def greet(self): return "C"
class D(B, C): pass

print(D().greet())        # "B" — but WHY B and not C?
print(D.__mro__)          # D -> B -> C -> A -> object
```

### Python's answer: MRO + C3 linearization

Python computes a **Method Resolution Order** — one unambiguous list — using
the **C3 linearization** algorithm. Lookup simply walks the list left to right
and takes the first match. Three guarantees: children before parents, parents
in declaration order (`B` before `C`), and monotonicity (a class never appears
before its own parents).

### How each language handles the diamond

| Language | Multiple class inheritance | Diamond strategy |
|---|---|---|
| Python | ✅ | C3 MRO — deterministic, first match wins |
| C++ | ✅ | Programmer resolves: `obj.B::greet()`; `virtual` inheritance shares one A |
| Java | ❌ (classes) | Banned the problem; interfaces use most-specific-default rules |

```cpp
// C++: virtual inheritance gives D ONE shared A instead of two copies
class A { public: int x; };
class B : virtual public A {};
class C : virtual public A {};
class D : public B, public C {};   // single A::x, no ambiguity
```

Java sidesteps the whole problem — one superclass, many interfaces:

```java
interface B { default void greet() { System.out.println("B"); } }
interface C { default void greet() { System.out.println("C"); } }
class D implements B, C {
    public void greet() { B.super.greet(); }  // clash resolved explicitly
}
```

### Interview traps

- "Why does Java ban multiple inheritance?" → *the diamond problem* — always pair the two answers.
- `D.__mro__` is inspectable at runtime in Python — interviewers love asking you to predict it.
- C3 can *fail* with inconsistent hierarchies (`class X(A,B)` + `class Y(B,A)` mixed) → `TypeError: Cannot create a consistent MRO`.

**Takeaway:** The diamond is the ambiguity of two parents sharing a grandparent; Python resolves it with C3 MRO, C++ with virtual inheritance, Java by banning it.""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer draws the classic diamond — D inherits from B and C, which both inherit from A — and asks: 'What's the actual problem here? Name it.'",
                        "choices": [
                            "The problem of sorting diamond-shaped data structures",
                            "A performance bug in diamond-shaped databases",
                            "Ambiguity when a class inherits from two parents that share a common ancestor offering the same member",
                            "A syntax error caused by importing two modules",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "In the D(B, C) diamond with shared grandparent A, a call like D().greet() is ambiguous if B and C both override it — which version wins? Each language answers differently, and Java's answer was to ban the situation for classes outright.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Zoho interviewer writes `class D(B, C)` where B and C both extend A, then asks: 'What's D's MRO — and whose `greet()` wins?'",
                        "choices": [
                            "D → B → C → A; B's greet wins",
                            "D → A → B → C; A's greet wins",
                            "There is no MRO; Python raises an error",
                            "D → C → B → A; C's greet wins",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "C3 linearisation orders parents as declared (B before C) while keeping children before parents, giving D → B → C → A → object. Lookup takes the first match walking left to right, so B's greet() wins.",
                        "company_tags": ["wipro", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Accenture interviewer asks: 'C++ lets you write `class B : virtual public A`. What problem does that `virtual` keyword solve in a diamond?'",
                        "choices": [
                            "It makes method calls run faster",
                            "It ensures D gets only ONE shared copy of A's members instead of two (one via B, one via C)",
                            "It bans multiple inheritance",
                            "It automatically picks which parent's method wins",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Without virtual, D contains two separate A subobjects — so d.x is ambiguous (which A's x?). Virtual inheritance collapses them into a single shared A, eliminating the data ambiguity; remaining method ambiguity is resolved with scope resolution.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Google interviewer pushes: 'If multiple inheritance is so dangerous that Java banned it, why is multiple INTERFACE inheritance perfectly safe?'",
                        "choices": [
                            "Java interfaces cannot have methods at all",
                            "Interfaces are slower, so ambiguity doesn't matter",
                            "Interfaces carry no instance state and (pre-Java-8) no implementation, so there's nothing ambiguous to inherit",
                            "The JVM secretly converts interfaces to classes",
                        ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "The diamond problem is about inheriting conflicting state and implementations. Classic interfaces are pure contracts — method signatures only — so implementing two is just promising two behaviours, with the class providing the single implementation. (Java 8 default-method clashes are resolved by most-specific-wins rules.)",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer writes this and says: 'Predict the output. Most candidates get it wrong:'\n```python\nclass A:\n    def who(self): return \"A\"\nclass B(A):\n    def who(self): return \"B\"\nclass C(A):\n    def who(self): return \"C\"\nclass D(C, B): pass\nprint(D().who())\n```",
                        "choices": [
                            "TypeError",
                            "\"A\"",
                            "\"B\"",
                            "\"C\"",
                        ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "Declaration order is C, B — so C3 gives D → C → B → A → object, and the first who() found walking that list is C's. The trick is that declaration order (D(C, B)) beats any intuition about alphabetical or 'first defined' order.",
                        "company_tags": ["meta", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Uber interviewer shows you a hierarchy that dies with 'TypeError: Cannot create a consistent MRO' and asks: 'Don't just tell me it fails — explain WHY no valid ordering exists.'",
                        "choices": [
                            "Python forbids more than two base classes",
                            "No consistent C3 linearisation exists — X demands A before B, Y demands B before A: a contradiction",
                            "Classes X and Y are undefined",
                            "Multiple inheritance requires the `virtual` keyword",
                        ],
                        "answer_index": 1,
                        "difficulty": 9,
                        "explanation": "C3 must respect every parent's local order: X's MRO needs A before B, Y's needs B before A. No single list satisfies both, so Python raises 'TypeError: Cannot create a consistent method resolution order (MRO)'. This is C3's monotonicity guarantee refusing an impossible hierarchy — a superb deep-cut interview answer.",
                        "company_tags": ["netflix", "uber"],
                    },
                ],
            },
        ],
    },
]
