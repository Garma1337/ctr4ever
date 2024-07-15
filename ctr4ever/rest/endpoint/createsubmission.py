# coding=utf-8

from ctr4ever.rest.endpoint.endpoint import Endpoint


class CreateSubmission(Endpoint):

    def handle_request(self, request):
        return {'success': True}

    def get_accepted_request_method(self):
        return 'POST'
