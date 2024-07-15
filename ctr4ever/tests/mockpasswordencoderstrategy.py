# coding=utf-8

import hashlib

from ctr4ever.services.password_encoder_strategy.passwordencoderstrategy import PasswordEncoderStrategy


class MockPasswordEncoderStrategy(PasswordEncoderStrategy):

    def generate_salt(self) -> str:
        return '123456'

    def encode_password(self, password: str, salt: str) -> str:
        return hashlib.sha1(f'{password}{salt}'.encode()).hexdigest()
