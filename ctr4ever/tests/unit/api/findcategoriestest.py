# coding=utf-8

from unittest import TestCase

from flask import Config, Request

from ctr4ever.rest.endpoint.findcategories import FindCategories
from ctr4ever.services.container import Container
from ctr4ever.tests.mockmodelrepository import MockCategoryRepository


class FindCategoriesTest(TestCase):

    def setUp(self):
        self.category_repository = MockCategoryRepository()
        self.category_repository.create('Course')
        self.category_repository.create('Lap')
        self.category_repository.create('SL')

        self.container = Container()
        self.container.register('repository.category', lambda: self.category_repository)

        self.find_game_versions_endpoint = FindCategories(self.container, Config(''))

    def test_can_find_categories(self):
        request = Request.from_values()

        response = self.find_game_versions_endpoint.handle_request(request)
        data = response.get_data()

        categories = data['categories']

        self.assertEqual(3, len(categories))
        self.assertEqual(1, categories[0]['id'])
        self.assertEqual('Course', categories[0]['name'])
        self.assertEqual(2, categories[1]['id'])
        self.assertEqual('Lap', categories[1]['name'])
        self.assertEqual(3, categories[2]['id'])
        self.assertEqual('SL', categories[2]['name'])

    def test_can_find_categories_filtered_by_name(self):
        request = Request.from_values(query_string='name=Course')

        response = self.find_game_versions_endpoint.handle_request(request)
        data = response.get_data()

        categories = data['categories']

        self.assertEqual(1, len(categories))
        self.assertEqual('Course', categories[0]['name'])

    def test_can_find_categories_filtered_by_name_not_found(self):
        request = Request.from_values(query_string='name=Course (Fast Character)')

        response = self.find_game_versions_endpoint.handle_request(request)
        data = response.get_data()
