# coding=utf-8

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import EmptyResponse


class MockEndpoint(Endpoint):

    def handle_request(self, request):
        return EmptyResponse()

    def get_accepted_request_method(self):
        return 'GET'

    def require_authentication(self):
        return False
