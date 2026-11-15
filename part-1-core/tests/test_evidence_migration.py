"""Migration regression: historical v1 evidence must never become verified."""
from __future__ import annotations

import os
import re
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path


def test_legacy_evidence_is_unverified_and_reopens_task_after_upgrade():
    core_dir = Path(__file__).resolve().parent.parent
    tmp = Path(tempfile.mkdtemp(prefix="evidence_migration_test_"))
    db = tmp / "legacy.db"
    ini = tmp / "alembic.ini"

    ini_text = (core_dir / "alembic.ini").read_text()
    ini_text, n_url = re.subn(
        r"(?m)^sqlalchemy\.url\s*=.*$",
        f"sqlalchemy.url = sqlite:///{db}",
        ini_text,
    )
    assert n_url == 1
    ini_text, n_loc = re.subn(
        r"(?m)^script_location\s*=.*$",
        f"script_location = {core_dir / 'alembic'}",
        ini_text,
    )
    assert n_loc == 1
    ini.write_text(ini_text)
    env = dict(os.environ, SECRET_KEY="migration-test-secret-key-long-enough-for-ci")

    # Build the exact pre-review schema, then insert a historical submission
    # whose old workflow had marked its roadmap task completed.
    before = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(ini), "upgrade", "w9x0merge001"],
        cwd=core_dir, env=env, capture_output=True, text=True, check=False,
    )
    assert before.returncode == 0, before.stdout + "\\n" + before.stderr

    with sqlite3.connect(db) as conn:
        conn.execute(
            "INSERT INTO users (id,email,password_hash,role,created_at) "
            "VALUES (?,?,?,?,?)",
            ("u-legacy", "legacy@example.test", "hash", "user", "2026-01-01 00:00:00"),
        )
        conn.execute(
            "INSERT INTO roadmaps (id,user_id,version,title,source,created_at) "
            "VALUES (?,?,?,?,?,?)",
            ("r-legacy", "u-legacy", 1, "Legacy roadmap", "manual", "2026-01-01 00:00:00"),
        )
        conn.execute(
            "INSERT INTO roadmap_tasks "
            "(id,task_key,roadmap_id,title,status,created_at) VALUES (?,?,?,?,?,?)",
            ("rt-legacy", "t0001", "r-legacy", "Legacy task", "completed", "2026-01-01 00:00:00"),
        )
        conn.execute(
            "INSERT INTO evidence "
            "(id,user_id,roadmap_id,task_key,kind,content,feedback,created_at) "
            "VALUES (?,?,?,?,?,?,?,?)",
            ("ev-legacy", "u-legacy", "r-legacy", "t0001", "text",
             "Historical proof submitted before review existed.", "", "2026-01-02 00:00:00"),
        )

    after = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(ini), "upgrade", "head"],
        cwd=core_dir, env=env, capture_output=True, text=True, check=False,
    )
    assert after.returncode == 0, after.stdout + "\\n" + after.stderr

    with sqlite3.connect(db) as conn:
        evidence_status = conn.execute(
            "SELECT status FROM evidence WHERE id='ev-legacy'"
        ).fetchone()[0]
        task_status = conn.execute(
            "SELECT status FROM roadmap_tasks WHERE id='rt-legacy'"
        ).fetchone()[0]
    assert evidence_status == "legacy_unverified"
    assert task_status == "in_progress"
