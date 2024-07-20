# coding=utf-8

from unittest import TestCase

from ctr4ever.rest.routeresolver import RouteResolver
from ctr4ever.services.container import Container
from ctr4ever.tests.mockendpoint import MockEndpoint


class RouteResolverTest(TestCase):

    def setUp(self):
        self.container = Container()
        self.route_resolver = RouteResolver(self.container)

    def test_can_add_route(self):
        self.route_resolver.add_route('test', 'api.endpoint.test')
        self.assertTrue(self.route_resolver.route_exists('test'))

    def test_can_remove_route(self):
        self.route_resolver.add_route('test', 'api.endpoint.test')
        self.route_resolver.remove_route('test')
        self.assertFalse(self.route_resolver.route_exists('test'))

    def test_cannot_add_duplicate_route(self):
        self.route_resolver.add_route('test', 'api.endpoint.test')
        with self.assertRaises(Exception):
            self.route_resolver.add_route('test', 'api.endpoint.test')

    def test_cannot_remove_non_existent_route(self):
        with self.assertRaises(Exception):
            self.route_resolver.remove_route('test')

    def test_can_get_routes(self):
        self.route_resolver.add_route('test', 'api.endpoint.test')
        self.assertEqual(self.route_resolver.get_routes(), {'test': 'api.endpoint.test'})

    def test_can_resolve_route(self):
        self.route_resolver.add_route('test', 'api.endpoint.test')
        self.container.register('api.endpoint.test', lambda: MockEndpoint())

        self.assertIsNotNone(self.route_resolver.resolve_route('test'))

    def test_cannot_resolve_non_existent_route(self):
        with self.assertRaises(Exception):
            self.route_resolver.resolve_route('test')

    def test_cannot_resolve_route_if_endpoint_not_registered_in_container(self):
        self.route_resolver.add_route('test', 'api.endpoint.test')

        with self.assertRaises(Exception):
            self.route_resolver.resolve_route('test')
