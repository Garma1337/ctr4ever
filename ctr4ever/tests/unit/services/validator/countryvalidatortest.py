# coding=utf-8

from unittest import TestCase

from ctr4ever.services.validator.countryvalidator import CountryValidator
from ctr4ever.services.validator.validator import ValidationError
from ctr4ever.tests.mockmodelrepository import MockCountryRepository


class CountryValidatorTest(TestCase):

    def setUp(self):
        self.country_repository = MockCountryRepository()
        self.country_validator = CountryValidator(self.country_repository)

    def test_can_validate_country_name(self):
        self.country_validator.validate_name('United States')

    def test_can_not_validate_empty_country_name(self):
        with self.assertRaises(ValidationError):
            self.country_validator.validate_name('')

    def test_can_not_validate_existing_country_name(self):
        self.country_repository.create('United States', 'us.png')

        with self.assertRaises(ValidationError):
            self.country_validator.validate_name('United States')

    def test_can_validate_country_id(self):
        country = self.country_repository.create('United States', 'us.png')

        self.country_validator.validate_id(country.id)

    def test_can_not_validate_empty_country_id(self):
        with self.assertRaises(ValidationError):
            self.country_validator.validate_id(None)

    def test_can_not_validate_nonexistent_country_id(self):
        with self.assertRaises(ValidationError):
            self.country_validator.validate_id(1)
