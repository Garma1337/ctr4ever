# coding=utf-8

from unittest import TestCase

from flask import Config, Request

from ctr4ever.rest.endpoint.getgameversions import GetGameVersion
from ctr4ever.services.container import Container
from ctr4ever.tests.mockmodelrepository import MockGameVersionRepository


class GetGameVersionTest(TestCase):

    def setUp(self):
        self.game_version_repository = MockGameVersionRepository()
        self.game_version_repository.create('PAL', 'pal.png')

        self.container = Container()
        self.container.register('repository.game_version_repository', lambda: self.game_version_repository)

        self.get_game_version_endpoint = GetGameVersion(self.container, Config(''))

    def test_can_get_game_version(self):
        request = Request.from_values(path = 'gameversion?id=1')
        response = self.get_game_version_endpoint.handle_request(request)
        data = response.get_data()

        self.assertEqual(
            data,
            {
                'game_version': {
                    'id': 1,
                    'name': 'PAL',
                    'icon': 'pal.png',
                    'submissions': []
                }
            }
        )

    def test_can_not_get_game_version_when_game_version_not_exists(self):
        request = Request.from_values(path = 'gameversion?id=2')

        response = self.get_game_version_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_get_game_version_when_id_missing(self):
        request = Request.from_values(path = 'gameversion')

        response = self.get_game_version_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])
