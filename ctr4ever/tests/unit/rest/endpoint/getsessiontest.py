# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask import Request

from ctr4ever.rest.endpoint.getsession import GetSession


class GetSessionTest(TestCase):

    def setUp(self):
        self.get_session_endpoint = GetSession()

    def test_can_get_session_when_logged_in(self):
        self.get_session_endpoint._get_current_user = Mock(return_value={'id': 1, 'name': 'Garma'})

        response = self.get_session_endpoint.handle_request(Request.from_values())

        data = response.get_data()
        self.assertEqual(data['current_user'], {'id': 1, 'name': 'Garma'})

    def test_can_get_session_when_not_logged_in(self):
        self.get_session_endpoint._get_current_user = Mock(return_value=None)

        response = self.get_session_endpoint.handle_request(Request.from_values())

        data = response.get_data()
        self.assertIsNone(data['current_user'])
