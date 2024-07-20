# coding=utf-8

from unittest import TestCase

from flask import Request

from ctr4ever.rest.endpoint.findenginestyles import FindEngineStyles
from ctr4ever.tests.mockmodelrepository import MockEngineStyleRepository


class FindEngineStylesTest(TestCase):

    def setUp(self):
        self.engine_style_repository = MockEngineStyleRepository()
        self.engine_style_repository.create('Speed')
        self.engine_style_repository.create('Acceleration')
        self.engine_style_repository.create('Turning')

        self.find_engine_styles_endpoint = FindEngineStyles(self.engine_style_repository)

    def test_can_find_engine_styles(self):
        request = Request.from_values()

        response = self.find_engine_styles_endpoint.handle_request(request)
        data = response.get_data()

        engine_styles = data['engine_styles']

        self.assertEqual(3, len(engine_styles))
        self.assertEqual(1, engine_styles[0]['id'])
        self.assertEqual('Speed', engine_styles[0]['name'])
        self.assertEqual(2, engine_styles[1]['id'])
        self.assertEqual('Acceleration', engine_styles[1]['name'])
        self.assertEqual(3, engine_styles[2]['id'])
        self.assertEqual('Turning', engine_styles[2]['name'])

    def test_can_find_engine_styles_filtered_by_name(self):
        request = Request.from_values(query_string='name=Speed')

        response = self.find_engine_styles_endpoint.handle_request(request)
        data = response.get_data()

        engine_styles = data['engine_styles']

        self.assertEqual(1, len(engine_styles))
        self.assertEqual('Speed', engine_styles[0]['name'])

    def test_can_find_engine_styles_filtered_by_name_not_found(self):
        request = Request.from_values(query_string='name=Drift')

        response = self.find_engine_styles_endpoint.handle_request(request)
        data = response.get_data()

        engine_styles = data['engine_styles']
        self.assertEqual(0, len(engine_styles))
