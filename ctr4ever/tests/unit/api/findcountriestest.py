# coding=utf-8

from unittest import TestCase

from flask import Request

from ctr4ever.rest.endpoint.findcountries import FindCountries
from ctr4ever.tests.mockmodelrepository import MockCountryRepository


class FindCountriesTest(TestCase):

    def setUp(self):
        self.country_repository = MockCountryRepository()
        self.country_repository.create('Germany')

        self.find_countries_endpoint = FindCountries(self.country_repository)

    def test_can_find_countries(self):
        response = self.find_countries_endpoint.handle_request(Request.from_values())

        data = response.get_data()
        countries = data['countries']

        self.assertEqual(1, len(countries))
        self.assertEqual('Germany', countries[0]['name'])

    def test_can_find_countries_filtered_by_name(self):
        request = Request.from_values(query_string='name=Germany')

        response = self.find_countries_endpoint.handle_request(request)

        data = response.get_data()
        countries = data['countries']

        self.assertEqual(1, len(countries))
        self.assertEqual('Germany', countries[0]['name'])

    def test_can_find_countries_filtered_by_name_not_found(self):
        request = Request.from_values(query_string='name=France')

        response = self.find_countries_endpoint.handle_request(request)

        data = response.get_data()
        countries = data['countries']

        self.assertEqual(0, len(countries))
