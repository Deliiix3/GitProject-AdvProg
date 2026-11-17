import csv
import os
import time
import uuid
from contextlib import contextmanager
from datetime import datetime
from typing import Optional

QUEUE_FILE = "jobs.csv"
LOCK_FILE = QUEUE_FILE + ".lock"
FIELDS = [
    "id",
    "description",
    "status",
    "consumer",
    "created_at",
    "updated_at",
]

PENDING = "pending"
IN_PROGRESS = "in_progress"
DONE = "done"

LOCK_TIMEOUT = 30
STALE_LOCK_AGE = 10


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


@contextmanager
def file_lock():
    """Blokada na czas zapisu/odczytu pliku, żeby kilku konsumerów
    nie pobrało tej samej pracy."""
    started = time.time()
    while True:
        try:
            fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(LOCK_FILE) > STALE_LOCK_AGE:
                    os.remove(LOCK_FILE)
                    continue
            except OSError:
                pass
            if time.time() - started > LOCK_TIMEOUT:
                raise TimeoutError("Nie udało się zdobyć blokady pliku")
            time.sleep(0.05)
    try:
        yield
    finally:
        try:
            os.remove(LOCK_FILE)
        except OSError:
            pass


def read_jobs() -> list:
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_jobs(jobs: list) -> None:
    temp_file = QUEUE_FILE + ".tmp"
    with open(temp_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(jobs)
    os.replace(temp_file, QUEUE_FILE)


def add_job(description: str) -> dict:
    job = {
        "id": uuid.uuid4().hex[:8],
        "description": description,
        "status": PENDING,
        "consumer": "",
        "created_at": now(),
        "updated_at": now(),
    }
    with file_lock():
        jobs = read_jobs()
        jobs.append(job)
        write_jobs(jobs)
    return job


def claim_next_job(consumer: str) -> Optional[dict]:
    """Zwraca pierwszą pracę pending po zmianie jej statusu
    na in_progress (albo None, gdy nie ma pracy)."""
    with file_lock():
        jobs = read_jobs()
        for job in jobs:
            if job["status"] == PENDING:
                job["status"] = IN_PROGRESS
                job["consumer"] = consumer
                job["updated_at"] = now()
                write_jobs(jobs)
                return dict(job)
    return None


def mark_done(job_id: str) -> None:
    with file_lock():
        jobs = read_jobs()
        for job in jobs:
            if job["id"] == job_id:
                job["status"] = DONE
                job["updated_at"] = now()
        write_jobs(jobs)
