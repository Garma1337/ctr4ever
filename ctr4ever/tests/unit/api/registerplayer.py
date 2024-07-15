# coding=utf-8

from unittest import TestCase

from flask import Request

from ctr4ever.rest.endpoint.registerplayer import RegisterPlayer
from ctr4ever.services.authenticator import Authenticator
from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.tests.mockmodelrepository import MockPlayerRepository, MockCountryRepository
from ctr4ever.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class RegisterPlayerTest(TestCase):

    def setUp(self):
        self.country_repository = MockCountryRepository()
        self.player_repository = MockPlayerRepository()

        self.germany = self.country_repository.create('Germany')

        self.authenticate_endpoint = RegisterPlayer(Authenticator(
            PasswordManager(MockPasswordEncoderStrategy()),
            self.country_repository,
            self.player_repository
        ))

    def test_can_register_player(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'country_id': self.germany.id,
                'username': 'Garma',
                'email': 'email@domain.com',
                'password': 'Password123!',
            }
        ))

        data = response.get_data()

        self.assertTrue(data['success'])
        self.assertIsNotNone(data['player'])

        # this is covered by other tests but it's good to have it here as well
        self.assertFalse('password' in data['player'])
        self.assertFalse('email' in data['player'])
        self.assertFalse('salt' in data['player'])

    def test_can_not_register_player_if_no_country(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'username': 'Garma',
                'email': 'email@domain.com',
                'password': 'Password',
            }
        ))

        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_register_player_if_no_username(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'country_id': self.germany.id,
                'email': 'email@domain.com',
                'password': 'Password',
            }
        ))

        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_register_player_if_no_email(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'country_id': self.germany.id,
                'username': 'Garma',
                'password': 'Password',
            }
        ))

        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_register_player_if_no_password(self):
        response = self.authenticate_endpoint.handle_request(Request.from_values(
            json={
                'country_id': self.germany.id,
                'username': 'Garma',
                'email': 'email@domain.com',
            }
        ))

        data = response.get_data()

        self.assertIsNotNone(data['error'])
