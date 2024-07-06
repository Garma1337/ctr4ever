# coding=utf-8

from abc import ABC, abstractmethod


class CacheError(Exception):
    pass


class Cache(ABC):

    @abstractmethod
    def store(self, key: str, value, override: bool = False) -> None:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
