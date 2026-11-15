"""Local SQLite persistence and connection configuration regression tests."""
from sqlalchemy import text

from app.core.database import create_database_engine


def test_sqlite_creates_parent_and_persists_across_engine_restart(tmp_path):
    database_file = tmp_path / "nested" / "local" / "skillforge.db"
    url = f"sqlite:///{database_file}"

    first = create_database_engine(url)
    assert database_file.exists() is False  # engine setup creates directories, not the DB file
    with first.begin() as connection:
        connection.execute(text("CREATE TABLE persistence_probe (id INTEGER PRIMARY KEY, value TEXT NOT NULL)"))
        connection.execute(text("INSERT INTO persistence_probe (value) VALUES ('saved-before-restart')"))
        assert connection.execute(text("PRAGMA foreign_keys")).scalar_one() == 1
        assert connection.execute(text("PRAGMA busy_timeout")).scalar_one() == 30000
        assert connection.execute(text("PRAGMA journal_mode")).scalar_one().lower() == "wal"
    first.dispose()

    # A fresh engine/process sees the committed row in the same on-disk file.
    second = create_database_engine(url)
    with second.connect() as connection:
        value = connection.execute(
            text("SELECT value FROM persistence_probe WHERE id=1")
        ).scalar_one()
        assert value == "saved-before-restart"
    second.dispose()
