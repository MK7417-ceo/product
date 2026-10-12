"""Domain: interview/hiring prep. PURE.

Curated question bank (topic + level tagged). Unlike assessments, these are
LEARNING material — guidance/answer points ship with the question. The bank
is the seed; AI-generated questions plug in later behind the same port.
"""
from __future__ import annotations

from dataclasses import dataclass

from app.domain.user import DomainError

TOPICS = ("python", "dsa", "ml-basics", "system-design", "quant", "behavioral")
LEVELS = ("beginner", "intermediate", "advanced")


@dataclass(frozen=True)
class PrepQuestion:
    id: str
    topic: str
    level: str
    question: str
    guidance: tuple[str, ...]  # answer points, not a script
    tags: tuple[str, ...] = ()

    def validate(self) -> None:
        if self.topic not in TOPICS:
            raise DomainError(f"unknown prep topic: {self.topic}")
        if self.level not in LEVELS:
            raise DomainError(f"unknown level: {self.level}")
        if not self.question.strip() or not self.guidance:
            raise DomainError("question and guidance required")


def _q(qid: str, topic: str, level: str, question: str,
       guidance: list[str], tags: list[str] | None = None) -> PrepQuestion:
    q = PrepQuestion(id=qid, topic=topic, level=level, question=question,
                     guidance=tuple(guidance), tags=tuple(tags or []))
    q.validate()
    return q


