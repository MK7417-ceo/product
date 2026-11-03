"""1v1 skill battles — pure domain logic (no I/O, no framework).

Rules (user-approved, Nov 1 2026):
- Level-matched: a beginner NEVER faces an intermediate/advanced/expert.
  Levels collapse into 3 brackets: beginner | intermediate | advanced
  (advanced + expert both play in the advanced bracket).
- Same questions, same time window: both players get the identical question
  set; the window is 3-5 minutes (default 180s).
- Scoring = speed + accuracy: each correct answer is worth 100 points plus
  a speed bonus of up to 50 points that decays linearly across the window.
  A tie on points is broken by lower total answer time; a full tie is a draw.
- Rewards: winner +30 coins, loser +5 practice coins, draw = +5 each.
  (Coins move through the real coin ledger; there is no XP wallet or badge
  system in the app yet, so no XP/badge is claimed — see REPORT notes.)
- Anti-cheat (submission-similarity basics, heuristic — NOT proof):
  identical answer vectors are only suspicious when they share WRONG
  answers (two strong players both going all-correct is plausible) AND the
  timing lines up. An impossibly fast all-correct run is also flagged.
  A flagged battle still counts as played, but coins are WITHHELD pending
  review — the flag is stored on the battle, never silently dropped.
"""
from __future__ import annotations

from dataclasses import dataclass

# ---- brackets ----

BRACKETS = ("beginner", "intermediate", "advanced")

_LEVEL_TO_BRACKET: dict[str, str] = {
    "beginner": "beginner",
    "intermediate": "intermediate",
    "advanced": "advanced",
    "expert": "advanced",
}


def bracket_for(level: str) -> str:
    """Collapse a declared level into its matchmaking bracket.

    Raises ValueError for unknown levels — callers map this to 400.
    """
    bracket = _LEVEL_TO_BRACKET.get((level or "").strip().lower())
    if bracket is None:
        raise ValueError(f"unknown level: {level}")
    return bracket


# ---- window + questions ----

DEFAULT_WINDOW_SECONDS = 180
ALLOWED_WINDOWS = (180, 240, 300)
BATTLE_QUESTION_COUNT = 5
MIN_QUESTIONS = 3
QUEUE_EXPIRY_SECONDS = 600
CHALLENGE_EXPIRY_SECONDS = 24 * 3600

WINNER_COINS = 30
PARTICIPATION_COINS = 5

BASE_POINTS = 100
MAX_SPEED_BONUS = 50


def pick_questions(pool: list, battle_id: str) -> list:
    """Deterministically pick up to BATTLE_QUESTION_COUNT questions.

    Both players MUST see the same set: the pick is seeded by battle id,
    so re-deriving it later gives the identical set. Raises ValueError
    when the pool is too small to run a fair battle.
    """
    import random

    if len(pool) < MIN_QUESTIONS:
        raise ValueError(
            f"not enough questions for a battle: have {len(pool)}, "
            f"need at least {MIN_QUESTIONS}")
    rng = random.Random(battle_id)
    shuffled = list(pool)
    rng.shuffle(shuffled)
    return shuffled[:BATTLE_QUESTION_COUNT]


# ---- scoring ----

@dataclass(frozen=True)
class PlayerScore:
    correct: int
    total: int
    points: int
    total_time: float  # seconds, summed over answered questions


def score_player(answers: dict, answer_times: dict, correct_map: dict,
                 window_seconds: int) -> PlayerScore:
    """Score one player's submission.

    answers: {question_id: chosen_index}; answer_times: {question_id:
    seconds-since-battle-start} (optional — missing times earn no bonus).
    correct_map: {question_id: correct_index}. Unknown question ids and
    out-of-window times are ignored, never scored.
    """
    correct = 0
    points = 0
    total_time = 0.0
    for qid, correct_idx in correct_map.items():
        given = answers.get(qid)
        if given is None or given != correct_idx:
            continue
        correct += 1
        points += BASE_POINTS
        t = answer_times.get(qid)
        if isinstance(t, (int, float)) and 0 <= t <= window_seconds:
            total_time += float(t)
            bonus = round(MAX_SPEED_BONUS * (1 - t / window_seconds))
            points += max(0, bonus)
    return PlayerScore(correct=correct, total=len(correct_map),
                       points=points, total_time=total_time)


