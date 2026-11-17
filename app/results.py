import sqlite3
from datetime import datetime
from typing import Optional

DB_FILE = "results.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS results (
    job_id     TEXT PRIMARY KEY,
    url        TEXT NOT NULL,
    status     TEXT NOT NULL,
    people     INTEGER,
    error      TEXT,
    updated_at TEXT NOT NULL
)
"""


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_FILE, timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute(SCHEMA)
    return connection


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def create_job(job_id: str, url: str) -> None:
    connection = _connect()
    with connection:
        connection.execute(
            "INSERT INTO results (job_id, url, status, updated_at)"
            " VALUES (?, ?, 'queued', ?)",
            (job_id, url, _now()),
        )
    connection.close()


def save_result(
    job_id: str, people: Optional[int], error: Optional[str] = None
) -> None:
    status = "error" if error else "done"
    connection = _connect()
    with connection:
        connection.execute(
            "UPDATE results SET status = ?, people = ?, error = ?,"
            " updated_at = ? WHERE job_id = ?",
            (status, people, error, _now(), job_id),
        )
    connection.close()


def get_result(job_id: str) -> Optional[dict]:
    connection = _connect()
    row = connection.execute(
        "SELECT * FROM results WHERE job_id = ?", (job_id,)
    ).fetchone()
    connection.close()
    return dict(row) if row else None
