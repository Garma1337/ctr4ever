# coding=utf-8
from datetime import datetime
from unittest import TestCase

from ctr4ever.services.authenticator import Authenticator, RegistrationError
from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.tests.mockmodelrepository import MockPlayerRepository, MockCountryRepository
from ctr4ever.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class AuthenticatorTest(TestCase):

    def setUp(self):
        self.password_manager = PasswordManager(MockPasswordEncoderStrategy())
        self.country_repository = MockCountryRepository()
        self.player_repository = MockPlayerRepository()

        self.germany = self.country_repository.create('Germany', 'de.png')
        self.netherlands = self.country_repository.create('Netherlands', 'nl.png')

        self.garma = self.player_repository.create(
            self.germany.id,
            'Garma',
            'email@domain.com',
            '98a16c09b0759e63ef7df53592724e8eeddb953a',
            '123456',
            True,
            datetime.now()
        )

        self.authenticator = Authenticator(self.password_manager, self.country_repository, self.player_repository)

    def test_can_authenticate_player(self):
        self.assertTrue(self.authenticator.authenticate_player('Garma', 'password'))

    def test_can_not_authenticate_player_if_wrong_password(self):
        self.assertFalse(self.authenticator.authenticate_player('Garma', 'password1'))

    def test_can_not_authenticate_player_if_wrong_username(self):
        self.assertFalse(self.authenticator.authenticate_player('Garma1', 'password'))

    def test_can_not_authenticate_player_if_wrong_username_and_password(self):
        self.assertFalse(self.authenticator.authenticate_player('Garma1', 'password1'))

    def test_can_register_player(self):
        player = self.authenticator.register_player(self.netherlands.id, 'Dutchesss', 'email2@domain2.com', 'ruheoiI"1122"!#xx')
        self.assertIsNotNone(player)

    def test_can_not_register_player_if_country_does_not_exist(self):
        with self.assertRaises(RegistrationError) as context:
            self.authenticator.register_player(3, 'Dutchesss', 'email2@domain2.com', 'ruheoiI"1122"!#xx')

    def test_can_not_register_player_if_username_already_exists(self):
        with self.assertRaises(RegistrationError) as context:
            self.authenticator.register_player(self.germany.id, 'Garma', 'email2@domain2.com', 'ruheoiI"1122"!#xx')

    def test_can_not_register_player_if_email_already_exists(self):
        with self.assertRaises(RegistrationError) as context:
            self.authenticator.register_player(self.netherlands.id, 'Dutchesss', 'email@domain.com', 'ruheoiI"1122"!#xx')

    def test_can_not_register_player_if_password_is_not_secure(self):
        with self.assertRaises(RegistrationError) as context:
            self.authenticator.register_player(self.netherlands.id, 'Dutchesss', 'email2@domain2.com', 'password')
