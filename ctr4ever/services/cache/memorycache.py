# coding=utf-8

from ctr4ever.services.cache.cache import Cache, CacheError


class MemoryCache(Cache):

    def __init__(self):
        self._cache = {}

    def store(self, key: str, value, override: bool = False) -> None:
        if not self.exists(key):
            self._cache.setdefault(key, value)
            return

        if override:
            self._cache.pop(key)
            self._cache.setdefault(key, value)
            return

        raise CacheError(f'A value with key "{key}" already exists in the cache.')

    def get(self, key: str):
        if not self.exists(key):
            raise CacheError(f'No cached value with key "{key}" exists.')

        return self._cache.get(key)

    def exists(self, key: str) -> bool:
        return key in self._cache

    def clear(self) -> None:
        self._cache = {}
