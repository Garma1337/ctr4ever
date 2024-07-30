# coding=utf-8

class ContainerError(Exception):
    pass


class Container(object):

    def __init__(self):
        self._services = {}

    def register(self, key, func):
        if key in self._services:
            raise ContainerError(f'A service with key {key} has already been registered')

        self._services[key] = func

    def get(self, key):
        if not key in self._services:
            raise ContainerError(f'No service with key {key} has been registered')

        func = self._services[key]
        return func()
