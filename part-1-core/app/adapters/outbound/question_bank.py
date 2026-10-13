"""Outbound adapter: curated diagnostic question bank.

Seed of the hybrid strategy (curated bank first, AI-generated questions
later). 54 questions: Python (8 beginner / 8 intermediate / 8 advanced /
6 expert) + ML basics (6 per level across beginner/intermediate/advanced/
expert). Every question carries a skill tag used for gap reports. Every
topic/level pool holds at least 4 questions so placement sessions can draw
a random spread from basic to advanced.
"""
from __future__ import annotations

from app.domain.profile import Question, WrittenQuestion


def _q(qid: str, topic: str, level: str, skill: str, prompt: str,
       choices: list[str], answer: int) -> Question:
    return Question(id=qid, topic=topic, level=level, skill=skill,
                    prompt=prompt, choices=tuple(choices), answer_index=answer)


def _wq(qid: str, topic: str, level: str, prompt: str,
        key_concepts: list[str], sample_answer: str) -> WrittenQuestion:
    return WrittenQuestion(id=qid, topic=topic, level=level, prompt=prompt,
                           key_concepts=tuple(key_concepts),
                           sample_answer=sample_answer)


# ---- written (subjective) bank: 1 per level for python (F6d v4) ----
_WRITTEN_BANK: list[WrittenQuestion] = [
    _wq(
        "py-w1", "python", "beginner",
        "Explain the difference between a list and a tuple in Python. "
        "When would you choose one over the other?",
        ["mutable", "immutable", "ordered", "square brackets", "parentheses",
         "fixed data"],
        "A list is mutable and written with square brackets; a tuple is "
        "immutable and written with parentheses. Both are ordered. Use a list "
        "when the collection changes, a tuple for fixed data like coordinates.",
    ),
    _wq(
        "py-w2", "python", "intermediate",
        "Explain how a Python dictionary lookup works. What makes it fast, "
        "and what can go wrong?",
        ["hash", "hash table", "key", "average O(1)", "collision",
         "immutable keys"],
        "Dicts are hash tables: the key is hashed to find a bucket, giving "
        "average O(1) lookup. Collisions are resolved internally. Keys must be "
        "hashable (immutable); unhashable keys raise TypeError.",
    ),
    _wq(
        "py-w3", "python", "advanced",
        "What is Python's GIL? How does it affect multithreaded programs, "
        "and what are the common workarounds?",
        ["global interpreter lock", "thread", "CPU-bound", "I/O-bound",
         "multiprocessing", "single core"],
        "The GIL is a mutex allowing only one thread to execute Python "
        "bytecode at a time. CPU-bound threads don't speed up (single core); "
        "I/O-bound threads still benefit. Workarounds: multiprocessing, "
        "C extensions releasing the GIL, or nogil builds.",
    ),
]


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
    # ---- ml-basics / beginner (top-up) ----
    _q("ml-b5", "ml-basics", "beginner", "ml-concepts", "In a dataset of houses, what is a 'feature'?",
       ["the price to predict", "an input attribute like area or rooms",
        "the model's name", "the training error"], 1),
    _q("ml-b6", "ml-basics", "beginner", "ml-workflow", "What are the three standard data splits?",
       ["train / validation / test", "input / output / error",
        "small / medium / large", "raw / clean / final"], 0),
    # ---- ml-basics / intermediate (top-up) ----
    _q("ml-i5", "ml-basics", "intermediate", "ml-concepts", "What is the bias-variance tradeoff about?",
       ["speed vs memory", "underfitting vs overfitting as model complexity changes",
        "CPU vs GPU training", "batch size vs epochs"], 1),
    _q("ml-i6", "ml-basics", "intermediate", "ml-workflow", "What does k-fold cross-validation do?",
       ["trains k models on k different datasets",
        "rotates which fold is held out for validation to use all data",
        "copies the dataset k times", "tests k hyperparameters at once"], 1),
    # ---- ml-basics / advanced ----
    _q("ml-a1", "ml-basics", "advanced", "ml-concepts", "What does L2 regularization (ridge) do?",
       ["removes features entirely", "penalizes large weights to reduce overfitting",
        "speeds up training", "adds more layers"], 1),
    _q("ml-a2", "ml-basics", "advanced", "ml-metrics", "When is F1-score preferred over accuracy?",
       ["always", "when classes are imbalanced and both precision and recall matter",
        "only for regression", "when the dataset is tiny"], 1),
    _q("ml-a3", "ml-basics", "advanced", "ml-concepts", "What problem does batch normalization address?",
       ["slow disk I/O", "internal covariate shift, stabilizing layer inputs",
        "too many features", "label noise"], 1),
    _q("ml-a4", "ml-basics", "advanced", "ml-concepts", "Why do deep networks suffer from vanishing gradients?",
       ["too much data", "repeated multiplication of small derivatives through layers",
        "large batch sizes", "high learning rates"], 1),
    _q("ml-a5", "ml-basics", "advanced", "ml-concepts", "What is the core idea of the attention mechanism?",
       ["random weight init", "weighing input parts by relevance when producing output",
        "dropping random neurons", "sorting the training data"], 1),
    _q("ml-a6", "ml-basics", "advanced", "ml-workflow", "What is data leakage in ML evaluation?",
       ["a slow data pipeline", "test information leaking into training, inflating scores",
        "losing data files", "a security breach only"], 1),
    # ---- ml-basics / expert ----
    _q("ml-e1", "ml-basics", "expert", "ml-systems", "What is the main idea behind LoRA fine-tuning?",
       ["training from scratch", "learning low-rank updates while freezing base weights",
        "deleting layers", "quantizing to 1 bit"], 1),
    _q("ml-e2", "ml-basics", "expert", "ml-systems", "Why use mixed-precision training?",
       ["it is more accurate", "faster training and lower memory with minimal accuracy loss",
        "it needs no GPU", "it removes hyperparameters"], 1),
    _q("ml-e3", "ml-basics", "expert", "ml-concepts", "What do neural scaling laws describe?",
       ["exact test accuracy", "power-law gains from more parameters, data and compute",
        "optimal batch size", "learning rate schedules"], 1),
    _q("ml-e4", "ml-basics", "expert", "ml-workflow", "In distributed data-parallel training, what is synchronized?",
       ["the datasets", "gradients averaged across workers each step",
        "the random seeds only", "the model architectures"], 1),
    _q("ml-e5", "ml-basics", "expert", "ml-metrics", "What does a high ROC-AUC with poor calibration mean?",
       ["the model is useless", "good ranking of positives vs negatives, but probabilities are off",
        "perfect predictions", "underfitting"], 1),
    _q("ml-e6", "ml-basics", "expert", "ml-concepts", "What is the key risk of offline evaluation for recommender systems?",
       ["it is too slow", "feedback loops and position bias differ from live behavior",
        "it needs labels", "it only works for movies"], 1),
    # ---- python / expert ----
    _q("py-e1", "python", "expert", "advanced-python", "What is a metaclass in Python?",
       ["a fast loop", "a class whose instances are classes, customizing class creation",
        "a type of decorator", "a C extension"], 1),
    _q("py-e2", "python", "expert", "advanced-python", "What does the descriptor protocol (__get__/__set__) enable?",
       ["faster imports", "custom attribute access, powering properties and slots",
        "multiple inheritance", "async I/O"], 1),
    _q("py-e3", "python", "expert", "advanced-python", "Why can asyncio not speed up CPU-bound work alone?",
       ["it can", "the event loop is single-threaded; CPU work blocks it",
        "it needs more RAM", "it only works on Linux"], 1),
    _q("py-e4", "python", "expert", "advanced-python", "What does __init_subclass__ let a base class do?",
       ["skip __init__", "hook into subclass creation for registration or validation",
        "prevent inheritance", "speed up instantiation"], 1),
    _q("py-e5", "python", "expert", "advanced-python", "In typing, what is a Protocol used for?",
       ["runtime speed", "structural subtyping: matching by methods, not inheritance",
        "data validation", "network protocols"], 1),
    _q("py-e6", "python", "expert", "advanced-python", "What happens during import of a module with circular imports?",
       ["always an error", "partially initialized module objects may be seen; order matters",
        "infinite loop", "nothing special"], 1),
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

    def pool(self, topic: str, level: str) -> list[Question]:
        """Full pool for a topic/level (used for random placement sampling)."""
        return [q for q in self._questions if q.topic == topic and q.level == level]

    def written_pool(self, topic: str, level: str) -> list[WrittenQuestion]:
        """Written-question pool for a topic/level (F6d v4)."""
        return [q for q in _WRITTEN_BANK if q.topic == topic and q.level == level]

    def get(self, question_id: str) -> Question | None:
        return self._by_id.get(question_id)
