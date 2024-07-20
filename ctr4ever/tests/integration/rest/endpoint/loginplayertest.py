# coding=utf-8

from flask import Request, session

from ctr4ever.models.repository.countryrepository import CountryRepository
from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.rest.endpoint.loginplayer import LoginPlayer
from ctr4ever.services.authenticator import Authenticator
from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.tests.integration.integrationtestbase import IntegrationTest
from ctr4ever.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class LoginPlayerTest(IntegrationTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.player_repository = PlayerRepository(cls.db)
        cls.country_repository = CountryRepository(cls.db)

        with cls.app.app_context():
            germany = cls.country_repository.create('Germany', 'de.png')

            cls.garma = cls.player_repository.create(
                germany.id,
                'Garma',
                'email@domain.com',
                '98a16c09b0759e63ef7df53592724e8eeddb953a',
                '123456',
                True
            )

    def setUp(self):
        self.password_manager = PasswordManager(MockPasswordEncoderStrategy())

        self.authenticator = Authenticator(self.password_manager, self.country_repository, self.player_repository)
        self.login_player_endpoint = LoginPlayer(self.player_repository, self.authenticator)

    def test_can_login_player(self):
        with self.app.test_request_context():
            response = self.login_player_endpoint.handle_request(Request.from_values(json={
                'username': 'Garma',
                'password': 'password'
            }))

            data = response.get_data()

            self.assertTrue(data['success'])
            self.assertEqual(session['player_id'], 1)
            self.assertEqual(session['username'], 'Garma')

    def test_cannot_login_player_with_wrong_password(self):
        with self.app.test_request_context():
            response = self.login_player_endpoint.handle_request(Request.from_values(json={
                'username': 'Garma',
                'password': 'wrongpassword'
            }))

            data = response.get_data()
            self.assertFalse(data['success'])

    def test_cannot_login_player_with_wrong_username(self):
        with self.app.test_request_context():
            response = self.login_player_endpoint.handle_request(Request.from_values(json={
                'username': 'GarmaWrong',
                'password': 'password'
            }))

            data = response.get_data()
            self.assertFalse(data['success'])

    def test_cannot_login_player_with_wrong_username_and_password(self):
        with self.app.test_request_context():
            response = self.login_player_endpoint.handle_request(Request.from_values(json={
                'username': 'GarmaWrong',
                'password': 'wrongpassword'
            }))

            data = response.get_data()
            self.assertFalse(data['success'])

    def test_cannot_login_player_with_empty_username(self):
        with self.app.test_request_context():
            response = self.login_player_endpoint.handle_request(Request.from_values(json={
                'username': '',
                'password': 'password'
            }))

            data = response.get_data()
            self.assertFalse(data['success'])

    def test_cannot_login_player_with_empty_password(self):
        with self.app.test_request_context():
            response = self.login_player_endpoint.handle_request(Request.from_values(json={
                'username': 'Garma',
                'password': ''
            }))

            data = response.get_data()
            self.assertFalse(data['success'])
