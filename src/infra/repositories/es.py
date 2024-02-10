from typing import Any, Optional

from src import settings
from src.domain.interfaces import AbstractRepo


class ESRepo(AbstractRepo):
    def __init__(self, client) -> None:
        self.es = client
        super().__init__()

    async def get(self, **kwargs) -> Optional[Any]:
        documents = await self.es.search(
            index=self.index_name,  # type: ignore
            body={"query": {"match_all": {}}},
            size=20,
        )
        return documents

    async def insert(self, **kwargs) -> None:
        # document = await self.es.bulk(
            
        # )
        # return document
        pass
