"""P2b tests: plagiarism similarity — flag-only, deterministic, no LLM."""
import pytest
from fastapi.testclient import TestClient

from app.domain.plagiarism import check, fingerprint, normalize, similarity
from app.main import create_app

ORIG = '''def solve(nums):
    total = 0
    for n in nums:
        total = total + n
    return total
'''

RENAMED = '''def compute(values):  # renamed everything
    result = 0
    for v in values:
        result = result + v
    return result
'''

DIFFERENT = '''def solve(nums):
    return sum(x * x for x in nums if x > 0)
'''

BOILER = "def solve(nums):\n"
SOL_A = BOILER + "    return sum(nums)\n"
SOL_B = BOILER + "    s = 0\n    for x in nums:\n        s += x\n    return s\n"

client = TestClient(create_app())


def test_identical_code_scores_one_and_flags():
    score, _ = similarity(ORIG, ORIG, "python")
    assert score == 1.0
    v = check(ORIG, [{"id": "c1", "code": ORIG}], "python")[0]
    assert v.flagged is True
    assert any("human review" in r for r in v.reasons)


def test_renamed_identifiers_still_flagged():
    score, _ = similarity(ORIG, RENAMED, "python")
    assert score >= 0.85, score


def test_different_logic_not_flagged():
    score, _ = similarity(ORIG, DIFFERENT, "python")
    assert score < 0.85, score
    v = check(ORIG, [{"id": "c1", "code": DIFFERENT}], "python")[0]
    assert v.flagged is False
    assert v.reasons == ()


def test_boilerplate_excluded():
    # same starter, different solutions -> must NOT flag
    score, _ = similarity(SOL_A, SOL_B, "python", boilerplate=BOILER)
    assert score < 0.85, score
    # but without the exclusion the shared starter inflates the score
    raw, _ = similarity(SOL_A, SOL_B, "python")
    assert raw > score


def test_comments_and_whitespace_ignored():
    noisy = "# a comment\n\n\n" + ORIG.replace("total = 0", "total=0  # inline")
    score, _ = similarity(ORIG, noisy, "python")
    assert score == 1.0


def test_string_literals_folded():
    a = 'print("hello")\n'
    b = 'print("goodbye")\n'
    score, _ = similarity(a, b, "python")
    assert score == 1.0


def test_cpp_renamed_variables_flagged():
    a = "int main(){ int total = 0; for(int i=0;i<10;i++){ total += i; } return total; }"
    b = "int main(){ int sum = 0; for(int j=0;j<10;j++){ sum += j; } return sum; }"
    score, _ = similarity(a, b, "cpp")
    assert score >= 0.85, score


def test_fingerprint_deterministic():
    assert fingerprint(ORIG, "python") == fingerprint(ORIG, "python")


def test_normalize_canonicalizes_identifiers():
    toks = normalize("def f(abc, xyz):\n    return abc + xyz\n", "python")
    assert "v1" in toks and "v2" in toks
    assert "abc" not in toks and "xyz" not in toks


def test_api_plagiarism_check():
    r = client.post("/v1/plagiarism/check", json={
        "language": "python",
        "code": ORIG,
        "candidates": [{"id": "renamed", "code": RENAMED},
                       {"id": "other", "code": DIFFERENT}],
    })
    assert r.status_code == 200, r.text
    res = {x["candidate_id"]: x for x in r.json()["results"]}
    assert res["renamed"]["flagged"] is True
    assert res["other"]["flagged"] is False
    assert "ngram_hash" in res["renamed"]["fingerprint_a"]


def test_api_rejects_bad_input():
    r = client.post("/v1/plagiarism/check", json={
        "language": "rust", "code": "x", "candidates": [{"id": "a", "code": "y"}]})
    assert r.status_code == 400
    r = client.post("/v1/plagiarism/check", json={
        "language": "python", "code": "x", "candidates": []})
    assert r.status_code == 400
