"""Outbound adapter: curated diagnostic question bank.

Seed of the hybrid strategy (curated bank first, AI-generated questions
later). 77 questions: Python (8 x beginner/intermediate/advanced) +
ML basics (4 x beginner/intermediate) + JavaScript (5 x beginner/
intermediate/advanced) + Java (5 x beginner/intermediate/advanced) +
Web dev (5 x beginner/intermediate/advanced). Every question carries
a skill tag used for gap reports.
"""
from __future__ import annotations

from app.domain.profile import Question


def _q(qid: str, topic: str, level: str, skill: str, prompt: str,
       choices: list[str], answer: int) -> Question:
    return Question(id=qid, topic=topic, level=level, skill=skill,
                    prompt=prompt, choices=tuple(choices), answer_index=answer)


_BANK: list[Question] = [
    # ---- python / beginner ----
    _q("py-b1", "python", "beginner", "python-basics", "What does len([1, 2, 3]) return?",
       ["2", "3", "6", "TypeError"], 1),
    _q("py-b2", "python", "beginner", "python-basics", "Which keyword defines a function in Python?",
       ["function", "def", "fn", "define"], 1),
    _q("py-b3", "python", "beginner", "python-basics", "What is the type of 3.0?",
       ["int", "float", "str", "number"], 1),
    _q("py-b4", "python", "beginner", "python-basics", "How do you write a single-line comment?",
       ["// comment", "# comment", "/* comment */", "-- comment"], 1),
    _q("py-b5", "python", "beginner", "data-structures", "What does type([]) return?",
       ["dict", "tuple", "list", "set"], 2),
    _q("py-b6", "python", "beginner", "python-basics", "Which is a valid variable name?",
       ["2fast", "my-var", "my_var", "class"], 2),
    _q("py-b7", "python", "beginner", "iterators", "What values does range(3) produce?",
       ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3, 2, 1"], 1),
    _q("py-b8", "python", "beginner", "data-structures", "How do you get the last element of list a?",
       ["a[0]", "a[last]", "a[-1]", "a[len]"], 2),
    # ---- python / intermediate ----
    _q("py-i1", "python", "intermediate", "iterators", "What is the value of [x * 2 for x in range(3)]?",
       ["[2, 4, 6]", "[0, 2, 4]", "[0, 1, 2]", "SyntaxError"], 1),
    _q("py-i2", "python", "intermediate", "data-structures", "What does d.get(k) return when k is missing from dict d?",
       ["KeyError", "None", "False", "0"], 1),
    _q("py-i3", "python", "intermediate", "functions", "In def f(*args), what does args collect?",
       ["keyword arguments as a dict", "positional arguments as a tuple",
        "only the first argument", "a list of default values"], 1),
    _q("py-i4", "python", "intermediate", "python-basics", "What is the difference between == and is?",
       ["no difference", "== compares values, is compares identity",
        "is compares values, == compares identity", "is only works on numbers"], 1),
    _q("py-i5", "python", "intermediate", "oop", "What is `self` in a method definition?",
       ["a keyword for static methods", "a reference to the instance",
        "the class itself", "a decorator"], 1),
    _q("py-i6", "python", "intermediate", "stdlib", "What does sorted([3, 1, 2]) return?",
       ["[3, 1, 2]", "[1, 2, 3] (new list)", "None", "[2, 1, 3]"], 1),
    _q("py-i7", "python", "intermediate", "stdlib", "What does `with open(path) as f:` guarantee?",
       ["faster reads", "the file is closed afterwards",
        "the file is locked", "binary mode"], 1),
    _q("py-i8", "python", "intermediate", "data-structures", "Key difference between list and tuple?",
       ["tuples are immutable", "lists are immutable",
        "tuples cannot hold numbers", "no difference"], 0),
    # ---- python / advanced ----
    _q("py-a1", "python", "advanced", "functions", "What is a decorator in Python?",
       ["a special comment", "a function that wraps another function to extend behavior",
        "a class inheritance trick", "a type annotation"], 1),
    _q("py-a2", "python", "advanced", "advanced-python", "What does the GIL limit in CPython?",
       ["memory usage", "true parallelism of threads", "recursion depth", "import speed"], 1),
    _q("py-a3", "python", "advanced", "oop", "What is the main purpose of __slots__ in a class?",
       ["to make attributes private", "to restrict and speed up attribute storage",
        "to enable multiple inheritance", "to define class methods"], 1),
    _q("py-a4", "python", "advanced", "functions", "What is risky about def f(items=[])?",
       ["nothing", "the default list is shared across calls",
        "it raises SyntaxError", "it is slower than None"], 1),
    _q("py-a5", "python", "advanced", "iterators", "What is a generator?",
       ["a random number tool", "a lazy iterator using yield",
        "a test framework", "a type of decorator"], 1),
    _q("py-a6", "python", "advanced", "stdlib", "What does functools.lru_cache do?",
       ["clears memory", "memoizes function results",
        "speeds up imports", "caches files"], 1),
    _q("py-a7", "python", "advanced", "advanced-python", "What is monkey patching?",
       ["fixing syntax errors", "modifying code at runtime",
        "a testing library", "a git command"], 1),
    _q("py-a8", "python", "advanced", "oop", "What does MRO stand for?",
       ["method resolution order", "memory read operation",
        "multiple return objects", "module reload option"], 0),
    # ---- ml-basics / beginner ----
    _q("ml-b1", "ml-basics", "beginner", "ml-concepts", "Which of these is a supervised learning task?",
       ["clustering customers", "predicting house prices from features",
        "finding anomalies", "compressing images"], 1),
    _q("ml-b2", "ml-basics", "beginner", "ml-concepts", "What is a 'label' in supervised learning?",
       ["the model's name", "the target value to predict",
        "a data column to ignore", "the loss function"], 1),
    _q("ml-b3", "ml-basics", "beginner", "ml-libraries", "Which library is the standard for numerical computing in Python?",
       ["requests", "numpy", "flask", "pytest"], 1),
    _q("ml-b4", "ml-basics", "beginner", "ml-concepts", "What is overfitting?",
       ["training too slowly", "model memorizes training data, fails on new data",
        "using too little data", "a hardware error"], 1),
    # ---- ml-basics / intermediate ----
    _q("ml-i1", "ml-basics", "intermediate", "ml-metrics", "What does a confusion matrix show?",
       ["feature importance", "predicted vs actual classes",
        "training loss curve", "data distribution"], 1),
    _q("ml-i2", "ml-basics", "intermediate", "ml-workflow", "Why split data into train and test sets?",
       ["to train faster", "to evaluate generalization on unseen data",
        "to reduce memory", "it is optional"], 1),
    _q("ml-i3", "ml-basics", "intermediate", "ml-concepts", "What is gradient descent?",
       ["a data cleaning step", "an optimization algorithm minimizing loss",
        "a model architecture", "a metric"], 1),
    _q("ml-i4", "ml-basics", "intermediate", "ml-metrics", "Why can accuracy mislead on imbalanced data?",
       ["it cannot", "the majority class dominates the score",
        "it is too slow", "it needs more epochs"], 1),
    # ---- javascript / beginner ----
    _q("js-b1", "javascript", "beginner", "js-basics", "Which keyword declares a block-scoped variable in JavaScript?",
       ["var", "let", "dim", "define"], 1),
    _q("js-b2", "javascript", "beginner", "js-basics", "What does typeof null return in JavaScript?",
       ["\"null\"", "\"object\"", "\"undefined\"", "\"number\""], 1),
    _q("js-b3", "javascript", "beginner", "js-basics", "How do you write a single-line comment in JavaScript?",
       ["# comment", "// comment", "<!-- comment -->", "/* comment */"], 1),
    _q("js-b4", "javascript", "beginner", "js-arrays", "What does [1, 2, 3].length return?",
       ["2", "3", "4", "undefined"], 1),
    _q("js-b5", "javascript", "beginner", "js-arrays", "Which method adds an element to the end of an array?",
       ["push()", "pop()", "shift()", "unshift()"], 0),
    # ---- javascript / intermediate ----
    _q("js-i1", "javascript", "intermediate", "js-functions", "What is a closure in JavaScript?",
       ["a function bundled with its lexical environment",
        "a way to close browser tabs", "a loop construct", "a type of error"], 0),
    _q("js-i2", "javascript", "intermediate", "js-arrays", "What does Array.prototype.map() return?",
       ["the same array mutated", "a new array with transformed elements",
        "undefined", "the first element"], 1),
    _q("js-i3", "javascript", "intermediate", "js-basics", "What is the output of console.log(0.1 + 0.2 === 0.3)?",
       ["true", "false", "TypeError", "undefined"], 1),
    _q("js-i4", "javascript", "intermediate", "js-basics", "What does the === operator check?",
       ["value only", "type only",
        "value and type without coercion", "reference only"], 2),
    _q("js-i5", "javascript", "intermediate", "js-async", "What is the event loop in JavaScript?",
       ["a for loop", "the mechanism handling async callbacks via the task queue",
        "a DOM event", "a debugging tool"], 1),
    # ---- javascript / advanced ----
    _q("js-a1", "javascript", "advanced", "js-async", "What does a Promise represent?",
       ["a synchronous value", "the eventual completion of an async operation",
        "a callback function", "a thread"], 1),
    _q("js-a2", "javascript", "advanced", "js-async", "What does async/await provide?",
       ["parallel threads", "cleaner syntax over promises for async code",
        "main-thread blocking", "bytecode compilation"], 1),
    _q("js-a3", "javascript", "advanced", "js-functions", "What is hoisting in JavaScript?",
       ["lifting DOM elements", "declarations moved to the top of their scope before execution",
        "a CSS technique", "compressing JS files"], 1),
    _q("js-a4", "javascript", "advanced", "js-basics", "What is the key difference between let and var?",
       ["no difference", "let is block-scoped, var is function-scoped",
        "var is block-scoped", "let cannot be reassigned"], 1),
    _q("js-a5", "javascript", "advanced", "js-functions", "In obj.method(), what does 'this' refer to inside method?",
       ["the global object", "obj", "always undefined", "the function itself"], 1),
    # ---- java / beginner ----
    _q("jv-b1", "java", "beginner", "java-basics", "Which keyword defines a class in Java?",
       ["class", "define", "struct", "object"], 0),
    _q("jv-b2", "java", "beginner", "java-basics", "What is the entry point method of a Java program?",
       ["start()", "main()", "run()", "init()"], 1),
    _q("jv-b3", "java", "beginner", "java-basics", "Which of these is NOT a primitive type in Java?",
       ["int", "String", "boolean", "char"], 1),
    _q("jv-b4", "java", "beginner", "java-basics", "How do you write a single-line comment in Java?",
       ["# comment", "// comment", "<!-- -->", "-- comment"], 1),
    _q("jv-b5", "java", "beginner", "java-basics", "What does System.out.println(3 + 4 + \"x\") print?",
       ["7x", "34x", "3+4x", "compile error"], 0),
    # ---- java / intermediate ----
    _q("jv-i1", "java", "intermediate", "java-oop", "What is inheritance in Java?",
       ["a class acquiring properties of another via extends",
        "copying code files", "a type of loop", "importing packages"], 0),
    _q("jv-i2", "java", "intermediate", "java-collections", "Which collection does NOT allow duplicate elements?",
       ["ArrayList", "LinkedList", "HashSet", "Vector"], 2),
    _q("jv-i3", "java", "intermediate", "java-oop", "What is the difference between == and .equals() for objects?",
       ["no difference", "== compares references, equals() compares content",
        "equals() compares references", "== is always true"], 1),
    _q("jv-i4", "java", "intermediate", "java-basics", "What does the 'final' keyword mean on a variable?",
       ["it can be changed once", "it cannot be reassigned after initialization",
        "it is static", "it is private"], 1),
    _q("jv-i5", "java", "intermediate", "java-exceptions", "Which keywords are used to handle exceptions in Java?",
       ["handle", "try/catch", "error", "rescue"], 1),
    # ---- java / advanced ----
    _q("jv-a1", "java", "advanced", "java-generics", "What are generics in Java?",
       ["generic error messages", "type parameters enabling type-safe collections",
        "a naming convention", "default method arguments"], 1),
    _q("jv-a2", "java", "advanced", "java-streams", "What does the Stream API enable?",
       ["network sockets", "functional-style operations on collections",
        "file streaming only", "multithreading primitives"], 1),
    _q("jv-a3", "java", "advanced", "java-jvm", "What is the JVM?",
       ["a Java IDE", "the virtual machine executing Java bytecode",
        "a build tool", "a testing framework"], 1),
    _q("jv-a4", "java", "advanced", "java-basics", "What is autoboxing in Java?",
       ["automatic UI layout", "automatic conversion between primitives and wrapper types",
        "compressing bytecode", "serializing objects"], 1),
    _q("jv-a5", "java", "advanced", "java-oop", "Which is true about interfaces in Java?",
       ["they can hold instance fields", "a class can implement multiple interfaces",
        "they cannot declare methods", "they support multiple inheritance of state"], 1),
    # ---- webdev / beginner ----
    _q("wd-b1", "webdev", "beginner", "html-basics", "What does HTML stand for?",
       ["Hyper Text Markup Language", "High Tech Machine Language",
        "Hyperlink Text Mode Language", "Home Tool Markup Language"], 0),
    _q("wd-b2", "webdev", "beginner", "html-basics", "Which tag creates the largest heading in HTML?",
       ["<h6>", "<h1>", "<head>", "<header>"], 1),
    _q("wd-b3", "webdev", "beginner", "css-basics", "What does CSS stand for?",
       ["Computer Style Sheets", "Cascading Style Sheets",
        "Creative Style System", "Colorful Style Sheets"], 1),
    _q("wd-b4", "webdev", "beginner", "html-basics", "Which HTML tag creates a hyperlink?",
       ["<link>", "<a>", "<href>", "<url>"], 1),
    _q("wd-b5", "webdev", "beginner", "html-basics", "What does the 'src' attribute of <img> specify?",
       ["the image size", "the image file URL",
        "the alt text", "the alignment"], 1),
    # ---- webdev / intermediate ----
    _q("wd-i1", "webdev", "intermediate", "http-basics", "What does HTTP stand for?",
       ["Hyper Text Transfer Protocol", "High Transfer Text Protocol",
        "Hyperlink Text Transport Program", "Home Transfer Protocol"], 0),
    _q("wd-i2", "webdev", "intermediate", "http-basics", "Which HTTP method submits form data that creates a resource?",
       ["GET", "POST", "DELETE", "HEAD"], 1),
    _q("wd-i3", "webdev", "intermediate", "css-responsive", "What does 'responsive design' mean?",
       ["fast loading only", "layout adapts to different screen sizes",
        "using React", "dark mode"], 1),
    _q("wd-i4", "webdev", "intermediate", "css-layout", "Which CSS declaration makes an element a flex container?",
       ["display: flex", "flex: true", "position: flex", "layout: flexbox"], 0),
    _q("wd-i5", "webdev", "intermediate", "css-basics", "What is the CSS box model order, inside out?",
       ["margin, border, padding, content", "content, padding, border, margin",
        "padding, content, margin, border", "border, content, padding, margin"], 1),
    # ---- webdev / advanced ----
    _q("wd-a1", "webdev", "advanced", "browser-dom", "What is the DOM?",
       ["a database", "a programming interface representing the page as objects",
        "a CSS framework", "a server protocol"], 1),
    _q("wd-a2", "webdev", "advanced", "css-basics", "Which CSS selector has the highest specificity?",
       [".class", "#id", "element", "*"], 1),
    _q("wd-a3", "webdev", "advanced", "browser-security", "What is CORS?",
       ["a CSS property", "a security mechanism controlling cross-origin requests",
        "a JS framework", "an HTML tag"], 1),
    _q("wd-a4", "webdev", "advanced", "browser-storage", "What is the difference between localStorage and sessionStorage?",
       ["no difference", "localStorage persists across sessions; sessionStorage clears on tab close",
        "sessionStorage is larger", "localStorage is per-tab only"], 1),
    _q("wd-a5", "webdev", "advanced", "css-layout", "In CSS Grid, what does 'grid-template-columns: 1fr 2fr' do?",
       ["sets row heights", "creates two columns, the second twice as wide",
        "hides the grid", "centers all items"], 1),
]


class StaticQuestionBank:
    def __init__(self, questions: list[Question] | None = None) -> None:
        self._questions = questions if questions is not None else list(_BANK)
        self._by_id = {q.id: q for q in self._questions}

    def topics(self) -> list[str]:
        return sorted({q.topic for q in self._questions})

    def levels(self, topic: str) -> list[str]:
        return sorted({q.level for q in self._questions if q.topic == topic})

    def questions(self, topic: str, level: str, count: int) -> list[Question]:
        pool = [q for q in self._questions if q.topic == topic and q.level == level]
        return pool[:count]

    def get(self, question_id: str) -> Question | None:
        return self._by_id.get(question_id)
