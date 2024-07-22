# coding=utf-8

from typing import List

from flask import Request

from ctr4ever.models.platform import Platform
from ctr4ever.models.repository.platformrepository import PlatformRepository
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindPlatforms(Endpoint):

    def __init__(self, platform_repository: PlatformRepository):
        self.platform_repository = platform_repository

    def handle_request(self, request: Request) -> Response:
        platforms: List[Platform] = self.platform_repository.find_by(name=request.args.get('name'))

        return Response({'platforms' : [platform.to_dictionary() for platform in platforms]})

    def get_accepted_request_method(self) -> str:
        return 'GET'

    def require_authentication(self) -> bool:
        return False
