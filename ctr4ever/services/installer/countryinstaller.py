# coding=utf-8

from typing import List

from ctr4ever.models.country import Country
from ctr4ever.models.repository.countryrepository import CountryRepository
from ctr4ever.services.installer.installer import Installer


class CountryInstaller(Installer):

    def __init__(self, country_repository: CountryRepository):
        self.country_repository = country_repository

    def _validate_entry(self, entry):
        if not 'name' in entry or not entry['name']:
            raise ValueError('Country name is required')

        if not 'flag' in entry or not entry['flag']:
            raise ValueError('Country flag is required')

    def _parse_json(self, json_content: list[dict]) -> List[Country]:
        countries = []

        for entry in json_content:
            countries.append(Country(name=entry['name'], flag=entry['flag']))

        return countries

    def _create_entries(self, countries: List[Country]) -> None:
        for country in countries:
            result = self.country_repository.find_by(country.name)

            if len(result) > 0:
                existing_country = result[0]
                self.country_repository.update(
                    id=existing_country.id,
                    name=country.name,
                    flag=country.flag
                )
            else:
                self.country_repository.create(country.name, country.flag)
