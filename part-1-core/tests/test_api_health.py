"""API tests — exercise the hexagon through HTTP with a fake outbound adapter."""
from fastapi.testclient import TestClient

from app.adapters.inbound.health_service import SystemHealthService
from app.main import create_app


class FakeProbe:
    def __init__(self, ok: bool = True):
        self._ok = ok

    def check(self) -> tuple[bool, str]:
        return self._ok, "fake"


def make_client(db_ok: bool = True) -> TestClient:
    app = create_app()
    # swap the real DB probe for a fake — the port makes this trivial
    app.state.health_service = SystemHealthService(FakeProbe(db_ok))
    return TestClient(app)


def test_health_ok():
    resp = make_client(db_ok=True).get("/api/v1/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is True
    assert body["summary"] == "all systems operational"
    assert "X-Request-ID" in resp.headers


def test_health_degraded_when_db_down():
    resp = make_client(db_ok=False).get("/api/v1/health")
    assert resp.status_code == 503
    assert resp.json()["ok"] is False
