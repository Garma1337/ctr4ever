# coding=utf-8

from flask import session, Request

from ctr4ever.rest.endpoint.logoutplayer import LogoutPlayer
from ctr4ever.tests.integration.integrationtestbase import IntegrationTest


class LogoutPlayerTest(IntegrationTest):

    def setUp(self):
        self.logout_player_endpoint = LogoutPlayer()

    def test_can_logout_player(self):
        with self.app.test_request_context():
            session['player_id'] = 1
            response = self.logout_player_endpoint.handle_request(Request.from_values())

            data = response.get_data()

            self.assertTrue(data['success'])
            self.assertIsNone(session.get('player_id'))

    def test_cannot_logout_player_when_not_logged_in(self):
        with self.app.test_request_context():
            response = self.logout_player_endpoint.handle_request(Request.from_values())

            data = response.get_data()

            self.assertFalse(data['success'])
            self.assertIsNone(session.get('player_id'))
