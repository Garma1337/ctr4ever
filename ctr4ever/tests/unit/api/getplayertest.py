# coding=utf-8

from typing import Optional
from unittest import TestCase
from unittest.mock import MagicMock

from flask import Config
from werkzeug import Request

from ctr4ever.models.player import Player
from ctr4ever.rest.endpoint.getplayer import GetPlayer
from ctr4ever.services.container import Container


class GetPlayerTest(TestCase):

    def setUp(self):
        self.set_up()

    def set_up(self, player: Optional[Player] = None):
        self.player_repository = MagicMock()
        self.player_repository.find_one = MagicMock(return_value=player)

        self.container = Container()
        self.container.register('repository.player_repository', lambda: self.player_repository)

        self.get_player_endpoint = GetPlayer(self.container, Config(''))

    def test_can_get_player(self):
        self.set_up(Player(id=1, country_id=1, name='Garma', email='email@domain.com', password='12345678'))

        request = Request.from_values(path = 'player?id=1')
        response = self.get_player_endpoint.handle_request(request)
        data = response.get_data()

        self.assertEqual(
            data,
            {
                'player': {
                    'id': 1,
                    'name': 'Garma',
                    'country_id': 1,
                    'country' : None,
                    'submissions' : []
                }
            }
        )

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
