# coding=utf-8

from unittest import TestCase

from ctr4ever.models.modelbase import ModelBase


class ModelBaseTest(TestCase):

    def setUp(self):
        self.model_base = ModelBase()

    def test_can_not_convert_to_dictionary_when_no_schema_set(self):
        dictionary = self.model_base.to_dictionary()
        self.assertEqual(dictionary, {})

    def test_can_not_convert_to_json_when_no_schema_set(self):
        json = self.model_base.to_json()
        self.assertEqual(json, '{}')
