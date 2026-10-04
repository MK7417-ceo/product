"""Test bootstrap: env vars + fresh sqlite DB, BEFORE any app import."""
import os

os.environ.setdefault("SECRET_KEY", "test-only-secret-not-for-production")
_db = "/tmp/skillforge-f1-test.db"
os.environ.setdefault("DATABASE_URL", f"sqlite:///{_db}")
if os.path.exists(_db):
    os.remove(_db)

import pytest  # noqa: E402

import app.adapters.outbound.models  # noqa: E402,F401  (register tables)
from app.core.database import Base, engine  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _create_tables():
    Base.metadata.create_all(engine)
    yield
