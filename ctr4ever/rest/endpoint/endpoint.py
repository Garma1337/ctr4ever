# coding=utf-8

from abc import ABC, abstractmethod
from typing import Optional

from flask import Request
from flask_jwt_extended import get_jwt_identity

from ctr4ever.rest.response import Response


class Endpoint(ABC):

    @abstractmethod
    def handle_request(self, request: Request) -> Response:
        pass

    @abstractmethod
    def get_accepted_request_method(self) -> str:
        pass

    @abstractmethod
    def require_authentication(self) -> bool:
        pass

    def assert_user_is_authenticated(self):
        if not self._get_current_user():
            raise ValueError('You need to be authenticated to perform this action.')

    def _get_current_user(self):
        return get_jwt_identity()

    def _get_boolean_query_parameter(self, request: Request, parameter_name: str) -> Optional[bool]:
        parameter = request.args.get(parameter_name)

        if parameter is not None:
            return bool(int(parameter))

        return None