def decide_winner(score1: PlayerScore, score2: PlayerScore) -> int:
    """Return 1 if player 1 wins, 2 if player 2 wins, 0 for a draw."""
    if score1.points != score2.points:
        return 1 if score1.points > score2.points else 2
    if score1.total_time != score2.total_time:
        return 1 if score1.total_time < score2.total_time else 2
    return 0


# ---- anti-cheat (heuristic basics) ----

@dataclass(frozen=True)
class CheatFlag:
    flagged: bool
    reason: str = ""


# All-correct in under 3s per question on average: not humanly plausible
# for reading + answering MCQs.
IMPOSSIBLE_SECONDS_PER_QUESTION = 3.0
# Copy tell: identical vectors AND per-question times within this many
# seconds of each other (or total times within this window).
COPY_TIME_TOLERANCE = 3.0
COPY_TOTAL_TOLERANCE = 5.0


def check_submission(answers1: dict, times1: dict,
                     answers2: dict, times2: dict,
                     correct_map: dict) -> CheatFlag:
    """Heuristic similarity check between the two submissions.

    Flags ONLY when there is something genuinely suspicious:
    - IMPOSSIBLE_SPEED: a player answered everything correctly in
      under 3s/question on average.
    - COPY_PATTERN: identical answer vectors that share at least one
      WRONG answer, with closely matching timing.
    Identical all-correct runs by two strong players are NOT flagged.
    """
    qids = sorted(correct_map)
    if not qids:
        return CheatFlag(False)

    for answers, times in ((answers1, times1), (answers2, times2)):
        answered = [q for q in qids if answers.get(q) is not None]
        if not answered:
            continue
        if all(answers.get(q) == correct_map[q] for q in answered):
            total = sum(float(times.get(q, 0) or 0) for q in answered)
            if total < IMPOSSIBLE_SECONDS_PER_QUESTION * len(answered):
                return CheatFlag(
                    True,
                    "impossible_speed: all-correct run faster than "
                    "3s/question on average")

    vec1 = [answers1.get(q) for q in qids]
    vec2 = [answers2.get(q) for q in qids]
    if vec1 != vec2 or all(v is None for v in vec1):
        return CheatFlag(False)
    shared_wrong = any(
        v is not None and v != correct_map[q]
        for q, v in zip(qids, vec1))
    if not shared_wrong:
        return CheatFlag(False)
    per_q_close = all(
        abs(float(times1.get(q, 0) or 0) - float(times2.get(q, 0) or 0))
        <= COPY_TIME_TOLERANCE for q in qids)
    total1 = sum(float(times1.get(q, 0) or 0) for q in qids)
    total2 = sum(float(times2.get(q, 0) or 0) for q in qids)
    if per_q_close or abs(total1 - total2) <= COPY_TOTAL_TOLERANCE:
        return CheatFlag(
            True,
            "copy_pattern: identical answers incl. shared wrong answers "
            "with matching timing")
    return CheatFlag(False)


FAIR_PLAY_RULES = (
    "1v1 battles are level-matched: beginners only face beginners, "
    "intermediates only intermediates, advanced/expert players share the "
    "advanced bracket. Both players answer the same questions in the same "
    "time window. Scoring rewards accuracy first, then speed. "
    "Copying is checked: identical answers with shared wrong answers and "
    "matching timing, or an impossibly fast all-correct run, flags the "
    "battle and withholds coins pending review. A flagged battle still "
    "counts as played. No bots: every opponent is a real user — if nobody "
    "is waiting in your bracket, you wait in queue; you are never matched "
    "against a fake player."
)
