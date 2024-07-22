# coding=utf-8

from unittest import TestCase

from flask import Request

from ctr4ever.rest.endpoint.findplatforms import FindPlatforms
from ctr4ever.tests.mockmodelrepository import MockPlatformRepository


class FindPlatformsTest(TestCase):

    def setUp(self):
        self.platform_repository = MockPlatformRepository()
        self.platform_repository.create('Console (PS1)')
        self.platform_repository.create('Emulator')

        self.find_platforms_endpoint = FindPlatforms(self.platform_repository)

    def test_can_find_platforms(self):
        request = Request.from_values()

        response = self.find_platforms_endpoint.handle_request(request)
        data = response.get_data()

        platforms = data['platforms']

        self.assertEqual(2, len(platforms))
        self.assertEqual(1, platforms[0]['id'])
        self.assertEqual('Console (PS1)', platforms[0]['name'])
        self.assertEqual(2, platforms[1]['id'])
        self.assertEqual('Emulator', platforms[1]['name'])

    def test_can_find_platforms_filtered_by_name(self):
        request = Request.from_values(query_string='name=Emulator')

        response = self.find_platforms_endpoint.handle_request(request)
        data = response.get_data()

        platforms = data['platforms']

        self.assertEqual(1, len(platforms))
        self.assertEqual('Emulator', platforms[0]['name'])

    def test_can_find_platforms_filtered_by_name_not_found(self):
        request = Request.from_values(query_string='name=Console')

        response = self.find_platforms_endpoint.handle_request(request)
        data = response.get_data()

        platforms = data['platforms']

        self.assertEqual(0, len(platforms))
