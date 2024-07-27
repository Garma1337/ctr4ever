# coding=utf-8

from flask import Config, Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class GetSettings(Endpoint):

    def __init__(self, app_config: Config):
        self.app_config = app_config

    def handle_request(self, request: Request) -> Response:
        return Response({
            'submission_comment_max_length': self.app_config.get('SUBMISSION_COMMENT_MAX_LENGTH'),
        })

    def get_accepted_request_method(self) -> str:
        return 'GET'

    def require_authentication(self) -> bool:
        return False
