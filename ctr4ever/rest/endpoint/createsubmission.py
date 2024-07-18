# coding=utf-8

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class CreateSubmission(Endpoint):

    def handle_request(self, request):
        return Response({'submissions': []})

    def get_accepted_request_method(self):
        return 'POST'
