from dataclasses import dataclass
from typing import Union


@dataclass()
class Movie:
    title: str
    year: int
    imdbid: str


@dataclass()
class MovieQuery:
    title: str
    year: int | None = None
    page: int | None = 1
