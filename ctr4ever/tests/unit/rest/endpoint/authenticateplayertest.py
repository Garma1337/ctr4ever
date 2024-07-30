# coding=utf-8

from datetime import datetime
from unittest import TestCase

from flask import Request

from ctr4ever.rest.endpoint.authenticateplayer import AuthenticatePlayer
from ctr4ever.services.authenticator import Authenticator
from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.tests.mockmodelrepository import MockPlayerRepository, MockCountryRepository
from ctr4ever.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class AuthenticatePlayerTest(TestCase):

    def setUp(self):
        self.player_repository = MockPlayerRepository()
        self.player_repository.create(
            1,
            'Garma',
            'email@domain.com',
            'Password123!',
            '123456',
            True,
            datetime.now()
        )

        self.authenticate_endpoint = AuthenticatePlayer(Authenticator(
            PasswordManager(MockPasswordEncoderStrategy()),
            MockCountryRepository(),
            self.player_repository
        ))

    def test_can_authenticate_player(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'username': 'Garma',
                'password': 'Password123!'
            }
        ))

        data = response.get_data()

        self.assertTrue(data['success'])

    def test_can_not_authenticate_player_if_wrong_password(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'username': 'Garma',
                'password': 'password1'
            }
        ))

        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_authenticate_player_if_wrong_username(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'username': 'Garma1',
                'password': 'password'
            }
        ))

        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_authenticate_player_if_wrong_username_and_password(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'username': 'Garma1',
                'password': 'password1'
            }
        ))

        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_authenticate_player_if_no_username_provided(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'password': 'password'
            }
        ))

        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_authenticate_player_if_no_password_provided(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'username': 'Garma'
            }
        ))

        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_authenticate_player_if_no_credentials_provided(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(json={}))
        data = response.get_data()

        self.assertIsNotNone(data['error'])
