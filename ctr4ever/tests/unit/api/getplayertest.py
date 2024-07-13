# coding=utf-8

from unittest import TestCase

from flask import Config
from werkzeug import Request

from ctr4ever.rest.endpoint.getplayer import GetPlayer
from ctr4ever.services.container import Container
from ctr4ever.tests.mockmodelrepository import MockPlayerRepository


class GetPlayerTest(TestCase):

    def setUp(self):
        self.player_repository = MockPlayerRepository()
        self.player_repository.create(1, 'Garma', 'email@domain.com', '$2a$12$nZ08AihzKUC1TXIJPdTUQOvCQQe0LZePgnMRFiTo6v6Y.cmxRV8zO', '123456', True)

        self.container = Container()
        self.container.register('repository.player_repository', lambda: self.player_repository)

        self.get_player_endpoint = GetPlayer(self.container, Config(''))

    def test_can_get_player(self):
        request = Request.from_values(path = 'player?id=1')
        response = self.get_player_endpoint.handle_request(request)
        data = response.get_data()

        self.assertEqual(
            data,
            {
                'player': {
                    'id': 1,
                    'country_id': 1,
                    'name': 'Garma',
                    'active': True,
                    'country' : None,
                    'submissions' : []
                }
            }
        )

    def test_can_not_get_sensitive_player_data(self):
        request = Request.from_values(path = 'player?id=1')
        response = self.get_player_endpoint.handle_request(request)
        data = response.get_data()

        self.assertNotIn('email', data['player'])
        self.assertNotIn('password', data['player'])
        self.assertNotIn('salt', data['player'])

    def test_can_not_get_player_when_player_not_exists(self):
        request = Request.from_values(path = 'player?id=2')

        response = self.get_player_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_get_player_when_id_missing(self):
        request = Request.from_values(path = 'player')

        response = self.get_player_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])
