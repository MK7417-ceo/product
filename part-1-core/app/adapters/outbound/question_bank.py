"""Outbound adapter: curated diagnostic question bank.

Seed of the hybrid strategy (curated bank first, AI-generated questions
later). 32 questions: Python (8 x beginner/intermediate/advanced) +
ML basics (4 x beginner/intermediate). Every question carries a skill tag
used for gap reports.
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
