import dataclasses
import logging

from src.domain.model import Movie
from src.domain.repository import MovieRepo
from src.infra.repositories.es import ESRepo

logger = logging.getLogger("default")


class ESMovieRepo(ESRepo, MovieRepo):

    entity = Movie
    index_name = "movies"

    async def get(self, title: str | None = None, year: int | None = None, **kwargs) -> list[Movie] | None:
        body = {}
        if title and year:
            body["query"] = {
                "bool": {
                    "must": [
                        {"match": {"title": title}},
                        {"match": {"year": year}},
                    ]
                }
            }
        elif title:
            body["query"] = {"match": {"title": title}}
        elif year:
            body["query"] = {"match": {"year": year}}
        else:
            body["query"] = {"match_all": {}}
        results = await super().get(index=self.index_name, body=body)
        logger.debug(f"Search: {body} | Results: {results}")
        if results.get("hits", {}).get("hits", []):  # type: ignore
            return [
                Movie(
                    **{field.name: doc["_source"].get(field.name) for field in dataclasses.fields(Movie)}
                )
                for doc in results["hits"]["hits"]  # type: ignore
            ]

    async def insert(self, **kwargs) -> int | None:
        actions = [
            {
                "_index": self.index_name,  # type: ignore
                "_source": {k.lower(): v for k, v in doc.items()}
            }
            for doc in kwargs.get("documents", [])
        ]
        success, errors = await super().insert(actions=actions)
        if errors:
            raise Exception(f"Failed to insert: {errors}")
        return success

    async def delete(self, **kwargs) -> None:
        body = {}
        if kwargs.get("all"):
            body = {"query": {"match_all": {}}}
        elif kwargs.get("title"):
            body = {
                "query": {"match": {"title": kwargs["title"]}}
            }
        await super().delete(index=self.index_name, body=body)
