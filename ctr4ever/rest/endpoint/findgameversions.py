# coding=utf-8

from typing import List

from flask import Request

from ctr4ever.models.gameversion import GameVersion
from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindGameVersions(Endpoint):

    def handle_request(self, request: Request) -> Response:
        game_version_repository: GameVersionRepository = self.container.get('repository.game_version')
        game_versions: List[GameVersion] = game_version_repository.find_by(name=request.args.get('name'))

        return Response({'game_versions' : [game_version.to_dictionary() for game_version in game_versions]})

    def get_accepted_request_method(self) -> str:
        return 'GET'
