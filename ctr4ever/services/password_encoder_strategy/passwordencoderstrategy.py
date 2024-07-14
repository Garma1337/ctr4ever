# coding=utf-8

from abc import abstractmethod


class PasswordEncoderStrategy(object):

    @abstractmethod
    def generate_salt(self) -> str:
        pass

    @abstractmethod
    def encode_password(self, password: str, salt: str) -> str:
        pass
