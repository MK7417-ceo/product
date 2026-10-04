"""Adapter tests: service orchestrates domain + fake outbound ports (except
real crypto, because faking crypto hides real bugs)."""
import pytest

from app.adapters.inbound.auth_service import JwtAuthService
from app.adapters.outbound.security import BcryptPasswordHasher, JwtTokenIssuer
from app.domain.user import DomainError, User


class FakeUsers:
    def __init__(self):
        self.by_email: dict[str, User] = {}
        self.by_id: dict[str, User] = {}

    def save(self, user: User) -> None:
        self.by_email[user.email] = user
        self.by_id[user.id] = user

    def find_by_email(self, email: str):
        return self.by_email.get(email)

    def get(self, user_id: str):
        return self.by_id.get(user_id)

    def update_role(self, user_id: str, role: str):
        u = self.by_id.get(user_id)
        if not u:
            return None
        nu = User(id=u.id, email=u.email, password_hash=u.password_hash, role=role,
                  created_at=u.created_at)
        self.save(nu)
        return nu

    def delete(self, user_id: str) -> None:
        u = self.by_id.pop(user_id, None)
        if u:
            self.by_email.pop(u.email, None)


class FakeTokens:
    def __init__(self):
        self.revoked: set[str] = set()
        self.owner: dict[str, str] = {}

    def store(self, token: str, user_id: str, expires_at=None) -> None:
        self.owner[token] = user_id

    def revoke(self, token: str) -> None:
        self.revoked.add(token)  # idempotent

    def is_revoked(self, token: str) -> bool:
        return token not in self.owner or token in self.revoked

    def owner_of(self, token: str):
        return None if self.is_revoked(token) else self.owner.get(token)

    def revoke_all_for_user(self, user_id: str) -> None:
        for t, uid in self.owner.items():
            if uid == user_id:
                self.revoked.add(t)


@pytest.fixture()
def svc():
    return JwtAuthService(FakeUsers(), BcryptPasswordHasher(),
                          JwtTokenIssuer("unit-test-secret"), FakeTokens())


def test_register_and_login(svc):
    res = svc.register("ada@x.com", "password123")
    assert res.user.email == "ada@x.com"
    assert res.user.role == "user"
    again = svc.login("ada@x.com", "password123")
    assert again.user.id == res.user.id


def test_register_duplicate_email(svc):
    svc.register("ada@x.com", "password123")
    with pytest.raises(DomainError, match="already registered"):
        svc.register("ada@x.com", "password123")


def test_login_wrong_password(svc):
    svc.register("ada@x.com", "password123")
    with pytest.raises(DomainError, match="invalid credentials"):
        svc.login("ada@x.com", "wrongpass")


def test_login_unknown_email(svc):
    with pytest.raises(DomainError, match="invalid credentials"):
        svc.login("ghost@x.com", "password123")


def test_refresh_rotates_and_kills_old(svc):
    res = svc.register("ada@x.com", "password123")
    rotated = svc.refresh(res.refresh_token)
    assert rotated.refresh_token != res.refresh_token
    with pytest.raises(DomainError, match="revoked"):
        svc.refresh(res.refresh_token)  # replay of old token must fail


def test_refresh_with_access_token_rejected(svc):
    res = svc.register("ada@x.com", "password123")
    with pytest.raises(DomainError, match="not a refresh token"):
        svc.refresh(res.access_token)


def test_logout_is_idempotent(svc):
    res = svc.register("ada@x.com", "password123")
    svc.logout(res.refresh_token)
    svc.logout(res.refresh_token)  # must not raise
    with pytest.raises(DomainError):
        svc.refresh(res.refresh_token)


def test_set_role_bad_role(svc):
    res = svc.register("ada@x.com", "password123")
    with pytest.raises(DomainError, match="unknown role"):
        svc.set_role(res.user.id, "ceo")


def test_export_never_leaks_hash(svc):
    res = svc.register("ada@x.com", "password123")
    data = svc.export_data(res.user.id)
    assert "password_hash" not in data
    assert data["email"] == "ada@x.com"


def test_delete_account(svc):
    res = svc.register("ada@x.com", "password123")
    svc.delete_account(res.user.id)
    with pytest.raises(DomainError, match="not found"):
        svc.get_user(res.user.id)


def test_expired_token_rejected():
    issuer = JwtTokenIssuer("unit-test-secret", access_minutes=-1)
    svc = JwtAuthService(FakeUsers(), BcryptPasswordHasher(), issuer, FakeTokens())
    res = svc.register("ada@x.com", "password123")
    with pytest.raises(DomainError, match="invalid or expired"):
        issuer.decode(res.access_token)
