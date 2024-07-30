# coding=utf-8

from ctr4ever.models.repository.countryrepository import CountryRepository
from ctr4ever.services.validator.validator import ValidationError


class CountryValidator(object):

    def __init__(self, country_repository: CountryRepository):
        self.country_repository = country_repository

    def validate_country(self, name: str):
        self.validate_name(name)

    def validate_name(self, name: str):
        if not name:
            raise ValidationError('The country name cannot be empty.')

        existing_countries = self.country_repository.find_by(name=name)

        if len(existing_countries) > 0:
            raise ValidationError(f'A country with the name "{name}" already exists.')

    def validate_id(self, country_id: int):
        if not country_id:
            raise ValidationError('The country id cannot be empty.')

        country = self.country_repository.find_one(country_id)

        if not country:
            raise ValidationError(f'No country with the id "{country_id}" exists.')
