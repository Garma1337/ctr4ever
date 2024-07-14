# coding=utf-8

from unittest import TestCase

from flask import Config, Request

from ctr4ever.rest.endpoint.findcharacters import FindCharacters
from ctr4ever.services.container import Container
from ctr4ever.tests.mockmodelrepository import MockCharacterRepository


class FindCharactersTest(TestCase):

    def setUp(self):
        self.character_repository = MockCharacterRepository()
        self.character_repository.create('Penta Penguin', 1, 'penta.png')
        self.character_repository.create('Fake Crash', 2, 'fakecrash.png')
        self.character_repository.create('N. Tropy', 3, 'ntropy.png')

        self.container = Container()
        self.container.register('repository.character', lambda: self.character_repository)

        self.find_characters_endpoint = FindCharacters(self.container, Config(''))

    def test_can_find_characters(self):
        request = Request.from_values()

        response = self.find_characters_endpoint.handle_request(request)
        data = response.get_data()

        characters = data['characters']

        self.assertEqual(3, len(characters))
        self.assertEqual(1, characters[0]['id'])
        self.assertEqual('Penta Penguin', characters[0]['name'])
        self.assertEqual('penta.png', characters[0]['icon'])
        self.assertEqual(2, characters[1]['id'])
        self.assertEqual('Fake Crash', characters[1]['name'])
        self.assertEqual('fakecrash.png', characters[1]['icon'])
        self.assertEqual(3, characters[2]['id'])
        self.assertEqual('N. Tropy', characters[2]['name'])
        self.assertEqual('ntropy.png', characters[2]['icon'])

    def test_can_find_characters_filtered_by_name(self):
        request = Request.from_values(query_string='name=Penta Penguin')

        response = self.find_characters_endpoint.handle_request(request)
        data = response.get_data()

        characters = data['characters']

        self.assertEqual(1, len(characters))
        self.assertEqual('Penta Penguin', characters[0]['name'])

    def test_can_find_characters_filtered_by_name_not_found(self):
        request = Request.from_values(query_string='name=Crash Bandicoot')

        response = self.find_characters_endpoint.handle_request(request)
        data = response.get_data()

        characters = data['characters']

        self.assertEqual(0, len(characters))
