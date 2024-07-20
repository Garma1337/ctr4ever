# coding=utf-8

from unittest import TestCase

from flask import Request

from ctr4ever.rest.endpoint.findrulesets import FindRulesets
from ctr4ever.tests.mockmodelrepository import MockRulesetRepository


class FindRulesetsTest(TestCase):

    def setUp(self):
        self.ruleset_repository = MockRulesetRepository()
        self.ruleset_repository.create('Unrestricted')
        self.ruleset_repository.create('No TPM')
        self.ruleset_repository.create('Classic')

        self.find_rulesets_endpoint = FindRulesets(self.ruleset_repository)

    def test_can_find_rulesets(self):
        request = Request.from_values()

        response = self.find_rulesets_endpoint.handle_request(request)
        data = response.get_data()

        rulesets = data['rulesets']

        self.assertEqual(3, len(rulesets))
        self.assertEqual(1, rulesets[0]['id'])
        self.assertEqual('Unrestricted', rulesets[0]['name'])
        self.assertEqual(2, rulesets[1]['id'])
        self.assertEqual('No TPM', rulesets[1]['name'])
        self.assertEqual(3, rulesets[2]['id'])
        self.assertEqual('Classic', rulesets[2]['name'])

    def test_can_find_rulesets_filtered_by_name(self):
        request = Request.from_values(query_string='name=Unrestricted')

        response = self.find_rulesets_endpoint.handle_request(request)
        data = response.get_data()

        rulesets = data['rulesets']

        self.assertEqual(1, len(rulesets))
        self.assertEqual('Unrestricted', rulesets[0]['name'])

    def test_can_find_rulesets_filtered_by_name_not_found(self):
        request = Request.from_values(query_string='name=NTSC')

        response = self.find_rulesets_endpoint.handle_request(request)
        data = response.get_data()
