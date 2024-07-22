# coding=utf-8

from flask import Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response, ErrorResponse, SuccessResponse
from ctr4ever.services.authenticator import RegistrationError, Authenticator


class RegisterPlayer(Endpoint):

    def __init__(self, authenticator: Authenticator):
        self.authenticator = authenticator

    def handle_request(self, request: Request) -> Response:
        country_id = request.json.get('country_id')
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')

        if not country_id:
            return ErrorResponse('A country is required.')

        if not username:
            return ErrorResponse('A username is required.')

        if not password:
            return ErrorResponse('A password is required.')

        if not email:
            return ErrorResponse('An email is required.')

        try:
            player = self.authenticator.register_player(
                country_id,
                username,
                email,
                password
            )
        except RegistrationError as e:
            return ErrorResponse(str(e))

        return SuccessResponse({'player': player.to_dictionary()})

    def get_accepted_request_method(self) -> str:
        return 'POST'

    def require_authentication(self) -> bool:
        return False
