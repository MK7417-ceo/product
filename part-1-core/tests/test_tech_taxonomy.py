"""Tests: tech taxonomy data + API."""
from fastapi.testclient import TestClient

from app.adapters.outbound import tech_taxonomy as tx


def test_tool_count_at_least_60():
    assert tx.tool_count() >= 60, f"only {tx.tool_count()} tools"


def test_importance_values_valid():
    for t in tx.list_tools():
        assert t["importance"] in tx.VALID_IMPORTANCE, t


def test_slugs_unique():
    slugs = [t["slug"] for t in tx.list_tools()]
    assert len(slugs) == len(set(slugs)), "duplicate slugs"


def test_required_fields():
    for t in tx.list_tools():
        for field in ("slug", "name", "importance", "why", "related_domain",
                      "category", "category_name"):
            assert t.get(field), f"{t.get('slug')} missing {field}"


def test_get_tool_found_and_missing():
    docker = tx.get_tool("docker")
    assert docker and docker["name"] == "Docker"
    assert docker["importance"] == "critical"
    assert tx.get_tool("no-such-tool") is None


def test_get_critical_tools_all_critical():
    crit = tx.get_critical_tools()
    assert crit, "no critical tools"
    assert all(t["importance"] == "critical" for t in crit)


def test_get_important_tools_domain():
    tools = tx.get_important_tools("devops")
    assert tools, "no devops tools"
    assert any(t["slug"] == "docker" for t in tools)
    # sorted critical first
    order = [tx.IMPORTANCE_ORDER[t["importance"]] for t in tools]
    assert order == sorted(order)


def test_list_categories_counts():
    cats = tx.list_categories()
    assert len(cats) == len(tx.TECH_TAXONOMY)
    assert all(c["tool_count"] > 0 for c in cats)
    assert sum(c["tool_count"] for c in cats) == tx.tool_count()


def test_invalid_importance_raises():
    import pytest
    with pytest.raises(ValueError):
        tx.list_tools("bogus")


# --- API tests ---

def _client():
    from app.main import create_app
    return TestClient(create_app())


def test_api_tools_public():
    c = _client()
    r = c.get("/api/v1/taxonomy/tools")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 60


def test_api_tools_filter_importance():
    c = _client()
    r = c.get("/api/v1/taxonomy/tools", params={"importance": "critical"})
    assert r.status_code == 200
    assert all(t["importance"] == "critical" for t in r.json()["tools"])


def test_api_tools_bad_importance_422():
    c = _client()
    r = c.get("/api/v1/taxonomy/tools", params={"importance": "bogus"})
    assert r.status_code == 422


def test_api_tool_detail_and_404():
    c = _client()
    r = c.get("/api/v1/taxonomy/tools/jwt")
    assert r.status_code == 200
    assert r.json()["name"] == "JWT"
    r = c.get("/api/v1/taxonomy/tools/nope")
    assert r.status_code == 404


def test_api_categories_and_critical():
    c = _client()
    r = c.get("/api/v1/taxonomy/categories")
    assert r.status_code == 200 and r.json()["count"] >= 10
    r = c.get("/api/v1/taxonomy/critical")
    assert r.status_code == 200 and r.json()["count"] > 0
