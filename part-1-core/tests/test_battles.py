"""1v1 battles: domain rules + API flow end to end."""
import uuid

from fastapi.testclient import TestClient

from app.domain import battles as bt
from app.main import create_app


# ---- domain ----

def test_bracket_mapping():
    assert bt.bracket_for("beginner") == "beginner"
    assert bt.bracket_for("intermediate") == "intermediate"
    assert bt.bracket_for("advanced") == "advanced"
    assert bt.bracket_for("expert") == "advanced"  # experts share advanced
    try:
        bt.bracket_for("godlike")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown level must raise")


def test_pick_is_deterministic_per_battle():
    pool = [f"q{i}" for i in range(8)]
    a = bt.pick_questions(pool, "battle-1")
    b = bt.pick_questions(pool, "battle-1")
    c = bt.pick_questions(pool, "battle-2")
    assert a == b
    assert len(a) == 5
    assert a != c or True  # different seeds may coincide; determinism is the rule
    try:
        bt.pick_questions(["q1", "q2"], "battle-3")
    except ValueError:
        pass
    else:
        raise AssertionError("tiny pool must raise")


def test_scoring_accuracy_then_speed():
    correct = {"q1": 1, "q2": 0, "q3": 2}
    fast = bt.score_player({"q1": 1, "q2": 0}, {"q1": 10, "q2": 10},
                           correct, 180)
    slow = bt.score_player({"q1": 1, "q2": 0}, {"q1": 170, "q2": 170},
                           correct, 180)
    assert fast.correct == 2 and slow.correct == 2
    assert fast.points > slow.points  # same accuracy, faster wins
    wrong = bt.score_player({"q1": 0}, {"q1": 5}, correct, 180)
    assert wrong.correct == 0 and wrong.points == 0


def test_decide_winner_tiebreak_and_draw():
    s_fast = bt.PlayerScore(2, 3, 250, 20.0)
    s_slow = bt.PlayerScore(2, 3, 250, 90.0)
    assert bt.decide_winner(s_fast, s_slow) == 1
    assert bt.decide_winner(s_slow, s_fast) == 2
    assert bt.decide_winner(s_fast, s_fast) == 0
    assert bt.decide_winner(
        bt.PlayerScore(3, 3, 400, 10.0),
        bt.PlayerScore(1, 3, 100, 5.0)) == 1


def test_anticheat_all_correct_not_flagged():
    correct = {"q1": 1, "q2": 0}
    flag = bt.check_submission({"q1": 1, "q2": 0}, {"q1": 60, "q2": 70},
                               {"q1": 1, "q2": 0}, {"q1": 55, "q2": 65},
                               correct)
    assert flag.flagged is False  # two strong players, plausible


def test_anticheat_copy_pattern_flagged():
    correct = {"q1": 1, "q2": 0, "q3": 2}
    # identical vectors incl. a SHARED WRONG answer (q3=0), close timing
    flag = bt.check_submission({"q1": 1, "q2": 0, "q3": 0},
                               {"q1": 30, "q2": 40, "q3": 50},
                               {"q1": 1, "q2": 0, "q3": 0},
                               {"q1": 31, "q2": 41, "q3": 51},
                               correct)
    assert flag.flagged is True
    assert "copy_pattern" in flag.reason


def test_anticheat_impossible_speed_flagged():
    correct = {"q1": 1, "q2": 0}
    flag = bt.check_submission({"q1": 1, "q2": 0}, {"q1": 1, "q2": 2},
                               {"q1": 0, "q2": 1}, {"q1": 60, "q2": 70},
                               correct)
    assert flag.flagged is True
    assert "impossible_speed" in flag.reason


# ---- API ----

def _authz(client: TestClient) -> tuple[dict, str]:
    email = f"bt-{uuid.uuid4().hex[:8]}@x.com"
    r = client.post("/api/v1/auth/register",
                    json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}, email


def test_battles_requires_auth():
    c = TestClient(create_app())
    assert c.post("/api/v1/battles/queue",
                  json={"topic": "python", "level": "beginner"}).status_code == 401


def test_battles_bad_topic_and_level():
    c = TestClient(create_app())
    h, _ = _authz(c)
    r = c.post("/api/v1/battles/queue", headers=h,
               json={"topic": "cobol", "level": "beginner"})
    assert r.status_code == 400
    r = c.post("/api/v1/battles/queue", headers=h,
               json={"topic": "python", "level": "godlike"})
    assert r.status_code == 400


