# coding=utf-8

import bcrypt

from ctr4ever.services.password_encoder_strategy.passwordencoderstrategy import PasswordEncoderStrategy


class BcryptPasswordEncoderStrategy(PasswordEncoderStrategy):

    def __init__(self):
        self._salt_rounds = 12

    def generate_salt(self) -> str:
        return bcrypt.gensalt(self._salt_rounds).decode()

    def encode_password(self, password: str, salt: str) -> str:
        hash_value = bcrypt.hashpw(password.encode(), salt.encode())
        return hash_value.decode()
