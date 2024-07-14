# coding=utf-8

from typing import List

from flask import Request

from ctr4ever.helpers.pagination import Pagination
from ctr4ever.models.player import Player
from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindPlayers(Endpoint):

    def handle_request(self, request: Request):
        player_repository: PlayerRepository = self.container.get('repository.player')

        active = self._get_boolean_query_parameter(request, 'active')

        player_count = player_repository.count(
            country_id=request.args.get('country_id'),
            name=request.args.get('name'),
            email=request.args.get('email'),
            active=active
        )

        pagination = Pagination(request.args.get('page', 1), request.args.get('per_page', 20), player_count)

        players: List[Player] = player_repository.find_by(
            country_id=request.args.get('country_id'),
            name=request.args.get('name'),
            email=request.args.get('email'),
            active=active,
            limit=pagination.get_limit(),
            offset=pagination.get_offset()
        )

        return Response({'pagination': pagination.to_dictionary(), 'players' : [player.to_dictionary() for player in players]})

    def get_accepted_request_method(self) -> str:
        return 'GET'
