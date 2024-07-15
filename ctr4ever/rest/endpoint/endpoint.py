# coding=utf-8

from abc import ABC, abstractmethod
from typing import Optional

from flask import Request

from ctr4ever.rest.response import Response


class Endpoint(ABC):

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
