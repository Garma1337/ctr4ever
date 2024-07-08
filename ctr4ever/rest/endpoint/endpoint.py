# coding=utf-8

from abc import ABC, abstractmethod

from flask import Request, Config

from ctr4ever.rest.response import Response
from ctr4ever.services.container import Container


class Endpoint(ABC):

    def __init__(self, container: Container, app_config: Config):
        self.container = container
        self.app_config = app_config

    @abstractmethod
    def handle_request(self, request: Request) -> Response:
        pass

    @abstractmethod
    def get_accepted_request_method(self) -> str:
        pass
