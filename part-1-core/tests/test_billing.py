"""P3f tests: tiers, subscription API, account links, roadmap tier gate."""
import uuid

import pytest
from fastapi.testclient import TestClient

from app.domain.billing import TIERS, AccountLinks, check_tier, tier_info
from app.domain.user import DomainError
from app.main import create_app


def test_tier_matrix_sane():
    assert set(TIERS) == {"free", "pro", "expert"}
    assert TIERS["free"]["price_inr"] == 0
    assert TIERS["free"]["max_roadmaps"] < TIERS["pro"]["max_roadmaps"]
    for t in TIERS.values():
        assert t["features"]
    assert tier_info("pro")["name"] == "Pro"
    with pytest.raises(DomainError):
        check_tier("nope")


def test_account_links_validation():
    AccountLinks(user_id="u", github="octocat", leetcode="user_1").validate()
    with pytest.raises(DomainError):
        AccountLinks(user_id="u", github="bad handle!").validate()


def _client():
    return TestClient(create_app())


def _register(c: TestClient, prefix: str = "bl") -> tuple[dict, str]:
    email = f"{prefix}-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    body = r.json()
    return ({"Authorization": f"Bearer {body['access_token']}"}, body["user"]["id"])


def _make_admin(c: TestClient, user_id: str):
    # promote via the user repo directly (test-only seam)
    from app.adapters.outbound.user_repository import SqlAlchemyUserRepository
    from app.core.database import SessionLocal
    repo = SqlAlchemyUserRepository(SessionLocal)
    with SessionLocal() as s:
        from app.adapters.outbound.models import UserModel
        m = s.query(UserModel).filter_by(id=user_id).one()
        m.role = "admin"
        s.commit()


def test_subscription_flow():
    c = _client()
    h, uid = _register(c)

    s = c.get("/api/v1/account/subscription", headers=h)
    assert s.status_code == 200, s.text
    body = s.json()
    assert body["subscription"]["tier"] == "free"
    assert set(body["tiers"]) == {"free", "pro", "expert"}

    # checkout is honest: payments not connected
    co = c.post("/api/v1/account/subscription/checkout", headers=h,
                json={"tier": "pro"})
    assert co.status_code == 501
    assert co.json()["error"] == "payments_not_connected"

    co2 = c.post("/api/v1/account/subscription/checkout", headers=h,
                 json={"tier": "nope"})
    assert co2.status_code == 400

    # admin can set tiers
    _make_admin(c, uid)
    st = c.post("/api/v1/account/subscription/set-tier", headers=h,
                json={"user_id": uid, "tier": "pro"})
    assert st.status_code == 200, st.text
    assert st.json()["tier"] == "pro"
    s2 = c.get("/api/v1/account/subscription", headers=h)
    assert s2.json()["subscription"]["tier"] == "pro"

    # non-admin cannot
    h2, _ = _register(c, "bl2")
    st2 = c.post("/api/v1/account/subscription/set-tier", headers=h2,
                 json={"user_id": uid, "tier": "free"})
    assert st2.status_code == 403


def test_links_crud():
    c = _client()
    h, _ = _register(c)

    g = c.get("/api/v1/account/links", headers=h)
    assert g.json() == {"github": "", "linkedin": "", "leetcode": ""}

    p = c.put("/api/v1/account/links", headers=h,
              json={"github": "octocat", "linkedin": "in-octocat",
                    "leetcode": "octo_123"})
    assert p.status_code == 200, p.text
    assert p.json()["github"] == "octocat"

    g2 = c.get("/api/v1/account/links", headers=h)
    assert g2.json()["leetcode"] == "octo_123"

    bad = c.put("/api/v1/account/links", headers=h,
                json={"github": "bad handle!"})
    assert bad.status_code == 400

    assert c.get("/api/v1/account/links").status_code == 401
    assert c.get("/api/v1/account/subscription").status_code == 401


def test_roadmap_tier_gate():
    c = _client()
    h, uid = _register(c)
    gaps = {"gaps": [{"skill": "python-basics", "mastery_pct": 30}]}

    # free tier: 10 roadmaps ok
    for _ in range(10):
        r = c.post("/api/v1/roadmaps/generate", json=gaps, headers=h)
        assert r.status_code == 201, r.text

    # 11th blocked
    r = c.post("/api/v1/roadmaps/generate", json=gaps, headers=h)
    assert r.status_code == 400
    assert "tier_limit" in r.json()["detail"]

    # upgrade -> unblocked
    _make_admin(c, uid)
    c.post("/api/v1/account/subscription/set-tier", headers=h,
           json={"user_id": uid, "tier": "pro"})
    r = c.post("/api/v1/roadmaps/generate", json=gaps, headers=h)
    assert r.status_code == 201, r.text
