# coding=utf-8

from flask import Request, session

from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response, ErrorResponse
from ctr4ever.services.authenticator import Authenticator


class LoginPlayer(Endpoint):

    def __init__(self, player_repository: PlayerRepository, authenticator: Authenticator):
        self.player_repository = player_repository
        self.authenticator = authenticator

    def handle_request(self, request: Request) -> Response:
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

        session['player_id'] = player.id
        session['username'] = player.name

        return Response({'success': True})

    def get_accepted_request_method(self) -> str:
        return 'POST'
