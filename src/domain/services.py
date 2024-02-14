import logging
from typing import Any

from httpx import AsyncClient

logger = logging.getLogger("default")


class BaseService:
    async def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError


class MoviesFetcher(BaseService):
    def __init__(self) -> None:
        self._client = AsyncClient()

    @property
    def http_client(self):
        return self._client

    async def close_client(self):
        await self.http_client.aclose()

    @property
    def base_url(self):
        return "https://jsonmock.hackerrank.com/api/moviesdata/search/"

    async def __call__(self, *args: Any, title: str | None = None, **kwargs: Any) -> Any:
        params = {}
        if title:
            params["Title"] = title
        if kwargs.get("page"):
            params["page"] = kwargs["page"]
        response = await self.http_client.get(self.base_url, params=params)
        if not kwargs.get("keep_open"):
            await self.close_client()
        response.raise_for_status()
        logger.debug(f"Response: {response.json()}")
        return response.json()