BANK: list[PrepQuestion] = [
    # ---- python ----
    _q("py1", "python", "beginner", "List aur tuple mein kya difference hai?",
       ["List mutable, tuple immutable",
        "Tuple hashable -> dict key / set member ban sakta hai",
        "Heterogeneous data, unpacking examples"], ["collections"]),
    _q("py2", "python", "beginner", "*args aur **kwargs kya karte hain?",
       ["*args positional args ko tuple mein pack karta hai",
        "**kwargs keyword args ko dict mein",
        "Function signature flexible banane ke liye"], ["functions"]),
    _q("py3", "python", "intermediate", "Decorator kya hai? Ek example do.",
       ["Function ko wrap karke behavior extend karna",
        "@timer / @login_required jaisa example",
        "functools.wraps kyun zaroori hai"], ["functions"]),
    _q("py4", "python", "intermediate", "def f(items=[]) mein kya problem hai?",
       ["Default argument ek baar evaluate hota hai — shared across calls",
        "Fix: def f(items=None)",
        "Python ka gotcha — interviewer ko pata hai tumne bug dekha hai"], ["gotchas"]),
    _q("py5", "python", "advanced", "GIL kya hai? Multithreading par kya asar hai?",
       ["Global Interpreter Lock — ek time par ek thread Python bytecode",
        "CPU-bound kaam threads se fast nahi hota; I/O-bound hota hai",
        "Workaround: multiprocessing, C extensions, PyPy/STM"], ["concurrency"]),
    _q("py6", "python", "advanced", "Context manager kya hai? with kaise kaam karta hai?",
       ["__enter__ / __exit__ protocol",
        "contextlib.contextmanager se generator-based",
        "Resource cleanup guarantee — file, lock, DB connection"], ["advanced"]),
    # ---- dsa ----
    _q("ds1", "dsa", "beginner", "Array mein second largest element nikalo.",
       ["Ek pass mein two variables track karo",
        "Edge: duplicates, n < 2",
        "Complexity O(n) time, O(1) space"], ["arrays"]),
    _q("ds2", "dsa", "beginner", "Two Sum problem samjhao.",
       ["Hashmap: complement = target - x",
        "O(n) time — brute force O(n^2) se behtar",
        "Follow-up: sorted array -> two pointers"], ["hashmap"]),
    _q("ds3", "dsa", "intermediate", "Linked list reverse karo (iterative).",
       ["Three pointers: prev, curr, next",
        "O(1) space iterative vs O(n) recursive",
        "Edge: empty / single node"], ["linked-list"]),
    _q("ds4", "dsa", "intermediate", "Binary search kab fail hota hai?",
       ["Sirf sorted data par kaam karta hai",
        "Mid overflow: mid = lo + (hi-lo)//2",
        "Rotated sorted array variant"], ["searching"]),
    _q("ds5", "dsa", "advanced", "BFS vs DFS — kab kaunsa?",
       ["BFS: shortest path unweighted graph; queue",
        "DFS: connectivity, topological sort, recursion/stack",
        "Dono O(V+E)"], ["graphs"]),
    _q("ds6", "dsa", "advanced", "HashMap internally kaise kaam karta hai?",
       ["Hash function -> bucket array",
        "Collision: chaining vs open addressing",
        "Load factor aur resizing; Python dict ka open addressing"], ["hashmap"]),
    # ---- ml-basics ----
    _q("ml1", "ml-basics", "beginner", "Overfitting kya hai? Kaise pehchano?",
       ["Model noise yaad kar leta hai — train accha, test kharab",
        "Gap between train/val accuracy",
        "Fix: more data, regularization, dropout, early stopping"], ["generalization"]),
    _q("ml2", "ml-basics", "intermediate", "Train/validation/test split kyun?",
       ["Train: seekhna; val: hyperparameter tune; test: final unbiased score",
        "Test ko sirf ek baar chhuna chahiye",
        "Data leakage se bacho"], ["evaluation"]),
    _q("ml3", "ml-basics", "intermediate", "Precision vs recall — kab kaunsa?",
       ["Precision: predicted positive kitne sahi (spam filter)",
        "Recall: actual positive kitne pakde (cancer screening)",
        "F1 = harmonic mean"], ["metrics"]),
    _q("ml4", "ml-basics", "advanced", "Gradient descent ek line mein, phir detail.",
       ["Loss kam karne ke liye parameters ko negative gradient direction mein step",
        "Learning rate: bada -> diverge, chhota -> slow",
        "SGD vs Adam ka intuition"], ["optimization"]),
    # ---- system-design ----
    _q("sd1", "system-design", "beginner", "URL shortener design karo (high level).",
       ["Requirements: write-heavy? read-heavy? (read-heavy)",
        "Base62 encode of auto-increment id / hash",
        "DB + cache (Redis); 301 redirect"], ["web"]),
    _q("sd2", "system-design", "intermediate", "Rate limiter kaise banayenge?",
       ["Token bucket vs fixed window vs sliding window",
        "Redis + Lua ya in-memory per instance",
        "Headers: X-RateLimit-Remaining"], ["scalability"]),
    _q("sd3", "system-design", "intermediate", "Caching strategies samjhao.",
       ["Cache-aside, read-through, write-through, write-behind",
        "Cache invalidation — 'two hard problems'",
        "CDN vs application cache"], ["caching"]),
    _q("sd4", "system-design", "advanced", "Load balancer kya karta hai? Types?",
       ["Traffic distribute karna; health checks",
        "L4 (TCP) vs L7 (HTTP) — round robin, least connections, IP hash",
        "Sticky sessions kab chahiye"], ["scalability"]),
    # ---- quant ----
    _q("q1", "quant", "beginner", "Ek number ka 20% = 60. Number kya hai?",
       ["60 / 0.20 = 300",
        "Reverse percentage — common trap"], ["percentages"]),
    _q("q2", "quant", "beginner", "Train 60 km/h se 2.5 ghante chalti hai. Distance?",
       ["Distance = speed × time = 150 km",
        "Units consistent rakho"], ["speed-time"]),
    _q("q3", "quant", "intermediate", "A:B = 2:3, B:C = 4:5. A:B:C?",
       ["B common karo: 8:12 aur 12:15 -> 8:12:15",
        "LCM trick"], ["ratios"]),
    _q("q4", "quant", "intermediate", "Ek bag mein 3 laal, 2 neele ball. Ek nikalne par laal ki probability?",
       ["Favourable / total = 3/5",
        "'Bina replacement' doosre draw mein badal jaata hai"], ["probability"]),
    _q("q5", "quant", "advanced", "2, 6, 12, 20, 30, ? Next number?",
       ["Differences: 4, 6, 8, 10 -> next diff 12 -> 42",
        "Pattern: n(n+1)"], ["series"]),
    _q("q6", "quant", "advanced", "5 numbers ka average 27 hai. Ek number 18 hata diya. Naya average?",
       ["Total = 135; naya total 117; /4 = 29.25",
        "Weighted socho"], ["averages"]),
    # ---- behavioral / PI ----
    _q("b1", "behavioral", "beginner", "Tell me about yourself. (2 minute)",
       ["Present -> past -> future structure",
        "Resume ke bullet points ko story banao",
        "Role se connect karke khatam karo"], ["pi"]),
    _q("b2", "behavioral", "beginner", "Tumhari sabse badi strength / weakness?",
       ["Strength: example ke saath",
        "Weakness: real + 'is par kaam kar raha hun'",
        "'Perfectionist hun' cliché se bacho"], ["pi"]),
    _q("b3", "behavioral", "intermediate", "Ek time batao jab team mein conflict hua.",
       ["STAR format: Situation, Task, Action, Result",
        "Blame nahi — tumne kya kiya",
        "Seekha kya"], ["pi", "star"]),
    _q("b4", "behavioral", "intermediate", "Why should we hire you? / Why our company?",
       ["Company ka specific point (product, tech, mission)",
        "Tumhari skills -> unki problem",
        "Generic praise nahi"], ["pi"]),
    _q("b5", "behavioral", "advanced", "Ek failure aur usse kya seekha?",
       ["Real failure chunna — chhota nahi, fake nahi",
        "Tumhari galti own karo",
        "System/process change jo tumne lagaya"], ["pi", "star"]),
    _q("b6", "behavioral", "advanced", "5 saal mein khud ko kahan dekhte ho?",
       ["Role-relevant growth dikhao",
        "Company ke andar growth — 'startup kholunga' mat bolo",
        "Skills + impact, sirf title nahi"], ["pi"]),
]


def topics() -> list[dict]:
    return [{"topic": t,
             "count": sum(1 for q in BANK if q.topic == t)}
            for t in TOPICS]


def questions(topic: str = "", level: str = "", count: int = 10) -> list[PrepQuestion]:
    pool = [q for q in BANK
            if (not topic or q.topic == topic)
            and (not level or q.level == level)]
    if topic and topic not in TOPICS:
        raise DomainError(f"unknown prep topic: {topic}")
    if level and level not in LEVELS:
        raise DomainError(f"unknown level: {level}")
    return pool[:max(1, min(count, 50))]
