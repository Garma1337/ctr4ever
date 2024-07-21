# coding=utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from flask import Request

from ctr4ever.rest.endpoint.loginplayer import LoginPlayer
from ctr4ever.services.authenticator import Authenticator
from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.tests.mockmodelrepository import MockCountryRepository, MockPlayerRepository
from ctr4ever.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class LoginPlayerTest(TestCase):

    def setUp(self):
        self.country_repository = MockCountryRepository()
        self.player_repository = MockPlayerRepository()
        self.password_manager = PasswordManager(MockPasswordEncoderStrategy())

        self.player_repository.create(
            1,
            'Garma',
            'email@domain.com',
            '98a16c09b0759e63ef7df53592724e8eeddb953a',
            '123456',
            True,
            datetime.now()
        )

        self.authenticator = Authenticator(self.password_manager, self.country_repository, self.player_repository)
        self.login_player_endpoint = LoginPlayer(self.player_repository, self.authenticator)

        self.login_player_endpoint._get_current_user = Mock(return_value=None)
        self.login_player_endpoint._create_access_token = Mock(return_value='123456')

    def test_can_login_player(self):
        response = self.login_player_endpoint.handle_request(Request.from_values(json={
            'username': 'Garma',
            'password': 'password'
        }))

        data = response.get_data()

        self.assertTrue(data['success'])
        self.assertIsNotNone(data['access_token'])

    def test_can_not_login_player_with_wrong_password(self):
        response = self.login_player_endpoint.handle_request(Request.from_values(json={
            'username': 'Garma',
            'password': 'wrongpassword'
        }))

        data = response.get_data()
        self.assertFalse(data['success'])
        self.assertNotIn('access_token', data)

    def test_can_not_login_player_with_wrong_username(self):
        response = self.login_player_endpoint.handle_request(Request.from_values(json={
            'username': 'GarmaWrong',
            'password': 'password'
        }))

        data = response.get_data()
        self.assertFalse(data['success'])
        self.assertNotIn('access_token', data)

    def test_can_not_login_player_with_wrong_username_and_password(self):
        response = self.login_player_endpoint.handle_request(Request.from_values(json={
            'username': 'GarmaWrong',
            'password': 'wrongpassword'
        }))

        data = response.get_data()
        self.assertFalse(data['success'])
        self.assertNotIn('access_token', data)

    def test_can_not_login_player_with_empty_username(self):
        response = self.login_player_endpoint.handle_request(Request.from_values(json={
            'username': '',
            'password': 'password'
        }))

        data = response.get_data()
        self.assertFalse(data['success'])
        self.assertNotIn('access_token', data)

    def test_can_not_login_player_with_empty_password(self):
        response = self.login_player_endpoint.handle_request(Request.from_values(json={
            'username': 'Garma',
            'password': ''
        }))

        data = response.get_data()
        self.assertFalse(data['success'])
        self.assertNotIn('access_token', data)

    def test_can_not_login_player_when_player_is_already_logged_in(self):
        self.login_player_endpoint._get_current_user = Mock(return_value={'name': 'Garma'})

        response = self.login_player_endpoint.handle_request(Request.from_values(json={
            'username': 'Garma',
            'password': 'password'
        }))

        data = response.get_data()

        self.assertFalse(data['success'])
        self.assertNotIn('access_token', data)
