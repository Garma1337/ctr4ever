# coding=utf-8

from unittest import TestCase
from unittest.mock import MagicMock

from flask import Config, Request

from ctr4ever.rest.endpoint.baseendpoint import BaseEndpoint
from ctr4ever.rest.requestdispatcher import RequestDispatcher
from ctr4ever.rest.response import EmptyResponse, Response
from ctr4ever.services.container import Container


class TestEndpoint(BaseEndpoint):

    def handle_request(self, request: Request) -> Response:
        return EmptyResponse()

    def get_accepted_request_method(self) -> str:
        return 'GET'


class RequestDispatcherTest(TestCase):

    def setUp(self):
        self.request_dispatcher = RequestDispatcher(
            Container(),
            Config('')
        )

    def test_cannot_access_route_if_route_unspecified(self):
        response = self.request_dispatcher.dispatch_request({}, '', Request.from_values())
        data = response.get_data()

        self.assertIsNotNone(data['error'])
        self.assertEqual(response.get_status_code(), 400)

    def test_cannot_access_route_if_route_does_not_exist(self):
        response = self.request_dispatcher.dispatch_request({}, 'test', Request.from_values())
        data = response.get_data()

        self.assertIsNotNone(data['error'])
        self.assertEqual(response.get_status_code(), 404)

    def test_cannot_access_route_if_endpoint_instantiation_fails(self):
        routes = {'test': TestEndpoint}
        TestEndpoint.__init__ = MagicMock(side_effect=Exception('Failed to instantiate'))

        response = self.request_dispatcher.dispatch_request(routes, 'test', Request.from_values())
        data = response.get_data()

        TestEndpoint.__init__ = MagicMock(return_value=None)

        self.assertIsNotNone(data['error'])
        self.assertEqual(response.get_status_code(), 500)

    def test_cannot_access_route_if_invalid_request_method(self):
        routes = {'test': TestEndpoint}

        request = Request.from_values()
        request.method = 'POST'

        response = self.request_dispatcher.dispatch_request(routes, 'test', request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])
        self.assertEqual(response.get_status_code(), 405)

    def test_can_dispatch_request(self):
        routes = {'test': TestEndpoint}
        response = self.request_dispatcher.dispatch_request(routes, 'test', Request.from_values())

        self.assertEqual(response.get_data(), '')
        self.assertEqual(response.get_status_code(), 204)
