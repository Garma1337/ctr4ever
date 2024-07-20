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
            'registerPlayer': 'api.endpoint.register_player',
            'loginPlayer': 'api.endpoint.login_player',
            'logoutPlayer': 'api.endpoint.logout_player',
            'characters': 'api.endpoint.find_characters',
            'categories': 'api.endpoint.find_categories',
            'countries': 'api.endpoint.find_countries',
            'engineStyles': 'api.endpoint.find_engine_styles',
            'gameVersions': 'api.endpoint.find_game_versions',
            'players': 'api.endpoint.find_players',
            'rulesets': 'api.endpoint.find_rulesets',
            'submissions': 'api.endpoint.find_submissions',
            'tracks': 'api.endpoint.find_tracks',
            'createSubmission': 'api.endpoint.create_submission'
        }

        for route, endpoint_service_key in routes.items():
            route_resolver.add_route(route, endpoint_service_key)

        return route_resolver
