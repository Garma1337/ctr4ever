# coding=utf-8

from abc import ABC, abstractmethod
from typing import Optional

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

    def _get_boolean_query_parameter(self, request: Request, parameter_name: str) -> Optional[bool]:
        parameter = request.args.get(parameter_name)

        if parameter is not None:
            return bool(int(parameter))

        return None
