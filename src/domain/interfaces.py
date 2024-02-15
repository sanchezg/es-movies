import abc
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class AbstractRepo(abc.ABC, Generic[T]):
    @abc.abstractmethod
    async def get(self, **kwargs) -> Optional[T]:
        pass

    @abc.abstractmethod
    async def insert(self, **kwargs) -> None:
        pass

    @abc.abstractmethod
    async def delete(self, **kwargs) -> None:
        pass
