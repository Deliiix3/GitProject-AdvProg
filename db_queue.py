import sqlite3
from datetime import datetime
from typing import Optional

DB_FILE = "queue.db"

PENDING = "pending"
IN_PROGRESS = "in_progress"
DONE = "done"

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'in_progress', 'done')),
    consumer    TEXT,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
)
"""


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def connect() -> sqlite3.Connection:
    # isolation_level=None - transakcjami sterujemy sami (BEGIN/COMMIT)
    connection = sqlite3.connect(DB_FILE, timeout=30, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute(SCHEMA)
    return connection


def add_job(description: str) -> dict:
    connection = connect()
    try:
        cursor = connection.execute(
            "INSERT INTO jobs (description, status, created_at, updated_at)"
            " VALUES (?, ?, ?, ?)",
            (description, PENDING, now(), now()),
        )
        return {"id": cursor.lastrowid, "status": PENDING}
    finally:
        connection.close()


def claim_next_job(consumer: str) -> Optional[dict]:
    """Pobiera pierwszą pracę pending i zmienia jej status na in_progress.
    BEGIN IMMEDIATE blokuje zapis, więc dwóch konsumerów nie weźmie
    tej samej pracy."""
    connection = connect()
    try:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT id, description FROM jobs"
            " WHERE status = ? ORDER BY id LIMIT 1",
            (PENDING,),
        ).fetchone()
        if row is None:
            connection.execute("COMMIT")
            return None
        connection.execute(
            "UPDATE jobs SET status = ?, consumer = ?, updated_at = ?"
            " WHERE id = ?",
            (IN_PROGRESS, consumer, now(), row["id"]),
        )
        connection.execute("COMMIT")
        return {"id": row["id"], "description": row["description"]}
    except Exception:
        connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def mark_done(job_id: int) -> None:
    connection = connect()
    try:
        connection.execute(
            "UPDATE jobs SET status = ?, updated_at = ? WHERE id = ?",
            (DONE, now(), job_id),
        )
    finally:
        connection.close()
