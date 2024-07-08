# coding=utf-8

from flask import Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindPlayerSubmissions(Endpoint):

    def handle_request(self, request: Request) -> Response:
        pass

    def get_accepted_request_method(self) -> str:
        pass
