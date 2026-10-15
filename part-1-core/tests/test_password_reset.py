"""Tests for forgot-password with Resend: domain, service, email adapter."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from app.domain import password_reset as pr
from app.domain.user import DomainError


# ---------- domain: pure functions ----------

def test_generate_token_unique_and_urlsafe():
    t1, t2 = pr.generate_token(), pr.generate_token()
    assert t1 != t2
    assert len(t1) >= 43  # 32 bytes url-safe
    assert all(c.isalnum() or c in "-_" for c in t1)


def test_hash_token_is_sha256_and_deterministic():
    h1 = pr.hash_token("abc123")
    h2 = pr.hash_token("abc123")
    assert h1 == h2
    assert len(h1) == 64
    assert h1 != "abc123"  # never the raw token


def test_hash_token_differs_per_token():
    assert pr.hash_token("a") != pr.hash_token("b")


def test_is_expired_future_and_past():
    now = datetime.now(timezone.utc)
    assert not pr.is_expired(now + timedelta(minutes=30), now)
    assert pr.is_expired(now - timedelta(seconds=1), now)


def test_is_expired_handles_naive_datetimes():
    # SQLite returns naive datetimes — must not crash, treated as UTC.
    past_naive = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=2)
    assert pr.is_expired(past_naive)


def test_token_ttl_is_one_hour():
    assert pr.TOKEN_TTL_HOURS == 1


# ---------- service: forgot/reset flow ----------

class _FakeUser:
    def __init__(self, id, email):
        self.id = id
        self.email = email


class _FakeUsers:
    def __init__(self, users):
        self._users = {u["email"]: _FakeUser(u["id"], u["email"]) for u in users}
        self.hashes = {}

    def find_by_email(self, email):
        return self._users.get(email)

    def set_password_hash(self, user_id, password_hash):
        for u in self._users.values():
            if u.id == user_id:
                self.hashes[user_id] = password_hash
                return True
        return False


class _FakeResets:
    def __init__(self):
        self.rows = []

    def create(self, user_id, token_hash, expires_at):
        row = {"id": f"r{len(self.rows)}", "user_id": user_id,
               "token_hash": token_hash, "expires_at": expires_at,
               "used_at": None}
        self.rows.append(row)
        return row

    def find_valid(self, token_hash):
        return next((r for r in self.rows if r["token_hash"] == token_hash), None)

    def mark_used(self, reset_id):
        for r in self.rows:
            if r["id"] == reset_id:
                r["used_at"] = datetime.now(timezone.utc)

    def count_recent_for_email(self, user_id, since):
        return sum(1 for r in self.rows if r["user_id"] == user_id)


class _FakeHasher:
    def hash(self, password):
        return f"hashed:{password}"


def _make_service(users=None, email_sender=None):
    from app.adapters.inbound.password_reset_service import PasswordResetServiceImpl
    users = users or [{"id": "u1", "email": "a@x.com"}]
    return PasswordResetServiceImpl(
        _FakeUsers(users), _FakeResets(), _FakeHasher(),
        email_sender=email_sender or (lambda to_email, reset_link: True))


def test_forgot_unknown_email_returns_ok_without_sending():
    sent = []
    svc = _make_service(email_sender=lambda to_email, reset_link: sent.append(to_email) or True)
    result = svc.forgot_password("nobody@x.com")
    assert result == {"ok": True, "email_sent": False}
    assert sent == []  # nothing sent, no account revealed


def test_forgot_known_email_creates_token_and_sends():
    links = []
    svc = _make_service(
        email_sender=lambda to_email, reset_link: links.append((to_email, reset_link)) or True)
    result = svc.forgot_password("a@x.com")
    assert result["ok"] is True and result["email_sent"] is True
    assert links[0][0] == "a@x.com"
    assert "/reset-password?token=" in links[0][1]
    # stored row holds the HASH, never the raw token
    row = svc._resets.rows[0]
    raw = links[0][1].split("token=")[1]
    assert row["token_hash"] == pr.hash_token(raw)
    assert row["token_hash"] != raw


def test_forgot_rate_limited_after_three_per_hour():
    svc = _make_service()
    for _ in range(3):
        svc.forgot_password("a@x.com")
    with pytest.raises(DomainError, match="too many"):
        svc.forgot_password("a@x.com")


def test_forgot_invalid_email_rejected():
    svc = _make_service()
    with pytest.raises(DomainError):
        svc.forgot_password("not-an-email")


def test_reset_happy_path_rotates_password_and_marks_used():
    links = []
    svc = _make_service(
        email_sender=lambda to_email, reset_link: links.append(reset_link) or True)
    svc.forgot_password("a@x.com")
    token = links[0].split("token=")[1]
    result = svc.reset_password(token, "newpassword123")
    assert result == {"ok": True}
    assert svc._users.hashes["u1"] == "hashed:newpassword123"
    assert svc._resets.rows[0]["used_at"] is not None


def test_reset_rejects_unknown_token():
    svc = _make_service()
    with pytest.raises(DomainError, match="invalid or expired"):
        svc.reset_password("bogus-token", "newpassword123")


def test_reset_rejects_expired_token():
    svc = _make_service()
    token = pr.generate_token()
    svc._resets.create("u1", pr.hash_token(token),
                       datetime.now(timezone.utc) - timedelta(minutes=1))
    with pytest.raises(DomainError, match="expired"):
        svc.reset_password(token, "newpassword123")


def test_reset_rejects_used_token():
    links = []
    svc = _make_service(
        email_sender=lambda to_email, reset_link: links.append(reset_link) or True)
    svc.forgot_password("a@x.com")
    token = links[0].split("token=")[1]
    svc.reset_password(token, "newpassword123")
    with pytest.raises(DomainError, match="already used"):
        svc.reset_password(token, "anotherpass1")


def test_reset_rejects_short_password():
    links = []
    svc = _make_service(
        email_sender=lambda to_email, reset_link: links.append(reset_link) or True)
    svc.forgot_password("a@x.com")
    token = links[0].split("token=")[1]
    with pytest.raises(DomainError, match="at least 8"):
        svc.reset_password(token, "short")


# ---------- email adapter ----------

def test_email_without_api_key_returns_false(monkeypatch):
    from app.adapters.outbound import email_service as es
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    assert es.send_password_reset_email("a@x.com", "http://x/reset") is False


def test_email_uses_project_address_not_personal(monkeypatch):
    from app.adapters.outbound import email_service as es
    monkeypatch.delenv("FROM_EMAIL", raising=False)
    assert es._from_email() == "noreply@skillforge.app"
    assert "gmail" not in es._from_email() and "yahoo" not in es._from_email()


def test_email_success_path(monkeypatch):
    import httpx
    from app.adapters.outbound import email_service as es
    monkeypatch.setenv("RESEND_API_KEY", "re_test_key")
    monkeypatch.setenv("FROM_EMAIL", "noreply@skillforge.app")

    captured = {}

    class _Resp:
        status_code = 200
        text = '{"id":"x"}'

    def fake_post(url, headers, json, timeout):
        captured["url"] = url
        captured["auth"] = headers["Authorization"]
        captured["from"] = json["from"]
        captured["to"] = json["to"]
        captured["html"] = json["html"]
        return _Resp()

    monkeypatch.setattr(httpx, "post", fake_post)
    assert es.send_password_reset_email("user@x.com", "http://x/reset?token=t") is True
    assert captured["url"] == "https://api.resend.com/emails"
    assert captured["auth"] == "Bearer re_test_key"
    assert "noreply@skillforge.app" in captured["from"]
    assert captured["to"] == ["user@x.com"]
    assert "1 hour" in captured["html"]


def test_email_api_error_returns_false(monkeypatch):
    import httpx
    from app.adapters.outbound import email_service as es
    monkeypatch.setenv("RESEND_API_KEY", "re_test_key")

    class _Resp:
        status_code = 401
        text = "invalid key"

    monkeypatch.setattr(httpx, "post", lambda *a, **k: _Resp())
    assert es.send_password_reset_email("a@x.com", "http://x") is False


def test_email_network_failure_returns_false(monkeypatch):
    import httpx
    from app.adapters.outbound import email_service as es
    monkeypatch.setenv("RESEND_API_KEY", "re_test_key")

    def boom(*a, **k):
        raise httpx.ConnectError("no network")

    monkeypatch.setattr(httpx, "post", boom)
    assert es.send_password_reset_email("a@x.com", "http://x") is False
