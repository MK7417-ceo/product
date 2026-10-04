"""Outbound adapter: a small curated diagnostic question bank.

This is the seed of the hybrid strategy (curated bank first, AI-generated
questions later). Enough to prove the placement/verification loop end to end.
"""
from __future__ import annotations

from app.domain.profile import Question


def _q(qid: str, level: str, prompt: str, choices: list[str], answer: int) -> Question:
    return Question(id=qid, topic="python", level=level, prompt=prompt,
                    choices=tuple(choices), answer_index=answer)


_BANK: list[Question] = [
    # ---- beginner ----
    _q("py-b1", "beginner", "What does len([1, 2, 3]) return?",
       ["2", "3", "6", "TypeError"], 1),
    _q("py-b2", "beginner", "Which keyword defines a function in Python?",
       ["function", "def", "fn", "define"], 1),
    _q("py-b3", "beginner", "What is the type of 3.0?",
       ["int", "float", "str", "number"], 1),
    _q("py-b4", "beginner", "How do you write a single-line comment?",
       ["// comment", "# comment", "/* comment */", "-- comment"], 1),
    # ---- intermediate ----
    _q("py-i1", "intermediate", "What is the value of [x * 2 for x in range(3)]?",
       ["[2, 4, 6]", "[0, 2, 4]", "[0, 1, 2]", "SyntaxError"], 1),
    _q("py-i2", "intermediate", "What does d.get(k) return when k is missing from dict d?",
       ["KeyError", "None", "False", "0"], 1),
    _q("py-i3", "intermediate", "In def f(*args), what does args collect?",
       ["keyword arguments as a dict", "positional arguments as a tuple",
        "only the first argument", "a list of default values"], 1),
    _q("py-i4", "intermediate", "What is the difference between == and is?",
       ["no difference", "== compares values, is compares identity",
        "is compares values, == compares identity", "is only works on numbers"], 1),
    # ---- advanced ----
    _q("py-a1", "advanced", "What is a decorator in Python?",
       ["a special comment", "a function that wraps another function to extend behavior",
        "a class inheritance trick", "a type annotation"], 1),
    _q("py-a2", "advanced", "What does the GIL limit in CPython?",
       ["memory usage", "true parallelism of threads", "recursion depth", "import speed"], 1),
    _q("py-a3", "advanced", "What is the main purpose of __slots__ in a class?",
       ["to make attributes private", "to restrict and speed up attribute storage",
        "to enable multiple inheritance", "to define class methods"], 1),
    _q("py-a4", "advanced", "What is risky about def f(items=[])?",
       ["nothing", "the default list is shared across calls",
        "it raises SyntaxError", "it is slower than None"], 1),
]


class StaticQuestionBank:
    def __init__(self, questions: list[Question] | None = None) -> None:
        self._questions = questions if questions is not None else list(_BANK)
        self._by_id = {q.id: q for q in self._questions}

    def topics(self) -> list[str]:
        return sorted({q.topic for q in self._questions})

    def questions(self, topic: str, level: str, count: int) -> list[Question]:
        pool = [q for q in self._questions if q.topic == topic and q.level == level]
        return pool[:count]

    def get(self, question_id: str) -> Question | None:
        return self._by_id.get(question_id)
