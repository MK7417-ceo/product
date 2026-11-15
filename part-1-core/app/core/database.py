"""Database infrastructure — lives OUTSIDE the domain (adapter-side).

SQLite is the zero-setup local database. Its file is persisted on disk, not in
browser storage. WAL mode improves read concurrency; busy_timeout lets short
write contention wait instead of failing immediately. Production should use
managed PostgreSQL with connection pooling and automated backups.
"""
from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

_database_url = make_url(settings.DATABASE_URL)
_is_sqlite = _database_url.get_backend_name() == "sqlite"
_connect_args: dict = {}

if _is_sqlite:
    _connect_args["check_same_thread"] = False
    _connect_args["timeout"] = 30

    # Ensure a configured local SQLite file has a real parent directory.
    # Do not create a directory for in-memory SQLite databases used by tests.
    if _database_url.database and _database_url.database != ":memory:":
        Path(_database_url.database).expanduser().resolve().parent.mkdir(
            parents=True, exist_ok=True
        )

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
    pool_pre_ping=True,
)

if _is_sqlite:
    @event.listens_for(engine, "connect")
    def _configure_sqlite_connection(dbapi_connection, _connection_record) -> None:
        """Set safe, low-overhead SQLite defaults on every DB connection."""
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("PRAGMA busy_timeout=30000")
            # WAL lets readers continue while a writer commits. SQLite still
            # serializes writers, so PostgreSQL remains the production choice.
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
        finally:
            cursor.close()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