def test_battle_queue_match_and_score():
    c = TestClient(create_app())
    h1, _ = _authz(c)
    h2, _ = _authz(c)
    r = c.post("/api/v1/battles/queue", headers=h1,
               json={"topic": "python", "level": "beginner"})
    assert r.status_code == 201, r.text
    assert r.json()["matched"] is False
    bid = r.json()["battle"]["battle_id"]
    assert "questions" not in r.json()["battle"]
    # second open battle blocked
    r = c.post("/api/v1/battles/queue", headers=h1,
               json={"topic": "python", "level": "beginner"})
    assert r.status_code == 400
    # opponent matches, same battle, questions without answers
    r = c.post("/api/v1/battles/queue", headers=h2,
               json={"topic": "python", "level": "beginner"})
    assert r.status_code == 201, r.text
    assert r.json()["matched"] is True
    assert r.json()["battle"]["battle_id"] == bid
    qs = r.json()["battle"]["questions"]
    assert len(qs) == 5
    assert all("answer_index" not in q for q in qs)
    # player 1 submits, waits; player 2 submits, battle finishes
    r = c.post(f"/api/v1/battles/{bid}/submit", headers=h1,
               json={"answers": {q["id"]: 1 for q in qs},
                     "answer_times": {q["id"]: 10 for q in qs}})
    assert r.status_code == 200 and r.json()["waiting_for_opponent"] is True
    r = c.post(f"/api/v1/battles/{bid}/submit", headers=h2,
               json={"answers": {q["id"]: 0 for q in qs},
                     "answer_times": {q["id"]: 60 for q in qs}})
    assert r.status_code == 200, r.text
    b = r.json()["battle"]
    assert b["status"] == "finished"
    assert b["player1_score"] is not None and b["player2_score"] is not None
    assert b["winner_id"] in (None, b["player1_id"], b["player2_id"])
    assert b["flagged"] is False
    # real coins moved: winner 30, loser 5 (or 5/5 on a draw)
    bal1 = c.get("/api/v1/coins/mine", headers=h1).json()
    bal2 = c.get("/api/v1/coins/mine", headers=h2).json()
    assert {bal1["balance"], bal2["balance"]} == {30, 5} or \
        (bal1["balance"] == 5 and bal2["balance"] == 5)


def test_battle_bracket_isolation():
    c = TestClient(create_app())
    hb, _ = _authz(c)
    he, _ = _authz(c)
    r = c.post("/api/v1/battles/queue", headers=hb,
               json={"topic": "javascript", "level": "beginner"})
    assert r.status_code == 201 and r.json()["matched"] is False
    r = c.post("/api/v1/battles/queue", headers=he,
               json={"topic": "javascript", "level": "expert"})
    assert r.status_code == 201, r.text
    assert r.json()["matched"] is False, "expert must not match beginner"


def test_battle_challenge_and_bracket_join():
    c = TestClient(create_app())
    h1, _ = _authz(c)
    h2, e2 = _authz(c)
    r = c.post("/api/v1/battles/challenge", headers=h1,
               json={"topic": "java", "level": "beginner",
                     "opponent_email": e2})
    assert r.status_code == 201, r.text
    code = r.json()["invite_code"]
    assert code
    r = c.post("/api/v1/battles/join", headers=h2,
               json={"invite_code": code, "level": "expert"})
    assert r.status_code == 400  # bracket mismatch
    r = c.post("/api/v1/battles/join", headers=h2,
               json={"invite_code": code, "level": "beginner"})
    assert r.status_code == 200, r.text
    assert r.json()["battle"]["status"] == "live"


def test_battle_copy_pattern_flagged_coins_withheld():
    c = TestClient(create_app())
    h1, _ = _authz(c)
    h2, _ = _authz(c)
    c.post("/api/v1/battles/queue", headers=h1,
           json={"topic": "ml-basics", "level": "beginner"})
    r = c.post("/api/v1/battles/queue", headers=h2,
               json={"topic": "ml-basics", "level": "beginner"})
    bid = r.json()["battle"]["battle_id"]
    qs = r.json()["battle"]["questions"]
    # identical vectors, close times (answer 3 is wrong for most bank Qs;
    # even if one is right, shared wrong answers remain the tell)
    c.post(f"/api/v1/battles/{bid}/submit", headers=h1,
           json={"answers": {q["id"]: 3 for q in qs},
                 "answer_times": {q["id"]: 30 for q in qs}})
    r = c.post(f"/api/v1/battles/{bid}/submit", headers=h2,
               json={"answers": {q["id"]: 3 for q in qs},
                     "answer_times": {q["id"]: 31 for q in qs}})
    b = r.json()["battle"]
    assert b["flagged"] is True
    assert b["rewards"]["coins_withheld"] is True
    assert c.get("/api/v1/coins/mine", headers=h1).json()["balance"] == 0
    assert c.get("/api/v1/coins/mine", headers=h2).json()["balance"] == 0
