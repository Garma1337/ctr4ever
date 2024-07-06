# coding=utf-8

import pickle
from unittest import TestCase

from ctr4ever.services.container import Container, ContainerError


class TestService(object):

    def __init__(self):
        pass


class ContainerTest(TestCase):

    def setUp(self):
        self.container = Container()

    def test_can_register_service(self):
        self.container.register('test', lambda: TestService())
        self.assertEqual(
            pickle.dumps(self.container._services['test']()),
            pickle.dumps(TestService())
        )

    def test_cannot_register_service_when_service_exists(self):
        self.container.register('test', lambda: TestService())
        self.assertRaises(ContainerError, self.container.register, 'test', lambda: TestService())

    def test_can_get_service_by_key(self):
        self.container.register('test', lambda: TestService())
        service = self.container.get('test')

        self.assertEqual(pickle.dumps(service), pickle.dumps(TestService()))

    def test_can_get_unique_instance_when_getting_service_by_key(self):
        self.container.register('test', lambda: TestService())
        service1 = self.container.get('test')
        service2 = self.container.get('test')

        self.assertNotEqual(service1, service2)

    def test_cannot_get_service_by_key_when_service_does_not_exist(self):
        self.assertRaises(ContainerError, self.container.get, 'test')
