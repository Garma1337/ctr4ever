# coding=utf-8
from datetime import datetime
from unittest import TestCase

from werkzeug import Request

from ctr4ever.rest.endpoint.findplayers import FindPlayers
from ctr4ever.tests.mockmodelrepository import MockPlayerRepository


class FindPlayersTest(TestCase):

    def setUp(self):
        self.player_repository = MockPlayerRepository()

        self.player_repository.create(1, 'Garma', 'email@domain.com', 'test', '123456', True, datetime.now())
        self.player_repository.create(2, 'Dutchesss', 'email2@domain2.com', 'test2', '987654', False, datetime.now())
        self.player_repository.create(1, 'Niikasd', 'email3@domain3.com', 'test3', '123456', True, datetime.now())
        self.player_repository.create(2, 'Turismo', 'email4@domain4.com', 'test4', '987654', False, datetime.now())

        self.find_players_endpoint = FindPlayers(self.player_repository)

    def test_can_find_players(self):
        request = Request.from_values()

        response = self.find_players_endpoint.handle_request(request)
        data = response.get_data()

        pagination = data['pagination']
        players = data['players']

        self.assertEqual(4, len(players))
        self.assertEqual(1, players[0]['id'])
        self.assertEqual(1, players[0]['country_id'])
        self.assertEqual('Garma', players[0]['name'])
        self.assertEqual(True, players[0]['active'])
        self.assertEqual(2, players[1]['id'])
        self.assertEqual(2, players[1]['country_id'])
        self.assertEqual('Dutchesss', players[1]['name'])
        self.assertEqual(False, players[1]['active'])
        self.assertEqual(3, players[2]['id'])
        self.assertEqual(1, players[2]['country_id'])
        self.assertEqual('Niikasd', players[2]['name'])
        self.assertEqual(True, players[2]['active'])
        self.assertEqual(4, players[3]['id'])
        self.assertEqual(2, players[3]['country_id'])
        self.assertEqual('Turismo', players[3]['name'])
        self.assertEqual(False, players[3]['active'])

    def test_can_find_players_filtered_by_country_id(self):
        request = Request.from_values(query_string='country_id=1')

        response = self.find_players_endpoint.handle_request(request)
        data = response.get_data()

        pagination = data['pagination']
        players = data['players']

        self.assertEqual(2, len(players))
        self.assertEqual('Garma', players[0]['name'])
        self.assertEqual('Niikasd', players[1]['name'])

    def test_can_find_players_filtered_by_name(self):
        request = Request.from_values(query_string='name=Garma')

        response = self.find_players_endpoint.handle_request(request)
        data = response.get_data()

        pagination = data['pagination']
        players = data['players']

        self.assertEqual(1, len(players))
        self.assertEqual('Garma', players[0]['name'])

    def test_can_find_players_filtered_by_email(self):
        request = Request.from_values(query_string='email=email@domain.com')

        response = self.find_players_endpoint.handle_request(request)
        data = response.get_data()

        pagination = data['pagination']
        players = data['players']

        self.assertEqual(1, len(players))
        self.assertEqual('Garma', players[0]['name'])

    def test_can_find_players_filtered_by_active(self):
        request = Request.from_values(query_string='active=1')

        response = self.find_players_endpoint.handle_request(request)
        data = response.get_data()

        pagination = data['pagination']
        players = data['players']

        self.assertEqual(2, len(players))
        self.assertEqual('Garma', players[0]['name'])
        self.assertEqual('Niikasd', players[1]['name'])

    def test_can_find_players_filtered_by_inactive(self):
        request = Request.from_values(query_string='active=0')

        response = self.find_players_endpoint.handle_request(request)
        data = response.get_data()

        pagination = data['pagination']
        players = data['players']

        self.assertEqual(2, len(players))
        self.assertEqual('Dutchesss', players[0]['name'])
        self.assertEqual('Turismo', players[1]['name'])

    def test_can_find_players_paginated(self):
        request = Request.from_values(query_string='page=2')

        response = self.find_players_endpoint.handle_request(request)
        data = response.get_data()

        pagination = data['pagination']
        players = data['players']

        self.assertEqual(2, pagination['current_page'])
        self.assertEqual(20, pagination['items_per_page'])
        self.assertEqual(4, pagination['total_item_count'])

        self.assertEqual(0, len(players))

    def test_can_find_players_paginated_with_limit(self):
        request = Request.from_values(query_string='page=1&per_page=2')

        response = self.find_players_endpoint.handle_request(request)
        data = response.get_data()

        pagination = data['pagination']
        players = data['players']

        self.assertEqual(1, pagination['current_page'])
        self.assertEqual(2, pagination['items_per_page'])
        self.assertEqual(4, pagination['total_item_count'])

        self.assertEqual(2, len(players))
        self.assertEqual('Garma', players[0]['name'])
        self.assertEqual('Dutchesss', players[1]['name'])

    def test_can_find_players_paginated_with_offset(self):
        request = Request.from_values(query_string='page=2&per_page=2')

        response = self.find_players_endpoint.handle_request(request)
        data = response.get_data()

        pagination = data['pagination']
        players = data['players']

        self.assertEqual(2, pagination['current_page'])
        self.assertEqual(2, pagination['items_per_page'])
        self.assertEqual(4, pagination['total_item_count'])

        self.assertEqual(2, len(players))
        self.assertEqual('Niikasd', players[0]['name'])
        self.assertEqual('Turismo', players[1]['name'])
