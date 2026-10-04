"""API tests — full HTTP auth flows through the real hexagon (sqlite)."""
import uuid

from fastapi.testclient import TestClient

from app.main import create_app


def make_client() -> TestClient:
    return TestClient(create_app())


def _email() -> str:
    return f"u-{uuid.uuid4().hex[:8]}@x.com"


def _register(client: TestClient, email: str, password: str = "password123") -> dict:
    r = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert r.status_code == 201, r.text
    return r.json()


def _authz(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_register_login_me_flow():
    c = make_client()
    email = _email()
    reg = _register(c, email)
    assert reg["user"]["role"] == "user"
    assert "password" not in str(reg["user"])

    r = c.post("/api/v1/auth/login", json={"email": email, "password": "password123"})
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "bearer"

    r = c.get("/api/v1/auth/me", headers=_authz(body["access_token"]))
    assert r.status_code == 200
    assert r.json()["email"] == email


def test_duplicate_register_409():
    c = make_client()
    email = _email()
    _register(c, email)
    r = c.post("/api/v1/auth/register", json={"email": email, "password": "password123"})
    assert r.status_code == 409


def test_bad_login_401():
    c = make_client()
    email = _email()
    _register(c, email)
    r = c.post("/api/v1/auth/login", json={"email": email, "password": "wrongpass1"})
    assert r.status_code == 401


def test_short_password_422():
    c = make_client()
    r = c.post("/api/v1/auth/register", json={"email": _email(), "password": "short"})
    assert r.status_code == 422


def test_me_without_token_401():
    assert make_client().get("/api/v1/auth/me").status_code == 401


def test_refresh_rotation_replay_fails():
    c = make_client()
    reg = _register(c, _email())
    r1 = c.post("/api/v1/auth/refresh", json={"refresh_token": reg["refresh_token"]})
    assert r1.status_code == 200
    new_pair = r1.json()
    assert new_pair["refresh_token"] != reg["refresh_token"]
    # replay of the old refresh token must be rejected
    r2 = c.post("/api/v1/auth/refresh", json={"refresh_token": reg["refresh_token"]})
    assert r2.status_code == 401


def test_logout_revokes_refresh():
    c = make_client()
    reg = _register(c, _email())
    r = c.post("/api/v1/auth/logout", json={"refresh_token": reg["refresh_token"]})
    assert r.status_code == 204
    r = c.post("/api/v1/auth/refresh", json={"refresh_token": reg["refresh_token"]})
    assert r.status_code == 401


def test_set_role_forbidden_for_plain_user():
    c = make_client()
    reg = _register(c, _email())
    r = c.post(f"/api/v1/auth/users/{reg['user']['id']}/role", json={"role": "admin"},
               headers=_authz(reg["access_token"]))
    assert r.status_code == 403


def test_set_role_by_admin():
    c = make_client()
    admin = _register(c, _email())
    # promote directly through the service (bootstrapping the first admin)
    c.app.state.auth_service.set_role(admin["user"]["id"], "admin")
    login = c.post("/api/v1/auth/login", json={"email": admin["user"]["email"], "password": "password123"})
    admin_token = login.json()["access_token"]

    other = _register(c, _email())
    r = c.post(f"/api/v1/auth/users/{other['user']['id']}/role", json={"role": "reviewer"},
               headers=_authz(admin_token))
    assert r.status_code == 200
    assert r.json()["role"] == "reviewer"


def test_export_excludes_password_hash():
    c = make_client()
    reg = _register(c, _email())
    r = c.get("/api/v1/auth/export", headers=_authz(reg["access_token"]))
    assert r.status_code == 200
    assert "password_hash" not in r.json()


def test_delete_account():
    c = make_client()
    email = _email()
    reg = _register(c, email)
    r = c.delete("/api/v1/auth/me", headers=_authz(reg["access_token"]))
    assert r.status_code == 204
    r = c.post("/api/v1/auth/login", json={"email": email, "password": "password123"})
    assert r.status_code == 401
