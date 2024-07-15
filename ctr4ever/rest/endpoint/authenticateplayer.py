# coding=utf-8

from flask import Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response
from ctr4ever.services.authenticator import Authenticator


class AuthenticatePlayer(Endpoint):

    def handle_request(self, request: Request) -> Response:
        authenticator: Authenticator = self.container.get('services.authenticator')
        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            return Response({'error': 'Username is required'})

        if not password:
            return Response({'error': 'Password is required'})

        if not authenticator.authenticate_player(username, password):
            return Response({'error': 'The credentials you provided are not correct.'})

        return Response({'success': True})

    def get_accepted_request_method(self) -> str:
        return 'POST'
