import abc

from src.domain.interfaces import AbstractRepo
from src.domain.model import Movie


class MovieRepo(AbstractRepo[Movie], metaclass=abc.ABCMeta):
    pass
