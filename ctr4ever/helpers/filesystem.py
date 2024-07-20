# coding=utf-8

import os


class FileSystem(object):

    @staticmethod
    def file_exists(file_name: str) -> bool:
        return os.path.exists(file_name)

    @staticmethod
    def read_file(file_name: str) -> str:
        with open(file_name) as file_pointer:
            return file_pointer.read()

    @staticmethod
    def get_current_directory() -> str:
        return os.path.dirname(os.path.realpath(__file__))
