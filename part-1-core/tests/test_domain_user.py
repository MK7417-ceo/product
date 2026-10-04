"""Domain tests — pure rules, no adapters."""
import pytest

from app.domain.user import (
    DomainError,
    new_user,
    validate_email,
    validate_password,
    validate_role,
)


def test_validate_email_ok():
    assert validate_email("  Ada@Example.COM ") == "ada@example.com"


def test_validate_email_bad():
    for bad in ["nope", "a@b", "@x.com", "a b@c.com"]:
        with pytest.raises(DomainError):
            validate_email(bad)


def test_validate_password_too_short():
    with pytest.raises(DomainError):
        validate_password("short")


def test_new_user_defaults_to_user_role():
    u = new_user("id1", "a@x.com", "hash")
    assert u.role == "user"
    assert u.email == "a@x.com"


def test_validate_role_rejects_unknown():
    with pytest.raises(DomainError):
        validate_role("superuser")
    assert validate_role("admin") == "admin"
