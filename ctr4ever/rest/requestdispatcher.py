# coding=utf-8

from flask import Request, Config

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response
from ctr4ever.services.container import Container


class RequestDispatcherErrror(Exception):
    pass


class RequestDispatcher(object):
    """
    Flask does not have a request dispatcher by itself, so handling different requests is normally a lot of
    copy & paste. Since a dynamic request dispatcher is not that much work to create we use a custom one here.
    """

    def __init__(self, container: Container, app_config: Config) -> None:
        self.container = container
        self.app_config = app_config

    def dispatch_request(self, existing_routes: dict[str, type], requested_route: str, request: Request) -> Response:
        if not requested_route:
            return Response({'error': 'No route specified'}, 400)

        if requested_route not in existing_routes:
            return Response({'error': f'No route {requested_route} exists'}, 404)

        # we should maybe just grab the instance from the container instead of instantiating it manually
        # this would also allow us to keep the dependencies of each endpoint well-defined instead of just
        # making every endpoint dependent on the container ...
        try:
            endpoint: Endpoint = existing_routes[requested_route](self.container, self.app_config)
        except Exception as e:
            return Response({'error': f'Error while instantiating endpoint {existing_routes[requested_route].__name__}: {e}'}, 500)

        if request.method != endpoint.get_accepted_request_method():
            return Response({'error': f'Unsupported request method "{request.method}" for endpoint {existing_routes[requested_route].__name__}'}, 405)

        return endpoint.handle_request(request)
