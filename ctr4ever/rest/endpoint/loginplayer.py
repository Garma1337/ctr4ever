# coding=utf-8

from flask import Request
from flask_jwt_extended import create_access_token, get_jwt_identity

from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response, ErrorResponse
from ctr4ever.services.authenticator import Authenticator


class LoginPlayer(Endpoint):

    def __init__(self, player_repository: PlayerRepository, authenticator: Authenticator):
        self.player_repository = player_repository
        self.authenticator = authenticator

    def handle_request(self, request: Request) -> Response:
        current_user = self._get_current_user()

        if current_user:
            return ErrorResponse(f'You are already logged in as {current_user['name']}.')

        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            return ErrorResponse('A username is required.')

        if not password:
            return ErrorResponse('A password is required.')

        if not self.authenticator.authenticate_player(username, password):
            return ErrorResponse('Invalid username or password.')

        players = self.player_repository.find_by(name=username)
        player = players[0]

        access_token = self._create_access_token(player)
        return Response({'success': True, 'access_token': access_token})

    def _create_access_token(self, player):
        return create_access_token(identity=player)

    def _get_current_user(self):
        return get_jwt_identity()

    def get_accepted_request_method(self) -> str:
        return 'POST'

    def require_authentication(self) -> bool:
        return False
