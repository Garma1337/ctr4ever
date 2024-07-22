# coding=utf-8

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.services.container import Container, ContainerError


class RouteResolverError(Exception):
    pass


class RouteResolver(object):

    def __init__(self, container: Container):
        self.container = container
        self.routes = {}

    def resolve_route(self, route: str) -> Endpoint:
        try:
            endpoint: Endpoint = self.container.get(self.routes[route])
            return endpoint
        except ContainerError as e:
            raise RouteResolverError(f'Could not find api endpoint service "{self.routes[route]}" in the container')

    def add_route(self, route: str, endpoint_service_key: str):
        if self.route_exists(route):
            raise RouteResolverError(f'Route {route} has already been registered')

        self.routes[route] = endpoint_service_key

    def route_exists(self, route: str):
        return route in self.routes

    def remove_route(self, route: str):
        if not self.route_exists(route):
            raise RouteResolverError(f'Route {route} does not exist')

        del self.routes[route]

    def get_routes(self):
        return self.routes


class RouteResolverFactory(object):

    @staticmethod
    def create(container: Container) -> RouteResolver:
        route_resolver = RouteResolver(container)

        routes = {
            'authenticatePlayer': 'api.endpoint.authenticate_player',
            'categories': 'api.endpoint.find_categories',
            'characters': 'api.endpoint.find_characters',
            'countries': 'api.endpoint.find_countries',
            'createSubmission': 'api.endpoint.create_submission',
            'engineStyles': 'api.endpoint.find_engine_styles',
            'gameVersions': 'api.endpoint.find_game_versions',
            'loginPlayer': 'api.endpoint.login_player',
            'platforms': 'api.endpoint.find_platforms',
            'players': 'api.endpoint.find_players',
            'registerPlayer': 'api.endpoint.register_player',
            'rulesets': 'api.endpoint.find_rulesets',
            'session': 'api.endpoint.get_session',
            'submissions': 'api.endpoint.find_submissions',
            'tracks': 'api.endpoint.find_tracks'
        }

        for route, endpoint_service_key in routes.items():
            route_resolver.add_route(route, endpoint_service_key)

        return route_resolver
