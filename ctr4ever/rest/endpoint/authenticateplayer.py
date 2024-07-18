# coding=utf-8

from flask import Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response, ErrorResponse, SuccessResponse
from ctr4ever.services.authenticator import Authenticator


class AuthenticatePlayer(Endpoint):

    def __init__(self, authenticator: Authenticator):
        self.authenticator = authenticator

    def handle_request(self, request: Request) -> Response:
        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            return ErrorResponse('Username is required')

        if not password:
            return ErrorResponse('Password is required')

        if not self.authenticator.authenticate_player(username, password):
            return ErrorResponse('The credentials you provided are not correct.')

        return SuccessResponse({})

    def get_accepted_request_method(self) -> str:
        return 'POST'
