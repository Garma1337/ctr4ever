# coding=utf-8

from flask import Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response, ErrorResponse
from ctr4ever.rest.routeresolver import RouteResolver, RouteResolverError


class RequestDispatcherErrror(Exception):
    pass


class RequestDispatcher(object):
    """
    Flask does not have a request dispatcher by itself, so handling different requests is normally a lot of
    copy & paste. Since a dynamic request dispatcher is not that much work to create we use a custom one here.
    """

    def __init__(self, route_resolver: RouteResolver) -> None:
        self.route_resolver = route_resolver

    def dispatch_request(self, requested_route: str, request: Request) -> Response:
        if not requested_route:
            return ErrorResponse('No route specified', 400)

        if not self.route_resolver.route_exists(requested_route):
            return ErrorResponse(f'No route {requested_route} exists', 404)

        try:
            endpoint: Endpoint = self.route_resolver.resolve_route(requested_route)
        except RouteResolverError as e:
            return ErrorResponse(str(e), 500)

        if request.method != endpoint.get_accepted_request_method():
            return ErrorResponse(f'Unsupported request method "{request.method}" for endpoint "{endpoint.__class__.__name__}"', 405)

        if endpoint.require_authentication():
            try:
                endpoint.assert_user_is_authenticated()
            except ValueError as e:
                return ErrorResponse(str(e), 401)

        return endpoint.handle_request(request)
