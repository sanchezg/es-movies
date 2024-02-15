from src.infra.repositories.movies import ESMovieRepo


class MockESMovieRepo(ESMovieRepo):
    def __init__(self) -> None:
        self._documents = [
            {
                "title": "The Matrix",
                "year": 1999,
                "imdbid": "tt0133093",
            },
            {
                "title": "The Matrix Reloaded",
                "year": 2003,
                "imdbid": "tt0234215",
            },
            {
                "title": "The Matrix Revolutions",
                "year": 2003,
                "imdbid": "tt0242653",
            },
        ]
    async def get(self, title: str | None = None, year: int | None = None, **kwargs) -> list[dict] | None:
        return self._documents if title and "matrix" in title else []

    async def insert(self, **kwargs) -> int | None:
        self._documents.extend(kwargs.get("documents", []))
        return len(kwargs.get("documents", []))

    async def delete(self, **kwargs) -> None:
        pass


class MockMoviesFetcher:
    def __init__(self) -> None:
        self._documents = [
            {
                "title": "The Matrix",
                "year": 1999,
                "imdbid": "tt0133093",
            },
            {
                "title": "The Matrix Reloaded",
                "year": 2003,
                "imdbid": "tt0234215",
            },
            {
                "title": "The Matrix Revolutions",
                "year": 2003,
                "imdbid": "tt0242653",
            },
            {
                "title": "The Lord of the Rings",
                "year": 2001,
                "imdbid": "tt0120737",
            },
            {
                "title": "The Lord of the Rings: The Two Towers",
                "year": 2002,
                "imdbid": "tt0167261",
            },
            {
                "title": "The Lord of the Rings: The Return of the King",
                "year": 2003,
                "imdbid": "tt0167260",
            },
        ]

    async def __call__(self, *args, title: str | None = None, **kwargs) -> list[dict]:
        return self._documents[:3] if title and "matrix" in title else self._documents
