import dataclasses

from src.domain.model import Movie
from src.domain.repository import MovieRepo
from src.infra.repositories.es import ESRepo


class ESMovieRepo(ESRepo, MovieRepo):

    entity = Movie
    index_name = "movies"

    async def get(self, **kwargs) -> list[Movie] | None:
        docs = await super().get(
            index=self.index_name, body=kwargs.get("body", {"query": {"match_all": {}}})
        )  # TODO: add filters from kwargs
        if docs:
            return [
                Movie(
                    **{field.name: doc[field.name] for field in dataclasses.fields(Movie)}
                )
                for doc in docs
            ]

    async def insert(self, **kwargs) -> None:
        actions = [
            {
                "_index": self.index_name,  # type: ignore
                "doc": dataclasses.asdict(doc)
            }
            for doc in kwargs.get("documents", [])
        ]
        success, errors = await super().insert(actions=actions)
        if errors:
            raise Exception(f"Failed to insert: {errors}")
