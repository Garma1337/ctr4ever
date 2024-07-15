# coding=utf-8

from typing import List

from flask import Request

from ctr4ever.models.enginestyle import EngineStyle
from ctr4ever.models.repository.enginestylerepository import EngineStyleRepository
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindEngineStyles(Endpoint):

    def handle_request(self, request: Request) -> Response:
        engine_style_repository: EngineStyleRepository = self.container.get('repository.engine_style')
        engine_styles: List[EngineStyle] = engine_style_repository.find_by(name=request.args.get('name'))

        return Response({'engine_styles' : [engine_style.to_dictionary() for engine_style in engine_styles]})

    def get_accepted_request_method(self) -> str:
        return 'GET'
