"""Domain: English/IELTS track. PURE.

Daily English set (vocabulary + grammar + comprehension), deterministic
per user+day — same pattern as practice.py. Answer keys never leave the
server; scoring is server-side.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from app.domain.user import DomainError

DAILY_COUNT = 5


@dataclass(frozen=True)
class EnglishQuestion:
    id: str
    kind: str  # vocabulary | grammar | comprehension
    level: str
    prompt: str
    choices: tuple[str, ...]
    answer_index: int
    passage: str = ""  # for comprehension


def _q(qid: str, kind: str, level: str, prompt: str, choices: list[str],
       answer: int, passage: str = "") -> EnglishQuestion:
    if not 0 <= answer < len(choices):
        raise DomainError("bad answer index")
    return EnglishQuestion(id=qid, kind=kind, level=level, prompt=prompt,
                           choices=tuple(choices), answer_index=answer,
                           passage=passage)


BANK: list[EnglishQuestion] = [
    # ---- vocabulary ----
    _q("en-v1", "vocabulary", "beginner",
       "Choose the synonym of 'rapid'.", ["slow", "fast", "steady", "late"], 1),
    _q("en-v2", "vocabulary", "beginner",
       "Choose the antonym of 'ancient'.", ["old", "modern", "historic", "classic"], 1),
    _q("en-v3", "vocabulary", "intermediate",
       "Choose the synonym of 'meticulous'.", ["careless", "thorough", "hasty", "vague"], 1),
    _q("en-v4", "vocabulary", "intermediate",
       "'Ubiquitous' means:", ["rare", "present everywhere", "expensive", "hidden"], 1),
    _q("en-v5", "vocabulary", "advanced",
       "Choose the synonym of 'pragmatic'.", ["idealistic", "practical", "emotional", "rigid"], 1),
    _q("en-v6", "vocabulary", "advanced",
       "'Ephemeral' means:", ["eternal", "short-lived", "transparent", "fragile"], 1),
    # ---- grammar ----
    _q("en-g1", "grammar", "beginner",
       "Choose the correct sentence.",
       ["She go to school daily.", "She goes to school daily.",
        "She going to school daily.", "She gone to school daily."], 1),
    _q("en-g2", "grammar", "beginner",
       "Fill in: 'I have lived here ___ 2019.'", ["since", "for", "from", "at"], 0),
    _q("en-g3", "grammar", "intermediate",
       "Choose the correct sentence.",
       ["Neither of the answers are correct.", "Neither of the answers is correct.",
        "Neither of the answer is correct.", "Neither of answers is correct."], 1),
    _q("en-g4", "grammar", "intermediate",
       "Fill in: 'Hardly ___ reached home when it rained.'", ["I had", "had I", "I have", "have I"], 1),
    _q("en-g5", "grammar", "advanced",
       "Choose the correct sentence.",
       ["The committee were divided in its opinion.",
        "The committee was divided in their opinions.",
        "The committee were divided in their opinions.",
        "The committee was divided in its opinion."], 3),
    _q("en-g6", "grammar", "advanced",
       "Fill in: 'No sooner ___ the news than she called.'",
       ["she heard", "had she heard", "did she heard", "she had heard"], 1),
    # ---- comprehension ----
    _q("en-c1", "comprehension", "intermediate",
       "What is the main challenge described?",
       ["Lack of funding", "Balancing speed with correctness",
        "Hiring engineers", "Choosing a database"], 1,
       passage=("Startups often face a dilemma: move fast to capture the market, "
                "or move carefully to avoid costly mistakes. The most successful "
                "teams find a rhythm — shipping small, reversible changes quickly "
                "while slowing down for irreversible decisions.")),
    _q("en-c2", "comprehension", "intermediate",
       "According to the passage, what should teams slow down for?",
       ["Small changes", "Hiring", "Irreversible decisions", "Meetings"], 2,
       passage=("Startups often face a dilemma: move fast to capture the market, "
                "or move carefully to avoid costly mistakes. The most successful "
                "teams find a rhythm — shipping small, reversible changes quickly "
                "while slowing down for irreversible decisions.")),
    _q("en-c3", "comprehension", "advanced",
       "What does 'cognitive offloading' refer to here?",
       ["Forgetting things deliberately", "Relying on tools to store information",
        "Multitasking efficiently", "Meditation techniques"], 1,
       passage=("Cognitive offloading — relying on phones and notebooks to store "
                "information — frees working memory for harder problems. But "
                "over-reliance can weaken recall: the brain treats externally "
                "stored facts as 'known', even when they cannot be retrieved "
                "without the tool.")),
    _q("en-c4", "comprehension", "advanced",
       "What is the risk of over-reliance mentioned?",
       ["Slower phones", "Weaker recall without the tool",
        "Higher costs", "Less creativity"], 1,
       passage=("Cognitive offloading — relying on phones and notebooks to store "
                "information — frees working memory for harder problems. But "
                "over-reliance can weaken recall: the brain treats externally "
                "stored facts as 'known', even when they cannot be retrieved "
                "without the tool.")),
]

_BY_ID = {q.id: q for q in BANK}
assert len(_BY_ID) == len(BANK), "duplicate english question ids"


def public(q: EnglishQuestion) -> dict:
    return {"id": q.id, "kind": q.kind, "level": q.level,
            "prompt": q.prompt, "choices": list(q.choices),
            "passage": q.passage}


def daily_set(user_id: str, date: str, count: int = DAILY_COUNT) -> list[dict]:
    """Deterministic daily English set. Same user+day -> same questions."""
    if not user_id:
        raise DomainError("user_id required")
    if len(date) != 10:
        raise DomainError("date must be YYYY-MM-DD")
    # spread kinds: 2 vocab, 2 grammar, 1 comprehension
    kinds = ["vocabulary", "vocabulary", "grammar", "grammar", "comprehension"]
    rng = random.Random(f"en:{user_id}:{date}:v1")
    picked: list[EnglishQuestion] = []
    for kind in kinds[:count]:
        pool = [q for q in BANK if q.kind == kind and q not in picked]
        picked.append(rng.choice(pool))
    return [public(q) for q in picked]


def score(user_id: str, date: str, answers: dict[str, int]) -> tuple[int, int]:
    """Server-side scoring against the deterministic set."""
    rng = random.Random(f"en:{user_id}:{date}:v1")
    kinds = ["vocabulary", "vocabulary", "grammar", "grammar", "comprehension"]
    picked: list[EnglishQuestion] = []
    for kind in kinds:
        pool = [q for q in BANK if q.kind == kind and q not in picked]
        picked.append(rng.choice(pool))
    ids = {q.id for q in picked}
    if set(answers) - ids:
        raise DomainError("answers contain unknown question ids")
    correct = sum(1 for q in picked if answers.get(q.id) == q.answer_index)
    return correct, len(picked)
