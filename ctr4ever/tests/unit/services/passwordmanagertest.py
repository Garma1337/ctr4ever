# coding=utf-8

from unittest import TestCase

from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class PasswordManagerTest(TestCase):

    def setUp(self):
        self.password_encoder_strategy = MockPasswordEncoderStrategy()
        self.password_manager = PasswordManager(self.password_encoder_strategy)

    def test_can_generate_salt(self):
        self.assertEqual('123456', self.password_manager.generate_salt())

    def test_can_encode_password(self):
        self.assertEqual('password', self.password_manager.encode_password('password', '123456'))

    def test_can_check_password(self):
        self.assertTrue(self.password_manager.check_password('password', 'password', '123456'))

    def test_can_not_check_password_if_wrong_salt_provided(self):
        self.assertFalse(self.password_manager.check_password('password', '98a16c09b0759e63ef7df53592724e8eeddb953a', '987654'))

    def test_can_not_check_password_if_wrong_password_provided(self):
        self.assertFalse(self.password_manager.check_password('password1', '98a16c09b0759e63ef7df53592724e8eeddb953a', '123456'))

    def test_can_not_check_password_if_wrong_hash_provided(self):
        self.assertFalse(self.password_manager.check_password('password', '7c4a8d09ca3762af61e59520943dc265', '123456'))

    def test_can_validate_secure_password(self):
        self.assertTrue(self.password_manager.is_secure_password('Password123!'))

    def test_can_not_validate_insecure_password(self):
        self.assertFalse(self.password_manager.is_secure_password('password'))

    def test_can_not_validate_insecure_password_with_no_digits(self):
        self.assertFalse(self.password_manager.is_secure_password('Password'))

    def test_can_not_validate_insecure_password_with_no_uppercase(self):
        self.assertFalse(self.password_manager.is_secure_password('password123'))

    def test_can_not_validate_insecure_password_with_no_lowercase(self):
        self.assertFalse(self.password_manager.is_secure_password('PASSWORD123'))

    def test_can_not_validate_insecure_password_with_no_special_characters(self):
        self.assertFalse(self.password_manager.is_secure_password('Password123'))
