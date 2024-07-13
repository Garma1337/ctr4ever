# coding=utf-8

from abc import abstractmethod


class Installer(object):

    @abstractmethod
    def install(self, file_name: str):
        pass
