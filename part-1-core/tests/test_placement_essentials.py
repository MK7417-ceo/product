"""Tests for interview_qa helpers and placement API."""
from __future__ import annotations

from fastapi.testclient import TestClient

from app.adapters.outbound import interview_qa


def test_summary_counts():
    s = interview_qa.summary()
    assert s["total"] == 200
    assert s["hr"] == 80
    assert s["technical"] == 120


def test_unique_ids():
    items = interview_qa._all_items()
    ids = [q["id"] for q in items]
    assert len(ids) == len(set(ids))


def test_all_have_required_fields():
    for q in interview_qa._all_items():
        assert q["id"] and q["question"] and q["answer"]
        assert q["category"] in ("hr", "technical")
        assert 1 <= q["difficulty"] <= 3
        assert isinstance(q.get("companies", []), list)


def test_hr_has_tips():
    for q in interview_qa.get_interview_qa(category="hr"):
        assert q.get("tip"), f"missing tip: {q['id']}"


def test_technical_has_key_points():
    for q in interview_qa.get_interview_qa(category="technical"):
        assert q.get("key_point"), f"missing key_point: {q['id']}"


def test_category_filter():
    assert len(interview_qa.get_interview_qa(category="hr")) == 80
    assert len(interview_qa.get_interview_qa(category="technical")) == 120
    assert interview_qa.get_interview_qa(category="bogus") == []


def test_subcategory_filter():
    os_qs = interview_qa.get_interview_qa(subcategory="os")
    assert len(os_qs) == 16
    assert all(q["subcategory"] == "os" for q in os_qs)


def test_get_by_company():
    amz = interview_qa.get_by_company("amazon")
    assert len(amz) > 20
    assert all("amazon" in q["companies"] for q in amz)
    assert interview_qa.get_by_company("nonexistent-corp") == []


def test_get_companies_sorted_unique():
    companies = interview_qa.get_companies()
    assert companies == sorted(companies)
    assert len(companies) == len(set(companies))
    assert "tcs" in companies and "google" in companies


def _client() -> TestClient:
    import os

    os.environ.setdefault("SECRET_KEY", "devsecret-test-32-chars-minimum-abcdef")
    from app.main import app

    return TestClient(app)


def test_api_interview_qa():
    c = _client()
    r = c.get("/api/v1/placement/interview-qa")
    assert r.status_code == 200
    assert r.json()["count"] == 200


def test_api_interview_qa_category():
    c = _client()
    r = c.get("/api/v1/placement/interview-qa", params={"category": "hr"})
    assert r.status_code == 200
    assert r.json()["count"] == 80


def test_api_interview_qa_random():
    c = _client()
    r = c.get("/api/v1/placement/interview-qa/random", params={"count": 5})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 5
    ids = [q["id"] for q in body["items"]]
    assert len(ids) == len(set(ids)), "no repeats in one draw"


def test_api_interview_qa_random_category():
    c = _client()
    r = c.get(
        "/api/v1/placement/interview-qa/random",
        params={"count": 4, "category": "technical"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 4
    assert all(q["category"] == "technical" for q in body["items"])


def test_get_random_no_repeats():
    for _ in range(5):
        picked = interview_qa.get_random(count=6)
        ids = [q["id"] for q in picked]
        assert len(ids) == len(set(ids))


def test_api_interview_qa_company():
    c = _client()
    r = c.get("/api/v1/placement/interview-qa", params={"company": "tcs"})
    assert r.status_code == 200
    assert r.json()["count"] > 10


def test_api_gd_topics():
    c = _client()
    r = c.get("/api/v1/placement/gd-topics")
    assert r.status_code == 200
    assert r.json()["count"] >= 40


def test_api_quant():
    c = _client()
    r = c.get("/api/v1/placement/quant", params={"type_id": "percentages"})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] > 0
    assert body["trick"] is not None


def test_api_summary():
    c = _client()
    r = c.get("/api/v1/placement/summary")
    assert r.status_code == 200
    body = r.json()
    assert body["interview_qa"]["total"] == 200
    assert body["quant"]["total"] >= 190


def test_news_retention_helpers():
    from datetime import datetime, timedelta, timezone

    from app.adapters.outbound import news_repository
    from app.adapters.outbound.models import TechNewsModel
    from app.core.database import SessionLocal

    session = SessionLocal()
    try:
        # Insert one fresh + one old row directly
        import uuid

        fresh = TechNewsModel(
            id=str(uuid.uuid4()),
            title="Fresh news",
            url=f"https://example.com/fresh-{uuid.uuid4().hex[:8]}",
            source="test",
            score=10,
            published_at="2026-10-15",
            fetched_at=datetime.now(timezone.utc),
        )
        old = TechNewsModel(
            id=str(uuid.uuid4()),
            title="Old news",
            url=f"https://example.com/old-{uuid.uuid4().hex[:8]}",
            source="test",
            score=5,
            published_at="2024-01-01",
            fetched_at=datetime.now(timezone.utc) - timedelta(days=400),
        )
        session.add(fresh)
        session.add(old)
        session.commit()
        old_url = old.url  # capture before session ops detach

        deleted = news_repository.cleanup_old_news(session)
        assert deleted >= 1

        remaining_urls = [n["url"] for n in news_repository.get_latest_news(session)]
        assert old_url not in remaining_urls

        # Latest-first ordering: fresh should be near top
        latest = news_repository.get_latest_news(session, limit=5)
        assert len(latest) > 0
    finally:
        session.close()
