"""P2c tests: Core -> Code Engine integration (proxied, auth-gated)."""
import uuid

from fastapi.testclient import TestClient

from app.adapters.outbound.code_runner_client import (
    CodeEngineError,
    HttpCodeRunnerClient,
)
from app.main import create_app


def _ok_transport(url, payload, headers, timeout, method="POST"):
    if url.endswith("/v1/run"):
        assert headers.get("X-Request-ID")
        return 200, {"run_id": "abc123", "verdict": "OK", "stdout": "42\n",
                     "stderr": "", "truncated": False, "exit_code": 0,
                     "cpu_ms": 5, "peak_ram_mb": 3.1, "timed_out": False}
    return 200, {"languages": [{"id": "cpp", "available": True}]}


def _reject_transport(url, payload, headers, timeout, method="POST"):
    return 400, {"error": "empty_code", "message": "code must not be empty"}


def _down_transport(url, payload, headers, timeout, method="POST"):
    raise CodeEngineError("engine_unreachable", "code engine unreachable: boom")


def _client_with(transport):
    app = create_app()
    app.state.code_runner = HttpCodeRunnerClient("http://engine:9",
                                                 transport=transport)
    return TestClient(app)


def _authz(c: TestClient) -> dict:
    email = f"code-{uuid.uuid4().hex[:8]}@x.com"
    r = c.post("/api/v1/auth/register",
               json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_run_proxied_to_engine():
    c = _client_with(_ok_transport)
    h = _authz(c)
    r = c.post("/api/v1/code/run", headers=h,
               json={"language": "cpp", "code": "int main(){}"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["verdict"] == "OK" and body["stdout"] == "42\n"


def test_engine_rejection_becomes_400():
    c = _client_with(_reject_transport)
    h = _authz(c)
    r = c.post("/api/v1/code/run", headers=h,
               json={"language": "python", "code": "   "})
    assert r.status_code == 400
    assert r.json()["error"] == "empty_code"


def test_engine_down_becomes_502():
    c = _client_with(_down_transport)
    h = _authz(c)
    r = c.post("/api/v1/code/run", headers=h,
               json={"language": "python", "code": "print(1)"})
    assert r.status_code == 502
    assert r.json()["error"] == "engine_unreachable"


def test_languages_proxied():
    c = _client_with(_ok_transport)
    h = _authz(c)
    r = c.get("/api/v1/code/languages", headers=h)
    assert r.status_code == 200
    assert r.json()["languages"][0]["id"] == "cpp"


def test_code_endpoints_require_auth():
    c = _client_with(_ok_transport)
    assert c.post("/api/v1/code/run",
                  json={"language": "python", "code": "print(1)"}).status_code == 401
    assert c.get("/api/v1/code/languages").status_code == 401
