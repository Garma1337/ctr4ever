# coding=utf-8

import re

from ctr4ever.services.password_encoder_strategy.passwordencoderstrategy import PasswordEncoderStrategy


class Password(object):

    def __init__(self, hash_value: str, salt: str):
        self.hash_value = hash_value
        self.salt = salt


class PasswordManager(object):

    def __init__(self, password_encoder_strategy: PasswordEncoderStrategy):
        self.password_encoder_strategy = password_encoder_strategy

    def generate_salt(self) -> str:
        return self.password_encoder_strategy.generate_salt()

    def encode_password(self, password: str, salt: str) -> str:
        return self.password_encoder_strategy.encode_password(password, salt)

    def check_password(self, provided_password: str, stored_password: str, stored_salt: str) -> bool:
        encoded_provided_password = self.password_encoder_strategy.encode_password(provided_password, stored_salt)
        return stored_password == encoded_provided_password

    def is_secure_password(self, password: str) -> bool:
        if len(password) < 8:
            return False

        if not re.search(r'[a-z]', password):
            return False

        if not re.search(r'[A-Z]', password):
            return False

        if not re.search(r'[0-9]', password):
            return False

        if not re.search(r'[@_!#$%^&*()<>?/|}{~:]', password):
            return False

        return True
