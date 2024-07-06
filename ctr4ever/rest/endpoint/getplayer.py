# coding=utf-8

from flask import Request

from ctr4ever.models.player import Player
from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.rest.endpoint.baseendpoint import BaseEndpoint
from ctr4ever.rest.response import Response


class GetPlayer(BaseEndpoint):

    def handle_request(self, request: Request):
        if not 'id' in request.args:
            return Response({'error': 'Parameter "id" is required'})

        id = int(request.args.get('id'))
        player_repository: PlayerRepository = self.container.get('repository.player_repository')

        player: Player = player_repository.find_one(id)

        if not player:
            return Response({'error': f'No player with id {id} found'})

        return Response({'player' : player.to_dictionary()})

    def get_accepted_request_method(self) -> str:
        return 'GET'
