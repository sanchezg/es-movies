import dataclasses
from typing import Optional

from src.domain.model import Movie
from src.domain.repository import MovieRepo
from src.infra.repositories.es import ESRepo


class ESMovieRepo(ESRepo, MovieRepo):

    entity = Movie
    index_name = "movies"

    async def get(self, **kwargs) -> Optional[Movie]:
        # TODO: use some object-mapper lib for this
        doc = await super().get(**kwargs)
        if doc:
            return Movie(
                **{field.name: doc[field.name] for field in dataclasses.fields(Movie)}
            )
        return None
