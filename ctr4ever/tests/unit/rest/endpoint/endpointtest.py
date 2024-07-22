# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask import Request

from ctr4ever.tests.mockendpoint import MockEndpoint


class EndpointTest(TestCase):

    def setUp(self):
        self.endpoint = MockEndpoint()

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

    def test_raises_error_when_not_logged_in(self):
        self.endpoint._get_current_user = Mock(return_value=None)

        with self.assertRaises(ValueError):
            self.endpoint.assert_user_is_authenticated()
