# coding=utf-8

from flask import Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response
from ctr4ever.services.authenticator import RegistrationError


class RegisterPlayer(Endpoint):

    def handle_request(self, request: Request) -> Response:
        country_id = request.json.get('country_id')
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')

        if not country_id:
            return Response({'error': 'A country is required.'})

        if not username:
            return Response({'error': 'A username is required.'})

        if not password:
            return Response({'error': 'Password is required.'})

        if not email:
            return Response({'error': 'Email is required.'})

        authenticator = self.container.get('services.authenticator')

        try:
            player = authenticator.register_player(
                country_id,
                username,
                email,
                password
            )
        except RegistrationError as e:
            return Response({'error': f'Failed to register: {str(e)}'})

        return Response({'success': True, 'player': player.to_dictionary()})

    def get_accepted_request_method(self) -> str:
        return 'POST'
