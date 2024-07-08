# coding=utf-8

from flask import Request

from ctr4ever.models.gameversion import GameVersion
from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class GetGameVersion(Endpoint):

    def handle_request(self, request: Request) -> Response:
        if not 'id' in request.args:
            return Response({'error': 'Parameter "id" is required'})

        id = int(request.args.get('id'))
        game_version_repository: GameVersionRepository = self.container.get('repository.game_version_repository')

        game_version: GameVersion = game_version_repository.find_one(id)

        if not game_version:
            return Response({'error': f'No game version with id {id} found'})

        return Response({'game_version' : game_version.to_dictionary()})

    def get_accepted_request_method(self) -> str:
        return 'GET'
