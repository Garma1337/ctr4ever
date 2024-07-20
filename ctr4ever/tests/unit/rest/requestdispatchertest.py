# coding=utf-8

from unittest import TestCase

from flask import Request

from ctr4ever.rest.requestdispatcher import RequestDispatcher
from ctr4ever.rest.routeresolver import RouteResolver
from ctr4ever.services.container import Container
from ctr4ever.tests.mockendpoint import MockEndpoint


class RequestDispatcherTest(TestCase):

    def setUp(self):
        self.container = Container()
        self.route_resolver = RouteResolver(self.container)
        self.request_dispatcher = RequestDispatcher(self.route_resolver)

    def test_cannot_access_route_if_route_unspecified(self):
        response = self.request_dispatcher.dispatch_request('', Request.from_values())
        data = response.get_data()

        self.assertIsNotNone(data['error'])
        self.assertEqual(response.get_status_code(), 400)

    def test_cannot_access_route_if_route_does_not_exist(self):
        response = self.request_dispatcher.dispatch_request('test', Request.from_values())
        data = response.get_data()

        self.assertIsNotNone(data['error'])
        self.assertEqual(response.get_status_code(), 404)

    def test_cannot_access_route_if_endpoint_not_registered_in_container(self):
        self.route_resolver.add_route('test', 'api.endpoint.test')

        response = self.request_dispatcher.dispatch_request('test', Request.from_values())
        data = response.get_data()

        self.assertIsNotNone(data['error'])
        self.assertEqual(response.get_status_code(), 500)

    def test_cannot_access_route_if_invalid_request_method(self):
        self.route_resolver.container.register('api.endpoint.test', lambda: MockEndpoint())
        self.route_resolver.add_route('test', 'api.endpoint.test')

        request = Request.from_values()
        request.method = 'POST'

        response = self.request_dispatcher.dispatch_request('test', request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])
        self.assertEqual(response.get_status_code(), 405)

    def test_can_dispatch_request(self):
        self.route_resolver.container.register('api.endpoint.test', lambda: MockEndpoint())
        self.route_resolver.add_route('test', 'api.endpoint.test')

        response = self.request_dispatcher.dispatch_request('test', Request.from_values())

        self.assertEqual(response.get_data(), '')
        self.assertEqual(response.get_status_code(), 204)