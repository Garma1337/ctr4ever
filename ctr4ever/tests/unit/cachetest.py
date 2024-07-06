# coding=utf-8

from unittest import TestCase

from ctr4ever.services.cache.cache import CacheError
from ctr4ever.services.cache.memorycache import MemoryCache


class CacheTest(TestCase):

    def setUp(self):
        self.memory_cache = MemoryCache()

    def test_can_store_value(self):
        self.memory_cache.store('test', 'blabla')
        self.assertEqual(self.memory_cache._cache['test'], 'blabla')

    def test_can_store_and_override_value(self):
        self.memory_cache.store('test', 'blabla')
        self.memory_cache.store('test', 'test2', True)

        self.assertEqual(self.memory_cache._cache['test'], 'test2')

    def test_can_not_store_value_when_key_exists(self):
        self.memory_cache.store('test', 'blabla')
        self.assertRaises(CacheError, self.memory_cache.store, 'test', 'test2')

    def test_can_get_value(self):
        self.memory_cache.store('test', 'blabla')
        value = self.memory_cache.get('test')

        self.assertEqual(value, 'blabla')

    def test_can_not_get_value_when_value_does_not_exist(self):
        self.assertRaises(CacheError, self.memory_cache.get, 'test')
