# coding=utf-8

from unittest import TestCase

from flask import Config, Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.services.container import Container


class TestEndpoint(Endpoint):

    def handle_request(self, request: Request):
        pass

    def get_accepted_request_method(self) -> str:
        pass


class EndpointTest(TestCase):

    def setUp(self):
        self.endpoint = TestEndpoint(Container(), Config(''))

    def test_can_get_boolean_query_parameter(self):
        request = Request.from_values(query_string='active=1')
        parameter = self.endpoint._get_boolean_query_parameter(request, 'active')

        self.assertTrue(parameter)

    def test_can_get_boolean_query_parameter_with_false_value(self):
        request = Request.from_values(query_string='active=0')
        parameter = self.endpoint._get_boolean_query_parameter(request, 'active')

        self.assertFalse(parameter)

    def test_can_get_boolean_query_parameter_with_no_value(self):
        request = Request.from_values(query_string='')
        parameter = self.endpoint._get_boolean_query_parameter(request, 'active')

        self.assertIsNone(parameter)

    def test_can_get_boolean_query_parameter_with_no_parameter(self):
        request = Request.from_values(query_string='')
        parameter = self.endpoint._get_boolean_query_parameter(request, 'active')

        self.assertIsNone(parameter)
