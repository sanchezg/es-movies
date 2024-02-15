from typing import Any, Optional

from elasticsearch.helpers import async_bulk

from src import settings
from src.domain.interfaces import AbstractRepo


class ESRepo(AbstractRepo):
    def __init__(self, client) -> None:
        self.es = client
        super().__init__()

    async def get(self, index, body, **kwargs) -> Optional[Any]:
        documents = await self.es.search(
            index=index,
            body=body,
            size=settings.ES_MAX_SIZE,
        )
        return documents

    async def insert(self, actions: list[dict], **kwargs) -> tuple[int, int | list[Any]]:
        return await async_bulk(self.es, actions, chunk_size=settings.ES_CHUNK_SIZE)

    async def delete(self, index, body, **kwargs) -> None:
        return await self.es.delete_by_query(index=index, body=body)
