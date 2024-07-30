# coding=utf-8

from datetime import datetime
from unittest import TestCase

from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.services.validator.playervalidator import PlayerValidator
from ctr4ever.services.validator.validator import ValidationError
from ctr4ever.tests.mockmodelrepository import MockPlayerRepository, MockCountryRepository
from ctr4ever.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class PlayerValidatorTest(TestCase):

    def setUp(self):
        self.player_repository = MockPlayerRepository()
        self.country_repository = MockCountryRepository()
        self.password_manager = PasswordManager(MockPasswordEncoderStrategy())

        self.player_validator = PlayerValidator(self.country_repository, self.player_repository, self.password_manager)

    def test_can_validate_player_name(self):
        self.player_validator.validate_name('Garma')

    def test_can_not_validate_empty_player_name(self):
        with self.assertRaises(ValidationError):
            self.player_validator.validate_name('')

    def test_can_not_validate_existing_player_name(self):
        self.player_repository.create(1, 'Garma', 'test@test.com', 'password', '123456', True, datetime.now())

        with self.assertRaises(ValidationError):
            self.player_validator.validate_name('Garma')

    def test_can_validate_player_email(self):
        self.player_validator.validate_email('test@test.com')

    def test_can_not_validate_empty_player_email(self):
        with self.assertRaises(ValidationError):
            self.player_validator.validate_email('')

    def test_can_not_validate_existing_player_email(self):
        self.player_repository.create(1, 'Garma', 'test@test.com', 'password', '123456', True, datetime.now())

        with self.assertRaises(ValidationError):
            self.player_validator.validate_email('test@test.com')

    def test_can_validate_player_password(self):
        self.player_validator.validate_password('Password123!')

    def test_can_not_validate_insecure_player_password(self):
        with self.assertRaises(ValidationError):
            self.player_validator.validate_password('password')

    def test_can_validate_player_country_id(self):
        country = self.country_repository.create('United States', 'us.png')
        self.player_validator.validate_country(country.id)

    def test_can_not_validate_empty_player_country_id(self):
        with self.assertRaises(ValidationError):
            self.player_validator.validate_country(None)

    def test_can_not_validate_nonexistent_player_country_id(self):
        with self.assertRaises(ValidationError):
            self.player_validator.validate_country(1)
