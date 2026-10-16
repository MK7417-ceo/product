"""Seed content: OOP — Modules 3-4 (Polymorphism, Advanced Concepts).

ORIGINAL educational content. All Python examples are real and runnable;
Java examples follow standard Java semantics. Interview traps reflect real
interview questions asked at service and product companies.

Exports a single variable ``MODULES``: a list of 2 module dicts
(oop-polymorphism, oop-advanced), each with 6 lessons, each lesson with
exactly 6 MCQs (72 questions total).
"""

from __future__ import annotations

MODULES = [
    {
        "slug": "oop-polymorphism",
        "name": "Polymorphism",
        "description": "One interface, many forms: how the same call can behave differently across types — from compile-time overloading to runtime dynamic dispatch.",
        "lessons": [
            {
                "slug": "oop-poly-intro",
                "title": "Polymorphism: One Interface, Many Forms",
                "theory_md": """## Polymorphism: One Interface, Many Forms

**Polymorphism** comes from Greek: *poly* (many) + *morph* (form). In OOP it
means **one interface, many implementations** — the same operation behaves
differently depending on the object it acts on.

## A real-world analogy

Think of a person named Priya. To her manager she is an *employee*, to her
brother she is a *sister*, to her friend she is a *cricket buddy*. The same
person (one interface: "Priya") takes many forms depending on the context.
In code, the "context" is the **actual type of the object** behind a
reference.

## The two kinds of polymorphism

| Aspect | Compile-time (static) | Runtime (dynamic) |
|---|---|---|
| When resolved | At compile time | While the program runs |
| Main mechanism | Method overloading | Method overriding + upcasting |
| Languages | Java, C++ | Java, C++, Python |
| Speed | Slightly faster (no lookup) | Tiny lookup cost |

## A first taste in Python

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Cow:
    def speak(self):
        return "Moo!"

# One interface (speak), many forms — no inheritance needed:
for animal in (Dog(), Cat(), Cow()):
    print(animal.speak())   # Woof! / Meow! / Moo!
```

## The same idea in Java

```java
interface Shape {
    void draw();   // one interface
}

class Circle implements Shape {
    public void draw() { System.out.println("Drawing a circle"); }
}

class Square implements Shape {
    public void draw() { System.out.println("Drawing a square"); }
}

Shape s = new Circle();  // reference type: Shape
s.draw();                // actual object: Circle -> "Drawing a circle"
s = new Square();
s.draw();                // now -> "Drawing a square"
```

## Why interviewers care

Polymorphism is how frameworks achieve **extensibility**: the framework
calls `draw()` on `Shape` without knowing every shape that will ever exist.
When asked "what is polymorphism?", give the definition, the two kinds, and
one concrete example — that is the complete interview answer.

## Interview traps

- Saying "overloading is runtime polymorphism" — it is **compile-time**.
- Confusing *polymorphism* with *inheritance*: inheritance is the "is-a"
  relationship; polymorphism is the *behavioral* payoff of it.
- In Java the reference type decides what you can *call*; the object type
  decides what actually *runs*.

**Takeaway:** Polymorphism lets one interface drive many behaviors; the
compiler binds overloaded calls early, while overridden calls are bound
late, at runtime.
""",
                "difficulty_min": 1,
                "difficulty_max": 6,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer opens with: 'The word polymorphism comes from Greek — poly and morph. What does that tell you about what it means in code?'",
                        "choices": [
                            "Many forms",
                            "Single inheritance",
                            "Data hiding",
                            "Memory sharing",
                        ],
                        "answer_index": 0,
                        "difficulty": 1,
                        "explanation": "It comes from Greek 'poly' (many) and 'morph' (form). In OOP this maps directly to the idea of one interface taking many forms depending on the object.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An interviewer says: 'Explain polymorphism to me without using any code.' Which everyday situation captures it best?",
                        "choices": [
                            "A locked door that only one key can open",
                            "A person who acts as an employee at work, a sibling at home, and a friend on weekends",
                            "A photocopy that is identical to the original",
                            "A safe that stores only one type of document",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "The same person presents different behavior in different roles, just like one interface (e.g. speak()) produces different behavior for Dog, Cat, and Cow objects.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Infosys interviewer asks: 'I keep hearing static and dynamic polymorphism — how many broad kinds are there really, and what separates them?'",
                        "choices": [
                            "One: inheritance",
                            "Three: public, private, protected",
                            "Two: compile-time (static) and runtime (dynamic)",
                            "Four: one for each access modifier",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Polymorphism splits into compile-time polymorphism (method overloading, resolved by the compiler) and runtime polymorphism (method overriding, resolved while the program runs).",
                        "company_tags": ["tcs", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer asks: 'You wrote three methods all named process with different parameter lists. Which kind of polymorphism is this?'",
                        "choices": [
                            "Runtime polymorphism",
                            "Dynamic polymorphism",
                            "Late binding",
                            "Compile-time polymorphism",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "With overloading the compiler picks which version to call based on the argument list, so the binding happens at compile time — hence compile-time (static) polymorphism.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer asks: 'Give me the one-sentence essence of polymorphism — what is it really about?' Which answer nails it?",
                        "choices": [
                            "It requires every class to inherit from exactly one parent",
                            "It makes programs run faster by removing method calls",
                            "The same interface can be used with different underlying types, each supplying its own behavior",
                            "It is only possible in languages with pointers",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "That is the essence of polymorphism: code written against a general interface works with any type that implements it, and each type decides its own behavior.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Flipkart interviewer writes four snippets on the board and asks: 'Point to the one that actually demonstrates runtime polymorphism.'",
                        "choices": [
                            "Two methods named add, one taking int and one taking double",
                            "Shape s = new Circle(); s.draw(); where Circle overrides draw()",
                            "A static method called through the class name",
                            "A private helper method used inside its own class",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Here the reference type is Shape but the actual object is Circle, so the overridden draw() is chosen at runtime — the textbook shape of dynamic dispatch. Overloading (option 1) is compile-time.",
                        "company_tags": ["amazon", "google"],
                    },
                ],
            },
            {
                "slug": "oop-overloading",
                "title": "Compile-Time Polymorphism: Overloading",
                "theory_md": """## Compile-Time Polymorphism: Overloading

**Method overloading** lets a class define several methods with the **same
name but different parameter lists** (different count, types, or order).
The compiler looks at the arguments in each call and picks the matching
version — hence "compile-time" polymorphism.

## The rules (Java)

- Overloaded methods must differ in their **signature**: number, type, or
  order of parameters.
- They may also differ in return type, but **return type alone is not
  enough** — `int add(int,int)` and `double add(int,int)` will NOT compile.
- Access modifiers and thrown exceptions do not create a new overload.

```java
class Calculator {
    int add(int a, int b) { return a + b; }
    double add(double a, double b) { return a + b; }
    int add(int a, int b, int c) { return a + b + c; }
}

Calculator c = new Calculator();
c.add(2, 3);        // calls the int version
c.add(2.5, 3.1);    // calls the double version
```

## Constructor overloading

Constructors can be overloaded the same way, giving callers flexible ways
to build an object:

```java
class Student {
    String name;
    int roll;
    Student(String name) { this.name = name; }
    Student(String name, int roll) { this(name); this.roll = roll; }
}
```

## Why Python has no true overloading

In Python, defining two methods with the same name simply **replaces**
the first one — the class keeps only the last definition. Instead, Python
developers use default arguments and `*args`/`**kwargs`:

```python
class Calculator:
    def add(self, a, b=0, c=0):   # one method, flexible calls
        return a + b + c

c = Calculator()
print(c.add(2, 3))        # 5
print(c.add(2, 3, 4))     # 9
```

## Operator overloading in Python

Python *does* support operator overloading through dunder methods like `__add__`, `__eq__`, and `__len__`:

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, other):          # overloads the + operator
        return Vector(self.x + other.x, self.y + other.y)
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

print(Vector(1, 2) + Vector(3, 4))   # Vector(4, 6)
```

## Interview traps

- "Can you overload by return type alone in Java?" — **No.**
- "Does Python support method overloading?" — **Not truly**; the last
  definition wins. Mention default args and `*args` as the Pythonic
  alternative.
- Confusing overloading (same class, same name, different params) with
  overriding (subclass redefines a parent method) — interviewers test this
  constantly.

**Takeaway:** Overloading gives one name many signatures and is resolved by
the compiler; Python fakes it with flexible arguments, but it does give you
real operator overloading via dunder methods.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A TCS interviewer asks: 'My teammate said overloading is when a subclass redefines a parent method. Is he right — and what is overloading really?'",
                        "choices": [
                            "A subclass redefining a parent method",
                            "Multiple methods with the same name but different parameter lists in the same class",
                            "A method calling itself recursively",
                            "Two classes sharing one method through inheritance",
                        ],
                        "answer_index": 1,
                        "difficulty": 2,
                        "explanation": "Overloading is about one class offering several versions of the same method name, distinguished by the number, type, or order of their parameters.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer scribbles `int add(int a, int b)` and `double add(int a, int b)` and asks: 'Will this compile as overloading? Why or why not?'",
                        "choices": [
                            "Yes, the compiler uses the return type to pick",
                            "Yes, but only for primitive return types",
                            "No — the parameter list must differ",
                            "No, overloading is not allowed in Java at all",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Java identifies an overload by its signature (name + parameter types). Return type alone never distinguishes two methods, so `int add(int,int)` and `double add(int,int)` fail to compile.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An interviewer asks: 'I want users of my Student class to create objects with just a name, or with a name and roll number. What technique is this, and how does it work?'",
                        "choices": [
                            "Calling a constructor from another class",
                            "Inheriting a constructor from the parent class",
                            "Overriding the parent constructor in the child class",
                            "Defining multiple constructors with different parameter lists in the same class",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Just like methods, constructors can be overloaded so callers can create an object in several ways — e.g. Student(name) vs Student(name, roll).",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During a Flipkart Python round, the interviewer shows a class with two `def add(...)` methods and asks: 'What survives — and what does that tell you about overloading in Python?'",
                        "choices": [
                            "The later definition replaces the earlier one — only the last survives",
                            "Python keeps both and picks by argument types",
                            "Python raises a DuplicateMethodError at class creation",
                            "The two methods are merged into one",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "Python has no true overloading: a class body is just assignments, so the second `def` rebinds the name and the first method is lost. Default arguments and *args are the Pythonic substitute.",
                        "company_tags": ["zoho", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Microsoft interviewer asks: 'I want `Vector(1,2) + Vector(3,4)` to just work in my Python class. Which method do I implement?'",
                        "choices": [
                            "__plus__",
                            "__sum__",
                            "__add__",
                            "__concat__",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "__add__ is the dunder method Python calls for the + operator, so implementing it is genuine operator overloading — Vector(1,2) + Vector(3,4) works once __add__ is defined.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer shows four method pairs and asks: 'Three of these compile as legal overloading. Which one fails — and what rule does it break?'",
                        "choices": [
                            "void show(int a) and void show(String s)",
                            "int add(int a, int b) and void add(int x, int y)",
                            "void print() and void print(int a)",
                            "double area(double r) and double area(double l, double w)",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Both methods have the identical signature add(int, int) — differing only in return type, which Java does not allow for overloading. The other three pairs differ in parameter count or type, so they compile fine.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                ],
            },
            {
                "slug": "oop-overriding-runtime",
                "title": "Runtime Polymorphism: Dynamic Dispatch",
                "theory_md": """## Runtime Polymorphism: Dynamic Dispatch

**Method overriding** happens when a subclass provides its own
implementation of a method already defined in its superclass — same name,
same parameter list. Combined with **upcasting** (holding a subclass object
in a superclass reference), the JVM picks the right method **at runtime**
based on the *actual* object. This late decision is called **dynamic
dispatch**.

## The classic interview example

```java
class Animal {
    void speak() { System.out.println("Some generic sound"); }
}

class Dog extends Animal {
    @Override
    void speak() { System.out.println("Woof!"); }
}

class Cat extends Animal {
    @Override
    void speak() { System.out.println("Meow!"); }
}

public class Demo {
    public static void main(String[] args) {
        Animal a = new Dog();   // upcasting: reference Animal, object Dog
        a.speak();              // prints "Woof!" — decided at runtime
        a = new Cat();
        a.speak();              // prints "Meow!"
    }
}
```

The **reference type** (`Animal`) decides which methods you are *allowed to
call*; the **object type** (`Dog`) decides which implementation *runs*.

## The same in Python

```python
class Animal:
    def speak(self):
        return "some generic sound"

class Dog(Animal):
    def speak(self):            # overriding — no annotation needed
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

def make_it_speak(animal: Animal):
    print(animal.speak())       # works for any present or future Animal

make_it_speak(Dog())   # Woof!
make_it_speak(Cat())   # Meow!
```

## Overriding rules (Java)

- Same name **and** same parameter list (else it is overloading, not
  overriding); return type may be a **covariant** subtype.
- You **cannot reduce visibility** (`public` cannot become `protected`).
- `static`, `private`, and `final` methods cannot be overridden — and
  `@Override` makes the compiler verify you really overrode something.

## Interview traps

- Forgetting `@Override` and accidentally *overloading* (a typo in the
  parameter list creates a new method, and the parent version keeps
  running).
- Saying the *reference* type decides which method runs — it only decides
  which methods are visible; the *object* type decides at runtime.
- Claiming static methods participate — they are bound at compile time to
  the reference type (method *hiding*, not overriding).

**Takeaway:** Overriding + upcasting gives runtime polymorphism: the
compiler checks the reference, but the running object chooses the method.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A TCS interviewer asks: 'My subclass needs its own version of the parent's speak() method. What is that called — and what must stay the same for it to work?'",
                        "choices": [
                            "Defining two methods with the same name in one class",
                            "Hiding a field of the parent class",
                            "A subclass providing its own implementation of a superclass method with the same signature",
                            "Calling the parent constructor with super()",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Overriding is a subclass redefining an inherited method — same name and parameter list — so that calls on subclass objects run the new behavior.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer writes on the board:\n```java\nAnimal a = new Dog();  // Dog overrides speak()\na.speak();\n```\n'Walk me through what prints — and why.'",
                        "choices": [
                            "It fails to compile because a is declared as Animal",
                            "The Animal version, because the reference type is Animal",
                            "It throws a runtime error",
                            "The Dog version, because the actual object is a Dog",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "This is dynamic dispatch: the reference type only controls which methods are visible, while the runtime object type (Dog) selects the implementation that executes.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An interviewer points at `Animal a = new Dog();` and asks: 'This line does something called upcasting. What does that mean — and why is it always safe?'",
                        "choices": [
                            "Treating a subclass object as an instance of its superclass type",
                            "Converting a parent object into a child object",
                            "Casting an int to a double",
                            "Moving a method from child class to parent class",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "Upcasting means assigning a subclass object to a superclass reference (Animal a = new Dog()). It is always safe and is what enables writing general code that works with any subclass.",
                        "company_tags": ["accenture", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer asks: 'When I call an overridden method, at what point does the JVM decide WHICH version runs — and what information does it use?'",
                        "choices": [
                            "Never — the parent version always runs",
                            "At runtime, based on the actual type of the object",
                            "At compile time, based on the reference type",
                            "At class-loading time, fixed forever",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "That late, runtime decision is exactly what makes it 'runtime polymorphism' or dynamic dispatch — the JVM inspects the real object, not the declared reference type.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During a Meta Java round, the interviewer lists four statements about overriding and says only one is a real rule. Which is it?",
                        "choices": [
                            "An overriding method may throw any new checked exceptions it likes",
                            "A static method can override an instance method",
                            "An overriding method cannot reduce the visibility of the inherited method",
                            "An overriding method must have a different parameter list",
                        ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "Visibility can only stay the same or widen — a public method cannot become protected in a subclass, because code using the parent contract must keep working. Different parameters would make it overloading, not overriding.",
                        "company_tags": ["amazon", "meta"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer writes this snippet on the board, asks what prints, then follows up: 'And why would I care about this in real code?'\n```java\nclass A { void m() { System.out.print(1); } }\nclass B extends A { void m() { System.out.print(2); } }\nA ref = new B();\nref.m();\n```",
                        "choices": [
                            "Compile error: m() is ambiguous",
                            "1",
                            "2",
                            "12",
                        ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "B.m() overrides A.m(), and ref points to a B object, so dynamic dispatch selects B's version at runtime and prints 2. The reference type A only guarantees that m() exists.",
                        "company_tags": ["google", "netflix"],
                    },
                ],
            },
            {
                "slug": "oop-vtable",
                "title": "Under the Hood: Virtual Tables",
                "theory_md": """## Under the Hood: Virtual Tables

Dynamic dispatch feels like magic, but in C++ it is a concrete data
structure: the **virtual table (vtable)** — a favorite deep-dive topic in
product-company interviews.

## The mechanism

- Per **class** with virtual functions, the compiler builds **one vtable**:
  an array of function pointers, one slot per virtual method.
- Per **object**, one hidden pointer — the **vptr** — aims at its class's
  vtable. `p->speak()` compiles to: follow vptr, take the `speak` slot,
  jump to that address.

```cpp
class Animal {
public:
    virtual void speak() { std::cout << "generic\\n"; }
    virtual ~Animal() = default;
};
class Dog : public Animal {
public:
    void speak() override { std::cout << "Woof!\\n"; }
};
Animal* a = new Dog();
a->speak();   // vptr -> Dog's vtable -> Dog::speak => "Woof!"
delete a;     // virtual dtor runs both destructors
```

## The cost of a virtual call

A virtual call adds one **indirection** versus a direct call — negligible
in most code. The subtler cost: the compiler **cannot inline** a call
whose target is unknown until runtime, which can matter in hot loops.

## Why the destructor must be virtual

If you `delete` a derived object through a base pointer and the base
destructor is **not** virtual, only the base destructor runs — leaked
resources and undefined behavior.

```cpp
class Base { public: ~Base() {} };            // NOT virtual — dangerous!
class Derived : public Base {
    int* data = new int[100];
public:
    ~Derived() { delete[] data; }
};
delete (Base*)new Derived();   // derived dtor never runs -> leak!
```

## C++11 helpers: override and final

- `override`: a signature typo becomes a compile error instead of a silent
  new method. `final`: forbids further overriding (or inheritance, on a class).

## The same idea in Java and Python

Java hides the machinery, but the JVM keeps per-class method tables that
work exactly like vtables:

```java
Animal a = new Dog();   // reference: Animal, object: Dog
a.speak();              // JVM consults Dog's method table at runtime
```

Python goes further — it has no visible vtables because *every* method
call is dynamically dispatched, as if all methods were virtual:

```python
class Dog(Animal):
    def speak(self): return "Woof!"

print(Dog().speak())   # Woof! — resolved via the object's type at runtime
```

## Interview traps

- "Every object has its own vtable" — **no**: one vtable per *class*,
  one vptr per *object*. Forgetting the virtual destructor is the other
  classic mistake.

**Takeaway:** A vtable is a per-class jump table and the vptr is the
object's link to it — that indirection *is* dynamic dispatch, and it is
why base-class destructors must be virtual.
""",
                "difficulty_min": 5,
                "difficulty_max": 10,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "In an Amazon C++ deep-dive, the interviewer asks: 'Everyone says virtual calls are resolved at runtime. What data structure actually makes that happen — and how?'",
                        "choices": [
                            "A hash table used by std::map",
                            "A per-object copy of all member variables",
                            "A per-class table of function pointers, one entry per virtual method",
                            "A debugging symbol table generated by the linker",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "The compiler builds one vtable per class that has virtual functions; each slot holds the address of that class's implementation, which is how p->speak() finds the right function at runtime.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Microsoft interviewer asks: 'Besides its data members, what hidden extra does each object of a class with virtual functions carry — and why is one pointer enough instead of a whole table?'",
                        "choices": [
                            "A vptr — a hidden pointer to its class's vtable",
                            "Its own private copy of the vtable",
                            "A string with the class name for reflection",
                            "A counter of how many virtual calls it made",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "Each object carries just one hidden pointer (the vptr). Following it reaches the shared per-class vtable, so the per-object memory cost is a single pointer.",
                        "company_tags": ["microsoft", "meta"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Netflix interviewer asks: 'Virtual calls cost a little more than direct calls. Where exactly does the extra cost come from — the pointer chase, or something subtler?'",
                        "choices": [
                            "Because it allocates memory on the heap each time",
                            "Because it goes through an extra indirection (vptr -> vtable -> function) and is harder for the compiler to inline",
                            "Because it always triggers a system call",
                            "Because virtual functions cannot use CPU registers",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "The pointer chase itself is cheap; the meaningful cost is that the compiler cannot inline a call whose target is only known at runtime, which can matter in hot loops.",
                        "company_tags": ["google", "netflix"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer sketches a Base/Derived pair where Base's destructor is NOT virtual, then asks: 'I run `Base* p = new Derived(); delete p;`. What breaks — and why do interviewers keep asking this exact question?'",
                        "choices": [
                            "Both destructors run normally — delete always finds the right one",
                            "The program refuses to compile",
                            "Only the base destructor runs; the derived destructor never executes, leaking resources (undefined behavior)",
                            "The derived destructor runs twice",
                        ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "Without a virtual destructor, delete through a base pointer statically binds to Base::~Base, so Derived's cleanup never runs — the classic resource-leak/UB trap interviewers love.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer asks: 'I marked a virtual function final in C++11. What did I just lock down — and what happens if a derived class tries to override it anyway?'",
                        "choices": [
                            "It makes the function run faster",
                            "It prevents any further overriding of that function in derived classes",
                            "It deletes the function",
                            "It makes the function callable without an object",
                        ],
                        "answer_index": 1,
                        "difficulty": 9,
                        "explanation": "final on a virtual function locks the override chain: derived classes must inherit that implementation as-is, and attempting to override it is a compile error.",
                        "company_tags": ["meta", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Uber systems interviewer says: 'No textbook answer — walk me through `p->f()` at the machine level, pointer by pointer:'\n```cpp\nBase* p = new Derived();  // Base declares virtual void f(); Derived overrides it\np->f();\n```",
                        "choices": [
                            "The compiler hard-codes a jump to Base::f because p is a Base*",
                            "At runtime the linker patches the call site to Derived::f",
                            "A string comparison on the class name picks the method",
                            "The object's vptr leads to Derived's vtable, whose f slot points to Derived::f",
                        ],
                        "answer_index": 3,
                        "difficulty": 10,
                        "explanation": "That is dynamic dispatch made concrete: p's hidden vptr points at Derived's vtable (because the object IS a Derived), and the f slot there holds Derived::f's address.",
                        "company_tags": ["netflix", "uber"],
                    },
                ],
            },
            {
                "slug": "oop-duck-typing",
                "title": "Duck Typing in Python",
                "theory_md": """## Duck Typing in Python

**Duck typing** — *"if it walks like a duck and quacks like a duck, it is
a duck"* — means an object's **suitability is decided by the methods it
has, not its class or inheritance chain.**

## No inheritance required

Python never asks "are you a subclass of Animal?" before letting you call
`speak()`. It just calls the method and trusts the object to handle it:

```python
class Duck:
    def quack(self):
        return "Quack!"

class Person:
    def quack(self):          # unrelated class, same method name
        return "I'm imitating a duck!"

def make_it_quack(thing):
    print(thing.quack())      # works for ANY object with quack()

make_it_quack(Duck())         # Quack!
make_it_quack(Person())       # I'm imitating a duck!
```

This is polymorphism without a shared base class — behavior, not lineage.

## The language itself is built on it

`len()` works on strings, lists, tuples, dicts, and sets — five unrelated
types — because they all implement **`__len__`**. File-like objects work
with any code expecting `.read()`: real files, `io.StringIO`, test
doubles. (`typing.Protocol` formalizes this idea with a name tag.)

## EAFP vs LBYL

Python prefers **EAFP** (*Easier to Ask Forgiveness than Permission*)
over **LBYL** (*Look Before You Leap*):

```python
if hasattr(obj, "quack"):      # LBYL: check first (verbose)
    obj.quack()

try:                           # EAFP: just try it (idiomatic)
    obj.quack()
except AttributeError:
    print("that thing doesn't quack")
```

EAFP avoids the check-then-act race (the attribute could vanish between
the check and the call) and reads cleaner.

## How Java does the same job (for contrast)

Java cannot duck-type — the compiler demands a declared type — so the
same flexibility comes from interfaces:

```java
interface Quacker { String quack(); }
class Duck implements Quacker {
    public String quack() { return "Quack!"; }
}
void makeItQuack(Quacker q) { System.out.println(q.quack()); }
```

Trade-off: a missing method is a compile error, not a runtime surprise.

## The trade-off

Duck typing's freedom has a price: **type errors surface only at runtime**,
when the missing method is actually called. Mitigations: good tests, type
hints, `Protocol`s, and `mypy` for static checking.

## Interview traps

- Saying Python "doesn't have polymorphism" — duck typing *is* its
  dynamic polymorphism.
- Overusing `isinstance` — LBYL thinking that breaks duck typing's
  flexibility. Duck typing needs no inheritance; shared *behavior* is
  the contract.

**Takeaway:** Duck typing judges objects by what they can do, not what
they are — maximum flexibility, with the bill paid in runtime errors and
the need for good tests.
""",
                "difficulty_min": 2,
                "difficulty_max": 6,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A Zoho interviewer asks: 'Python never checks an object's class before calling its methods. What is that philosophy called — and what does it actually mean?'",
                        "choices": [
                            "An object's suitability is determined by the methods it supports, not its type or inheritance",
                            "Every class must inherit from a class named Duck",
                            "Type checking is done by the compiler before running",
                            "Objects can only call methods defined in their own class",
                        ],
                        "answer_index": 0,
                        "difficulty": 2,
                        "explanation": "The duck test — 'if it quacks like a duck' — means Python cares about behavior (does it have quack()?) rather than lineage (is it a subclass of Duck?).",
                        "company_tags": ["zoho", "tcs"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An interviewer asks: 'len() works on strings, lists, tuples, dicts, and sets — five totally unrelated types. How is that possible with no shared base class?'",
                        "choices": [
                            "Because they all inherit from a common Sized base class",
                            "Because len() is overloaded five times in the interpreter",
                            "Because each type defines the __len__ protocol method",
                            "Because Python converts everything to a list first",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "len() is duck typing in the standard library: it simply calls the object's __len__ method, and every sized type implements it — no shared inheritance needed.",
                        "company_tags": ["infosys", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Swiggy interviewer shows four code snippets and asks: 'Which one is duck typing in action — and why aren't the others?'",
                        "choices": [
                            "A function that only accepts arguments of type Duck",
                            "A class hierarchy where Bird extends Animal",
                            "An isinstance check before every method call",
                            "A function calling obj.quack() that works with any object defining quack()",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Duck typing is exactly this: the function never names a type, it just uses the behavior, so Duck, Person, or any future class with quack() all work.",
                        "company_tags": ["flipkart", "swiggy"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Razorpay interviewer asks: 'I see Python devs wrap things in try/except instead of checking with hasattr first. What is that style called — and why is it preferred?'",
                        "choices": [
                            "LBYL, because checking types first is always safer",
                            "Neither — Python forbids both patterns",
                            "EAFP (try it, handle failure), because it avoids check-then-act races and reads cleaner",
                            "LBYL, because exceptions are expensive in Python",
                        ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "EAFP — 'easier to ask forgiveness than permission' — is the Pythonic default: try the operation and catch AttributeError, instead of guarding every call with hasattr/isinstance checks.",
                        "company_tags": ["google", "razorpay"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer pushes back: 'Duck typing sounds great, but where does it bite you in production?' What is the honest answer?",
                        "choices": [
                            "It makes programs run ten times slower",
                            "Type errors surface only at runtime, when the missing method is actually called",
                            "It forbids the use of inheritance entirely",
                            "It requires writing twice as much code",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Because no type is declared, passing an object without the expected method fails only when that method is invoked — possibly far from where the wrong object entered. Tests, type hints, and Protocols mitigate this.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A PhonePe interviewer describes: 'Engine and Sail share no base class, but both implement start(), and my run(machine) works with either. What principle makes that possible?'",
                        "choices": [
                            "Multiple inheritance",
                            "Method overloading",
                            "Duck typing — polymorphic behavior without inheritance",
                            "A compile-time error waiting to happen",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "No shared base class exists; run() relies purely on the shared behavior start(). That behavior-based polymorphism is duck typing, Python's native form of dynamic polymorphism.",
                        "company_tags": ["phonepe", "google"],
                    },
                ],
            },
            {
                "slug": "oop-poly-pitfalls",
                "title": "Polymorphism Pitfalls & Interview Traps",
                "theory_md": """## Polymorphism Pitfalls & Interview Traps

Interviewers love the gap between what *looks* polymorphic and what
actually is. These four traps decide many Java interviews.

## Trap 1: Fields are NOT polymorphic (field hiding)

Methods are chosen by the **object** type; fields are chosen by the
**reference** type. A subclass field with the same name *hides* the parent
field — it does not override it.

```java
class A {
    String label = "A-label";
    void show() { System.out.println("A-show"); }
}
class B extends A {
    String label = "B-label";   // HIDES A.label — does not override it
    void show() { System.out.println("B-show"); }   // OVERRIDES
}
A ref = new B();
System.out.println(ref.label);  // "A-label" <- reference type wins!
ref.show();                     // "B-show"  <- object type wins!
```

## Trap 2: Static methods are hidden, not overridden

Static methods belong to the *class*, so the call is bound at **compile
time** to the reference type. The subclass version merely *hides* the
parent's.

```java
class A { static void who() { System.out.println("A"); } }
class B extends A { static void who() { System.out.println("B"); } }
A ref = new B();
ref.who();   // "A" — bound at compile time to the reference type
```

## Trap 3: Private methods cannot be overridden

A `private` method is not inherited, so a subclass method with the same
name is a **brand-new, unrelated method**. Same for constructors: never
inherited, never overridden.

## Trap 4: `final` methods cannot be overridden

Marking a method `final` locks it — subclasses inherit it as-is, and
overriding it is a compile error.

## Does Python have these traps?

Mostly no — which is the contrast to remember:

```python
class A: label = "A-label"
class B(A): label = "B-label"
print(B().label)   # "B-label" — lookup finds B's attribute first
```

Python has no static/instance dispatch split and no `final`, so these
traps are Java/C++ territory. Lesson: know *your* language's binding
rules.

## Quick-reference table

| Member | Polymorphic? | Decided by |
|---|---|---|
| Instance method (non-final, non-private, non-static) | Yes — overridden | Object type, at runtime |
| Field | No — hidden | Reference type, at compile time |
| Static method | No — hidden | Reference type, at compile time |
| Private method | No — not inherited | N/A |
| Final method | No — locked | N/A |

## Interview traps

- Assuming `ref.field` follows the object — it follows the *reference*.
- Calling a static method through an instance and expecting dynamic
  dispatch.
- Forgetting that `@Override` on a static/private method is a compile
  error — the compiler is telling you it is not an override.

**Takeaway:** Only overridable instance methods are truly polymorphic;
fields and static methods answer to the reference type — memorize the
table and these traps stop being traps.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks a trick question: 'Methods are polymorphic — but are instance FIELDS polymorphic too? Think carefully before you answer.'",
                        "choices": [
                            "Yes, fields are overridden exactly like methods",
                            "No — field access is resolved by the reference type at compile time",
                            "Yes, but only for public fields",
                            "No, fields cannot be declared in subclasses at all",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "A subclass field with the same name hides the parent field rather than overriding it, so ref.field uses the declared type of ref — unlike methods, which follow the actual object.",
                        "company_tags": ["tcs", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer writes this on the whiteboard and asks for the output:\n```java\nclass A { int x = 10; }\nclass B extends A { int x = 20; }\nA a = new B();\nSystem.out.println(a.x);\n```",
                        "choices": [
                            "Compile error",
                            "20",
                            "10",
                            "0",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "Fields are not polymorphic: a.x is bound at compile time to the reference type A, so it prints A's x (10) even though the object is a B.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Microsoft interviewer asks: 'My subclass redefines the parent's static method. I have overridden it — right?' What is wrong with that claim?",
                        "choices": [
                            "No — they are hidden, and the call binds at compile time to the reference type",
                            "Yes, exactly like instance methods",
                            "Yes, but only if marked @Override",
                            "No, static methods cannot exist in subclasses",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "Static methods belong to the class, not the object, so ref.who() resolves using ref's declared type. The subclass version hides the parent's; @Override on it is a compile error.",
                        "company_tags": ["microsoft", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer asks: 'A subclass declares a private method with the same name as a private method in its superclass. Did it just override it?'",
                        "choices": [
                            "The subclass method overrides the superclass method",
                            "They form an overloaded pair",
                            "The superclass method is abstract now",
                            "There is none — private methods are not inherited, so it is a new unrelated method",
                        ],
                        "answer_index": 3,
                        "difficulty": 7,
                        "explanation": "Overriding requires inheritance, and private members are not inherited. The two methods merely share a name; no polymorphic call can ever reach the subclass one through a parent reference.",
                        "company_tags": ["google", "meta"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Netflix interviewer writes this everything-at-once snippet and says: 'Three different binding rules are fighting in here. What prints?'\n```java\nclass A {\n    int x = 1;\n    void m() { System.out.print(\"Am\"); }\n    static void s() { System.out.print(\"As\"); }\n}\nclass B extends A {\n    int x = 2;\n    void m() { System.out.print(\"Bm\"); }\n    static void s() { System.out.print(\"Bs\"); }\n}\nA ref = new B();\nref.m(); ref.s(); System.out.print(ref.x);\n```",
                        "choices": [
                            "AmAs1",
                            "BmBs2",
                            "BmAs1",
                            "AmBs2",
                        ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "Only the instance method m() is truly polymorphic (object type B -> 'Bm'). The static s() binds to the reference type A ('As'), and the field x also follows the reference type (1). Hence 'BmAs1'.",
                        "company_tags": ["netflix", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer asks: 'I marked a security-sensitive method final, and a junior tried to override it anyway. What does the compiler do — and why is final the right tool there?'",
                        "choices": [
                            "It works, but generates a warning",
                            "Compile error — final methods cannot be overridden",
                            "It works at runtime but not in tests",
                            "The parent method is automatically deleted",
                        ],
                        "answer_index": 1,
                        "difficulty": 9,
                        "explanation": "final locks a method's implementation: subclasses inherit it as-is, and any attempt to override is rejected by the compiler. That is precisely why security-sensitive methods are marked final.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Meta interviewer shows you this field-hiding bug and asks why the output surprises juniors:\n```java\nclass A {\n    String label = \"A-label\";\n    void show() { System.out.println(label); }\n}\nclass B extends A {\n    String label = \"B-label\";   // hides A.label — does NOT override it\n}\nA ref = new B();\nref.show();\n```\nWhat prints — and why?",
                        "choices": [
                            "\"B-label\" — show() runs on a B object, so B's field wins",
                            "\"A-label\" — show() is inherited from A, so the method body reads A's field; fields bind at compile time, never polymorphically",
                            "Compile error — a subclass may not redeclare a parent field",
                            "\"A-labelB-label\" — both fields are printed",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "B never overrides show(), so A's method body executes — and inside that body, `label` was bound to A's field at compile time. Field access follows the class where the code is written, never the runtime object; that is exactly why juniors expecting \"B-label\" are surprised.",
                        "company_tags": ["meta", "google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer asks: 'Why does putting @Override on this static method fail to compile — and what does that failure prove?'\n```java\nclass A { static void who() { System.out.println(\"A\"); } }\nclass B extends A {\n    @Override\n    static void who() { System.out.println(\"B\"); }\n}\n```",
                        "choices": [
                            "It compiles fine — @Override is just optional documentation",
                            "Compile error: static methods are hidden, not overridden — the compiler is proving no overriding relationship exists",
                            "Compile error: two static methods may never share a name in one hierarchy",
                            "Runtime error: the JVM rejects the duplicate when class B loads",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "@Override asks the compiler to verify a genuine override; it fails because static methods belong to the class and bind at compile time to the reference type — B.who() merely hides A.who(). The compile error is the proof that no polymorphic relationship exists.",
                        "company_tags": ["google", "amazon", "microsoft"],
                    },
                ],
            },
        ],
    },
    {
        "slug": "oop-advanced",
        "name": "Advanced OOP Concepts",
        "description": "Design wisdom beyond the basics: the five SOLID principles, composition over inheritance, and the DRY/KISS/YAGNI habits that separate working code from maintainable code.",
        "lessons": [
            {
                "slug": "oop-solid-srp",
                "title": "SOLID: Single Responsibility Principle",
                "theory_md": """## SOLID: Single Responsibility Principle

**SRP:** *A class should have only one reason to change.* Not one method —
one **responsibility**, one axis of change. If a class does user
authentication, sends emails, *and* writes to the database, then a change
in email policy, auth rules, or DB schema all force edits to the same
class. That is the **god class** smell.

## The violation

```python
class User:                       # does THREE jobs — SRP violated
    def __init__(self, name, email, password):
        self.name, self.email, self.password = name, email, password

    def save_to_db(self):         # job 1: persistence
        print(f"INSERT INTO users ... {self.email}")

    def authenticate(self, pwd):  # job 2: auth
        return pwd == self.password

    def send_welcome_email(self): # job 3: notifications
        print(f"Email sent to {self.email}")
```

Change the email provider? Edit `User`. Change the DB? Edit `User`. Three
reasons to change = three ways to break unrelated behavior.

## The fix: split by responsibility

```python
class User:                       # job: hold user data only
    def __init__(self, name, email, password_hash):
        self.name = name
        self.email = email
        self.password_hash = password_hash

class UserRepository:             # job: persistence
    def save(self, user: User):
        print(f"INSERT INTO users ... {user.email}")

class AuthService:                # job: authentication
    def authenticate(self, user: User, password: str) -> bool:
        return hash(password) == user.password_hash

class EmailService:               # job: notifications
    def send_welcome(self, user: User):
        print(f"Welcome email sent to {user.email}")
```

## The same split in Java

```java
class User {
    private String name, email, passwordHash;
    // constructor + getters only — pure data holder
}

class UserRepository {
    void save(User u) { /* JDBC insert */ }
}

class AuthService {
    boolean authenticate(User u, String password) { /* check hash */ return true; }
}

class EmailService {
    void sendWelcome(User u) { /* SMTP call */ }
}
```

## Signs you are violating SRP

- The class name contains "and" or "Manager/Util" doing five things.
- Import lists spanning unrelated domains (SQL + SMTP + crypto).
- A change in one feature breaks tests for an unrelated feature.

## Interview traps

- "One class, one method" — **wrong**. SRP allows many methods as long as
  they serve one responsibility (e.g. `EmailService` can have
  `sendWelcome`, `sendReset`, `sendReceipt`).
- Splitting into 50 one-method classes is also bad — that is fragmentation,
  not SRP. Cohesion matters: keep related behavior together.

**Takeaway:** Give every class exactly one reason to change; when a class
starts doing "and", split it along its responsibilities.
""",
                "difficulty_min": 2,
                "difficulty_max": 7,
                "is_important": True,
                "has_visual": True,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A TCS interviewer asks: 'SRP in one sentence — go. And no, one class one method is not the answer.'",
                        "choices": [
                            "A class should have only one method",
                            "A program should have only one class",
                            "A class should have only one reason to change",
                            "A method should have only one parameter",
                        ],
                        "answer_index": 2,
                        "difficulty": 2,
                        "explanation": "SRP is about reasons to change, not method counts: a class should serve one responsibility so that each kind of change touches exactly one place.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a code-review round, the interviewer shows you a class and asks: 'What smell tells you this class is violating SRP?' Which of these is that smell?",
                        "choices": [
                            "A 'god class' that validates input, writes to the DB, sends emails, and logs analytics",
                            "A class with private fields and public getters",
                            "A class that is marked final",
                            "A class with a single constructor",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "When one class juggles validation, persistence, email, and logging, a change in any one concern forces edits to the same class — the textbook god-class SRP violation.",
                        "company_tags": ["accenture", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer reviews your PR: 'Your User class did auth, email, AND database saves. You split it into User, AuthService, EmailService, UserRepository — which principle did you apply, and why was the original a problem?'",
                        "choices": [
                            "Liskov Substitution Principle",
                            "Single Responsibility Principle",
                            "Interface Segregation Principle",
                            "Dependency Inversion Principle",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "Each new class now owns exactly one responsibility — data, auth, notifications, persistence — so each has a single reason to change. That is SRP applied.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Google interviewer shows you this class in a design review and asks which SOLID principle it breaks — and what you would split it into:\n```python\nclass Report:\n    def generate(self): ...\n    def save_to_db(self): ...\n    def email_to_manager(self): ...\n```",
                        "choices": [
                            "Open/Closed Principle",
                            "Dependency Inversion Principle",
                            "Liskov Substitution Principle",
                            "Single Responsibility Principle",
                        ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "Report mixes report generation, persistence, and notification — three responsibilities, three reasons to change. Splitting those into separate collaborators fixes the SRP violation.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer pushes back: 'So SRP means every class gets exactly one method, right?' How do you correct them?",
                        "choices": [
                            "Yes — one class, one method, no exceptions",
                            "No — it means one responsibility; a class may have many methods serving that single responsibility",
                            "Yes, but only in Java",
                            "No — SRP is about the number of fields, not methods",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "An EmailService with sendWelcome, sendReset, and sendReceipt has many methods but one responsibility (notifications) — perfectly SRP-compliant. The unit is the reason to change, not the method count.",
                        "company_tags": ["meta", "netflix"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Uber interviewer asks: 'Convince me SRP is worth the extra classes. What breaks in six months if I ignore it?'",
                        "choices": [
                            "Programs run measurably faster",
                            "Changes in one concern don't ripple into unrelated code, and each class stays small and focused",
                            "You need fewer unit tests",
                            "Inheritance hierarchies become deeper",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "With one responsibility per class, an email-provider switch touches only EmailService — DB and auth code are never at risk. SRP localizes change, which is the core maintainability win.",
                        "company_tags": ["uber", "google"],
                    },
                ],
            },
            {
                "slug": "oop-solid-ocp",
                "title": "SOLID: Open/Closed Principle",
                "theory_md": """## SOLID: Open/Closed Principle

**OCP:** *Software entities should be open for extension but closed for
modification.* You should be able to add new behavior **without editing
tested, working code** — extend it instead, typically through inheritance
or composition.

## The violation: the if-else chain

```python
class DiscountCalculator:
    def calculate(self, customer_type: str, amount: float) -> float:
        if customer_type == "regular":
            return amount * 0.95
        elif customer_type == "premium":
            return amount * 0.90
        elif customer_type == "vip":
            return amount * 0.85
        # adding "festive" means EDITING this tested method — OCP violated
        return amount
```

Every new discount type forces you to reopen and edit this method,
re-risking the existing branches.

## The fix: strategy-flavored extension

```python
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):          # closed for modification
    @abstractmethod
    def apply(self, amount: float) -> float: ...

class RegularDiscount(DiscountStrategy):
    def apply(self, amount): return amount * 0.95

class PremiumDiscount(DiscountStrategy):
    def apply(self, amount): return amount * 0.90

class DiscountCalculator:
    def calculate(self, strategy: DiscountStrategy, amount: float) -> float:
        return strategy.apply(amount)  # never edited again

# New discount? Add a class — touch nothing existing:
class FestiveDiscount(DiscountStrategy):
    def apply(self, amount): return amount * 0.80
```

## The same idea in Java

```java
interface DiscountStrategy { double apply(double amount); }

class RegularDiscount implements DiscountStrategy {
    public double apply(double amount) { return amount * 0.95; }
}

class DiscountCalculator {
    double calculate(DiscountStrategy s, double amount) {
        return s.apply(amount);   // closed: this method never changes
    }
}
// New behavior = new class implementing DiscountStrategy (open).
```

## OCP in the wild

Plugins, middleware chains, and payment gateways all follow OCP: the core
engine is closed, and new behavior arrives as new classes/modules. The
**Strategy pattern** is the canonical OCP example.

## Interview traps

- "Closed for modification means never touch the code" — **no**. Bug fixes
  are fine; the rule targets *new behavior*, which should come via
  extension.
- Reaching for inheritance when composition fits better — OCP works with
  both; injecting a strategy object (composition) is often cleaner than
  subclassing the calculator.
- A `switch` on a type code is the #1 OCP smell interviewers show you.

**Takeaway:** When adding a feature means editing old code, reach for
abstraction: make the varying part a new class, and keep the stable core
untouched.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A Cognizant interviewer asks: 'OCP says software should be open for one thing and closed for another. Open for what — closed for what?'",
                        "choices": [
                            "Classes should be open for extension but closed for modification",
                            "Source files should be closed after writing",
                            "Classes should be open for modification but closed for extension",
                            "Only open-source code can be extended",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "OCP's exact wording: open for extension (new behavior via new code), closed for modification (existing tested code stays untouched).",
                        "company_tags": ["tcs", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer asks: 'Marketing wants a new festive discount next week. Which design lets me add it without touching a single line of existing code?'",
                        "choices": [
                            "Add another elif branch to the existing calculate() method",
                            "Add a new DiscountStrategy subclass without touching existing code",
                            "Copy the whole calculator class and edit the copy",
                            "Delete the old discount types first",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "The strategy approach extends behavior by adding a class; the calculator's tested code is never reopened — OCP satisfied. Editing the elif chain is the violation.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During an Infosys LLD round, the interviewer points at a 40-line if-else chain on customer type and asks: 'This worked fine for a year. What is the design flaw that will hurt us next quarter?'",
                        "choices": [
                            "Nothing — it is the fastest possible design",
                            "Every new customer type forces editing already-tested code, risking existing behavior",
                            "It uses too much memory",
                            "Python does not support elif",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Each new branch reopens a working method, so a change for festive discounts can break regular discounts. That edit-to-extend cycle is exactly what OCP forbids.",
                        "company_tags": ["infosys", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Flipkart interviewer asks: 'Name the design pattern that is basically OCP in pattern form — new behavior arrives as a new class behind a common interface.'",
                        "choices": [
                            "Singleton",
                            "Factory Method",
                            "Strategy",
                            "Builder",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "Strategy encapsulates each varying algorithm (each discount) in its own class behind a common interface, so new algorithms extend the system without modifying the context that uses them.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer describes a real incident: 'Adding FestiveDiscount meant editing calculate() in three places — and last time that broke premium discounts. Which principle did we violate, and what is the structural fix?'",
                        "choices": [
                            "SRP — split the class into smaller methods",
                            "LSP — make FestiveDiscount a subclass of PremiumDiscount",
                            "ISP — split the interface",
                            "OCP — extract a DiscountStrategy abstraction so new discounts are added as new classes",
                        ],
                        "answer_index": 3,
                        "difficulty": 7,
                        "explanation": "The symptom — new behavior requires editing old code and breaks it — is the OCP violation signature. Introducing the strategy abstraction makes the calculator closed and each discount open for addition.",
                        "company_tags": ["google", "meta"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Netflix interviewer tries to trap you: 'OCP says closed for modification — so if I find a bug in that class, I am not allowed to fix it?' What is the correct response?",
                        "choices": [
                            "Yes — the class must never be touched again, even for bugs",
                            "No — bug fixes are fine; the rule targets new behavior, which should arrive via extension",
                            "Yes, but only in statically typed languages",
                            "No — OCP actually encourages rewriting classes monthly",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "OCP is about the economics of change: fixing a defect edits the class, but adding a feature should not require it. Extension (new classes) is the preferred vehicle for new behavior.",
                        "company_tags": ["netflix", "uber"],
                    },
                ],
            },
            {
                "slug": "oop-solid-lsp",
                "title": "SOLID: Liskov Substitution Principle",
                "theory_md": """## SOLID: Liskov Substitution Principle

**LSP:** *Objects of a subclass must be usable wherever objects of the
superclass are expected, without breaking the program.* If your code
accepts an `Animal`, handing it a `Dog` must never surprise it. Named
after Barbara Liskov, this is the principle that keeps inheritance
honest.

## The classic violation: Square vs Rectangle

Mathematically a square *is* a rectangle — so `Square extends Rectangle`
feels natural. It breaks in code:

```java
class Rectangle {
    protected int width, height;
    void setWidth(int w) { width = w; }
    void setHeight(int h) { height = h; }
    int area() { return width * height; }
}

class Square extends Rectangle {
    void setWidth(int w) { width = height = w; }   // keeps it square...
    void setHeight(int h) { width = height = h; }  // ...but breaks the contract
}

void resize(Rectangle r) {
    r.setWidth(5);
    r.setHeight(4);
    assert r.area() == 20;   // FAILS for Square (area is 16)!
}
```

`Square` cannot honor `Rectangle`'s contract (width and height vary
independently), so substituting it breaks client code. **Inheritance was
the wrong tool** — a square is not a *behavioral* rectangle.

## The contract rules behind LSP

- **Preconditions** cannot be strengthened: a subclass must accept at
  least what the parent accepts.
- **Postconditions** cannot be weakened: it must guarantee at least what
  the parent guarantees.
- No new **exceptions** for inputs the parent handled fine.

```python
class Bird:
    def fly(self) -> str:
        return "flying high"

class Penguin(Bird):          # LSP violation!
    def fly(self) -> str:
        raise Exception("penguins can't fly")

def migrate(bird: Bird):
    print(bird.fly())         # breaks for Penguin

# Better: don't force the hierarchy — separate the capability
class Flyable:
    def fly(self) -> str: ...
```

## Fixes that respect LSP

1. **Don't inherit** — use composition or sibling classes (`Square` and
   `Rectangle` both implement `Shape`).
2. **Weaken the parent contract** or split capabilities into small
   interfaces (`Flyable` for birds that fly).
3. When in doubt, prefer composition — it cannot violate LSP because
   there is no substitution.

## Interview traps

- "Square is-a Rectangle, so inheritance is correct" — mathematically
  yes, behaviorally **no**; LSP cares about behavior.
- Overriding a method to throw `UnsupportedOperationException` for inputs
  the parent accepted — a textbook LSP violation (looking at you,
  immutable-collection wrappers that throw on `add`).
- Thinking LSP is only about Java — it governs any subtype relationship,
  including Python duck-typed substitutability.

**Takeaway:** Inheritance is a behavioral promise: if a subclass can't
stand in for its parent without surprises, don't inherit — compose or
restructure instead.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A TCS interviewer asks: 'LSP in one line. Then, in plain words — what breaks in real code when it is violated?'",
                        "choices": [
                            "Objects of a subclass must be usable wherever the superclass is expected, without breaking behavior",
                            "Every subclass must add at least one new method",
                            "Subclasses must be smaller than their superclasses",
                            "A superclass must never be instantiated directly",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "That substitutability sentence IS LSP: client code written against the parent contract must keep working with any child object, no surprises allowed.",
                        "company_tags": ["tcs", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer says: 'Mathematically a square IS a rectangle, so Square extends Rectangle should be perfect design.' Where does that reasoning collapse in real code?",
                        "choices": [
                            "Because squares have four sides and rectangles don't",
                            "Because Java forbids geometric class names",
                            "Because Square cannot honor setWidth/setHeight varying independently, breaking Rectangle's contract",
                            "Because area() runs slower for squares",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "Rectangle promises independent width/height; Square must couple them to stay square. Code like resize() that relies on the parent contract then fails — substitution broken.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer asks: 'Your subclass rejects an input the parent happily accepted. Which LSP contract rule did you just break — and why does it matter to callers?'",
                        "choices": [
                            "A subclass must strengthen preconditions to be safer",
                            "A subclass must not strengthen preconditions — it must accept at least what the parent accepts",
                            "Preconditions don't matter as long as postconditions hold",
                            "Only the parent class may declare preconditions",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Strengthening preconditions (rejecting inputs the parent accepted) means existing client code can suddenly fail with a subclass — the opposite of safe substitution.",
                        "company_tags": ["microsoft", "meta"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During a Google code review you spot a subclass whose process(data) throws on input the superclass handled fine. You flag it — which principle backs your review comment?",
                        "choices": [
                            "Single Responsibility Principle",
                            "Open/Closed Principle",
                            "Dependency Inversion Principle",
                            "Liskov Substitution Principle",
                        ],
                        "answer_index": 3,
                        "difficulty": 7,
                        "explanation": "Client code written against the superclass reasonably passes that input; the subclass blows up instead. The subclass is not substitutable — a direct LSP violation.",
                        "company_tags": ["google", "netflix"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Uber interviewer follows up on the Square/Rectangle mess: 'Okay, it is broken. No hacks — what is the clean structural fix?'",
                        "choices": [
                            "Make setWidth and setHeight final in Rectangle",
                            "Don't inherit — model Square and Rectangle as siblings (e.g. both implement Shape) or use composition",
                            "Add more methods to Square until it behaves like Rectangle",
                            "Catch the assertion error in client code",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "The inheritance itself is the lie: a square is not a behavioral rectangle. Removing the false IS-A (siblings under Shape, or composition) eliminates the substitutability problem at its root.",
                        "company_tags": ["uber", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Microsoft interviewer asks the famous follow-up: '`Penguin extends Bird`, but penguins cannot fly, so `Penguin.fly()` throws. Why is this an LSP violation — and what is the standard fix you would give in an interview?'",
                        "choices": [
                            "It isn't a violation — exceptions are fine anywhere",
                            "It violates LSP because Bird clients expect fly() to work; fix by restructuring — e.g. a Flyable interface only for birds that fly, with Penguin not extending a flying Bird",
                            "It violates SRP — Penguin does too much",
                            "It violates OCP — Bird should be closed",
                        ],
                        "answer_index": 1,
                        "difficulty": 9,
                        "explanation": "Any code calling bird.fly() on a Bird breaks when handed a Penguin — substitutability fails. The accepted fix separates the capability (Flyable) from the taxonomy so Penguin never promises flight.",
                        "company_tags": ["google", "microsoft"],
                    },
                ],
            },
            {
                "slug": "oop-solid-isp",
                "title": "SOLID: Interface Segregation Principle",
                "theory_md": """## SOLID: Interface Segregation Principle

**ISP:** *Clients should not be forced to depend on methods they do not
use.* A **fat interface** — one big interface with many unrelated methods
— forces every implementer to stub out methods it doesn't need. Split fat
interfaces into small, focused ones.

## The violation: the fat Worker interface

```java
interface Worker {
    void work();
    void eat();
}

class Human implements Worker {
    public void work() { /* ... */ }
    public void eat()  { /* ... */ }
}

class Robot implements Worker {
    public void work() { /* ... */ }
    public void eat()  {
        throw new UnsupportedOperationException("robots don't eat!");
    }
}
```

`Robot` is forced to implement `eat()` — a method meaningless for it —
and the `throw` is a latent LSP violation too. The interface is fat.

## The fix: segregate

```java
interface Workable { void work(); }
interface Eatable  { void eat(); }

class Human implements Workable, Eatable {
    public void work() { /* ... */ }
    public void eat()  { /* ... */ }
}
class Robot implements Workable {   // only what it needs
    public void work() { /* ... */ }
}
```

## The same idea in Python

```python
from abc import ABC, abstractmethod

class Workable(ABC):
    @abstractmethod
    def work(self): ...

class Eatable(ABC):
    @abstractmethod
    def eat(self): ...

class Human(Workable, Eatable):
    def work(self): print("working")
    def eat(self):  print("eating")

class Robot(Workable):          # no fake eat() needed
    def work(self): print("working")```

## ISP vs SRP — don't confuse them

- **SRP** is about a *class* having one responsibility (one reason to
  change).
- **ISP** is about *interfaces* being small and client-specific (no forced
  dependencies on unused methods).

They rhyme, but they govern different artifacts.

## Interview traps

- "ISP means interfaces must be tiny" — **no**. A cohesive interface whose
  clients use all of it is fine; the rule targets *forced* dependencies.
- Implementing a method as `throw new UnsupportedOperationException()` —
  interviewers read this as both an ISP smell and an LSP violation.
- Confusing ISP with SRP in "which principle?" questions — check whether
  the complaint is about the *interface's* breadth (ISP) or the *class's*
  responsibilities (SRP).

**Takeaway:** Keep interfaces lean and client-shaped: no implementer
should ever have to write a method that means nothing to it.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "An Infosys interviewer asks: 'ISP in one line — and what is the fat-interface problem it is trying to kill?'",
                        "choices": [
                            "Interfaces must never have more than three methods",
                            "Clients should not be forced to depend on methods they don't use",
                            "Every class must implement every interface",
                            "Interfaces should be segregated by programming language",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "ISP's core complaint is the fat interface: when one big interface bundles unrelated methods, implementers are forced to carry methods meaningless to them.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Flipkart interviewer reviews your Robot class: its eat() just throws UnsupportedOperationException because robots do not eat. 'Which principle did this design violate — and what forced your hand here?'",
                        "choices": [
                            "Single Responsibility Principle",
                            "Open/Closed Principle",
                            "Liskov Substitution Principle",
                            "Interface Segregation Principle",
                        ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Robot is forced to depend on eat(), a method it can never meaningfully implement — the textbook fat-interface ISP violation (the throw is also an LSP smell).",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An interviewer asks: 'Your Robot is stuck implementing an eat() it cannot honor. How do you refactor the interface design so nobody implements a meaningless method?'",
                        "choices": [
                            "Split it into small focused interfaces like Workable and Eatable, so each client implements only what it needs",
                            "Delete the eat() method from Human too",
                            "Make Robot extend Human",
                            "Mark the interface as final",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "Segregating the interface lets Human take both roles while Robot takes only Workable — nobody implements a meaningless method anymore.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer asks the classic confusion question: 'ISP and SRP sound like the same idea. What is the real difference — what does each one govern?'",
                        "choices": [
                            "They are the same principle with two names",
                            "ISP applies only to Java, SRP only to Python",
                            "SRP is about a class having one responsibility; ISP is about interfaces being small and client-specific",
                            "SRP is about interfaces and ISP is about classes",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "SRP governs classes (reasons to change); ISP governs interfaces (forced dependencies). A question complaining about interface breadth is ISP; about a class doing many jobs is SRP.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer describes: 'You must implement a 10-method interface but genuinely need only 2 of them — eight empty stubs. Name the smell, and the ISP-aligned fix.'",
                        "choices": [
                            "No smell — just leave 8 methods empty",
                            "ISP violation — segregate the interface into smaller role interfaces (or use an adapter) so clients depend only on what they use",
                            "SRP violation — delete the class",
                            "OCP violation — the interface must be rewritten monthly",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Being forced to carry 8 unused methods is exactly what ISP forbids. Splitting into role interfaces lets each client depend only on its slice.",
                        "company_tags": ["meta", "netflix"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Uber interviewer pushes: 'So ISP means no interface can ever be large? What if every client genuinely uses all fifteen methods?'",
                        "choices": [
                            "Yes — every interface must have at most 3 methods",
                            "Yes — large interfaces always break compilation",
                            "No — it forbids forcing clients to depend on methods they don't use; a cohesive interface whose clients use all of it is fine",
                            "No — ISP only applies to abstract classes",
                        ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "ISP is client-centric, not size-centric: the sin is unused forced dependencies, not method count. A broad but fully-used, cohesive interface complies with ISP.",
                        "company_tags": ["uber", "google"],
                    },
                ],
            },
            {
                "slug": "oop-solid-dip",
                "title": "SOLID: Dependency Inversion Principle",
                "theory_md": """## SOLID: Dependency Inversion Principle

**DIP:** *High-level modules should not depend on low-level modules; both
should depend on abstractions. Abstractions should not depend on details;
details should depend on abstractions.* In plain words: **depend on
interfaces, not on concrete classes.**

## The violation: new-ing the concretion

```python
class StripeGateway:                 # low-level detail
    def charge(self, amount): ...

class OrderService:                  # high-level policy
    def __init__(self):
        self.gateway = StripeGateway()   # hard-wired to a concretion!

    def checkout(self, amount):
        self.gateway.charge(amount)
```

Want to test `OrderService` without hitting Stripe? Want to switch to
Razorpay? You must edit the class — and you cannot substitute a fake.

## The fix: depend on an abstraction (constructor injection)

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):           # abstraction
    @abstractmethod
    def charge(self, amount): ...

class StripeGateway(PaymentGateway):
    def charge(self, amount): print(f"Stripe: {amount}")

class FakeGateway(PaymentGateway):   # test double — swappable!
    def charge(self, amount): print(f"Fake: {amount}")

class OrderService:
    def __init__(self, gateway: PaymentGateway):  # injected abstraction
        self.gateway = gateway

    def checkout(self, amount):
        self.gateway.charge(amount)

OrderService(StripeGateway()).checkout(500)   # production
OrderService(FakeGateway()).checkout(500)     # tests — no edit needed
```

## The same in Java

```java
interface PaymentGateway { void charge(double amount); }

class OrderService {
    private final PaymentGateway gateway;
    // constructor injection: the abstraction is supplied, not created
    OrderService(PaymentGateway gateway) { this.gateway = gateway; }
    void checkout(double amount) { gateway.charge(amount); }
}
```

## DIP vs DI vs IoC — the interview trifecta

| Term | What it is |
|---|---|
| **DIP** | The *principle*: depend on abstractions |
| **DI** (Dependency Injection) | The *technique*: supply dependencies from outside (constructor/setter) |
| **IoC** (Inversion of Control) | The *broader concept*: the framework calls your code, not vice versa; DI containers are one IoC mechanism |

DIP says *what* (depend on abstractions); DI is *how* you wire it;
IoC frameworks (Spring, etc.) *automate* the wiring.

## Interview traps

- "DIP means never use concrete classes" — **wrong**. Concretions are
  created at the *composition root* (main/wiring code); the rule is that
  high-level logic *depends* on abstractions.
- Confusing DI with DIP — DI is the technique, DIP the principle; you can
  do DI without DIP (injecting a concrete class) and gain little.
- `new` inside business logic is the #1 DIP smell interviewers show.

**Takeaway:** Invert the dependency arrow — both sides point at the
abstraction; inject concretions at the edges, and testing plus swapping
become trivial.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A TCS interviewer asks: 'DIP inverts something — what exactly gets inverted, and what should both sides depend on instead?'",
                        "choices": [
                            "Subclasses must invert the methods of their parents",
                            "High-level modules should not depend on low-level modules — both should depend on abstractions",
                            "Dependencies should be listed in reverse alphabetical order",
                            "Low-level modules should never be written",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "DIP flips the traditional dependency direction: instead of policy depending on details, both depend on an abstraction (usually an interface) sitting between them.",
                        "company_tags": ["tcs", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer points at this constructor and asks what design decision it encodes:\n```python\ndef __init__(self, gateway: PaymentGateway): ...  # PaymentGateway is an interface\n```",
                        "choices": [
                            "DIP: the high-level OrderService depends on an abstraction, with the concretion supplied from outside",
                            "SRP: OrderService has one method",
                            "LSP: PaymentGateway is substitutable",
                            "A syntax error — interfaces can't be type hints",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "This is constructor injection of an abstraction — OrderService never names StripeGateway, so any PaymentGateway (real or fake) can be supplied. That is DIP in action.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During an Infosys code review, the interviewer highlights this line and asks what is wrong with it:\n```python\nclass OrderService:\n    def __init__(self):\n        self.gateway = StripeGateway()  # created inside the class\n```",
                        "choices": [
                            "Nothing — this is the recommended pattern",
                            "It violates SRP because there are two classes",
                            "It hard-wires the high-level class to a low-level concretion, so you can't swap or test-double the gateway without editing the class",
                            "Python forbids instantiating classes in __init__",
                        ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "Creating the concretion inside the class fuses policy to detail: switching providers or injecting a fake for tests requires editing OrderService — the DIP violation signature.",
                        "company_tags": ["infosys", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Microsoft interviewer asks the trifecta question: 'Everyone mixes up DIP, DI, and IoC. Untangle them — which is the principle, which is the technique, which is the concept?'",
                        "choices": [
                            "They are three names for the exact same thing",
                            "DIP is the principle (depend on abstractions), DI is the technique (supply dependencies externally), IoC is the broader concept (framework calls your code; containers automate wiring)",
                            "DI is the principle and DIP is the framework",
                            "IoC means never using interfaces",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "DIP states the design goal, DI is how you achieve it (constructor/setter injection), and IoC is the wider inversion idea that DI containers implement. Interviewers ask this distinction deliberately.",
                        "company_tags": ["microsoft", "meta"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer describes a war story: 'Our unit tests hit a real database because the class news up its own DB client. Which principle would have prevented this — and how?'",
                        "choices": [
                            "Single Responsibility Principle",
                            "Liskov Substitution Principle",
                            "Interface Segregation Principle",
                            "DIP — inject the database abstraction so tests can supply a fake",
                        ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "Depending on a database abstraction (injected) instead of a concretion (new-ed) is precisely DIP; it makes the class testable and the database swappable without edits.",
                        "company_tags": ["google", "netflix"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Uber interviewer tries the extreme take: 'DIP says depend on abstractions — so the new keyword is banned everywhere, right?' How do you answer?",
                        "choices": [
                            "No — concretions are created at the composition root / wiring code; the rule is that high-level logic depends on abstractions, not that concretions never exist",
                            "Yes — every object must be an interface",
                            "Yes — the `new` keyword is banned by DIP",
                            "No — DIP only applies to Python",
                        ],
                        "answer_index": 0,
                        "difficulty": 9,
                        "explanation": "Someone must eventually new up StripeGateway — DIP just says that happens once at the application's edge (main, config, container), while the business logic depends only on PaymentGateway.",
                        "company_tags": ["uber", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Swiggy interviewer reviews your notification service and points at the constructor:\n```python\nclass NotificationService:\n    def __init__(self):\n        self.client = SMTPClient()  # concrete class, built inside\n```\n'Tell me everything that's wrong with this line from a DIP perspective.'",
                        "choices": [
                            "Nothing — building collaborators in the constructor is the standard pattern",
                            "The high-level service is hard-wired to a low-level concretion: you cannot swap providers or inject a fake for tests without editing the class",
                            "It violates SRP because the constructor performs two responsibilities",
                            "Python forbids instantiating classes inside __init__",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Creating SMTPClient inside the constructor fuses the high-level notification policy to a low-level detail. Depending on an injected MailClient abstraction instead would let you swap providers or pass a fake in tests with zero edits to the service — that is DIP's whole payoff.",
                        "company_tags": ["swiggy", "flipkart", "razorpay"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Razorpay interviewer asks: 'You did everything right — OrderService takes an injected PaymentGateway abstraction. So why do your unit tests still take 40 seconds hitting the sandbox gateway, and what's the fix in your test setup?'",
                        "choices": [
                            "DIP can't fix slow tests — you need faster hardware or a closer sandbox",
                            "Pass a FakeGateway test double that implements the same PaymentGateway abstraction — DIP is exactly what makes the swap possible without touching the service",
                            "Make the gateway a global singleton so all tests share one sandbox connection",
                            "Drop the abstraction in tests — concretions are faster to exercise directly",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "The abstraction is only half the win; the other half is using it. In tests you inject a FakeGateway implementing PaymentGateway, so checkout() runs in milliseconds with no network. If the service had new-ed the real gateway, no test double could ever be substituted.",
                        "company_tags": ["razorpay", "amazon", "flipkart"],
                    },
                ],
            },
            {
                "slug": "oop-composition",
                "title": "Composition over Inheritance + DRY/KISS/YAGNI",
                "theory_md": """## Composition over Inheritance + DRY/KISS/YAGNI

Inheritance is OOP's most famous tool — and its most misused. The
industry rule of thumb: **prefer composition (HAS-A) over inheritance
(IS-A)**, and let three tiny acronyms guard your simplicity.

## HAS-A vs IS-A: the decision guide

Ask one question: *"Is X really a Y, behaviorally?"*

- `Car` **HAS-A** `Engine` — composition. The car delegates: it is not
  an engine.
- `Dog` **IS-A** `Animal` — inheritance fits, if Dog honors Animal's
  contract (LSP!).

When in doubt, compose: you can change behavior at runtime by swapping
the contained object, with no fragile parent-child coupling.

```python
# Inheritance (rigid): every vehicle bakes in its engine behavior
class Vehicle: ...
class Car(Vehicle): ...

# Composition (flexible): swap the engine without touching Car
class Engine:
    def start(self): return "vroom"

class ElectricMotor:
    def start(self): return "whirr"

class Car:
    def __init__(self, engine):      # HAS-A engine
        self.engine = engine
    def start(self):
        return self.engine.start()

Car(Engine()).start()          # vroom
Car(ElectricMotor()).start()   # whirr — no subclass needed
```

```java
class Car {
    private final Engine engine;   // HAS-A, not IS-A
    Car(Engine engine) { this.engine = engine; }
    void start() { engine.start(); }
}
```

## The fragile base class problem

With inheritance, a change to the base class can silently break
subclasses: a new base method can collide with a subclass method, or a
changed base behavior can violate subclass assumptions. Composition
isolates you — the contained object's internals are hidden behind its
interface.

## Coupling vs cohesion — the twin goals

- **High cohesion:** each module does one thing well (echoes SRP).
- **Low coupling:** modules depend on as little of each other as possible
  (echoes DIP/ISP).

Composition naturally lowers coupling: `Car` depends only on `Engine`'s
`start()`, not on a whole inheritance chain.

## DRY / KISS / YAGNI — the simplicity trio

| Principle | Meaning | Example |
|---|---|---|
| **DRY** (Don't Repeat Yourself) | Every piece of knowledge lives in one place | Extract the validation logic copied in 5 places into one function |
| **KISS** (Keep It Simple, Stupid) | Prefer the simplest design that works | A plain list beats a custom linked list for 20 items |
| **YAGNI** (You Aren't Gonna Need It) | Don't build speculative features | Skip the "maybe we'll need plugins" framework on day one |

DRY fights duplication, KISS fights cleverness, YAGNI fights
over-engineering — together they keep composition-based designs from
ballooning.

## Interview traps

- "Inheritance is always better because it reuses code" — reuse via
  composition reuses just as well, without the coupling.
- DRY taken to extremes: abstracting two similar lines into a
  parameterized monster is *worse* than mild duplication — DRY is about
  knowledge, not characters.
- YAGNI vs planning: YAGNI doesn't forbid good seams (interfaces are
  cheap); it forbids *building* the unneeded feature.

**Takeaway:** Inherit only for true behavioral IS-A; otherwise compose —
and let DRY, KISS, and YAGNI keep the result simple.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "A TCS interviewer asks: 'Everyone says prefer composition over inheritance. Prefer it for what — and when IS inheritance the right call?'",
                        "choices": [
                            "Never use inheritance under any circumstances",
                            "Always use multiple inheritance",
                            "Composition and inheritance are identical",
                            "Prefer HAS-A relationships via contained objects; inherit only for a true behavioral IS-A",
                        ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "The guideline isn't anti-inheritance — it's pro-choice: compose by default for flexibility, and reserve inheritance for genuine is-a relationships that satisfy LSP.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a design round you must model a Car and an Engine: `Car extends Engine`, or Car holds an Engine object. Which do you pick — and what is the one question that decides it?",
                        "choices": [
                            "Car extends Engine — inheritance always wins",
                            "Car containing an Engine (HAS-A) — a car is not behaviorally an engine, and composition lets you swap engines",
                            "Both are equally good",
                            "Neither — cars shouldn't have engines in OOP",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "A car HAS an engine; it isn't one. Composition models this truthfully and lets you plug in ElectricMotor without new subclasses, while inheritance would bake in the wrong relationship.",
                        "company_tags": ["accenture", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer asks: 'I changed one method in a base class and three subclasses broke in production. What is this phenomenon called — and which design choice invites it?'",
                        "choices": [
                            "Base classes use too much memory",
                            "Base classes cannot have constructors",
                            "Changes to a base class can unexpectedly break its subclasses",
                            "Subclasses cannot access base class fields",
                        ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "Because subclasses depend on base-class internals and behavior, editing the base (new methods, changed semantics) can silently break children — a key argument for preferring composition.",
                        "company_tags": ["amazon", "google"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Flipkart interviewer asks: 'You keep saying high cohesion, low coupling like a mantra. Define both — and tell me how composition helps achieve them.'",
                        "choices": [
                            "Each module does one thing well and depends on as little of other modules as possible",
                            "All code should live in one highly coupled module",
                            "Modules should never communicate",
                            "Cohesion means using only inheritance",
                        ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "Cohesion is internal focus (one job per module, echoing SRP); coupling is external dependence (minimized via abstractions, echoing DIP/ISP). Composition naturally serves both.",
                        "company_tags": ["microsoft", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer asks: 'Your teammate built a plugin framework for future flexibility on day one of the project. Which principle did they violate?'",
                        "choices": [
                            "Writing any code at all",
                            "Building speculative features 'just in case' before there is a real need",
                            "Using design patterns",
                            "Refactoring existing code",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "YAGNI targets speculative generality — the plugin framework nobody asked for. Build what today's requirements need, but keep seams (interfaces) cheap so extension stays easy.",
                        "company_tags": ["google", "meta"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During a Netflix code review you find the same validation logic copy-pasted in 5 files. You leave a review comment — which principle do you cite, and what fix do you propose?",
                        "choices": [
                            "YAGNI — delete 4 of the copies",
                            "KISS — rewrite it more cleverly in each place",
                            "DRY — extract the logic into one shared function/class used by all 5 places",
                            "LSP — make the copies inherit from each other",
                        ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "Duplicated knowledge is DRY's exact target: one canonical implementation means a bug fix or rule change happens once, not five times, with no drift between copies.",
                        "company_tags": ["netflix", "uber"],
                    },
                ],
            },
        ],
    },
]

