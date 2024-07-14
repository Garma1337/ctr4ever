# coding=utf-8

from unittest import TestCase

from flask import Config, Request

from ctr4ever.rest.endpoint.findgameversions import FindGameVersions
from ctr4ever.services.container import Container
from ctr4ever.tests.mockmodelrepository import MockGameVersionRepository


class FindGameVersionsTest(TestCase):

    def setUp(self):
        self.game_version_repository = MockGameVersionRepository()
        self.game_version_repository.create('PAL', 'pal.png')
        self.game_version_repository.create('NTSC-U', 'ntscu.png')
        self.game_version_repository.create('NTSC-J', 'ntscj.png')

        self.container = Container()
        self.container.register('repository.game_version', lambda: self.game_version_repository)

        self.find_game_versions_endpoint = FindGameVersions(self.container, Config(''))

    def test_can_find_game_versions(self):
        request = Request.from_values()

        response = self.find_game_versions_endpoint.handle_request(request)
        data = response.get_data()

        game_versions = data['game_versions']

        self.assertEqual(3, len(game_versions))
        self.assertEqual(1, game_versions[0]['id'])
        self.assertEqual('PAL', game_versions[0]['name'])
        self.assertEqual('pal.png', game_versions[0]['icon'])
        self.assertEqual(2, game_versions[1]['id'])
        self.assertEqual('NTSC-U', game_versions[1]['name'])
        self.assertEqual('ntscu.png', game_versions[1]['icon'])
        self.assertEqual(3, game_versions[2]['id'])
        self.assertEqual('NTSC-J', game_versions[2]['name'])
        self.assertEqual('ntscj.png', game_versions[2]['icon'])

    def test_can_find_game_versions_filtered_by_name(self):
        request = Request.from_values(query_string='name=PAL')

        response = self.find_game_versions_endpoint.handle_request(request)
        data = response.get_data()

        game_versions = data['game_versions']

        self.assertEqual(1, len(game_versions))
        self.assertEqual('PAL', game_versions[0]['name'])
        self.assertEqual('pal.png', game_versions[0]['icon'])

    def test_can_find_game_versions_filtered_by_name_not_found(self):
        request = Request.from_values(query_string='name=NTSC')

        response = self.find_game_versions_endpoint.handle_request(request)
        data = response.get_data()

        game_versions = data['game_versions']

        self.assertEqual(0, len(game_versions))
