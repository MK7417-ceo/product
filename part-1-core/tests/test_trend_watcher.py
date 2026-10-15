"""Tests: trend watcher (pure domain) + new-domain migration data validation."""
import importlib.util

from app.domain.trend_watcher import (
    TechCandidate,
    TrendingRepo,
    detect_new_tech,
    fetch_trending_repos,
    normalize_tech,
    run_weekly_check,
    suggest_domain,
    suggest_modules,
)


class _FakeResp:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {"items": []}

    def json(self):
        return self._payload


class _FakeClient:
    def __init__(self, resp=None, exc=None):
        self._resp = resp or _FakeResp()
        self._exc = exc

    def get(self, *a, **k):
        if self._exc:
            raise self._exc
        return self._resp


def _repo(**kw):
    d = dict(name="x", full_name="u/x", description="", language=None,
             stars=100, topics=[])
    d.update(kw)
    return TrendingRepo(**d)


# ---------- fetch ----------

def test_fetch_returns_empty_on_connection_error():
    repos = fetch_trending_repos(client=_FakeClient(exc=ConnectionError("down")))
    assert repos == []


def test_fetch_returns_empty_on_bad_status():
    repos = fetch_trending_repos(client=_FakeClient(_FakeResp(status_code=403)))
    assert repos == []


def test_fetch_parses_repos():
    payload = {"items": [{
        "name": "bun", "full_name": "oven-sh/bun",
        "description": "Fast JS runtime", "language": "Zig",
        "stargazers_count": 70000, "topics": ["runtime", "javascript"],
    }]}
    repos = fetch_trending_repos(client=_FakeClient(_FakeResp(payload=payload)))
    assert len(repos) == 1
    assert repos[0].language == "Zig"
    assert repos[0].stars == 70000
    assert "runtime" in repos[0].topics


def test_fetch_handles_garbage_payload():
    repos = fetch_trending_repos(client=_FakeClient(_FakeResp(payload=None)))
    assert repos == []


# ---------- detect ----------

def test_known_slug_is_filtered():
    repos = [_repo(language="Python", full_name="psf/requests", stars=50000)]
    out = detect_new_tech(["python", "dsa"], repos=repos)
    assert all(c.id != "python" for c in out)


def test_new_language_detected_as_candidate():
    repos = [_repo(name="bun", full_name="oven-sh/bun", language="Zig",
                   description="Bun is a fast runtime", stars=60000,
                   topics=["bun", "runtime"])]
    out = detect_new_tech(["python", "dsa", "rust"], repos=repos)
    ids = {c.id for c in out}
    assert "bun" in ids
    bun = next(c for c in out if c.id == "bun")
    assert "Trending on GitHub" in bun.reason
    assert bun.stars >= 60000


def test_stopwords_never_become_candidates():
    repos = [_repo(name="awesome-python", full_name="u/awesome-python",
                   description="awesome list of tutorials", stars=90000)]
    out = detect_new_tech(["dsa"], repos=repos)
    assert all(c.id not in {"awesome", "tutorial", "tutorials", "list"} for c in out)


def test_detect_never_raises_on_bad_input():
    assert detect_new_tech([], repos=None, client=_FakeClient(exc=RuntimeError("x"))) == []
    assert run_weekly_check(["python"], client=_FakeClient(exc=RuntimeError("x"))) == []


def test_candidates_sorted_by_stars_desc():
    repos = [
        _repo(language="Zig", full_name="u/a", stars=1000),
        _repo(language="Mojo", full_name="u/b", stars=9000),
    ]
    out = detect_new_tech(["python"], repos=repos)
    stars = [c.stars for c in out]
    assert stars == sorted(stars, reverse=True)


# ---------- suggest ----------

def test_suggest_domain_shape():
    c = TechCandidate(id="bun", name="Bun", category="tech-domain",
                      reason="trending", stars=1000, repo="oven-sh/bun")
    d = suggest_domain(c)
    assert d["slug"] == "bun"
    assert d["name"] == "Bun"
    assert d["category"] in ("language", "tech-domain")
    assert len(d["modules"]) == 4
    assert all("slug" in m and "name" in m for m in d["modules"])


def test_suggest_modules_generic_outline():
    mods = suggest_modules("Bun")
    assert len(mods) == 4
    assert mods[0]["slug"] == "fundamentals"


def test_normalize_tech():
    assert normalize_tech("C++") == "c"
    assert normalize_tech("Node.js") == "nodejs"
    assert normalize_tech("  Scikit-Learn ") == "scikitlearn"


# ---------- migration data ----------

def _load_migration():
    path = "alembic/versions/n3o4trend001_new_domains.py"
    spec = importlib.util.spec_from_file_location("trend_mig", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_migration_has_five_new_domains():
    mod = _load_migration()
    slugs = [d[0] for d in mod.NEW_DOMAINS]
    assert slugs == ["aws", "java-advanced", "big-data", "system-design", "git-github"]


def test_migration_starter_questions_20_per_domain():
    mod = _load_migration()
    from collections import Counter
    counts = Counter(q[0] for q in mod.STARTER_QUESTIONS)
    assert len(mod.STARTER_QUESTIONS) == 100
    for slug in ["aws", "java-advanced", "big-data", "system-design", "git-github"]:
        assert counts[slug] == 20, f"{slug} has {counts[slug]} questions"


def test_migration_questions_valid():
    mod = _load_migration()
    for i, q in enumerate(mod.STARTER_QUESTIONS):
        domain, module, diff, prompt, choices, ans, expl, companies = q
        assert 1 <= diff <= 5, f"q{i} difficulty {diff}"
        assert len(choices) == 4, f"q{i} choices"
        assert 0 <= ans <= 3, f"q{i} answer_index"
        assert prompt and expl, f"q{i} empty prompt/explanation"
        assert isinstance(companies, list), f"q{i} company_tags"
    # unique prompts
    prompts = [q[3] for q in mod.STARTER_QUESTIONS]
    assert len(set(prompts)) == len(prompts), "duplicate prompts found"
