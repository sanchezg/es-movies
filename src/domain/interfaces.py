import abc
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class AbstractRepo(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def get(self, **kwargs) -> Optional[T]:
        pass

    @abc.abstractmethod
    def insert(self, **kwargs) -> None:
        pass
