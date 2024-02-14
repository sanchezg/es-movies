import asyncio
import logging
from itertools import chain
from functools import wraps
from typing import Any

from httpx import AsyncClient, HTTPError

logger = logging.getLogger("default")


def retry_async(max_attempts=3, delay=1, backoff=2):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except HTTPError as e:
                    logger.warning(f"Attempt {attempts+1} failed: {e}")
                    await asyncio.sleep(delay * (backoff ** attempts))
                    attempts += 1
            raise Exception(f"Failed after {max_attempts} attempts")
        return wrapped
    return wrapper


class LoggingAsyncClient(AsyncClient):
    async def get(self, *args: Any, **kwargs: Any) -> Any:
        logger.debug(f"GET: {args} | {kwargs}")
        response = await super().get(*args, **kwargs)
        response.raise_for_status()
        logger.debug(f"Response: {response}")
        return response


class BaseService:
    async def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError


class MoviesFetcher(BaseService):
    def __init__(self) -> None:
        self._client = LoggingAsyncClient()

    @property
    def http_client(self):
        return self._client

    async def close_client(self):
        await self.http_client.aclose()

    @property
    def base_url(self):
        return "https://jsonmock.hackerrank.com/api/moviesdata/search/"

    @retry_async()
    async def fetch(self, params: dict[str, Any]) -> Any:
        response = await self.http_client.get(self.base_url, params=params)
        return response.json().get("data")

    async def __call__(self, *args: Any, title: str | None = None, **kwargs: Any) -> Any:
        params = {"page": kwargs.get("page", 1)}
        if title:
            params["Title"] = title
        response = await self.http_client.get(self.base_url, params=params)
        response_data = response.json()
        results = response_data.get("data")
        if total_pages := response_data.get("total_pages"):
            tasks = []
            for page in range(2, total_pages + 1):
                tasks.append(self.fetch(params={"Title": title, "page": page}))
            additional_results = await asyncio.gather(*tasks)
            results.extend(chain(*additional_results))
        await self.close_client()
        return results
