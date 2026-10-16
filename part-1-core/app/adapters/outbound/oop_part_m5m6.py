"""Seed content: OOP — Modules 5-6 (Design Patterns, OOP in Practice).

Module 5 (oop-patterns): the Gang of Four essentials interviewers actually ask
about — Singleton, Factory variants, Observer, Strategy, Decorator, Adapter /
Facade, and the MVC/MVP/MVVM family — with real Python and Java examples.

Module 6 (oop-practice): language-specific OOP depth (Python dunder +
dataclasses, Java final/records, C++ RAII + smart pointers), LLD interview
basics via a parking-lot walkthrough, and a rapid-fire revision sheet.

All theory is original educational prose with real, runnable code — no copied
textbook passages. Each lesson carries exactly 6 MCQs with varied answer
positions, difficulty spread >= 4 within the lesson, and WHY-style
explanations.

Exports a single variable: MODULES (list of 2 module dicts).
"""
from __future__ import annotations

MODULES = [
    {
        "slug": "oop-patterns",
        "name": "Design Patterns",
        "description": (
            "Reusable solutions to recurring design problems: the Gang of Four "
            "essentials every interviewer expects — Singleton, Factory variants, "
            "Observer, Strategy, Decorator, Adapter/Facade, and MVC vs MVP vs "
            "MVVM — with real Python and Java implementations, thread-safety "
            "traps, and when each pattern genuinely applies."
        ),
        "lessons": [
            {
                "slug": "oop-pattern-singleton",
                "title": "Singleton Pattern",
                "theory_md": """## Singleton Pattern

The **Singleton** guarantees that a class has **exactly one instance** and
provides a **global point of access** to it. Think of it as "there can be only
one": one configuration object, one logger, one database connection pool for
the whole application.

Legitimate uses are narrow: configuration holders, logging services,
thread pools, caches, and device-driver wrappers. If you reach for it for
ordinary business objects, pause — that is usually the trap.

### Python: three idioms

**1. Override `__new__`** — control instance creation directly:

```python
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = {}
        return cls._instance

a = Config()
b = Config()
print(a is b)          # True
a.settings["mode"] = "dark"
print(b.settings)      # {'mode': 'dark'}
```

**2. A metaclass** — apply the rule to every class that uses it:

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    pass

print(Logger() is Logger())   # True
```

**3. Just use a module.** A Python module is imported once and shared —
often the simplest, most Pythonic "singleton".

### Java: eager, lazy, double-checked, enum

```java
// Eager: simple, thread-safe, but created even if never used
class EagerDB {
    private static final EagerDB INSTANCE = new EagerDB();
    private EagerDB() {}
    public static EagerDB getInstance() { return INSTANCE; }
}

// Double-checked locking: lazy AND thread-safe (note `volatile`!)
class LazyDB {
    private static volatile LazyDB instance;
    private LazyDB() {}
    public static LazyDB getInstance() {
        if (instance == null) {
            synchronized (LazyDB.class) {
                if (instance == null) {
                    instance = new LazyDB();
                }
            }
        }
        return instance;
    }
}

// Enum: the safest — serialization- and reflection-proof
enum EnumDB {
    INSTANCE;
    public void query(String sql) { /* ... */ }
}
```

### The thread-safety trap

A naive lazy singleton (`if (instance == null) instance = new ...`
without synchronization) lets **two threads create two instances** when they
race through the null check together. The `volatile` keyword in
double-checked locking prevents instruction reordering from exposing a
half-constructed object — a classic interview follow-up.

### When NOT to use it

* It hides dependencies — `new OrderService()` secretly depends on a global.
* It makes unit testing painful (global state leaks between tests).
* It is often just a global variable wearing a tuxedo. Prefer **dependency
  injection**: pass the one instance in through the constructor.

**Takeaway:** Singleton = one instance, global access — reach for it for
config/loggers/pools, implement it thread-safely, and question it everywhere
else.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer opens with a warm-up: 'We need one shared configuration object for the whole application — no matter how many places ask for it. What two guarantees must your design provide?'",
                        "choices": [
                            "The class is immutable and all its methods are static",
                            "The class cannot be subclassed and cannot be serialized",
                            "Exactly one instance exists, with a global point of access to it",
                            "The instance is created lazily and destroyed on program exit",
                        ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Singleton's whole contract is (1) only one instance of the class can ever exist and (2) everyone reaches it through one global access point, typically getInstance(). Immutability, non-subclassability, and lazy creation are separate, optional properties.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this Python snippet print?\n\nclass Cache:\n    _inst = None\n    def __new__(cls):\n        if cls._inst is None:\n            cls._inst = super().__new__(cls)\n        return cls._inst\n\nprint(Cache() is Cache(), Cache() == Cache())",
                        "choices": [
                                       "False False",
                                       "False True",
                                       "True False",
                                       "True True",
                                   ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "__new__ returns the same stored object every time, so `is` is True. Since the class doesn't override __eq__, `==` falls back to identity comparison, which is also True for the same object.",
                        "company_tags": ["wipro", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Flipkart interviewer points at your lazy singleton on the whiteboard and asks: 'Walk me through what breaks when fifty threads hit get() at the same instant.\n\nprivate static DB conn;\npublic static DB get() {\n    if (conn == null) conn = new DB();\n    return conn;\n}",
                        "choices": [
                                       "Two threads can both pass the null check and create two instances",
                                       "Static fields cannot be assigned inside static methods",
                                       "The JVM forbids lazy initialization of static fields",
                                       "get() must be declared synchronized to compile",
                                   ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "The race is in the null check: thread A sees conn == null and pauses before constructing; thread B also sees null and constructs. Now two DB objects exist and the second assignment silently overwrites the first. Synchronization (or eager init, or an enum) closes the race.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An interviewer leans in: 'Clever developers can break a singleton with reflection or by deserializing it. Which Java implementation survives both attacks — and why does it survive?'",
                        "choices": [
                            "Enums are allocated on the stack, so they are faster",
                            "The JVM guarantees single instantiation even against reflection and serialization attacks",
                            "Enums cannot have methods, so the instance can never be misused",
                            "Enum constants are lazily loaded only when first serialized",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Reflection can invoke private constructors to break __new__-style singletons, and deserialization creates fresh objects unless you write readResolve(). The JVM itself enforces enum uniqueness, so both attack vectors fail automatically — no extra code needed.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer nods at your double-checked locking and follows up: 'You've got the synchronized block and the double null-check — so why does the instance field ALSO need to be volatile? What breaks without it?'",
                        "choices": [
                                       "volatile makes the synchronized block unnecessary",
                                       "volatile forces eager initialization at class-load time",
                                       "volatile prevents the JVM from reordering writes so no thread sees a half-constructed object",
                                       "volatile allows multiple threads to enter the synchronized block",
                                   ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "Without volatile, the write of the reference can become visible to other threads before the constructor finishes (instruction reordering), so a thread could grab a non-null but half-built object. volatile establishes a happens-before edge that forbids this reordering.",
                        "company_tags": ["amazon", "uber"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A teammate makes the database handle, the config, the logger, and the current user all singletons. What is the strongest objection?",
                        "choices": [
                            "Hidden global dependencies make the code hard to test and reason about — prefer dependency injection",
                            "Singletons use too much memory because they are never garbage collected",
                            "Singletons cannot be used from more than one thread under any circumstances",
                            "The Singleton pattern is deprecated in modern Java and Python",
                        ],
                        "answer_index": 0,
                        "difficulty": 8,
                        "explanation": "The real cost of singleton abuse is invisible coupling: every class secretly depends on global state, so tests can't isolate units and behavior depends on execution order. Passing the single instance through constructors (dependency injection) keeps the 'only one' property while making dependencies explicit and testable.",
                        "company_tags": ["meta", "netflix"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your PhonePe interviewer asks: 'Our payment service needs exactly one database connection pool shared across threads. You write a lazy getInstance() with a plain null check — what breaks under load, and how do you fix it?'",
                        "choices": [
                            "Nothing breaks — the first thread to finish wins and later threads silently reuse its instance",
                            "Two threads can pass the null check together and build two pools; fix it with double-checked locking on a volatile field, or use an eager or enum singleton",
                            "The JVM serializes all static method calls automatically, so the naive version is already thread-safe",
                            "Lazy initialization cannot work for connection pools; only eager singletons are legal here",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "The naive null check is a check-then-act race: two threads can both observe null and each construct a pool, so 'exactly one' silently becomes two. Double-checked locking with a volatile field closes the race while keeping lazy startup; an eager or enum singleton avoids the race entirely. Name the race first, then the fix — that ordering is what interviewers listen for.",
                        "company_tags": ["phonepe", "amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Flipkart interviewer serializes your singleton instance to disk, deserializes it back, and asks: 'How many instances exist now?' — then: 'Fix it without switching to an enum.'",
                        "choices": [
                            "Still one — deserialization always reuses the existing instance",
                            "Two — deserialization bypasses the constructor and builds a fresh object; add a readResolve() method that returns the canonical instance",
                            "Zero — deserialization destroys the original instance",
                            "Two — and the only fix is to make the class implement Cloneable",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Java deserialization does not call constructors or go through getInstance() — it materializes a brand-new object, so you silently end up with two 'singletons'. A readResolve() method returning the existing instance makes deserialization hand back the canonical object instead. The enum singleton dodges this whole attack class, which is why interviewers steer you toward it.",
                        "company_tags": ["flipkart", "amazon", "paytm"],
                    },
                ],
            },
            {
                "slug": "oop-pattern-factory",
                "title": "Factory Patterns",
                "theory_md": """## Factory Patterns

Factories **decouple object creation from object use**: client code asks for
a product by name or type and never touches `new` / constructor details.
Three flavors form a ladder — know which rung you are on:

| | Simple Factory | Factory Method | Abstract Factory |
|---|---|---|---|
| Idea | One method with if/else picks the class | Subclasses decide which class to create | Creates *families* of related objects |
| Grows by | Adding another branch | Adding another subclass | Adding another family |
| Example | `make_shape("circle")` | `Dialog.create_button()` overridden per OS | `GUIFactory` making matching Button + Checkbox |

### Python: Simple Factory + Factory Method

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self): ...

class Circle(Shape):
    def draw(self): return "Drawing a circle"

class Square(Shape):
    def draw(self): return "Drawing a square"

# Simple Factory: one function, client passes a key
def make_shape(kind: str) -> Shape:
    if kind == "circle":
        return Circle()
    if kind == "square":
        return Square()
    raise ValueError(f"unknown shape: {kind}")

# Factory Method: subclasses override the creation step
class ShapeApp(ABC):
    @abstractmethod
    def make_shape(self) -> Shape: ...

    def render(self):
        print(self.make_shape().draw())

class CircleApp(ShapeApp):
    def make_shape(self): return Circle()

CircleApp().render()   # Drawing a circle
```

### Java: Abstract Factory with a Notification family

```java
interface Notifier { void send(String msg); }
class EmailNotifier implements Notifier {
    public void send(String m) { System.out.println("Email: " + m); }
}
class SMSNotifier implements Notifier {
    public void send(String m) { System.out.println("SMS: " + m); }
}

interface NotifierFactory { Notifier create(); }
class EmailFactory implements NotifierFactory {
    public Notifier create() { return new EmailNotifier(); }
}

// Client code never names EmailNotifier — swap the factory, swap the channel
class AlertService {
    private final NotifierFactory factory;
    AlertService(NotifierFactory f) { this.factory = f; }
    void alert(String msg) { factory.create().send(msg); }
}
```

### Interview traps

* **Simple Factory is not a GoF pattern** — it is an idiom. The GoF ones
  are Factory Method and Abstract Factory. Saying so earns points.
* Use **Abstract Factory** when products come in *matching families* (a
  Windows button must pair with a Windows checkbox, never a Mac one).
* Factories shine when construction is complex (parsing config, pooling,
  choosing subclasses) — for trivial `new` calls they are overkill.

**Takeaway:** Simple Factory picks by key, Factory Method lets subclasses
decide, Abstract Factory builds matching families — all so clients stop
caring how objects are born.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'Our checkout code calls new UpiProcessor() in twelve places. Next month we add cards, then wallets. What problem would introducing a factory solve here?'",
                        "choices": [
                            "They reduce the number of classes in the system",
                            "They decouple the client from the concrete classes being instantiated",
                            "They make object creation faster by caching constructors",
                            "They enforce that only one object of each type exists",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "The client asks for a product through an abstraction and never names the concrete class, so you can swap implementations (or add new ones) without touching client code. The last option describes Singleton, not Factory.",
                        "company_tags": ["tcs", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print?\n\ndef make(kind):\n    return {\"email\": \"E\", \"sms\": \"S\"}.get(kind, \"?\")\n\nprint(make(\"sms\") + make(\"push\") + make(\"email\"))",
                        "choices": [
                                       "KeyError",
                                       "sms pushemail",
                                       "SE?",
                                       "S?E",
                                   ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "The dict maps 'sms' to 'S' and 'email' to 'E'; the unknown key 'push' falls back to the default '?'. Concatenating gives 'S' + '?' + 'E'. This dict-dispatch is the Pythonic shape of a Simple Factory.",
                        "company_tags": ["cognizant", "swiggy"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Infosys interviewer circles your make_shape(kind) if/else chain on the board and says: 'Show me how Factory Method would restructure this — and in that version, who decides which concrete class gets created?'",
                        "choices": [
                            "Factory Method delegates the creation decision to subclasses via an overridden method",
                            "Factory Method creates exactly one object per program run",
                            "Factory Method only works with abstract classes, never interfaces",
                            "Factory Method requires the client to pass a string key",
                        ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "In Factory Method the abstract creator declares a factory method and each concrete subclass overrides it to instantiate its own product — the 'which class' decision moves from an if/else chain into the class hierarchy. Simple Factory keeps that decision in one centralized method.",
                        "company_tags": ["infosys", "razorpay"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "You are building a UI toolkit for Windows, macOS, and Linux. Each OS needs its own matching Button, Checkbox, and Scrollbar that must never be mixed. Which pattern fits?",
                        "choices": [
                                       "Singleton, one toolkit instance per OS",
                                       "Observer, so widgets update when the OS theme changes",
                                       "Abstract Factory, one concrete factory per OS producing its matching widget family",
                                       "Decorator, wrapping each widget per OS",
                                   ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "This is the textbook Abstract Factory scenario: families of related products (Button + Checkbox + Scrollbar) that must stay consistent within a family. One concrete factory per OS guarantees a Windows button never pairs with a macOS checkbox.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this Java print?\n\ninterface N { String id(); }\nclass E implements N { public String id(){ return \"email\"; } }\nclass S implements N { public String id(){ return \"sms\"; } }\nclass F {\n    static N create(boolean urgent){ return urgent ? new S() : new E(); }\n}\nSystem.out.println(F.create(false).id() + \"/\" + F.create(true).id());",
                        "choices": [
                            "sms/email",
                            "email/sms",
                            "E/S",
                            "It does not compile: ternary cannot return different types",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "create(false) takes the else branch and returns an E whose id() is 'email'; create(true) returns an S whose id() is 'sms'. The ternary is fine because both branches are subtypes of the declared return type N — a classic Simple Factory in Java.",
                        "company_tags": ["amazon", "phonepe"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Meta interviewer follows up: 'Your abstract factory ships Windows, macOS, and Linux widget families. Now product wants a brand-new Toggle widget on all three platforms. What's the catch?'",
                        "choices": [
                                       "It cannot create more than one object per factory",
                                       "Concrete factories cannot be tested in isolation",
                                       "It breaks encapsulation by exposing constructors publicly",
                                       "Adding a brand-new product type (e.g. a Toggle) forces changes to every concrete factory",
                                   ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "Abstract Factory makes adding new *families* easy but adding new *product kinds* hard: the abstract factory interface gains a method, and every concrete factory (Windows, macOS, Linux...) must implement it. This is the known trade-off to state when an interviewer asks 'what's the catch?'",
                        "company_tags": ["meta", "uber"],
                    },
                ],
            },
            {
                "slug": "oop-pattern-observer",
                "title": "Observer Pattern",
                "theory_md": """## Observer Pattern

The **Observer** defines a one-to-many dependency: when one object (the
**subject** / publisher) changes state, all its **observers** (subscribers)
are notified automatically. The subject never knows *who* is watching — it
only knows they implement the observer interface.

Everyday examples: a YouTube channel notifying subscribers of a new video,
a stock ticker updating dashboard widgets, Java Swing buttons firing
`ActionListener`s, a newsletter mailing list.

### Python: a tiny YouTube channel

```python
class Channel:                      # the subject
    def __init__(self, name):
        self.name = name
        self._subs = []

    def subscribe(self, user):
        self._subs.append(user)

    def unsubscribe(self, user):
        self._subs.remove(user)

    def upload(self, title):
        print(f"[{self.name}] uploaded: {title}")
        for sub in list(self._subs):        # copy: safe if someone unsubscribes mid-loop
            sub.notify(self.name, title)

class User:                         # the observer
    def __init__(self, name):
        self.name = name

    def notify(self, channel, title):
        print(f"  -> {self.name} got ping: new '{title}' on {channel}")

ch = Channel("CodeDaily")
ch.subscribe(User("Asha"))
ch.subscribe(User("Ravi"))
ch.upload("Observer Pattern in 10 min")
```

### Push vs pull

* **Push:** the subject sends the changed data along with the notification
  (`notify(title)`). Simple, but observers may receive data they ignore.
* **Pull:** the subject sends only "something changed"; observers query back
  for what they need. More flexible, slightly chattier.

### Java: listeners are observers

```java
button.addActionListener(e -> System.out.println("clicked!"));
```

`addActionListener` is `subscribe`, the button is the subject, and your
lambda is the observer. Recognizing this in an interview shows you see
patterns in real code, not just diagrams.

### Interview traps

* **Memory leaks:** observers that never unsubscribe keep the subject (and
  everything it references) alive. Always provide `unsubscribe`.
* **No ordering guarantee:** observers are notified in *some* order — never
  write logic that depends on subscriber A running before subscriber B.
* **Notification storms:** an observer that modifies the subject during
  `notify` can trigger infinite recursion. Guard or document reentrancy.

**Takeaway:** Observer = subscribe, change, notify — loose coupling between
event source and reactions, but always unsubscribe and never assume order.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'A stock-price feed must update a dashboard, a mobile alert, and a logger the moment a price changes — without the feed knowing who is listening. Which pattern fits, and what's its core idea?'",
                        "choices": [
                            "Define a one-to-many dependency so all dependents are notified automatically when a subject changes",
                            "Ensure only one instance of the subject class exists",
                            "Convert the interface of a class into one clients expect",
                            "Encapsulate interchangeable algorithms in separate classes",
                        ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "Observer's entire point is the one-to-many notify relationship: the subject changes state once, and every registered observer reacts without the subject knowing their concrete types. The other options describe Singleton, Adapter, and Strategy respectively.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print?\n\nclass Pub:\n    def __init__(self):\n        self.s = []\n    def sub(self, f):\n        self.s.append(f)\n    def fire(self, v):\n        for f in self.s:\n            f(v)\n\np = Pub()\np.sub(lambda x: print(\"A:\", x))\np.sub(lambda x: print(\"B:\", x * 2))\np.fire(5)",
                        "choices": [
                                       "A: 5",
                                       "B: 10\nA: 5",
                                       "A: 5\nB: 10",
                                       "TypeError: lambdas cannot be stored in a list",
                                   ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "fire(5) iterates subscribers in registration order: the first lambda prints 'A: 5', the second prints 'B: 10'. Lambdas are ordinary objects in Python, so storing them in a list is perfectly legal.",
                        "company_tags": ["infosys", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a Flipkart system-design round you're told: 'Our order service notifies inventory, billing, and notifications on every order event.' The interviewer asks: 'Would you push the order data along with the event, or just send a signal and let each team pull what it needs? What decides it?'",
                        "choices": [
                                       "Push uses threads while pull is single-threaded",
                                       "There is no difference; the terms are interchangeable",
                                       "Push notifies all observers, pull notifies only one",
                                       "Push sends the changed data with the notification; pull sends only a signal and observers query the subject",
                                   ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "Push is 'here is what changed' — the subject ships the data with the event. Pull is 'something changed, come and look' — observers fetch what they need. Pull is more flexible when observers care about different slices of state; push is simpler when everyone wants the same payload.",
                        "company_tags": ["accenture", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a long-running GUI app, widgets subscribe to a data model but are never unsubscribed when closed. What is the classic consequence?",
                        "choices": [
                            "The app crashes immediately with a null reference",
                            "Closed widgets stay reachable through the subscriber list, leaking memory",
                            "The model stops notifying the remaining live widgets",
                            "Subscribers are automatically garbage collected anyway",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "The subject holds a strong reference to every observer, so a closed-but-subscribed widget can never be garbage collected — and worse, it still receives notifications. This 'lapsed listener' leak is the most-asked Observer pitfall in interviews.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer asks: 'Point at one API in the Java standard library where the Observer pattern is hiding in plain sight — no UML, just real code.'",
                        "choices": [
                                       "A Swing JButton notifying registered ActionListeners on click",
                                       "java.util.ArrayList storing elements in order",
                                       "StringBuilder appending characters efficiently",
                                       "A private constructor preventing instantiation",
                                   ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "addActionListener is subscribe, the button is the subject, and each listener is an observer notified on the click event. Spotting the pattern inside a familiar API is exactly what interviewers probe for — patterns in the wild, not just UML boxes.",
                        "company_tags": ["google", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "During notification, one observer calls back into the subject and changes its state again, triggering a second notification round mid-loop. What is the key design concern?",
                        "choices": [
                                       "Observers must always run on separate threads",
                                       "The subject must delete all observers before any state change",
                                       "Reentrant updates can cause infinite notification loops; iterate over a snapshot and document reentrancy rules",
                                       "Pull-style notification is impossible in this situation",
                                   ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "If notify() mutates the subject, you get reentrant notification — potentially unbounded recursion or ConcurrentModification-style failures. Robust implementations notify over a copied snapshot of the subscriber list and clearly document whether observers may mutate the subject during callbacks.",
                        "company_tags": ["meta", "netflix"],
                    },
                ],
            },
            {
                "slug": "oop-pattern-strategy",
                "title": "Strategy Pattern",
                "theory_md": """## Strategy Pattern

The **Strategy** pattern defines a **family of interchangeable algorithms**,
encapsulates each one in its own class, and lets the client swap them at
runtime. Instead of a giant `if/elif/else` chain picking behavior, you pick
an *object* that *is* the behavior.

Classic cases: payment methods (UPI / card / wallet) at checkout, sorting
strategies, compression algorithms, route planning (fastest vs cheapest).

### Python: strategies as classes (and plain functions)

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount): ...

class UpiPay(PaymentStrategy):
    def pay(self, amount):
        return f"Paid Rs.{amount} via UPI"

class CardPay(PaymentStrategy):
    def pay(self, amount):
        return f"Paid Rs.{amount} via Card"

class Checkout:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy          # the algorithm is injected

    def complete(self, amount):
        return self.strategy.pay(amount)

print(Checkout(UpiPay()).complete(500))
# Paid Rs.500 via UPI
print(Checkout(CardPay()).complete(500))
# Paid Rs.500 via Card
```

In Python, functions themselves can be strategies — `sorted(items,
key=...)` is Strategy in the standard library. Recognizing that scores
points.

### Java: the classic interface version

```java
interface SortStrategy {
    void sort(int[] a);
}
class BubbleSort implements SortStrategy {
    public void sort(int[] a) { System.out.println("bubble sorting"); }
}
class QuickSort implements SortStrategy {
    public void sort(int[] a) { System.out.println("quick sorting"); }
}

class Sorter {
    private SortStrategy strategy;
    Sorter(SortStrategy s) { this.strategy = s; }
    void setStrategy(SortStrategy s) { this.strategy = s; }  // swap at runtime
    void run(int[] a) { strategy.sort(a); }
}
```

### Why it kills if-else chains

Without Strategy, `Checkout.complete()` grows a branch per payment method —
every new method edits tested code, violating the **Open/Closed Principle**
(open for extension, closed for modification). With Strategy, a new payment
method is a *new class*; `Checkout` never changes.

### Strategy vs State — the interview trap

| | Strategy | State |
|---|---|---|
| Who picks the behavior? | The **client** chooses and injects it | The **object itself** switches as its internal state changes |
| Switches at runtime? | Yes, but explicitly by the client | Yes, automatically on state transitions |
| Example | Payment method chosen at checkout | TCP connection: Closed -> Listening -> Established |

Same structure, different intent. Interviewers love this distinction.

**Takeaway:** Strategy turns "which algorithm?" from a branching decision
into a pluggable object — the client chooses, the context just delegates.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'Checkout supports UPI today; cards and wallets land next quarter, and product keeps reshuffling the list. How do you design it so adding a payment method never touches existing, tested code?'",
                        "choices": [
                                       "Guarantee a class has only one instance",
                                       "Notify many objects automatically when one object changes",
                                       "Add responsibilities to objects dynamically by wrapping them",
                                       "Define a family of interchangeable algorithms and let clients swap them at runtime",
                                   ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Strategy encapsulates each algorithm behind a common interface so the client can pick any of them interchangeably — even swapping mid-run. The distractors describe Singleton, Observer, and Decorator respectively.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print?\n\nclass Add:\n    def run(self, a, b): return a + b\nclass Mul:\n    def run(self, a, b): return a * b\n\nclass Calc:\n    def __init__(self, s): self.s = s\n    def go(self, a, b): return self.s.run(a, b)\n\nprint(Calc(Mul()).go(3, 4), Calc(Add()).go(3, 4))",
                        "choices": [
                            "7 12",
                            "12 7",
                            "12 12",
                            "TypeError",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "Calc delegates to whatever strategy it was constructed with: Mul gives 3*4=12, Add gives 3+4=7. The context never knows which algorithm it holds — that is the whole pattern in six lines.",
                        "company_tags": ["wipro", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer looks at your strategy-based checkout and asks: 'You replaced the if/elif chain with strategy classes — which SOLID principle did you just demonstrate, and why does it matter the day the next payment method arrives?'",
                        "choices": [
                                       "Open/Closed Principle",
                                       "Single Responsibility Principle",
                                       "Liskov Substitution Principle",
                                       "Interface Segregation Principle",
                                   ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "Open/Closed: the Checkout class is closed for modification (you never edit it to add a payment method) but open for extension (each new method is a new strategy class). The if-chain version forces you to modify tested code for every new method.",
                        "company_tags": ["amazon", "razorpay"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Google interviewer draws two identical-looking diagrams — a Context delegating to a behavior object — and says: 'One of these is Strategy, the other is State. In an interview answer, how do you tell them apart?'",
                        "choices": [
                                       "State uses inheritance while Strategy uses composition",
                                       "Strategy is only for sorting algorithms, State is only for network protocols",
                                       "In Strategy the client chooses the behavior; in State the object switches behavior itself as its internal state changes",
                                       "State requires a singleton context, Strategy forbids it",
                                   ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "Structurally they look alike (context delegating to a behavior object), but the intent differs: Strategy = client picks the algorithm; State = the object's own state machine drives transitions (e.g. a TCP connection moving from Listening to Established). Interviewers ask this to test depth beyond diagrams.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this Java print?\n\ninterface P { String go(); }\nclass U implements P { public String go(){ return \"UPI\"; } }\nclass C implements P { public String go(){ return \"CARD\"; } }\nclass K {\n    P p = new U();\n    void set(P x){ p = x; }\n    String run(){ return p.go(); }\n}\nK k = new K();\nk.set(new C());\nSystem.out.println(k.run());",
                        "choices": [
                                       "UPI",
                                       "UPI CARD",
                                       "NullPointerException",
                                       "CARD",
                                   ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "The context starts with the UPI strategy but set() swaps it for CARD before run() is called, so delegation hits C.go() and prints CARD. Runtime swapping of the strategy object is the pattern's signature move.",
                        "company_tags": ["flipkart", "phonepe"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What is the most honest drawback of the Strategy pattern to mention in an interview?",
                        "choices": [
                            "Strategies cannot be swapped at runtime under any circumstances",
                            "Clients must understand the differences between strategies to pick one, and many strategies mean many small classes",
                            "Strategy always breaks encapsulation of the context class",
                            "The pattern only works in dynamically typed languages",
                        ],
                        "answer_index": 1,
                        "difficulty": 9,
                        "explanation": "The trade-off is real: the client now bears the burden of choosing among strategies (it must know their trade-offs), and a rich algorithm family becomes a proliferation of tiny classes. Naming the cost — not just the benefit — is what separates a memorized answer from understanding.",
                        "company_tags": ["meta", "uber"],
                    },
                ],
            },
            {
                "slug": "oop-pattern-decorator",
                "title": "Decorator Pattern",
                "theory_md": """## Decorator Pattern

The **Decorator** attaches **additional responsibilities to an object
dynamically** by *wrapping* it in another object with the same interface.
The classic example: a coffee object wrapped in Milk, then Sugar, then
WhippedCream — each wrapper adds its cost and description.

Why not just subclass? Four condiments would need 2^4 = 16 subclasses
(plain, milk, sugar, milk+sugar, ...). Decorators compose at *runtime* with
a handful of small classes.

### Python: the GoF object decorator

```python
from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self): ...
    @abstractmethod
    def desc(self): ...

class SimpleCoffee(Coffee):
    def cost(self): return 50
    def desc(self): return "Simple coffee"

class CoffeeDecorator(Coffee):          # wraps another Coffee
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    def cost(self): return self._coffee.cost()
    def desc(self): return self._coffee.desc()

class Milk(CoffeeDecorator):
    def cost(self): return self._coffee.cost() + 10
    def desc(self): return self._coffee.desc() + ", milk"

class Sugar(CoffeeDecorator):
    def cost(self): return self._coffee.cost() + 5
    def desc(self): return self._coffee.desc() + ", sugar"

order = Sugar(Milk(SimpleCoffee()))
print(order.desc(), "= Rs." + str(order.cost()))
# Simple coffee, milk, sugar = Rs.65
```

### The Python `@` trap — interview favorite

Python's `@decorator` syntax (e.g. `@lru_cache`, `@property`) wraps
**functions**, adding behavior around calls. The GoF Decorator wraps
**objects**, adding behavior while preserving the interface. Same word,
related spirit (composition over inheritance), but **different mechanisms**.
Saying "they're the same thing" is the trap; explaining the distinction is
the win.

### Java: I/O streams are decorators

```java
// Each wrapper adds behavior; all are InputStreams
InputStream in = new BufferedInputStream(
                     new GzipInputStream(
                       new FileInputStream("data.gz")));
int b = in.read();   // buffered + decompressed + file-backed, transparently
```

`BufferedInputStream` doesn't care what it wraps — file, network, or
another decorator. That substitutability (same interface in and out) is the
pattern's essence.

### Watch the order

Decorators compose, but **order can matter**: `Sugar(Milk(coffee))` vs
`Milk(Sugar(coffee))` give the same cost here, but with behavior like
encryption-then-compression vs compression-then-encryption, swapping the
wrappers breaks everything.

**Takeaway:** Decorator = wrap to extend — runtime composition without the
subclass explosion; and Python's `@` is function-wrapping, not the GoF
object pattern.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'Our notification sender needs optional extras — retry logic, logging, rate-limiting — in any combination, without exploding into dozens of subclasses. What does the Decorator pattern let you do here?'",
                        "choices": [
                            "Attach additional responsibilities to an object dynamically by wrapping it",
                            "Ensure a class has exactly one instance",
                            "Convert one interface into another incompatible one",
                            "Define a family of interchangeable algorithms",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "Decorator wraps an object in another object sharing the same interface, layering on new behavior at runtime. The other options describe Singleton, Adapter, and Strategy.",
                        "company_tags": ["tcs", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print?\n\nclass D:\n    def __init__(self, w): self.w = w\n    def msg(self): return self.w.msg()\nclass Base:\n    def msg(self): return \"hi\"\nclass Loud(D):\n    def msg(self): return self.w.msg().upper() + \"!\"\n\nprint(Loud(Loud(Base())).msg())",
                        "choices": [
                                       "hi!",
                                       "HI!",
                                       "hi!!",
                                       "HI!!",
                                   ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "Decorators stack: the inner Loud turns 'hi' into 'HI!', then the outer Loud uppercases 'HI!' (unchanged) and appends another '!', giving 'HI!!'. Each wrapper delegates inward, then adds its own touch on the way out.",
                        "company_tags": ["zoho", "swiggy"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An interviewer asks: 'Is Python's @lru_cache an example of the Decorator design pattern?' What is the sharpest answer?",
                        "choices": [
                                       "Yes, it is exactly the GoF Decorator pattern",
                                       "No — Python does not support design patterns at all",
                                       "No — @decorators wrap functions to modify call behavior, while the GoF Decorator wraps objects preserving their interface; same name, different mechanism",
                                       "Yes, because both use the @ symbol",
                                   ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "This is the famous naming-overlap trap. Python's @ syntax composes function wrappers around calls; GoF Decorator composes object wrappers around an interface. They share the 'wrap to extend' spirit, but conflating them signals memorization without understanding.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer writes new BufferedInputStream(new GzipInputStream(new FileInputStream(...))) and asks: 'Convince me this single line is the Decorator pattern — what's being wrapped, and what does each layer add?'",
                        "choices": [
                            "BufferedInputStream inherits all file-reading logic from FileInputStream",
                            "Each wrapper shares the InputStream interface while transparently adding behavior, and wrappers can nest arbitrarily",
                            "It converts the file interface into a network interface",
                            "Only one BufferedInputStream can ever exist per JVM",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "The key is interface preservation: a BufferedInputStream IS an InputStream that happens to wrap another InputStream, adding buffering invisibly. Because input and output types match, decorators nest — buffering over decompression over file access — with zero changes to client code.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Meta interviewer asks: 'Your coffee shop has 4 optional add-ons. Why would subclassing be a disaster here — and what exactly does Decorator buy you instead?'",
                        "choices": [
                            "4 condiments would need 16 subclasses for every combination; decorators compose the same options at runtime with 4 small classes",
                            "Subclasses cannot add new methods in Python",
                            "Decorators use less memory than subclasses in all cases",
                            "Subclassing is deprecated in modern OOP",
                        ],
                        "answer_index": 0,
                        "difficulty": 8,
                        "explanation": "Subclassing multiplies: every on/off combination of 4 condiments is a distinct class (2^4 = 16), and a 5th condiment doubles it again. Decorators add linearly — one tiny wrapper per condiment — composed at runtime in any order and combination.",
                        "company_tags": ["meta", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Two decorators wrap a stream: Encrypt then Compress vs Compress then Encrypt. Why might swapping their order break the system?",
                        "choices": [
                                       "Decorator order never matters; both orders are always equivalent",
                                       "Java forbids stacking more than one decorator",
                                       "The outer decorator's constructor would fail to compile",
                                       "Compressed data encrypts poorly and encrypted data barely compresses — behavior depends on composition order, so order is part of the design",
                                   ],
                        "answer_index": 3,
                        "difficulty": 9,
                        "explanation": "Decorator composition is not always commutative. Encrypting first destroys the redundancy that compression exploits, so compress(encrypt(x)) is nearly useless while encrypt(compress(x)) is the correct pipeline. Order-sensitivity is a genuine design consideration with stacked decorators.",
                        "company_tags": ["netflix", "uber"],
                    },
                ],
            },
            {
                "slug": "oop-pattern-adapter",
                "title": "Adapter & Facade Patterns",
                "theory_md": """## Adapter & Facade Patterns

These two structural patterns are constantly confused. One line separates
them: **Adapter converts an interface; Facade simplifies one.**

### Adapter: making incompatible interfaces work together

Real-world analogy: your Indian 3-pin plug doesn't fit a European socket —
a **plug adapter** sits between them, converting without changing either
side. In code: you have a shiny new interface the client expects, and a
legacy class with a different method name/signature. The adapter wraps the
legacy class and translates calls.

```python
# Legacy library you cannot change
class OldPrinter:
    def print_legacy(self, text):
        print(f"[legacy] {text}")

# The interface your app expects
class Printer:
    def print(self, text):
        raise NotImplementedError

# Adapter: translates new-style calls into legacy calls
class PrinterAdapter(Printer):
    def __init__(self):
        self._old = OldPrinter()

    def print(self, text):
        self._old.print_legacy(text.upper())

def office_work(printer: Printer):      # client only knows the new interface
    printer.print("hello")

office_work(PrinterAdapter())   # [legacy] HELLO
```

Java's `Arrays.asList(array)` adapts an array to the `List` interface.
Chargers, HDMI-to-VGA dongles, JSON-to-XML translators — all adapters.

### Facade: a simple front door for a messy subsystem

A **Facade** provides one clean, high-level interface over a tangle of
subsystem classes. Starting a car: you turn one key; behind it, the facade
coordinates ignition, fuel pump, starter motor, and electronics.

```java
// Subsystem: messy details
class Engine { void start() { System.out.println("engine on"); } }
class FuelPump { void pump() { System.out.println("fuel flowing"); } }
class Lights { void on() { System.out.println("lights on"); } }

// Facade: one simple method for the common job
class CarFacade {
    private Engine engine = new Engine();
    private FuelPump pump = new FuelPump();
    private Lights lights = new Lights();

    public void startCar() {
        pump.pump();
        engine.start();
        lights.on();
    }
}

// Client: one call instead of three coordinated ones
new CarFacade().startCar();
```

### Adapter vs Facade — the comparison interviewers want

| | Adapter | Facade |
|---|---|---|
| Goal | **Convert** one existing interface into another | **Simplify** a whole subsystem behind one interface |
| Wraps | Usually one class | Many classes |
| Changes behavior? | No — only translates the interface | Defines a new, simpler workflow |
| Analogy | Plug adapter | Car ignition key |

A handy memory hook: **Adapter = translator, Facade = receptionist.**

**Takeaway:** Reach for Adapter when interfaces clash but the logic is
fine; reach for Facade when the logic is fine but using it takes ten
steps — convert vs simplify.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'We bought a vendor library with solid logic but method names nothing like our codebase expects — and we cannot modify their code. What is the Adapter pattern's job in this situation?'",
                        "choices": [
                                       "Simplify a complex subsystem behind one easy interface",
                                       "Ensure only one instance of a class exists",
                                       "Convert the interface of a class into another interface clients expect",
                                       "Notify multiple objects when one object changes state",
                                   ],
                        "answer_index": 2,
                        "difficulty": 3,
                        "explanation": "Adapter is a translator: it wraps a class with an incompatible interface and exposes the interface the client wants, without changing the wrapped class. Simplifying a subsystem is Facade's job.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Infosys interviewer asks: 'Give me a real-world object that works exactly like the Adapter pattern — something that lets two incompatible things work together without changing either side.'",
                        "choices": [
                            "A car ignition key that starts many subsystems at once",
                            "A travel plug adapter letting a 3-pin plug fit a foreign socket",
                            "A remote control with one button per device",
                            "A combination lock with a single dial",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "The plug adapter converts one physical interface into another without modifying either side — exactly what the software Adapter does between incompatible classes. The ignition key is the Facade analogy (one simple front for many subsystems).",
                        "company_tags": ["infosys", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print?\n\nclass Legacy:\n    def old_send(self, m): return \"LEG:\" + m\n\nclass Sender:\n    def send(self, m): raise NotImplementedError\n\nclass Adapt(Sender):\n    def __init__(self): self.l = Legacy()\n    def send(self, m): return self.l.old_send(m[::-1])\n\nprint(Adapt().send(\"abc\"))",
                        "choices": [
                                       "LEG:abc",
                                       "abc",
                                       "NotImplementedError",
                                       "LEG:cba",
                                   ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "Adapt.send reverses the message ('abc' -> 'cba') and delegates to the legacy old_send, which prefixes 'LEG:'. The client called the new interface; the adapter translated both the call and the data — the pattern in miniature.",
                        "company_tags": ["accenture", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Flipkart interviewer asks for the one-liner: 'I keep mixing up Adapter and Facade. Give me the single sentence that separates them forever.'",
                        "choices": [
                                       "Adapter converts an interface; Facade simplifies a subsystem",
                                       "Adapter simplifies a subsystem; Facade converts an interface",
                                       "Adapter works only in Java; Facade works only in Python",
                                       "There is no difference — they are two names for one pattern",
                                   ],
                        "answer_index": 0,
                        "difficulty": 6,
                        "explanation": "Adapter = translator between two existing interfaces (convert). Facade = receptionist giving one simple entry point to many subsystem classes (simplify). Mixing up the direction is the classic interview slip.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer asks: 'Is Java's Arrays.asList(array) an Adapter? Defend your answer — what's being wrapped, and what interface comes out the other side?'",
                        "choices": [
                                       "It copies the array into a faster data structure",
                                       "It sorts the array before returning",
                                       "It wraps a plain array and exposes it through the List interface without changing the array itself",
                                       "It guarantees only one list instance exists per array",
                                   ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "asList doesn't convert or copy the array — it returns a List view backed by the original array, translating List-method calls into array operations. Wrapping one interface to present another, leaving the original untouched, is precisely the Adapter pattern.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your app must integrate a legacy payment gateway whose API uses XML and oddly-named methods, while your codebase expects a clean `pay(amount)` interface. Which pattern and why?",
                        "choices": [
                            "Facade, because the gateway has too many classes",
                            "Adapter, because you must convert the gateway's incompatible interface into the one your code expects, without rewriting the gateway",
                            "Singleton, so only one gateway connection exists",
                            "Observer, so the gateway notifies you of payment status",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "This is the canonical Adapter scenario: a third-party/legacy component you can't change, speaking a different 'language' than your code. The adapter translates pay(amount) into the gateway's XML calls. Facade would apply if the gateway were already compatible but merely cumbersome to use.",
                        "company_tags": ["razorpay", "phonepe"],
                    },
                ],
            },
            {
                "slug": "oop-pattern-mvc",
                "title": "MVC, MVP & MVVM",
                "theory_md": """## MVC, MVP & MVVM

These three are **UI architecture patterns** — they answer one question:
where does the logic live between what the user sees and the data behind
it? Interviewers ask you to compare them, so learn the data flow, not just
the letters.

### The three, compared

| | MVC (Model-View-Controller) | MVP (Model-View-Presenter) | MVVM (Model-View-ViewModel) |
|---|---|---|---|
| Stands for | Model-View-Controller | Model-View-Presenter | Model-View-ViewModel |
| Who talks to whom | View <-> Controller, both touch Model | View <-> Presenter only; View is passive | View <-> ViewModel via **data binding** |
| View's smarts | View can observe Model directly | View is dumb; Presenter decides everything | View is declarative; binding syncs it |
| Testability | Moderate | Excellent (mock the View) | Excellent (test ViewModel logic) |
| Seen in | Django/Rails/Spring MVC | Classic Android apps | WPF, Angular, modern Android |

### Data flow in each

* **MVC:** User acts -> **Controller** handles input, updates the **Model**
  -> **View** reads the Model and re-renders. The View may observe the
  Model directly.
* **MVP:** User acts -> **View** forwards everything to the **Presenter**
  -> Presenter updates the Model, then tells the View exactly what to
  display. The View never touches the Model — it is deliberately passive,
  which makes it trivially mockable in tests.
* **MVVM:** User acts -> **View** updates bound properties -> **ViewModel**
  (plain logic, no UI references) updates the Model; **two-way data
  binding** keeps View and ViewModel in sync automatically.

### Where you'll meet them

* **Django** calls it MTV (Model-Template-View), but Template = View and
  Django's View = Controller. Saying "Django is MVC with renamed parts"
  shows real understanding.
* **Classic Android** activities stuffed with logic were mini-MVC; the
  community moved to **MVP** then **MVVM** (Architecture Components'
  `ViewModel` + LiveData) for testability.
* **Angular/React:** component + service layers echo MVVM/MVC thinking.

### Interview traps

* "Which is best?" is a trap — answer with trade-offs: MVP/MVVM win on
  testability; MVC is simpler for small apps; MVVM needs binding
  infrastructure.
* **Massive ViewModel / Massive View Controller** is the real-world
  failure mode: the pattern doesn't help if you dump all logic in one
  layer. Name the layers' jobs crisply: Model = data + rules, View =
  pixels, Controller/Presenter/ViewModel = the in-between.

### Python sketch: the same separation of concerns

```python
class Model:                        # data + rules, knows nothing about UI
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item.strip().title())

class View:                         # pixels only
    def show(self, items):
        for i in items:
            print(f"- {i}")

class Controller:                   # input handling + coordination
    def __init__(self):
        self.model = Model()
        self.view = View()

    def add_item(self, raw):
        self.model.add(raw)         # update the model...
        self.view.show(self.model.items)  # ...then refresh the view

app = Controller()
app.add_item("  apples ")
# - Apples
```

### Java sketch: MVP's passive view

```java
interface LoginView {
    void showError(String msg);
    void goHome();
}

class LoginPresenter {
    private final LoginView view;
    LoginPresenter(LoginView view) { this.view = view; }

    void onLogin(String user, String pass) {
        if (user.isEmpty()) view.showError("Enter username");
        else view.goHome();   // the view is dumb: the presenter decides everything
    }
}
```

**Takeaway:** MVC lets View and Controller share Model access, MVP makes
the View passive behind a Presenter, MVVM syncs View and ViewModel with
binding — same goal (separate UI from logic), different data flow.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer opens with: 'Everyone drops the term MVC. Before we go further — what do the three letters actually stand for, and what job does each part do?'",
                        "choices": [
                            "Module-View-Component",
                            "Model-View-Controller",
                            "Model-Variable-Constant",
                            "Method-View-Callback",
                        ],
                        "answer_index": 1,
                        "difficulty": 3,
                        "explanation": "Model (data + business rules), View (what the user sees), Controller (handles input and coordinates). The other expansions are invented — interviewers sometimes float them to check you're not guessing.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a Wipro interview you're sketching MVC for a to-do app when the interviewer asks: 'The user clicks Add. Which component hears about it first — and what does it do with it?'",
                        "choices": [
                            "The Controller — it receives input, updates the Model, and selects the View",
                            "The Model — it validates all input directly",
                            "The View — it both renders and processes all input",
                            "The database — input bypasses the application layers",
                        ],
                        "answer_index": 0,
                        "difficulty": 4,
                        "explanation": "The Controller is the input-handling layer: it interprets the user's action, mutates the Model accordingly, and picks the View to render the result. The Model stays UI-ignorant and the View stays logic-light.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Swiggy interviewer asks: 'Our Android team moved from MVC to MVP and suddenly the whole login flow became unit-testable. What single change made that possible?'",
                        "choices": [
                                       "MVP has no Model layer at all",
                                       "MVP merges the View and Controller into one class",
                                       "MVP can only be used for mobile apps",
                                       "In MVP the View is passive — it never touches the Model and the Presenter mediates everything",
                                   ],
                        "answer_index": 3,
                        "difficulty": 5,
                        "explanation": "MVP's defining move is the passive View: all logic lives in the Presenter, which fetches from the Model and commands the View what to show. Because the View is dumb, you can mock it and unit-test the entire Presenter — MVP's big selling point.",
                        "company_tags": ["cognizant", "swiggy"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Microsoft interviewer asks: 'In MVVM I change a property and the UI updates itself — no refresh calls anywhere. What mechanism makes that magic happen?'",
                        "choices": [
                                       "The View directly executes SQL against the Model",
                                       "Controllers are replaced with database triggers",
                                       "Two-way data binding keeps the View and ViewModel automatically in sync",
                                       "The ViewModel inherits from the View class",
                                   ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "MVVM's hallmark is declarative data binding: the View binds to ViewModel properties, and changes propagate both ways without imperative update code. The ViewModel holds presentation logic but zero UI references, so it's cleanly unit-testable.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Amazon interviewer grins: 'Django insists it's MTV, not MVC. Settle it — map each MTV part onto MVC, or defend why the mapping fails.'",
                        "choices": [
                            "It doesn't map at all; MTV is unrelated to MVC",
                            "Django's Template is the View (presentation) and Django's View is the Controller (request handling logic)",
                            "Django's Model is the Controller and Template is the Model",
                            "MTV is just MVC with the letters rearranged randomly",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "The mapping is Template = View (what gets rendered) and Django View = Controller (the callable that handles the request and picks the template). Knowing this mapping — rather than insisting 'Django is not MVC' — demonstrates you understand the pattern's roles, not just its acronym.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A team complains their MVVM app has a 2000-line ViewModel doing networking, formatting, navigation, and validation. What is the correct diagnosis?",
                        "choices": [
                                       "This is the 'Massive ViewModel' anti-pattern — the pattern's layering failed because responsibilities weren't separated, not because MVVM itself is broken",
                                       "MVVM is the wrong pattern; only MVC scales to large apps",
                                       "Data binding cannot handle more than a few properties",
                                       "ViewModels must never contain any logic by definition",
                                   ],
                        "answer_index": 0,
                        "difficulty": 8,
                        "explanation": "Patterns assign responsibilities; they don't enforce them. A bloated ViewModel means networking/formatting/navigation leaked into one layer instead of being split across repositories, use-cases, and formatters. The fix is honoring the separation the pattern promises, not abandoning the pattern.",
                        "company_tags": ["meta", "netflix"],
                    },
                ],
            },
        ],
    },
    {
        "slug": "oop-practice",
        "name": "OOP in Practice",
        "description": (
            "OOP where interviews actually probe it: Python's dunder methods, "
            "properties, dataclasses and MRO; Java's packages, final, records "
            "and sealed classes; C++ RAII, the Rule of 3/5/0 and smart "
            "pointers; low-level design interviews via a parking-lot "
            "walkthrough; and a rapid-fire revision sheet of the 20 most-asked "
            "OOP questions."
        ),
        "lessons": [
            {
                "slug": "oop-python-deep",
                "title": "OOP in Python: Dunder, Dataclasses, Properties",
                "theory_md": """## OOP in Python: Dunder, Dataclasses, Properties

Python's OOP feels informal until interviews probe the machinery. Four
areas come up again and again: **dunder (double-underscore) methods**,
**properties**, **dataclasses**, and **multiple inheritance / MRO**.

### Dunder methods: the hooks behind the syntax

Dunders let your objects speak Python's native syntax:

```python
class Money:
    def __init__(self, paise):
        self.paise = paise
    def __str__(self):                    # str(obj), print(obj): human-readable
        return f"Rs.{self.paise/100:.2f}"
    def __repr__(self):                   # repr(obj): unambiguous, for debugging
        return f"Money({self.paise})"
    def __eq__(self, other):              # == operator
        return isinstance(other, Money) and self.paise == other.paise
    def __add__(self, other):             # + operator
        return Money(self.paise + other.paise)

m = Money(250) + Money(100)
print(m)            # Rs.3.50   (uses __str__)
print(repr(m))      # Money(350) (uses __repr__)
print(m == Money(350))  # True
```

**`__str__` vs `__repr__`:** `__str__` is for users (readable), `__repr__`
is for developers (unambiguous — ideally `eval(repr(x))` rebuilds `x`).
Trap: defining `__eq__` without `__hash__` makes instances **unhashable**
(Python sets `__hash__` to None), so they can't go in sets/dicts.

### @property: managed attributes

```python
class Temp:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero!")
        self._celsius = value

t = Temp(25)
t.celsius = -300   # ValueError: below absolute zero!
```

Callers use plain attribute syntax (`t.celsius = 30`) while you keep
validation — encapsulation without ugly getters/setters.

### Dataclasses: boilerplate killers

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    roll: int
    cgpa: float = 0.0     # default allowed

s1 = Student("Asha", 7, 9.1)
s2 = Student("Asha", 7, 9.1)
print(s1 == s2)   # True — __eq__ auto-generated
print(s1)         # Student(name='Asha', roll=7, cgpa=9.1) — __repr__ free
```

You get `__init__`, `__repr__`, and `__eq__` for free. Use
`@dataclass(frozen=True)` for immutable value objects.

### Multiple inheritance & MRO

```python
class A:
    def who(self): return "A"
class B(A):
    def who(self): return "B"
class C(A):
    def who(self): return "C"
class D(B, C):   # diamond!
    pass

print(D().who())              # B
print([c.__name__ for c in D.__mro__])
# ['D', 'B', 'C', 'A', 'object']
```

Python linearizes the hierarchy with the **C3 algorithm** — depth-first,
left-to-right, no class twice. `D.__mro__` *is* the answer to "which
method wins?" Never guess; read the MRO.

### abc: real abstract classes

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...

Shape()   # TypeError: Can't instantiate abstract class
```

Unlike informal "don't instantiate me" conventions, `ABC` + `@abstractmethod`
is *enforced* — subclasses must implement every abstract method.

### Java parallel: the same ideas, Java's way

```java
class Temp {
    private double celsius;
    public double getCelsius() { return celsius; }   // like a @property getter
    public void setCelsius(double v) {               // like a @property setter
        if (v < -273.15) throw new IllegalArgumentException("below absolute zero!");
        celsius = v;
    }
}

record Point(int x, int y) {}   // Java's answer to @dataclass: free equals/repr
```

**Takeaway:** Dunders hook syntax, `@property` guards attributes,
dataclasses erase boilerplate, C3 MRO settles every inheritance dispute.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'Your Money class prints nicely with print(m) but shows garbage in the debugger. Which two dunder methods are involved — and what job does each one do?'",
                        "choices": [
                                       "There is no difference; they are aliases",
                                       "__repr__ is for users and __str__ is for logging",
                                       "__str__ is called by repr() and __repr__ by str()",
                                       "__str__ is a human-readable display for users; __repr__ is an unambiguous representation for developers/debugging",
                                   ],
                        "answer_index": 3,
                        "difficulty": 3,
                        "explanation": "__str__ powers print()/str() and should be pleasant to read; __repr__ powers repr() and should ideally be unambiguous (often looking like a constructor call). The convention 'str for users, repr for developers' is exactly what interviewers want to hear.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print?\n\nclass Box:\n    def __init__(self):\n        self._v = 0\n    @property\n    def v(self):\n        return self._v\n    @v.setter\n    def v(self, x):\n        self._v = x * 2\n\nb = Box()\nb.v = 21\nprint(b.v)",
                        "choices": [
                                       "21",
                                       "0",
                                       "42",
                                       "AttributeError",
                                   ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "b.v = 21 invokes the setter, which stores 21 * 2 = 42; reading b.v then invokes the getter returning 42. The caller used plain attribute syntax while the setter quietly transformed the value — the whole point of @property.",
                        "company_tags": ["wipro", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print?\n\nfrom dataclasses import dataclass\n\n@dataclass\nclass P:\n    x: int\n    y: int = 5\n\nprint(P(1) == P(1, 5), P(1))",
                        "choices": [
                                       "True P(x=1, y=5)",
                                       "False P(x=1, y=5)",
                                       "True <P object>",
                                       "TypeError: missing y",
                                   ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "Dataclasses auto-generate __eq__ comparing all fields, so P(1) (y defaults to 5) equals P(1, 5). They also auto-generate a readable __repr__, giving P(x=1, y=5). Both are free boilerplate wins.",
                        "company_tags": ["accenture", "swiggy"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print?\n\nclass A:\n    def f(self): return \"A\"\nclass B(A):\n    def f(self): return \"B\"\nclass C(A):\n    def f(self): return \"C\"\nclass D(B, C):\n    pass\nprint(D().f())",
                        "choices": [
                            "A",
                            "B",
                            "C",
                            "TypeError: ambiguous inheritance",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "Python's C3 linearization gives D -> B -> C -> A -> object, so B.f wins — depth-first, left-to-right. Python resolves the diamond deterministically instead of erroring; D.__mro__ lets you verify the exact order.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Microsoft interviewer points at this snippet and asks: 'Can I actually create an S() here — and what exactly stops me, if anything?\n\nfrom abc import ABC, abstractmethod\nclass S(ABC):\n    @abstractmethod\n    def area(self): ...\nprint(S())",
                        "choices": [
                                       "It creates an S instance; abstractmethod is only documentation",
                                       "It prints None",
                                       "It works only if area has a body",
                                       "TypeError: Can't instantiate abstract class S with abstract method area",
                                   ],
                        "answer_index": 3,
                        "difficulty": 7,
                        "explanation": "ABC + @abstractmethod is enforced by the interpreter: instantiating a class with unimplemented abstract methods raises TypeError. Any concrete subclass must override area() before it can be instantiated.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Uber interviewer asks: 'You defined __eq__ on your class, and now instances mysteriously can't be used as dict keys. What did Python do behind your back — and why?'",
                        "choices": [
                                       "Nothing breaks; Python synthesizes a matching __hash__",
                                       "== stops working for the class",
                                       "Instances become unhashable (can't go in sets or be dict keys) because Python sets __hash__ to None when __eq__ is defined",
                                       "The class can no longer be subclassed",
                                   ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "Python's rule: defining __eq__ without __hash__ sets __hash__ to None, making instances unhashable. The rationale is sound — equal objects must hash equally, and a default identity hash would violate that for a value-based __eq__. Fix it by defining __hash__ explicitly or using @dataclass(frozen=True)/eq=False as appropriate.",
                        "company_tags": ["meta", "uber"],
                    },
                ],
            },
            {
                "slug": "oop-java-deep",
                "title": "OOP in Java: Packages, final, Records",
                "theory_md": """## OOP in Java: Packages, final, Records

Java interviews go beyond "what is polymorphism" into language mechanics:
**packages and access levels**, the three faces of **`final`**, **records**,
**sealed classes**, and **enums with behavior**.

### Packages & access control

```java
package com.skillforge.billing;   // groups related classes, avoids name clashes

public class Invoice {
    public String id;          // visible everywhere
    protected double total;    // package + subclasses
    double tax;                // package-private (default): package only!
    private String secret;     // this class only
}
```

The trap is the **default (no modifier)**: it is *package-private*, not
public. Least privilege wins — start private, widen only as needed.

### final: three meanings, one keyword

```java
final double PI = 3.14159;   // 1) final variable: cannot be reassigned
// PI = 3.14;                // compile error!

class Base {
    final void audit() { }   // 2) final method: cannot be overridden
}

final class Config { }       // 3) final class: cannot be extended
// class MyConfig extends Config { }  // compile error!
```

Note: `final` on a *reference* freezes the reference, not the object —
a `final List` can't point elsewhere but its contents can still change.
`String` is final, which is why nobody can subclass and subvert it.

### Records (Java 16+): data carriers without boilerplate

```java
record Point(int x, int y) { }

// The compiler generates: constructor, x()/y() accessors,
// equals(), hashCode(), toString()
Point p1 = new Point(3, 4);
Point p2 = new Point(3, 4);
System.out.println(p1);          // Point[x=3, y=4]
System.out.println(p1.equals(p2)); // true
```

Records are implicitly final and immutable-ish — perfect for DTOs, API
responses, and map keys. Interview line: "a record is a transparent,
shallowly-immutable data carrier."

### Sealed classes: controlled inheritance

```java
sealed class Payment permits UpiPayment, CardPayment { }
final class UpiPayment extends Payment { }
final class CardPayment extends Payment { }
// class CashPayment extends Payment { }  // compile error: not permitted
```

Sealed classes say *exactly who* may extend them — the compiler then knows
every subtype, so `switch` expressions over them can be exhaustive without
a default branch.

### Enums with behavior

```java
enum DayType {
    WEEKDAY("Work hard"), WEEKEND("Rest well");

    private final String motto;
    DayType(String motto) { this.motto = motto; }  // enums CAN have constructors
    public String motto() { return motto; }
}
System.out.println(DayType.WEEKEND.motto());  // Rest well
```

Java enums are full classes — fields, constructors, methods. If an
interviewer asks "are enums just named ints?" (as in C), the answer is an
emphatic no.

### Python parallel: enums and data carriers

```python
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class Point:            # Python's answer to a Java record
    x: int
    y: int

class DayType(Enum):    # like Java enums, these are real objects, not ints
    WEEKDAY = "Work hard"
    WEEKEND = "Rest well"

print(Point(2, 3) == Point(2, 3))  # True, like a record
print(DayType.WEEKEND.value)       # Rest well
```

**Takeaway:** Default access is package-private, `final` freezes
reassignment/overriding/extension separately, records kill DTO boilerplate,
sealed classes whitelist subclasses, and enums are real classes.
""",
                "difficulty_min": 3,
                "difficulty_max": 8,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'You declared a field with no access modifier at all. A teammate in a different package tries to use it — what happens, and what's that default level actually called?'",
                        "choices": [
                                       "package-private — visible only within the same package",
                                       "public — visible everywhere",
                                       "private — visible only in the class",
                                       "protected — visible to subclasses everywhere",
                                   ],
                        "answer_index": 0,
                        "difficulty": 3,
                        "explanation": "No modifier means package-private (sometimes called 'default'): accessible within the same package only. It is a perennial interview trap because many developers assume 'no modifier = public'.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Infosys interviewer writes final List<String> names = new ArrayList<>(); and asks: 'I just called names.add(\"Asha\") and it worked fine. So what did final actually freeze here?'",
                        "choices": [
                            "The variable becomes a compile-time constant that can never change in any way",
                            "The reference cannot be reassigned, but the object it points to may still be mutated",
                            "The variable is automatically thread-safe",
                            "The variable is stored in read-only memory",
                        ],
                        "answer_index": 1,
                        "difficulty": 4,
                        "explanation": "final freezes the reference, not the object: `final List<String> l = new ArrayList<>()` can't be repointed, but l.add(...) still works. True immutability needs an immutable class, not just a final reference.",
                        "company_tags": ["infosys", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print? (Java 16+)\n\nrecord Point(int x, int y) {}\nPoint a = new Point(2, 3);\nPoint b = new Point(2, 3);\nSystem.out.println(a.equals(b) + \" \" + a);",
                        "choices": [
                                       "false Point@1a2b3c",
                                       "true Point(2, 3)",
                                       "true Point[x=2, y=3]",
                                       "It does not compile: records cannot override equals",
                                   ],
                        "answer_index": 2,
                        "difficulty": 5,
                        "explanation": "Records auto-generate value-based equals()/hashCode() and a readable toString() of the form Point[x=2, y=3]. That's the entire appeal: DTO semantics with zero boilerplate.",
                        "company_tags": ["cognizant", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer asks: 'final on a method, final on a class — same thing or different? Give me the precise difference and one real-world example of each.'",
                        "choices": [
                                       "There is no difference between the two",
                                       "A final method cannot be called; a final class cannot be instantiated",
                                       "Final methods are implicitly static; final classes are implicitly abstract",
                                       "A final method cannot be overridden; a final class cannot be extended",
                                   ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "final on a method locks the implementation against overriding (used for security-sensitive or performance-critical methods); final on a class locks the hierarchy (String is final so its behavior can't be subverted by subclasses).",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Flipkart interviewer asks: 'Why did Java's designers make it impossible for anyone to subclass String? I want the real engineering reason — not just the keyword.'",
                        "choices": [
                            "String is declared final, so subclassing is forbidden",
                            "String's constructor is private",
                            "The JVM hard-codes a check specifically for String",
                            "String is an interface, not a class",
                        ],
                        "answer_index": 0,
                        "difficulty": 7,
                        "explanation": "String is a final class — no subclass can alter its immutability or equality contract, which the JVM, security manager, and string pool all depend on. It's the canonical real-world example of final classes.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Meta interviewer asks: 'You sealed class P so only A and B may extend it. What superpower does that give the compiler that an open hierarchy can never offer?'",
                        "choices": [
                            "It can skip generating bytecode for P entirely",
                            "It knows the complete set of subtypes, enabling exhaustive switch expressions without a default branch",
                            "A and B automatically become singletons",
                            "P's methods become implicitly synchronized",
                        ],
                        "answer_index": 1,
                        "difficulty": 8,
                        "explanation": "Sealing closes the hierarchy: the compiler enumerates every permitted subtype, so a switch over P can be proven exhaustive at compile time. This is the modern answer to the fragile 'catch-all default' in type switches.",
                        "company_tags": ["meta", "uber"],
                    },
                ],
            },
            {
                "slug": "oop-cpp-deep",
                "title": "OOP in C++: RAII, Rule of 3/5, Smart Pointers",
                "theory_md": """## OOP in C++: RAII, Rule of 3/5, Smart Pointers

C++ interviews orbit one idea: **who owns the memory?** Three topics prove
you get it — **RAII**, the **Rule of 3/5/0**, and **smart pointers** — plus
the eternal **virtual destructor** question.

### RAII: Resource Acquisition Is Initialization

Tie every resource's lifetime to an object's lifetime: acquire in the
constructor, release in the destructor. Stack unwinding then guarantees
cleanup — even when exceptions fly.

```cpp
#include <fstream>
#include <string>

void write_log(const std::string& msg) {
    std::ofstream f("app.log", std::ios::app);  // acquire in ctor
    f << msg << "\\n";
}   // destructor closes the file HERE — no matter how we exit
```

No `finally` blocks, no forgotten `close()` calls. `std::lock_guard`,
`std::vector`, `std::string` are all RAII types.

### Rule of Three / Five / Zero

If your class manages a raw resource (owning pointer, file handle), the
compiler-generated copies will **shallow-copy** it — two objects, one
resource, double-free crash. So:

* **Rule of 3:** if you define any of {destructor, copy constructor, copy
  assignment}, define all three.
* **Rule of 5:** add {move constructor, move assignment} (C++11) to steal
  resources cheaply instead of copying.
* **Rule of 0:** best of all — hold resources via RAII types (`std::string`,
  `std::vector`, smart pointers) and define *none* of them.

### Smart pointers: ownership made explicit

```cpp
#include <memory>

auto u = std::make_unique<int>(42);   // unique_ptr: SOLE owner, non-copyable
// auto u2 = u;                       // compile error — ownership can't split
auto u3 = std::move(u);               // transfer ownership explicitly

auto s1 = std::make_shared<int>(7);   // shared_ptr: shared ownership, ref-counted
auto s2 = s1;                         // ref count = 2, freed when last one dies

std::weak_ptr<int> w = s1;            // weak_ptr: observes WITHOUT owning
// w.lock() gives a temporary shared_ptr if the object still lives
```

**The cycle trap:** two `shared_ptr`s pointing at each other keep each
other's ref-count above zero forever — a leak. Break cycles with
`weak_ptr` (classic parent/child: parent owns child via `shared_ptr`,
child refers back via `weak_ptr`).

### The virtual destructor — non-negotiable

```cpp
class Base {
public:
    virtual ~Base() = default;   // ALWAYS virtual if the class has virtuals
    virtual void run() = 0;
};

class Child : public Base {
    int* buf;
public:
    Child() : buf(new int[100]) {}
    ~Child() override { delete[] buf; }
    void run() override {}
};

Base* p = new Child();
delete p;   // calls ~Child() THEN ~Base() — correct cleanup
```

Without `virtual ~Base()`, `delete p` calls **only** `~Base()` — the
child's buffer leaks and behavior is undefined. Interviewers ask this
constantly: *"when do you need a virtual destructor?"* → whenever a class
is meant to be deleted through a base pointer (i.e., has any virtual
function).

### Python parallel: RAII via context managers

```python
class ManagedFile:
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        self.f = open(self.path, "a")   # acquire, like a constructor
        return self.f
    def __exit__(self, *exc):
        self.f.close()                  # release, like a destructor

with ManagedFile("app.log") as f:       # cleanup guaranteed on block exit
    f.write("hello\n")
```

**Takeaway:** RAII ties resources to lifetimes, Rule of 0 beats Rule of 5,
`unique_ptr` = sole owner / `shared_ptr` = shared / `weak_ptr` = cycle
breaker, and destructors of polymorphic bases must be virtual.
""",
                "difficulty_min": 4,
                "difficulty_max": 9,
                "is_important": False,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer asks: 'Your function opens a file, then throws halfway through. C++ has no finally blocks — so how does RAII guarantee that file still gets closed?'",
                        "choices": [
                                       "All objects must be allocated on the heap",
                                       "Every class must define all five special member functions",
                                       "Resource lifetime is tied to object lifetime: acquire in the constructor, release in the destructor",
                                       "Resources are shared globally to avoid duplication",
                                   ],
                        "answer_index": 2,
                        "difficulty": 4,
                        "explanation": "RAII makes cleanup automatic: when the object dies (scope exit, stack unwinding during exceptions), its destructor releases the resource. std::vector, std::lock_guard, and smart pointers are all RAII types built on this idea.",
                        "company_tags": ["tcs", "infosys"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Wipro interviewer reviews your class — custom destructor, raw owning pointer, no copy operations — and asks: 'Ship it? Tell me what the Rule of Three says will happen the first time someone copies this object.'",
                        "choices": [
                                       "You must also define the copy constructor and copy assignment — otherwise copies shallow-copy the pointer and cause double-free",
                                       "The compiler will refuse to compile the class",
                                       "The destructor alone is sufficient; copies are automatically deep",
                                       "Raw pointers are banned by the Rule of Three",
                                   ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "The default copy operations copy the pointer value, not the pointee — so two objects end up owning one allocation and both destructors free it. Defining all three (destructor, copy ctor, copy assign) — or better, following the Rule of Zero with RAII members — fixes it.",
                        "company_tags": ["wipro", "accenture"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print?\n\n#include <memory>\n#include <iostream>\nint main() {\n    auto u = std::make_unique<int>(10);\n    auto v = std::move(u);\n    std::cout << (u == nullptr) << *v;\n}",
                        "choices": [
                            "010",
                            "110",
                            "1010",
                            "It does not compile",
                        ],
                        "answer_index": 1,
                        "difficulty": 6,
                        "explanation": "std::move transfers unique_ptr ownership: u becomes null (so u == nullptr is 1, printed as '1') and v now owns the int, so *v is 10. Copying a unique_ptr is a compile error — moving is the only transfer.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Google interviewer asks the classic: 'I delete a Derived object through a Base pointer, and your base destructor isn't virtual. Walk me through exactly what goes wrong.'",
                        "choices": [
                                       "To allow the class to be instantiated",
                                       "Virtual destructors make construction faster",
                                       "It is required for all classes, polymorphic or not",
                                       "So that `delete` through a base pointer runs the derived destructor first — otherwise only the base destructor runs and derived resources leak (undefined behavior)",
                                   ],
                        "answer_index": 3,
                        "difficulty": 7,
                        "explanation": "Deleting a Derived through a Base* with a non-virtual destructor calls only ~Base(): derived members never get destroyed — a leak at best, undefined behavior formally. The rule of thumb: if a class has any virtual function, its destructor must be virtual.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Two objects hold std::shared_ptr to each other. What happens, and what is the fix?",
                        "choices": [
                                       "Nothing — shared_ptr detects cycles automatically",
                                       "The program crashes immediately with a null dereference",
                                       "Their reference counts never reach zero, leaking both; break the cycle by making one link a std::weak_ptr",
                                       "shared_ptr cannot point to user-defined types",
                                   ],
                        "answer_index": 2,
                        "difficulty": 8,
                        "explanation": "A reference cycle keeps both counts ≥ 1 forever, so neither object is destroyed — the classic shared_ptr leak. std::weak_ptr observes without owning (it doesn't increment the count), so the standard fix is parent-owns-child via shared_ptr, child-points-back via weak_ptr.",
                        "company_tags": ["meta", "uber"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Netflix interviewer asks: 'Rule of Three, Rule of Five — what did C++11 actually add, and honestly, what's the modern answer you'd use in new code today?'",
                        "choices": [
                                       "It adds the move constructor and move assignment for cheap resource stealing; the Rule of Zero — using RAII member types so you define none of them — is preferred",
                                       "It adds two more copy constructors; there is no alternative",
                                       "It adds virtual destructors; the alternative is raw new/delete",
                                       "It bans move semantics entirely",
                                   ],
                        "answer_index": 0,
                        "difficulty": 9,
                        "explanation": "C++11 move semantics let you transfer (not copy) resources, so the Rule of Three grew into the Rule of Five. But the modern guidance is the Rule of Zero: compose your class from std::string, std::vector, and smart pointers, and the compiler-generated operations are all correct automatically.",
                        "company_tags": ["netflix", "phonepe"],
                    },
                ],
            },
            {
                "slug": "oop-lld-basics",
                "title": "LLD Basics: Designing a Parking Lot",
                "theory_md": """## LLD Basics: Designing a Parking Lot

Low-Level Design interviews ("design a parking lot / elevator / splitwise")
test whether you can turn fuzzy requirements into clean classes in 35
minutes. Interviewers score your **process** as much as your diagram. Use
this four-step method every time:

### Step 1 — Clarify requirements (ask, don't assume)

* What vehicle types? (bike, car, truck — different spot sizes)
* How many floors / spots? Multiple entry-exit gates?
* Pricing model? (hourly, per vehicle type — and who computes it?)
* Ticketing: paper token, QR, app-based?
* Concurrency: two cars entering different gates simultaneously?

Asking these first signals senior thinking. Jumping straight to classes
signals the opposite.

### Step 2 — Identify entities (nouns become classes)

ParkingLot, Floor, Spot, Vehicle, Ticket, Gate (Entry/Exit), Payment,
PricingStrategy. Verbs become methods: `park(vehicle)`, `unpark(ticket)`,
`calculate_fee(ticket)`.

### Step 3 — Relationships & the class sketch

```
ParkingLot 1 ---- * Floor        (composition: floors die with the lot)
Floor      1 ---- * Spot         (composition)
Spot       * ---- 1 VehicleType  (spot fits certain vehicle kinds)
Vehicle    1 ---- 1 Ticket       (a parked vehicle holds a ticket)
Ticket     * ---- 1 PricingStrategy  (strategy picks the fee rule)
EntryGate  * ---- 1 ParkingLot   (gates delegate spot allocation)
```

Key design moves to narrate aloud:

* **Spot allocation is a Strategy**: `NearestSpotStrategy`,
  `RandomSpotStrategy` — the lot shouldn't hard-code "nearest".
* **Pricing is a Strategy too**: `HourlyPricing`, `FlatPricing` per vehicle
  type. Never bury fee math inside `Ticket`.
* **VehicleType as an enum** (BIKE, CAR, TRUCK); a Spot declares which types
  it accepts — a bike can take a car spot, never the reverse.

### Step 4 — Walk a flow & name extensibility points

"Car arrives at EntryGate -> gate asks ParkingLot for a Spot (strategy) ->
Spot marked occupied, Ticket issued with entry time -> at ExitGate, fee =
PricingStrategy(ticket), Payment processed, Spot freed."

Then volunteer extensibility: EV charging spots (new Spot subtype),
dynamic surge pricing (new PricingStrategy), reservations (new entity,
no existing changes) — this is the Open/Closed Principle in action.

### Concurrency — the follow-up they always ask

Two gates assigning the same spot is the classic race. Answers that score:
synchronize the allocate/release path, or use an atomic
check-and-reserve on the Spot. Mention it *before* they ask.

### What NOT to do

* Don't over-engineer: no microservices, no database schemas — it's a
  *class* design round.
* Don't put everything in one `ParkingLotManager` god class.
* Don't forget the Ticket — stateless designs can't compute fees at exit.

### Python sketch: the core classes

```python
from enum import Enum, auto

class VehicleType(Enum):
    BIKE = auto(); CAR = auto(); TRUCK = auto()

class Spot:
    def __init__(self, spot_id, allowed):
        self.spot_id = spot_id
        self.allowed = allowed        # set of VehicleType this spot accepts
        self.vehicle = None

    def can_fit(self, vehicle):
        return vehicle.kind in self.allowed and self.vehicle is None

class Ticket:
    def __init__(self, vehicle, spot, entry_time):
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = entry_time
```

### Java sketch: atomic spot allocation

```java
class Spot {
    private final String id;
    private Vehicle vehicle;                       // null = free

    Spot(String id) { this.id = id; }

    synchronized boolean occupy(Vehicle v) {       // atomic check-and-reserve
        if (vehicle != null) return false;         // already taken: one gate wins
        vehicle = v;
        return true;
    }

    synchronized void release() { vehicle = null; }
}
```

**Takeaway:** Requirements -> entities -> relationships -> walk the flow,
then volunteer extensibility and concurrency handling — process is the
product in LLD rounds.
""",
                "difficulty_min": 5,
                "difficulty_max": 10,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon LLD round begins: 'Design a parking lot.' The interviewer is watching your very first move. What should it be — and what does jumping straight to classes signal about you?",
                        "choices": [
                            "Draw the complete class diagram immediately",
                            "Clarify requirements by asking questions — vehicle types, scale, pricing, concurrency — before designing",
                            "Write all the code for the core classes",
                            "Choose the database schema",
                        ],
                        "answer_index": 1,
                        "difficulty": 5,
                        "explanation": "LLD interviews score process: clarifying scope first shows you design against real constraints instead of imagined ones. Candidates who jump to classes usually build the wrong system confidently.",
                        "company_tags": ["amazon", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "In a Google LLD round you've finished clarifying the requirements for a parking lot. The interviewer asks: 'Nouns become classes — which nouns from this domain actually deserve to be classes?'",
                        "choices": [
                                       "Compiler, Parser, Lexer, Optimizer",
                                       "Database, Server, Cache, LoadBalancer",
                                       "User, Password, Session, Cookie",
                                       "ParkingLot, Floor, Spot, Vehicle, Ticket, Gate, Payment",
                                   ],
                        "answer_index": 3,
                        "difficulty": 6,
                        "explanation": "Entities come from the domain nouns: the lot contains floors, floors contain spots, vehicles occupy spots, tickets track stays, gates control entry/exit, payments settle fees. The other lists are infrastructure or unrelated domains.",
                        "company_tags": ["google", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Uber interviewer points at your diagram: 'ParkingLot and Floor — is that inheritance? If not, name the exact relationship and justify it.'",
                        "choices": [
                                       "Inheritance — Floor extends ParkingLot",
                                       "Dependency — Floor merely uses ParkingLot temporarily",
                                       "Composition — a ParkingLot has Floors that belong to it and die with it",
                                       "There is no relationship; they are independent",
                                   ],
                        "answer_index": 2,
                        "difficulty": 7,
                        "explanation": "Floors are parts of the lot with no independent lifecycle — delete the lot, the floors go too. That's composition (strong has-a), not inheritance (a floor is not a kind of parking lot).",
                        "company_tags": ["uber", "swiggy"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "The client now wants EV-charging spots and surge pricing added to your parking lot design. Which principle does a good design demonstrate here?",
                        "choices": [
                            "Open/Closed — new spot types and pricing rules plug in as new classes without modifying existing ones",
                            "Singleton — only one pricing object may exist",
                            "Encapsulation — hide the parking lot from the client",
                            "Polymorphism — every class must be subclassed",
                        ],
                        "answer_index": 0,
                        "difficulty": 8,
                        "explanation": "If pricing was a Strategy and spots form a hierarchy, EV spots and surge pricing arrive as new classes — zero edits to tested code. That's Open/Closed in action, and volunteering this extensibility story is what elevates an LLD answer.",
                        "company_tags": ["meta", "razorpay"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Two cars enter through different gates at the same instant and both get assigned the same spot. What is the right fix to discuss?",
                        "choices": [
                            "Assign spots randomly so collisions are unlikely",
                            "Make spot allocation atomic — synchronize the allocate/release path or use check-and-reserve so one gate wins",
                            "Give each gate its own separate copy of the spot list",
                            "Concurrency cannot occur because gates are physical objects",
                        ],
                        "answer_index": 1,
                        "difficulty": 9,
                        "explanation": "This is the check-then-act race: both gates saw the spot as free before either marked it taken. The fix is atomicity — a synchronized allocation method or an atomic compare-and-set on the spot's state. Interviewers always probe this follow-up.",
                        "company_tags": ["netflix", "phonepe"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Where should the parking fee calculation logic live in a clean design, and why?",
                        "choices": [
                                       "Inside the Ticket class, since the ticket knows the entry time",
                                       "In the Vehicle class, since vehicle type affects price",
                                       "In the main() function, to keep all logic in one place",
                                       "In a separate PricingStrategy hierarchy — fee rules vary independently (hourly, per vehicle type, surge) and shouldn't be hard-coded into Ticket",
                                   ],
                        "answer_index": 3,
                        "difficulty": 10,
                        "explanation": "Pricing is an independent axis of change: new fee rules shouldn't require editing Ticket. A PricingStrategy hierarchy (HourlyPricing, VehicleTypePricing, SurgePricing) keeps Ticket focused on stay records and makes each rule testable in isolation — Strategy + Single Responsibility working together.",
                        "company_tags": ["google", "amazon"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Uber interviewer extends the parking lot mid-round: 'Now add valet parking — an attendant takes the car at the gate, parks it, and retrieves it later. What changes in your class design?'",
                        "choices": [
                            "Nothing changes — the existing park/unpark flow already covers valet",
                            "Add an Attendant entity that performs the park/retrieve steps on the customer's behalf; Ticket, Spot, and Gate keep their contracts, so the design absorbs the new actor without rewriting core classes",
                            "Merge the attendant into the Vehicle class as a boolean is_valet flag",
                            "Delete the Gate classes and let the attendant handle entry directly",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Valet is a new actor performing the same park/retrieve operations the driver used to do, so the clean move is a new Attendant class driving the existing flow — Ticket, Spot, and Gate keep their contracts. If adding valet forced you to rewrite parking logic, the original design had responsibilities in the wrong place. Interviewers extend requirements mid-round precisely to test this.",
                        "company_tags": ["uber", "google", "atlassian"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Atlassian interviewer pushes further: 'Your lot has 50,000 spots across 10 floors. Finding the nearest free spot by scanning everything on every arrival is too slow — how do you make allocation fast without breaking the design?'",
                        "choices": [
                            "Cache the last allocated spot and always hand out the next one",
                            "Maintain an index of free spots per vehicle type (an ordered structure updated on every park/unpark), so allocation becomes a lookup instead of a scan",
                            "Store the spots in a linked list so traversal is faster",
                            "Make spot allocation a Singleton so the scan only ever happens once",
                        ],
                        "answer_index": 1,
                        "difficulty": 9,
                        "explanation": "Scanning 50,000 spots per arrival puts O(n) work on the hot path. The standard fix is an index — free spots organized per vehicle type in an ordered structure, maintained incrementally on park/unpark — so allocation is a fast lookup. Crucially this lives inside the allocation strategy, so Ticket, Gate, and Pricing never notice. Interviewers ask this to see whether you think about scale after correctness.",
                        "company_tags": ["atlassian", "amazon", "google"],
                    },
                ],
            },
            {
                "slug": "oop-interview-marathon",
                "title": "OOP Interview Marathon",
                "theory_md": """## OOP Interview Marathon

Twenty rapid-fire questions, one-line answers each. This is a **revision
sheet** — if any answer surprises you, go back to its lesson before the
interview.

### The 20

1. **What is OOP?** — Modeling software as interacting objects bundling
   data (state) and behavior (methods).
2. **Four pillars?** — Encapsulation, Abstraction, Inheritance,
   Polymorphism.
3. **Encapsulation vs Abstraction?** — Encapsulation *hides* data (private
   + methods); Abstraction *hides* complexity (expose only what matters).
4. **Polymorphism in one line?** — Same interface, different behavior:
   `shape.draw()` does the right thing per subclass.
5. **Compile-time vs runtime polymorphism?** — Overloading (resolved by
   signatures at compile time) vs overriding (resolved by object type at
   runtime).
6. **Abstract class vs interface?** — Abstract class: partial implementation
   + state, single inheritance; interface: pure contract, multiple
   inheritance. (Java 8+ interfaces can have defaults — say it.)
7. **Can you instantiate an abstract class?** — No; but you can hold a
   reference of its type pointing to a subclass object.
8. **Diamond problem?** — Ambiguity from multiple inheritance of state;
   solved by interfaces (Java), virtual inheritance (C++), C3 MRO (Python).
9. **Composition vs inheritance?** — "Has-a" vs "is-a"; prefer composition —
   it's flexible and avoids fragile base classes.
10. **What is coupling?** — How much classes depend on each other; low
    coupling = easier changes.
11. **What is cohesion?** — How focused a class's responsibilities are;
    high cohesion = one clear job.
12. **SOLID in one breath?** — Single responsibility, Open/closed, Liskov
    substitution, Interface segregation, Dependency inversion.
13. **Liskov in one line?** — Subclasses must be usable wherever their
    base is expected, without breaking behavior.
14. **Why virtual destructor?** — So `delete` via a base pointer destroys
    the derived part too.
15. **Static vs dynamic binding?** — Static: call target fixed at compile
    time; dynamic: chosen at runtime via vtable.
16. **Can constructors be virtual?** — No — the object's type isn't known
    until construction finishes. (Virtual *destructor*: yes.)
17. **Method hiding vs overriding?** — Overriding: same signature, runtime
    dispatch. Hiding (C++ non-virtual, Java static): compile-time, based on
    reference type.
18. **What is a pure virtual function?** — `virtual void f() = 0;` — makes
    the class abstract; subclasses must implement it.
19. **Is Java 100% object-oriented?** — No — primitives (`int`, `char`)
    aren't objects (autoboxing bridges the gap).
20. **Deep vs shallow copy?** — Shallow copies references (shared pointee);
    deep copies the pointed-to data too.

### How to use this sheet

Read it once the night before, once the morning of. For each line, force
yourself to produce a **one-sentence example** — interviewers promote
one-liners into "explain with an example" instantly.

### Quick Python demos of the classics

```python
class A:
    def f(self): return "A"
class B(A):
    def f(self): return "B"      # overriding: runtime polymorphism

print(B().f())                  # B — dispatch on object type, not reference

# shallow vs deep copy in one glance
import copy
orig = [[1, 2]]
shallow = copy.copy(orig)
shallow[0].append(99)
print(orig)                     # [[1, 2, 99]] — inner list is shared!
```

### The two-line Java demo to keep in your pocket

```java
class A { void f() { System.out.print("A"); } }
class B extends A { void f() { System.out.print("B"); } }
// A x = new B(); x.f();   -> prints B (runtime dispatch on the OBJECT's type)
```

**Takeaway:** Twenty answers, twenty seconds each — fluency on these buys
you the confidence to handle everything deeper they throw next.
""",
                "difficulty_min": 4,
                "difficulty_max": 10,
                "is_important": True,
                "has_visual": False,
                "questions": [
                    {
                        "qtype": "mcq",
                        "prompt": "Your TCS interviewer opens with: 'Explain polymorphism to me in one line — but make it a line that proves you've actually used it, not memorized it.'",
                        "choices": [
                                       "Using many classes in one program",
                                       "Hiding data inside private fields",
                                       "Inheriting from multiple base classes",
                                       "Same interface, different behavior — e.g. shape.draw() does the right thing per subclass",
                                   ],
                        "answer_index": 3,
                        "difficulty": 4,
                        "explanation": "Polymorphism is one call site, many behaviors: the same draw() invocation dispatches to Circle's or Square's implementation based on the actual object. The other options describe scale, encapsulation, and multiple inheritance.",
                        "company_tags": ["tcs", "wipro"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An Infosys interviewer asks: 'I need a can-do contract that unrelated classes can all adopt — plus some shared code for one family of classes. Which tool for which job: abstract class or interface?'",
                        "choices": [
                                       "Abstract classes can hold state and partial implementation with single inheritance; interfaces are pure contracts allowing multiple inheritance",
                                       "Interfaces can be instantiated; abstract classes cannot",
                                       "There is no difference in any modern language",
                                       "Abstract classes are always faster at runtime",
                                   ],
                        "answer_index": 0,
                        "difficulty": 5,
                        "explanation": "Abstract classes give you shared code + fields but one parent only; interfaces give you a pure 'can-do' contract that many types can adopt. Bonus point: since Java 8, interfaces can carry default methods — mention it to show you're current.",
                        "company_tags": ["infosys", "cognizant"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "What does this print? (Java)\n\nclass A { void f(){ System.out.print(\"A\"); } }\nclass B extends A { void f(){ System.out.print(\"B\"); } }\nA x = new B();\nx.f();",
                        "choices": [
                                       "A",
                                       "AB",
                                       "B",
                                       "Compile error: type mismatch",
                                   ],
                        "answer_index": 2,
                        "difficulty": 6,
                        "explanation": "Runtime polymorphism: the reference type is A but the object is B, and Java dispatches overridden instance methods on the object's actual type. This two-line snippet is an interview staple — 'B' is the answer they want instantly.",
                        "company_tags": ["accenture", "zoho"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "Your Amazon interviewer asks: 'The diamond problem — Java, C++, Python. Three languages, three different escapes. Walk me through each one.'",
                        "choices": [
                            "All three forbid multiple inheritance entirely",
                            "Java uses interfaces (no state MI), C++ uses virtual inheritance, Python uses C3 MRO linearization",
                            "Java uses virtual inheritance, C++ uses interfaces, Python uses single inheritance only",
                            "The diamond problem has no solution in any language",
                        ],
                        "answer_index": 1,
                        "difficulty": 7,
                        "explanation": "Each language picked its own escape hatch: Java sidesteps by allowing multiple inheritance only of (stateless) interfaces, C++ shares one base subobject via virtual inheritance, and Python linearizes deterministically with C3. Knowing all three shows cross-language depth.",
                        "company_tags": ["amazon", "microsoft"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "A Google interviewer pushes back: 'Everyone chants prefer composition over inheritance. Give me the real engineering reason — what actually breaks when you lean on inheritance?'",
                        "choices": [
                                       "Inheritance is deprecated in modern OOP",
                                       "Composition always runs faster than inheritance",
                                       "Inheritance cannot express polymorphism",
                                       "Composition ('has-a') is more flexible and avoids fragile-base-class problems; inheritance ('is-a') tightly couples subclasses to parent implementation details",
                                   ],
                        "answer_index": 3,
                        "difficulty": 8,
                        "explanation": "Inheritance exposes subclasses to every change in the parent's internals (the fragile base class problem) and locks you into one hierarchy. Composition lets you swap, decorate, and combine behaviors at runtime with far less coupling.",
                        "company_tags": ["google", "flipkart"],
                    },
                    {
                        "qtype": "mcq",
                        "prompt": "An interviewer asks: 'Is Java 100% object-oriented? Can constructors be virtual?' What is the correct combined answer?",
                        "choices": [
                                       "No — primitives like int aren't objects; and no, constructors can't be virtual because the object's type isn't established until construction completes",
                                       "Yes to both — everything is an object and constructors dispatch virtually",
                                       "Yes Java is pure OOP, but constructors cannot be virtual",
                                       "No Java is not pure OOP, but constructors are virtual by default",
                                   ],
                        "answer_index": 0,
                        "difficulty": 10,
                        "explanation": "Two classic gotchas in one: Java has non-object primitives (int, char — autoboxing just bridges them), and a virtual constructor is nonsensical because virtual dispatch needs an existing object whose type is known, which is exactly what construction is still establishing. Nailing both back-to-back signals genuine fluency.",
                        "company_tags": ["meta", "netflix"],
                    },
                ],
            },
        ],
    },
]
