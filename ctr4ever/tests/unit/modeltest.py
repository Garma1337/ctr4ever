# coding=utf-8

from unittest import TestCase

from ctr4ever.models.model import Model


class ModelTest(TestCase):

    def setUp(self):
        self.abstract_model = Model()

    def test_can_not_convert_to_dictionary_when_no_schema_set(self):
        dictionary = self.abstract_model.to_dictionary()
        self.assertEqual(dictionary, {})

    def test_can_not_convert_to_json_when_no_schema_set(self):
        json = self.abstract_model.to_json()
        self.assertEqual(json, '{}')
