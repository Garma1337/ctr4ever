# coding=utf-8

from flask import session

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response, ErrorResponse


class LogoutPlayer(Endpoint):

    def handle_request(self, request) -> Response:
        if not session.get('player_id'):
            return ErrorResponse('You are not logged in.')

        session.clear()

        return Response({'success': True})

    def get_accepted_request_method(self) -> str:
        return 'POST'
