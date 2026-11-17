import csv
from functools import lru_cache
from pathlib import Path

from app.models import Link, Movie, Rating, Tag

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _read_rows(file_name: str):
    with open(DATA_DIR / file_name, newline="", encoding="utf-8") as file:
        yield from csv.DictReader(file)


@lru_cache(maxsize=None)
def load_movies() -> list:
    return [
        Movie(int(row["movieId"]), row["title"], row["genres"])
        for row in _read_rows("movies.csv")
    ]


@lru_cache(maxsize=None)
def load_links() -> list:
    return [
        Link(
            int(row["movieId"]),
            row["imdbId"],
            int(row["tmdbId"]) if row["tmdbId"] else None,
        )
        for row in _read_rows("links.csv")
    ]


@lru_cache(maxsize=None)
def load_ratings() -> list:
    return [
        Rating(
            int(row["userId"]),
            int(row["movieId"]),
            float(row["rating"]),
            int(row["timestamp"]),
        )
        for row in _read_rows("ratings.csv")
    ]


@lru_cache(maxsize=None)
def load_tags() -> list:
    return [
        Tag(
            int(row["userId"]),
            int(row["movieId"]),
            row["tag"],
            int(row["timestamp"]),
        )
        for row in _read_rows("tags.csv")
    ]
