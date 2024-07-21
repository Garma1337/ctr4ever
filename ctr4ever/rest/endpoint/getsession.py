# coding=utf-8

from flask import Request
from flask_jwt_extended import get_jwt_identity

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class GetSession(Endpoint):

    def handle_request(self, request: Request) -> Response:
        current_user = self._get_current_user()
        return Response({'current_user': current_user})

    def _get_current_user(self):
        return get_jwt_identity()

    def get_accepted_request_method(self) -> str:
        return 'GET'
